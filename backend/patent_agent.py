import json
import os
import logging

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class PatentAgent:
    """Patent Landscape Analysis Agent"""
    
    def search_patents(self, molecule):
        """Search for patents related to a molecule"""
        try:
            path = os.path.join(DATA_DIR, "mock_patents.json")
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)
                result = data.get(molecule, [])
                logger.info(f"Patent: Found {len(result)} patents for {molecule}")
                return result
            else:
                logger.warning(f"Patent data file not found")
                return []
        except Exception as e:
            logger.error(f"Patent: Error searching patents: {str(e)}")
            return []
