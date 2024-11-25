'''
This code uses a .mat file with time series, then evaluates Granger Causality using grangercausalitytests
from statsmodels and creates heat maps. Make sure your data label is 'data', and ensure the order is correct.
To use it, just replace the first list with your file names and your path.
'''
from pathlib import Path
from granger_causality import granger_test, extract_p_values, matrix
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import seaborn as sns
file ='SUJETO_'
edf_pre = ['482','490','621','638','652','654','733','907','5225','5958','5975','6025']
edf_post = ['855','828','5655','841','846','1079','830','1070','851','698','867','849']
PRE = Path('./SUJETOS_DE_PRUEBA/PRE/All_signals/Matlab')
POST = Path('./SUJETOS_DE_PRUEBA/POST/All_signals/Matlab')
variable_names = ['VLF','LF','HF',r'$\delta$',r'$\theta$', r'$\alpha$', r'$\beta$', r'$\gamma$']
p_matrix_sum = np.zeros((8, 8))

print('Pre tratamiento')
for edf_file in edf_pre: 
    edf_path = PRE.joinpath(f"{file}{edf_file}.mat") 
    #print(edf_path )
    mat_path = PRE.joinpath('Heat_maps_nlc',f"{file}{edf_file}.mat") 
    mat = scipy.io.loadmat(edf_path, simplify_cells=True)
    data = mat['data']
    data = data.T

    bands = {
        'VLF': data[:,0],
        'LF': data[:,1],
        'HF': data[:,2],
        'delta': data[:,3],
        'theta': data[:,4],
        'alpha': data[:,5],
        'beta': data[:,6],
        'gamma': data[:,7]
     }

    results = granger_test(bands)
    p = extract_p_values(results)
    p_matrix = matrix(p)
    p_matrix_sum += p_matrix
    
p_matrix_pre = p_matrix_sum
plt.figure(figsize=(10, 8))  #
sns.heatmap(p_matrix_pre, annot=True, cmap="Greys", cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names)
plt.title("GC Before Therapy")
plt.xlabel("Target")
plt.ylabel("Source")

p_matrix_sum = np.zeros((8, 8))
print('Post tratamiento')
for edf_file in edf_post: 
    edf_path = POST.joinpath(f"{file}{edf_file}.mat") 
    #print(edf_path)
    mat_path = POST.joinpath('Heat_maps_nlc',f"{file}{edf_file}.mat") 
    mat = scipy.io.loadmat(edf_path, simplify_cells=True)
    data = mat['data']
    data = data.T

    bands = {
        'VLF': data[:,0],
        'LF': data[:,1],
        'HF': data[:,2],
        'delta': data[:,3],
        'theta': data[:,4],
        'alpha': data[:,5],
        'beta': data[:,6],
        'gamma': data[:,7]
     }

    results = granger_test(bands)
    p = extract_p_values(results)
    p_matrix = matrix(p)
    p_matrix_sum += p_matrix
    
p_matrix_post = p_matrix_sum
plt.figure(figsize=(10, 8))  
sns.heatmap(p_matrix_post, annot=True, cmap="Greys", cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names)
plt.title("GC After Therapy")
plt.xlabel("Target")
plt.ylabel("Source")

plt.show()