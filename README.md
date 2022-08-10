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

Setting up the Linux server environment
------------------------------------------------

Install pip on server:

        sudo apt update

        sudo apt install python3-pip

Install miniconda on the server (Python 3.7):

        wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.12.0-Linux-x86_64.sh

Change permission to make the bash script executable:

        chmod +x Miniconda3-py37_4.12.0-Linux-x86_64.sh

Run the installer, follow the instructions (press enter a number of times and then type yes a couple of times):

        ./Miniconda3-latest-Linux-x86_64.sh

Once miniconda is installed, create a python 3.7 environment using the below command:


        conda create -n py37 python=3.7 numpy=1.21.5 pandas=1.3.5 requests=2.28.1 scipy=1.7.3 xarray=0.20.1

Activate the newly created environment:

        conda activate py37

Installation of cdsapi requires pip, use the following command:

        pip install -I cdsapi==0.5.1

Install cfgrib library, a dependency in Xarray using the following command:

        conda install -c conda-forge cfgrib

Requirements For Using CDSAPI & Transferring Processed FIle
-----------------------------------------------------------

For running this code in linux server, create a file named:

        .cdsapirc

The content of .cdsapirc should be following:

        url: https://ads.atmosphere.copernicus.eu/api/v2
        key: <api key>

The code uploads data to a server, for this you need to create an environment variable named:

        SERVER_URL --> This should contain the url of the server where we want to push the data

Project Organization
------------------------

    ├── README.md                          <- The top-level README for developers using this project.
    │
    ├── downloaded_data                    <- The directory which stores the downloaded data from ECMWF
    │
    ├── india_coordinates                  <- The directory which stores coordinates of India
    │    │
    │    └──india_coordinates.csv          <- The CSV file containing the coordinates of India
    │
    ├── output_data                        <- The directory in which the processed data will be saved
    │
    ├── main.py                            <- The main script file containing the scraping logic
    │
    └── pre_processor.py                   <- The script for processing the downloaded data.
    