import sys
sys.path.append("../..")
import requests
from datetime import date, timedelta
from datetime import datetime as dt
import pytest
import os
# from api_call_examples import *
import json
import pandas as pd
import numpy as np
import sqlalchemy as db
import pickle
from reporter_app.models import ElecUse, Co2, ElecGen, Trading

AIMLAC_CC_MACHINE = os.getenv("AIMLAC_CC_MACHINE")
assert AIMLAC_CC_MACHINE is not None
host = f"http://{AIMLAC_CC_MACHINE}"


engine = db.create_engine(os.environ.get('AIMLACKIES_REPORTER_DATABASE_URL'))
connection = engine.connect()
metadata = db.MetaData()

# finds the table NAME defined inside models.py
trading_table=db.Table('trading', metadata, autoload=True, autoload_with=engine)
predicted_load=db.Table('predicted_load', metadata, autoload=True, autoload_with=engine)
actual_load=db.Table('actual_load', metadata, autoload=True, autoload_with=engine)

# Functions placed in execution order. Whichever function completes its task first comes first in the script

def get_predicted_load_next_day():
    api_key= "cncw84m146gcswv"
    
    base_url="https://api.bmreports.com"
    tdelta=timedelta(days=1)
    settlementdate=(date.today()+tdelta).isoformat()
    tab=pd.read_csv(f"{base_url}/BMRS/B0620/V1?ServiceType=CSV&Period=*&APIKey={api_key}&SettlementDate={settlementdate}",skiprows=4)
    filtered_tab=tab[["Settlement Date", "Settlement Period", "Quantity"]]
    filtered_tab=filtered_tab.dropna(subset=["Settlement Date"])

    
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
    print(filtered_tab.columns)
    processed_tab=pd.DataFrame()
    processed_tab=filtered_tab.get(["Year","week","wday","doy","Hour","Quantity"])
    processed_tab.columns=['Year', 'Week', 'Day', 'Day of Year', 'hours', 'Units(MWh)']
    return processed_tab
    
def prediction_model(x):
    print(os.path.abspath(os.getcwd()))
    pkl_filename= "./reporter_app/trading/model/pickle_model.pkl"
    
    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)

    predictedPrice=model.predict(x)
    return predictedPrice
    
def get_predicted_price():
    filtered_tab=get_predicted_load_next_day()
    
    processed_tab=process(filtered_tab)
    #What is the best way to normalise the data before prediction?
    # will need to create model, then load weights to the model then do the predict. Before that the model needs to be moved to a script or does it even? Probably not.
    predicted_price=prediction_model(processed_tab)
    processed_tab["Price"]=predicted_price
    
    return processed_tab

def get_gen_use(applying_date):
    # applying_date = date.today() + timedelta(days=1)
    
    predictedGeneration=ElecGen.query.filter(ElecUse.date_time==applying_date).all()
    predictedDemand=ElecUse.query.filter(ElecUse.date_time==applying_date).all()
    
    
    return predictedGeneration,predictedDemand


    
def get_surplus():
    '''Calculate the surplus or deficit in available energy and define price to post'''

    predictedPrice=get_predicted_price()    
    predictedGeneration=get_gen_use()[0]
    predictedDemand= get_gen_use()[1]
    
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
    #needs to be identical to get_surplus other than the input params
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
            
    
        
def post_bids():
    ''' 
    Post bids and report to the database table once bids posted
    Surplus and posted price supplied as numpy arrays in descending
    order(to match predicted load)
    '''
    surplus=get_surplus()[0]
    posted_price=get_surplus()[1]
    
    applying_date = date.today() + timedelta(days=1)
    for i, value in enumerate(surplus): 
        
        print("Surplus: ", surplus[i],"\n"
              ,"Price:", posted_price[i])
        print("Accessing ", host)
        print("hour", i+1)
        
        if value<0:         
            p = requests.post(url=host + "/auction/bidding/set",
                              json={
                                  "key":
                                  "AIMLACkies275001901",
                                  "orders": [{
                                      "applying_date": applying_date.isoformat(),
                                      "hour_ID": i+1,
                                      "type": "BUY",
                                      "volume": str(-1 * surplus[i]),
                                      "price": str( posted_price[i])
                                      }] 
                                  })
            # c="{}"
            # loaded_sample_json=json.loads(c)
            print(type(p))
            d = p.json()
            print("Posting bids:")
            print("POST JSON reply:", d)
            
            # query=db.insert(trading_table).values(date_time=applying_date , bid_units=-1*surplus[i],bid_price=posted_price[i])
            # connection.execute(query)
            
        elif value>0:
               # So that the bid is accepted
            
            
            p = requests.post(url=host + "/auction/bidding/set",
                              json={
                                  "key":
                                  "AIMLACkies275001901",
                                  "orders": [{
                                      "applying_date": applying_date.isoformat(),
                                      "hour_ID": i+1,
                                      "type": "SELL",
                                      "volume": str(surplus[i]),
                                      "price": str(posted_price[i])
                                      }]
                                  })
            d = p.json()
            print("Posting bids:")
            print("POST JSON reply:", d)

            # query=db.insert(trading_table).values(date_time=applying_date , bid_units=surplus[i],bid_price=posted_price[i])
            # connection.execute(query)
        
    
        else:
            print("No bids posted"  ) 
            
    return d

           
