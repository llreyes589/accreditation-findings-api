from src.train_model import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    train_and_save_model
)

def test_train_and_save_model_creates_model_artifact(tmp_path, monkeypatch):
    model_path = tmp_path / "risk_level_model.joblib"

    monkeypatch.setattr("src.train_model.MODEL_DIR", tmp_path)
    monkeypatch.setattr("src.train_model.MODEL_PATH", model_path)

    model = train_and_save_model()

    assert model_path.exists()
    assert FEATURE_COLUMNS == [
        "category",
        "corrective_action_days"
    ]
    assert TARGET_COLUMN == "risk_level"
    assert set(model.classes_) == {"High", "Low", "Medium"}