import numpy as np
import pytest
import pandas as pd
from utils import *



def test_get_predicted_load_next_day():
    filtered_tab=get_predicted_load_next_day()
    assert filtered_tab.shape==(48,3)

@pytest.mark.parametrize("datestring,expected", [("2021-01-04",(2021,1,1,4)),("2021-09-12",(2021,36,7,255))])
def test_get_wday_wk_doy(datestring,expected):
    output=get_wday_wk_doy(datestring)
    assert output==expected
    
filtered_tab=pd.DataFrame({"Settlement Date":["2021-01-04","2021-09-12"], "Settlement Period":[3,36],"Quantity":[23345,34456]})

processed_tab=pd.DataFrame({"Year":[2021,2021], "Week":[1,36],"Day":[5,7],"Day of Year":[4,255],"hours":[2,18],"Units(MWh)":[23345,34456]})

@pytest.mark.parametrize("filtered_tab,expected",[(filtered_tab,processed_tab)])
def test_process(filtered_tab,expected):
    output=process(filtered_tab)
    assert (output==expected).all().all()
   
@pytest.mark.parametrize("processed_tab",[(processed_tab)])
def test_prediction_model(processed_tab):
    price=prediction_model.predict(processed_tab)
    assert len(price)==2
    
predictedGeneration=np.array([ 61, 182, 147, 192, 131,  32,  58,  44, 130, 140, 191, 112,  57,
        19, 104, 196, 197,  66,  40, 166, 132, 169, 177, 184])
predictedDemand=np.array([ 92, 101,  85,  45,  63, 119,  44,  83,  93,  90, 122,  84,  22,
        95,  24,  66, 127,  41, 117, 125,  29, 120, 107, 123])
predictedPrice= np.array([69, 57, 78, 76, 43, 49, 39, 38, 55, 77, 48, 31, 43, 39, 32, 45, 46,
       54, 76, 67, 71, 39, 50, 73])
surplus=np.array([-31, 81, 62, 147, 68, -87, 14, -39, 37, 50, 69, 28, 35, -76,
                    80, 130, 70, 25, -77, 41, 103, 49, 70, 61])
posted_price=np.array([103.5,  28.5,  39. ,  38. ,  21.5,  73.5,  19.5,  57. ,  27.5,
        38.5,  24. ,  15.5,  21.5,  58.5,  16. ,  22.5,  23. ,  27. ,
       114. ,  33.5,  35.5,  19.5,  25. ,  36.5])
  
     
@pytest.mark.parametrize("predictedGeneration predictedDemand predictedPrice surplus posted_price", [predictedGeneration,predictedDemand,predictedPrice, surplus, posted_price])
def test_surplus(predictedGeneration,predictedDemand,predictedPrice, expect):
    '''Check if the surplus testing and posting price calculation is correct'''
    
    output=get_surplus_test(predictedGeneration,predictedDemand,predictedPrice)
    assert output[0].sum()==surplus.sum()
    assert output[1].sum()==posted_price.sum()
    print("Surplus tested OK")


       
def test_post_bids():
        d= post_bids()
        assert d["accepted"] == 1
        assert d["message"] == ''

def test_get_bids():
    g,_=get_bids()
    assert len(g.json()) >= 1
    
def test_get_untraded_volume():
    
    
@pytest.mark.parametrize("kind_of_data", ["imbalance",
                                           "clearout-prices"])
def test_get_market_data_wrapper(kind_of_data):
    see_get_market_data(kind_of_data)
    
  
def test_get_bids_grouping():

    # So that the bid is accepted
    applying_date = date.today() + timedelta(days=2)

    p = requests.post(url=host + "/auction/bidding/set",
                      json={
                          "key":
                          "AIMLACkies275001901",
                          "orders": [{
                              "applying_date": applying_date.isoformat(),
                              "hour_ID":13,
                              "type": "BUY",
                              "volume": "0.60",
                              "price": "30"
                          }]
                      })

    d = p.json()
    print(type(p))
    print("Posting bids:")
    print("POST JSON reply:", d)
    assert d["accepted"] == 1
    assert d["message"] == ''

    g = requests.get(url=host + "/auction/bidding/get",
                     params=dict(
                         key="AIMLACkies275001901",
                         applying_date=applying_date.isoformat(),
                     ))

    # if we run the same test twice we will have more
    assert len(g.json()) >= 1

    print("Getting bids (JSON reply):")
    for order in g.json():
        print(order)