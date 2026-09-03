from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import asyncio

app = FastAPI(title="SeismoDetect API", version="1.0.0")

# CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FetchRequest(BaseModel):
    network: str
    station: str
    channel: str
    starttime: str
    endtime: str
    source: str = "scedc"

@app.post("/upload")
async def upload_waveform(file: UploadFile = File(...)):
    """Uploads a local .mseed file."""
    # Logic to save to MinIO and Postgres goes here
    signal_id = str(uuid.uuid4())
    return {"status": "ok", "signal_id": signal_id, "filename": file.filename}

@app.post("/fetch")
async def fetch_waveform(req: FetchRequest, background_tasks: BackgroundTasks):
    """Fetches waveform from EIDA or SCEDC."""
    signal_id = str(uuid.uuid4())
    
    # In a real app, we'd trigger a Celery task here.
    # background_tasks.add_task(celery_fetch_task, req, signal_id)
    
    return {"status": "accepted", "signal_id": signal_id, "message": "Fetching in background"}

@app.post("/infer/{signal_id}")
async def run_inference(signal_id: str):
    """Triggers ML detection and picking pipeline."""
    # Logic to trigger celery task for preprocessing + EQT
    return {"status": "accepted", "message": "Inference started"}

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    """Returns event details and picks."""
    # Mock data
    return {
        "event_id": event_id,
        "origin_time": "2021-01-01T00:00:15Z",
        "magnitude_proxy": 2.5,
        "picks": [
            {"phase": "P", "time": "2021-01-01T00:00:18Z", "confidence": 0.95},
            {"phase": "S", "time": "2021-01-01T00:00:23Z", "confidence": 0.88}
        ]
    }

@app.get("/similar/{event_id}")
async def get_similar_events(event_id: str, limit: int = 5):
    """Queries Qdrant for similar events based on CNN embeddings."""
    # Mock data
    return {
        "results": [
            {"similar_event_id": str(uuid.uuid4()), "score": 0.98, "time": "2020-05-12T..."},
            {"similar_event_id": str(uuid.uuid4()), "score": 0.85, "time": "2019-11-20T..."}
        ]
    }

@app.get("/report/{event_id}")
async def generate_report(event_id: str):
    """Generates PDF report for an event."""
    return {"status": "ok", "download_url": f"/static/reports/{event_id}.pdf"}

@app.websocket("/ws/infer/{signal_id}")
async def websocket_endpoint(websocket: WebSocket, signal_id: str):
    """Streams inference progress to frontend."""
    await websocket.accept()
    try:
        # Mock streaming progress
        for progress in [10, 30, 50, 80, 100]:
            await asyncio.sleep(1)
            await websocket.send_json({"signal_id": signal_id, "progress": progress})
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
