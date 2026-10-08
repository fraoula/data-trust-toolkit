# Fraoula Data Trust Toolkit

Open-source tools for **data quality, schema validation, and data contract enforcement**.

Built by [Fraoula](https://www.fraoula.co) — data trust software for regulated enterprises.

[![CI](https://github.com/fraoula/data-trust-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/fraoula/data-trust-toolkit/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

## Included Tool: Schema Drift Guard

**Fraoula Schema Drift Guard** detects breaking schema changes before bad data reaches production.

It compares an approved baseline schema with an incoming schema and classifies changes as:

- **BREAKING** — removed fields or incompatible type changes
- **WARNING** — newly introduced sensitive fields
- **SAFE** — non-sensitive additive fields

### Quick start

```bash
python schema-drift/drift_guard.py \
  schema-drift/examples/baseline.json \
  schema-drift/examples/incoming.json
```

## GitHub Action

```yaml
name: Schema Drift Check
on:
  pull_request:
jobs:
  schema-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check schema drift
        uses: fraoula/data-trust-toolkit/schema-drift@main
        with:
          baseline: schema/baseline.json
          incoming: schema/current.json
```

A breaking schema change exits with status code `1`, so the workflow fails and can block a pull request.

## Why this exists

Bad data should be detected **before** it propagates into analytics, AI systems, financial workflows, healthcare systems, or other mission-critical applications.

Fraoula created this toolkit as a small open-source contribution to the data engineering community.

## Repository structure

```text
data-trust-toolkit/
├── .github/
│   ├── workflows/test.yml
│   └── ISSUE_TEMPLATE/
├── schema-drift/
│   ├── action.yml
│   ├── drift_guard.py
│   ├── README.md
│   ├── examples/
│   └── tests/
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

## Roadmap

Possible future additions:

- JSON Schema support
- Configurable field criticality
- Configurable sensitive-field dictionaries
- JSON machine-readable reports
- Data contract validation
- Pull-request comments
- Schema version history

## Fraoula

Fraoula builds data trust software for regulated enterprises.

Website: https://www.fraoula.co

## License

Apache License 2.0.
