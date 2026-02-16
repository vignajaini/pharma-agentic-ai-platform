import json
import os
import logging

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

class ClinicalTrialsAgent:
    """Clinical Trials Research Agent"""
    
    def search_trials(self, molecule):
        """Search for clinical trials for a molecule"""
        try:
            path = os.path.join(DATA_DIR, "mock_trials.json")
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)

                # Case-insensitive lookup for molecule keys
                lookup = {k.strip().lower(): v for k, v in data.items()}
                result = lookup.get((molecule or '').strip().lower())
                if result:
                    logger.info(f"Clinical: Found {len(result)} trials for {molecule}")
                    return result
                else:
                    logger.info(f"Clinical: No trials for {molecule}, returning example trial")
                    return [
                        {"trial_id": "NCT9999", "phase": "Phase I", "status": "Recruiting", "title": f"Example trial for {molecule}"}
                    ]
            else:
                logger.warning(f"Clinical trials data file not found")
                return []
        except Exception as e:
            logger.error(f"Clinical: Error searching trials: {str(e)}")
            return []
