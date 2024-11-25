'''
This code evaluates Granger causality (GC) using the nlc library and saves an 8x8 matrix in a .mat file.
To use it, replace the first list with your file names and your paths.
'''
from pathlib import Path
from non_lincausality import nonlincausality_f, matrix_nlc, save_mat
import scipy.io
file ='SUJETO_'
edf_pre = ['482','490','621','638','652','654','733','907','5225','5958','5975','6025']
edf_post = ['855','828','5655','841','846','1079','830','1070','851','698','867','849']
PRE = Path('./SUJETOS_DE_PRUEBA/PRE/All_signals/Matlab')
POST = Path('./SUJETOS_DE_PRUEBA/POST/All_signals/Matlab')
print('Pre tratamiento')
for edf_file in edf_pre: 
    edf_path = PRE.joinpath(f"{file}{edf_file}.mat") 
    print(edf_path )
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

    all_results, p_nlc = nonlincausality_f(bands,edf_file)
    p_matrix_nlc = matrix_nlc(p_nlc)
    save_mat(mat_path, p_matrix_nlc)

print('Post tratamiento')
for edf_file in edf_post: 
    edf_path = POST.joinpath(f"{file}{edf_file}.mat") 
    print(edf_path)
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

    p_nlc = nonlincausality_f(bands,edf_file)
    p_matrix_nlc = matrix_nlc(p_nlc)
    save_mat(mat_path, p_matrix_nlc)
