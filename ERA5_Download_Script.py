# This python script downloads ERA5 data utilizing the CDS API to the /DATA
# folder for this project. If the /DATA folder does not exist it will be
# created. It will also check to see if ERA5 files with the name/data already
# exist before going through with the download.

# IMPORTS GO HERE
import os #path/folder management
import cdsapi #access the CDS to get the ERA5 data

# Paths go here
data_path = os.getcwd() + '/DATA'
root = os.getcwd()

# FUNCTIONS GO HERE
def create_data_folder() -> None:
    '''
        Creates the /DATA folder if it doesn't already exist
    '''

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    return None

def make_u850_request() -> None:
    '''
        Requests ERA5 u850 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_u850.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'u_component_of_wind',
                ],
                'pressure_level': '850',
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_u850.nc')

    os.chdir(root)

    return None

def make_v850_request() -> None:
    '''
        Requests ERA5 v850 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_v850.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'v_component_of_wind',
                ],
                'pressure_level': '850',
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_v850.nc')

    os.chdir(root)

    return None

def make_u500_request() -> None:
    '''
        Requests ERA5 u500 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_u500.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'u_component_of_wind',
                ],
                'pressure_level': '500',
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_u500.nc')

    os.chdir(root)

    return None

def make_v500_request() -> None:
    '''
        Requests ERA5 v500 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_v500.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'v_component_of_wind',
                ],
                'pressure_level': '500',
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_v500.nc')

    os.chdir(root)

    return None

def make_w500_request() -> None:
    '''
        Requests ERA5 w500 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_w500.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'vertical_velocity',
                ],
                'pressure_level': '500',
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_w500.nc')

    os.chdir(root)

    return None

def make_z200_request() -> None:
    '''
        Requests ERA5 z200 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_z200.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'geopotential',
                ],
                'pressure_level': '200',
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_z200.nc')
    
    os.chdir(root)

    return None

def make_q850_request() -> None:
    '''
        Requests ERA5 q850 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_q850.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'specific_humidity',
                ],
                'pressure_level': '850',
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_q850.nc')

    os.chdir(root)

    return None

def make_surfP_request() -> None:
    '''
        Requests ERA5 q850 data from 1979-2023 over 10N-40S, 0-80E
    '''

    #navigate to the data folder
    create_data_folder()
    os.chdir(data_path)

    #check if the file already exists if not make the request
    if not os.path.isfile(data_path + '/ERA5_surfP.nc'):
        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    'surface_pressure',
                ],
                'month': [
                    '01', '02', '03',
                    '04', '05', '10',
                    '11', '12',
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'year': [
                    '1979', '1980', '1981',
                    '1982', '1983', '1984',
                    '1985', '1986', '1987',
                    '1988', '1989', '1990',
                    '1991', '1992', '1993',
                    '1994', '1995', '1996',
                    '1997', '1998', '1999',
                    '2000', '2001', '2002',
                    '2003', '2004', '2005',
                    '2006', '2007', '2008',
                    '2009', '2010', '2011',
                    '2012', '2013', '2014',
                    '2015', '2016', '2017',
                    '2018', '2019', '2020',
                    '2021', '2022',
                ],
                'time': '12:00',
                'area': [
                    0, 0, -50,
                    80,
                ],
            },
            'ERA5_surfP.nc')
    
    os.chdir(root)

    return None


# MAIN FUNCTION GOES HERE
def main() -> None:
    #first make the folder if it doesn't exist
    create_data_folder()
    #then send the download requests
    print('Starting u850 Request')
    make_u850_request()
    print('Request Complete')
    print('Starting v850 request')
    make_v850_request()
    print('Request Complete')
    print('Starting u500 Request')
    make_u500_request()
    print('Request Complete')
    print('Starting v500 Request')
    make_v500_request()
    print('Request Complete')
    print('Starting w500 request')
    make_w500_request()
    print('Request Complete')
    print('Starting z200 request')
    make_z200_request()
    print('Request Complete')
    print('Starting q850 request')
    make_q850_request()
    print('Request Complete')
    print('Starting Surface Pressure Request')
    make_surfP_request()
    print('Request Complete')

    return None

if __name__ == "__main__":
    main()