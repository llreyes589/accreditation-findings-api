import sys
from pathlib import Path

import pandas as pd

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from data_pipeline import(
    DataQualityError,
    clean_findings,
    get_data_quality_report,
    get_open_high_findings,
    get_valid_findings,
    validate_data_quality,
)

def create_sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "finding_id": ["F-001", "F-002", "F-001", "F-003"],
            "institution": ["Hospital Alpha", "Clinic Bravo", "Hospital Alpha", None],
            "inspection_date": [
                "2026-01-15",
                "invalid-date",
                "2026-01-15",
                "2026-02-01",
            ],
            "category": ["Documentation", "Facilities", "Documentation", "Equipment"],
            "severity": [" high ", "LOW", "High", "Medium"],
            "status": [" open ", "Closed", "Open", "In Progress"],
            "corrective_action_days": [30, 14, 30, None],
        }
    )

def test_clean_findings_normalizes_text_and_converts_types():
    raw_df = create_sample_dataframe()

    cleaned_df = clean_findings(raw_df)

    assert cleaned_df.loc[0, "severity"] == "High"
    assert cleaned_df.loc[0, "status"] == "Open"
    assert pd.isna(cleaned_df.loc[1, "inspection_date"])
    assert pd.isna(cleaned_df.loc[3, "corrective_action_days"])

def test_get_valid_findings_removes_invalid_and_duplicate_rows():
    cleaned_df = clean_findings(create_sample_dataframe())

    valid_df = get_valid_findings(cleaned_df)

    assert len(valid_df) == 1
    assert valid_df.iloc[0]["finding_id"] == "F-001"    

def test_get_open_high_findings_filters_correctly():
    cleaned_df = clean_findings(create_sample_dataframe())
    valid_df = get_valid_findings(cleaned_df)

    result_df = get_open_high_findings(valid_df)

    assert len(result_df) == 1
    assert result_df.iloc[0]["finding_id"] == "F-001"    

def test_get_data_quality_report_returns_expected_counts():
    cleaned_df = clean_findings(create_sample_dataframe())

    report = get_data_quality_report(cleaned_df)

    assert report["total_rows"] == 4
    assert report["duplicate_finding_id_count"] == 1
    assert report["invalid_inspection_date_count"] == 1
    assert report["missing_institution_count"] == 1
    assert report["missing_corrective_action_days_count"] == 1
    assert report["missing_values"] == {
        "institution": 1,
        "inspection_date": 1,
        "corrective_action_days": 1
    }

def test_validate_data_quality_raises_for_bad_data():
    cleaned_df = clean_findings(create_sample_dataframe())
    report = get_data_quality_report(cleaned_df)

    with pytest.raises(DataQualityError) as error:
        validate_data_quality(report)

    assert "Missing values: 3" in str(error.value)
    assert "Duplicate finding IDs: 1" in str(error.value)
    assert "Invalid inspection dates: 1" in str(error.value)


def test_validate_data_quality_accepts_clean_data():
    cleaned_df = clean_findings(create_sample_dataframe())
    valid_df = get_valid_findings(cleaned_df)
    report = get_data_quality_report(valid_df)

    validate_data_quality(report)