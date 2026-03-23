import json
import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8010"

st.set_page_config(
    page_title="Clinical Data Reconciliation Engine(Mini Version)",
    layout="wide"
)

st.title("Clinical Data Reconciliation Engine(Mini Version)")
st.write("A mini full-stack dashboard for medication reconciliation and patient data quality review.")

page = st.sidebar.selectbox(
    "Choose a workflow",
    ["Medication Reconciliation", "Data Quality Validation"]
)

# ---------------------------
# Medication Reconciliation
# ---------------------------
if page == "Medication Reconciliation":
    st.header("Medication Reconciliation")

    default_payload = {
        "patient_context": {
            "age": 67,
            "conditions": ["Type 2 Diabetes", "Hypertension"],
            "recent_labs": {"eGFR": 45}
        },
        "sources": [
            {
                "system": "Hospital EHR",
                "medication": "Metformin 1000mg twice daily",
                "last_updated": "2024-10-15",
                "source_reliability": "high"
            },
            {
                "system": "Primary Care",
                "medication": "Metformin 500mg twice daily",
                "last_updated": "2025-01-20",
                "source_reliability": "high"
            },
            {
                "system": "Pharmacy",
                "medication": "Metformin 1000mg daily",
                "last_filled": "2025-01-25",
                "source_reliability": "medium"
            }
        ]
    }

    payload_text = st.text_area(
        "Input JSON",
        value=json.dumps(default_payload, indent=2),
        height=350
    )

    if st.button("Run Reconciliation"):
        try:
            payload = json.loads(payload_text)

            with st.spinner("Analyzing patient data..."):
                response = requests.post(
                    f"{API_BASE_URL}/api/reconcile/medication",
                    json=payload,
                    timeout=60
                )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Reconciliation Summary")

                st.markdown("### Selected Medication")
                st.success(result.get("reconciled_medication", "N/A"))

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Confidence Score", result.get("confidence_score", "N/A"))

                with col2:
                    safety = result.get("clinical_safety_check", "UNKNOWN")
                    if safety == "PASSED":
                        st.success(f"Safety: {safety}")
                    elif safety == "CAUTION":
                        st.warning(f"Safety: {safety}")
                    else:
                        st.error(f"Safety: {safety}")

                st.markdown("### Reasoning")
                reasoning = result.get("reasoning", "No reasoning returned.")
                st.info(reasoning)


                st.markdown("### Recommended Actions")
                actions = result.get("recommended_actions", [])
                if actions:
                    for action in actions:
                        st.markdown(f"- {action}")
                else:
                    st.info("No recommended actions returned.")

                st.markdown("### Clinician Review")
                col3, col4 = st.columns(2)

                with col3:
                    if st.button("Approve", type = "primary"):
                        st.success("Suggestion marked as approved.")

                with col4:
                    if st.button("Reject", type = "secondary"):
                        st.warning("Suggestion marked as rejected.")

            else:
                st.error(f"Request failed with status code {response.status_code}")
                st.code(response.text, language="json")

        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check your input.")
        except requests.exceptions.RequestException as e:
            st.error(f"API request error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# ---------------------------
# Data Quality Validation
# ---------------------------
else:
    st.header("Data Quality Validation")

    default_payload = {
        "demographics": {
            "name": "John Doe",
            "dob": "1955-03-15",
            "gender": "M"
        },
        "medications": ["Metformin 500mg", "Lisinopril 10mg"],
        "allergies": [],
        "conditions": ["Type 2 Diabetes"],
        "vital_signs": {
            "blood_pressure": "340/180",
            "heart_rate": 72
        },
        "last_updated": "2024-06-15"
    }

    payload_text = st.text_area(
        "Input JSON",
        value=json.dumps(default_payload, indent=2),
        height=350
    )

    if st.button("Validate Data"):
        try:
            payload = json.loads(payload_text)

            with st.spinner("Evaluating data quality..."):
                response = requests.post(
                    f"{API_BASE_URL}/api/validate/data-quality",
                    json=payload,
                    timeout=60
                )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Validation Summary")

                overall_score = result.get("overall_score", 0)
                if overall_score >= 80:
                    st.success(f"Overall Score: {overall_score}")
                elif overall_score >= 60:
                    st.warning(f"Overall Score: {overall_score}")
                else:
                    st.error(f"Overall Score: {overall_score}")

                st.markdown("### Breakdown")
                breakdown = result.get("breakdown", {})

                if breakdown:
                    col1, col2 = st.columns(2)
                    items = list(breakdown.items())

                    for i, (key, value) in enumerate(items):
                        label = key.replace("_", " ").title()
                        if i % 2 == 0:
                            with col1:
                                st.metric(label, value)
                        else:
                            with col2:
                                st.metric(label, value)
                else:
                    st.write("No breakdown returned.")

                st.markdown("### Issues Detected")
                issues = result.get("issues_detected", [])

                if issues:
                    for issue in issues:
                        severity = issue.get("severity", "unknown").lower()
                        message = (
                            f"**{issue.get('field', 'Unknown field')}**: "
                            f"{issue.get('issue', 'No issue description')} "
                            f"({issue.get('severity', 'unknown severity')})"
                        )

                        if severity == "high":
                            st.error(message)
                        elif severity == "medium":
                            st.warning(message)
                        else:
                            st.info(message)
                else:
                    st.success("No issues detected.")

            else:
                st.error(f"Request failed with status code {response.status_code}")
                st.code(response.text, language="json")

        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check your input.")
        except requests.exceptions.RequestException as e:
            st.error(f"API request error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")