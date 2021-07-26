import requests
from datetime import date, timedelta, datetime
import pytest
import os
from api_call_examples import *
import json
import pandas as pd
import numpy as np

AIMLAC_CC_MACHINE = os.getenv("AIMLAC_CC_MACHINE")
assert AIMLAC_CC_MACHINE is not None
host = f"http://{AIMLAC_CC_MACHINE}"



        
def post_bids(surplus,posted_price,host):
    applying_date = date.today() + timedelta(days=2)
    for i, value in enumerate(surplus): 
        
        print("Surplus: ", surplus[i],"\n"
              ,"Price:", posted_price[i])
        print("Accessing ", host)
        print("hour", i+1)
        if value<0:
            # So that the bid is accepted
            
            
    
            p = requests.post(url=host + "/auction/bidding/set",
                              json={
                                  "key":
                                  "AIMLACkies275001901",
                                  "orders": [{
                                      "applying_date": applying_date.isoformat(),
                                      "hour_ID": i+1,
                                      "type": "BUY",
                                      "volume": str(-1* surplus[i]),
                                      "price": str( posted_price[i])
                                      }] 
                                  })
            # c="{}"
            # loaded_sample_json=json.loads(c)
            print(type(p))
            d = p.json()
            print("Posting bids:")
            print("POST JSON reply:", d)
            assert d["accepted"] == 1
            assert d["message"] == ''
            
            
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
            assert d["accepted"] == 1
            assert d["message"] == ''
        else:
            print("No bids posted"  )  
    
        
   
     
            
def get_surplus(predictedGeneration, predictedDemand,predictedPrice):
    '''Calculate the surplus or deficit in available energy and define price to post'''
    
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
            
def get_bids(host):
    '''Collect accepted bids'''
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
    for order in g.json():
        print (order)

    
    bids=pd.DataFrame(g.json())
    print(bids.head(5))
  
    # need to filter out the time
    agg_volume=bids.groupby(2).sum()
    agg_prices=bids.groupby(5).mean() #this should be fine assuming closing price for all bids is same every hour
    
    return agg_volume,agg_prices
            
            
            
def get_untraded(surplus,host):
    agg_volume=get_bids(host)[0]
    untraded=surplus- agg_volume
    return untraded
    
def get_imbalance_prices(host):
    '''Needs to run some time after 12 pm after buy and sell orders matched
    '''
    # Report sold/bought
    g = requests.get(url=host + "/live/prices/get",
                 params=dict(
                     key="AIMLACkies275001901",
                     applying_date=date.today().isoformat(),
                 ))

    # if we run the same test twice we will have more
    assert len(g.json()) >= 1

    print("Getting bids (JSON reply):")
    
    #lets assume returned order is exactly in same format as post
    #create a dictionary with volume and price
    bid_prices= np.zeros(len(g.json()))
    bid_volume= np.zeros(len(g.json()))
    bid_hour= np.zeros(len(g.json()))
    bid_type=[]
    
    for i, order in enumerate(g.json()):
        print(order)
        data=json.loads(order)
        bid_prices[i] = data["price"]
        bid_hour[i] = data["hour_ID"]
        bid_volume[i] = data["volume"] 
        bid_type.append(data["type"])
    
    bids= pd.DataFrame(zip(bid_hour,bid_volume))
    all_prices=pd.DataFrame(zip(bid_hour,bid_prices))
    agg_volume=bids.groupby(0).sum()
    agg_prices=bids.groupby(0).mean()

    
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
 
    
    