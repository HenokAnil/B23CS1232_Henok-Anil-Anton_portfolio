import numpy as np
import os
from obspy import Stream, Trace, UTCDateTime

def create_sample_mseed(output_dir="sample_data"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 60 seconds at 100 Hz = 6000 samples
    n_samples = 6000
    sampling_rate = 100.0
    t0 = UTCDateTime()
    times = np.linspace(0, 60, n_samples)
    
    # Components: Z, N, E
    np.random.seed(42)
    
    for filename, snr_factor in [("earthquake_station_CI_PAS.mseed", 1.0), ("clean_event_BK_PKD.mseed", 1.5)]:
        # Background noise
        noise_z = np.random.normal(0, 50, n_samples)
        noise_n = np.random.normal(0, 50, n_samples)
        noise_e = np.random.normal(0, 50, n_samples)
        
        # P-wave arrival at 18.0s, dominant on Z
        p_idx = int(18.0 * sampling_rate)
        p_len = int(10.0 * sampling_rate)
        p_t = np.linspace(0, 10, p_len)
        p_wave = 400 * snr_factor * np.sin(2 * np.pi * 5.0 * p_t) * np.exp(-p_t / 2.0)
        
        # S-wave arrival at 26.5s, dominant on N and E
        s_idx = int(26.5 * sampling_rate)
        s_len = int(15.0 * sampling_rate)
        s_t = np.linspace(0, 15, s_len)
        s_wave_n = 750 * snr_factor * np.sin(2 * np.pi * 2.5 * s_t) * np.exp(-s_t / 3.5)
        s_wave_e = 600 * snr_factor * np.cos(2 * np.pi * 2.5 * s_t) * np.exp(-s_t / 3.5)
        
        data_z = noise_z.copy()
        data_z[p_idx:p_idx+p_len] += p_wave
        data_z[s_idx:s_idx+s_len] += (s_wave_n * 0.3)
        
        data_n = noise_n.copy()
        data_n[p_idx:p_idx+p_len] += (p_wave * 0.2)
        data_n[s_idx:s_idx+s_len] += s_wave_n
        
        data_e = noise_e.copy()
        data_e[p_idx:p_idx+p_len] += (p_wave * 0.2)
        data_e[s_idx:s_idx+s_len] += s_wave_e
        
        traces = []
        for comp, data in [('HHZ', data_z), ('HHN', data_n), ('HHE', data_e)]:
            tr = Trace(data=data.astype(np.float32))
            tr.stats.network = "CI"
            tr.stats.station = "PAS"
            tr.stats.channel = comp
            tr.stats.sampling_rate = sampling_rate
            tr.stats.starttime = t0
            traces.append(tr)
            
        st = Stream(traces=traces)
        filepath = os.path.join(output_dir, filename)
        st.write(filepath, format="MSEED")
        print(f"Created sample seismic file: {filepath}")

if __name__ == "__main__":
    create_sample_mseed()
