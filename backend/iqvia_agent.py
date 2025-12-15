import json
import os
import logging

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class IQVIAAgent:
    """IQVIA Market Intelligence Agent"""
    
    DEFAULT_MARKET_DATA = {
        "market_size": 500000000,  # $500M default
        "cagr": 5.5,  # 5.5% growth
        "regions": [
            {"name": "North America", "size": 250000000, "growth": 4.2},
            {"name": "Europe", "size": 150000000, "growth": 3.8},
            {"name": "Asia Pacific", "size": 100000000, "growth": 8.5}
        ],
        "key_players": ["Company A", "Company B", "Company C"],
        "competitive_landscape": "Moderate competition with several established players and emerging entrants",
        "forecast": "Steady growth expected due to aging population and increased R&D"
    }
    
    def fetch_market(self, molecule):
        """
        Fetch market data for a molecule
        
        Args:
            molecule: Molecule name
        
        Returns:
            Dictionary containing market analysis
        """
        try:
            path = os.path.join(DATA_DIR, "mock_iqvia.json")
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)
                result = data.get(molecule, data.get("default", self.DEFAULT_MARKET_DATA))
                logger.info(f"IQVIA: Found market data for {molecule}")
                return result
            else:
                logger.warning(f"IQVIA data file not found, using default data")
                return self.DEFAULT_MARKET_DATA.copy()
        except Exception as e:
            logger.error(f"IQVIA: Error fetching market data: {str(e)}")
            return self.DEFAULT_MARKET_DATA.copy()
