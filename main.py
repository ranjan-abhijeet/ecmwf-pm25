import cdsapi
import xarray as xr
import os
import pandas as pd
from datetime import datetime, timedelta
from pre_processor import extrapolator

cds_client = cdsapi.Client()

# Date from which we want the forecasts to start.
# Final query format is as per the requirement of cdsapi
query_delay = 1 # delay in query
query_date = datetime.now() - timedelta(days=query_delay)
date = query_date.strftime("%Y-%m-%d")
cds_download_date = date + "/" + date

# The data product we are using for PM 1.0, PM 2.5, and PM 10.0 forcasts
product = 'cams-global-atmospheric-composition-forecasts'

# Format of downloading data, other option is netcdf
data_download_format = 'grib' 

# Forecasted lead time in hours.. asks for queries for next 24 hours
# lead_time = [str(i) for i in range(0, 24)]
# Need to work on the logic, staying with 36th hour forecast for now
lead_time = ['36']
# Variables we want to forecast, PM 1.0, PM 2.5, and PM 10.0 in this case
forecasted_variables = [
                        # 'particulate_matter_10um',
                        'particulate_matter_2.5um',
                        # 'particulate_matter_1um'
                        ]

# Hour from which forecast is required.
time = '00:00'  # other option is '12:00'

# Bounding box for query region.. India at the moment
# [north, west, south, east]
bounding_box = [38, 68, 7, 98]

# path of downloaded data
data_path = f"downloaded_data/{date}.csv"

# path of coordinates where we want to extrapolate
india_coordinates_path = "india_coordinates/india_coordinates.csv" 

print("[+] Retrieving data from CAMS Global Atmospheric Composition Forecasts")

try:
    cds_client.retrieve(
        product,
        {
            'date': cds_download_date,
            'type': 'forecast',
            'format': data_download_format,
            'variable': forecasted_variables,
            'time': '00:00',
            'leadtime_hour':lead_time,
            'area': bounding_box,
        },
        f'downloaded_data/{date}.grib')    # name of the .grib file

    print(f"[+] Reading download {date}.grib file")
    ds = xr.open_dataset(f'downloaded_data/{date}.grib')

    print(f"[+] Converting .grib to .csv file format")
    df = ds.to_dataframe()
    df.to_csv(f'downloaded_data/{date}.csv')
    print(f"[+] Downloaded data for {date} in .csv file")

    df = pd.read_csv(data_path)
    df.drop(columns=["step", "number", "surface", "time", "valid_time"], inplace=True)
    renamed_column = {"pm2p5":"pm2.5"}
    df.rename(columns=renamed_column, inplace=True)

    output = extrapolator(df, india_coordinates_path)
    output.to_csv("output_data/pm2.5.csv", index=False)

    print("[+] Task Complete")
except Exception as err:
    print("[-] Kindly check the following: ")
    print(f"[-] {err}")