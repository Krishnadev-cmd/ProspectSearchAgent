"""
Crunchbase API Client
Free tier: Basic company data
API Docs: https://data.crunchbase.com/docs
"""
import logging
from typing import List, Dict, Any, Optional
from .api_client_base import BaseAPIClient

logger = logging.getLogger(__name__)


class CrunchbaseClient(BaseAPIClient):
    """Client for Crunchbase API"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://api.crunchbase.com/api/v4",
            calls_per_minute=20  # Conservative rate limit
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with API key"""
        headers = super()._get_headers()
        # Crunchbase uses user-key in headers
        headers["X-cb-user-key"] = self.api_key
        return headers
    
    def search_organizations(
        self,
        categories: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        funding_rounds: Optional[List[str]] = None,
        employee_range: Optional[str] = None,
        revenue_range: Optional[str] = None,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Search for organizations
        
        Args:
            categories: Industry categories
            locations: Location names (e.g., ['United States'])
            funding_rounds: Funding stage filters
            employee_range: Employee count range (e.g., '101-250')
            revenue_range: Revenue range
            limit: Max results
        
        Returns:
            List of organization entities
        """
        # Build field IDs for the query
        field_ids = [
            "identifier",
            "name",
            "short_description",
            "website",
            "revenue_range",
            "num_employees_enum",
            "categories",
            "location_identifiers",
            "funding_total"
        ]
        
        # Build query filters
        query = []
        
        if categories:
            query.append({
                "type": "predicate",
                "field_id": "categories",
                "operator_id": "includes",
                "values": categories
            })
        
        if locations:
            query.append({
                "type": "predicate",
                "field_id": "location_identifiers",
                "operator_id": "includes",
                "values": locations
            })
        
        if employee_range:
            query.append({
                "type": "predicate",
                "field_id": "num_employees_enum",
                "operator_id": "eq",
                "values": [employee_range]
            })
        
        if funding_rounds:
            query.append({
                "type": "predicate",
                "field_id": "last_funding_type",
                "operator_id": "includes",
                "values": funding_rounds
            })
        
        body = {
            "field_ids": field_ids,
            "limit": min(limit, 100),
            "order": [
                {
                    "field_id": "rank_org",
                    "sort": "asc"
                }
            ]
        }
        
        if query:
            body["query"] = query
        
        try:
            response = self._make_request(
                method="POST",
                endpoint="/searches/organizations",
                json_data=body
            )
            
            entities = response.get("entities", [])
            return [entity.get("properties", {}) for entity in entities]
            
        except Exception as e:
            logger.error(f"Crunchbase organization search failed: {str(e)}")
            return []
    
    def get_organization(self, permalink: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed organization data by permalink
        
        Args:
            permalink: Crunchbase permalink (e.g., 'apollo-io')
        
        Returns:
            Organization details or None
        """
        field_ids = [
            "identifier",
            "name",
            "description",
            "website",
            "revenue_range",
            "num_employees_enum",
            "categories",
            "location_identifiers",
            "funding_total",
            "last_funding_at",
            "last_funding_type",
            "founded_on",
            "company_type",
            "ipo_status"
        ]
        
        params = {
            "field_ids": ",".join(field_ids)
        }
        
        try:
            response = self._make_request(
                method="GET",
                endpoint=f"/entities/organizations/{permalink}",
                params=params
            )
            return response.get("properties", {})
        except Exception as e:
            logger.error(f"Crunchbase get organization failed for {permalink}: {str(e)}")
            return None
    
    def search_funding_rounds(
        self,
        organization_name: Optional[str] = None,
        funding_types: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for funding rounds
        
        Args:
            organization_name: Filter by organization
            funding_types: Types of funding (e.g., ['series_a', 'series_b'])
            limit: Max results
        
        Returns:
            List of funding round entities
        """
        field_ids = [
            "identifier",
            "announced_on",
            "investment_type",
            "money_raised",
            "organization_identifier",
            "investor_identifiers"
        ]
        
        query = []
        
        if organization_name:
            query.append({
                "type": "predicate",
                "field_id": "organization_identifier",
                "operator_id": "includes",
                "values": [organization_name]
            })
        
        if funding_types:
            query.append({
                "type": "predicate",
                "field_id": "investment_type",
                "operator_id": "includes",
                "values": funding_types
            })
        
        body = {
            "field_ids": field_ids,
            "limit": min(limit, 100),
            "order": [
                {
                    "field_id": "announced_on",
                    "sort": "desc"
                }
            ]
        }
        
        if query:
            body["query"] = query
        
        try:
            response = self._make_request(
                method="POST",
                endpoint="/searches/funding_rounds",
                json_data=body
            )
            
            entities = response.get("entities", [])
            return [entity.get("properties", {}) for entity in entities]
            
        except Exception as e:
            logger.error(f"Crunchbase funding rounds search failed: {str(e)}")
            return []
