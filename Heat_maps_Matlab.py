'''
This code creates heat maps from a .mat data file obtained from MuTe (linue). To use it, change the list of file names and the path.
Make sure the variables order is correct. 
'''
from pathlib import Path
import scipy.io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

prefix = 'SUJETO_'
pre_n = ['482','490','621','638','652','654','733','907','5225','5958','5975','6025']
post_n = ['698','828','830','841','846','849','851','855','867','1070','1079','5655']
PRE = Path('./SUJETOS_DE_PRUEBA/PRE/All_signals/Matlab')
POST = Path('./SUJETOS_DE_PRUEBA/POST/All_signals/Matlab')
folder = 'entropyMatrices'
file = 'linue_reshapedSignificance.mat'
variable_names = ['VLF','LF','HF',r'$\delta$',r'$\theta$', r'$\alpha$', r'$\beta$', r'$\gamma$']
matrix_sum = np.zeros((8, 8))

for n in pre_n:
    result_path = PRE.joinpath(f"{prefix}{n}", f"{folder}{n}",file) 
    linue = scipy.io.loadmat(result_path)
    matrix = linue['reshapedSigni']
    matrix_sum += matrix
    print(f"{n} done")
    
plt.figure(figsize=(10, 8))  
sns.heatmap(matrix_sum, annot=True, cmap="Greys", cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names)

plt.title("GC Before Therapy")
plt.xlabel("Target")
plt.ylabel("Source")
matrix_sum = np.zeros((8, 8))
  
for n in post_n:
    result_path = POST.joinpath(f"{prefix}{n}", f"{folder}{n}",file) 
    linue = scipy.io.loadmat(result_path)
    matrix = linue['reshapedSigni']
    matrix_sum += matrix
    print(f"{n} done")
    
plt.figure(figsize=(10, 8)) 
sns.heatmap(matrix_sum, annot=True, cmap="Greys", cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names)

plt.title("GC After Therapy")
plt.xlabel("Target")
plt.ylabel("Source")
plt.show()