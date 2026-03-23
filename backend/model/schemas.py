#defines input and output data shapes
from pydantic import BaseModel
from typing import List, Optional, Dict


class SourceRecord(BaseModel):
    system: str
    medication: str
    last_updated: Optional[str] = None
    last_filled: Optional[str] = None
    source_reliability: str


class PatientContext(BaseModel):
    age: int
    conditions: List[str]
    recent_labs: Optional[Dict[str, float]] = None


class ReconcileMedicationRequest(BaseModel):
    patient_context: PatientContext
    sources: List[SourceRecord]


class ReconcileMedicationResponse(BaseModel):
    reconciled_medication: str
    confidence_score: float
    reasoning: str
    recommended_actions: List[str]
    clinical_safety_check: str


class DataQualityRequest(BaseModel):
    demographics: Dict
    medications: List[str]
    allergies: List[str]
    conditions: List[str]
    vital_signs: Dict
    last_updated: str


class DataQualityResponse(BaseModel):
    overall_score: int
    breakdown: Dict[str, int]
    issues_detected: List[Dict]