#starts FastAPI server and defines API routes and call functions from services.
from fastapi import FastAPI
from backend.model.schemas import (
    ReconcileMedicationRequest,
    ReconcileMedicationResponse,
    DataQualityRequest,
    DataQualityResponse
)
from backend.services.reconciliation import reconcile_medications
from backend.services.data_quality import validate_data_quality

app = FastAPI(title="Clinical Data Reconciliation Engine")


@app.get("/")
def home():
    return {"message": "API is working"}


@app.post("/api/reconcile/medication", response_model=ReconcileMedicationResponse)
def reconcile_medication_endpoint(data: ReconcileMedicationRequest):
    return reconcile_medications(data)


@app.post("/api/validate/data-quality", response_model=DataQualityResponse)
def validate_data_quality_endpoint(data: DataQualityRequest):
    return validate_data_quality(data)