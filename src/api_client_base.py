"""
Base API client with rate limiting and error handling
"""
import time
import logging
from typing import Optional, Dict, Any
import requests
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call = 0
    
    def wait(self):
        """Wait if necessary to respect rate limit"""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry failed API calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator


class BaseAPIClient:
    """Base class for all API clients"""
    
    def __init__(self, api_key: str, base_url: str, calls_per_minute: int = 60):
        self.api_key = api_key
        self.base_url = base_url
        self.rate_limiter = RateLimiter(calls_per_minute)
        self.session = requests.Session()
        self.timeout = 30
    
    @retry_on_failure(max_retries=3, delay=1.0)
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an API request with rate limiting and error handling"""
        self.rate_limiter.wait()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        default_headers = self._get_headers()
        if headers:
            default_headers.update(headers)
        
        logger.info(f"Making {method} request to {url}")
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            headers=default_headers,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        return response.json()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get default headers for requests. Override in subclasses."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def close(self):
        """Close the session"""
        self.session.close()
