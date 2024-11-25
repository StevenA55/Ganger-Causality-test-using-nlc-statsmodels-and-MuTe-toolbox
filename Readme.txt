This repository aims to evaluate Granger causality using nlc and statsmodels on data from EEG C3-A2 and ECG I during sleep apnea. 
The data is preprocessed to obtain 8 bands, then causality is evaluated, and finally, heat maps are generated.

To use this, you need to update the paths and file names, as the database is not shared due to privacy concerns. 
Run the HRV file if you already have an EDF file containing EEG and ECG signals. Please note that the EEG signal should be on channel 0, 
and the ECG signal should be on channel 1. If you have multiple EDF files and wish to combine them, run the Main_N code. 
For MuTe execution in Matlab, please refer to its documentation, as the provided code does not include any Matlab scripts. 
Files containing the word "matlab" are intended for time series in .mat format or for generating heat maps of MuTe results.