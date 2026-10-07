# Chronos Agent Operating Rules

## Purpose

Chronos uses specialized AI agents rather than a single general-purpose agent.

Each agent has a clearly defined responsibility and operates within explicit boundaries.

## Supervisor Agent

The Supervisor is responsible for intent classification and routing.

It can:

- Understand the user question
- Determine whether the question is analytical or knowledge-oriented
- Select SQL or RAG

It cannot:

- Generate SQL
- Execute SQL
- Retrieve documents
- Provide the final answer

## SQL Specialist

The SQL specialist handles structured analytical questions.

It can:

- Retrieve schema context
- Generate SQL
- Validate SQL
- Repair invalid SQL
- Execute approved queries
- Validate query results

It cannot:

- Modify database data
- Execute arbitrary SQL
- Access unapproved tables
- Bypass SQL validation
- Decide the final user-facing answer

## RAG Specialist

The RAG specialist handles knowledge-oriented questions.

It can:

- Search the vector store
- Retrieve relevant Chronos documents
- Build evidence context

It cannot:

- Invent missing evidence
- Modify source documents
- Bypass retrieval
- Independently override the quality gate

## Quality Validator

The quality validator acts as a common trust boundary.

It verifies that specialist output satisfies minimum requirements before final answer generation.

The quality validator should be deterministic where possible.

## Final Answer Generator

The final answer generator converts validated evidence into a user-facing response.

It must:

- Use only supplied evidence
- Avoid unsupported claims
- Clearly communicate uncertainty
- Explain relevant source or reconciliation information
- Avoid pretending unavailable information was retrieved

## SQL Safety

AI-generated SQL is considered untrusted until validated.

The current POC SQL policy allows only:

- `SELECT`
- `WITH`

queries against:

`CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS`

The SQL validator rejects:

- INSERT
- UPDATE
- DELETE
- DROP
- ALTER
- TRUNCATE
- MERGE
- CREATE
- GRANT
- REVOKE
- CALL
- COPY
- PUT
- REMOVE

Multiple SQL statements are not allowed.

## Evidence Grounding

An answer should be grounded in evidence produced by the appropriate specialist.

The system should not treat the LLM's general knowledge as authoritative for Chronos-specific facts.

## Failure Handling

If SQL validation fails, the SQL specialist may attempt a bounded repair.

If retrieval produces no supporting documents, the RAG path should fail rather than fabricate an answer.

If the quality gate fails, final answer generation should not proceed normally.

## Separation of Responsibilities

Chronos intentionally separates:

```text
Intent
  |
  v
Specialist execution
  |
  v
Validation
  |
  v
Answer generation
```

This prevents one general-purpose agent from having unrestricted responsibility.

## Design Principle

The goal of agent orchestration is not to maximize the number of agents.

The goal is to give each agent a narrow responsibility with explicit boundaries and deterministic validation wherever possible.
