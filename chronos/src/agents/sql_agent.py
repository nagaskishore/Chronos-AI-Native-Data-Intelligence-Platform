from src.agents.snowflake_client import SnowflakeClient
from src.agents.schema_context import SchemaContext
from src.agents.sql_generator import SQLGenerator
from src.agents.sql_validator import validate_sql
from src.agents.answer_generator import AnswerGenerator


class SQLAgent:

    def __init__(self):

        self.snowflake = SnowflakeClient()

        self.schema_context = SchemaContext(
            self.snowflake
        )

        self.generator = SQLGenerator()
        
        self.answer_generator = AnswerGenerator()

    def run(self, question: str):

        # -----------------------------------------
        # 1. Retrieve schema context
        # -----------------------------------------

        schema = self.schema_context.get_context()

        # -----------------------------------------
        # 2. Generate SQL
        # -----------------------------------------

        generated_sql = self.generator.generate(
            question=question,
            schema_context=schema
        )

        # -----------------------------------------
        # 3. Validate SQL
        # -----------------------------------------

        validation = validate_sql(
            generated_sql
        )

        if not validation["valid"]:

            return {
                "success": False,
                "question": question,
                "sql": generated_sql,
                "validation": validation,
                "result": None
            }

        # -----------------------------------------
        # 4. Execute SQL
        # -----------------------------------------

        result = self.snowflake.execute_query(
            generated_sql
        )
        
        answer = self.answer_generator.generate(
            question=question,
            sql=generated_sql,
            result=result
        )

        # -----------------------------------------
        # 5. Return structured result
        # -----------------------------------------

        return {
            "success": True,
            "question": question,
            "sql": generated_sql,
            "validation": validation,
            "result": result,
            "answer": answer
        }

    def close(self):

        self.snowflake.close()