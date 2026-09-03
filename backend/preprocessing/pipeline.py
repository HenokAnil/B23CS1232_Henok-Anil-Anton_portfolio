import numpy as np
from obspy import Stream
import logging

logger = logging.getLogger(__name__)

class Preprocessor:
    def __init__(self, target_sampling_rate=100.0, freqmin=1.0, freqmax=20.0):
        self.target_sampling_rate = target_sampling_rate
        self.freqmin = freqmin
        self.freqmax = freqmax

    def process(self, st: Stream, remove_response=False):
        """
        Processes a raw obspy Stream.
        """
        st = st.copy()
        
        # 1. Detrend and demean
        st.detrend("demean")
        st.detrend("linear")
        
        # 2. Remove response if requested (needs response info attached)
        if remove_response:
            try:
                st.remove_response(output="VEL", pre_filt=(0.5, 1.0, 45.0, 50.0))
            except Exception as e:
                logger.warning(f"Could not remove response: {e}")
                
        # 3. Filter
        st.filter("bandpass", freqmin=self.freqmin, freqmax=self.freqmax, corners=4)
        
        # 4. Resample
        for tr in st:
            if tr.stats.sampling_rate != self.target_sampling_rate:
                tr.resample(self.target_sampling_rate)
                
        # 5. Merge and return
        st.merge(method=1, fill_value=0)
        return st
