class QualityValidator:

    def validate(self, state: dict) -> dict:

        route = state.get("route")

        # ----------------------------------------------
        # SQL validation
        # ----------------------------------------------

        if route == "SQL":

            if state.get("sql_validation_status") != "RESULT_VALID":

                return {
                    "valid": False,
                    "reason": "SQL result validation failed."
                }

            result = state.get("query_result")

            if result is None:

                return {
                    "valid": False,
                    "reason": "No query result available."
                }

            return {
                "valid": True,
                "reason": "SQL result passed quality checks."
            }

        # ----------------------------------------------
        # RAG validation
        # ----------------------------------------------

        if route == "RAG":

            documents = state.get(
                "retrieved_documents",
                []
            )

            if not documents:

                return {
                    "valid": False,
                    "reason": "No supporting documents were retrieved."
                }

            return {
                "valid": True,
                "reason": "RAG response has supporting evidence."
            }

        return {
            "valid": False,
            "reason": "Unknown route."
        }