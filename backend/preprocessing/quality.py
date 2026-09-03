import numpy as np
from scipy.stats import kurtosis, entropy
from scipy.signal import welch

def compute_snr(trace_data, noise_window, signal_window):
    """
    Computes SNR given data and indices for noise and signal.
    """
    noise_rms = np.sqrt(np.mean(trace_data[noise_window]**2))
    signal_rms = np.sqrt(np.mean(trace_data[signal_window]**2))
    if noise_rms == 0:
        return 0.0
    return 20 * np.log10(signal_rms / noise_rms)

def compute_spectral_entropy(trace_data, fs=100.0):
    f, Pxx = welch(trace_data, fs, nperseg=256)
    Pxx_norm = Pxx / np.sum(Pxx)
    return entropy(Pxx_norm)

def extract_features(st):
    """
    Extract quality features from an obspy stream (assumes 3 components).
    """
    features = {}
    
    snrs = []
    entropies = []
    kurtosises = []
    clipping_flags = []
    
    for tr in st:
        data = tr.data
        if len(data) == 0:
            continue
            
        # Basic features
        kurt = kurtosis(data)
        kurtosises.append(kurt)
        
        spec_ent = compute_spectral_entropy(data, tr.stats.sampling_rate)
        entropies.append(spec_ent)
        
        # Clipping detection
        max_val = np.max(np.abs(data))
        if max_val > 0.95 * (2**23):  # Assuming 24-bit digitizer approx
            clipping_flags.append(True)
        else:
            clipping_flags.append(False)
            
        # Simple SNR (assuming event is in the middle, noise at start)
        n = len(data)
        if n > 200:
            noise_idx = slice(0, int(n * 0.1))
            sig_idx = slice(int(n * 0.4), int(n * 0.6))
            snr = compute_snr(data, noise_idx, sig_idx)
            snrs.append(snr)
            
    features['avg_snr'] = float(np.mean(snrs)) if snrs else 0.0
    features['avg_entropy'] = float(np.mean(entropies)) if entropies else 0.0
    features['avg_kurtosis'] = float(np.mean(kurtosises)) if kurtosises else 0.0
    features['is_clipped'] = any(clipping_flags)
    
    return features
