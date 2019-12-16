import pandas as pd
import numpy as np
import datetime as dt
from pandas import DataFrame as df
import os

###########################################################################
# def extract_data(dataset_master, dataset_stn, period_dt_list, stn_col, stn_name):
#
#     for step, datetime_master in enumerate(np.nditer(period_dt_list)):
#         index = (dataset_stn['date'][:]<=datetime_master).argmin()-1
#         dataset_master[step, stn_name]= dataset_stn[index, stn_col]
#
#     return dataset_master
###########################################################################
# here
############################################################################ time period setting
days_from_start = 1 # days will convert to hrs

###########################################################################
# build the data time ruler- start from a desired datetime

# we need to have a dt period. we are going to extract the following period from the dataset.
yr = 2019
mon = 1
day = 1
# number of 10-min intervals in an hour- range: 1-6 intervals in an hour
minunte_intervals_in_hr = 6 # intervals

# define start and end datetime
datetime_start = dt.datetime(yr, mon, day, 0, 0, 0)
datetime_end = datetime_start + dt.timedelta(days=days_from_start)
print('-> running for period of %s days starting from: %s-%s-%s' % (days_from_start,yr,mon,day))
print('-> start date is: %s' % str(datetime_start))
print('-> interval period in an hour: every %s min' % (60/minunte_intervals_in_hr))
# define the period in no of 10min steps
no_10mins_steps_in_period = (datetime_end - datetime_start).days*24*minunte_intervals_in_hr # change to each 10 min to make the period; days*24hrs*6observations per hr
# make number of time steps
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
print('-> shape of datetime ruler is: %s' %dt_ruler.shape)

###########################################################################
# we need to create a master dataset, open each station dataset, and fill the master dataset with sensor
# values at each observation timestep.  we have the ruler and we use it as the index of the the master dataset.

# define list of stations
station_list = ['E_Sagebrush.csv', 'E_Saltdesert.csv', 'W_Subalpine.csv', 'W_Montana.csv', 'W_Pinyon.csv', 'W_Sagebrush.csv']
print('-> no. of stations included in this processing step: %s' % len(station_list))
# list comprehension to use as the col of dataframe
col_list = [i[:-4] for i in station_list]

# create a np array as master dataset to store data; master data set= mds
master_ds_rows = dt_ruler.shape[0] # use ruler to make the ds index
master_ds_cols = len(station_list)
# create a master dataset
master_array = np.full([master_ds_rows, master_ds_cols], np.nan, dtype='float') # how create the mds array?
#print(master_array)

# iterate over each station list and read data to the master dataset
for stn_no, stn_name in enumerate(station_list):
    print('-> for stn no.: %s, %s' % (stn_no, stn_name))
    # read each csv file and load it into dataframe
    # note the format: <yyyy-MM-dd'T'HH:mm:ss.SSS'Z'> Z=timezone offset data, this is a challenge
    stn_dataset = pd.read_csv(stn_name, skiprows=9, names=['datetime', 'wind_speed'], parse_dates=['datetime']) # skip the first 10 rows with header info
    # stn_dataset['dt'] = stn_dataset['dt'].dt.tz_localize(timezone.utc)

    # check if datetime col is ware or naive
    stn_dt_sample = stn_dataset['datetime'][0]
    print('-> sample moment from stn dataset: %s' % stn_dt_sample)
    # if the output of bellow does not return None,
    ## datetime is aware= the moment knows about timezone by its UTC offset, else it's naive= localized
    ## our datetime shows time in utc timezone, i.e. it has offset from UTC time
    # print('-> check for yzinfo: %s' %stn_dt_sample.tzinfo)  # if None= no localization needed, else datetime object is sware
    # print('-> check for offset: %s' %stn_dt_sample.tzinfo.utcoffset(stn_dt_sample))  # datetime object is sware
    #naive_local_dt = stn_dt_sample.replace(tzinfo=None)
    #local_offset_dt = stn_dt_sample.utcoffset()
    #print('-> now convert to local')
    # stn_dt_sample.dt.tz_convert(tz=None)

    # update dataset == convert datetime column from UTC-offset to local time
    stn_dataset['datetime'] = stn_dataset['datetime'].dt.tz_convert(tz=None)

    # pick one datetime from ruler and compare against sensor data
    for step_ruler, ruler_dt_stamp in enumerate(dt_ruler):
        # pick each dt from stn dataset
        for stn_dt_step in range(len(stn_dataset['datetime'])):
            # check if datetime matches- Q-how compare dt? str or dt itself? how localize dt?
            stn_dt_stamp = stn_dataset['datetime'][stn_dt_step]

            if ruler_dt_stamp == stn_dt_stamp:
                # print('-> both agree for:')
                # print('ruler: %s' %ruler_dt_stamp)
                # print('  stn: %s' %stn_dt_stamp)

                # extract value from stn dataset and put it in the master array
                extracted_val = stn_dataset['wind_speed'][stn_dt_step]
                #print('-> found for stn no: %s at moment %s' %(stn_no, ruler_dt_stamp))
                master_array[step_ruler, stn_no] = extracted_val    # change it to col numbers later
                continue    # to next dt in stn dataset

            # else:
            #     #print('-> did not find dt match between: %s and %s' %(ruler_dt_stamp, stn_dt_stamp))
            #     # fill the row with nan at the same spot
            #     master_ds_array[step_ruler, stn_no] = '-999'
# print('step of ruler: %s' % step_ruler)
# no_of_days = (step_ruler/144)
# print('no of days: %s' % no_of_days)

# create a data-frame from np array for each month
master_df_with_nan = df(data=master_array, index=dt_ruler, columns=col_list)
print('-> the head of master dataset:\n %s' % master_df_with_nan.head())
print('-> the shape of master dataset: %s' % str(master_df_with_nan.shape))

# this section is for writing the data to a machine. Since we are running thsi example on colab,
# we do not write any file into the machine

# # define path and file name to write the data to a csv file
# master_file_name = ('master_dataset_%s-%s-%s_rundays_%s.txt' % (str(yr),str(mon),str(day),str(days_from_start)))
# # print('-> output file is: %s' % master_file_name)
# # master_file_path = '/Users/ehsanmos/Documents/CS_courses_UNR/Fall2019/Data_mining/Data_mining_projects/final_projects/task_2/datasets/'
# master_file_path = os.getcwd()
# # write the new formed dataset in to a csv file at desired location
# master_df.to_csv(os.path.join(master_file_path, master_file_name), index_label='date')
# ###########################################################################
