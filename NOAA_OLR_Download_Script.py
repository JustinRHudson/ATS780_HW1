# The Goal of this script is to download the NOAA Daily Interpolated OLR from
# NOAA PSL
# OLR Citation: Liebmann and Smith, Bulletin of the American Meteorological Society, 77
# 1275-1277, June 1996

#IMPORTS GO HERE
import os #path/file management
from urllib.request import urlretrieve  #manages downloading files from the internet

# Paths go here
root = os.getcwd()
data_path = root + '/DATA'

# urls go here
olr_ltm_url = 'https://downloads.psl.noaa.gov//Datasets/interp_OLR/olr.day.ltm.1981-2010.nc'
olr_daily_mean_url = 'https://downloads.psl.noaa.gov//Datasets/interp_OLR/olr.day.mean.nc'

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

'''
    Function for the actual download request
'''

def download_ltm_data(download_tries:int = 0) -> None:
    '''
        Downloads the NOAA Interpolated Daily OLR long term mean from 1981-2010
        from NOAA PSL

        download_tries (int): The number of times the download has been attempted previously
    '''

    #check if the number of download tries is below five
    if download_tries == 5:
        raise RuntimeError("Too Many Attemps, Please Retry Later")
    
    #change the path
    os.chdir(data_path)

    #try the download
    if not os.path.isfile('olr.day.ltm.1981-2010.nc'):
        try:
            print('Downloading the Long Term Mean Data.')
            urlretrieve(olr_ltm_url,'olr.day.ltm.1981-2010.nc')
            print('Long Term Mean Data Downloaded')
            os.chdir(root)
        except:
            print('Download Failed, Retrying.')
            #delete the failed download file if it exists
            if os.path.isfile('olr.day.ltm.1981-2010.nc'):
                os.remove('olr.day.ltm.1981-2010.nc')
            os.chdir(root)
            #retry with the number of download tries incremented by 1
            download_ltm_data(download_tries=download_tries+1)
    else:
        print("Long Term Mean File Already Exists")

    return None

def download_daily_data(download_tries:int = 0) -> None:
    '''
        Downloads the NOAA Interpolated Daily mean OLR from NOAA PSL

        download_tries (int): The number of times the download has been attempted previously
    '''

    #check if the number of download tries is below five
    if download_tries == 5:
        raise RuntimeError("Too Many Attemps, Please Retry Later")
    
    #change the path
    os.chdir(data_path)

    #try the download
    if not os.path.isfile('olr.day.mean.nc'):
        try:
            print('Downloading the Daily Mean OLR Data.')
            urlretrieve(olr_ltm_url,'olr.day.mean.nc')
            print('Daily Mean OLR Data Downloaded')
            os.chdir(root)
        except:
            print('Download Failed, Retrying.')
            #delete the failed download file if it exists
            if os.path.isfile('olr.day.mean.nc'):
                os.remove('olr.day.mean.nc')
            os.chdir(root)
            #retry with the number of download tries incremented by 1
            download_ltm_data(download_tries=download_tries+1)
    else:
        print("Daily Mean OLR File Already Exists")

    return None

# Main goes here
def main() -> None:
    #make sure the proper directory exists
    create_data_folder()
    #send the requests
    download_ltm_data()
    download_daily_data()

    return None

if __name__ == "__main__":
    main()