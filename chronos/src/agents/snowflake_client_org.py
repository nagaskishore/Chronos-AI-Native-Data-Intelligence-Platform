import snowflake.connector


class SnowflakeClient:

    def __init__(
        self,
        account,
        user,
        password,
        warehouse,
        database,
        schema,
        role=None
    ):
        self.connection = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            warehouse=warehouse,
            database=database,
            schema=schema,
            role=role
        )

    def execute_query(self, sql):
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
                "rows": rows
            }

        finally:
            cursor.close()