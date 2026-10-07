import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


class SQLGenerator:

    def __init__(self):

        self.llm = ChatGroq(
            #model="llama-3.3-70b-versatile",
            model="qwen/qwen3.8-27b",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the Chronos SQL generation agent.

Your job is to translate a user's natural-language
question into safe, read-only Snowflake SQL.

DATABASE:
CHRONOS

SCHEMA:
GOLD

ALLOWED TABLE:
CHRONOS.GOLD.V_AI_FINANCIAL_EVENTS

You must use ONLY the table and columns provided
in the schema context.

RULES:

1. Generate SELECT or WITH queries only.
2. Never generate INSERT.
3. Never generate UPDATE.
4. Never generate DELETE.
5. Never generate DROP.
6. Never generate ALTER.
7. Never generate CREATE.
8. Never generate MERGE.
9. Never generate TRUNCATE.
10. Never access tables outside the allowed table.
11. Never invent columns.
12. Never invent values.
13. Do not modify data.
14. Return ONLY SQL.
15. Do not wrap SQL in markdown code fences.

SCHEMA CONTEXT:

{schema_context}
"""
                ),
                (
                    "human",
                    "User question:\n{question}"
                )
            ]
        )

    def generate(self, question: str, schema_context: str):

        messages = self.prompt.format_messages(
            question=question,
            schema_context=schema_context
        )

        response = self.llm.invoke(messages)

        return response.content.strip()