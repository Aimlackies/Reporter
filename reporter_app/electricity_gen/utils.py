import numpy as np
import datetime
import pandas as pd
from scipy.stats import chisquare
import pygrib
import math
from pathlib import Path
import requests
import json
import urllib.request
import http.client
from urllib.parse import urlsplit
import argparse
from scipy.interpolate import interp1d
from reporter_app.models import RealPowerReadings
from reporter_app.rse_api.utils import DEVICES
from datetime import timedelta
#import matplotlib.pyplot as plt

def call_MET_API(parameter, run='00'):
    '''
    Function to grab data from the met office API - forecast for 24 h from 00:00 the day the model    is called

    Inputs: parameter (str) - weather parameter to grab, defaults to 250_agl_temperature (t 250m
                              above ground level).
            run (str)       - choices: 00, 06, 12, 18, indicates when in the day the model
                              is run, e.g. 00 gets midnight run data, RR(default) gets most
                              recent run.

    Outputs: '{parameter}_{run}.grib' - saves grib file locally to be used by
                                        process_grib.py
    '''
    conn = http.client.HTTPSConnection("api-metoffice.apiconnect.ibmcloud.com")

    # Keys for met office registered application
    headers = {
        'X-IBM-Client-Id': "7110e796-e39a-45ed-ab25-cd4f559f16a8",
        'X-IBM-Client-Secret': "pN1gP1gR0tL5aT2rT4fY3fI8wK4vO3vP1iF7nT7iT2gF6rB7vC",
        'accept': "application/x-grib"
        }

    # Request status of data
    conn.request("GET", f"/metoffice/production/1.0.0/orders/o090637572673/latest/{parameter}_+{run}/data", headers=headers)
    res = conn.getresponse()

    # Want response 302
    print(res.status, res.reason)
    #print(f'Parameter = {parameter}')
    #print(f'Run = {run}')

    # If data exists, grab and download
    if res.status == 302:
        file_loc = res.getheader("Location")
        file_download_url = urlsplit(file_loc)
        server_host       = file_download_url.hostname
        request_path      = file_download_url.path

        # Get file data
        connection2 = http.client.HTTPSConnection(server_host)
        connection2.request("GET", request_path, headers=headers)
        response2 = connection2.getresponse()

        # Want respone 200
        print(response2.status, response2.reason)

        data = response2.read()

        dat = datetime.datetime.today().strftime('%Y-%m-%d')
        file = open(f"./temp/{dat}_{parameter}_{run}.grib", "wb")
        file.write(data)
        file.close()

        print("Grib data downloaded")


def call_OWM_API():
    api_key = 'fc48723cebd9fadfc6643d4e6f41b5c8'
    lat = 52.1051
    lon = -3.6680
    url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    data = json.loads(response.text)
    return(data)


def get_grib_data(parameter, time):
    dat = datetime.datetime.today().strftime('%Y-%m-%d')
    grib_name = grib_name = f'./temp/{dat}_{parameter}_00.grib'
    grib_file = Path(grib_name)
    if not grib_file.is_file():
        print('Downloading GRIB file')
        call_MET_API(parameter=parameter, run='00')
    grbs = pygrib.open(grib_name)
    this_grbs = grbs[time+1]
    tol = 0.01
    i = 52.1051
    j = -3.6680
    data = this_grbs.data(lat1=i-tol, lon1=j-tol, lat2=i+tol, lon2=j+tol)
    return data[0][0]


