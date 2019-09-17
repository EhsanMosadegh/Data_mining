#!/usr/bin/python3

import random
import numpy as np
import matplotlib.pyplot as plt


total_points = 500
dimensions = 50

##################################################################################################################
#--- create random numbers

random_no_array_total = np.empty( shape=( total_points , dimensions ))#shape=( total_points , dimensions ) )
# print(total_points)
# print(dimensions)

for dim in range( 0 , dimensions ) :
	print( f'-> calculating random numbers for dimension = {dim}')

	#--- create random array for specific dim dimensions, gets deleted in each dim loop

	lower_bound = 1
	upper_bound = 100

	# produce random numbers in range = [0,100]
	rand_no_list_for_each_dim = []

	for point_counter in range( 0 , total_points , 1 ) :
		rand_number = random.randint( lower_bound , upper_bound )
		rand_no_list_for_each_dim.append( rand_number )

	random_no_array_for_each_dim = np.array( rand_no_list_for_each_dim )

	#print( f'-> random array before update = ') 
	#print( random_no_array_total )
	#print( f'-> new random list for new dimension')
	#print( random_no_array_for_each_dim )

	random_no_array_total[:,dim] = random_no_array_for_each_dim
	#print( f'-> random array total after update = ') 
	#print(random_no_array_total)

	#print( f'-> shape of random_no_array is = {random_no_array_total.shape}')
	#print( f'-> first col of array is = {random_no_array_total[:,0]}')


##################################################################################################################
#--- calculating the delta^2 array for each feature/dimension/column

total_row = total_points*total_points
delta2_array = np.zeros( shape=( total_row , dimensions ) )
#print( " " )
#print( f'-> shape of zero delta2_array = {delta2_array.shape}')
#print( delta2_array )

for dim in range( 0 , dimensions ) :
	print( f'-> calculating delta2 for dim = {dim}')

	row_counter = 0

	for list_elemenet_1 in random_no_array_total[:,dim] :
		for list_elemenet_2 in random_no_array_total[:,dim] :

			#print( f'-> calculating delta for point = {list_elemenet_1 , list_elemenet_2}')

			delta2 = ( list_elemenet_1 - list_elemenet_2 )**2 #  ????

			#print( f'-> delta^2 = {delta2}')

			#print( f'-> updating delta2_array at row&col = {row_counter , dim} ...')

			delta2_array[ row_counter , dim ] = delta2

			row_counter = row_counter+1
			#print( f'-> counter is = {row_counter}')

#print( " " )
#print( '-> delta2_array is = ')
#print(delta2_array)
#print( " " )


##################################################################################################################
#--- calculate distance from delta2 values for each dimensions/features/columns of data set one after each other

x_range = []
dispersion_factor_total_list = []

for dim in range( 0 , dimensions ) :
	print( f'-> calculating distance for all {dim} dimensions')

	#--- fill this list for each dimension

	dist_list_for_n_dim = []

	#--- calculate distance for each new dimension from begining and each row of array

	for row_of_delta2_array in range( len(delta2_array[:,0]) ) :
		#print( f'-> for row = {row_of_delta2_array}')

		#--- calculate distance for each new dim

		distance_2_points_at_each_dim = ( np.sum(delta2_array[ row_of_delta2_array , 0 : dim+1 ]) )**(1/2)	# check the range

		dist_list_for_n_dim.append( distance_2_points_at_each_dim )

	#print( f'-> distance list for {dim} dimensions is:')
	#print( dist_list_for_n_dim )

	#--- drop zeros in the list

	no_zero_dist_list_for_n_dim = []

	#print( f'-> removing zero from the list ...')

	for list_element in dist_list_for_n_dim :
		if ( list_element > 0.0 ) :
			no_zero_dist_list_for_n_dim.append( list_element )

		else:
			continue  # go check the next element

	#print( '-> now the non-zero list is =' )
	#print( no_zero_dist_list_for_n_dim )

	min_dist_dim = min( no_zero_dist_list_for_n_dim )
	max_dist_dim = max( no_zero_dist_list_for_n_dim )

	#print( f'-> min dis= {min_dist_dim} and max dis= {max_dist_dim}')

	dispersion_factor = (max_dist_dim - min_dist_dim) / min_dist_dim

	dispersion_factor_log10 = np.log10( dispersion_factor )
	#print( f'-> dispersion factor in log10 is= {dispersion_factor_log10}')

	dispersion_factor_total_list.append( dispersion_factor_log10 )

	x_range.append(dim+1)



#print( f'-> dispersion factor list for {total_points} data objects ({total_points}*{total_points}) is = ')
#print( dispersion_factor_total_list )
#print(x_range)

##################################################################################################################
#--- making the plot

print( '-> now making the plot ...' )

plt.plot( x_range , dispersion_factor_total_list )
plt.xlabel('Number of Dimensions')
plt.ylabel('log10 ((max_dist - min_dist / min_dis))')
plt.title( 'Curse of Dimensionality' )

plt.grid()

plt.savefig('curse_of_dimensionality_Ehsan.png' , dpi=400 , format='png')

print('-> SUCCESSFULLY FINISHED')

