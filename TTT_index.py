# The goal of this script is to process the NOAA PSL Daily Interpolated OLR
# into my modified version of the Ratna et al. 2013 Index

# IMPORTS GO HERE
import numpy as np #array functionality and mathmatical operators
import matplotlib.pyplot as plt #plot creations
from PIL import Image #GIF creation
from netCDF4 import Dataset #.nc file handling
import os #path/file management
import shutil #file/path deletion
import datetime as dt #date management
import numpy.ma as ma #masked array management, common with .nc files

# Paths Go Here
root = os.getcwd()
figure_path = root + '/FIGURES'
data_path = root + '/DATA'

#file names go here
OLR_file = 'olr.day.mean.nc'
OLR_clim = 'olr.day.ltm.1981-2010.nc'
ttt_index_file = 'TTT_Index.csv'

# Functions Go Here
'''
    Functions to handle folder validation, creation, and deletion
'''
def create_folder(folder_path:str,folder_name:str,move_to_folder:bool = False) -> None:
    '''
        Creates a folder at the specified path with the specified name.
        If the folder already exists nothing will happen.

        folder_path (str): The path leading to where the folder will be placed
        folder_name (str): The desired name of the folder you're creating
    '''

    #check if the folder already exists
    if os.path.exists(folder_path + '/' + folder_name):
        print(f'{folder_name} already exists at the specified location.')
    else: #doesn't exist so make it
        os.mkdir(folder_path + '/' + folder_name)
        if move_to_folder:
            os.chdir(folder_path + '/' + folder_name)

    return None

def delete_folder(folder_path:str,folder_name:str) -> None:
    '''
        Deletes the folder at the specified path with the specified name.
        If the folder doesn't exist nothing will happen.

        folder_path (str): The path leading to where the folder is located
        folder_name (str): The name of the folder to be deleted
    '''

    #check if the folder already exists
    if os.path.exists(folder_path + '/' + folder_name):
        shutil.rmtree(folder_path + '/' + folder_name)
    else: #folder doesn't exist
        print(f'{folder_name} not found at {folder_path}')
    
    return None

'''
    Functions to open up the OLR data and get anomalies and then means of it within the boxes
    specified in Ratna et al. 2013
'''
def retrieve_OLR_data() -> tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
    '''
        Open up the NOAA Interpolated Daily OLR from PSL and return the lat,
        lon, date, and OLR data from the file.

        OLR data will have the form of (time,lat,lon).

        Return order is date,lat,lon,OLR
    '''

    #navigate to the folder where the OLR data is stored
    os.chdir(data_path)
    #check if the file isn't located where it is suppposed to be
    if not os.path.isfile(OLR_file):
        raise FileNotFoundError("The OLR File was not found in the data folder.")
    
    #open the file
    nc_data = Dataset(OLR_file)
    #get the lats, and lons
    lats = nc_data.variables['lat'][:]
    lons = nc_data.variables['lon'][:]
    #get the indices needed to refine them
    lat_ei = np.where(lats == -40)[0][0]
    lat_si = np.where(lats == 10)[0][0]
    lon_si = np.where(lons == 0)[0][0]
    lon_ei = np.where(lons == 80)[0][0]
    #now refine everything and tet the OLR
    lats = lats[lat_si:lat_ei]
    lons = lons[lon_si:lon_ei]
    olr = ma.getdata(nc_data.variables['olr'][:,lat_si:lat_ei,lon_si:lon_ei])
    time = nc_data.variables['time'][:] #hours since 1,1,1800
    #convert the time to a useable data
    ref_date = dt.datetime(1800,1,1)
    dates = np.array([ref_date + dt.timedelta(hours = hr) for hr in time])
    #replace bad OLR values with nan's
    olr[np.where(olr < -9999)] = np.nan
    #close the .nc file
    nc_data.close()
    #go to my original path
    os.chdir(root)

    return dates,lats,lons,olr

def retrieve_OLR_clim() -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    '''
        Open up the NOAA Interpolated daily OLR climatology from 1981-2010
        from NOAA PSL and return the climatological OLR values for our
        region of interest.

        OLR data will have the form (lat,lon)

        return order is lat,lon,OLR
    '''
    #navigate to the folder where the OLR data is stored
    os.chdir(data_path)
    #check if the file isn't located where it is suppposed to be
    if not os.path.isfile(OLR_clim):
        raise FileNotFoundError("The OLR Climatology File was not found in the data folder.")
    
    #open the file
    nc_data = Dataset(OLR_clim)
    #get the lats/lons
    lats = nc_data.variables['lat'][:]
    lons = nc_data.variables['lon'][:]
    #get the indices needed to refine them
    lat_ei = np.where(lats == -40)[0][0]
    lat_si = np.where(lats == 10)[0][0]
    lon_si = np.where(lons == 0)[0][0]
    lon_ei = np.where(lons == 80)[0][0]
    #now refine everything and tet the OLR
    lats = lats[lat_si:lat_ei]
    lons = lons[lon_si:lon_ei]
    olr = ma.getdata(nc_data.variables['olr'][:,lat_si:lat_ei,lon_si:lon_ei])
    #replace bad OLR values with nan's
    olr[np.where(olr < -9999)] = np.nan
    #close the .nc file
    nc_data.close()
    #go to my original path
    os.chdir(root)

    return lats,lons,olr

