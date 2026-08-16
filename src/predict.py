from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "risk_level_model.joblib"

def load_model():
    """Load the trained risk-level model from disk."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file was not found: {MODEL_PATH}. "
            "Run 'python -m src.train_model' first."
        )    

    return joblib.load(MODEL_PATH)

def predict_risk_level(
    category: str,
    corrective_action_days: float
) -> dict:
    """Predict risk level and class probabilities for one finding."""
    model = load_model()

    input_df = pd.DataFrame(
        [
            {
                "category": category.strip().title(),
                "corrective_action_days": corrective_action_days
            }
        ]
    )

    predicted_risk_level = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    probability_by_class = {
        risk_level: round(float(probability), 4)
        for risk_level, probability in zip(model.classes_, probabilities)
    }

    return {
        "category": input_df.iloc[0]["category"],
        "corrective_action_days": corrective_action_days,
        "predicted_risk_level": predicted_risk_level,
        "probabilities": probability_by_class
    }

if __name__ == "__main__":
    result = predict_risk_level(
        category="Documentation",
        corrective_action_days=35
    )

    print(result)