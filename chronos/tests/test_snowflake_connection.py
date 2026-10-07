from src.agents.snowflake_client import SnowflakeClient


client = SnowflakeClient()

result = client.execute_query(
    """
    SELECT
        CURRENT_DATABASE(),
        CURRENT_SCHEMA(),
        CURRENT_USER()
    """
)

print(result)

client.close()