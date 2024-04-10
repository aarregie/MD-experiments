# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:07:33 2024

@author: aarregui
"""


import os
import pandas as pd
import numpy as np
import json



results_path = os.path.join('output', 'experimentation')
approaches = ['MP', 'MP_AV', 'CPC']



for approach in approaches:
    
    file_name = 'results_{}.json'.format(approach)
    
    file = os.path.join(results_path, file_name)
    
    with open(file) as results_file:
        results_json = json.load(results_file)
    
    results_file.close()
    
    print(results_json)
    data = pd.DataFrame.from_dict(results_json).iloc[:,1:]
    
    data = data.round(4)
    
    data_name = 'results_{}.csv'.format(approach)
    
    
    data.to_csv(os.path.join(results_path, data_name))
    