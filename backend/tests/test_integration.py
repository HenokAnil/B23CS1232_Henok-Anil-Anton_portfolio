import pytest
import os
from fastapi.testclient import TestClient
from backend.api.main import app, startup_event

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def init_app():
    startup_event()

def test_full_pipeline_workflow():
    sample_file = "sample_data/earthquake_station_CI_PAS.mseed"
    assert os.path.exists(sample_file), "Sample file should exist"

    # 1. Upload .mseed file
    with open(sample_file, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("earthquake_station_CI_PAS.mseed", f, "application/octet-stream")}
        )
    assert response.status_code == 200, f"Upload failed: {response.text}"
    upload_data = response.json()
    assert upload_data["status"] == "ok"
    assert "signal_id" in upload_data
    signal_id = upload_data["signal_id"]
    assert "quality" in upload_data
    assert upload_data["quality"]["noise_label"] in ["clean", "wind_noise", "traffic_noise", "instrument_glitch", "calibration_pulse"]

    # 2. Get waveform data for plotting
    wf_response = client.get(f"/waveform/{signal_id}")
    assert wf_response.status_code == 200
    wf_data = wf_response.json()
    assert len(wf_data["traces"]) >= 1
    assert "times" in wf_data["traces"][0]
    assert "data" in wf_data["traces"][0]

    # 3. Run ML Inference (Quality + EQTransformer + 1D-CNN + Qdrant)
    infer_response = client.post(f"/infer/{signal_id}")
    assert infer_response.status_code == 200
    infer_data = infer_response.json()
    assert infer_data["status"] == "ok"
    res = infer_data["result"]
    assert "event_id" in res
    event_id = res["event_id"]
    assert len(res["picks"]) >= 1
    # Check that at least P or S phase was picked
    phases = [p["phase"] for p in res["picks"]]
    assert "P" in phases or "S" in phases

    # 4. Get Event details
    event_response = client.get(f"/events/{event_id}")
    assert event_response.status_code == 200
    event_json = event_response.json()
    assert event_json["event_id"] == event_id
    assert len(event_json["picks"]) >= 1

    # 5. Query Vector DB Similar Events
    similar_response = client.get(f"/similar/{event_id}")
    assert similar_response.status_code == 200
    similar_json = similar_response.json()
    assert "results" in similar_json

    # 6. Generate and download ReportLab PDF
    report_response = client.get(f"/report/{event_id}")
    assert report_response.status_code == 200
    assert report_response.headers["content-type"] == "application/pdf"
    assert len(report_response.content) > 1000  # Valid PDF size
