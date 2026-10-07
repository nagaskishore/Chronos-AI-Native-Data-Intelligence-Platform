# Chronos Architecture

## Overview

Chronos is an AI-native data intelligence and operations platform combining data engineering, data quality, temporal modeling, reconciliation, Snowflake analytics, retrieval-augmented generation, agentic orchestration, AI-generated SQL, deterministic validation, and observability.

The platform separates data processing from AI reasoning.

## High-Level Flow

```text
External Vendor Data
        |
        v
   Bronze Ingestion
        |
        v
 Silver Normalization
        |
        v
  Data Quality Checks
        |
        v
 Temporal Data Model
        |
        v
  Reconciliation
        |
        v
     Gold Layer
        |
        +--------------------+
        |                    |
        v                    v
 Snowflake Semantic      Vector Store
       View                   |
        |                    |
        v                    v
    SQL Agent             RAG Agent
        |                    |
        +---------+----------+
                  |
                  v
           Quality Gate
                  |
                  v
        Final Answer Generator
                  |
                  v
             User Answer
```

## Bronze Layer

Bronze preserves source data in its original form.

Responsibilities:

- Source preservation
- Raw ingestion
- Batch identification
- Traceability

Bronze should not contain business reconciliation logic.

## Silver Layer

Silver converts heterogeneous vendor schemas into the canonical Chronos model.

Responsibilities:

- Field normalization
- Data type normalization
- Standardized timestamps
- Vendor identification
- Canonical field mapping

## Data Quality Layer

The quality layer performs deterministic validation:

- Required field validation
- Negative revenue checks
- Currency validation
- Source duplicate detection

Invalid records are quarantined.

## Temporal Layer

The temporal layer tracks:

- Event time
- Knowledge time
- Ingestion time
- Record versions
- Current state
- Historical state

## Reconciliation Layer

The reconciliation layer compares valid observations representing the same business event.

Business event identity:

`ticker + event_time`

Configured source priority is used when conflicts exist.

Supporting evidence is preserved separately.

## Gold Layer

The Gold layer contains trusted, reconciled business results.

The AI layer should consume the Gold semantic representation rather than raw source data.

## Snowflake Semantic View

Chronos exposes:

`CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS`

This view provides a controlled interface for AI-generated analytical queries.

The SQL agent is restricted to this approved view.

## SQL Agent

The SQL specialist handles structured analytical questions.

Workflow:

1. Retrieve schema context.
2. Generate SQL.
3. Validate SQL.
4. Repair invalid SQL when necessary.
5. Execute against Snowflake.
6. Validate the result.
7. Return structured evidence to the parent graph.

The SQL agent does not generate the final user-facing answer.

## RAG Agent

The RAG specialist handles knowledge-oriented questions.

Workflow:

1. Receive the user question.
2. Search the Chronos vector store.
3. Retrieve relevant knowledge documents.
4. Build evidence context.
5. Return retrieved evidence to the parent graph.

The RAG agent does not independently generate the final answer.

## Supervisor

The Supervisor determines which specialist should handle a question.

Structured analytical questions are routed to SQL.

Knowledge-oriented questions are routed to RAG.

The Supervisor does not answer questions and does not execute SQL.

## Quality Gate

Both specialist paths pass through a common quality gate.

The quality gate verifies that specialist output is usable before final answer generation.

This creates a trust boundary between probabilistic AI reasoning and final response generation.

## Final Answer Generator

The final answer generator receives:

- The original user question
- Validated SQL results, or
- Retrieved RAG evidence

It generates the user-facing response using only trusted evidence.

## Observability

Chronos records:

- Trace ID
- Supervisor route
- Agent execution
- Validation results
- Query execution
- Retrieval information
- Quality-gate outcome
- Errors
- Timing information

## Core Architecture Principle

Chronos separates:

**Reasoning**

from

**Execution**

and

**Validation**

LLMs can propose actions and interpretations. Deterministic components decide whether those actions are allowed.

## AI Trust Boundary

LLM output is an untrusted artifact until validated.

For SQL:

```text
LLM-generated SQL
        |
        v
deterministic validation
        |
        v
approved semantic view
        |
        v
Snowflake execution
```

For RAG:

```text
User question
      |
      v
retrieval
      |
      v
supporting evidence
      |
      v
quality validation
      |
      v
final answer
```
