import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class Supervisor:

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
You are the Chronos Supervisor.

Your job is to route the user's question
to the correct specialist agent.

Available agents:

SQL
- Questions requiring structured data analysis
- Revenue
- Ticker information
- Dates
- Aggregations
- Filtering
- Comparisons
- Trends
- Counts
- Numerical analysis

RAG
- Questions about documentation
- Business definitions
- Data definitions
- Source descriptions
- System explanations
- Policies
- Metadata
- Conceptual questions

Rules:

1. Return exactly one route.
2. The route must be either SQL or RAG.
3. Do not answer the user's question.
4. Do not generate SQL.
5. Do not retrieve documents.

Return exactly:

ROUTE: SQL

or

ROUTE: RAG
"""
                ),
                (
                    "human",
                    "User question:\n{question}"
                )
            ]
        )

    def route(self, question: str) -> dict:

        messages = self.prompt.format_messages(
            question=question
        )

        response = self.llm.invoke(messages)

        content = response.content.strip().upper()

        if "ROUTE: SQL" in content:

            return {
                "route": "SQL",
                "routing_reason": "Question requires structured data analysis."
            }

        if "ROUTE: RAG" in content:

            return {
                "route": "RAG",
                "routing_reason": "Question requires knowledge retrieval."
            }

        # Fail closed.
        return {
            "route": "RAG",
            "routing_reason": "Unable to confidently classify question."
        }