class getWeather:
    def __init__(self, source='OWM'):
        '''
        Generates and interpolates for next 5 days on initialisation, can call full df now
        '''
        self.time = self.get_time()
        self.source = source
        self.date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.data = self.get_weather()[1]
        self.full_df = self.interpolate_df()

    def get_time(self):
        '''
        Grabs time in correct format
        '''
        t = datetime.datetime.now().hour + 1
        if t < 10:
            t = f'0{t}'
        else:
            t = str(t)
        return t

    def get_weather(self, variable='all'):
        date_time = self.date + f' {self.time}:00:00'
        #print(f'Selecting data for {date_time}')
        got = False
        if self.source == 'MET':
            temp = get_grib_data('agl_temperature_250', self.time)
            w_speed = get_grib_data('agl_wind-speed_250', self.time)
            cloud = get_grib_data('atmosphere_total-cloud-cover', self.time)
            forecast = {'Temperature' : temp,
                        'Wind_speed' : w_speed,
                        'Percent_cloud' : cloud}
            if 'temp' in locals():
                got =True
            if not got:
                print('No Met office forecast available')
        elif self.source == 'OWM':
            data = call_OWM_API()
            for t in data['list']:
                if t['dt_txt'] == date_time:
                    forecast = {'Temperature' : t['main']['temp'],
                                'Wind_speed' : t['wind']['speed'],
                                'Percent_cloud' : t['clouds']['all']}
                    got = True
            if not got:
                print('No OWM forecast available, check time formatting')
            ##Initialise dataframes for each of the seperate dictionaries the OMW weather data is given in.
            dfMain = pd.DataFrame()
            dfWeath = pd.DataFrame()
            dfCloud = pd.DataFrame()
            dfWind = pd.DataFrame()
            for t in data['list']:
                #Append to each dataframe the corresponding line in the dic using 'dt_txt' as the index.
                dfMain = dfMain.append(pd.DataFrame(t['main'], index = [t['dt_txt'], ]))
                dfWeath = dfWeath.append(pd.DataFrame(t['weather'][0], index = [t['dt_txt'], ]))
                dfCloud = dfCloud.append(pd.DataFrame(t['clouds'], index = [t['dt_txt'], ]))
                dfWind = dfWind.append(pd.DataFrame(t['wind'], index = [t['dt_txt'], ]))
            #Concatenate the 4 dataframes horrizontally for one super weather dataframe. Ready for manipulation.
            df = pd.concat([dfMain, dfWeath], axis = 1)
            df = pd.concat([df, dfCloud], axis = 1)
            df = pd.concat([df, dfWind], axis = 1)
        else:
            print('source must be either "MET" or "OWM"')
        if not variable == 'all':
            forecast = forecast[variable]
        if got:
            #Returns the forecast line and full 5 days weather df.
            return forecast, df
        else:
            print('Unable to get forecast')

    def interpolate_df(self):
        # Add to this to interpolate more columns
        interpolated_columns = ['temp', 'all', 'speed']
        intdata = self.data[interpolated_columns]
        intdata.reset_index(level=0, inplace=True)
        times = intdata['index']
        interpolated_df = pd.DataFrame({})
        interpolated_df = interpolated_df.append(intdata[intdata.index < 1])
        for i in range(1, len(intdata)-2):
            d = {'temp':0, 'all':0, 'speed':0, 'index':0}
            d['index'] = times[times.index == i].values[0]
            d['index'] = [d['index'].replace(':00:00', ':30:00')]
            for col in interpolated_columns:
                thisdat = intdata[col]
                x0 = thisdat[thisdat.index == i-1].values[0]
                x1 = thisdat[thisdat.index == i].values[0]
                x2 = thisdat[thisdat.index == i+1].values[0]
                x3 = thisdat[thisdat.index == i+2].values[0]
                obs = [x0, x1, x2, x3]
                z1 = np.polyfit(np.linspace(0,1.2,4), obs, 1)
                z2 = np.polyfit(np.linspace(0,1.2,4), obs, 2)
                z3 = np.polyfit(np.linspace(0,1.2,4), obs, 3)
                f1 = np.poly1d(z1)
                f2 = np.poly1d(z2)
                f3 = np.poly1d(z3)
                f1err = chisquare(obs, f1(np.linspace(0, 1.2, 4)))[0]
                f2err = chisquare(obs, f2(np.linspace(0, 1.2, 4)))[0]
                f3err = chisquare(obs, f3(np.linspace(0, 1.2, 4)))[0]
                funcarr = [f1, f2, f3]
                function = funcarr[np.argmin([f1err, f2err, f3err])]
                int_val = function(0.6)
                d[col] = [int_val]
            this_row = pd.DataFrame(data=d)
            interpolated_df = interpolated_df.append(intdata[intdata.index==i], ignore_index=True)
            interpolated_df = interpolated_df.append(this_row, ignore_index=True)
        out_df = interpolated_df.rename(columns={'all':'cloud_percent', 'speed':'wind_speed', 'index':'time'})
        return(out_df.iloc[1:, :])

