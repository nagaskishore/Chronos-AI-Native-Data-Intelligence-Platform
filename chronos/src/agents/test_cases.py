# from src.agents.sql_validator import validate_sql
from chronos.src.agents.sql_validator_org import validate_sql
from snowflake_client import SnowflakeClient

sql = """
SELECT
    TICKER,
    REVENUE
FROM CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS
WHERE TICKER = 'AAPL'
"""

print(validate_sql(sql))

client = SnowflakeClient(
    account="EGQLJCW-QS91215",
    user="KISHORSVV",
    password="Venkateswara@10",
    warehouse="COMPUTE_WH",
    database="CHRONOS",
    schema="GOLD",
    role="ACCOUNTADMIN"
)

result = client.execute_query(
    "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE(), CURRENT_SCHEMA()"
)

print(result)

sql = """
DROP TABLE CHRONOS.GOLD.RECONCILED_EVENTS
"""

print(validate_sql(sql))