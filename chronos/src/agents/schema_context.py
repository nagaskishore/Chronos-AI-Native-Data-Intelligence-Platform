from src.agents.snowflake_client import SnowflakeClient


class SchemaContext:

    TABLE_NAME = "CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS"

    def __init__(self, client: SnowflakeClient):
        self.client = client

    def get_context(self) -> str:

        # sql = """
        # SELECT
        #     COLUMN_NAME,
        #     DATA_TYPE,
        #     DESCRIPTION,
        #     BUSINESS_MEANING
        # FROM CHRONOS.AI.DATA_DICTIONARY
        # WHERE TABLE_NAME = 'V_AI_FINANCIAL_EVENTS'
        # ORDER BY ORDINAL_POSITION
        # """
        
        sql = """
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    DESCRIPTION,
                    BUSINESS_MEANING
                FROM CHRONOS.AI.DATA_DICTIONARY
                WHERE TABLE_NAME = 'V_AI_FINANCIAL_EVENTS'
                ORDER BY COLUMN_NAME
                """

        result = self.client.execute_query(sql)

        lines = [
            f"TABLE: {self.TABLE_NAME}",
            "",
            "AVAILABLE COLUMNS:"
        ]

        for row in result["rows"]:

            column_name = row[0]
            data_type = row[1]
            description = row[2]
            business_meaning = row[3]

            lines.append(
                f"- {column_name} ({data_type})"
            )

            lines.append(
                f"  Description: {description}"
            )

            lines.append(
                f"  Business meaning: {business_meaning}"
            )

        return "\n".join(lines)