from datetime import datetime
import uuid


def create_trace_id():

    return str(uuid.uuid4())


def log_event(
    state: dict,
    node: str,
    status: str,
    details: dict | None = None
):

    logs = state.get(
        "execution_log",
        []
    )

    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "node": node,
        "status": status,
        "details": details or {}
    }

    logs.append(event)

    return {
        "execution_log": logs
    }