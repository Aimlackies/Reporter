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
from reporter_app.models import RealPowerReadings, RealSiteReadings
from datetime import timedelta


# list of site power devices [name, 2 if power user else 1 if solar else 0 if wind]
DEVICES = [
	["Llanwrtyd Wells - Computing Centre", 2],
	["Llanwrtyd Wells - Solar Generator", 1],
	["Llanwrtyd Wells - Wind Generator 1", 0],
	["Llanwrtyd Wells - Wind Generator 2", 0],
	["Llanwrtyd Wells - Wind Generator 3", 0],
	["Llanwrtyd Wells - Wind Generator 4", 0],
	["Llanwrtyd Wells - Wind Generator A", 0],
	["Llanwrtyd Wells - Wind Generator B", 0]
]


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


def get_real_power_usage_for_times(time_list):
    """
    given a list of time stamps return a list of real power usage for the site.
    This will grab all the reading in a half an hour window and average them.
    """
    filter_devices = [device[0] for device in DEVICES if device[1] == 2]

    real_power_usage = []
    for i in time_list:
        # get the most recent readings in time window for devices in list
        data = RealPowerReadings.query.filter(RealPowerReadings.date_time>i, RealPowerReadings.date_time<i+timedelta(minutes=30), RealPowerReadings.device_name.in_(filter_devices)).all()
        site_data = RealSiteReadings.query.filter(RealSiteReadings.date_time>i, RealSiteReadings.date_time<i+timedelta(minutes=30)).all()
        # if readings exist get average power
        if (len(data) > 0) or (len(site_data) > 0):
            sum = 0
            sum_site = 0
            for j in data:
                sum += abs(j.power)
            for j in site_data:
                sum_site += abs(j.power)
            sum = sum / len(data)
            sum_site = sum_site / len(site_data)
            # Add total to list
            real_power_usage.append((sum + sum_site) / 1000)  # Convert watt to Kilowatt
        else:
            real_power_usage.append(None)  # no value found, add None to skip data point in graph

    return real_power_usage
