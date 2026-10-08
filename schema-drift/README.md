# Fraoula Schema Drift Guard

Detect breaking schema changes before bad data reaches production.

Schema Drift Guard compares an incoming JSON schema against an approved baseline and identifies potentially breaking changes.

Built by [Fraoula](https://www.fraoula.co) — data trust software for regulated enterprises.

## What it detects

- Required fields removed
- Field type changes
- Unexpected new fields
- Newly introduced sensitive fields
- Safe additive fields

## Run locally

```bash
python drift_guard.py examples/baseline.json examples/incoming.json
```

## Input format

```json
{
  "customer_id": "integer",
  "name": "string",
  "email": "string"
}
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

## Exit codes

- `0` — PASS or WARN
- `1` — FAIL because a breaking change was detected
- `2` — invalid input / execution error

## Security

This tool reads local schema files only. It does not transmit schema contents to Fraoula or any external service.
