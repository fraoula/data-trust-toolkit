import json
import sys

# Ensure UTF-8 output encoding across all terminals and platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SENSITIVE_FIELDS = {
    "ssn",
    "email",
    "phone",
    "dob",
    "date_of_birth",
    "passport",
    "credit_card",
    "card_number",
}


def load_schema(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def compare_schemas(baseline, incoming):
    breaking = []
    warnings = []
    safe = []

    # Removed fields
    for field in baseline:
        if field not in incoming:
            breaking.append(
                f"Required field removed: {field}"
            )

    # Type changes
    for field in baseline:
        if field in incoming:
            if baseline[field] != incoming[field]:
                breaking.append(
                    f"{field}: {baseline[field]} → {incoming[field]}"
                )

    # New fields
    for field in incoming:
        if field not in baseline:
            if field.lower() in SENSITIVE_FIELDS:
                warnings.append(
                    f"New sensitive field detected: {field}"
                )
            else:
                safe.append(
                    f"Optional field added: {field}"
                )

    return breaking, warnings, safe


def calculate_risk(breaking, warnings):
    score = len(breaking) * 30 + len(warnings) * 10
    return min(score, 100)


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python drift_guard.py "
            "baseline.json incoming.json"
        )
        sys.exit(1)

    baseline = load_schema(sys.argv[1])
    incoming = load_schema(sys.argv[2])

    breaking, warnings, safe = compare_schemas(
        baseline,
        incoming
    )

    risk_score = calculate_risk(
        breaking,
        warnings
    )

    status = "PASS"

    if breaking:
        status = "FAIL"
    elif warnings:
        status = "WARN"

    print("\nFraoula Schema Drift Report")
    print("=" * 30)

    print(f"\nStatus: {status}")
    print(f"Risk Score: {risk_score}/100")

    if breaking:
        print("\nBREAKING")
        for issue in breaking:
            print(f"✗ {issue}")

    if warnings:
        print("\nWARNING")
        for issue in warnings:
            print(f"⚠ {issue}")

    if safe:
        print("\nSAFE")
        for issue in safe:
            print(f"✓ {issue}")

    print("\nPowered by Fraoula")
    print("https://www.fraoula.co")

    if breaking:
        sys.exit(1)


if __name__ == "__main__":
    main()
