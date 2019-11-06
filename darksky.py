from dotenv import load_dotenv
import json
import os
from tqdm import tqdm
import requests
import time
import copy

from datetime import datetime
from datetime import timezone
from datetime import timedelta
from pyepw.epw import EPW
import pandas as pd
import numpy as np

df = pd.DataFrame()
tmy_epw = EPW()

load_dotenv()

DARKSKY_API_KEY = os.getenv("DARKSKY_API_KEY")
tmy_filename = "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"

if DARKSKY_API_KEY == None:
    print("Darksky API Key not set!")

tmy_epw.read(tmy_filename)
lat = tmy_epw.location.latitude
lon = tmy_epw.location.longitude

for y in range(2009, 2020):
    print(y)
    with tqdm(total=8760) as pbar:
        for wd in tmy_epw.weatherdata:
            if(wd.hour == 1):
                # Convert year, month, day to UNIX time. (This uses first hour of the day since Darksky provides hourly data for that day.)
                dt = datetime(y, wd.month, wd.day)
                timestamp = dt.timestamp()
                timestamp = int(timestamp)

                # url = f'https://api.darksky.net/forecast/fake/{lat},{lon},{timestamp}?units=si'
                url = f'https://api.darksky.net/forecast/{DARKSKY_API_KEY}/{lat},{lon},{timestamp}?units=si'
                r = requests.get(url)
                if(r.status_code == requests.codes.ok):
                    r = r.json()
                else:
                    print("Darksky Request Failed!")
                    break
            try:
                dry_bulb_temperature = r['hourly']['data'][wd.hour-1].get('temperature')
            except Exception as e:
                dry_bulb_temperature = np.nan
            try:
                pressure = r['hourly']['data'][wd.hour-1].get('pressure')
                pressure = pressure*100
            except Exception as e:
                pressure = np.nan
            try:
                relative_humidity = r['hourly']['data'][wd.hour - 1].get('humidity')
            except Exception as e:
                relative_humidity = np.nan
            try:
                dew_point_temperature = r['hourly']['data'][wd.hour-1].get('dewPoint')
            except Exception as e:
                dew_point_temperature = np.nan
            try:
                wind_speed = r['hourly']['data'][wd.hour-1].get('windSpeed')
            except Exception as e:
                wind_speed = np.nan
            df2 = pd.DataFrame([[y, wd.month, wd.day, wd.hour, dry_bulb_temperature, pressure, relative_humidity, dew_point_temperature, wind_speed]], columns=['Year', 'Month', 'Day', 'Hour', 'Temperature', 'Pressure', 'Humidity', 'Dew Point', 'Wind Speed'])
            df = df.append(df2, ignore_index=True)
            # time.sleep(0.1)
            pbar.update(1)
df.to_csv('darksky_raw.csv')
