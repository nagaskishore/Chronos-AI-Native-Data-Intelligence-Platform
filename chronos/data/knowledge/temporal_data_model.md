# Chronos Temporal Data Model

## Purpose

Financial information can change after it is initially reported. Chronos therefore separates the time when an event occurred from the time when Chronos learned about the event.

This enables historical reconstruction and auditability.

## Event Time

`event_time` represents when the business event occurred.

Example:

`2026-01-05`

## Knowledge Time

`knowledge_time` represents when Chronos became aware of the observation or revision.

Example:

```text
Event time: 2026-01-05
Knowledge time: 2026-01-10
```

The event occurred on January 5, but Chronos did not receive or learn the relevant information until January 10.

## Ingestion Time

`ingestion_timestamp` represents when the Chronos ingestion process received the record.

Knowledge time and ingestion time may be close but represent different concepts.

## Revisions

A vendor may initially report:

```text
AAPL
2026-01-05
Revenue = 125000
```

Later, the vendor may issue:

```text
AAPL
2026-01-05
Revenue = 130000
```

The original observation should not simply be overwritten.

Chronos models the revised observation as a new version.

## Versioning

Temporal history includes concepts such as:

- `valid_from`
- `valid_to`
- `record_version`
- `is_current`

These fields allow Chronos to determine which version was valid at a particular point in time.

## Current State

The current Gold state represents the latest trusted canonical observation.

## Historical State

Temporal history can answer:

"What did Chronos know on January 7?"

This should reflect information available by January 7 rather than a later revision.

## Late Arriving Data

An observation may arrive after the event occurred.

Example:

```text
event_time = January 5
ingestion_time = January 12
```

This is late-arriving data.

Late arrival does not automatically make an observation invalid.

## Temporal Principle

Chronos follows this principle:

> Event time describes the business world. Knowledge time describes what Chronos knew. Ingestion time describes when the platform processed the data.

These concepts should not be treated as interchangeable.
