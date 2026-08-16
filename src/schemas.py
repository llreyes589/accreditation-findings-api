from datetime import datetime

from pydantic import BaseModel

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

