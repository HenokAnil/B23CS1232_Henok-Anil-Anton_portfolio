import pytest
import numpy as np
from obspy import Trace, Stream
from backend.preprocessing.pipeline import Preprocessor
from backend.preprocessing.quality import extract_features

@pytest.fixture
def dummy_stream():
    """Create a dummy 3-component stream for testing."""
    st = Stream()
    fs = 100.0
    t = np.arange(0, 30, 1/fs) # 30 seconds
    
    # Generate a dummy signal with a "pulse" in the middle
    data = np.random.normal(0, 1, len(t))
    pulse_start = int(10 * fs)
    pulse_end = int(15 * fs)
    data[pulse_start:pulse_end] += np.sin(2 * np.pi * 5 * t[pulse_start:pulse_end]) * 10
    
    for comp in ['Z', 'N', 'E']:
        tr = Trace(data=data.copy())
        tr.stats.network = 'XX'
        tr.stats.station = 'TEST'
        tr.stats.channel = f'BH{comp}'
        tr.stats.sampling_rate = fs
        st.append(tr)
        
    return st

def test_preprocessor(dummy_stream):
    preprocessor = Preprocessor(target_sampling_rate=50.0, freqmin=1.0, freqmax=20.0)
    processed_st = preprocessor.process(dummy_stream)
    
    assert len(processed_st) == 3
    for tr in processed_st:
        assert tr.stats.sampling_rate == 50.0
        # Check demean/detrend effects (mean should be close to 0)
        assert abs(np.mean(tr.data)) < 0.1

def test_quality_extraction(dummy_stream):
    features = extract_features(dummy_stream)
    
    assert 'avg_snr' in features
    assert 'avg_entropy' in features
    assert 'avg_kurtosis' in features
    assert 'is_clipped' in features
    
    assert features['avg_snr'] > 0
    assert not features['is_clipped']

def test_clipped_signal():
    st = Stream()
    data = np.zeros(1000)
    data[500] = 0.96 * (2**23) # Above threshold
    tr = Trace(data=data)
    tr.stats.sampling_rate = 100.0
    st.append(tr)
    
    features = extract_features(st)
    assert features['is_clipped'] is True
