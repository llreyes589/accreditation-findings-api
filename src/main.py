from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from src.data_pipeline import (
    clean_findings,
    get_data_quality_report,
    get_open_high_findings,
    get_valid_findings,
    load_and_validate_csv
)

from src.schemas import (
    DataQualityReportResponse,
    FindingResponse,
    FindingsSummaryResponse,
    HealthResponse
)

app = FastAPI(
    title="Accreditation Findings API",
    description="A starter API for validated accreditation inspection findings.",
    version="0.1.0",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "inspection_findings.csv"

def get_processed_data():
    """Load, clean, and filter the inspection findings dataset."""
    try:
        raw_df = load_and_validate_csv(CSV_PATH)
        cleaned_df = clean_findings(raw_df)
        valid_df = get_valid_findings(cleaned_df)

        return raw_df, cleaned_df, valid_df

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Inspection CSV was not found: {CSV_PATH}"
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return a simple service health response."""
    return {"status": "ok"}

@app.get("/findings/summary", response_model=FindingsSummaryResponse)
def get_findings_summary():
    """Return record counts before and after validation."""
    raw_df, _, valid_df = get_processed_data()    

    return {
        "raw_records": len(raw_df),
        "valid_records": len(valid_df)
    }

@app.get("/findings/open-high", response_model=list[FindingResponse])
def get_open_high_findings_endpoint(institution: str | None = Query(
    default=None,
    min_length=2,
    description="Optional institution name filter."
)):
    """Return valid findings that are both high severity and open."""
    _, _, valid_df = get_processed_data()
    open_high_df = get_open_high_findings(valid_df)

    if institution:
        normalized_institution = institution.strip().casefold()

        open_high_df = open_high_df[
            open_high_df["institution"]
            .str.casefold()
            .str.contains(normalized_institution, na=False)
        ]

    return open_high_df.to_dict(orient="records")

@app.get("/findings/quality-report", response_model=DataQualityReportResponse)
def get_quality_report():
    """Return data-quality metrics for the cleaned raw dataset."""
    _, cleaned_df, _ = get_processed_data()

    return get_data_quality_report(cleaned_df)