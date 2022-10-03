import cdsapi
import utils
import pandas as pd
import xarray as xr
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
product = "cams-global-atmospheric-composition-forecasts"

# Format of downloading data, other option is netcdf
data_download_format = "grib" 

# Forecasted lead time in hours.. asks for queries for next 24 hours
# lead_time = [str(i) for i in range(0, 24)]
# Need to work on the logic, staying with 36th hour forecast for now
lead_time = ["36"]
# Variables we want to forecast, PM 1.0, PM 2.5, and PM 10.0 in this case
forecasted_variables = [
                        # 'particulate_matter_10um',
                        "particulate_matter_2.5um",
                        # 'particulate_matter_1um'
                        ]

# Hour from which forecast is required.
time = "00:00"  # other option is '12:00'

# Bounding box for query region.. India at the moment
# [north, west, south, east]
bounding_box = [38, 68, 7, 98]

# path of downloaded data
csv_path = f"downloaded_data/{date}.csv"
grib_path = f"downloaded_data/{date}.grib"
interpolated_csv_path = "output_data/pm2.5.csv"

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
        grib_path)    # name of the .grib file
    
    print(f"[+] Processing data")
    utils.grib_to_csv(grib_file_path=grib_path, csv_file_path=csv_path)
    df = utils.cleanup_dataframe(csv_file_path=csv_path)
    output = extrapolator(df, india_coordinates_path)
    output.to_csv(interpolated_csv_path, index=False)

    print("[+] Cleaning up")
    utils.remove_file(parent_folder= "downloaded_data", extension="grib")
    utils.remove_file(parent_folder="downloaded_data", extension="csv")
    print("[+] Task complete")
    
except Exception as err:
    print("[-] Kindly check the following: ")
    print(f"[-] {err}")