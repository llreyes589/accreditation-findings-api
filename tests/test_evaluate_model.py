from src.evaluate_model import load_training_data

import pandas as pd
import pytest

from src.evaluate_model import (
    InsufficientDataError,
    load_training_data,
    validate_evaluation_data
)

def test_load_training_data_returns_expected_labels():
    _, y = load_training_data()

    assert len(y) == 8
    assert y.value_counts().to_dict() == {
        "High": 3,
        "Medium": 3,
        "Low": 2
    }

def test_validate_evaluation_data_blocks_small_dataset():
    _, y = load_training_data()

    with pytest.raises(InsufficientDataError) as error:
        validate_evaluation_data(y)

    message = str(error.value)

    assert "Total records: 8" in message
    assert "High: 3" in message
    assert "Low: 2" in message
    assert "Medium: 3" in message


def test_validate_evaluation_data_accepts_sufficient_data():
    y = pd.Series(
        ["High"] * 10
        + ["Low"] * 10
        + ["Medium"] * 10
    )

    validate_evaluation_data(y)    