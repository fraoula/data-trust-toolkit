# Fraoula Data Trust Toolkit

**Open-source tools for data quality, schema validation, and data contract enforcement.**

Built by [Fraoula](https://www.fraoula.co), a data trust software company for regulated enterprises.

---

## What it checks

- **Schema violations** — Field presence, unexpected columns, and data type alignment.
- **Missing required fields** — Enforce non-nullable constraints per contract.
- **Type mismatches** — Detect string, integer, float, boolean, and datetime mismatches.
- **Unexpected columns** — Flag unannounced upstream schema drift.
- **Duplicate records** — Key-based and full-row duplicate detection.
- **Null-value thresholds** — Configurable null-tolerance percentages per column.
- **Basic data-contract compliance** — Validate JSON or CSV datasets against declarative schema contracts.

## Why this exists

Bad data should be detected before it propagates into analytics, AI systems, financial workflows, or other mission-critical applications. In modern data stacks, silent schema drift and unvalidated pipeline ingestion degrade downstream machine learning models and create costly compliance violations.

The **Fraoula Data Trust Toolkit** provides a lightweight, zero-dependency Python utility for data teams to validate datasets locally, in CI/CD pipelines, or before loading into production lakehouses and warehouses.

## Installation

```bash
pip install .
```

Or install in development mode:

```bash
git clone https://github.com/fraoula/data-trust-toolkit.git
cd data-trust-toolkit
pip install -e .
```

## Quick Start

### 1. Python API

```python
from fraoula_data_trust import validate_dataset

# Validate CSV against expected schema contract
report = validate_dataset(
    data_path="examples/customers.csv",
    schema_path="examples/expected_schema.json"
)

# Print clean terminal summary
report.print_summary()

# Export machine-readable JSON
report.to_json("output_report.json")
```

### 2. CLI Usage

```bash
python -m fraoula_data_trust.validator --data examples/customers.csv --schema examples/expected_schema.json
```

## Data Contract Format

Declarative schema contracts are defined in standard JSON:

```json
{
  "name": "customer_ingestion_contract",
  "version": "1.0.0",
  "allow_unexpected_columns": false,
  "columns": {
    "customer_id": {
      "type": "string",
      "required": true,
      "unique": true
    },
    "email": {
      "type": "string",
      "required": true,
      "null_threshold_pct": 0.0
    },
    "account_balance": {
      "type": "float",
      "required": false
    },
    "is_active": {
      "type": "boolean",
      "required": true
    }
  }
}
```

## Project Structure

```
data-trust-toolkit/
├── fraoula_data_trust/
│   ├── __init__.py         # Package entry point
│   ├── validator.py        # Core DatasetValidator engine & CLI
│   ├── schema.py           # Schema inference & contract evaluation
│   ├── duplicates.py       # Duplicate detection logic
│   └── report.py           # Terminal formatting & JSON reporting
├── examples/               # Synthetic datasets and contracts
├── tests/                  # Unit tests for validation rules
└── docs/                   # Data contract guides
```

## Running Tests

```bash
python -m unittest discover tests
```

---

## Fraoula Data Auditor

For enterprise-scale, real-time data validation, observability, compliance controls, and managed deployments, see [Fraoula Data Auditor](https://www.fraoula.co/).

Website: [https://www.fraoula.co](https://www.fraoula.co)

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.
