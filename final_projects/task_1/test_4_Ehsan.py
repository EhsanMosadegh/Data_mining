#!/usr/bin/python3
from scipy.sparse import coo_matrix

print('hello again!')

coo_file = '/Users/ehsanmos/Documents/CS_courses_UNR/Fall2019/data_mining/projects/cs458_project/project_1_dataMining_data/testing.txt'

coo_list=coo_matrix(coo_file)
print(coo_list.toarray())
