import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pharma_backend.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# API Configuration
API_CONFIG = {
    'MAX_MOLECULE_LENGTH': 100,
    'MAX_PROMPT_LENGTH': 2000,
    'CACHE_ENABLED': True,
    'CACHE_TTL': 3600,  # 1 hour
    'LOG_REQUESTS': True,
    'ALLOWED_METHODS': ['POST', 'GET'],
    # LLM / provider configuration (set via environment variables for production)
    'LLM_PROVIDER': os.getenv('LLM_PROVIDER', 'openai'),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', None),
}

# Database/Storage paths
STORAGE_PATHS = {
    'reports': '../storage/reports',
    'cache': '../storage/cache',
    'logs': '../storage/logs',
}

# Agent timeout settings (in seconds)
AGENT_TIMEOUTS = {
    'iqvia': 10,
    'exim': 10,
    'patent': 15,
    'clinical': 15,
    'web': 20,
    'internal': 10,
}

# Response codes
RESPONSE_CODES = {
    'SUCCESS': 200,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
    'INTERNAL_ERROR': 500,
    'TIMEOUT': 504,
}
