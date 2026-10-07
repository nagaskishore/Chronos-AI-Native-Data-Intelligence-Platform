# Chronos Reconciliation Rules

## Purpose

Chronos receives financial observations from multiple external vendors. Because different vendors may report the same business event, Chronos must determine which observation becomes the canonical Gold value.

The reconciliation process is deterministic and auditable.

## Business Event Identity

Chronos identifies a business event using:

`ticker + event_time`

## Source Record Identity

A source record is identified using:

`vendor + record_id`

## Source Duplicates

A source duplicate occurs when the same vendor provides the same source record more than once.

Example:

`Vendor B + B-2004`

appearing multiple times is a source duplicate.

Source duplicates are rejected during the data quality stage and quarantined rather than silently merged.

## Cross-Vendor Conflicts

A cross-vendor conflict occurs when multiple vendors provide different observations for the same business event.

Example:

```text
Vendor A | AAPL | 2026-01-05 | 125000
Vendor B | AAPL | 2026-01-05 | 130000
```

These observations refer to the same business event but contain different revenue values.

A cross-vendor conflict is not automatically treated as bad data.

## Source Priority

Chronos uses configured source priority when resolving eligible conflicts.

Current source priority:

```text
Vendor A = Priority 1
Vendor B = Priority 2
Vendor C = Priority 3
```

Lower priority numbers represent higher source authority.

Therefore:

`Vendor A > Vendor B > Vendor C`

when resolving conflicting observations.

## Conflict Resolution

When multiple valid vendors report different values:

1. Identify the business event using `ticker + event_time`.
2. Collect all valid observations.
3. Determine whether the observations agree.
4. If they disagree, compare configured source priorities.
5. Select the highest-priority valid observation as the canonical value.
6. Preserve supporting and losing observations in reconciliation evidence.
7. Mark the Gold result as `CONFLICT_RESOLVED`.
8. Record the appropriate confidence level.

## Agreement

If multiple vendors provide the same relevant value for a business event, Chronos can classify the event as:

`MULTI_SOURCE_AGREEMENT`

## Single Source

If only one valid vendor observation is available, the event is classified as:

`SINGLE_SOURCE`

## Evidence Preservation

Chronos does not discard source observations merely because one becomes canonical.

The reconciliation evidence layer retains:

- Winning observation
- Supporting observations
- Losing observations
- Source vendor
- Source record identifier
- Reported value
- Reconciliation outcome

## Example

Vendor observations:

```text
Vendor A | AAPL | 2026-01-05 | 125000
Vendor B | AAPL | 2026-01-05 | 130000
Vendor C | AAPL | 2026-01-05 | 130000
```

Vendor A has the highest configured source priority.

Therefore:

```text
Canonical revenue = 125000
Source = Vendor A
Reconciliation status = CONFLICT_RESOLVED
```

Vendor B and Vendor C observations remain available as reconciliation evidence.

## What Reconciliation Does Not Mean

Reconciliation does not mean that the highest value is selected.

It does not mean that the majority value is automatically selected.

It does not mean that lower-priority observations are deleted.

Configured source priority determines the canonical value for an eligible conflict.
