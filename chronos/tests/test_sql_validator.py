from src.agents.sql_validator import validate_sql


sql = """
SELECT
    TICKER,
    REVENUE
FROM CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS
WHERE TICKER = 'AAPL'
"""

print(validate_sql(sql))

sql = """
DROP TABLE CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS
"""

print(validate_sql(sql))

sql = """
DELETE FROM CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS
"""

print(validate_sql(sql))

sql = """
SELECT * FROM SOME_OTHER_TABLE
"""

print(validate_sql(sql))