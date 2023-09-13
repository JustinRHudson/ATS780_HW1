# This file processes my data into a single CSV that can be used by my random forest model
# to predict TTT index, specifically days where it will be 2 sigma or more from the mean
# and indicate a TTT event

# IMPORTS GO HERE
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
from PIL import Image
import datetime as dt
import numpy.ma as ma
from urllib.request import urlretrieve
import os

# Paths go here
root = os.getcwd()
data_path = root + '/DATA'

# define the box objects for the ERA5 data
#boxes are defined as left,bottom,right,top
q850_box = [20,-30,40,-15]
z200_box1 = [35,-35,45,-25]
z200_box2 = [25,-40,35,-30]
u850_box = [10,-25,35,-10]
v850_box1 = [30,-30,40,-15]
v850_box2 = [30,-45,40,-30]
surfp_box1 = [40,-45,55,-35]
surfp_box2 = [10,-45,30,-35]
w500_box = [25,-30,40,-20]

# Download the OMI data in case it doesn't already exist
os.chdir(data_path)
if not os.path.isfile('MJO_OMI.txt'):
    urlretrieve('https://www.psl.noaa.gov/mjo/mjoindex/omi.1x.txt','MJO_OMI.txt')
os.chdir(root)

# Functions go here
#function to get the day of the year from the date
def doy_calc(dates:np.ndarray) -> np.ndarray:
    '''
        Given a list of dates get the DOY going alongside that date.
        On leap years Feb 29th and March 1st will be considered the same such that
        the maximum DOY will be 365
    '''

    #make an array to hold the DOYs
    doy_array = np.zeros(len(dates))
    ref_date = dt.datetime(2001,1,1)
    for i in range(len(dates)):
        if dates[i].month == 2 and dates[i].day == 29:
            use_date = dt.datetime(2001,3,1)
        else:
            use_date = dt.datetime(2001,dates[i].month,dates[i].day)
        doy_array[i] = ((use_date - ref_date).days)+1

    return doy_array

#functions for ERA5 data
def make_era5_climatology(file:str,key:str) -> np.ndarray:
    '''
        Makes a daily climatology of ERA5 data for Austral Summer for
        a specified variable.

        file (str): The name of the .nc file containing the ERA5 data
        key (str): The key needed to access the data within the 
            specified .nc file

        returns the climatology as a numpy array
    '''
    #ref date to convert from time to date
    ref_date = dt.datetime(1900,1,1)

    #dates need to encompass austral summer, Feb 29th with be folded
    #into March 1st to handle leap days
    climatology_start_date = dt.datetime(2001,1,1)
    climatology_dates = np.array([climatology_start_date + dt.timedelta(days = dd) for dd in range(365)])

    climatology_array = np.zeros((len(climatology_dates),201,321))
    climatology_count = np.zeros((len(climatology_dates),201,321))
    #now I want to open up the .nc file and pull an element one at a time and put it
    #in the appropriate slot for the climatology
    os.chdir(data_path)
    file_time = Dataset(file).variables['time'][:]
    file_dates = np.array([ref_date + dt.timedelta(hours = int(hr)) for hr in file_time])
    for i in range(len(file_dates)):
        daily_data = Dataset(file).variables[key][i,:,:]
        if file_dates[i].month == 2 and file_dates[i].day == 29:
            use_date = dt.datetime(2001,3,1)
        else:
            use_date = dt.datetime(2001,file_dates[i].month,file_dates[i].day)
        climatology_array[np.where(climatology_dates == use_date)[0][0]] += daily_data
        climatology_count[np.where(climatology_dates == use_date)[0][0]] += 1
    os.chdir(root)
    
    return climatology_array/climatology_count

def get_ERA5_anomalies(era5_data:np.ndarray,era5_clim:np.ndarray,era5_dates:np.ndarray) -> np.ndarray:
    '''
        Calculate the OLR anomalies relative to the 1981-2010 mean and return
        them as an array.

        Returns the olr anomalies with shape (time,lat,lon)
    '''

    #dates need to encompass austral summer, Feb 29th with be folded
    #into March 1st to handle leap days
    climatology_start_date = dt.datetime(2001,1,1)
    climatology_dates = np.array([climatology_start_date + dt.timedelta(days = dd) for dd in range(365)])

    #calculate the anomalies based on the correct day
    era5_anoms = np.empty(era5_data.shape)
    for i in range(len(era5_dates)):
        if era5_dates[i].month == 2 and era5_dates[i].day == 29:
            use_date = dt.datetime(2001,3,1)
        else:
            use_date = dt.datetime(2001,era5_dates[i].month,era5_dates[i].day)
        day_ind = np.where(climatology_dates == use_date)[0][0]
        era5_anoms[i] = era5_data[i] - era5_clim[day_ind]
    return era5_anoms

