import numpy as np
import pytest
from Bid_sell import BS



@pytest.mark.parametrize("predictedGeneration predictedDemand predictedPrice expect", [
    (np.array([ 61, 182, 147, 192, 131,  32,  58,  44, 130, 140, 191, 112,  57,
        19, 104, 196, 197,  66,  40, 166, 132, 169, 177, 184])),
                         (np.array([ 92, 101,  85,  45,  63, 119,  44,  83,  93,  90, 122,  84,  22,
        95,  24,  66, 127,  41, 117, 125,  29, 120, 107, 123])),
                         (np.array([69, 57, 78, 76, 43, 49, 39, 38, 55, 77, 48, 31, 43, 39, 32, 45, 46,
       54, 76, 67, 71, 39, 50, 73])),
        (np.array([-31, 81, 62, 147, 68, -87, 14, -39, 37, 50, 69, 28, 35, -76,
                    80, 130, 70, 25, -77, 41, 103, 49, 70, 61]),
          np.array([103.5,  28.5,  39. ,  38. ,  21.5,  73.5,  19.5,  57. ,  27.5,
        38.5,  24. ,  15.5,  21.5,  58.5,  16. ,  22.5,  23. ,  27. ,
       114. ,  33.5,  35.5,  19.5,  25. ,  36.5]))
                                                                            ])
def test_surplus(predictedGeneration,predictedDemand,predictedPrice, expect):
    '''Check if the surplus testing and posting price calculation is correct'''
    
    bid=BS(predictedGeneration,predictedDemand,predictedPrice)
    output=bid.get_surplus()
    assert output[0].sum()==expect[0].sum()
    assert output[1].sum()==expect[1].sum()
    print("Surplus tested OK")

# predictedGeneration=np.random.randint(10,200,24),
#                          predictedDemand=np.random.randint(20,150,24),
#                          predictedPrice=np.random.randint(30,80,24)

# Playing around with Git to get a  better feel for it
@pytest.mark.parametrize("kind_of_data", ["imbalance",
                                           "clearout-prices"])
def test_get_market_data_wrapper(kind_of_data):
    see_get_market_data(kind_of_data)
    
    
def test_set_and_get_bids():

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