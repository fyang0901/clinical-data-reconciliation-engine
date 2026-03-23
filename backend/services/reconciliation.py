#logic for deciding most likely medication with LLMs
from datetime import datetime
from backend.services.ai_service import get_ai_response


def reliability_score(level: str) -> int:
    mapping = {
        "high": 3,
        "medium": 2,
        "low": 1
    }
    return mapping.get(level.lower(), 0)


def recency_score(date_str):
    if not date_str:
        return 0

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        days_old = (datetime.now() - date_obj).days

        if days_old <= 30:
            return 3
        elif days_old <= 90:
            return 2
        else:
            return 1
    except Exception:
        return 0


def build_reconciliation_prompt(data, best_source, safety_check, actions):
    return f"""
You are assisting with clinical medication reconciliation.

Patient context:
- Age: {data.patient_context.age}
- Conditions: {data.patient_context.conditions}
- Recent labs: {data.patient_context.recent_labs}

Conflicting medication sources:
{[{
    "system": s.system,
    "medication": s.medication,
    "last_updated": s.last_updated,
    "last_filled": s.last_filled,
    "source_reliability": s.source_reliability
} for s in data.sources]}

Selected medication:
- {best_source.medication}

Current safety assessment:
- {safety_check}

Suggested actions:
- {actions}

Write a concise clinician-friendly explanation in 3 short bullet points:
- Why this medication was selected
- Any clinical safety concern
- Recommended follow-up

Keep it short, clear, and practical.
""".strip()


def determine_safety_check(best_source, patient_context):
    egfr = None
    if patient_context.recent_labs:
        egfr = patient_context.recent_labs.get("eGFR")

    medication_text = best_source.medication.lower()
    safety = "PASSED"

    if egfr is not None and "metformin" in medication_text:
        if egfr < 45:
            safety = "REVIEW"
        elif egfr <= 60:
            safety = "CAUTION"

    return safety, egfr


def build_recommended_actions(data, best_source, safety_check, egfr):
    actions = []
    actions.append("Review conflicting records across systems")

    systems = [s.system.lower() for s in data.sources]
    if any("pharmacy" in system for system in systems):
        actions.append("Verify active prescription with the pharmacy")

    medication_text = best_source.medication.lower()
    if egfr is not None and "metformin" in medication_text:
        if egfr < 45:
            actions.append("Reassess metformin use due to reduced kidney function")
            actions.append("Confirm dose with the prescribing clinician")
        elif egfr <= 60:
            actions.append("Monitor renal function regularly while continuing metformin")

    if "primary care" in best_source.system.lower():
        actions.append("Update other systems to reflect the latest primary care medication record")

    return actions


def calculate_confidence(scored_sources):
    """
    Confidence is based on:
    1. strength of the winning source
    2. disagreement between sources

    More agreement -> higher confidence
    More conflict -> lower confidence
    """
    scores = [score for score, _ in scored_sources]

    if not scores:
        return 0.5

    best_score = max(scores)
    avg_score = sum(scores) / len(scores)

    # larger gap means more disagreement among sources
    disagreement = best_score - avg_score

    confidence = 0.6 + (best_score * 0.07) - (disagreement * 0.05)

    # keep in realistic range
    confidence = max(0.5, min(confidence, 0.99))
    return round(confidence, 2)


def reconcile_medications(data):
    scored_sources = []

    for source in data.sources:
        score = 0
        score += reliability_score(source.source_reliability)
        score += recency_score(source.last_updated or source.last_filled)

        egfr = None
        if data.patient_context.recent_labs:
            egfr = data.patient_context.recent_labs.get("eGFR")

        med_lower = source.medication.lower()

        # simple clinical penalty example
        if egfr is not None and egfr < 60 and "metformin 1000mg twice daily" in med_lower:
            score -= 2

        scored_sources.append((score, source))

    best_score, best_source = max(scored_sources, key=lambda x: x[0])

    confidence = calculate_confidence(scored_sources)

    safety_check, egfr = determine_safety_check(best_source, data.patient_context)
    recommended_actions = build_recommended_actions(
        data,
        best_source,
        safety_check,
        egfr
    )

    prompt = build_reconciliation_prompt(
        data=data,
        best_source=best_source,
        safety_check=safety_check,
        actions=recommended_actions
    )

    try:
        ai_reasoning = get_ai_response(prompt)
    except Exception:
        ai_reasoning = (
            f"- Selected {best_source.medication} based on source reliability and recency.\n"
            f"- Safety check status: {safety_check}.\n"
            f"- Follow-up: review conflicting records and verify with the care team if needed."
        )

    return {
        "reconciled_medication": best_source.medication,
        "confidence_score": confidence,
        "reasoning": ai_reasoning,
        "recommended_actions": recommended_actions,
        "clinical_safety_check": safety_check
    }