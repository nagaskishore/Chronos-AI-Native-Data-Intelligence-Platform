from typing import TypedDict, Optional, Dict, Any, List


class ChronosState(TypedDict, total=False):

    # --------------------------------------------------
    # User request
    # --------------------------------------------------

    question: str

    # --------------------------------------------------
    # Supervisor
    # --------------------------------------------------

    route: str
    routing_reason: str

    # --------------------------------------------------
    # SQL Agent
    # --------------------------------------------------

    schema_context: str
    generated_sql: str

    sql_validation_status: str
    sql_validation_reason: str

    repair_attempts: int

    query_result: Dict[str, Any]

    # --------------------------------------------------
    # RAG Agent
    # --------------------------------------------------

    retrieved_documents: List[str]
    retrieval_scores: List[float]

    retrieval_context: str

    # --------------------------------------------------
    # Final validation
    # --------------------------------------------------

    quality_status: str
    quality_reason: str

    # --------------------------------------------------
    # Final answer
    # --------------------------------------------------

    answer: str

    # --------------------------------------------------
    # Observability
    # --------------------------------------------------

    trace_id: str
    execution_log: List[Dict[str, Any]]

    # --------------------------------------------------
    # Errors
    # --------------------------------------------------

    error: Optional[str]