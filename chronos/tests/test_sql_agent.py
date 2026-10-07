from src.agents.sql_agent import SQLAgent


agent = SQLAgent()

response = agent.run(
    "What was AAPL revenue on January 5 2026?"
)

print(response)

agent.close()