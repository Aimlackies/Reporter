from flask import Flask, render_template, url_for, redirect
from reporter_app.electricity_use import bp
from reporter_app import db
from reporter_app.models import User
import pandas as pd
from reporter_app.electricity_use.utils import electricity, getWeather

def call_leccyfunc():
    weather = getWeather(16, 'OWM').full_df
    temp = weather[['time', 'temp']]
    leccy_df = pd.DataFrame(columns=['Time', 'Electricity Usage (Kw)'])
    for i, time in enumerate(weather.time):
        leccy_df.loc[i] = [time, electricity(time, temp[temp.time == time])]
    return leccy_df

@bp.route('/electricity_use')
def electricity_use():
    df = call_leccyfunc()
    return render_template('electricity_use/electricity_use.html', 
                           column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)
