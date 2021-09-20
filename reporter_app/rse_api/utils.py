from datetime import date, timedelta, datetime
import json
import numpy as np
import os
import pandas as pd
import re
import requests
from reporter_app.trading.utils import get_surplus
import sys
sys.path.append("../..")



AIMLAC_CC_MACHINE = os.getenv("AIMLAC_CC_MACHINE")
AIMLAC_API_KEY = "AIMLACkies275001901" #os.getenv("AIMLAC_API_KEY") ##for some reason this was playing up
assert AIMLAC_CC_MACHINE is not None
HOST = f"http://{AIMLAC_CC_MACHINE}"

def get_device_power(generator_name):
	"""
	Given a generator name return the power currently being generated and a timestap of request
	"""
	g = requests.get(url=HOST + "/sim/llanwrtyd-wells")
	g = g.json()
	date_time = datetime.strptime(g['timedate'], '%a, %d %b %Y %H:%M:%S %Z')
	site=[generator_name]
	power = g['elements'][generator_name]['power']
	return {"site": site,'datetime': date_time, 'power': power}

#print(get_device_power("Llanwrtyd Wells - Wind Generator 1"))
#print("done")
def get_site_info():
	"""
	return current power, temperature and request time at the HQ
	"""
	g = requests.get(url=HOST + "/sim/llanwrtyd-wells")
	g = g.json()
	temperature = g['elements']['AIMLAC HQ Llanwrtyd Wells']['temperature']
	power = g['elements']['AIMLAC HQ Llanwrtyd Wells']['power']
	date_time = datetime.strptime(g['timedate'], '%a, %d %b %Y %H:%M:%S %Z')
	return {'datetime': date_time, 'power': power, 'temperature': temperature}

tdelta = timedelta(days=2)
in_date = (date.today()+tdelta).isoformat()

def post_bids(in_date):
	'''
	Post bids and report to the database table once bids posted
	Surplus and posted price supplied as numpy arrays in descending
	order(to match predicted load)
	'''
	surplus = get_surplus(in_date)[0]
	posted_price = get_surplus(in_date)[1]
   
    
	
	for i, value in enumerate(surplus):
		if value < 0:
			p = requests.post(
				url=HOST + "/auction/bidding/set",
				json={
					"key": AIMLAC_API_KEY,
					"orders": [{
						"applying_date": in_date,
						"hour_ID": i+1,
						"type": "BUY",
						"volume": str(-1 * surplus[i]),
						"price": str( posted_price[i])
					}]
				}
			)
			d = p.json()
			print("Posting bids:")
			print("POST JSON reply:", d)
		elif value>0:
			# So that the bid is accepted
			p = requests.post(
				url=HOST + "/auction/bidding/set",
				json={
					"key": AIMLAC_API_KEY,
					"orders": [{
						"applying_date": in_date,
						"hour_ID": i + 1,
						"type": "SELL",
						"volume": str(surplus[i]),
						"price": str(posted_price[i])
					}]
				}
			)
			d = p.json()
		# No bids posted
		else:
			return None

	return d


def get_bids(in_date):
	'''
	Queries and returns bids after buy and sell orders matched
	'''
	# Needs to run some time after 12 pm after buy and sell orders matched
	
	#Report sold/bought
	g = requests.get(
		url=HOST + "/auction/bidding/get",
		params={
			"key": AIMLAC_API_KEY,
			"applying_date": in_date,
		})

	# if we run the same test twice we will have more
	assert g.headers["content-type"].strip().startswith("application/json")==True
	assert len(g.json()) >= 1

	outcome = pd.DataFrame(g.json()) 
	outcome.iloc[:,1]=outcome["applying_date"].map(map_date_format)
    
	return outcome    

def split_outcome(in_date):
	outcome=get_bids(in_date)    
	bids_accepted=outcome[outcome["accepted"].notnull()]
	bids_ignored=outcome[outcome["accepted"].isnull()]
   # returns a series object with hour ID as index in ascending order
	volume=outcome.groupby(["hour_ID"]).sum()["volume"]

	return bids_accepted,bids_ignored, volume

def map_date_format(x):
    x=datetime.strptime(x, "%a, %d %b %Y %H:%M:%S %Z")
    x=datetime.strftime(x, "%Y-%m-%d %H:%M:%S")
    return x
    
    

def see_get_market_data(kind_of_data):
	'''
	kind_of_data in [ "imbalance","clearout-prices" ]
	'''
	start_date = date.today() - timedelta(days=1)
	end_date = date.today() + timedelta(days=1)
	g = requests.get(
		url=HOST + f"/auction/market/{kind_of_data}",
		params=dict(
			start_date=start_date.isoformat(),
			end_date=end_date.isoformat()
		)
	)

	# Some data should be present!
	assert len(g.json()) > 0

	return g

def get_clearout():
    clearout=pd.DataFrame(see_get_market_data("clearout-prices").json()) # returns clearout prices for the day in hours 
    clearout.iloc[:,0]=clearout["date"].map(map_date_format) 
    clear=clearout.append(clearout).reset_index(drop=True)
    clear.iloc[:,1]=np.array(clear["period"].index.tolist())+1
    
    return clear

def get_untraded_volume(in_date):

    surplus=get_surplus(in_date)[0]

    agg_volume=get_bids(in_date)[3]
    
    if len(agg_volume)<len(surplus):
        agg_volume=agg_volume[:len(surplus)]
    
    #hour_IDs will be in ascending order
    untraded_volume=surplus - agg_volume
    
    return untraded_volume

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
