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
pre_n = ['00000482-112835','00000490-113038','00000621-112873','00000638-112838','00000652-112795','00000654-112892',
           '00000733-113037','00000907-113040','00005225-LEBS18039','00005958-LEBS18046','00005975-LEBS18046',
           '00006025-LEBS18046']
post_n = ['00000855-112888','00000828-112888','00005655-LEBS20684','00000841-112888','00000846-112795','00001079-112837',
           '00000830-112892','00001070-112837','00000851-112888','00000698-112892','00000867-112888','00000849-113038']
PRE = Path('./SUJETOS_DE_PRUEBA/PRE/All_signals')
POST = Path('./SUJETOS_DE_PRUEBA/POST/All_signals')
num_files = 1
variable_names = ['VLF','LF','HF',r'$\delta$',r'$\theta$', r'$\alpha$', r'$\beta$', r'$\gamma$']
matrix_sum = np.zeros((8, 8))

for n in pre_n:
    result_path = PRE.joinpath(f"{n}.mat") 
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
matrix_sum = matrix_sum/ num_files
plt.figure(figsize=(10, 8))  
sns.heatmap(matrix_sum, annot=True, cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names,vmin=0,vmax=12,annot_kws={"fontsize": 18})

plt.title("GC Before Therapy")
plt.xlabel("Target")
plt.ylabel("Source")
matrix_sum = np.zeros((8, 8))
  
for n in post_n:
    result_path = POST.joinpath(f"{n}.mat") 
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
matrix_sum = matrix_sum/ num_files
plt.figure(figsize=(10, 8)) 
sns.heatmap(matrix_sum, annot=True, cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names,vmin=0,vmax=12,annot_kws={"fontsize": 18})

plt.title("GC After Therapy")
plt.xlabel("Target")
plt.ylabel("Source")
plt.show()