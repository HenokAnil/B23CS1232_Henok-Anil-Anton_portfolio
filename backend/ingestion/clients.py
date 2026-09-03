import logging
from obspy.clients.fdsn import Client, RoutingClient
from obspy import UTCDateTime
import time

logger = logging.getLogger(__name__)

class EIDAClient:
    def __init__(self, retries=3, backoff_factor=2):
        self.client = RoutingClient("eida-routing")
        self.retries = retries
        self.backoff_factor = backoff_factor

    def fetch_waveforms(self, network, station, location, channel, starttime, endtime, attach_response=True):
        for attempt in range(self.retries):
            try:
                logger.info(f"Fetching EIDA waveform: {network}.{station}.{location}.{channel} "
                            f"from {starttime} to {endtime} (attempt {attempt+1}/{self.retries})")
                st = self.client.get_waveforms(
                    network=network,
                    station=station,
                    location=location,
                    channel=channel,
                    starttime=starttime,
                    endtime=endtime,
                    attach_response=attach_response
                )
                return st
            except Exception as e:
                logger.warning(f"EIDA fetch failed: {e}")
                if attempt < self.retries - 1:
                    time.sleep(self.backoff_factor ** attempt)
        logger.error(f"Failed to fetch EIDA waveform after {self.retries} attempts.")
        return None

class SCEDCClient:
    def __init__(self, retries=3, backoff_factor=2):
        self.client = Client("SCEDC")
        self.retries = retries
        self.backoff_factor = backoff_factor

    def fetch_waveforms(self, network, station, location, channel, starttime, endtime, attach_response=True):
        for attempt in range(self.retries):
            try:
                logger.info(f"Fetching SCEDC waveform: {network}.{station}.{location}.{channel} "
                            f"from {starttime} to {endtime} (attempt {attempt+1}/{self.retries})")
                st = self.client.get_waveforms(
                    network=network,
                    station=station,
                    location=location,
                    channel=channel,
                    starttime=starttime,
                    endtime=endtime,
                    attach_response=attach_response
                )
                return st
            except Exception as e:
                logger.warning(f"SCEDC fetch failed: {e}")
                if attempt < self.retries - 1:
                    time.sleep(self.backoff_factor ** attempt)
        logger.error(f"Failed to fetch SCEDC waveform after {self.retries} attempts.")
        return None
