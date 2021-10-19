import sys
sys.path.append("../..")
import requests
from datetime import date, timedelta, time
from datetime import datetime
import pytest
import os
# from api_call_examples import *
import json
import pandas as pd
import numpy as np
import sqlalchemy as db
import pickle
from reporter_app.models import ElecUse, Co2, ElecGen, Trading
from reporter_app.electricity_gen.utils import get_energy_gen
from reporter_app.electricity_use.utils import call_leccyfunc
from sklearn.preprocessing import StandardScaler

# finds the table NAME defined inside models.py
# trading_table=db.Table('trading', metadata, autoload=True, autoload_with=engine)
# predicted_load=db.Table('predicted_load', metadata, autoload=True, autoload_with=engine)
# actual_load=db.Table('actual_load', metadata, autoload=True, autoload_with=engine)

# Functions placed in execution order. Whichever function completes its task first comes first in the script
tdelta = timedelta(days=1)
in_date = (date.today()+tdelta).isoformat()


load_date=(date.today()+tdelta-timedelta(days=7))
load_date=load_date.isoformat()


def get_predicted_load_next_day(in_date):
    in_date=datetime.strptime(in_date,"%Y-%m-%d")
    load_date=in_date-timedelta(days=7)
    date1=load_date.strftime("%Y-%m-%d")
    api_key= "cncw84m146gcswv"

    base_url="https://api.bmreports.com"

    tab=pd.read_csv(f"{base_url}/BMRS/B0620/V1?ServiceType=CSV&Period=*&APIKey={api_key}&SettlementDate={date1}",skiprows=4)
    filtered_tab=tab[["Settlement Date", "Settlement Period", "Quantity"]]
    filtered_tab=filtered_tab.dropna(subset=["Settlement Date"])

    # filtered_tab.to_csv(f"./{csv_name}")

    return filtered_tab


def get_wday_wk_doy(x):
    x=date.fromisoformat(x)
    year=x.isocalendar()[0]
    week=x.isocalendar()[1]
    wday=x.isocalendar()[2]
    doy=x.timetuple().tm_yday
    return year,week,wday,doy


