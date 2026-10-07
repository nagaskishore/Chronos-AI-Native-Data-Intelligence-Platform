# Chronos Data Quality Rules

## Purpose

Chronos applies deterministic data quality checks before observations are allowed into the trusted Gold reconciliation process.

AI agents do not replace these deterministic checks.

## Required Fields

Required fields:

- `record_id`
- `vendor`
- `ticker`
- `event_time`
- `revenue`
- `currency`

Records missing required fields are invalid.

## Revenue Validation

Revenue values must not be negative.

A negative revenue value fails the current Chronos data quality rule.

## Currency Validation

The current Chronos financial event pipeline expects:

`USD`

Observations using unsupported currencies fail the current validation rule unless currency handling is explicitly extended.

## Source Duplicate Detection

Source duplicates are detected using:

`vendor + record_id`

Example:

`Vendor B + B-2004`

appearing more than once indicates a source duplicate.

Source duplicates are rejected and moved to quarantine.

## Business Event Conflicts

Business event conflicts are identified using:

`ticker + event_time`

A conflict between vendors does not automatically mean the records are invalid.

For example:

```text
Vendor A | AAPL | 2026-01-05 | 125000
Vendor B | AAPL | 2026-01-05 | 130000
```

is a reconciliation problem rather than necessarily a data-quality rejection.

## Quarantine

Records that fail deterministic quality rules are placed into a quarantine area.

Quarantine allows invalid records to be investigated without contaminating trusted downstream data.

## Quality vs Reconciliation

Chronos separates:

### Data Quality

"Is this observation structurally and technically acceptable?"

from:

### Reconciliation

"Which valid observation should represent this business event?"

A record can be valid but still lose a reconciliation conflict.

## AI Safety Principle

The AI layer must not bypass deterministic data quality rules.

AI-generated SQL can analyze trusted data, but it must not redefine the underlying data-quality policy.

## Example

Suppose Vendor B sends:

```text
record_id = B-2004
revenue = 50000
```

twice.

The record may contain valid fields and a valid revenue value.

However, because the same vendor and record identifier appear multiple times, it is classified as a source duplicate and rejected.

## Quality Gate

Chronos uses a quality gate after specialist-agent execution.

For SQL:

- SQL must pass validation.
- Query execution must succeed.
- Results must be available.

For RAG:

- Supporting documents must be retrieved.
- Retrieval context must not be empty.

The final answer generator should only operate after the appropriate quality checks succeed.
