from sqlalchemy.orm import Session
from backend.models.database import Event, Pick, Signal
from backend.models.detector import DetectionResult
import datetime

def populate_events_and_picks(db: Session, signal_id, detection_results: list[DetectionResult], model_version: str):
    """
    Takes detection results from the ML model and populates the events and picks tables.
    """
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        raise ValueError(f"Signal {signal_id} not found in database.")
    
    fs = signal.sample_rate
    start_time = signal.starttime # Assuming datetime with timezone
    
    for det in detection_results:
        # Calculate absolute time
        event_time = start_time + datetime.timedelta(seconds=det.event_start_sample / fs)
        
        # Create Event
        new_event = Event(
            signal_id=signal.id,
            origin_time=event_time,
            detection_prob=det.confidence,
            model_version=model_version,
            catalog_source="ml_model"
        )
        db.add(new_event)
        db.flush() # To get the new_event.id
        
        # Create Picks
        for pick in det.picks:
            pick_time = start_time + datetime.timedelta(seconds=pick.sample_index / fs)
            new_pick = Pick(
                event_id=new_event.id,
                signal_id=signal.id,
                phase=pick.phase,
                pick_time=pick_time,
                confidence=pick.confidence,
                model_version=model_version
            )
            db.add(new_pick)
            
    db.commit()
