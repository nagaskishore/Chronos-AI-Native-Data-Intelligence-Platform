from pathlib import Path

from src.agents.knowledge_ingestion import ChronosKnowledgeIngestion
from src.agents.vector_store import get_vector_store


def main():
    ingestion = ChronosKnowledgeIngestion(
        knowledge_dir="data/knowledge",
        chunk_size=900,
        chunk_overlap=120,
    )

    documents = ingestion.ingest_documents()
    vector_store = get_vector_store()

    # Stable IDs make repeated ingestion deterministic for this POC.
    ids = [
        f'{doc.metadata["document"]}::chunk-{doc.metadata["chunk_id"]}'
        for doc in documents
    ]

    vector_store.add_documents(
        documents=documents,
        ids=ids,
    )

    print(f"Loaded source documents: {len(ingestion.load_documents())}")
    print(f"Created chunks: {len(documents)}")
    print(f"Vector store: data/vector_store/chronos_knowledge")
    print("Knowledge ingestion completed successfully.")


if __name__ == "__main__":
    main()
