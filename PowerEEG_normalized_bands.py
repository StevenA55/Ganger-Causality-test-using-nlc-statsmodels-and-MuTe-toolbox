'''
This code obtains the normalized power bands of the EEG.
'''
import numpy as np
from scipy.signal import butter, filtfilt, detrend
from scipy.fft import fft, next_fast_len

def PowerEEG_normalized_bands(z, sr, timew_sec=30):
    # Establece el vector con la información de los índices iniciales y finales de las ventanas de tiempo
    lims_ixs = [[0, sr * timew_sec]]

    i = 1
    while max(lims_ixs[-1]) + sr * timew_sec - 1 < len(z):
        lims_ixs.append([lims_ixs[i-1][1], lims_ixs[i-1][1] + sr * timew_sec])
        i += 1
    lims_ixs = np.array(lims_ixs)[0:]

    # Elimina la tendencia de la serie de tiempo EEG
    z_prime = detrend(z)

    # Aplica un filtro pasa banda con frecuencias de corte de 0.01 - 45 Hz
    b, a = butter(20, 45/(sr/2))
    x_prime = filtfilt(b, a, z_prime)

    b, a = butter(3, 0.01/(sr/2), btype='high')
    x = filtfilt(b, a, x_prime)

    PowEEG_each_timew_sec_delta = []
    PowEEG_each_timew_sec_theta = []
    PowEEG_each_timew_sec_alpha = []
    PowEEG_each_timew_sec_beta = []
    PowEEG_each_timew_sec_gamma = []

    for i in range(len(lims_ixs)):
        y = x[int(lims_ixs[i, 0]):int(lims_ixs[i, 1])]
        NFFT = next_fast_len(len(y))
        FFT_Y = fft(y, NFFT) / len(y)
        f = sr / 2 * np.linspace(0, 1, NFFT // 2 + 1)

        ix_delta = np.where((f >= 0.5) & (f < 3))[0]
        ix_theta = np.where((f >= 3) & (f < 8))[0]
        ix_alpha = np.where((f >= 8) & (f < 12))[0]
        ix_beta = np.where((f >= 12) & (f < 16))[0]
        ix_gamma = np.where((f >= 16) & (f < 25))[0]

        SpectrumEEG = 2 * np.abs(FFT_Y[:NFFT // 2 + 1])
        PowEEG_each_timew_sec_delta.append(np.trapz(SpectrumEEG[ix_delta]))
        PowEEG_each_timew_sec_theta.append(np.trapz(SpectrumEEG[ix_theta]))
        PowEEG_each_timew_sec_alpha.append(np.trapz(SpectrumEEG[ix_alpha]))
        PowEEG_each_timew_sec_beta.append(np.trapz(SpectrumEEG[ix_beta]))
        PowEEG_each_timew_sec_gamma.append(np.trapz(SpectrumEEG[ix_gamma]))

    mean_PowEEG_delta = np.mean(PowEEG_each_timew_sec_delta)
    mean_PowEEG_theta = np.mean(PowEEG_each_timew_sec_theta)
    mean_PowEEG_alpha = np.mean(PowEEG_each_timew_sec_alpha)
    mean_PowEEG_beta = np.mean(PowEEG_each_timew_sec_beta)
    mean_PowEEG_gamma = np.mean(PowEEG_each_timew_sec_gamma)
    
    Power_delta = []
    Power_theta = []
    Power_alpha = []
    Power_beta = []
    Power_gamma = []
    

    for ix_timew_sec in range(len(lims_ixs)):
        ix_5sec = np.arange(lims_ixs[ix_timew_sec, 0], lims_ixs[ix_timew_sec, 1], 5 * sr)

        PowEEG_5sec_delta = []
        PowEEG_5sec_theta = []
        PowEEG_5sec_alpha = []
        PowEEG_5sec_beta = []
        PowEEG_5sec_gamma = []

        for iy in range(len(ix_5sec) - 1):
            eeg_5sec = detrend(x[int(ix_5sec[iy]):int(ix_5sec[iy+1])])

            NFFT = next_fast_len(len(eeg_5sec))
            FFT_EEG_5sec = fft(eeg_5sec, NFFT) / len(eeg_5sec)
            f = sr / 2 * np.linspace(0, 1, NFFT // 2 + 1)

            ix_delta = np.where((f >= 0.5) & (f < 3))[0]
            ix_theta = np.where((f >= 3) & (f < 8))[0]
            ix_alpha = np.where((f >= 8) & (f < 12))[0]
            ix_beta = np.where((f >= 12) & (f < 16))[0]
            ix_gamma = np.where((f >= 16) & (f < 25))[0]

            SpectrumEEG = 2 * np.abs(FFT_EEG_5sec[:NFFT // 2 + 1])

            PowEEG_5sec_delta.append(np.trapz(SpectrumEEG[ix_delta]))
            PowEEG_5sec_theta.append(np.trapz(SpectrumEEG[ix_theta]))
            PowEEG_5sec_alpha.append(np.trapz(SpectrumEEG[ix_alpha]))
            PowEEG_5sec_beta.append(np.trapz(SpectrumEEG[ix_beta]))
            PowEEG_5sec_gamma.append(np.trapz(SpectrumEEG[ix_gamma]))

        Power_delta.append(np.mean(PowEEG_5sec_delta) / mean_PowEEG_delta)
        Power_theta.append(np.mean(PowEEG_5sec_theta) / mean_PowEEG_theta)
        Power_alpha.append(np.mean(PowEEG_5sec_alpha) / mean_PowEEG_alpha)
        Power_beta.append(np.mean(PowEEG_5sec_beta) / mean_PowEEG_beta)
        Power_gamma.append(np.mean(PowEEG_5sec_gamma) / mean_PowEEG_gamma)

    return Power_delta, Power_theta, Power_alpha, Power_beta, Power_gamma

