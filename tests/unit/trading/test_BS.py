import numpy as np
import pytest
import pandas as pd
from reporter_app.trading.utils import *
from conftest import app_client, db
from sqlalchemy.sql import func

AIMLAC_CC_MACHINE = os.getenv("AIMLAC_CC_MACHINE")
assert AIMLAC_CC_MACHINE is not None
host = f"http://{AIMLAC_CC_MACHINE}"

settlementdate=(date.today()).isoformat()
@pytest.mark.parametrize("settlementdate", [settlementdate])
def test_get_predicted_load_next_day(settlementdate):

    filtered_tab=get_predicted_load_next_day(settlementdate)
    assert filtered_tab.shape==(48,3)

@pytest.mark.parametrize("datestring,expected", [("2021-01-04",(2021,1,1,4)),("2021-09-12",(2021,36,7,255))])
def test_get_wday_wk_doy(datestring,expected):
    output=get_wday_wk_doy(datestring)
    assert output==expected

filtered_tab=pd.DataFrame({"Settlement Date":["2021-01-04","2021-09-12"], "Settlement Period":[3,36],"Quantity":[23345,34456]})

processed_tab=pd.DataFrame({"Year":[2021,2021], "Week":[1,36],"Day":[1,7],"Day of Year":[4,255],"hours":[2,18],"Units(MWh)":[23345,34456]})

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


@pytest.mark.parametrize("predictedGeneration, predictedDemand, predictedPrice, surplus, posted_price", [(predictedGeneration,predictedDemand,predictedPrice, surplus, posted_price)])
def test_surplus(predictedGeneration,predictedDemand,predictedPrice, surplus,posted_price):
    '''Check if the surplus testing and posting price calculation is correct'''
    output=get_surplus_test(predictedGeneration,predictedDemand,predictedPrice)
    assert surplus.sum()==output[0].sum()
    assert output[1].sum()==posted_price.sum()
    print("Surplus tested OK")
