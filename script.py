import os
from tqdm import tqdm
import copy
import csv
from pyepw.epw import EPW

tmy_epw = EPW()
multi_epw = EPW()

tmy_filename="USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"
multi_filename='multiyear.epw'

tmy_epw.read(tmy_filename)
lat = tmy_epw.location.latitude
lon = tmy_epw.location.longitude

multi_epw = copy.deepcopy(tmy_epw)
multi_epw.weatherdata = []

with open('darksky_interp.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for row in tqdm(reader):
        day = int(row[0])%8760
        wd = tmy_epw.weatherdata[day]
        new_wd = copy.deepcopy(wd)
        new_wd.year = row[2]
        new_wd.dry_bulb_temperature = row[6]
        new_wd.atmospheric_station_pressure = int(float(row[7]))
        new_wd.relative_humidity = float(row[8]) * 100
        new_wd.dew_point_temperature = row[9]
        new_wd.wind_speed = row[10]
        multi_epw.add_weatherdata(new_wd)

# for y in range(2011,2013):
#     print(y)
#     with tqdm(total=8760) as pbar:
#         for wd in tmy_epw.weatherdata:
#             new_wd = copy.deepcopy(wd)
#             new_wd.year = y
#             new_wd.dry_bulb_temperature = r['hourly']['data'][wd.hour-1].get('temperature')
#             pressure = r['hourly']['data'][wd.hour-1].get('pressure')
#             if(pressure!=None):
#                 new_wd.atmospheric_station_pressure = pressure*100
#             new_wd.relative_humidity = r['hourly']['data'][wd.hour-1].get('humidity')
#             new_wd.dew_point_temperature = r['hourly']['data'][wd.hour-1].get('dewPoint')
#             new_wd.wind_speed = r['hourly']['data'][wd.hour-1].get('windSpeed')
#             multi_epw.add_weatherdata(new_wd)
#     pbar.update(1)
multi_epw.save(multi_filename)