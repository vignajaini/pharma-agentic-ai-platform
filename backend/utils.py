import json
import hashlib
from datetime import datetime, timedelta
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Manages caching of molecule analyses"""
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl
        self.timestamps = {}
    
    def get_key(self, molecule, prompt):
        """Generate cache key from molecule and prompt"""
        key_str = f"{molecule}:{prompt}".lower()
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, molecule, prompt):
        """Get value from cache if not expired"""
        key = self.get_key(molecule, prompt)
        if key in self.cache:
            if datetime.utcnow() < self.timestamps[key]:
                logger.info(f"Cache hit for molecule: {molecule}")
                return self.cache[key]
            else:
                # Cache expired
                del self.cache[key]
                del self.timestamps[key]
                logger.info(f"Cache expired for molecule: {molecule}")
        return None
    
    def set(self, molecule, prompt, value):
        """Store value in cache with expiration"""
        key = self.get_key(molecule, prompt)
        self.cache[key] = value
        self.timestamps[key] = datetime.utcnow() + timedelta(seconds=self.ttl)
        logger.info(f"Cache set for molecule: {molecule}")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()
        logger.info("Cache cleared")
    
    def get_stats(self):
        """Get cache statistics"""
        return {
            "cached_items": len(self.cache),
            "ttl_seconds": self.ttl
        }


class RequestValidator:
    """Validates incoming requests"""
    
    @staticmethod
    def validate_query(data):
        """Validate query request data"""
        errors = []
        
        if not data:
            errors.append("Request body is empty")
            return errors
        
        molecule = data.get('molecule', '').strip()
        prompt = data.get('prompt', '').strip()
        
        if not molecule:
            errors.append("Molecule name is required")
        elif len(molecule) > 100:
            errors.append("Molecule name is too long (max 100 characters)")
        elif not molecule.replace(' ', '').isalnum():
            errors.append("Molecule name contains invalid characters")
        
        if not prompt:
            errors.append("Prompt is required")
        elif len(prompt) > 2000:
            errors.append("Prompt is too long (max 2000 characters)")
        
        return errors
    
    @staticmethod
    def validate_molecule_name(molecule):
        """Validate molecule name format"""
        if not molecule or not isinstance(molecule, str):
            return False
        
        molecule = molecule.strip()
        if not molecule:
            return False
        
        # Allow alphanumeric, spaces, hyphens, parentheses
        import re
        pattern = r'^[a-zA-Z0-9\s\-\(\)]+$'
        return bool(re.match(pattern, molecule))


class ResponseFormatter:
    """Formats API responses"""
    
    @staticmethod
    def success(data, message="Success", code=200):
        """Format success response"""
        return {
            "status": "success",
            "code": code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }, code
    
    @staticmethod
    def error(message, code=400, details=None):
        """Format error response"""
        response = {
            "status": "error",
            "code": code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        if details:
            response["details"] = details
        return response, code
    
    @staticmethod
    def validation_error(errors):
        """Format validation error response"""
        return {
            "status": "error",
            "code": 400,
            "message": "Validation failed",
            "timestamp": datetime.utcnow().isoformat(),
            "errors": errors
        }, 400


def handle_errors(f):
    """Decorator to handle common errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f"ValueError: {str(e)}")
            return ResponseFormatter.error(str(e), 400)
        except KeyError as e:
            logger.error(f"KeyError: {str(e)}")
            return ResponseFormatter.error(f"Missing required field: {str(e)}", 400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return ResponseFormatter.error("Internal server error", 500, str(e))
    return decorated_function
