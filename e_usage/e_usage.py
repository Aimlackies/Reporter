import requests
import os
from datetime import datetime, timedelta
import json
import sqlalchemy as db
from reporter_app.electricity_use.utils import call_leccyfunc

#setup database connection
engine = db.create_engine(os.environ.get('AIMLACKIES_REPORTER_DATABASE_URL'))
connection = engine.connect()
metadata = db.MetaData()
e_use_table = db.Table('e_use', metadata, autoload=True, autoload_with=engine)

#grab data
e_use_df = call_leccyfunc()

#write to database
for idx, row in e_use_df.iterrows():
    query = db.insert(e_use_table).values(date_time=row['Time'],
            electricity_use=row['Electricity Usage (kW)'])
    ResultProxy = connection.execute(query)
