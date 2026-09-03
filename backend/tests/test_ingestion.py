import pytest
from unittest.mock import patch, MagicMock
from obspy import UTCDateTime, Stream, Trace
from backend.ingestion.clients import EIDAClient, SCEDCClient

@pytest.fixture
def mock_stream():
    tr = Trace()
    tr.stats.network = 'XX'
    tr.stats.station = 'TEST'
    return Stream(traces=[tr])

@patch('backend.ingestion.clients.RoutingClient')
def test_eida_client_success(mock_routing_client, mock_stream):
    mock_instance = mock_routing_client.return_value
    mock_instance.get_waveforms.return_value = mock_stream
    
    client = EIDAClient(retries=1)
    st = client.fetch_waveforms('XX', 'TEST', '', 'BHZ', UTCDateTime(), UTCDateTime())
    
    assert st is not None
    assert len(st) == 1
    mock_instance.get_waveforms.assert_called_once()

@patch('backend.ingestion.clients.RoutingClient')
def test_eida_client_retry(mock_routing_client):
    mock_instance = mock_routing_client.return_value
    mock_instance.get_waveforms.side_effect = Exception("Network error")
    
    client = EIDAClient(retries=2, backoff_factor=0.1) # Fast retries for testing
    st = client.fetch_waveforms('XX', 'TEST', '', 'BHZ', UTCDateTime(), UTCDateTime())
    
    assert st is None
    assert mock_instance.get_waveforms.call_count == 2

@patch('backend.ingestion.clients.Client')
def test_scedc_client_success(mock_client, mock_stream):
    mock_instance = mock_client.return_value
    mock_instance.get_waveforms.return_value = mock_stream
    
    client = SCEDCClient(retries=1)
    st = client.fetch_waveforms('CI', 'TEST', '', 'BHZ', UTCDateTime(), UTCDateTime())
    
    assert st is not None
    assert len(st) == 1
    mock_instance.get_waveforms.assert_called_once()
