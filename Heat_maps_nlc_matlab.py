'''
This code uses a .mat file with a matrix 8x8 and creates heat maps. 
Make sure your data label is 'data', and ensure the order is correct.
To use it, just replace the first list with your file names and your path.
'''
from pathlib import Path
import scipy.io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

prefix = 'SUJETO_'
pre_n = ['482','490','621','638','652','654','733','907','5225','5958','5975','6025']
post_n = ['855','828','5655','841','846','1079','830','1070','851','698','867','849']
PRE = Path('./SUJETOS_DE_PRUEBA/PRE/All_signals/Matlab/Heat_maps_nlc_100_neurons')
POST = Path('./SUJETOS_DE_PRUEBA/POST/All_signals/Matlab/Heat_maps_nlc_100_neurons')
variable_names = ['VLF','LF','HF',r'$\delta$',r'$\theta$', r'$\alpha$', r'$\beta$', r'$\gamma$']
matrix_sum = np.zeros((8, 8))

for n in pre_n:
    result_path = PRE.joinpath(f"{prefix}{n}.mat") 
    nlc = scipy.io.loadmat(result_path)
    matrix = nlc['matrix_nlc']
    for i in range(8):
        for j in range(8):
            if i == j:
                matrix[i][j]=0
            elif matrix[i][j]<0.05:
                matrix[i][j]=1
            else:
                matrix[i][j]=0
    matrix_sum += matrix

plt.figure(figsize=(10, 8))
sns.heatmap(matrix_sum, annot=True, cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names,vmin=0,vmax=12,annot_kws={"fontsize": 18})

plt.title("GC Before Therapy")
plt.xlabel("Target")
plt.ylabel("Source")
matrix_sum = np.zeros((8, 8))
  
for n in post_n:
    result_path = POST.joinpath(f"{prefix}{n}.mat") 
    nlc = scipy.io.loadmat(result_path)
    matrix = nlc['matrix_nlc']
    for i in range(8):
        for j in range(8):
            if i == j:
                matrix[i][j]=0
            elif matrix[i][j]<0.05:
                matrix[i][j]=1
            else:
                matrix[i][j]=0
    matrix_sum += matrix

plt.figure(figsize=(10, 8))
sns.heatmap(matrix_sum, annot=True, cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names,vmin=0,vmax=12,annot_kws={"fontsize": 18})

plt.title("GC After Therapy")
plt.xlabel("Target")
plt.ylabel("Source")
plt.show()