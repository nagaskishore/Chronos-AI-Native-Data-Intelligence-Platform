# Chronos Data Dictionary

## Purpose

Chronos is an AI-native data intelligence platform that ingests financial event data from multiple vendor sources, normalizes heterogeneous schemas, applies data quality rules, models historical revisions, reconciles conflicting observations, and exposes trusted information to AI agents.

The primary business entity in Chronos is a financial event associated with a security ticker and an event timestamp.

## Canonical Financial Event

Chronos represents financial observations using:

| Field | Meaning |
|---|---|
| `record_id` | Unique identifier assigned by the source vendor |
| `vendor` | Source system or vendor that supplied the observation |
| `ticker` | Security or financial instrument symbol |
| `event_time` | Date/time when the business event occurred |
| `revenue` | Revenue value reported for the event |
| `currency` | Currency associated with the revenue value |
| `status` | Business status of the observation |
| `source_file` | File from which the observation originated |
| `batch_id` | Ingestion batch identifier |
| `ingestion_timestamp` | Time Chronos ingested the observation |

## Business Event Key

A business event is identified using:

`ticker + event_time`

Different vendors may therefore provide observations for the same business event.

## Source Key

A source-level record is identified using:

`vendor + record_id`

This identifies an individual observation supplied by a vendor.

## Gold Financial Event

The Chronos Gold layer contains the reconciled representation of current financial events.

The primary AI-facing semantic view is:

`CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS`

The view exposes:

- `TICKER`
- `EVENT_TIME`
- `REVENUE`
- `CURRENCY`
- `STATUS`
- `SOURCE`
- `RECONCILIATION_STATUS`
- `CONFIDENCE`
- `VENDOR_COUNT`
- `HAS_CONFLICT`
- `KNOWLEDGE_TIME`

## Reconciliation Status

`RECONCILIATION_STATUS` describes how Chronos resolved observations for a business event.

Possible values include:

### SINGLE_SOURCE

Only one valid source observation was available.

### MULTI_SOURCE_AGREEMENT

Multiple vendors supplied observations and their relevant values agreed.

### CONFLICT_RESOLVED

Multiple vendors supplied different values and Chronos selected a canonical value using source priority.

## Confidence

`CONFIDENCE` represents Chronos's confidence in the reconciled observation.

It should not be interpreted as a statistical probability.

## Vendor Count

`VENDOR_COUNT` indicates how many vendors contributed observations for the business event.

## Has Conflict

`HAS_CONFLICT` indicates whether multiple source observations disagreed for the same business event.

A conflict does not necessarily mean that the Gold record is invalid.

## Knowledge Time

`KNOWLEDGE_TIME` represents when Chronos became aware of the observation.

This is different from `EVENT_TIME`.

`EVENT_TIME` answers: "When did the business event happen?"

`KNOWLEDGE_TIME` answers: "When did Chronos know about this information?"

## AI Semantic View

AI agents should query:

`CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS`

rather than directly querying raw Bronze or Silver data.

The semantic view provides a controlled interface between the AI layer and the underlying data platform.

## Evidence Table

Detailed reconciliation evidence is stored separately from the Gold result.

The evidence layer preserves supporting and losing observations so that the canonical result can be explained and audited.

## AI Query Log

AI-generated analytical queries are recorded in:

`CHRONOS.AI.QUERY_LOG`

The query log records:

- Query identifier
- User question
- Generated SQL
- Validation status
- Validation reason
- Result row count
- Creation timestamp

This supports observability and auditability of AI-generated SQL.
