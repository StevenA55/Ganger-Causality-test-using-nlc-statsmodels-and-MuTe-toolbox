'''
This code creates a new edf file with two signals (EEG and ECG).
'''
import pyedflib
import numpy as np

def escribir(EEG, ECG, edf_path1, sample_rate_eeg, sample_rate_ecg):
    EEG = np.array(EEG)
    ECG = np.array(ECG)
    '''
    if len(EEG) != len(ECG):
        print("Error: The EEG and ECG signals must have the same number of samples.")
        return
    '''
    label = ["EEG", "ECG"]
    signal_headers = []


    eeg_physical_min = np.min(EEG)
    eeg_physical_max = np.max(EEG)
    
    ecg_physical_min = np.min(ECG)  
    ecg_physical_max = np.max(ECG)

    signal_headers.append({
        "label": "EEG",
        "sample_rate": sample_rate_eeg,
        "physical_min": eeg_physical_min,  
        "physical_max": eeg_physical_max,  
        "digital_min": -32768,  
        "digital_max": 32767,   
    })

    signal_headers.append({
        "label": "ECG",
        "sample_rate": sample_rate_ecg,
        "physical_min": ecg_physical_min,  
        "physical_max": ecg_physical_max, 
        "digital_min": -32768,  
        "digital_max": 32767,   
    })

    try:
        with pyedflib.EdfWriter(edf_path1, 2) as f:
            f.setSignalHeaders(signal_headers)
            f.writeSamples(np.array([EEG, ECG]),digital=False)

    except (OSError, ValueError) as e:
        print(f"Error al crear el archivo {edf_path1}: {e}")


    