import requests
from datetime import date, timedelta, datetime
import re
import pandas as pd

import os

AIMLAC_CC_MACHINE = os.getenv("AIMLAC_CC_MACHINE")
AIMLAC_API_KEY = os.getenv("AIMLAC_API_KEY")
assert AIMLAC_CC_MACHINE is not None
HOST = f"http://{AIMLAC_CC_MACHINE}"


def get_device_power(generator_name):
	"""
	Given a generator name return the power currently being generated and a timestap of request
	"""
	g = requests.get(url=HOST + "/sim/llanwrtyd-wells")
	g = g.json()
	date_time = datetime.strptime(g['timedate'], '%a, %d %b %Y %H:%M:%S %Z')
	power = g['elements'][generator_name]['power']
	return {'datetime': date_time, 'power': power}


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


def post_bids(settlementdate):
	'''
	Post bids and report to the database table once bids posted
	Surplus and posted price supplied as numpy arrays in descending
	order(to match predicted load)
	'''
	surplus = get_surplus(settlementdate)[0]
	posted_price = get_surplus(settlementdate)[1]

	applying_date = date.today() + timedelta(days=1)
	for i, value in enumerate(surplus):
		if value < 0:
			p = requests.post(
				url=HOST + "/auction/bidding/set",
				json={
					"key": AIMLAC_API_KEY,
					"orders": [{
						"applying_date": applying_date.isoformat(),
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
						"applying_date": applying_date.isoformat(),
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


def get_bids():
	'''
	Queries and returns bids after buy and sell orders matched
	'''
	# Needs to run some time after 12 pm after buy and sell orders matched
	applying_date = date.today() + timedelta(days=2)
	datestring = applying_date.isoformat()
	# Report sold/bought
	g = requests.get(
		url=HOST + "/auction/bidding/get",
		params={
			"key": AIMLAC_API_KEY,
			"applying_date": datestring,
		})

	# if we run the same test twice we will have more
	assert len(g.json()) >= 1

	outcome = pd.DataFrame(g.json())

	return g, outcome


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
