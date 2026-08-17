from src.evaluate_model import load_training_data

def test_load_training_data_returns_expected_labels():
    _, y = load_training_data()

    assert len(y) == 8
    assert y.value_counts().to_dict() == {
        "High": 3,
        "Medium": 3,
        "Low": 2
    }