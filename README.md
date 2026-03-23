# Clinical Data Reconciliation & Quality Engine

## Overview

This project implements a mini clinical data processing engine designed to:
- reconcile conflicting medication records from multiple sources
- evaluate patient data quality across key dimensions
- provide AI-assisted reasoning for clinical decision support

The system simulates real-world Electronic Health Record (EHR) challenges such as inconsistent data, outdated records, and clinical safety risks.

------------------------------------------------------------------------

## Architecture
Frontend (Streamlit Dashboard)
↓
Backend (FastAPI REST API)
↓
Service Layer
├── Reconciliation Engine
├── Data Quality Engine
└── AI Reasoning Service


------------------------------------------------------------------------

## Features

### Medication Reconciliation
- Aggregates medication records from multiple sources (EHR, Primary Care, Pharmacy)
- Scores each source using:
  - Reliability
  - Recency
- Selects the most appropriate medication
- Outputs:
  - Reconciled medication
  - Confidence score
  - Clinical safety assessment (PASSED / CAUTION / REVIEW)
  - Recommended actions

------------------------------------------------------------------------

### Confidence Scoring
- Based on:
  - Source reliability
  - Recency of data
  - Disagreement between sources
- Higher agreement → higher confidence
- More conflicting data → lower confidence

------------------------------------------------------------------------

### Clinical Safety Checks
- Example implemented:
  - Metformin use with reduced eGFR
- Provides safety classification:
  - PASSED
  - CAUTION
  - REVIEW

------------------------------------------------------------------------

### Data Quality Validation

Evaluates patient records across four dimensions:

| Dimension | Description |
|----------|------------|
| Completeness | Missing or incomplete fields |
| Accuracy | Invalid or unrealistic values |
| Timeliness | Outdated records |
| Clinical Plausibility | Medically impossible values |

Detects issues such as:
- Missing allergies
- Implausible vital signs (e.g., BP 340/180)
- Stale data (6+ months old)

------------------------------------------------------------------------

### AI-Assisted Reasoning
- Generates:
  - Explanation of medication selection
  - Clinical risk insights
  - Follow-up recommendations
- Uses LLM integration
- Includes fallback logic if API fails

------------------------------------------------------------------------

### Frontend Dashboard (Streamlit)
- Interactive interface for:
  - Medication reconciliation
  - Data quality validation
- Displays:
  - Confidence scores
  - Safety indicators
  - AI reasoning
  - Recommended actions
- Includes clinician-style workflow:
  - Approve / Reject suggestions

------------------------------------------------------------------------

## API Endpoints

### 1. Medication Reconciliation
POST /api/reconcile/medication


**Input Example:**
```json
{
  "patient_context": {
    "age": 67,
    "conditions": ["Type 2 Diabetes"],
    "recent_labs": { "eGFR": 45 }
  },
  "sources": [
    {
      "system": "Primary Care",
      "medication": "Metformin 500mg twice daily",
      "last_updated": "2025-01-20",
      "source_reliability": "high"
    }
  ]
}
**Output Example:**
{
  "reconciled_medication": "Metformin 500mg twice daily",
  "confidence_score": 0.82,
  "reasoning": "...",
  "recommended_actions": [...],
  "clinical_safety_check": "CAUTION"
}


### Data Quality Validation
POST /api/validate/data-quality
**Input Example:**
```json
{
  "demographics": {
    "name": "John Doe",
    "dob": "1955-03-15",
    "gender": "M"
  },
  "medications": ["Metformin 500mg"],
  "allergies": [],
  "conditions": ["Type 2 Diabetes"],
  "vital_signs": {
    "blood_pressure": "340/180",
    "heart_rate": 72
  },
  "last_updated": "2024-06-15"
}
**Output Example:**
```json
{
  "overall_score": 55,
  "breakdown": {
    "completeness": 60,
    "accuracy": 50,
    "timeliness": 70,
    "clinical_plausibility": 40
  },
  "issues_detected": [...]
}

------------------------------------------------------------------------

### Testing

- Unit tests were implemented to validate core logic, including:
  - medication reconciliation scoring
  - clinical safety checks
  - data quality validation
- Synthetic test cases were used to simulate realistic clinical scenarios, including:
  - conflicting medication sources
  - missing data
  - implausible vital signs

------------------------------------------------------------------------

##PyHealth-style Data Integration

This project simulates structured EHR data using a PyHealth-inspired model:

 - Patient → collection of clinical events
 - Event → diagnosis, medication, lab, etc.

An adapter layer converts this format into the API schema:
    PyHealth-style data → Adapter → API → Engine

------------------------------------------------------------------------

##How to run the engine:
    1. Backend: 
        uvicorn backend.main:app --reload --port 8010
    2. Frontend: 
        python -m streamlit run frontend/app.py
    3. Open in browser: 
        Local URL: http://localhost:8501
        Network URL: http://192.168.0.186:8501http://localhost:8501
    4. Run batch test: 
        python -m tests.batch_test_pyhealth

## Future Improvements
    - Integrate real EHR datasets (e.g., MIMIC via PyHealth)
    - Expand clinical rules (drug interactions, contraindications)
    - Replace scoring logic with ML models
    - Add authentication and logging
    - Deploy to cloud (Azure / AWS)


AUTHOR
Fangyilang Yang
Master's in Data Science and Applications
University at Buffalo