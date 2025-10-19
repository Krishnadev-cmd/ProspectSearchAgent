"""
Main ProspectSearchAgent orchestrator
"""
import os
import json
import yaml
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .apollo_client import ApolloClient
from .crunchbase_client import CrunchbaseClient
from .serpapi_client import SerpAPIClient
from .data_normalizer import DataNormalizer
from .scoring import ProspectScorer, Deduplicator
from .mock_data import MockDataGenerator

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProspectSearchAgent:
    """
    Autonomous B2B Prospect Finder Agent
    
    Discovers companies and contacts matching an Ideal Customer Profile (ICP)
    using multiple data sources (Apollo, Crunchbase, SerpAPI)
    """
    
    def __init__(
        self,
        apollo_api_key: Optional[str] = None,
        crunchbase_api_key: Optional[str] = None,
        serp_api_key: Optional[str] = None
    ):
        """
        Initialize ProspectSearchAgent with API clients
        
        Args:
            apollo_api_key: Apollo.io API key (or from .env)
            crunchbase_api_key: Crunchbase API key (or from .env)
            serp_api_key: SerpAPI key (or from .env)
        """
        # Initialize API clients
        self.apollo = None
        self.crunchbase = None
        self.serpapi = None
        
        # Apollo client
        apollo_key = apollo_api_key or os.getenv("APOLLO_API_KEY")
        if apollo_key and apollo_key != "your_apollo_api_key_here":
            self.apollo = ApolloClient(apollo_key)
            logger.info("Apollo client initialized")
        else:
            logger.warning("Apollo API key not provided")
        
        # Crunchbase client
        cb_key = crunchbase_api_key or os.getenv("CRUNCHBASE_API_KEY")
        if cb_key and cb_key != "your_crunchbase_api_key_here":
            self.crunchbase = CrunchbaseClient(cb_key)
            logger.info("Crunchbase client initialized")
        else:
            logger.warning("Crunchbase API key not provided")
        
        # SerpAPI client
        serp_key = serp_api_key or os.getenv("SERP_API_KEY")
        if serp_key and serp_key != "your_serpapi_key_here":
            self.serpapi = SerpAPIClient(serp_key)
            logger.info("SerpAPI client initialized")
        else:
            logger.warning("SerpAPI key not provided")
        
        self.normalizer = DataNormalizer()
        self.icp_config = None
        self.scorer = None
    
    def load_icp(self, config_path: str) -> Dict[str, Any]:
        """
        Load ICP configuration from YAML or JSON file
        
        Args:
            config_path: Path to ICP config file
        
        Returns:
            ICP configuration dict
        """
        logger.info(f"Loading ICP from {config_path}")
        
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                self.icp_config = yaml.safe_load(f)
            elif config_path.endswith('.json'):
                self.icp_config = json.load(f)
            else:
                raise ValueError("Config file must be YAML or JSON")
        
        # Initialize scorer with ICP config
        self.scorer = ProspectScorer(self.icp_config)
        
        logger.info(f"ICP loaded: {self.icp_config.get('icp', {})}")
        return self.icp_config
    
    def search_prospects(self, icp_config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Main method to search for prospects matching ICP
        
        Args:
            icp_config: ICP configuration dict (optional if already loaded)
        
        Returns:
            List of enriched prospect dicts with companies and contacts
        """
        if icp_config:
            self.icp_config = icp_config
            self.scorer = ProspectScorer(icp_config)
        
        if not self.icp_config:
            raise ValueError("ICP configuration not loaded. Call load_icp() first.")
        
        logger.info("Starting prospect search...")
        
        # Step 1: Fetch companies from multiple sources
        all_companies = []
        
        if self.apollo:
            logger.info("Fetching companies from Apollo...")
            apollo_companies = self._fetch_apollo_companies()
            all_companies.extend(apollo_companies)
        
        if self.crunchbase:
            logger.info("Fetching companies from Crunchbase...")
            cb_companies = self._fetch_crunchbase_companies()
            all_companies.extend(cb_companies)
        
        logger.info(f"Fetched {len(all_companies)} companies from all sources")
        
        # Step 2: Merge and deduplicate companies
        merged_companies = self.normalizer.merge_company_data(all_companies, primary_key="domain")
        unique_companies = Deduplicator.deduplicate_companies(merged_companies)
        
        logger.info(f"After merging and deduplication: {len(unique_companies)} unique companies")
        
        # Step 3: Enrich with signals (funding, hiring, tech stack)
        enriched_prospects = []
        
        for company in unique_companies:
            logger.info(f"Processing company: {company.get('company_name')}")
            
            # Fetch signals
            signals = self._fetch_signals(company)
            
            # Fetch contacts if requested
            contacts = []
            if self.icp_config.get("search_params", {}).get("include_contacts", True):
                contacts = self._fetch_contacts(company)
            
            # Calculate confidence score
            confidence = self.scorer.calculate_score(company, contacts, signals)
            
            # Filter by minimum confidence
            min_confidence = self.icp_config.get("search_params", {}).get("min_confidence_score", 0.7)
            if confidence < min_confidence:
                logger.info(f"Skipping {company.get('company_name')} - confidence {confidence} below threshold {min_confidence}")
                continue
            
            # Build prospect object
            prospect = {
                "company_name": company.get("company_name"),
                "domain": company.get("domain"),
                "revenue": company.get("revenue"),
                "employee_count": company.get("employee_count"),
                "industry": company.get("industry"),
                "location": company.get("location"),
                "description": company.get("description"),
                "funding_stage": company.get("funding_stage"),
                "funding_total": company.get("funding_total"),
                "contacts": contacts,
                "signals": signals,
                "source": company.get("sources", []),
                "confidence": confidence
            }
            
            enriched_prospects.append(prospect)
        
        # Sort by confidence score
        enriched_prospects.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Limit results
        max_results = self.icp_config.get("search_params", {}).get("max_results", 50)
        enriched_prospects = enriched_prospects[:max_results]
        
        logger.info(f"Search complete: {len(enriched_prospects)} prospects found")
        return enriched_prospects
    
    def _fetch_apollo_companies(self) -> List[Dict[str, Any]]:
        """Fetch companies from Apollo or use mock data for demo"""
        if not self.apollo:
            logger.info("Apollo client not available, using mock data for demo")
            return self._fetch_mock_companies()
        
        icp = self.icp_config.get("icp", {})
        
        try:
            response = self.apollo.search_organizations(
                industries=icp.get("industry"),
                revenue_range=(icp.get("revenue_min"), icp.get("revenue_max")),
                employee_count_range=(icp.get("employee_count_min"), icp.get("employee_count_max")),
                location=icp.get("geography"),
                keywords=icp.get("keywords"),
                per_page=25
            )
            
            organizations = response.get("organizations", [])
            
            # If Apollo returns no results (free tier limitation), use mock data
            if not organizations:
                logger.warning("Apollo returned no results (free tier limitation). Using mock data for demo.")
                return self._fetch_mock_companies()
            
            return [
                self.normalizer.normalize_apollo_organization(org)
                for org in organizations
            ]
        except Exception as e:
            logger.error(f"Failed to fetch from Apollo: {str(e)}")
            logger.info("Using mock data as fallback")
            return self._fetch_mock_companies()
    
    def _fetch_crunchbase_companies(self) -> List[Dict[str, Any]]:
        """Fetch companies from Crunchbase"""
        if not self.crunchbase:
            return []
        
        icp = self.icp_config.get("icp", {})
        
        try:
            organizations = self.crunchbase.search_organizations(
                categories=icp.get("industry"),
                locations=icp.get("geography"),
                limit=25
            )
            
            return [
                self.normalizer.normalize_crunchbase_organization(org)
                for org in organizations
            ]
        except Exception as e:
            logger.error(f"Failed to fetch from Crunchbase: {str(e)}")
            return []
    
    def _fetch_signals(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch signals (funding, hiring, tech stack) for a company
        
        Args:
            company: Company data dict
        
        Returns:
            Signals dict
        """
        signals = {
            "new_funding": False,
            "recent_hiring": False,
            "data_roles_count": 0,
            "tech_stack": []
        }
        
        company_name = company.get("company_name")
        
        # Check if company already has funding info from Crunchbase
        if company.get("funding_stage"):
            signals["new_funding"] = True
            signals["funding_stage"] = company.get("funding_stage")
        
        # Fetch hiring signals from SerpAPI
        if self.serpapi and company_name:
            try:
                job_titles = self.icp_config.get("signals", {}).get("job_titles_to_search", [])
                job_data = self.serpapi.search_jobs(
                    company_name=company_name,
                    job_titles=job_titles
                )
                
                signals["recent_hiring"] = job_data.get("hiring_signal", False)
                signals["data_roles_count"] = job_data.get("data_roles_count", 0)
            except Exception as e:
                logger.error(f"Failed to fetch hiring signals for {company_name}: {str(e)}")
        
        return signals
    
    def _fetch_contacts(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch contacts for a company
        
        Args:
            company: Company data dict
        
        Returns:
            List of contact dicts
        """
        if not self.apollo:
            # Use mock contacts for demo
            domain = company.get("domain", "example.com")
            max_contacts = self.icp_config.get("search_params", {}).get("max_contacts_per_company", 3)
            mock_contacts = MockDataGenerator.generate_contacts(domain, count=max_contacts)
            
            return [
                self.normalizer.normalize_apollo_person(contact)
                for contact in mock_contacts
            ]
        
        contacts = []
        
        try:
            # Search for people at this company
            job_titles = self.icp_config.get("signals", {}).get("job_titles_to_search", [])
            
            response = self.apollo.search_people(
                titles=job_titles,
                per_page=self.icp_config.get("search_params", {}).get("max_contacts_per_company", 5)
            )
            
            people = response.get("people", [])
            
            # If no results, use mock data
            if not people:
                logger.info(f"No contacts found via Apollo for {company.get('company_name')}, using mock data")
                domain = company.get("domain", "example.com")
                max_contacts = self.icp_config.get("search_params", {}).get("max_contacts_per_company", 3)
                mock_contacts = MockDataGenerator.generate_contacts(domain, count=max_contacts)
                people = mock_contacts
            
            for person in people:
                contact = self.normalizer.normalize_apollo_person(person)
                if contact.get("email"):  # Only include contacts with email
                    contacts.append(contact)
            
            # Deduplicate contacts
            contacts = Deduplicator.deduplicate_contacts(contacts)
            
        except Exception as e:
            logger.error(f"Failed to fetch contacts for {company.get('company_name')}: {str(e)}")
            # Fallback to mock data
            domain = company.get("domain", "example.com")
            max_contacts = self.icp_config.get("search_params", {}).get("max_contacts_per_company", 3)
            mock_contacts = MockDataGenerator.generate_contacts(domain, count=max_contacts)
            contacts = [
                self.normalizer.normalize_apollo_person(contact)
                for contact in mock_contacts
            ]
        
        return contacts
    
    def save_results(self, prospects: List[Dict[str, Any]], output_path: str):
        """
        Save prospect results to JSON file
        
        Args:
            prospects: List of prospect dicts
            output_path: Path to output file
        """
        logger.info(f"Saving {len(prospects)} prospects to {output_path}")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(prospects, f, indent=2, default=str)
        
        logger.info(f"Results saved to {output_path}")
    
    def _fetch_mock_companies(self) -> List[Dict[str, Any]]:
        """Generate mock company data for demo purposes"""
        logger.info("Generating mock company data for demo")
        
        # Generate mock companies
        mock_companies = MockDataGenerator.generate_companies(count=10, icp_filter=self.icp_config)
        
        # Normalize to same format as Apollo
        normalized = []
        for company in mock_companies:
            normalized_company = self.normalizer.normalize_apollo_organization(company)
            # Add mock funding data
            funding = MockDataGenerator.generate_funding_data(company["name"])
            normalized_company["funding_stage"] = funding["last_funding_type"]
            normalized_company["funding_total"] = funding["funding_total"]
            normalized.append(normalized_company)
        
        return normalized
    
    def close(self):
        """Close all API clients"""
        if self.apollo:
            self.apollo.close()
        if self.crunchbase:
            self.crunchbase.close()
        if self.serpapi:
            self.serpapi.close()
