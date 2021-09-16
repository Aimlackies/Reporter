import requests
from datetime import date, timedelta, datetime
import re

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
