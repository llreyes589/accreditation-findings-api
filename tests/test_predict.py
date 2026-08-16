import pytest

from src.predict import predict_risk_level


def test_predict_risk_level_returns_expected_structure():
    result = predict_risk_level(
        category="Documentation",
        corrective_action_days=35,
    )

    assert result["category"] == "Documentation"
    assert result["corrective_action_days"] == 35
    assert result["predicted_risk_level"] in {"High", "Low", "Medium"}
    assert set(result["probabilities"]) == {"High", "Low", "Medium"}

    total_probability = sum(result["probabilities"].values())
    assert total_probability == pytest.approx(1.0, abs=0.001)


def test_predict_risk_level_normalizes_category():
    result = predict_risk_level(
        category=" documentation ",
        corrective_action_days=35,
    )

    assert result["category"] == "Documentation"