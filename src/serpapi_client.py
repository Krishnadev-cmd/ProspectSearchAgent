"""
SerpAPI Client for job postings and hiring signals
Free tier: 100 searches/month
API Docs: https://serpapi.com/search-api
"""
import logging
from typing import List, Dict, Any, Optional
from .api_client_base import BaseAPIClient

logger = logging.getLogger(__name__)


class SerpAPIClient(BaseAPIClient):
    """Client for SerpAPI - Google Jobs scraping"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://serpapi.com",
            calls_per_minute=20
        )
    
    def search_jobs(
        self,
        company_name: str,
        job_titles: Optional[List[str]] = None,
        location: str = "United States"
    ) -> Dict[str, Any]:
        """
        Search for job postings for a company
        
        Args:
            company_name: Company name to search
            job_titles: Specific job titles to look for
            location: Location filter
        
        Returns:
            Dict with job results and signals
        """
        # Build search query
        query = f"{company_name}"
        if job_titles:
            query += f" {' OR '.join(job_titles)}"
        
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": self.api_key,
            "num": 10  # Limit results to save credits
        }
        
        try:
            response = self._make_request(
                method="GET",
                endpoint="/search",
                params=params
            )
            
            return self._parse_job_results(response)
            
        except Exception as e:
            logger.error(f"SerpAPI job search failed for {company_name}: {str(e)}")
            return {
                "jobs_found": 0,
                "data_roles_count": 0,
                "recent_postings": [],
                "hiring_signal": False
            }
    
    def _parse_job_results(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SerpAPI response into structured hiring signals"""
        jobs = response.get("jobs_results", [])
        
        # Keywords that indicate data-related roles
        data_keywords = [
            "data", "analytics", "scientist", "engineer", 
            "machine learning", "ml", "ai", "artificial intelligence"
        ]
        
        data_roles_count = 0
        recent_postings = []
        
        for job in jobs[:10]:  # Limit to first 10
            title = job.get("title", "").lower()
            
            # Check if it's a data role
            is_data_role = any(keyword in title for keyword in data_keywords)
            if is_data_role:
                data_roles_count += 1
            
            recent_postings.append({
                "title": job.get("title"),
                "posted_at": job.get("detected_extensions", {}).get("posted_at"),
                "is_data_role": is_data_role
            })
        
        return {
            "jobs_found": len(jobs),
            "data_roles_count": data_roles_count,
            "recent_postings": recent_postings,
            "hiring_signal": data_roles_count > 0
        }
    
    def search_company_news(
        self,
        company_name: str,
        keywords: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for recent news about a company
        
        Args:
            company_name: Company name
            keywords: Additional keywords to filter news
        
        Returns:
            List of news items
        """
        query = f"{company_name}"
        if keywords:
            query += f" {' '.join(keywords)}"
        
        params = {
            "engine": "google",
            "q": query,
            "tbm": "nws",  # News search
            "api_key": self.api_key,
            "num": 5
        }
        
        try:
            response = self._make_request(
                method="GET",
                endpoint="/search",
                params=params
            )
            
            news_results = response.get("news_results", [])
            return [
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "source": item.get("source"),
                    "date": item.get("date"),
                    "snippet": item.get("snippet")
                }
                for item in news_results
            ]
            
        except Exception as e:
            logger.error(f"SerpAPI news search failed for {company_name}: {str(e)}")
            return []
