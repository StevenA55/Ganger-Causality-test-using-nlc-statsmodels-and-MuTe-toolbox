'''
This is the main code to obtain the 8 power bands and evaluate Granger Causality using statsmodels
and NLC (uncomment the specific lines; it is not recommended to run NLC without using a GPU). 
This code plots the 8 power series and the heat maps obtained with the Granger Causality test.
Therefore, if you comment out the Granger Causality test lines, you should also comment out the heat map lines.
To use it, just replace the first list with your file names and your paths.
'''
from pathlib import Path
import pyedflib 
import numpy as np
import matplotlib.pyplot as plt
from PowerEEG_normalized_bands import PowerEEG_normalized_bands
from PowerHRV_normalized_bands import PowerHRV_normalized_bands
from granger_causality import granger_test, extract_p_values, matrix
from non_lincausality import nonlincausality_f, matrix_nlc, save_mat
import seaborn as sns
#from csv_own import save

edf_pre = ['00000482-112835','00000490-113038','00000621-112873','00000638-112838','00000652-112795','00000654-112892',
           '00000733-113037','00000907-113040','00005225-LEBS18039','00005958-LEBS18046','00005975-LEBS18046',
           '00006025-LEBS18046']
edf_post = ['00000855-112888','00000828-112888','00005655-LEBS20684','00000841-112888','00000846-112795','00001079-112837',
           '00000830-112892','00001070-112837','00000851-112888','00000698-112892','00000867-112888','00000849-113038']
PRE = Path('./SUJETOS_DE_PRUEBA/PRE/All_signals')
POST = Path('./SUJETOS_DE_PRUEBA/POST/All_signals')
variable_names = ['VLF','LF','HF',r'$\delta$',r'$\theta$', r'$\alpha$', r'$\beta$', r'$\gamma$']
p_matrix_sum = np.zeros((8, 8))
num_files = 1 #len(edf_pre) use it if you want a average
print('Pre tratamiento')
for edf_file in edf_pre: 
    edf_path = PRE.joinpath(edf_file, f"{edf_file}.edf") 
    mat_path = PRE.joinpath(f"{edf_file}.mat") 
    try:
        ECG = []
        EEG = []
        Power_delta, Power_theta, Power_alpha, Power_beta, Power_gamma = [], [], [], [], []
        P_VLF, P_LF, P_HF = [], [], []
        f = pyedflib.EdfReader(str(edf_path))
        sample_rate = f.getSampleFrequency(0)
        EEG = f.readSignal(0)
        Power_delta, Power_theta, Power_alpha, Power_beta, Power_gamma = PowerEEG_normalized_bands(EEG, sample_rate)
        ECG = f.readSignal(1)
        sample_rate = f.getSampleFrequency(1)
        P_VLF, P_LF, P_HF = PowerHRV_normalized_bands(ECG, sample_rate)

        while len(P_VLF) != len(Power_delta):
            Power_delta.pop(-1)
            Power_theta.pop(-1)
            Power_alpha.pop(-1)
            Power_beta.pop(-1)
            Power_gamma.pop(-1)
        f.close()
        #save([Power_delta,Power_theta,Power_alpha,Power_beta,Power_gamma,P_HF,P_LF,P_VLF],'Bandas_'+edf_file,PRE)
        bands = {
            'VLF': P_VLF,
            'LF': P_LF,
            'HF': P_HF,
            'delta': Power_delta,
            'theta': Power_theta,
            'alpha': Power_alpha,
            'beta': Power_beta,
            'gamma': Power_gamma
         }
        '''
        p_nlc = nonlincausality_f(bands,edf_file)
        p_matrix_nlc = matrix_nlc(p_nlc)
        save_mat(mat_path, p_matrix_nlc)
        '''
        results = granger_test(bands)
        
        p = extract_p_values(results)
        
        p_matrix = matrix(p)
        
        p_matrix_sum += p_matrix
        
        fig, axs = plt.subplots(8, 1, figsize=(10, 10))
        
        axs[0].plot(Power_delta, color='b')
        axs[0].set_title('Power Delta')
        axs[0].set_ylabel('Potencia')

        axs[1].plot(Power_theta, color='g')
        axs[1].set_title('Power Theta')
        axs[1].set_ylabel('Potencia')

        axs[2].plot(Power_alpha, color='r')
        axs[2].set_title('Power Alpha')
        axs[2].set_ylabel('Potencia')

        axs[3].plot(Power_beta, color='m')
        axs[3].set_title('Power Beta')
        axs[3].set_ylabel('Potencia')
        
        axs[4].plot(Power_gamma, color='c')
        axs[4].set_title('Power Gamma')
        axs[4].set_ylabel('Potencia')
        
        axs[5].plot(P_VLF, color='c')
        axs[5].set_title('Very Low Frecuency')
        axs[5].set_ylabel('Potencia')
        
        axs[6].plot(P_LF, color='g')
        axs[6].set_title('Low Frecuency')
        axs[6].set_ylabel('Potencia')

        axs[7].plot(P_HF, color='r')
        axs[7].set_title('High Frecuency')
        axs[7].set_ylabel('Potencia')
        axs[7].set_xlabel('Muestras')
        
        plt.tight_layout()

    except Exception as e:
        f.close()
        print(f"Error al cargar el archivo {edf_path}: {e}")

