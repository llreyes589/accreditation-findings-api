from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "finding_id",
    "institution",
    "inspection_date",
    "category",
    "severity",
    "status",
    "corrective_action_days",
]

class DataQualityError(ValueError):
    """Raised when a dataset does not meet the required quality threshold."""

def load_and_validate_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    return df

def clean_findings(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize text fields and safely convert date and numeric columns."""
    cleaned_df = df.copy()

    cleaned_df["severity"] = cleaned_df["severity"].str.strip().str.title()
    cleaned_df["status"] = cleaned_df["status"].str.strip().str.title()

    cleaned_df['inspection_date'] = pd.to_datetime(
        cleaned_df["inspection_date"],
        errors="coerce"
    )

    cleaned_df["corrective_action_days"] = pd.to_numeric(cleaned_df["corrective_action_days"], errors="coerce")

    return cleaned_df

def get_valid_findings(df: pd.DataFrame) -> pd.DataFrame:
    valid_df = df.dropna(subset=REQUIRED_COLUMNS).drop_duplicates(subset="finding_id", keep="first")

    return valid_df

def get_open_high_findings(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        (df["severity"] == "High") & (df["status"] == "Open")
    ]

def get_data_quality_report(df: pd.DataFrame) -> dict:
    """Return data-quality metrics for a cleaned findings DataFrame"""
    missing_values = df[REQUIRED_COLUMNS].isna().sum()

    duplicate_id_count = int(df["finding_id"].duplicated().sum())
    invalid_date_count = int(df["inspection_date"].isna().sum())
    missing_institution_count = int(df["institution"].isna().sum())
    missing_action_days_count = int(df["corrective_action_days"].isna().sum())

    return {
        "total_rows": len(df),
        "missing_values": missing_values[missing_values > 0].to_dict(),
        "duplicate_finding_id_count": duplicate_id_count,
        "invalid_inspection_date_count": invalid_date_count,
        "missing_institution_count": missing_institution_count,
        "missing_corrective_action_days_count": missing_action_days_count
    }

def validate_data_quality(
    report: dict,
    max_missing_values: int = 0,
    max_duplicate_ids: int = 0,
    max_invalid_dates: int = 0,
) -> None:
    """Raise DataQualityError when the report exceeds permitted thresholds."""
    total_missing_values = sum(report["missing_values"].values())

    errors = []

    if total_missing_values > max_missing_values:
        errors.append(
            f"Missing values: {total_missing_values} "
            f"(maximum allowed: {max_missing_values})"
        )

    if report["duplicate_finding_id_count"] > max_duplicate_ids:
        errors.append(
            f"Duplicate finding IDs: "
            f"{report['duplicate_finding_id_count']} "
            f"(maximum allowed: {max_duplicate_ids})"
        )

    if report["invalid_inspection_date_count"] > max_invalid_dates:
        errors.append(
            f"Invalid inspection dates: "
            f"{report['invalid_inspection_date_count']} "
            f"(maximum allowed: {max_invalid_dates})"
        )

    if errors:
        raise DataQualityError("; ".join(errors))