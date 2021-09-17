from datetime import date, datetime, timedelta
from utils import test_get_average_power
import json
import requests
from utils import call_power_API, test_get_sim_status, see_get_market_data, get_market_data
import pandas as pd
imbalance = get_market_data("imbalance")
clearout_prices = see_get_market_data("clearout-prices")
print('done')
type(imbalance)
imbalance[0]
print('done')



# imbalance_price = []
# im_response = requests.get(f'http://34.72.51.59/auction/market/imbalance')
# imbalance = json.loads(im_response.text)
# imbalance_prices = imbalance.pop('price')

url = f'http://34.72.51.59/sim/llanwrtyd-wells'
response = requests.get(url)
data = json.loads(response.text)
print(data)
# data_elements = data['elements']['AIMLAC HQ Llanwrtyd Wells']
# print(data_elements)
# print(data['elements']['AIMLAC HQ Llanwrtyd Wells']['power'])
# print('done')
#test_get_average_power()
data_names = data.pop('elements')
#PONIZEJ MAM DANE WELLS
data_names_wells=[]
data_names_wells_entries = []
temperature = []
for p_id, p_info in data_names.items():
       data_names_wells.append(p_id)
       data_names_wells_entries.append(p_info)
       if 'temperature' in p_info in data_names_wells_entries:
              temperature.append([p_info['temperature'] for p_info in data_names_wells_entries])
              del data_names_wells_entries[0]['temperature']
       else:
              continue
#print(temperature)       
print(data_names_wells)

print(data_names_wells_entries)
print('finito')
print(temperature)
#print(data_names_wells)

test_get_sim_status()
#nie dziala zle zbudowany slownik
# marketclearout = {'clearout':{
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 1, 'price': 68.67, 'volume': 845.3499999999999};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 2, 'price': 67.96000000000001, 'volume': 1288.8000000000002}   ;
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 3, 'price': 71.305, 'volume': 1323.85};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 4, 'price': 77.44999999999999, 'volume': 890.6};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 5, 'price': 71.015, 'volume': 1020.8};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 6, 'price': 72.375, 'volume': 1197.0};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 7, 'price': 78.25, 'volume': 1329.1};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 8, 'price': 80.435, 'volume': 2985.6499999999996};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 9, 'price': 73.725, 'volume': 2304.45};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 10, 'price': 85.44999999999999, 'volume': 2170.85};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 11, 'price': 96.635, 'volume': 2138.05};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 12, 'price': 105.895, 'volume': 1802.1};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 13, 'price': 106.07, 'volume': 1974.05};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 14, 'price': 102.345, 'volume': 1495.35};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 15, 'price': 92.155, 'volume': 2075.15};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 16, 'price': 81.28999999999999, 'volume': 1715.0500000000002}  ;
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 17, 'price': 83.59, 'volume': 1792.6};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 18, 'price': 84.965, 'volume': 2117.4};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 19, 'price': 88.78, 'volume': 1697.9};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 20, 'price': 78.97, 'volume': 1663.1};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 21, 'price': 71.58, 'volume': 1514.6};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 22, 'price': 67.30000000000001, 'volume': 2203.25};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 23, 'price': 66.755, 'volume': 2172.8};
# {'date': 'Sun, 20 Jun 2021 00:00:00 GMT', 'period': 24, 'price': 59.125, 'volume': 1268.25}}}

# people = {1: {'Name': 'John', 'Age': '27', 'Sex': 'Male'},
#           2: {'Name': 'Marie', 'Age': '22', 'Sex': 'Female'}}

# for p_id, p_info in people.items():
#     print("\nPerson ID:", p_id)
    
#     for key in p_info:
#         print(p_info)


# print('done')