def process(filtered_tab):
    # Ceiling division to get hour from period
    filtered_tab["Hour"]=[-(-x//2) for x in filtered_tab["Settlement Period"]]

    filtered_tab["Year"],filtered_tab["week"],filtered_tab["wday"],filtered_tab["doy"]=zip(*filtered_tab["Settlement Date"].map(get_wday_wk_doy))
    processed_tab=pd.DataFrame()
    processed_tab=filtered_tab.get(["Year","week","wday","doy","Hour","Quantity"])
    processed_tab.columns=['Year', 'Week', 'Day', 'Day of Year', 'hours', 'Units(MWh)']

    tab=processed_tab.copy()
    # Scaling BMRS data to match relative traffic through nordpool
    processed_tab.iloc[:,5]=processed_tab.iloc[:,5]/4.7

    syspath=os.path.abspath(os.getcwd())
    if syspath.endswith("reporter"):
        pkl_filename= "./reporter_app/trading/model/pickle_scaler.pkl"
    else:
        pkl_filename= "../trading/model/pickle_scaler.pkl"
    sc = pickle.load(open(pkl_filename,'rb'))

    processed=sc.transform(processed_tab)


    processed_tab.iloc[:,:]=processed

    return processed_tab,tab

def prediction_model(x):
    '''
    Takes the pickled model and uses it to predict based on the new data
    '''
    syspath=os.path.abspath(os.getcwd())

    if syspath.endswith("reporter"):
        pkl_filename= "./reporter_app/trading/model/pickle_model.pkl"
    else:
        pkl_filename= "../trading/model/pickle_model.pkl"

    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)

    predictedPrice=model.predict(x)
    return predictedPrice

def get_predicted_price(in_date):
    '''
    Returns a DataFrame with the predicted price in the "Price" column for each time period
    '''
    filtered_tab=get_predicted_load_next_day(in_date)

    processed_tab,tab=process(filtered_tab)
    #What is the best way to normalise the data before prediction?
    # will need to create model, then load weights to the model then do the predict. Before that the model needs to be moved to a script or does it even? Probably not.
    predicted_price=prediction_model(processed_tab)
    processed_tab["Price"]=predicted_price
    processed_tab["Units(MWh)"]=tab.iloc[:,5]

    return processed_tab

def next_day_filter(x,in_date):
    '''
    Filter to apply to get the right data for 24 hours
    '''

    # tdelta=timedelta(days=1)
    # applying_date=datetime.today()+tdelta
    # start_dt=datetime.combine(applying_date,time())
    start_dt=in_date+" 00:00:00"
    # if "Time" in x.columns:
    #     start_index=x[x["Time"]==start_dt.strftime("%Y-%m-%d %H:%M:%S")].index.tolist()[0]
    # elif "time" in x.columns:
    #     start_index=x[x["time"]==start_dt.strftime("%Y-%m-%d %H:%M:%S")].index.tolist()[0]
    # else:
    #     print("can't read time from energy use or generation")
    if "Time" in x.columns:
        start_index=x[x["Time"]==start_dt].index.tolist()[0]
    elif "time" in x.columns:
        start_index=x[x["time"]==start_dt].index.tolist()[0]
    else:
        print("can't read time from energy use or generation")
    end_index=start_index+48
    return x.iloc[start_index:end_index,:].reset_index(drop=True)


def get_gen_use(in_date):
    '''
    Get informtion about the predicted generation and usage. Predicts for 4 subsequent days until
    8:30 AM last day from present to future.
    '''
    ###predicts for today and 4 more days until 8:30 in the morning of the last day.
    e_use_df = call_leccyfunc()
    e_gen_df = get_energy_gen()
    ### gives the predicted gen and demand for the next 24 hours starting next 00:00
    gen=next_day_filter(e_gen_df,in_date)
    dem=next_day_filter(e_use_df,in_date)

    predictedGeneration=gen["windenergy"]+ gen["totalSolarEnergy"]
    predictedDemand=dem["Electricity Usage (kW)"]

    return predictedGeneration, predictedDemand


def get_surplus(in_date):
    '''
    Calculate the surplus or deficit in available energy and define price to post. Assuming simple case.
    '''

    predictedPrice = get_predicted_price(in_date)["Price"]
    predictedGeneration = get_gen_use(in_date)[0]
    predictedDemand = get_gen_use(in_date)[1]

    if len(predictedPrice)<len(predictedGeneration):
        predictedGeneration=predictedGeneration[:len(predictedPrice)]
        predictedDemand=predictedDemand[:len(predictedPrice)]

    if len(predictedGeneration) == 0 and len(predictedDemand) == 0 :
        surplus = []
    else:
        surplus=predictedGeneration-predictedDemand

    posted_price=np.zeros(len(predictedPrice))

    for i,difference in enumerate(surplus):
        if difference >0:
            # Minimum price willing to accept
            posted_price[i]=predictedPrice[i]*0.5

        else:
            # Maximum price willing to pay
            posted_price[i]= predictedPrice[i]*1.5


    return surplus,posted_price


def get_surplus_test(predictedGeneration, predictedDemand, predictedPrice):
    '''
    To test calculation of the surplus or deficit in available energy and define price to post

    '''
    # needs to be identical to get_surplus other than the input params
    surplus = predictedGeneration - predictedDemand
    posted_price = np.zeros(len(predictedPrice))

    for i, difference in enumerate(surplus):
        if difference > 0:
            # Minimum price willing to accept
            posted_price[i] = predictedPrice[i] * 0.5

        else:
            # Maximum price willing to pay
            posted_price[i] = predictedPrice[i] * 1.5

    return surplus, posted_price
