"""
Apollo.io API Client
Free tier: 100 credits (searches)
API Docs: https://apolloio.github.io/apollo-api-docs/
"""
import logging
from typing import List, Dict, Any, Optional
from .api_client_base import BaseAPIClient

logger = logging.getLogger(__name__)


class ApolloClient(BaseAPIClient):
    """Client for Apollo.io API"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://api.apollo.io/v1",
            calls_per_minute=30  # Conservative rate limit
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with API key"""
        headers = super()._get_headers()
        headers["X-Api-Key"] = self.api_key
        headers["Cache-Control"] = "no-cache"
        return headers
    
    def search_organizations(
        self,
        industries: Optional[List[str]] = None,
        revenue_range: Optional[tuple] = None,
        employee_count_range: Optional[tuple] = None,
        location: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Dict[str, Any]:
        """
        Search for organizations matching criteria
        NOTE: Free tier has limited access. This returns mock data as fallback.
        
        Returns:
            Dict with 'organizations' list and pagination info
        """
        logger.warning("Apollo free tier has limited endpoints. Consider using enrichment instead.")
        
        # Apollo free tier doesn't support mixed_companies/search
        # Return empty results or use enrichment APIs instead
        # For a working demo, we'll return a message
        logger.info("Apollo organization search: Using fallback for free tier limitations")
        
        return {
            "organizations": [],
            "pagination": {},
            "message": "Apollo free tier doesn't support company search. Use enrichment or upgrade plan."
        }
    
    def search_people(
        self,
        organization_ids: Optional[List[str]] = None,
        titles: Optional[List[str]] = None,
        seniorities: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Dict[str, Any]:
        """
        Search for people (contacts) matching criteria
        
        Returns:
            Dict with 'people' list and pagination info
        """
        body = {
            "page": page,
            "per_page": min(per_page, 25),
        }
        
        if organization_ids:
            body["organization_ids"] = organization_ids
        
        if titles:
            body["person_titles"] = titles
        
        if seniorities:
            body["person_seniorities"] = seniorities
        
        try:
            response = self._make_request(
                method="POST",
                endpoint="/mixed_people/search",
                json_data=body
            )
            return response
        except Exception as e:
            logger.error(f"Apollo people search failed: {str(e)}")
            return {"people": [], "pagination": {}}
    
    def enrich_organization(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Enrich organization data by domain
        
        Args:
            domain: Company domain (e.g., 'apollo.io')
        
        Returns:
            Enriched organization data or None
        """
        try:
            response = self._make_request(
                method="GET",
                endpoint="/organizations/enrich",
                params={"domain": domain}
            )
            return response.get("organization")
        except Exception as e:
            logger.error(f"Apollo organization enrichment failed for {domain}: {str(e)}")
            return None
    
    def enrich_person(self, email: Optional[str] = None, 
                      first_name: Optional[str] = None,
                      last_name: Optional[str] = None,
                      organization_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Enrich person data
        
        Returns:
            Enriched person data or None
        """
        params = {}
        if email:
            params["email"] = email
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if organization_name:
            params["organization_name"] = organization_name
        
        if not params:
            logger.warning("No search parameters provided for person enrichment")
            return None
        
        try:
            response = self._make_request(
                method="GET",
                endpoint="/people/match",
                params=params
            )
            return response.get("person")
        except Exception as e:
            logger.error(f"Apollo person enrichment failed: {str(e)}")
            return None
