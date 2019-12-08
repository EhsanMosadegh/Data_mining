import pandas as pd
import numpy as np
import datetime as dt
from pandas import DataFrame as df

import pytz
from datetime import timezone
import tzlocal

# def extract_data(dataset_master, dataset_stn, period_dt_list, stn_col, stn_name):
#
#     for step, datetime_master in enumerate(np.nditer(period_dt_list)):
#         index = (dataset_stn['date'][:]<=datetime_master).argmin()-1
#         dataset_master[step, stn_name]= dataset_stn[index, stn_col]
#
#     return dataset_master
###########################################################################
# time period setting
days_from_start = 30 # days will convert to hrs

###########################################################################
# build the data time ruller- start from a desired datetime

# we need to have a dt period
datetime_start = dt.datetime(2019, 3, 1, 0, 0, 0)
datetime_end = datetime_start + dt.timedelta(days=days_from_start)
# define the period in no of 10min steps
no_10mins_steps_in_period = (datetime_end - datetime_start).days*24*6 # change to each 10 min to make the period; days*24hrs*6observations per hr
# make no of time steps
no_10mins_steps_in_period = int(no_10mins_steps_in_period)
# create a np array for our ruler, fill it with nan
dt_ruler = np.full([no_10mins_steps_in_period + 1], np.nan, dtype='object')
# define a new var to use in loop
dt_at_10min_interval = datetime_start
# create a list of date-time objects from 10min steps as a ruler for our dataset; then fill it
for step in range(no_10mins_steps_in_period):
    # period_dt_list[step]
    dt_at_10min_interval = dt_at_10min_interval + dt.timedelta(minutes=10) # increment every 10min
    dt_ruler[step] = dt_at_10min_interval # fill the ruler with dt at 10min interval
print('shape of dt ruler is: %s' %dt_ruler)

###########################################################################
# we need to create a master dataset, open each station dataset, and fill the master dataset with sensor
# values at each observation timestep.  we have the ruler and we use it as the index of the the master dataset.

# define list of stations
station_list = ['E_Sagebrush.csv'] #'E_Saltdesert.csv']#, ]#, 'W_Subalpine.csv', 'W_Montana.csv', 'W_Pinyon.csv', 'W_Sagebrush.csv']
# create a np array as master dataset to store data; master data set= mds
master_ds_rows = dt_ruler.shape[0] # use ruler to make the ds index
master_ds_cols = len(station_list)
# create a master dataset
master_ds_array = np.full([master_ds_rows, master_ds_cols], np.nan, dtype='float') # how create the mds array?

# iterate over each station list and read data to the master dataset
for stn_no, stn_name in enumerate(station_list):
    # read each csv file and load it into dataframe
    # note the format: <yyyy-MM-dd'T'HH:mm:ss.SSS'Z'> Z=timezone offset data, this is a challenge
    stn_dataset = pd.read_csv(stn_name, skiprows=9, names=['datetime', 'wind_speed'], parse_dates=['datetime']) # skip the first 10 rows with header info
    #stn_dataset['dt'] = stn_dataset['dt'].dt.tz_localize(timezone.utc)

    # check if datetime col is ware or naive
    stn_dt_sample = stn_dataset['datetime'][0]
    print('-> sample moment: %s' %stn_dt_sample)
    ## if the output of bellow does not return None,
    ## datetime is aware= the moment knows about timezone by its UTC offset, else it's naive= localized
    ## our datetime shows time in utc timezone, i.e. it has offset from UTC time
    # print('-> check for yzinfo: %s' %stn_dt_sample.tzinfo)  # if None= no localization needed, else datetime object is sware
    # print('-> check for offset: %s' %stn_dt_sample.tzinfo.utcoffset(stn_dt_sample))  # datetime object is sware
    #naive_local_dt = stn_dt_sample.replace(tzinfo=None)
    #local_offset_dt = stn_dt_sample.utcoffset()
    print('-> now convert to local')
    #stn_dt_sample.dt.tz_convert(tz=None)

    # update dataset ==> convert datetime column from UTC-offset to local time
    stn_dataset['datetime'] = stn_dataset['datetime'].dt.tz_convert(tz=None)




    # pick one datetime from ruler and compare against sensor data
    for step_ruler, ruler_dt_stamp in enumerate(dt_ruler):
        # pick each dt from stn dataset
        for stn_dt_step in range(len(stn_dataset['datetime'])):
            # check if datetime matches- Q-how compare dt? str or dt itself? how localize dt?
            stn_dt_stamp = stn_dataset['datetime'][stn_dt_step]

            #print('-> checking ruler dt %s agains stn dt %s' %(ruler_dt_stamp, stn_dt_stamp))

            if (str(ruler_dt_stamp) == str(stn_dt_stamp)):  ## error here!
                print('both agree for:')
                print('-> ruler: %s' %ruler_dt_stamp)
                print('->   stn: %s' %stn_dt_stamp)
                # extract value from stn dataset and put it in the master array
                master_ds_array[step_ruler, stn_no] = stn_dataset['wind_speed'][stn_dt_step] # change it to col numbers later
            else:
                #print('-> did not find dt match between: %s and %s' %(ruler_dt_stamp, stn_dt_stamp))
                # fill the row with nan at the same spot
                master_ds_array[step_ruler, stn_no] = 'nan'




# then write out the file into a new dataset

