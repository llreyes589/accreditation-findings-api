from assessment import assess_finding


def test_high_open_is_urgent():
    result = assess_finding("High", "Open")

    assert result == "Urgent: needs immediate review"


def test_closed_finding_needs_no_action():
    result = assess_finding("Low", "Closed")

    assert result == "No active action required"


def test_input_is_normalized():
    result = assess_finding(" high ", " open ")

    assert result == "Urgent: needs immediate review"