def get_OLR_anomalies(olr_data:np.ndarray,olr_clim:np.ndarray,olr_dates:np.ndarray) -> np.ndarray:
    '''
        Calculate the OLR anomalies relative to the 1981-2010 mean and return
        them as an array.

        Returns the olr anomalies with shape (time,lat,lon)
    '''

    #make a ref date for the anomaly calculation
    ref_date = dt.datetime(2001,1,1)
    #convert olr dates to a pseudo 2001 state, Feb 29th becomes March 1st
    anom_dates = []
    for i in range(len(olr_dates)):
        if olr_dates[i].month == 2 and olr_dates[i].day == 29:
            anom_dates.append(dt.datetime(2001,3,1))
        else:
            anom_dates.append(dt.datetime(2001,olr_dates[i].month,olr_dates[i].day))
    #calculate the anomalies based on the correct day
    olr_anoms = olr_data[:]
    for i in range(len(olr_dates)):
        day_dif = (anom_dates[i] - ref_date).days
        olr_anoms[i] = olr_data[i] - olr_clim[day_dif]

    return olr_anoms

def get_Ebox_values(olr_anoms:np.ndarray,lats:np.ndarray,lons:np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    '''
        Get the mean OLR anomalies within the eastern boxes of the index E1
        and E2.

        The return values have a dimension of time

        Return order is boxE1_mean, boxE2_mean
    '''

    # box E1 has bounds of 37E-42E, 17S-12S due to resolution of the OLR data
    # it will be 37.5E-42.5E,17.5S-12.5S
    # box E2 has bounds of 45E-50E, 23S-15S due to resolution of the OLR data
    # it will be 45E-50E, 22.5S-15S

    #use the lats/lons to refine the OLR anomalies
    E1_lat_ei = np.where(lats == -17.5)[0][0]
    E1_lat_si = np.where(lats == -12.5)[0][0]
    E2_lat_ei = np.where(lats == -22.5)[0][0]
    E2_lat_si = np.where(lats == -15)[0][0]
    E1_lon_si = np.where(lons == 37.5)[0][0]
    E1_lon_ei = np.where(lons == 42.5)[0][0]
    E2_lon_si = np.where(lons == 45)[0][0]
    E2_lon_ei = np.where(lons == 50)[0][0]

    #refine the anomalies to the boxes
    E1_olr_anoms = olr_anoms[:,E1_lat_si:E1_lat_ei,E1_lon_si:E1_lon_ei]
    E2_olr_anoms = olr_anoms[:,E2_lat_si:E2_lat_ei,E2_lon_si:E2_lon_ei]

    #take the mean
    E1_olr_anoms = np.nanmean(E1_olr_anoms,axis = (1,2))
    E2_olr_anoms = np.nanmean(E2_olr_anoms,axis = (1,2))

    return E1_olr_anoms,E2_olr_anoms

def get_Wbox_values(olr_anoms:np.ndarray,lats:np.ndarray,lons:np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    '''
        Get the mean OLR anomalies within the western boxes of the index W1
        and W2.

        The return values have a dimension of time

        Return order is boxW1_mean, boxW2_mean
    '''

    # box E1 has bounds of 22E-32E, 24S-18S due to resolution of the OLR data
    # it will be 22.5E-32.5E,25S-17.5S
    # box E2 has bounds of 32E-42E, 36S-28S due to resolution of the OLR data
    # it will be 32.5E-42.5E, 35S-27.5S

    #use the lats/lons to refine the OLR anomalies
    W1_lat_ei = np.where(lats == -25)[0][0]
    W1_lat_si = np.where(lats == -17.5)[0][0]
    W2_lat_ei = np.where(lats == -35)[0][0]
    W2_lat_si = np.where(lats == -27.5)[0][0]
    W1_lon_si = np.where(lons == 22.5)[0][0]
    W1_lon_ei = np.where(lons == 32.5)[0][0]
    W2_lon_si = np.where(lons == 32.5)[0][0]
    W2_lon_ei = np.where(lons == 42.5)[0][0]

    #refine the anomalies to the boxes
    W1_olr_anoms = olr_anoms[:,W1_lat_si:W1_lat_ei,W1_lon_si:W1_lon_ei]
    W2_olr_anoms = olr_anoms[:,W2_lat_si:W2_lat_ei,W2_lon_si:W2_lon_ei]

    #take the mean
    W1_olr_anoms = np.nanmean(W1_olr_anoms,axis = (1,2))
    W2_olr_anoms = np.nanmean(W2_olr_anoms,axis = (1,2))

    return W1_olr_anoms,W2_olr_anoms

def calculate_index(E1_vals:np.ndarray,E2_vals:np.ndarray,W1_vals:np.ndarray,W2_vals:np.ndarray) -> np.ndarray:
    '''
        Given the values within E1,E2,W1, and W2 calculate the value of my TTT
        index.

        Returns the Index time series
    '''

    #calculate the individual terms
    term_a = 0.4 * ((E1_vals+E2_vals)/2.0)
    term_b = 0.6 * ((W1_vals+W2_vals)/2.0)
    #put it all together
    ttt_index = term_a - term_b

    return ttt_index

'''
    Functions to determine the TTT days from the Index and create a file
    containing the index,date, and whether or not a day is the peak day
    of a TTT
'''

def index_std_and_mean(TTT_index:np.ndarray,TTT_dates:np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    '''
        Calcuates the mean and std deviation of the TTT index, but only for 
        days in austral summer (Oct - May)

        Return order is mean,std. dev.
    '''
    #make a subet of my index
    TTT_subset = TTT_index[:]
    for i in range(len(TTT_dates)):
        if TTT_dates[i].month < 10 and TTT_dates[i].month > 5:
            TTT_subset[i] = np.nan

    TTT_index_mean = np.nanmean(TTT_subset)
    TTT_index_std = np.nanstd(TTT_subset)

    return TTT_index_mean,TTT_index_std

def determine_ttt_days(TTT_index:np.ndarray,TTT_dates:np.ndarray) -> np.ndarray:
    '''
        Determine which days are TTT days by seeing which days are more than
        2 standard deviations above the mean for my TTT index.

        Returns a binary array where 1 is the peak day of a TTT event (day 0)
        and 0 is any other day.
    '''

    #get the mean and std. dev.
    index_mean,index_std = index_std_and_mean(TTT_index,TTT_dates)

    #find all values that are greater than 2 std. dev. from mean
    ttt_peak_days = np.zeros(len(TTT_index))
    ttt_peak_days[np.where(TTT_index > (index_mean+(2.*index_std)))] = 1

    #possible TTT days w/in 5 days of each other will be consolidated into a
    #single event with the day with the highest index value being considered
    #the true peak day of the TTT event.
    for i in range(len(TTT_index)):
        if ttt_peak_days[i] == 1: #if a TTT day
            #now I need to check if any days w/in 5 days of it are also TTTs
            if 1 in ttt_peak_days[i-5:i] or 1 in ttt_peak_days[i+1:i+5]: #can't include i in the search
                ttt_range = TTT_index[i-5:i+5]
                #find where the maximum occurs
                range_max = np.nanmax(ttt_range)
                #check if it is i
                if range_max == TTT_index[i]: #i would be 5 here
                    #zero out the non i days and make i a 1
                    ttt_peak_days[i-5:i+5] = 0
                    ttt_peak_days[i] = 1
                else:
                    #i isn't the peak so zero it out and move on
                    ttt_peak_days[i] = 0
    
    return ttt_peak_days
                
def make_ttt_file(file_name:str,TTT_index:np.ndarray,dates:np.ndarray,ttt_days:np.ndarray) -> None:
    '''
        Make a text file containing the value of my index, corresponding dates,
        and whether or not a particular day is the peak of a TTT event
    '''

    #navigate to where the file will be stored
    os.chdir(data_path)
    #open/make the file
    ttt_file = open(file_name,mode = 'w')
    #write the header
    ttt_file.write('# Year, Month, Day, Index Value, Event Day\n')
    #loop to write in the rest of the file
    for i in range(len(TTT_index)):
        ttt_file.write(f'{dates[i].year},{dates[i].month},{dates[i].day},{TTT_index[i]:.3f},{ttt_days[i]}\n')
    #close the file
    ttt_file.close()

    return None

# main function
def main() -> None:
    '''
        main function. Puts all the pieces together and finishes running
        either on an error or after creating the TTT index file
    '''

    #bring in the OLR data and climatology
    olr_dates,olr_lats,olr_lons,olr = retrieve_OLR_data()
    _,_,olr_clim = retrieve_OLR_clim()
    #get the OLR anomalies
    olr_anoms = get_OLR_anomalies(olr,olr_clim,olr_dates)
    #get the values in the boxes
    E1,E2 = get_Ebox_values(olr_anoms,olr_lats,olr_lons)
    W1,W2 = get_Wbox_values(olr_anoms,olr_lats,olr_lons)
    #calculate the index
    ttt_index = calculate_index(E1,E2,W1,W2)
    #get the ttt_day array
    ttt_days = determine_ttt_days(ttt_index,olr_dates)
    #write the data/index to a file
    make_ttt_file(ttt_index_file,ttt_index,olr_dates,ttt_days)

    return None

if __name__ == "__main__":
    main()
