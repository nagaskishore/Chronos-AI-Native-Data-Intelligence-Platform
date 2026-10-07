from src.agents.snowflake_client import SnowflakeClient
from src.agents.schema_context import SchemaContext
from src.agents.sql_generator import SQLGenerator


client = SnowflakeClient()

schema = SchemaContext(client)
generator = SQLGenerator()

schema_context = schema.get_context()

sql = generator.generate(
    "What was AAPL revenue on January 5 2026?",
    schema_context
)

print(sql)

client.close()