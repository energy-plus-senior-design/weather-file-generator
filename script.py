import json
import os
from tqdm import tqdm
import requests
import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from pyepw.epw import EPW
epw = EPW()

from dotenv import load_dotenv
load_dotenv()

DARKSKY_API_KEY = os.getenv("DARKSKY_API_KEY")
filename="USA_TX_Austin.722540_TMY2_mod.epw"

if DARKSKY_API_KEY == None:
    print("Darksky API Key not set!")
epw.read(filename)
lat = epw.location.latitude
lon = epw.location.longitude

for y in range(2011,2019):
    filename = f'{y}_weather.epw'
    print(filename)
    with tqdm(total=8760) as pbar:
        for wd in epw.weatherdata:
            wd.year = y
            if(wd.hour == 1):
                #Convert year, month, day to UNIX time. (This uses first hour of the day since Darksky provides hourly data for that day.)
                dt = datetime(wd.year, wd.month, wd.day)
                timestamp = dt.timestamp()
                timestamp = int(timestamp)
                url = f'https://api.darksky.net/forecast/{DARKSKY_API_KEY}/{lat},{lon},{timestamp}?units=si'
                r = requests.get(url)
                if(r.status_code == requests.codes.ok):
                    r = r.json()
                else:
                    break
            try:
                wd.dry_bulb_temperature = r['hourly']['data'][wd.hour-1].get('temperature')
                pressure = r['hourly']['data'][wd.hour-1].get('pressure')
                if(pressure!=None):
                    wd.atmospheric_station_pressure = pressure*100
                wd.relative_humidity = r['hourly']['data'][wd.hour-1].get('humidity')
                wd.dew_point_temperature = r['hourly']['data'][wd.hour-1].get('dewPoint')
                wd.wind_speed = r['hourly']['data'][wd.hour-1].get('windSpeed')
            except Exception as e:
                print(e)
            time.sleep(0.1)
            pbar.update(1)
    epw.save(filename)