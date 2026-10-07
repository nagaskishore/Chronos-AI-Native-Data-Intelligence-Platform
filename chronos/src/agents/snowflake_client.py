import os

import snowflake.connector
from dotenv import load_dotenv


load_dotenv()


class SnowflakeClient:

    def __init__(self):
        self.connection = snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE", "CHRONOS"),
            schema=os.getenv("SNOWFLAKE_SCHEMA", "GOLD"),
            role=os.getenv("SNOWFLAKE_ROLE"),
        )

    def execute_query(self, sql: str):

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql)

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = cursor.fetchall()

            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows)
            }

        finally:
            cursor.close()

    def close(self):
        self.connection.close()