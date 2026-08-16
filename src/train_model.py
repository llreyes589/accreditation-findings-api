from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.data_pipeline import (
    clean_findings,
    get_valid_findings,
    load_and_validate_csv
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "inspection_findings.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "risk_level_model.joblib"

FEATURE_COLUMNS = [
    "category",
    "corrective_action_days",
]
TARGET_COLUMN = "risk_level"

def train_and_save_model() -> Pipeline:
    """Train a risk-level classifier using validated inspection findings."""
    raw_df = load_and_validate_csv(CSV_PATH)
    cleaned_df = clean_findings(raw_df)
    valid_df = get_valid_findings(cleaned_df)

    x = valid_df[FEATURE_COLUMNS]
    y = valid_df[TARGET_COLUMN]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "category",
                OneHotEncoder(handle_unknown="ignore"),
                ["category"]
            ),
            (
                "numeric",
                "passthrough",
                ["corrective_action_days"]
            )
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1_000,
                    random_state=42
                )
            )
        ]
    )

    model.fit(x, y)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)


    print(f"Training records: {len(valid_df)}")
    print(f"Features: {', '.join(FEATURE_COLUMNS)}")
    print(f"Target: {TARGET_COLUMN}")
    print(f"Classes: {', '.join(model.classes_)}")
    print(f"Saved model to: {MODEL_PATH}")

    return model

if __name__ == "__main__":
    train_and_save_model()    