#!/usr/bin/env python3
#wybierz prawidlowe srodowisko aimlacReporter:conda w pythonie 
import requests
from datetime import date, timedelta, datetime
import pytest
import os


AIMLAC_CC_MACHINE = os.getenv("AIMLACkies275001901")
#assert AIMLAC_CC_MACHINE is not None
host = f"http://34.72.51.59"

def test_set_and_get_bids():

    # So that the bid is accepted
    applying_date = date.today() + timedelta(days=2)

    p = requests.post(url=host + "/auction/bidding/set",
                      json={
                          "key":
                          "TESTKEY",
                          "orders": [{
                              "applying_date": applying_date.isoformat(),
                              "hour_ID": 15,
                              "type": "BUY",
                              "volume": "0.60",
                              "price": "30"
                          }]
                      })

    d = p.json()
    print("Posting bids:")
    print("POST JSON reply:", d)
    assert d["accepted"] == 1
    assert d["message"] == ''

    g = requests.get(url=host + "/auction/bidding/get",
                     params=dict(
                         key="TESTKEY",
                         applying_date=applying_date.isoformat(),
                     ))

    # if we run the same test twice we will have more
    assert len(g.json()) >= 1

    print("Getting bids (JSON reply):")
    for order in g.json():
        print(order)
print("Finished")

@pytest.mark.parametrize("kind_of_data", ["imbalance",
                                           "clearout-prices"])
def test_get_market_data_wrapper(kind_of_data):
    see_get_market_data(kind_of_data)


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


def test_get_sim_status():
    g = requests.get(url=host + "/sim/llanwrtyd-wells")

    assert len(g.json()) > 0
    print("Getting sim status:")
    print("GET JSON reply:", g.json())


def test_get_average_power():
    last_30m_start = datetime.now() - timedelta(minutes=30)
    g = requests.get(url=host + "/sim/llanwrtyd-wells/30m-average-power",
                     params=dict(
                         year=last_30m_start.year,
                         month=last_30m_start.month,
                         day=last_30m_start.day,
                         hour=last_30m_start.hour,
                         minute=last_30m_start.minute,
                     ))

    print("Getting average power:")
    assert "average power" in g.json()
    print("GET JSON reply:", g.json())


def main():
    test_set_and_get_bids()
    see_get_market_data("clearout-prices")
    see_get_market_data("imbalance")
    test_get_sim_status()
    test_get_average_power()

