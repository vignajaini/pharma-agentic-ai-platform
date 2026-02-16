import json
import os
import logging

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

class EXIMAgent:
    """EXIM Trade Flow Analysis Agent"""
    
    DEFAULT_TRADE_DATA = {
        "imports": 45000000,
        "exports": 60000000,
        "countries": [
            {"name": "China", "imports": 25000000, "exports": 15000000},
            {"name": "India", "imports": 15000000, "exports": 30000000},
            {"name": "Germany", "imports": 5000000, "exports": 15000000}
        ],
        "trends": "Increasing trade volume with emerging markets"
    }
    
    def fetch_trade(self, molecule):
        """Fetch trade data for a molecule"""
        try:
            path = os.path.join(DATA_DIR, "mock_exim.json")
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)
                # Case-insensitive lookup
                lookup = {k.strip().lower(): v for k, v in data.items()}
                result = lookup.get((molecule or '').strip().lower())
                if result:
                    logger.info(f"EXIM: Found trade data for {molecule}")
                    return result
                else:
                    logger.info(f"EXIM: No trade data for {molecule}, returning default example")
                    return self.DEFAULT_TRADE_DATA.copy()
            else:
                logger.warning(f"EXIM data file not found, using default data")
                return self.DEFAULT_TRADE_DATA.copy()
        except Exception as e:
            logger.error(f"EXIM: Error fetching trade data: {str(e)}")
            return {}
