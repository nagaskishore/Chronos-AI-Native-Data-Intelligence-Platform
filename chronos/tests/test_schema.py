from src.agents.snowflake_client import SnowflakeClient
from src.agents.schema_context import SchemaContext


client = SnowflakeClient()

schema_context = SchemaContext(client)

print(schema_context.get_context())

client.close()