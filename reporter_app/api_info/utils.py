import requests
from datetime import date, timedelta, datetime
import re

import os

# AIMLAC_CC_MACHINE = os.getenv("AIMLACkies275001901")
# assert AIMLAC_CC_MACHINE is not None
HOST = f"http://34.72.51.59"


def get_average_power(last_30m_start):
    g = requests.get(url=HOST + "/sim/llanwrtyd-wells/30m-average-power",
                     params=dict(
                         year=last_30m_start.year,
                         month=last_30m_start.month,
                         day=last_30m_start.day,
                         hour=last_30m_start.hour,
                         minute=last_30m_start.minute,
                     ))
    g = g.json()
    if re.match(r'^-?\d+(?:\.\d+)$', g['average power']) is not None:
        return float(g['average power'])
    else:
        return None
    
    