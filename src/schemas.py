from datetime import datetime

from pydantic import BaseModel, Field

class RiskPredictionRequest(BaseModel):
    category: str = Field(
        min_length=2,
        max_length=100,
        description="Finding category, such as Documentation"
    )
    corrective_action_days: float = Field(
        gt=0,
        le=365,
        description="Number of days assigned for corrective action."
    )

class RiskPredictionResponse(BaseModel):
    category: str
    corrective_action_days: float
    predicted_risk_level: str
    probabilities: dict[str, float]

class HealthResponse(BaseModel):
    status: str

class FindingsSummaryResponse(BaseModel):
    raw_records: int
    valid_records: int

class FindingResponse(BaseModel):
    finding_id: str
    institution: str
    inspection_date: datetime
    category: str
    severity: str
    status: str
    corrective_action_days: float

class DataQualityReportResponse(BaseModel):
    total_rows: int
    missing_values: dict[str, int]
    duplicate_finding_id_count: int
    invalid_inspection_date_count: int
    missing_institution_count: int
    missing_corrective_action_days_count: int

