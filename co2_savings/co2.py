import requests
import os
from datetime import datetime, timedelta
import json
import sqlalchemy as db

#setup database connection
engine = db.create_engine(os.environ.get('AIMLACKIES_REPORTER_DATABASE_URL'))
connection = engine.connect()
metadata = db.MetaData()
co2_table = db.Table('co2', metadata, autoload=True, autoload_with=engine)

def co2ForTime(start):
    '''
    Lookup CO2 intensity from api.carbonintensity.org and write to database

    Parameters
    ----------
    date
        a python datetime

    Returns
    -------
    integer
        The forecast grams of CO2 per kilowatt-hour (gCO2/kWh) for the South Wales area for the 30-minute interval that includes the passed date parameter
    '''
    #Get date and format it for url
    end = start + timedelta(minutes=30) #api requires an end time as well, so add 30 minutes to the start time
    url=("https://api.carbonintensity.org.uk/regional/intensity/" + str(start.strftime("%Y-%m-%dT%H:%MZ")) + "/" + str(end.strftime("%Y-%m-%dT%H:%MZ")) + "/regionid/7")
    #print(url)

    #Fetch data from from API
    response = requests.get(url)

    #select co2 forecast from within json data
    data = response.json()
    co2Forecast = data["data"]["data"][0]["intensity"]["forecast"]

    #write to database
    query = db.insert(co2_table).values(date_time=start, co2_intensity=co2Forecast)
    ResultProxy = connection.execute(query)

    return co2Forecast

def co2Savings(dateProduced, energyProduced):
    '''
    Calculates the amount of CO2 emissions saved from the onsite renewables over the grid

    Parameters
    ----------
    float64
        The energy produced by the renewables in kWh

    date
        a python datetime for the 30-minute period in which the energy was produced

    Returns
    -------
    integer
        The grams of CO2 saved during the 30 minute period specified
    '''

    carbonIntensity = co2ForTime(dateProduced)
    emissionsSavings = carbonIntensity * energyProduced

    return emissionsSavings

co2 = co2ForTime(datetime.now())
print ("Grid CO2 intensity (gCO2/kWh):", co2)
