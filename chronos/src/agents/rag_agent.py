class RAGAgent:

    def __init__(self, retriever=None):

        self.retriever = retriever

    def run(self, question: str):

        if self.retriever is None:

            return {
                "documents": [],
                "scores": [],
                "context": "",
                "error": "Retriever is not configured"
            }

        documents = self.retriever.retrieve(question)

        context = "\n\n".join(
            documents
        )

        return {
            "documents": documents,
            "scores": [],
            "context": context
        }