p_matrix_pre = p_matrix_sum / num_files

plt.figure(figsize=(10, 8))  
sns.heatmap(p_matrix_pre, annot=True, cmap="Greys", cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names)

plt.title("GC Before Therapy")
plt.xlabel("Target")
plt.ylabel("Source")

p_matrix_sum = np.zeros((8, 8))

print('Post tratamiento')
for edf_file in edf_post: 
    edf_path = POST.joinpath(edf_file, f"{edf_file}.edf") 
    mat_path = POST.joinpath(f"{edf_file}.mat") 
    try:
        ECG = []
        EEG = []
        Power_delta, Power_theta, Power_alpha, Power_beta, Power_gamma = [], [], [], [], []
        P_VLF, P_LF, P_HF = [], [], []
        f = pyedflib.EdfReader(str(edf_path))
        sample_rate = f.getSampleFrequency(0)
        EEG = f.readSignal(0)
        Power_delta, Power_theta, Power_alpha, Power_beta, Power_gamma = PowerEEG_normalized_bands(EEG, sample_rate)
        ECG = f.readSignal(1)
        sample_rate = f.getSampleFrequency(1)
        P_VLF, P_LF, P_HF = PowerHRV_normalized_bands(ECG, sample_rate)
        
        while len(P_VLF) != len(Power_delta):
            Power_delta.pop(-1)
            Power_theta.pop(-1)
            Power_alpha.pop(-1)
            Power_beta.pop(-1)
            Power_gamma.pop(-1)
        
        f.close()
        #save([Power_delta,Power_theta,Power_alpha,Power_beta,Power_gamma,P_HF,P_LF,P_VLF],'Bandas_'+edf_file,POST)
        bands = {
            'VLF': P_VLF,
            'LF': P_LF,
            'HF': P_HF,
            'delta': Power_delta,
            'theta': Power_theta,
            'alpha': Power_alpha,
            'beta': Power_beta,
            'gamma': Power_gamma
         }
        '''
        p_nlc = nonlincausality_f(bands,edf_file)
        p_matrix_nlc = matrix_nlc(p_nlc)
        save_mat(mat_path, p_matrix_nlc)
        '''
        result = granger_test(bands)
        p = extract_p_values(result)
        p_matrix = matrix(p)
        
        p_matrix_sum += p_matrix
        
        
        fig, axs = plt.subplots(8, 1, figsize=(10, 10))
        
        axs[0].plot(Power_delta, color='b')
        axs[0].set_title('Power Delta')
        axs[0].set_ylabel('Potencia')

        axs[1].plot(Power_theta, color='g')
        axs[1].set_title('Power Theta')
        axs[1].set_ylabel('Potencia')

        axs[2].plot(Power_alpha, color='r')
        axs[2].set_title('Power Alpha')
        axs[2].set_ylabel('Potencia')

        
        axs[3].plot(Power_beta, color='m')
        axs[3].set_title('Power Beta')
        axs[3].set_ylabel('Potencia')
        
        axs[4].plot(Power_gamma, color='c')
        axs[4].set_title('Power Gamma')
        axs[4].set_ylabel('Potencia')
        
        axs[5].plot(P_VLF, color='c')
        axs[5].set_title('Very Low Frecuency')
        axs[5].set_ylabel('Potencia')
        
        axs[6].plot(P_LF, color='g')
        axs[6].set_title('Low Frecuency')
        axs[6].set_ylabel('Potencia')

        axs[7].plot(P_HF, color='r')
        axs[7].set_title('High Frecuency')
        axs[7].set_ylabel('Potencia')
        axs[7].set_xlabel('Muestras')
        
        plt.tight_layout()
 
    except Exception as e:
        f.close()
        print(f"Error al cargar el archivo {edf_path}: {e}")
  
p_matrix_post = p_matrix_sum / num_files

plt.figure(figsize=(10, 8))
sns.heatmap(p_matrix_post, annot=True, cmap="Greys", cbar=True, linewidths=0.5, square=True,
            xticklabels=variable_names, yticklabels=variable_names)

plt.title("GC After Therapy")
plt.xlabel("Target")
plt.ylabel("Source")

plt.show()
