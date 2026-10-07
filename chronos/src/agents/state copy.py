from typing import TypedDict, Optional, Dict, Any


class SQLAgentState(TypedDict, total=False):

    # User input
    question: str

    # Retrieved metadata/schema
    schema_context: str

    # LLM-generated SQL
    generated_sql: str

    # SQL validation
    validation_status: str
    validation_reason: str

    # Repair loop
    repair_attempts: int

    # Snowflake execution
    query_result: Dict[str, Any]

    # Final natural-language answer
    answer: str

    # Workflow status
    error: Optional[str]