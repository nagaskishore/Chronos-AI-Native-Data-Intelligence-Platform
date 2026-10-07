import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


class AnswerGenerator:

    def __init__(self):

        self.llm = ChatGroq(
            model="qwen/qwen3.8-27b",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the Chronos answer generation agent.

Answer the user's question using ONLY the
Snowflake query result provided.

Rules:

1. Do not invent facts.
2. Do not invent values.
3. Do not modify numbers.
4. If the result contains no rows, say that no matching
   data was found.
5. Mention the source when available.
6. Mention reconciliation status when available.
7. Mention confidence when available.
8. Keep the answer concise.
"""
                ),
                (
                    "human",
                    """
QUESTION:
{question}

SQL:
{sql}

QUERY RESULT:
{result}
"""
                )
            ]
        )

    def generate(
        self,
        question: str,
        sql: str,
        result: dict
    ):

        messages = self.prompt.format_messages(
            question=question,
            sql=sql,
            result=result
        )

        response = self.llm.invoke(messages)

        return response.content.strip()