def electricity(time, weather):
    '''
    Function to calculate electricity use for a given time and temperature

    Inputs: time (str)   - time to calculate electricity use for,
                           in year-month-day hour:minute_second format
            weather (df) - dataframe of weather values from getWeather class

    Outputs: electricity (float) - value of electricity used at time (in kW)
    '''
    temp = weather[weather.time == time]
    # Determine if building is occupied

    date, hour = time.split(' ')
    yr, mn, dy = date.split('-')
    hour = hour[:5].replace(':', '.')
    weekno = datetime.date(int(yr), int(mn), int(dy)).weekday()
    office_hours = False
    weekday = False
    if weekno < 5:
        weekday = True
    if float(hour) < 18 and float(hour) > 9:
        office_hours = True
    if weekday and office_hours:
        occupied = 1
    else:
        occupied = 0

    # Temp function
    heating = np.amin([np.amax([-6*temp['temp'].values[0] + 1728.0, 0]), 120])

    electricity = 200 + (30 + heating)*occupied

    return round(electricity, 1)


def call_leccyfunc():
    '''
    Function to call electricity and construct dataframe of electricity use

    Inputs: none

    Outputs: leccy_df (df) - Dataframe of electricity use in half hour
                             intervals for next 5 days
    '''
    weather = getWeather('OWM').full_df
    temp = weather[['time', 'temp']]
    leccy_df = pd.DataFrame(columns=['Time', 'Electricity Usage (kW)'])
    for i, time in enumerate(weather.time):
        leccy_df.loc[i] = [time, electricity(time, temp[temp.time == time])]
    return leccy_df



def predict_wind_energy(df, debugPlot = False):
    #Numbers given by the wind turbine manufacturers.
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    y = [0.0, 0.0, 0.0, 0.0, 1.8, 7.7, 15.1, 24.8, 34.1, 43.9, 50.3, 54.8, 58.9, 63.5, 65.6, 66.8, 66.8, 67.2, 66.4, 66.4, 66.4, 66.4, 66.4, 66.4, 66.4, 66.4]
    #Interpolate these two arrays to get a power curve.
    #f = interp1d(x, y) #Not the best interp.
    f2 = interp1d(x, y, kind='cubic')
    xnew = np.linspace(0, 25, num=100, endpoint=True)

    #Will plot the power curve if turned on in input.
    #if(debugPlot):
    #    plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
    #    plt.legend(['data', 'linear', 'cubic'], loc='best')
    #    plt.show()

    #Calculates the wind energy using the power curve and the interpolation.
    df['windenergy'] = f2(df['wind_speed'])
    #If speed is above 25 we turn the turbine off to save damage, returning 0 energy.
    for i in range(df.shape[0]):
        if df.iloc[i]['wind_speed'] > 25:
            df.iloc[i]['windenergy'] = 0
    df['windenergy'][df['windenergy'] < 0] = 0
    return df['windenergy']



