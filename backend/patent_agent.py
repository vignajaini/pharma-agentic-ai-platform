import json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class PatentAgent:
    def search_patents(self, molecule):
        path = os.path.join(DATA_DIR, "mock_patents.json")
        try:
            with open(path) as f:
                data = json.load(f)
            return data.get(molecule, [])
        except:
            return []
