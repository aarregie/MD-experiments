# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:10:47 2024

@author: aarregui
"""



import os
import pandas as pd
import numpy as np
import json
from tslearn.barycenters import softdtw_barycenter
from tslearn.metrics import dtw



def generate_pred_ops(matches, len_series, window_size):
    pred_ops = np.zeros(len_series)
    for match in matches[:, 1]:
        begin, end = match, match+window_size
        pred_ops[begin:end] = 1
    
    return pred_ops



def get_ops(ops):
    
    true_op_ex = np.diff(ops)
    #enumeramos las ejecuciones de las distintas operaciones (POR AHORA, indiferentemente)
    true_op_ex = np.where(true_op_ex<=0, 0, 1)
    true_op_ex = np.insert(true_op_ex, 0, true_op_ex[0]).cumsum()
    true_op_ex[ops == 0] = 0
    
    return true_op_ex




#EVALUATION
def overlap_rate(pred_ops, true_ops):
    
    overlap_rate = 0
    
    true_positive = ((pred_ops == 1) & (true_ops == 1)).sum()
    truepred = ((pred_ops == 1) | (true_ops == 1)).sum()
    overlap_rate = true_positive/truepred
    
    return overlap_rate



def true_positive_rate(pred_ops, true_ops):

    true_positive_rate = 0
    
    true_and_pred = ((pred_ops == 1) & (true_ops == 1)).sum()
    pred = (pred_ops == 1).sum()
    true_positive_rate = true_and_pred/pred  

    return true_positive_rate




def false_discovery_rate(pred_ops, true_ops):
    
    false_discovery_rate = 0
    
    pred = (true_ops == 1).sum()
    false_positive = ((pred_ops == 0) & (true_ops == 1)).sum()
    
    false_discovery_rate = false_positive/pred
    
    return false_discovery_rate



def get_matches_by_start(series, m, start_idx):

    
    X = list()
    
    for start in start_idx:
        begin, end = start, start+m
        match_seq = series[begin:end]
        X.append(list(match_seq))
        
    return X
        


def get_centroid(X):
    
    
    centroid = softdtw_barycenter(X, gamma=1., max_iter=50, tol=1e-3)    
    centroid = np.array(centroid).flatten()
    
    return centroid
    



def get_nrmse(centroid, matches):
    
    Dm = np.array([])
    max_length = 0
    
    for match in matches:
        match = np.array([match]).flatten()
        
        match_length = len(match)
        if match_length>max_length:
            max_length = match_length
            
        d_m = dtw(centroid, match)
        Dm = np.append(Dm, d_m)

    #ponderar por longitud de serie
    #Zm = Dm/max_length
    #normalize
    #Zm = (Dm - Dm.mean())/Dm.std()
    
    ssz = np.sum(Zm**2)
    mse = ssz/len(matches)    
    nrmse = np.sqrt(mse)
    
    
    return nrmse




def get_sse(centroid, matches):
    
    sse = 0
    ds = list()
    
    for match in matches:
        
        match = np.array([match]).flatten()
        d_m = dtw(centroid, match)
        ds.append(d_m)
        sse += d_m**2
    
    
    return sse


def store_results(results, results_file):
    
    
    if os.path.isfile(results_file):
        
        results_to_store = {}
        with open(results_file, "r") as outfile: 
            
            other_results = json.load(outfile)
                        
            for key, value in other_results.items():
                new_value_list = value + results[key]
                results_to_store[key] = new_value_list
            
        with open(results_file, 'w') as outfile:
            json.dump(results_to_store, outfile)
            
            
    else:
        with open(results_file, 'w') as outfile:
            json.dump(results, outfile)
    outfile.close()
    
    
    return True