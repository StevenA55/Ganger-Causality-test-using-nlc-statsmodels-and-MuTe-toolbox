'''
This code takes EDF files organized by hour and creates a single EDF file combining all hours. 
Additionally, it checks the data. To use it, just replace the first list with your file names and your paths.
Uncomment the escribir line to save the combined EDF file.
'''

from pathlib import Path
import pyedflib 
from Check import check_data
from Write import escribir

edf_pre = ['00000482-112835','00000490-113038','00000621-112873','00000638-112838','00000652-112795','00000654-112892',
           '00000733-113037','00000907-113040','00005225-LEBS18039','00005958-LEBS18046','00005975-LEBS18046',
           '00006025-LEBS18046']
edf_post = ['00000855-112888','00000828-112888','00005655-LEBS20684','00000841-112888','00000846-112795','00001079-112837',
           '00000830-112892','00001070-112837','00000851-112888','00000698-112892','00000867-112888','00000849-113038']
PRE = Path('./SUJETOS_DE_PRUEBA/PRE')
POST = Path('./SUJETOS_DE_PRUEBA/POST')
test =[]
print('Pre tratamiento')   

for edf_file in edf_pre: 
    EEG = []
    ECG = []
    edf_path1 = PRE.joinpath(f"{edf_file}.edf") 
    for i in range (1, 11):
        file = f"{edf_file}[{i:03d}].edf"  
        #print(file)
        edf_path = PRE.joinpath(edf_file,file)
        #print(edf_path) 
        if edf_path.exists(): 
            #print(f"file's loading: {edf_path}")

            try:
                f = pyedflib.EdfReader(str(edf_path))
                
                EEG, ECG, sample_rate_eeg, sample_rate_ecg = check_data(f, file, EEG, ECG)

                f.close()
                #n_samples, sample_rate, signal = graficar_una_senal(f, i)
            except Exception as e:
                print(f"Error al cargar el archivo {edf_path}: {e}")
    
    #escribir(EEG, ECG, str(edf_path1), sample_rate_eeg, sample_rate_ecg)
         
print('Post tratamiento')      
       
for edf_file in edf_post: 
    EEG = []
    ECG = []
    edf_path1 = POST.joinpath(f"{edf_file}.edf") 
    for i in range (1, 11):
        file = f"{edf_file}[{i:03d}].edf" 
        #print(file)
        edf_path = POST.joinpath(edf_file,file)
        #print(edf_path) 
        if edf_path.exists():  
            #print(f"file's loading: {edf_path}")

            try:
                f = pyedflib.EdfReader(str(edf_path))

                EEG, ECG, sample_rate_eeg, sample_rate_ecg = check_data(f, file, EEG, ECG)
                f.close()
            except Exception as e:
                print(f"Error al cargar el archivo {edf_path}: {e}")

    #escribir(EEG, ECG, str(edf_path1),sample_rate_eeg, sample_rate_ecg)
