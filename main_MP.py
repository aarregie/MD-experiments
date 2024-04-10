# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:10:36 2024

@author: aarregui
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import stumpy
from src.utils import *
import json
import time

plt.rcParams["figure.figsize"] = (25,12)


def main_MP(data, m, output_folder):
    
    series = data['current'].to_numpy()
    # true_ops = data['op_id'].to_numpy()
    
    #true_ops solo la op principal --> op_id == 1
    true_ops = np.where(data['op_id'] == 1, 1, 0)
    
    series_length = len(series)
    
    suffix = 'MP'
    
    start = time.time()
    mp = stumpy.stump(series, m)
        
    #o identify the index location of the motif we’ll need to find the 
    #index location where the matrix profile, mp[:, 0], has the smallest value:
    motif_idx = np.argsort(mp[:, 0])[0]
    nearest_neighbor_idx = mp[motif_idx, 1]
        
    subsequence = series[motif_idx:(motif_idx+m)]
        
    distance_profile = stumpy.mass(subsequence, series)
    
    nn_idx = np.argsort(distance_profile)[1]
       
    
    matches = stumpy.match(subsequence, series, max_distance = 30.0)
    final = time.time()
    
    pred_ops = generate_pred_ops(matches, series_length, m)
    
    output_folder = os.path.join('output', 'experimentation')
    plt.plot(series, color = 'gray', alpha = .7, lw = 2)
    for match in matches[:,1]:
        begin, end = match, match+len(subsequence)
        x_range = np.arange(begin, end)
        plt.plot(x_range, series[begin:end], lw = 2)
    plt.title('Simulated Signal m = {}'.format(m), fontsize = 20)
    plt.xlabel('Time', fontsize = 15)
    plt.ylabel('Simulated Signal', fontsize = 15)
    plt.savefig(os.path.join(output_folder, 'pattern_simulated_signal_{}_{}.png'.format(suffix, m)))
    plt.close()
    
    
    #superpuestos
    start_idx = matches[:, 1]
    
    for match in start_idx:
        begin, end = match, match+len(subsequence)
        plt.plot(series[begin:end], lw = 2, alpha = .4, color = 'gray')
    
    plt.title('Simulated Signal m = {}'.format(m), fontsize = 20)
    plt.ylabel('Simulated Signal',fontsize = 15)
    plt.xlabel('Time',fontsize = 15)
    plt.tick_params(axis = 'both', labelsize = 15)
    plt.tick_params(axis = 'both', labelsize = 15)
    plt.savefig(os.path.join(output_folder, 'patterns_simulated_signal_{}_SUPERPUESTOS_{}.png'.format(suffix, m)))
    plt.close()
    
    #get centroid
    X = get_matches_by_start(series, m, start_idx)
    centroid = get_centroid(X)
    
    sse = get_sse(centroid, X)
    nrmse = get_nrmse(centroid, X)
    
    results = {'params': [m]}
    
    data['true_op_ex'] = get_ops(true_ops)
    
    results['w'] = [m]
    results['overlap_rate'] = [overlap_rate(pred_ops, true_ops)]
    results['true_positive_rate'] = [true_positive_rate(pred_ops, true_ops)]
    results['false_discovery_rate'] = [false_discovery_rate(pred_ops, true_ops)]
    results['sse'] = [sse]
    results['nrmse'] = [nrmse]
    results['n_matches'] = [len(matches)]
    results['run_time'] = [final-start]

    #store results
    results_file = os.path.join(output_folder, 'results_{}.json'.format(suffix))
    
    store_results(results, results_file)
    
    return True




