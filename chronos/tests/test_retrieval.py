from src.agents.vector_store import get_vector_store


QUESTIONS = [
    "Why does Chronos retain supporting observations?",
    "What is the difference between event time and knowledge time?",
    "Which vendor has the highest source priority?",
    "What does CONFLICT_RESOLVED mean?",
    "How does Chronos prevent unsafe AI-generated SQL?",
]


def main():
    vector_store = get_vector_store()

    for question in QUESTIONS:
        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)

        documents = vector_store.similarity_search(question, k=3)

        for index, document in enumerate(documents, start=1):
            print(f"\n[Result {index}]")
            print(f"Source: {document.metadata.get('document')}")
            print(f"Chunk: {document.metadata.get('chunk_id')}")
            print(document.page_content[:700])


if __name__ == "__main__":
    main()