def predict_solar_energy(df, debugPlot = False):
    #These are the factors required for the sin curves. We have 7 different ones and a lookup table to show where each month maps to on the year.
    outmultfactor = np.linspace(100, 200, 7)
    inmultfactor = np.linspace(3.2, 4.5, 7)
    additionfactor = np.linspace(21, 20, 7)
    additionfactor2 = np.linspace(2, 2, 7)
    lut = [0,0,1,2,3,4,5,6,5,4,3,2,1]

    #Sin curve for the solar output.
    def sinCurve(x, oF, iF, add, add2):
        returnVal = (oF * np.sin((x-add2) / iF - add))
        if returnVal>0:
            return returnVal
        else:
            return 0

    #If debugPlot is on in the input it will plot all the sin curves. Use for debugging.
    #if(debugPlot):
    #    x = np.linspace(0, 24, 360)
    #    i = 0
    #    for fact in outmultfactor:
    #        y = [sinCurve(xs, outmultfactor[i], inmultfactor[i], additionfactor[i], additionfactor2[i]) for xs in x]
    #        plt.plot(x, y)
    #        plt.xticks(rotation=90)
    #        i = i + 1
    #    plt.show()

    #This calculates the raw solar energy according to the sin curve, and then multiplies by the cover factor to account for clouds.
    df['coverfactor'] = (100 - df['cloud_percent']*0.5)/100
    #df['timestamp'] = df.index
    df['ts'] = [datetime.datetime.strptime(t, '%Y-%m-%d  %H:%M:%S') for t in df['time']]
    df['month'] = [df.iloc[i]['ts'].month for i in range(df.shape[0])]
    df['hour'] = [df.iloc[i]['ts'].hour + (df.iloc[i]['ts'].minute/60.0) for i in range(df.shape[0])]
    df['rawEnergy'] = [ sinCurve(df.iloc[i]['hour'], outmultfactor[lut[df.iloc[i]['month']]], inmultfactor[lut[df.iloc[i]['month']]],
                                 additionfactor[lut[df.iloc[i]['month']]], additionfactor2[lut[df.iloc[i]['month']]])
                        for i in range(df.shape[0]) ]
    df['totalSolarEnergy'] = df['rawEnergy'] * df['coverfactor'] * 0.001
    return df['totalSolarEnergy']


def get_energy_gen(debugPlot = False):
    weatherObj = getWeather()
    weatherObj.interpolate_df()
    weather = weatherObj.full_df

    #Predict wind
    weather['totalSolarEnergy'] = predict_solar_energy(weather)
    #Change to 1 if you want to see the plots.
#    if(debugPlot):
#        plt.plot(weather.index, weather['speed'], 'o', weather.index, weather['windenergy'], '-')
#        plt.legend(['wind speed m/s', 'energy produced kW'], loc='best')
#        plt.xticks(rotation=90)
#        plt.show()

    #Predict solar
    weather['windenergy'] = predict_wind_energy(weather)
    #Change to 1 if you want to see the plots.
#    if(debugPlot):
#        plt.plot(weather.index, weather['rawEnergy'], 'o', weather.index, weather['totalSolarEnergy'], '-')
#        plt.legend(['maximum possible', 'total energy produced kW'], loc='best')
#        plt.xticks(rotation=90)
#        plt.show()

    return weather[['windenergy', 'totalSolarEnergy', 'time']]


def get_real_power_readings_for_times(time_list):
    """
    given a list of time stamps return a list of real power generated for wind and solar for thoes times.
    This will grab the most recent readings after each time stamp given.
    """
    real_wind_e_gen = []
    real_solar_e_gen = []
    for i in time_list:
        # get the most recent readings for all devices at site
        data = RealPowerReadings.query.filter(RealPowerReadings.date_time>i, RealPowerReadings.date_time<i+timedelta(minutes=30)).order_by(RealPowerReadings.date_time)[:len(DEVICES)]
        # if readings exist sum all devices of same type (wind and solar)
        if len(data) > 0:
            sum_wind = 0
            sum_solar = 0
            for j in data:
                if "Wind" in j.device_name:
                    sum_wind += j.power
                elif "Solar" in j.device_name:
                    sum_solar += j.power
            # Add total to list
            real_wind_e_gen.append(sum_wind/1000)  # Convert watt to Kilowatt
            real_solar_e_gen.append(sum_solar/1000)  # Convert watt to Kilowatt
        else:
            real_wind_e_gen.append(None)  # no value found, add None to skip data point in grahp
            real_solar_e_gen.append(None)    # no value found, add None to skip data point in grahp

    return real_wind_e_gen, real_solar_e_gen
