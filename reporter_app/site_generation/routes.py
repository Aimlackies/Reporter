#ggg
from flask import Flask, render_template, url_for, redirect
from reporter_app.site_generation import bp
from reporter_app import db
from reporter_app.models import User
import pandas as pd
from reporter_app.site_generation.utils import test_get_average_power, test_get_sim_status, see_get_market_data, test_set_and_get_bids
#do I need this security thing???
from flask_security import auth_required, roles_required
rezult = test_set_and_get_bids(2000)
print(rezult)

def auction_bidding_accepted():
    bids = 
    
# def call_leccyfunc():
#     weather = getWeather(16, 'OWM').full_df
#     temp = weather[['time', 'temp']]
#     leccy_df = pd.DataFrame(columns=['Time', 'Electricity Usage (Kw)'])
#     for i, time in enumerate(weather.time):
#         leccy_df.loc[i] = [time, electricity(time, temp[temp.time == time])]
#     return leccy_df



# @bp.route('/electricity_use')
# @auth_required("token", "session")
# @roles_required('verified')
# def electricity_use():
#     df = call_leccyfunc()
#     return render_template('electricity_use/electricity_use.html',
#                            column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)
