'''
This code obtains the normalized power bands of the ECG.
'''
import numpy as np
from scipy.signal import resample
from Pan_tompkin import pan_tompkin 
from scipy.interpolate import interp1d
from scipy import signal

def PowerHRV_normalized_bands(ekg_original, fs_original, duracion_ventana=300, solapamiento=270):
    # 1. Remuestrear a 400 Hz
    num_samples = int(len(ekg_original) * 400 / fs_original)
    ekg_400hz = resample(ekg_original, num_samples)
    
    # 2. Aplicar Pan-Tompkins para detectar picos R
    r_peaks = pan_tompkin(ekg_400hz, 400)
    
    # 3. Calcular intervalos RR y remuestrear a 8 Hz
    rr_intervals = np.diff(r_peaks) / 400
    t_rr = np.cumsum(rr_intervals)
    t_8hz = np.arange(t_rr[0], t_rr[-1], 1/8)
    rr_8hz = interp1d(t_rr, rr_intervals, kind='linear', bounds_error=False, fill_value='extrapolate')(t_8hz)
    
    # 4. Dividir en ventanas de 300 segundos con 270 segundos de solapamiento
    muestras_por_ventana = int(duracion_ventana * 8)  # 300 segundos * 8 Hz
    solapamiento_muestras = int(solapamiento * 8)  # 270 segundos * 8 Hz
    ventanas_rr = [rr_8hz[i:i+muestras_por_ventana] for i in range(0, len(rr_8hz) - muestras_por_ventana + 1, muestras_por_ventana - solapamiento_muestras)]
    
    vlf_list, lf_list, hf_list = [], [], []
    potencia_total_hrv = 0
    
    for ventana in ventanas_rr:
        # 5. Detrend, aplicar ventana Hanning, y calcular FFT
        ventana_detrend = signal.detrend(ventana)
        ventana_hann = ventana_detrend * signal.windows.hann(len(ventana_detrend))
        fft = np.fft.rfft(ventana_hann)
        freq = np.fft.rfftfreq(len(ventana_hann), d=1/8)
        potencia = np.abs(fft)**2
        
        # Calcular potencias en las bandas de frecuencia
        idx_vlf = (freq >= 0.003) & (freq < 0.04)
        idx_lf = (freq >= 0.04) & (freq < 0.15)
        idx_hf = (freq >= 0.15) & (freq <= 0.4)
        idx_hrv = (freq >= 0.003) & (freq <= 0.4)
        
        vlf = np.sum(potencia[idx_vlf])
        lf = np.sum(potencia[idx_lf])
        hf = np.sum(potencia[idx_hf])
        potencia_total_hrv += np.sum(potencia[idx_hrv])
        
        vlf_list.append(vlf)
        lf_list.append(lf)
        hf_list.append(hf)
    
    # 6. Normalizar VLF, LF y HF con respecto a la potencia total del HRV en todo el registro
    vlf_norm = [vlf / potencia_total_hrv for vlf in vlf_list]
    lf_norm = [lf / potencia_total_hrv for lf in lf_list]
    hf_norm = [hf / potencia_total_hrv for hf in hf_list]
    
    return vlf_norm, lf_norm, hf_norm
