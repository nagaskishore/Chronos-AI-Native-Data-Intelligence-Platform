import re


ALLOWED_STATEMENTS = {
    "SELECT",
    "WITH"
}


FORBIDDEN_KEYWORDS = {
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "MERGE",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE"
}


def validate_sql(sql: str) -> dict:

    sql_clean = sql.strip()

    if not sql_clean:
        return {
            "valid": False,
            "reason": "Empty SQL"
        }

    first_word = sql_clean.split()[0].upper()

    if first_word not in ALLOWED_STATEMENTS:
        return {
            "valid": False,
            "reason": (
                f"Statement type '{first_word}' "
                "is not allowed"
            )
        }

    sql_upper = sql_clean.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql_upper):
            return {
                "valid": False,
                "reason": (
                    f"Forbidden SQL keyword: {keyword}"
                )
            }

    return {
        "valid": True,
        "reason": "SQL passed validation"
    }