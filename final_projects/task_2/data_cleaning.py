import pandas as pd
import numpy as np
import datetime as dt

def extract_data(dataset_master, dataset_stn, studyperiod_dt_list, stn_col, stn_name):

    for step, datetime_master in enumerate(np.nditer(studyperiod_dt_list)):
        index = (dataset_stn['date'][:]<=datetime_master).argmin()-1
        dataset_master[step, stn_name]= dataset_stn[index, stn_col]

    return dataset_master


def main():

    station_list = ['E_Saltdesert.csv', 'E_Sagebrush.csv', 'W_Subalpine.csv', 'W_Montana.csv', 'W_Pinyon.csv', 'W_Sagebrush.csv']

    datetime_start = dt.datetime(2019, 1, 1, 0, 0, 0)
    datetime_end = datetime_start + dt.timedelta(minutes=10)
    n_hrs = (datetime_end - datetime_start).min + 10

    studyperiod_dt_list = np.full([n_hrs + 1], np.nan, dtype='object')
    for hr in range(0, n_hrs + 1, 1):
        studyperiod_dt_list[hr] = datetime_start + dt.timedelta(hours=hr)

    print(studyperiod_dt_list)

    shape = [len(studyperiod_dt_list), len(station_list)]
    dataset_master = np.full(shape, np.nan, dtype='float')

    # read all data files
    for step, stn_name in enumerate(station_list):

        print('step= %s, file= %s' %(step, stn_name))
        dataset_stn = pd.read_csv(stn_name, skiprows=9, names=['date','wind_speed'], parse_dates=['date']) # skip the first 10 rows with header info

        dataset_master = extract_data(dataset_master, dataset_stn, studyperiod_dt_list, stn_col, stn_name)


if __name__ == '__main__':
    main()