def make_era5_box(era5_anoms:np.ndarray,era5_lats:np.ndarray,era5_lons:np.ndarray,box:list) -> np.ndarray:
    '''
        Uses a defined box to get the ERA5 data within the box and returns the
        spatial mean as a function of time.
    '''
    #boxes are left,bottom,right,top
    #get the indices that correspond to the box
    lat_si = np.where(era5_lats == box[3])[0][0]
    lat_ei = np.where(era5_lats == box[1])[0][0]
    lon_si = np.where(era5_lons == box[0])[0][0]
    lon_ei = np.where(era5_lons == box[2])[0][0]

    box_anoms = era5_anoms[:,lat_si:lat_ei,lon_si:lon_ei]

    return np.nanmean(box_anoms,axis = (1,2))

def process_era5_data(file:str,key:str,box:list) -> tuple[np.ndarray,np.ndarray]:
    '''
        Open up an ERA5 file, compute the climatology and calculate anomalies
        then get the values of the anomalies within the box

        file (str): The name of the .nc file containing the ERA5 data
        key (str): The key needed to access the data within the 
            specified .nc file
        box (list): The box outlining the area of interest within the ERA5 data
            specifies the left,bottom,right,and top boundaries in that order
    '''
    
    #navigate to the data path and open the ERA5 data
    os.chdir(data_path)
    e5_data = ma.getdata(Dataset(file).variables[key][:])
    e5_lats = Dataset(file).variables['latitude'][:]
    e5_lons = Dataset(file).variables['longitude'][:]
    e5_time = Dataset(file).variables['time'][:]
    os.chdir(root)
    #convert the time to dates
    e5_dates = np.array([dt.datetime(1800,1,1) + dt.timedelta(hours = int(hr)) for hr in e5_time])
    #get the climatology
    e5_clim = make_era5_climatology(file,key)
    #get the anomalies
    e5_anoms = get_ERA5_anomalies(e5_data,e5_clim,e5_dates)
    #refine to just the box
    e5_box = make_era5_box(e5_anoms,e5_lats,e5_lons,box)

    return e5_box,e5_dates

#functions for the TTT Index
def open_ttt_index() -> tuple[np.ndarray]:
    '''
        Opens up the TTT Index that I made and returns the dates and
        the value of the TTT Index as well as whether or not the day
        was a TTT day
    '''

    #navigate to the data directory and open up the file
    os.chdir(data_path)
    ttt_index_file = np.loadtxt('TTT_Index.csv',delimiter=',',skiprows = 1)
    os.chdir(root)
    #now portion it out to the individual columns
    year = ttt_index_file[:,0]
    month = ttt_index_file[:,1]
    day = ttt_index_file[:,2]
    index_val = ttt_index_file[:,3]
    ttt_day_bool = ttt_index_file[:,4]
    #convert the year,month,day into the actual date
    ttt_dates = np.array([dt.datetime(int(year[i]),int(month[i]),int(day[i])) for i in range(len(year))])

    return ttt_dates,index_val,ttt_day_bool

#functions for the MJO Index
#first a function to determine the phase of the MJO based on the OMI
# index values so I can classify by phase in case it is helpful
def omi_phase_check(omi1:np.ndarray,omi2:np.ndarray) -> np.ndarray:
    '''
        Calculates the phase of the MJO based on the values of the PCs in the
        omi index.
    '''

    #array to hold the phases
    omi_phase = np.zeros(len(omi1))
    #now use if statements to do it
    for i in range(len(omi_phase)):
        if omi2[i] < 0:
            #this means it is either phase 1,2,7,8
            if -omi1[i] <= 0:
                #this means it is either phase 1 or 2
                if omi2[i] == -omi1[i] :
                    omi_phase[i] = 2
                elif omi2[i] < -omi1[i]:
                    omi_phase[i]  = 1
                elif omi2[i] > -omi1[i]:
                    omi_phase[i] = 2
            elif -omi1[i] > 0:
                if -omi2[i] == -omi1[i]:
                    omi_phase[i] = 8
                elif -omi2[i] < -omi1[i]:
                    omi_phase[i] = 7
                elif -omi2[i] > -omi1[i]:
                    omi_phase[i] = 8
        elif omi2[i] >= 0:
            #it is either phase 3,4,5,6
            if -omi1[i] < 0:
                if -omi2[i] > -omi1[i]:
                    omi_phase[i] = 3
                elif -omi2[i] == -omi1[i]:
                    omi_phase[i] = 4
                elif -omi2[i] < -omi1[i]:
                    omi_phase[i] = 4
            elif -omi1[i] >= 0:
                if omi2[i] > -omi1[i]:
                    omi_phase[i] = 5
                if omi2[i] == -omi1[i]:
                    omi_phase[i] = 6
                if omi2[i] < -omi1[i]:
                    omi_phase[i] = 6

    return omi_phase

