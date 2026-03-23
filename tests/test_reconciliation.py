from backend.model.schemas import (
    PatientContext,
    SourceRecord,
    ReconcileMedicationRequest,
)
from backend.services.reconciliation import (
    reconcile_medications,
    reliability_score,
    recency_score,
    calculate_confidence,
    determine_safety_check,
)


def test_reliability_score_mapping():
    assert reliability_score("high") == 3
    assert reliability_score("medium") == 2
    assert reliability_score("low") == 1
    assert reliability_score("unknown") == 0


def test_recency_score_recent_date():
    # A modern recent year should return > 0 if parsed correctly.
    score = recency_score("2026-03-01")
    assert score in [1, 2, 3]


def test_reconciliation_selects_primary_care_lower_metformin_dose():
    data = ReconcileMedicationRequest(
        patient_context=PatientContext(
            age=67,
            conditions=["Type 2 Diabetes", "Hypertension"],
            recent_labs={"eGFR": 45},
        ),
        sources=[
            SourceRecord(
                system="Hospital EHR",
                medication="Metformin 1000mg twice daily",
                last_updated="2024-10-15",
                source_reliability="high",
            ),
            SourceRecord(
                system="Primary Care",
                medication="Metformin 500mg twice daily",
                last_updated="2025-01-20",
                source_reliability="high",
            ),
            SourceRecord(
                system="Pharmacy",
                medication="Metformin 1000mg daily",
                last_filled="2025-01-25",
                source_reliability="medium",
            ),
        ],
    )

    result = reconcile_medications(data)

    assert result["reconciled_medication"] == "Metformin 500mg twice daily"
    assert 0.5 <= result["confidence_score"] <= 0.99
    assert result["clinical_safety_check"] in ["PASSED", "CAUTION", "REVIEW"]


def test_determine_safety_check_returns_caution_for_metformin_with_egfr_45():
    patient_context = PatientContext(
        age=67,
        conditions=["Type 2 Diabetes"],
        recent_labs={"eGFR": 45},
    )
    best_source = SourceRecord(
        system="Primary Care",
        medication="Metformin 500mg twice daily",
        last_updated="2025-01-20",
        source_reliability="high",
    )

    safety, egfr = determine_safety_check(best_source, patient_context)

    assert safety == "CAUTION"
    assert egfr == 45


def test_determine_safety_check_returns_review_for_metformin_with_low_egfr():
    patient_context = PatientContext(
        age=67,
        conditions=["Type 2 Diabetes"],
        recent_labs={"eGFR": 30},
    )
    best_source = SourceRecord(
        system="Primary Care",
        medication="Metformin 500mg twice daily",
        last_updated="2025-01-20",
        source_reliability="high",
    )

    safety, egfr = determine_safety_check(best_source, patient_context)

    assert safety == "REVIEW"
    assert egfr == 30


def test_calculate_confidence_penalizes_disagreement():
    low_disagreement_sources = [
        (5, "a"),
        (5, "b"),
        (4, "c"),
    ]
    high_disagreement_sources = [
        (5, "a"),
        (1, "b"),
        (1, "c"),
    ]

    confidence_low_disagreement = calculate_confidence(low_disagreement_sources)
    confidence_high_disagreement = calculate_confidence(high_disagreement_sources)

    assert confidence_low_disagreement > confidence_high_disagreement
    assert 0.5 <= confidence_low_disagreement <= 0.99
    assert 0.5 <= confidence_high_disagreement <= 0.99