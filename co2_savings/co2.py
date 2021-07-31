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
    Looks up CO2 intensity from api.carbonintensity.org and writes to the database

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
    query = db.insert(co2_table).values(date_time=start, co2=co2Forecast)
    ResultProxy = connection.execute(query)

    return co2Forecast
    
#rounds the current time down to nearest 30 minutes (to allow for database relationship with electricity usage
now = datetime.now()
rounded = now - (now - datetime.min) % timedelta(minutes=30)

#fetch co2 intensity for the period and write to db
co2 = co2ForTime(rounded)
print ("For the 30-min time period starting:", rounded, "the grid CO2 intensity (gCO2/kWh) was:", co2)