def get_bids(host):
    '''
    Queries and returns bids after buy and sell orders matched
    '''
    # Needs to run some time after 12 pm after buy and sell orders matched
    applying_date = date.today() + timedelta(days=2)
    datestring=applying_date.isoformat()
    # Report sold/bought
    g = requests.get(url=host + "/auction/bidding/get",
                 params={
                     "key":"AIMLACkies275001901",
                     "applying_date":datestring,
                 })
  
    # if we run the same test twice we will have more
    assert len(g.json()) >= 1
    
    
    print("Getting bids (JSON reply):")
    
    outcome=pd.DataFrame(g.json())
    
    return g,outcome

def get_untraded_volume(host):
        
    surplus=get_surplus()[0]
    
    agg_volume=get_bids(host)[0]
    
    untraded_volume=surplus - agg_volume
    return untraded_volume
    
def get_stuff_from_bids():
    #arrays to hold values from the response    
    bid_date= np.zeros(len(g.json()))
    bid_prices= np.zeros(len(g.json()))
    bid_volume= np.zeros(len(g.json()))
    bid_hour= np.zeros(len(g.json()))
    bid_type=[]
    
    for i, order in enumerate(g.json()):
        print(order)
        data=json.loads(order)
        bid_date[i]=data['date']
        bid_prices[i] = data["price"]
        bid_hour[i] = data["period"]
        bid_volume[i] = data["volume"] 
        bid_type.append(data["type"])

    
    listy=pd.DataFrame([bid_hour,bid_date,bid_volume]).T
    listy.columns=["period","date","volume"]
    type_list=pd.DataFrame([bid_hour,bid_type]).T
    type_list.columns=["period","type"]
    
    #hopefully this won't break because the types should all be the same
    type_df=type_list.groupby("hour").sample()
    sum_vol= listy.groupby("hour").sum()
    #Assuming only a single date returned, only either of buy or sell performed for each slot
    bid_date=bid_date[:48]
    sum_vol["date"]=bid_date
    
    cout=see_get_market_data("clearout-prices")
    
  
    bid_date1= np.zeros(len(cout.json()))
    bid_prices1= np.zeros(len(cout.json()))

    bid_type=[]
    
    #Assuming it happens in order.
    for i, order in enumerate(cout.json()):
        print(order)
        data1=json.loads(order)
        bid_date1[i]=data1['date']
        bid_prices1[i] = data1["price"]
        bid_hour1[i] = data1["period"]
        
    untraded=get_untraded(host)
    #create a pandas DF with all table elements to ensure everything can go into the same table
    
    # for i in range(48):
        # query=db.insert(trading_table).values(date_time=bid_date[i] , period=sum_vol["period"][i],
        # bid_outcome_vol=sum_vol["volume"][i], bid_outcome_price=bid_prices1[i], bid_type=type_df["type"][i],
        # volume_untraded=untraded[i])
        # connection.execute(query)
    
    return sum_vol
           
            
          


    
    
def get_imbalance():
    g = see_get_market_data("imbalance")
    
    bid_date= np.zeros(len(g.json()))
    bid_hour= np.zeros(len(g.json()))
    imbalance_prices= np.zeros(len(g.json()))
    
    for i,order in enumerate(g.json()):
        data=json.loads(order)
        bid_date[i]=data['date']
        bid_hour[i] = data["period"]
        imbalance_prices[i]=data["price"]
    d_list=[bid_date,bid_hour,imbalance_prices]
    df=pd.DataFrame(d_list).T
    df.columns=["date", "period", "Imbalance price"]
    
    return df

    
def see_get_market_data(kind_of_data):
    '''
    kind_of_data in [ "imbalance","clearout-prices" ]
    '''
    start_date = date.today() - timedelta(days=1)
    end_date = date.today() + timedelta(days=1)
    g = requests.get(url=host + f"/auction/market/{kind_of_data}",
                     params=dict(start_date=start_date.isoformat(),
                                 end_date=end_date.isoformat()))

    # Some data should be present!
    assert len(g.json()) > 0

    print(f"Getting data ({kind_of_data}):")
    print("GET JSON reply:")
    for entry in g.json():
        print(entry)
    return g
 
 


# This ain't necessary?
def dbwrite_load_next_day():

    filtered_tab=get_predicted_load_next_day()
        
    #write to database
    query=db.insert(trading_table).values(date_time=filtered_tab["Settlement Date"]
    ,period=filtered_tab["Settlement Period"],predicted_load=filtered_tab["Quantity"])
    ResultProxy = connection.execute(query)    