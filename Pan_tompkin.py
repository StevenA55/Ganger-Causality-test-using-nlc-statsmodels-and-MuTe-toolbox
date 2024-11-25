# Pan-Tompkins algorithm.
import numpy as np
from scipy.signal import butter, lfilter, find_peaks

def butter_lowpass(cutoff, fs, order=2):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_highpass(cutoff, fs, order=2):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def pan_tompkin(ecg, fs, gr=0):
    # Filtro de paso bajo
    b_lp, a_lp = butter_lowpass(15, fs, order=2)
    ecg_l = lfilter(b_lp, a_lp, ecg)
    ecg_l = ecg_l / np.max(np.abs(ecg_l))
    
    # Filtro de paso alto
    b_hp, a_hp = butter_highpass(0.5, fs, order=2)
    ecg_h = lfilter(b_hp, a_hp, ecg_l)
    ecg_h = ecg_h / np.max(np.abs(ecg_h))

    # Derivación
    ecg_d = np.diff(ecg_h)
    ecg_d = ecg_d / np.max(np.abs(ecg_d))
    
    # Cuadrado
    ecg_s = ecg_d ** 2
    
    # Media móvil
    window_size = int(0.150 * fs)
    ecg_m = np.convolve(ecg_s, np.ones(window_size)/window_size, mode='same')

    # Encontrar picos
    locs, _ = find_peaks(ecg_m, distance=int(0.2 * fs))

    return locs

