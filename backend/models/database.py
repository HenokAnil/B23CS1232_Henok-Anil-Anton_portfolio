from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Signal(Base):
    __tablename__ = 'signals'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network = Column(String, nullable=False)
    station = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    location = Column(String)
    starttime = Column(DateTime(timezone=True), nullable=False)
    endtime = Column(DateTime(timezone=True), nullable=False)
    sample_rate = Column(Float, nullable=False)
    s3_key = Column(String, nullable=False, unique=True)
    source = Column(String)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())
    quality = relationship("SignalQuality", back_populates="signal", uselist=False)

class Station(Base):
    __tablename__ = 'stations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network = Column(String)
    station = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    elevation = Column(Float)
    sensor_type = Column(String)

class SignalQuality(Base):
    __tablename__ = 'signal_quality'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True), ForeignKey('signals.id'))
    snr = Column(Float)
    rms = Column(Float)
    noise_label = Column(String)
    clipping_flag = Column(Boolean, default=False)
    quality_score = Column(Float)
    features_json = Column(JSONB)
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
    signal = relationship("Signal", back_populates="quality")

class Event(Base):
    __tablename__ = 'events'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True), ForeignKey('signals.id'))
    origin_time = Column(DateTime(timezone=True))
    detection_prob = Column(Float)
    magnitude_proxy = Column(Float)
    model_version = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    depth = Column(Float)
    catalog_source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Pick(Base):
    __tablename__ = 'picks'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'))
    signal_id = Column(UUID(as_uuid=True), ForeignKey('signals.id'))
    phase = Column(String)
    pick_time = Column(DateTime(timezone=True))
    confidence = Column(Float)
    uncertainty_s = Column(Float)
    model_version = Column(String)

class ProcessingRun(Base):
    __tablename__ = 'processing_runs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True), ForeignKey('signals.id'))
    run_type = Column(String)
    status = Column(String, default='pending')
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    config_json = Column(JSONB)
    error_msg = Column(String)
