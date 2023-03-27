PM 2.5 data fetcher, source: ECMWF
------------------------------------
This script downloads data from CAMS Global Atmospheric Composition Forecasts. 

To use this code you need to have access to ECMWF.

Visit: https://ads.atmosphere.copernicus.eu/api-how-to to create an account
and get your login credentials, username and api key.

For windows server, use the following article:

        https://confluence.ecmwf.int/display/CKB/How+to+install+and+use+CDS+API+on+Windows

For linux server, use the following article:

        https://ads.atmosphere.copernicus.eu/api-how-to


Project Organization
------------------------

    ├── README.md                          <- The top-level README for developers using this project.
    │
    ├── downloaded_data                    <- The directory which stores the downloaded data from ECMWF
    │
    ├── output_data                        <- The directory in which the processed data will be saved
    │
    ├── main.py                            <- The main script file containing the scraping logic
    │
    └── utils.py                           <- The script for processing the downloaded data.
    │
    └── requirements.txt                    <- Required libraries
    │
    └── .env                               <- To set environment varriables
    
`.env` file should be of following format:

        CDS_URL=https://ads.atmosphere.copernicus.eu/api/v2
        CDS_KEY=<USER-ID>:<API-KEY>           