def open_mjo_index() -> tuple[np.ndarray]:
    '''
        Opens up the MJO OMI Index file and returns the date, the amplitude,
        and the phase of the MJO from 1979 - Present
    '''

    #navigate to the data directory and open up the file
    os.chdir(data_path)
    omi_index_file = np.loadtxt('MJO_OMI.txt')
    os.chdir(root)
    #now portion out the file
    year = omi_index_file[:,0]
    month = omi_index_file[:,1]
    day = omi_index_file[:,2]
    omi1 = omi_index_file[:,4]
    omi2 = omi_index_file[:,5]
    omi_amp = omi_index_file[:,6]
    #get the phase of the MJO
    omi_phase = omi_phase_check(omi1,omi2)
    #get the dates
    omi_dates = np.array([dt.datetime(int(year[i]),int(month[i]),int(day[i])) for i in range(len(year))])

    return omi_dates,omi_amp,omi_phase

#now let's make a function to make my csv
def csv_writer(file_name:str,doys:np.ndarray,ttt_index_vals:np.ndarray,ttt_day_bool:np.ndarray,
               omi_amp:np.ndarray,omi_phase:np.ndarray,q850:np.ndarray,z200_b1:np.ndarray,
               z200_b2:np.ndarray,u850:np.ndarray,v850_b1:np.ndarray,v850_b2:np.ndarray,
               surfp_b1:np.ndarray,surfp_b2:np.ndarray,w500:np.ndarray,random_var:np.ndarray) -> None:
    '''
        Makes the CSV file I will use as the input for my random forest model
    '''
    os.chdir(data_path)
    f = open(file_name,'w')
    f.write('# DOY,TTT_INDEX_VAL,TTT_DAY_BOOL,OMI_AMP,OMI_PHASE,Q850,Z200_B1,Z200_B2,U850,V850_B1,V850_B2,SURF_PRES_B1,SURF_PRES_B2,W500,RAND_VAR\n')
    for i in range(len(doys)):
        if not np.isnan(ttt_index_vals[i]):
            f.write(f'{doys[i]},{ttt_index_vals[i]},{ttt_day_bool[i]},{omi_amp[i]},{omi_phase[i]},{q850[i]},{z200_b1[i]},{z200_b2[i]},{u850[i]},{v850_b1[i]},{v850_b2[i]},{surfp_b1[i]},{surfp_b2[i]},{w500[i]},{random_var[i]}\n')
    f.close()

    return None

#main function
def main() -> None:
    #first let's get the TTT index and MJO index done
    print('Processing TTT Data')
    _,ttt_index_values,ttt_event_bool = open_ttt_index()
    print('Processing OMI Data')
    _,omi_amp,omi_phase = open_mjo_index()
    #now let's do the various era5 boxes
    print('Processing q850 Data')
    q850,e5_dates = process_era5_data('ERA5_q850.nc','q',q850_box)
    print('Processing z200 B1 Data')
    z200_b1,_ = process_era5_data('ERA5_z200.nc','z',z200_box1)
    print('Processing z200 B2 Data')
    z200_b2,_ = process_era5_data('ERA5_z200.nc','z',z200_box2)
    print('Processing u850 Data')
    u850,_ = process_era5_data('ERA5_u850.nc','u',u850_box)
    print('Processing v850 B1 Data')
    v850_b1,_ = process_era5_data('ERA5_v850.nc','v',v850_box1)
    print('Processing v850 B2 Data')
    v850_b2,_ = process_era5_data('ERA5_v850.nc','v',v850_box2)
    print('Processing surface pressure B1 Data')
    surfp_b1,_ = process_era5_data('ERA5_surfP.nc','sp',surfp_box1)
    print('Processing surface pressure B2 Data')
    surfp_b2,_ = process_era5_data('ERA5_surfP.nc','sp',surfp_box2)
    print('Processing w500 Data')
    w500,_ = process_era5_data('ERA5_w500.nc','w',w500_box)
    #get the doy data
    doys = doy_calc(e5_dates)
    #make a random uniform variable of the same length
    rand_var = np.random.uniform(0,100,len(doys))
    #get the indices where TTT_index_values are not_nan

    #now let's write to my csv file
    print('Writing to TTT_DATA.csv')
    csv_writer('TTT_DATA.csv',doys,ttt_index_values,ttt_event_bool,omi_amp,omi_phase,q850,z200_b1,z200_b2,u850,v850_b1,v850_b2,surfp_b1,surfp_b2,w500,rand_var)

    return None

if __name__ == "__main__":
    main()
