# The Goal of this script is to download the NOAA OISST v2 0.25 x 0.25 degree
# SST data from NOAA PSL utilizing urllib
# SST Citation: Huang, B., C. Liu, V. Banzon, E. Freeman, G. Graham, B. Hankins,
# T. Smith, and H.-M. Zhang, 2021: Improvements of the Daily Optimum Interpolation
# Sea Surface Temperature (DOISST) Version 2.1, Journal Of Climate, 34, 2923-2939.
# doi: 10.1175/JCLI-D-20-0166.1

#IMPORTS GO HERE
import os #path/file management
from urllib.request import urlretrieve  #manages downloading files from the internet

# Paths go here
root = os.getcwd()
data_path = root + '/DATA'
SST_path = data_path + '/OISST'

# URL Base goes here
url_base = 'https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2.highres/sst.day.anom.'

# Functions go Here
'''
    Functions to ensure the proper paths exist for the downloads
'''
def create_data_folder() -> None:
    '''
        Creates the /DATA folder if it doesn't already exist
    '''

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    return None

def create_sst_folder() -> None:
    '''
        Creates the /DATA/OISST folder if it doesn't already exist
    '''

    if not os.path.exists(SST_path):
        os.mkdir(SST_path)
    
    return None

'''
    Function for the actual download request
'''
def make_download_request(year:int,download_tries:int = 0) -> None:
    '''
        Sends a download request for a specific year of data.

        year (int): The year in the range [1981-2023] you want data for
        download_tries (int): number of times the download has already been
        tried
    '''
    #limit the number of download tries to 5
    if download_tries == 5:
        raise RuntimeError("Too Many Attemps, Please Retry Later")

    #change the path
    os.chdir(SST_path)

    #check if the year input was valid
    if year < 1981 or year > 2023:
        raise ValueError("Invalid Year Input Received")

    if not os.path.isfile(f'NOAA_OISST_Anomaly_{year}.nc'):
        try:
            print(f'Downloading data for {year}.')
            urlretrieve(url_base + f'{year}.nc',f'NOAA_OISST_Anomaly_{year}.nc')
            print(f'Data downloaded for {year}.')
            os.chdir(root) #go back to root is successful
        except:
            #delete the failed download file
            if os.path.isfile(f'NOAA_OISST_Anomaly_{year}.nc'):
                os.remove(f'NOAA_OISST_Anomaly_{year}.nc')
            os.chdir(root) #go back to root if failed
            print(f'Error downloading data for {year}, retrying.')
            make_download_request(year,download_tries=download_tries+1) #retry if the request fails for some reason
    else:
        print(f"NOAA OISST Anomaly File Already Exists for {year}.")
        
    return None

def download_request_loop() -> None:
    '''
        Contains a loop to request SST data for every year between 1981 and 2022
    '''

    for yr in range(1981,2023):
        make_download_request(yr)
    
    return None

# Main function goes here
def main() -> None:
    #make the folders if they don't already exist
    create_data_folder()
    create_sst_folder()
    #now do the download requests
    download_request_loop()
    
    return None

if __name__ == "__main__":
    main()
