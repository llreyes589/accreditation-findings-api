from pathlib import Path

from src.data_pipeline import (
    clean_findings,
    get_valid_findings,
    load_and_validate_csv
)
from src.train_model import TARGET_COLUMN

class InsufficientDataError(ValueError):
    """Raised when there is not enough labeled data for reliable evaluation."""
    

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




def validate_evaluation_data(
    y,
    minimum_total_records: int = 30,
    minimum_records_per_class: int = 10
) -> None:
    """Ensure labels meet minimum volume requirements for evaluation."""
    total_records = len(y)
    class_counts = y.value_counts()

    errors = []

    if total_records < minimum_records_per_class:
        errors.append(
            f"Total records: {total_records} "
            f"(minimum required: {minimum_total_records})"            
        )

    underrepresented_classes = class_counts[
        class_counts < minimum_records_per_class
    ]

    if not underrepresented_classes.empty:
        classes = ", ".join(
            f"{risk_level}: {count}"
            for risk_level, count in underrepresented_classes.sort_index().items()
        )

        errors.append(
            f"Classes below minimum count "
            f"({minimum_records_per_class}): {classes}"            
        )


    if errors:
        raise InsufficientDataError("; ".join(errors))        

if __name__ == "__main__":
    _, y = load_training_data()
    print_class_distribution(y)

    try:
        validate_evaluation_data(y)
        print("Dataset meets the minimum evaluation requirements.")
    except InsufficientDataError as error:
        print(f"Evaluation blocked: {error}")
