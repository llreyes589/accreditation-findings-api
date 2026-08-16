def assess_finding(severity: str, status: str) -> str:
    severity = severity.strip().title()
    status = status.strip().title()

    if severity == "High" and status != "Closed":
        return "Urgent: needs immediate review"

    if status == "Closed":
        return "No active action required"

    return "Monitor and follow up"


if __name__ == "__main__":
    # Add five calls to assess_finding() using different severity/status combinations.
    # Store each result in a variable or print it directly.
    findings = [
        ("High", "Open"),
        ("High", "Closed"),
        ("Medium", "Open"),
        ("Low", "In Progress"),
        ("Low", "Closed"),
        # added findings
        (" high ", " open "),
        ("LOW", "closed"),
        ("medium", "IN PROGRESS"),    
    ]

    for severity, status in findings:
        assessment = assess_finding(severity, status)

    # Print the input and result in a readable format.
    # High / Open
        print(f"Severity: {severity} | Status: {status}")
        print(f"Assessment: {assessment}")



