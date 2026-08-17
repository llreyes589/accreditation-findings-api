from pathlib import Path

from src.data_pipeline import (
    clean_findings,
    get_valid_findings,
    load_and_validate_csv
)
from src.train_model import TARGET_COLUMN

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "inspection_findings.csv"

def load_training_data():
    """Load valid findings and split them into features and target labels."""
    raw_df = load_and_validate_csv(CSV_PATH)
    cleaned_df = clean_findings(raw_df)
    valid_df = get_valid_findings(cleaned_df)

    x = valid_df.drop(columns=[TARGET_COLUMN])
    y = valid_df[TARGET_COLUMN]

    return x, y

def print_class_distribution(y) -> None:
    """Print the number of training records for each risk-level class."""
    class_counts = y.value_counts().sort_index()

    print("Risk-level class distribution:")
    for risk_level, count in class_counts.items():
        print(f"- {risk_level}: {count}")

if __name__ == "__main__":
    _, y = load_training_data()
    print_class_distribution(y)