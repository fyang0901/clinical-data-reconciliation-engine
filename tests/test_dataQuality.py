from types import SimpleNamespace
from backend.services.data_quality import validate_data_quality


def build_quality_input(
    allergies=None,
    blood_pressure="120/80",
    last_updated="2025-01-01",
):
    if allergies is None:
        allergies = []

    return SimpleNamespace(
        demographics={"name": "John Doe", "dob": "1955-03-15", "gender": "M"},
        medications=["Metformin 500mg", "Lisinopril 10mg"],
        allergies=allergies,
        conditions=["Type 2 Diabetes"],
        vital_signs={"blood_pressure": blood_pressure, "heart_rate": 72},
        last_updated=last_updated,
    )


def test_data_quality_flags_missing_allergies():
    data = build_quality_input(allergies=[])

    result = validate_data_quality(data)

    assert any(issue["field"] == "allergies" for issue in result["issues_detected"])
    assert result["breakdown"]["completeness"] < 100


def test_data_quality_flags_implausible_blood_pressure():
    data = build_quality_input(blood_pressure="340/180", allergies=["Penicillin"])

    result = validate_data_quality(data)

    assert any(
        issue["field"] == "vital_signs.blood_pressure"
        for issue in result["issues_detected"]
    )
    assert result["breakdown"]["clinical_plausibility"] < 100
    assert result["breakdown"]["accuracy"] < 100


def test_data_quality_flags_stale_record():
    data = build_quality_input(
        allergies=["Penicillin"],
        blood_pressure="120/80",
        last_updated="2024-06-15",
    )

    result = validate_data_quality(data)

    assert any(issue["field"] == "last_updated" for issue in result["issues_detected"])
    assert result["breakdown"]["timeliness"] < 100


def test_data_quality_returns_expected_top_level_keys():
    data = build_quality_input(allergies=["Penicillin"])

    result = validate_data_quality(data)

    assert "overall_score" in result
    assert "breakdown" in result
    assert "issues_detected" in result


def test_data_quality_with_cleaner_input_has_higher_score():
    clean_data = build_quality_input(
        allergies=["Penicillin"],
        blood_pressure="120/80",
        last_updated="2026-02-15",
    )
    problematic_data = build_quality_input(
        allergies=[],
        blood_pressure="340/180",
        last_updated="2024-06-15",
    )

    clean_result = validate_data_quality(clean_data)
    problematic_result = validate_data_quality(problematic_data)

    assert clean_result["overall_score"] > problematic_result["overall_score"]