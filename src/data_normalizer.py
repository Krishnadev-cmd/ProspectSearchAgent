"""
Data normalizer to convert different API responses into unified schema
"""
import logging
from typing import Dict, Any, List, Optional
import tldextract

logger = logging.getLogger(__name__)


class DataNormalizer:
    """Normalize data from different sources into unified schema"""
    
    @staticmethod
    def normalize_apollo_organization(apollo_org: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Apollo organization data
        
        Args:
            apollo_org: Raw organization data from Apollo
        
        Returns:
            Normalized company dict
        """
        try:
            # Extract domain
            domain = apollo_org.get("website_url") or apollo_org.get("domain", "")
            if domain:
                domain = DataNormalizer._clean_domain(domain)
            
            # Revenue mapping
            revenue = None
            revenue_range = apollo_org.get("estimated_num_employees")
            if revenue_range:
                revenue = DataNormalizer._estimate_revenue_from_range(revenue_range)
            
            return {
                "company_name": apollo_org.get("name", ""),
                "domain": domain,
                "revenue": revenue,
                "employee_count": apollo_org.get("estimated_num_employees"),
                "industry": apollo_org.get("industry") or apollo_org.get("primary_industry"),
                "location": apollo_org.get("city"),
                "country": apollo_org.get("country"),
                "description": apollo_org.get("short_description", ""),
                "linkedin_url": apollo_org.get("linkedin_url"),
                "phone": apollo_org.get("phone"),
                "founded_year": apollo_org.get("founded_year"),
                "source": "Apollo",
                "raw_data": apollo_org
            }
        except Exception as e:
            logger.error(f"Failed to normalize Apollo organization: {str(e)}")
            return {}
    
    @staticmethod
    def normalize_apollo_person(apollo_person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Apollo person (contact) data
        
        Args:
            apollo_person: Raw person data from Apollo
        
        Returns:
            Normalized contact dict
        """
        try:
            # Get email
            email = apollo_person.get("email")
            if not email and "email_guesses" in apollo_person:
                email = apollo_person["email_guesses"][0] if apollo_person["email_guesses"] else None
            
            return {
                "name": f"{apollo_person.get('first_name', '')} {apollo_person.get('last_name', '')}".strip(),
                "first_name": apollo_person.get("first_name"),
                "last_name": apollo_person.get("last_name"),
                "title": apollo_person.get("title"),
                "email": email,
                "linkedin_url": apollo_person.get("linkedin_url"),
                "phone": apollo_person.get("phone_numbers", [{}])[0].get("raw_number") if apollo_person.get("phone_numbers") else None,
                "seniority": apollo_person.get("seniority"),
                "departments": apollo_person.get("departments", []),
                "source": "Apollo",
                "raw_data": apollo_person
            }
        except Exception as e:
            logger.error(f"Failed to normalize Apollo person: {str(e)}")
            return {}
    
    @staticmethod
    def normalize_crunchbase_organization(cb_org: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Crunchbase organization data
        
        Args:
            cb_org: Raw organization data from Crunchbase
        
        Returns:
            Normalized company dict
        """
        try:
            # Extract domain
            domain = cb_org.get("website", {}).get("value", "")
            if domain:
                domain = DataNormalizer._clean_domain(domain)
            
            # Get categories (industries)
            categories = cb_org.get("categories", [])
            industry = categories[0].get("value") if categories else None
            
            # Get location
            locations = cb_org.get("location_identifiers", [])
            location = locations[0].get("value") if locations else None
            
            # Parse revenue range
            revenue_range = cb_org.get("revenue_range", {}).get("value")
            revenue = DataNormalizer._parse_crunchbase_revenue(revenue_range)
            
            # Parse employee count
            employee_range = cb_org.get("num_employees_enum", {}).get("value")
            employee_count = DataNormalizer._parse_crunchbase_employees(employee_range)
            
            # Funding info
            funding_total = cb_org.get("funding_total", {})
            funding_amount = funding_total.get("value_usd") if isinstance(funding_total, dict) else None
            
            return {
                "company_name": cb_org.get("name", {}).get("value", ""),
                "domain": domain,
                "revenue": revenue,
                "employee_count": employee_count,
                "industry": industry,
                "location": location,
                "description": cb_org.get("short_description", {}).get("value", ""),
                "funding_stage": cb_org.get("last_funding_type", {}).get("value"),
                "funding_total": funding_amount,
                "founded_year": cb_org.get("founded_on", {}).get("value", "").split("-")[0] if cb_org.get("founded_on") else None,
                "ipo_status": cb_org.get("ipo_status", {}).get("value"),
                "source": "Crunchbase",
                "raw_data": cb_org
            }
        except Exception as e:
            logger.error(f"Failed to normalize Crunchbase organization: {str(e)}")
            return {}
    
    @staticmethod
    def _clean_domain(url: str) -> str:
        """Extract clean domain from URL"""
        try:
            extracted = tldextract.extract(url)
            return f"{extracted.domain}.{extracted.suffix}"
        except Exception:
            return url.replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0]
    
    @staticmethod
    def _estimate_revenue_from_range(employee_count: int) -> int:
        """Estimate revenue based on employee count (rough heuristic)"""
        # Average revenue per employee: $200K for tech companies
        if isinstance(employee_count, int):
            return employee_count * 200000
        return None
    
    @staticmethod
    def _parse_crunchbase_revenue(revenue_range: Optional[str]) -> Optional[int]:
        """Parse Crunchbase revenue range to midpoint value"""
        if not revenue_range:
            return None
        
        revenue_map = {
            "r_00000000": 0,
            "r_00001000": 500000,
            "r_00010000": 5000000,
            "r_00100000": 50000000,
            "r_01000000": 500000000,
            "r_10000000": 5000000000,
        }
        
        return revenue_map.get(revenue_range)
    
    @staticmethod
    def _parse_crunchbase_employees(employee_range: Optional[str]) -> Optional[int]:
        """Parse Crunchbase employee range to midpoint value"""
        if not employee_range:
            return None
        
        employee_map = {
            "c_00001_00010": 5,
            "c_00011_00050": 30,
            "c_00051_00100": 75,
            "c_00101_00250": 175,
            "c_00251_00500": 375,
            "c_00501_01000": 750,
            "c_01001_05000": 3000,
            "c_05001_10000": 7500,
            "c_10001_max": 15000,
        }
        
        return employee_map.get(employee_range)
    
    @staticmethod
    def merge_company_data(
        companies: List[Dict[str, Any]],
        primary_key: str = "domain"
    ) -> List[Dict[str, Any]]:
        """
        Merge company data from multiple sources
        
        Args:
            companies: List of company dicts from different sources
            primary_key: Key to use for matching (domain or company_name)
        
        Returns:
            List of merged company dicts
        """
        merged = {}
        
        for company in companies:
            key_value = company.get(primary_key, "").lower().strip()
            if not key_value:
                continue
            
            if key_value not in merged:
                merged[key_value] = company.copy()
                merged[key_value]["sources"] = [company.get("source")]
            else:
                # Merge data, preferring non-None values
                existing = merged[key_value]
                sources = existing.get("sources", [])
                sources.append(company.get("source"))
                
                for key, value in company.items():
                    if key in ["source", "raw_data"]:
                        continue
                    
                    if value is not None and (existing.get(key) is None or value != ""):
                        existing[key] = value
                
                existing["sources"] = list(set(sources))  # Deduplicate sources
        
        return list(merged.values())
