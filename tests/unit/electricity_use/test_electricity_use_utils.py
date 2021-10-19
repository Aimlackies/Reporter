from reporter_app.electricity_use.utils import electricity, call_OWM_API, getWeather, call_leccyfunc
import flask
import pandas as pd
import pytest
import numpy as np


def test_call_OWM_API_type():
    '''
    GIVEN: none (super simple test)
    WHEN: call_OWM_API is called
    THEN: function should return weather data as dict type
    '''
    d = call_OWM_API()
    assert type(d) is dict


@pytest.mark.parametrize('param, expect', [
    ([pd.DataFrame({'time': ['2021-06-30 10:30:00', 'foo'],
      'temp': [293.7, 0]}, index=[0,1]), '2021-06-30 10:30:00'], 230),
    ([pd.DataFrame({'time': '2021-06-26 12:00:00', 'temp': 281.2}, index=[0]),
      '2021-06-26 12:00:00'], 200),
])
def test_electricity(param, expect):
    '''
    GIVEN: weather dataframe and desired time to calculate
           electricity use for
    WHEN: electricity function called
    EXPECT: electricity use in kW for given time

    params:
    param: time (str) - time to calculate for
    param: weather (df) - weather temperature dataframe
    expect: electricity (float) - electricity use at given time
    '''
    weather = param[0]
    time = param[1]
    output = electricity(time, weather)
    assert output == expect


#def test_call_leccyfunc_type():
#    '''
#    GIVEN: none (super simple test)
#    WHEN: call_leccyfunc is called
#    THEN: function returns dataframe
#    '''
#    l = call_leccyfunc()
#    assert type(l.Time[0]) is str
#    assert type(l['Electricity Usage (kW)'][0]) is np.float64
