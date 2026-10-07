# Chronos Vendor Source Rules

## Purpose

Chronos receives financial event data from multiple vendors with different schemas and source conventions.

The ingestion and normalization layers convert these heterogeneous representations into a common canonical model.

## Vendor A

Vendor A provides:

```text
vendor_record_id
ticker
event_date
revenue
currency
status
```

Vendor A has the highest configured source priority.

Priority: `1`

## Vendor A Schema Evolution

Vendor A may change field names between source versions.

Version 1:

```text
event_date
revenue
```

Version 2:

```text
eventDate
revenue_amount
```

Chronos handles these changes during normalization.

## Vendor B

Vendor B provides:

```text
record_id
security
trade_date
amount
ccy
```

Example mapping:

```text
record_id  -> record_id
security   -> ticker
trade_date -> event_time
amount     -> revenue
ccy        -> currency
```

Vendor B has source priority: `2`

## Vendor C

Vendor C provides:

```text
id
symbol
business_date
value
currency_code
```

Example mapping:

```text
id             -> record_id
symbol         -> ticker
business_date  -> event_time
value          -> revenue
currency_code  -> currency
```

Vendor C has source priority: `3`

## Source Priority

Current source authority:

```text
1. Vendor A
2. Vendor B
3. Vendor C
```

Source priority is used when valid observations conflict and reconciliation requires a deterministic winner.

## Schema Heterogeneity

Different vendors may use different:

- Field names
- Date formats
- Numeric field names
- Currency field names
- Record identifiers

The Silver normalization layer maps these source-specific fields into the Chronos canonical schema.

## Raw Data Preservation

Bronze ingestion preserves source data in its original representation.

Normalization happens downstream.

This provides:

- Auditability
- Reprocessing capability
- Schema evolution analysis
- Source-level debugging

## Canonical Model

After normalization:

```text
record_id
vendor
ticker
event_time
revenue
currency
status
source_file
batch_id
ingestion_timestamp
```

## Important Principle

Vendor-specific schemas belong at the ingestion and normalization boundary.

Business and AI consumers should interact with the canonical representation rather than vendor-specific schemas.
