# weather-file-generator
Generates EnergyPlus compatible weather file using [Darksky API](https://darksky.net/dev)

## darksky.py
The darksky.py file requires a Darksky API Key which should be set in a .env file (view .env.example for reference).
The file also takes in a TMY EPW file. This is used for latitude and longitude information as well as weather data that Darksky does not have.
To change the time range that the script executes on, change the range in the loop.
All of the output is put into a darksky_raw.csv file.

## interpolate.py
Darksky occasionally does not have data for certain things. To fill these in, we use pandas linear interpolation. This takes in darksky_raw.csv
The output is stored in darksky_interp.csv

## script.py
This script takes in darksky_interp and generates an EPW file called multiyear.epw
