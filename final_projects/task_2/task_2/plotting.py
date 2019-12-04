import pandas as pd
import matplotlib.pyplot as plt
import os


#input_file = 'E_Subalpaine.csv' # no wind data

station_list=['E_Saltdesert.csv', 'E_Sagebrush.csv', 'W_Subalpine.csv', 'W_Montana.csv', 'W_Pinyon.csv', 'W_Sagebrush.csv']
stn = station_list[0]

data = pd.read_csv(stn, skiprows=9, names=['date','wind_speed'], parse_dates=['date']) # skip the first 10 rows with header info
X = data['date']
Y = data['wind_speed']
plt.plot(X, Y, color='b', linewidth=0.2)
plt.xlabel('hr')
plt.ylabel('Wind Speed')
plt.title('10 min wind speed at %s station' %stn[:-4])
plt.axvline(x='2019-05-01T00', color='red')
plt.axvline(x='2019-07-25T00', color='red')

plt.ylim(0, 50)
plt.gcf().autofmt_xdate()


    # ax = plt.subplot(3, 3, stn + 1)
    # ax = data.plot(X, Y)
    # fig, ax = plt.subplots()
    # ax.plot(X,Y)
    # ax.set_xlabel('hr/day')
    # ax.set_ylabel('wind speed')
    # ax.set_title(station_list[stn][:-4])

plt.savefig(os.path.join('./my_images/')+stn[:-4]+".png")
#plt.show()
