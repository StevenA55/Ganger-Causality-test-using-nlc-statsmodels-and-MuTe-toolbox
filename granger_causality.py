'''
This code generates a matrix with p-values (taking the minimum value) from the grangercausalitytests function in statsmodels.
You can change the number of lags.'''
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

def extract_p_values(results):
    p_values = []
    
    # Iterate over the results (which are now a list of tuples)
    for result in results:
        key, value = result  # Unpack the tuple (key is 'Y -> X', value is the results)
        
        # Initialize a list to store the p-values for each lag
        lag_p_values = []
        
        # Iterate over the lags and extract the p-value from the F-test
        for lag, lag_results in value.items():
            p_value = lag_results[0]['ssr_chi2test'][1]
            lag_p_values.append(p_value)
        
        # Calculate the minimum p-value
        min_p_value = np.min(lag_p_values)
        
        # Conditional to determine if there is causality or not
        if min_p_value < 0.05:
            min_p_value = 1
        else:
            min_p_value = 0
        
        # Add the result to the list of p-values
        p_values.append((key, min_p_value))
    
    # Sort the values by the key (Y -> X)
    #p_values_sorted_by_key = sorted(p_values, key=lambda x: x[0])
    
    return p_values
    
def matrix(p_values):
    h = 0
    p_matrix = np.zeros((8, 8))
    for i in range(8):
       for j in range(8):
           if i == j:
               p_matrix[i, j] = 0
           else:
               p_matrix[i, j] = p_values[h][1]
               
           h = h + 1
    
    return p_matrix

def granger_test(bands, max_lag=20):
    results = []
    band_names = list(bands.keys())

    for i in range(len(band_names)):
        for j in range(len(band_names)):
            # Combine the two bands for the test
            data = np.column_stack([bands[band_names[j]], bands[band_names[i]]])
            df = pd.DataFrame(data, columns=[band_names[j], band_names[i]])
            
            # Perform the Granger test
            result = grangercausalitytests(df, max_lag, verbose=False)
            results.append((f'{band_names[i]} -> {band_names[j]}', result))
            #results[f'{band_names[j]} -> {band_names[i]}'] = result
    
    return results
