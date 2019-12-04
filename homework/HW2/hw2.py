#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt


print('-> hello Ehsan!')



center = 10
std = 1.0
size_array = [10, 2]

gaussian_list_x = np.random.normal( center , std , size=size_array )
#gaussian_list_y = np.random.normal( center , std , size )

#uniform_list = []

x_axis= gaussian_list_x
y_axis= gaussian_list_x
print(f'-> x axis= {x_axis}')

plt.scatter( x_axis , y_axis , marker='+' )

plt.show()