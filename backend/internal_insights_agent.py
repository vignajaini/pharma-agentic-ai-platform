class InternalInsightsAgent:
    def summarize_docs(self, molecule):
        return {
            "key_takeaways": [
                f"Internal review suggests {molecule} has potential in oncology repurposing."
            ]
        }
