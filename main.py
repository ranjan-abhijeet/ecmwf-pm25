import cdsapi
import utils
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
logger = utils.get_logger()

if not os.getenv('CDS_URL') and not os.getenv('CDS_KEY'):
    raise EnvironmentError('[-] Error, please set "CDS_URL" and "CDS_KEY" environment variables')

CDS_URL = os.getenv('CDS_URL')
CDS_KEY = os.getenv('CDS_KEY')
try:
    cds_client = cdsapi.Client(url=CDS_URL, key=CDS_KEY)
    logger.info('cdsapi client instantiated')
except Exception as err:
    print(f'[-] Error: {err}')

def create_folders(list_of_folders: list=['downloaded_data', 'output_data']):
    """
    Creates the directories to store data as per the project structure.
    The function checks if the requrired directories are present in the
    current working directory, if not, they are created using the os module.
    
    Args:
    list_of_folders: (list) :List of names of folders to create or check.
    """
    for folder in list_of_folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

def download_data(
        data_download_date: str,
        lead_time: list,
        data_type: str='forecast',
        format: str='grib',
        variables_to_download: list=['particulate_matter_2.5um',],
        start_time: str='00:00',
        bounding_box: list=[38, 68, 7, 98], 
        product_name: str='cams-global-atmospheric-composition-forecasts',
        downloaded_data_home_path: str='downloaded_data',
        processed_data_home_path: str='output_data'

    ):
    logger.info(f'downloading data for {data_download_date}')
    try:
        lead_time = lead_time
        for i, lead in enumerate(lead_time):
            csv_path = f"{downloaded_data_home_path}/{data_download_date}_{lead}.csv"
            grib_path = f"{downloaded_data_home_path}/{data_download_date}_{lead}.grib"

            cds_client.retrieve(
                product_name,
                {
                    'date': data_download_date,
                    'type': data_type,
                    'format': format,
                    'variable': variables_to_download,
                    'time': start_time,
                    'leadtime_hour':lead,
                    'area': bounding_box,
                },
                grib_path)    # name of the .grib file
            
            logger.info(f'processing downloaded data for date {data_download_date} hour {int(lead)}')
            utils.grib_to_csv(grib_file_path=grib_path, csv_file_path=csv_path)
            df = utils.cleanup_dataframe(csv_file_path=csv_path)
            current_hour = f"hour_{int(lead)}"
            df.rename(columns={"pm25": current_hour}, inplace=True)
            print(df.columns)
            df[current_hour] = 1e+9 * df[current_hour]
            if i == 0:
                data = df
            else:
                df.drop(columns=['longitude', 'latitude'], inplace=True)
                data = pd.concat([data, df], axis=1)
            logger.info('processing complete')
            
            logger.info('cleaning up local files')
            utils.remove_file(parent_folder= downloaded_data_home_path, extension="grib")
            utils.remove_file(parent_folder=downloaded_data_home_path, extension="csv")
            
            logger.info(f'data downloaded for date {data_download_date} hour {int(lead)}')
        data.to_csv(f"{processed_data_home_path}/{data_download_date}.csv", index=False)
        logger.info(f'process complete, data exported for date {data_download_date}')

    except Exception as err:
        logger.exception(err)
        print('[-] Error: ')


if __name__=="__main__":
    data_download_date='2023-03-27' # Format "%Y-%m-%d"
    TYPE = 'forecast'
    data_download_format = "grib" 
    lead_time = [str(i) for i in range(24)]
    variables_to_download = ["particulate_matter_2.5um",]
    time = "00:00"
    bounding_box = [38, 68, 7, 98]
    PRODUCT = "cams-global-atmospheric-composition-forecasts"
    # path of downloaded data
    downloaded_data_home_path = "downloaded_data"
    processed_data_home_path = "output_data"
    list_of_folders = [downloaded_data_home_path, processed_data_home_path]
    
    # Calling the functions
    create_folders(
        list_of_folders=list_of_folders
        )
    download_data(
        data_download_date=data_download_date,
        lead_time=lead_time,
        data_type=TYPE,
        format=data_download_format,
        variables_to_download=variables_to_download,
        start_time=time,
        bounding_box=bounding_box,
        product_name=PRODUCT,
        downloaded_data_home_path=downloaded_data_home_path,
        processed_data_home_path=processed_data_home_path
        )