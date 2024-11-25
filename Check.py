'''
This checks the data. f is the EDF file, file is the name of the data, and EEG and ECG are the extend signals.
'''
import numpy as np
from scipy.stats import zscore

def check_data(f, file, EEG, ECG):
    try:
        num_signals = f.signals_in_file
        signal_names = f.getSignalLabels()
        #sample_rate = f.getSampleFrequency(0)
        '''
        if sample_rate != 200:
            print(f"{file} tiene fs igual a: {sample_rate}")
        '''
        index_EEG = -1
        index_ECG = -1

        for i in range(len(signal_names)):
            if signal_names[i] == 'EEG C3-A2' and index_EEG == -1:
                index_EEG = i  
        
            if signal_names[i] == 'ECG I' and index_ECG == -1: 
                index_ECG = i
                     
        if index_EEG != -1:
            #print(f"{file} has EEG C3-A2")
            type = 'EEG'
            signal = f.readSignal(index_EEG)
            sample_rate_eeg = f.getSampleFrequency(index_EEG)
            EEG.extend(signal)
            # outliers
            z_scores = zscore(signal)
            outliers = np.where(np.abs(z_scores) > 3)
            percent = len(outliers[0])/len(signal)*100

            if percent > 5.0:
                print(f"Discard the signal {file}, outliers: {percent:.3f}%;{index_EEG}")
                
        if index_EEG == -1:
            print(f"{file} NO tiene EEG C3-A2")
            
        if index_ECG != -1:
            #print(f"{file} has ECG I")
            type = 'ECG'
            signal = f.readSignal(index_ECG)
            sample_rate_ecg = f.getSampleFrequency(index_ECG)

            ECG.extend(signal)
            # outliers
            z_scores = zscore(signal)
            outliers = np.where(np.abs(z_scores) > 3)
            N = int(f.getNSamples()[index_ECG])
            percent = (len(outliers[0])/N)*100

            if percent > 5.0:
               print(f"Discard {file}, outliers: {percent:.3f}%;{index_ECG}")
                
        if index_ECG == -1:
            print(f"{file} NO tiene ECG I")
            
        # Check signal duration
        for i in range(num_signals):
            n_samples = f.getNSamples()[i]
            sample_rate = f.getSampleFrequency(i)
            #print(sample_rate)
            duration = n_samples / sample_rate
                
              
        #if duration/3600 < 0.5:
        #    print(f"Signal duration {file} is: {duration/3600:.3f} h ")
        

        #print("Verification complete.\n")

    except Exception as e:
        print(f"Verification error: {e}; {file}; {index_ECG}")
        
    return EEG, ECG, sample_rate_eeg, sample_rate_ecg