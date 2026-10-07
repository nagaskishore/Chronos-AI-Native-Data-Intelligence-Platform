import re


ALLOWED_TABLE = (
    "CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS"
)


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "MERGE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "CALL",
    "COPY",
    "PUT",
    "REMOVE"
}


def validate_sql(sql: str) -> dict:

    sql_clean = sql.strip()

    if not sql_clean:
        return {
            "valid": False,
            "reason": "SQL is empty"
        }

    # Remove a trailing semicolon but reject multiple statements.
    sql_without_trailing_semicolon = sql_clean.rstrip(";")

    if ";" in sql_without_trailing_semicolon:
        return {
            "valid": False,
            "reason": "Multiple SQL statements are not allowed"
        }

    first_word = (
        sql_without_trailing_semicolon
        .split()[0]
        .upper()
    )

    if first_word not in {"SELECT", "WITH"}:
        return {
            "valid": False,
            "reason": (
                f"Statement '{first_word}' "
                "is not allowed"
            )
        }

    sql_upper = sql_without_trailing_semicolon.upper()

    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql_upper):

            return {
                "valid": False,
                "reason": (
                    f"Forbidden SQL keyword: {keyword}"
                )
            }

    # Require our approved table.
    if ALLOWED_TABLE not in sql_upper:
        return {
            "valid": False,
            "reason": (
                "SQL must query the approved "
                "Chronos semantic view"
            )
        }

    return {
        "valid": True,
        "reason": "SQL passed validation"
    }