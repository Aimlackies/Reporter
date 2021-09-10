import requests
import os
from datetime import datetime, timedelta
import json
import sqlalchemy as db

engine = db.create_engine(os.environ.get('AIMLACKIES_REPORTER_DATABASE_URL'))
connection = engine.connect()
metadata = db.MetaData()
trading_table=db.Table('trading'. metadata, autoload=True, autoload_with=engine)


 def get_predicted_load_next_day():
    api_key= "cncw84m146gcswv"

    base_url="https://api.bmreports.com"
    tdelta=dt.timedelta(days=1)
    settlementdate=(dt.date.today()+tdelta).isoformat()
    tab=pd.read_csv(f"{base_url}/BMRS/B0620/V1?ServiceType=CSV&Period=*&APIKey={api_key}&SettlementDate={settlementdate}",skiprows=4)
    filtered_tab=tab[["Settlement Date", "Settlement Period", "Quantity"]]
    
    #write to database
    query=db.insert(trading_table).values(date_time=filtered_tab["Settlement Date"]
    ,period=filtered_tab["Settlement Period"],predicted_load=filtered_tab["Quantity"])
    ResultProxy = connection.execute(query)
    
    return filtered_tab
    