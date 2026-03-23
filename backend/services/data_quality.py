#logic for scoring records quality and completeness, and flagging potential issues for review.
from datetime import datetime


def validate_data_quality(data):
    issues = []

    completeness = 100
    accuracy = 100
    timeliness = 100
    clinical_plausibility = 100

    # completeness check
    if not data.allergies:
        completeness -= 40
        issues.append({
            "field": "allergies",
            "issue": "No allergies documented - likely incomplete",
            "severity": "medium"
        })

    # blood pressure plausibility
    bp = data.vital_signs.get("blood_pressure", "")
    if "/" in bp:
        try:
            systolic, diastolic = bp.split("/")
            systolic = int(systolic)
            diastolic = int(diastolic)

            if systolic > 300 or diastolic > 180:
                accuracy -= 50
                clinical_plausibility -= 60
                issues.append({
                    "field": "vital_signs.blood_pressure",
                    "issue": f"Blood pressure {bp} is physiologically implausible",
                    "severity": "high"
                })
        except Exception:
            accuracy -= 20
            issues.append({
                "field": "vital_signs.blood_pressure",
                "issue": "Blood pressure format is invalid",
                "severity": "medium"
            })

    # timeliness
    try:
        last_updated = datetime.strptime(data.last_updated, "%Y-%m-%d")
        months_old = (datetime.now() - last_updated).days / 30

        if months_old > 6:
            timeliness -= 30
            issues.append({
                "field": "last_updated",
                "issue": "Data is half year old",
                "severity": "medium"
            })
    except Exception:
        timeliness -= 20
        issues.append({
            "field": "last_updated",
            "issue": "Invalid date format",
            "severity": "medium"
        })

    overall_score = int((completeness + accuracy + timeliness + clinical_plausibility) / 4)

    return {
        "overall_score": max(0, overall_score),
        "breakdown": {
            "completeness": max(0, completeness),
            "accuracy": max(0, accuracy),
            "timeliness": max(0, timeliness),
            "clinical_plausibility": max(0, clinical_plausibility)
        },
        "issues_detected": issues
    }