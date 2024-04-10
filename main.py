# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 13:28:10 2022

@author: aarregui
"""

import sys
import numpy as np
from main_MP import *
from main_MP_AV import * 
from main_CPC import *

window_sizes = [500, 1700, 2500]
 
data_file_name = 'python-main-op.csv'
data_path = os.path.join('data', data_file_name)
suffix = 'MP_AV'


data = pd.read_csv(data_path)
series = data['current'].to_numpy()
true_ops = data['op_id'].to_numpy()


output_folder = os.path.join('output', 'experimentation')


##########
#clear output_folder files

files = os.listdir(output_folder)

# Itera sobre cada archivo y elimínalo
for file in files:
    file_path = os.path.join(output_folder, file)
    if os.path.isfile(file_path):
        os.remove(file_path)
##########




for window_size in window_sizes:
    print('Matrix Profile')
    print('Window Size: {}'.format(window_size))
    main_MP(data, window_size, output_folder)
    main_MP_AV(data, window_size, output_folder)



window_sizes = [400, 750, 1200]

for window_size in window_sizes:
    print('Changepoint Detection + Clustering DBSCAN')
    print('Window Size: {}'.format(window_size))
    main_CPC(data, window_size, output_folder)