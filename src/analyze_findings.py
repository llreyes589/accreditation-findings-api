from pathlib import Path

from data_pipeline import (
    DataQualityError,
    clean_findings,
    get_data_quality_report,
    get_open_high_findings,
    get_valid_findings,
    load_and_validate_csv,
    validate_data_quality
)


project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "data" / "inspection_findings.csv"

try:
    raw_df = load_and_validate_csv(csv_path)
    cleaned_df = clean_findings(raw_df)

    quality_report = get_data_quality_report(cleaned_df)

    print("\nData quality report")
    for key, value in quality_report.items():
        print(f"{key}: {value}")

    try:
        validate_data_quality(quality_report)
        print("Raw dataset passed the quality gate.")
    except DataQualityError as error:
        print(f"Raw dataset failed the quality gate: {error}")
      

    valid_df = get_valid_findings(cleaned_df)

    valid_report = get_data_quality_report(valid_df)
    validate_data_quality(valid_report)

    print("Validated dataset passed the quality gate.")    

    print(f"Raw records loaded: {len(raw_df)}")
    print(f"Valid records: {len(valid_df)}")

    open_high_findings = get_open_high_findings(valid_df)
    print(open_high_findings[["finding_id", "institution"]].to_string(index=False))


except FileNotFoundError:
    print(f"Inspection CSV was not found: {csv_path}")

except ValueError as error:
    print(error)