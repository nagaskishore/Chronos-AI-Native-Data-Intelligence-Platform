from src.agents.graph import app


question = """
What was the revenue for AAPL on January 5 2026?
"""


result = app.invoke(
    {
        "question": question,
        "repair_attempts": 0
    }
)


print("\n==============================")
print("FINAL RESULT")
print("==============================")

print("Question:")
print(result["question"])

print("\nSQL:")
print(result.get("generated_sql"))

print("\nValidation:")
print(result.get("validation_status"))

print("\nQuery Result:")
print(result.get("query_result"))

print("\nAnswer:")
print(result.get("answer"))

print("\nError:")
print(result.get("error"))