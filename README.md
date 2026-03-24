# Clinical Data Reconciliation & Data Quality Engine

## Overview
This project implements a mini clinical data processing engine designed to:

- Reconcile conflicting medication records from multiple sources  
- Evaluate patient data quality across key dimensions  
- Provide AI-assisted reasoning for clinical decision support  

The system simulates real-world Electronic Health Record (EHR) challenges such as inconsistent data, outdated records, and clinical safety risks.

---

## Architecture

**Frontend:** Streamlit Dashboard  
**Backend:** FastAPI REST API  

**Core Components:**
- Service Layer  
- Reconciliation Engine  
- Data Quality Engine  
- AI Reasoning Service  

### LLM API Used
This project uses the OpenAI API for AI-assisted clinical reasoning.
Why OpenAI?
  - Strong performance in structured reasoning tasks
  - Reliable output formatting for clinical explanations
  - Easy integration with Python backend (FastAPI)
  - Supports rapid prototyping for decision-support systems

---

## Key Design Decisions & Trade-offs

### 1. Hybrid Approach (Rule-based + LLM)
- **Decision:** Combine deterministic rules with LLM-based reasoning  
- **Reason:** Clinical systems require both interpretability and flexibility  
- **Trade-off:**  
  -  More reliable and explainable  
  -  Increased system complexity  

---

### 2. FastAPI + Streamlit Architecture
- **Decision:** Separate backend API and frontend dashboard  
- **Reason:** Improves modularity, testing, and scalability  
- **Trade-off:**  
  -  Slight setup overhead  
  -  Better maintainability  

---

### 3. Rule-based Confidence Scoring
- **Decision:** Score based on reliability, recency, and agreement  
- **Reason:** Ensures transparency in decision-making  
- **Trade-off:**  
  -  Easy to interpret  
  -  Less adaptive than ML-based approaches  

---

### 4. Synthetic Data Simulation
- **Decision:** Use simulated EHR-like data  
- **Reason:** Avoid privacy constraints and enable rapid development  
- **Trade-off:**  
  -  Less realistic than production data  
  -  Safe and flexible for experimentation  

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

## How to Run the Engine Locally

### 1. Clone the Repository
```bash
git clone https://github.com/fyang0901/clinical-data-reconciliation-engine.git
cd clinical-data-reconciliation-engine
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Requirements
```bash
  pip install -r requirements.txt
```

### 4. Set API Key
```bash
  OPENAI_API_KEY=your_api_key_here
```

### 5. Backend(FastAPI)
```bash
  uvicorn backend.main:app --reload --port 8010
```
### 6. Frontend(Streamlit)
```bash
  python -m streamlit run frontend/app.py
```

### 7. Open in Browser and Access the Application
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.0.186:8501http://localhost:8501
```

---

## What can I improve next?
- Integrate with real EHR datasets and format adapters
- Replace rule-based scoring with ML models
- Expand clinical rules
- Better UI for better user experience
- Add authentication, logging features
- Deploy to cloud
- Add automated evaluation metrics for model outputs

---

## ⏱️ Estimated Time Spent: ~ 8 hours total

---
## Author: Fangyilang Yang
