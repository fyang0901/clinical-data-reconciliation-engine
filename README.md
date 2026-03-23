# Clinical Data Reconciliation & Quality Engine

## Overview
This project implements a mini clinical data processing engine designed to:

- Reconcile conflicting medication records from multiple sources  
- Evaluate patient data quality across key dimensions  
- Provide AI-assisted reasoning for clinical decision support  

The system simulates real-world Electronic Health Record (EHR) challenges such as inconsistent data, outdated records, and clinical safety risks.

---

## Architecture

## Architecture

**Frontend:** Streamlit Dashboard  
**Backend:** FastAPI REST API  

**Core Components:**
- Service Layer  
- Reconciliation Engine  
- Data Quality Engine  
- AI Reasoning Service  


---

## Features

### Medication Reconciliation
- Aggregates medication records from:
  - EHR systems
  - Primary care
  - Pharmacy sources
- Scores each source based on:
  - Reliability
  - Recency
- Outputs:
  - Reconciled medication
  - Confidence score
  - Clinical safety assessment (PASSED / CAUTION / REVIEW)
  - Recommended actions

---

### Confidence Scoring
Based on:
- Source reliability  
- Recency of data  
- Agreement across sources  

Higher agreement → higher confidence  
More conflicts → lower confidence  

---

### Clinical Safety Checks
Example:
- Metformin use with reduced eGFR  

Outputs:
- PASSED  
- CAUTION  
- REVIEW  

---

### Data Quality Validation

| Dimension | Description |
|----------|------------|
| Completeness | Missing or incomplete fields |
| Accuracy | Invalid or unrealistic values |
| Timeliness | Outdated records |
| Clinical Plausibility | Medically impossible values |

Detects issues such as:
- Missing allergies  
- Implausible vitals (e.g., BP 340/180)  
- Stale data (> 6 months old)  

---

### AI-Assisted Reasoning
- Explanation of medication selection  
- Clinical risk insights  
- Follow-up recommendations  
- LLM integration with fallback logic  

---

## API Endpoints

### POST `/api/reconcile/medication`

```json
{
  "patient_context": {
    "age": 67,
    "conditions": ["Type 2 Diabetes"]
  },
  "recent_labs": {
    "eGFR": 45
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
```

---

## How to Run the Engine
### 1.Backend
```
  uvicorn backend.main:app --reload --port 8010
```
### 2.Frontend
```
  python -m streamlit run frontend/app.py
```

### 3.Open in Browser
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.0.186:8501http://localhost:8501
```

---

## Author: Fangyilang Yang
