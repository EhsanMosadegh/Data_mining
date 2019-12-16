import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
###########################################################

# monthly-mean diurnal plots of wind speed
# the whole process here should convert master_df_with_nan to master_df_nan_filled
master_file = 'master_file_2019-06-01_rundays_30.txt'
master_df = pd.read_csv(master_file)
#master_df_with_nan = master_df.set_index('date', drop=False) # key=col name
master_df['date'] = pd.to_datetime(master_df['date'])
master_df_with_nan = master_df.set_index('date', drop=True) # key=col name


stn_name_list = [i for i in master_df_with_nan.columns]
stn_ws_average = []
ws_diurnal_val = []

# calculate monthly mean WS diurnal plots
# select columns of dataframe inside loop
for col_step in range(len(master_df_with_nan.columns)):
    # select each column
    df_one_col = master_df_with_nan.iloc[:,col_step]
    # hrly_list = df_one_col.groupby(master_df_with_nan.index.hour).mean()
    #diurnal_group = df_one_col.groupby([master_df_with_nan.index.hour, master_df_with_nan.index.minute]).mean()
    diurnal_group = df_one_col.groupby(master_df_with_nan.index.hour).mean()
    # take the average of the diurnal profile
    stn_ws_average.append(diurnal_group.mean())
    # save the diurnal values
    ws_diurnal_val.append(diurnal_group)
    plt.title('monthly-mean diurnal profile at stn: %s' % stn_name_list[col_step])
    plt.ylabel('wind speed')
    plt.xlabel('hour of day')
    #
    # diurnal_group.plot()
    # plt.show()

###########################################################
# define function to estimate hourly wind speed
def ws_nan_estimate(stn_mean_ws, hr_of_day):
    theta=0.3 # from literature
    hr_of_peak_ws = 20
    ws_hrly_estimated = stn_mean_ws * (1 + (theta * np.cos(((2 * np.pi) / 24) * (hr_of_day - hr_of_peak_ws))))

    return ws_hrly_estimated
# the function returns the following list
#ws_diurnal_cycle_list = []

# ###########################################################
# loop to iterate over all columns to find out if we have nan in dataset
for stn_step, stn_name in enumerate(stn_name_list): #master_df_with_nan.columns.to_list()):
    print('-> processing stn no. %s and name %s' % (stn_step, stn_name))

    condition = master_df_with_nan.iloc[:, stn_step].isnull()
    # index = np.where(condition)[0]     # returns original index
    # find the datetime index of the rows with nan values in a list, if any
    nan_index_list = master_df_with_nan.loc[condition].index.to_list()
    print('-> found %s dt/rows with NaN:\n%s' % (len(nan_index_list), nan_index_list))
    # if the index list does not have any nan values then go to next iteration==station
    if (len(nan_index_list) == 0):
        print('-> did NOt find any NaN for stn: %s, going to next stn!' % stn_name)
        continue

    # will fill this list later from a WS function
    ws_diurnal_cycle_list = [i for i in range(0, 24, 1)]

    # we pick each dt with nan and find the estimated value for it
    for nan_dt_row in nan_index_list:
        # # change str to dt
        # dt_obj = dt.datetime.strptime(nan_dt_row, '%Y-%m-%d %H:%M:%S')

        # only extract the hr from dt
        hr_of_day = nan_dt_row.hour
        #print(hr_of_day)

        # here we use the list from the function
        # find the suitable value from the estimated list
        # ws_estimated = ws_diurnal_cycle_list[hr_of_day]

        stn_mean_ws = stn_ws_average[stn_step]
        ws_estimated = ws_nan_estimate(stn_mean_ws, hr_of_day)
        print('-> nan replaced with: %s' % ws_estimated)

        # update NaN with estimated value
        master_df_with_nan.loc[nan_dt_row, stn_name] = ws_estimated

print(master_df_with_nan.head())
# the master_df_with_nan is updated inside the loop above
# we need the nan_filld master df for next step which is the regression
master_df_nan_filled = master_df_with_nan.copy()