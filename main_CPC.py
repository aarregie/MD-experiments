# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:46:04 2024

@author: aarregui
"""


import os
import pandas as pd
import numpy as np
import ruptures as rpt
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import tsfel
from sklearn.preprocessing import normalize
from src.utils import *
import time

# import sklearn
plt.rcParams["figure.figsize"] = (25,12)


def main_CPC(data, m, output_folder):
    
    
    suffix = 'CPC'
    
    series = data['current'].to_numpy()
    # true_ops = data['op_id'].to_numpy()
    
    #true_ops solo la op principal --> op_id == 1
    true_ops = np.where(data['op_id'] == 1, 1, 0)
    
    start = time.time()
    
    # detection 
    # algo = rpt.Pelt(model="l2", jump = 600, min_size = 600).fit(series.reshape(-1,1))
    # algo = rpt.Window(width=10, min_size = 100, model='normal').fit(rolling_series.reshape(-1,1))
    # algo = rpt.BottomUp(model = 'normal', jump = 10, min_size = 50).fit(series.reshape(-1,1))
    algo = rpt.Binseg(model = 'normal', min_size = m).fit(series.reshape(-1,1))
    result = algo.predict(pen = 400)
    
    result = np.insert(result, 0, 0)
    
    
    #clustering --> DBSCAN
    n_bkp = len(result)
    segments = np.zeros((n_bkp, 2), dtype = int )
    
    #extracción features 
    for row in range(n_bkp):
        
        if row == 0:
            continue
        else:
            segments[row,0] = result[row-1]
            segments[row,1] = result[row]
    
    
    #El primero se quita
    segments = segments[1:]
    

    cfg = tsfel.get_features_by_domain()
    
    
    features_data = pd.DataFrame([])
    
    for row, segment in enumerate(segments):
        begin, end = segment
            
        features = tsfel.time_series_features_extractor(cfg, series[begin:end])
        
        features_data = pd.concat([features_data, features], ignore_index = True)
    
    
    features_data = features_data.dropna(axis = 1)
    
    #normalize data
    X = normalize(features_data)
    
      
    #clustering
    clustering = DBSCAN(eps=2e-3, min_samples=2).fit(X)
    
    
    features_data['label'] = clustering.labels_+1
    
    labels = features_data['label'].to_numpy()
    
    data['label'] = 0
    data['execution'] = 0
    
    #assign label and execution enumeration to segment
    for index, segment in enumerate(segments):
        
        label = labels[index]
        begin, end = segment
        
        #assign cluster label to segment
        data.loc[begin:end, 'label'] = label
        
        #enumerate executions
        data.loc[begin:end, 'execution'] = index+1
            
        
    executions = data['execution'].unique()
    
      
    color_list = ['red', 'blue', 'purple', 'black', 'green', 'orange', 'gray', 
                  'mediumslateblue', 'lime', 'brown', 'gold', 'firebrick', 'cyan',
                  'violet', 'crimson', 'coral', 'magenta', 'deeppink', 'lightpink',
                  'navy', 'darkorange', 'burlywood', 'gainsboro', 'turquoise']
    end = time.time()
    
    for execution in executions:
        
        label = data.loc[data['execution'] == execution, 'label'].iloc[0]
        begin, end = segments[execution-1]
        
        x_range = np.arange(begin, end)
        plt.plot(x_range, series[begin:end], color = color_list[label], label = 'Cluster {}'.format(label))
    
    plt.savefig(os.path.join(output_folder, 'patterns_simulated_signal_{}_{}.png'.format(suffix, m)))
    plt.close()
    
    unique_labels = data['label'].unique()
    var_clusters = np.zeros(len(unique_labels))

    for label in unique_labels:
        
        label_var = data.loc[data['label'] == label, 'current'].var()
        
        var_clusters[label] = label_var
        
        
    main_motif = np.argmax(var_clusters)
    
    final = time.time()
    
    #"olvidarse" de los otros clusters
    data.loc[data['label'] != main_motif, 'label'] = 0
    data.loc[data['label'] == main_motif, 'label'] = 1
    
    
    pred_ops = data['label'].to_numpy()
    data['pred_op_ex'] = get_ops(pred_ops)
    data['op_ex'] = get_ops(true_ops)
    
    #plot
    X = list()
    label_ex = data.loc[data['label'] == 1, 'pred_op_ex'].unique()
    for execution in label_ex:
        series = data.loc[data['pred_op_ex'] == execution, 'current'].to_numpy()
        
        X.append(list(series))
        plt.plot(series, lw = 2, alpha = .4, color = 'gray')
        
    plt.title('Simulated Signal m = {}'.format(m), fontsize = 20)
    plt.ylabel('Simulated Signal',fontsize = 15)
    plt.xlabel('Time',fontsize = 15)
    plt.savefig(os.path.join(output_folder, 'patterns_simulated_signal_{}_SUPERPUESTOS_{}.png'.format(suffix, m)))
    plt.close()
    
    #get centroid
    
    centroid = get_centroid(X)
    
    sse = get_sse(centroid, X)
    nrmse = get_nrmse(centroid, X)
    
    results = {'params': [m]}
    
    
    results['w'] = [m]
    results['overlap_rate'] = [overlap_rate(pred_ops, true_ops)]
    results['true_positive_rate'] = [true_positive_rate(pred_ops, true_ops)]
    results['false_discovery_rate'] = [false_discovery_rate(pred_ops, true_ops)]
    results['sse'] = [sse]
    results['nrmse'] = [nrmse]
    results['n_matches'] = [len(label_ex)]
    results['run_time'] = [final-start]
    
    
    #store results
    results_file = os.path.join(output_folder, 'results_{}.json'.format(suffix))
    
    store_results(results, results_file)
    
    return True
    

