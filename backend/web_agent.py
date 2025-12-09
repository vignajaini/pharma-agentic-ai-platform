class WebAgent:
    def search(self, molecule):
        return {
            "top_papers": [
                {"title": f"Research on {molecule} for metabolic disorders", "source": "MockJournal"}
            ]
        }
