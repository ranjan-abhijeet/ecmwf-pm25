import cdsapi
import utils
import os
import pandas as pd
import xarray as xr
from datetime import datetime, timedelta
from pre_processor import extrapolator
from dotenv import load_dotenv


load_dotenv()

logger = utils.get_logger()
CDS_URL = os.getenv('CDS_URL')
CDS_KEY = os.getenv('CDS_KEY')
cds_client = cdsapi.Client(url=CDS_URL, key=CDS_KEY)
logger.info('cdsapi client instantiated')

# cds_download_date = date + "/" + date
date = "2022-11-07"
cds_download_date = date + "/" + date
logger.info(f'downloading data for {cds_download_date}')

# The data product we are using for PM 1.0, PM 2.5, and PM 10.0 forcasts
PRODUCT = "cams-global-atmospheric-composition-forecasts"
# Type of data which needs to be fetched
TYPE = 'forecast'

# Format of downloading data, other option is netcdf
data_download_format = "grib" 

# Forecasted lead time in hours.. asks for for next forecast for current day's 12 hours
lead_time = ["14"]
# lead_time = [str(i) for i in range(1)]
# Variables we want to forecast, PM 1.0, PM 2.5, and PM 10.0 in this case
forecasted_variables = [
                        "particulate_matter_2.5um",
                        ]

# Hour from which forecast is required.
time = "00:00"  # other option is '12:00'

# Bounding box for query region.. India for this context
# [north, west, south, east] latitudes and longitudes
bounding_box = [38, 68, 7, 98]

# path of downloaded data
data_download_home_path = "downloaded_data"
interpolated_data_home_path = "output_data"

# path of coordinates where we want to extrapolate
india_coordinates_path = "india_coordinates/india_coordinates.csv" 


def download_data():
    try:
        data = pd.read_csv(india_coordinates_path)
        for lead in lead_time:
            csv_path = f"{data_download_home_path}/{date}_{lead}.csv"
            grib_path = f"{data_download_home_path}/{date}_{lead}.grib"

            cds_client.retrieve(
                PRODUCT,
                {
                    'date': cds_download_date,
                    'type': TYPE,
                    'format': data_download_format,
                    'variable': forecasted_variables,
                    'time': time,
                    'leadtime_hour':lead,
                    'area': bounding_box,
                },
                grib_path)    # name of the .grib file
            
            logger.info(f'processing downloaded data for date {date} hour {int(lead)}')
            utils.grib_to_csv(grib_file_path=grib_path, csv_file_path=csv_path)
            df = utils.cleanup_dataframe(csv_file_path=csv_path)
            output = extrapolator(df, india_coordinates_path)
            output.rename(columns={"pm25": f"hour_{int(lead)}"}, inplace=True)
            data = pd.concat([data, output], axis=1)
            logger.info('processing complete')
            
            logger.info('cleaning up local files')
            utils.remove_file(parent_folder= "downloaded_data", extension="grib")
            utils.remove_file(parent_folder="downloaded_data", extension="csv")
            
            logger.info(f'data downloaded for date {date} hour {int(lead)}')
        data.to_csv(f"{interpolated_data_home_path}/{date}.csv", index=False)
        logger.info(f'process complete, data exported for date {date}')

    except Exception as err:
        logger.exception(err)
        print('[-] Error')


if __name__=="__main__":
    download_data()