"""
Scoring and deduplication logic for prospect data
"""
import logging
from typing import List, Dict, Any, Set
from difflib import SequenceMatcher
import re

logger = logging.getLogger(__name__)


class ProspectScorer:
    """Calculate confidence scores for prospects based on ICP match"""
    
    def __init__(self, icp_config: Dict[str, Any]):
        """
        Initialize scorer with ICP configuration
        
        Args:
            icp_config: ICP configuration dict
        """
        self.icp = icp_config.get("icp", {})
        self.signals = icp_config.get("signals", {})
        self.icp_industries = [i.lower() for i in self.icp.get("industry", [])]
        self.icp_keywords = [k.lower() for k in self.icp.get("keywords", [])]
        self.icp_tech_stack = [t.lower() for t in self.signals.get("tech_stack", [])]
    
    def calculate_score(
        self,
        company: Dict[str, Any],
        contacts: List[Dict[str, Any]] = None,
        signals: Dict[str, Any] = None
    ) -> float:
        """
        Calculate confidence score for a company
        
        Score breakdown:
        - Industry match: 0.3
        - Revenue/size match: 0.2
        - Keyword match: 0.15
        - Funding signal: 0.15
        - Hiring signal: 0.1
        - Tech stack: 0.1
        
        Args:
            company: Company data dict
            contacts: List of contact dicts
            signals: Signals dict (funding, hiring, etc.)
        
        Returns:
            Confidence score between 0 and 1
        """
        score = 0.0
        
        # Industry match (30%)
        score += self._score_industry(company) * 0.3
        
        # Revenue and size match (20%)
        score += self._score_revenue_size(company) * 0.2
        
        # Keyword match (15%)
        score += self._score_keywords(company) * 0.15
        
        # Signals (35% total)
        if signals:
            score += self._score_funding(signals) * 0.15
            score += self._score_hiring(signals) * 0.1
            score += self._score_tech_stack(signals) * 0.1
        
        return round(min(score, 1.0), 2)
    
    def _score_industry(self, company: Dict[str, Any]) -> float:
        """Score industry match"""
        company_industry = (company.get("industry") or "").lower()
        
        if not company_industry or not self.icp_industries:
            return 0.5  # Neutral score if no data
        
        # Check for exact or partial match
        for icp_industry in self.icp_industries:
            if icp_industry in company_industry or company_industry in icp_industry:
                return 1.0
            
            # Fuzzy match
            similarity = SequenceMatcher(None, icp_industry, company_industry).ratio()
            if similarity > 0.6:
                return similarity
        
        return 0.0
    
    def _score_revenue_size(self, company: Dict[str, Any]) -> float:
        """Score revenue and employee count match"""
        score = 0.0
        count = 0
        
        # Revenue check
        revenue = company.get("revenue")
        if revenue and isinstance(revenue, (int, float)):
            rev_min = self.icp.get("revenue_min", 0)
            rev_max = self.icp.get("revenue_max", float("inf"))
            
            if rev_min <= revenue <= rev_max:
                score += 1.0
            elif revenue < rev_min:
                # Partial score if close
                score += max(0, 1.0 - (rev_min - revenue) / rev_min)
            else:
                score += max(0, 1.0 - (revenue - rev_max) / rev_max)
            count += 1
        
        # Employee count check
        employee_count = company.get("employee_count")
        if employee_count and isinstance(employee_count, (int, float)):
            emp_min = self.icp.get("employee_count_min", 0)
            emp_max = self.icp.get("employee_count_max", float("inf"))
            
            if emp_min <= employee_count <= emp_max:
                score += 1.0
            elif employee_count < emp_min:
                score += max(0, 1.0 - (emp_min - employee_count) / emp_min)
            else:
                score += max(0, 1.0 - (employee_count - emp_max) / emp_max)
            count += 1
        
        return score / count if count > 0 else 0.5
    
    def _score_keywords(self, company: Dict[str, Any]) -> float:
        """Score keyword match in company description"""
        description = (company.get("description") or "").lower()
        company_name = (company.get("company_name") or "").lower()
        
        if not description and not company_name:
            return 0.5
        
        text = f"{description} {company_name}"
        
        if not self.icp_keywords:
            return 0.5
        
        matches = sum(1 for keyword in self.icp_keywords if keyword in text)
        return matches / len(self.icp_keywords)
    
    def _score_funding(self, signals: Dict[str, Any]) -> float:
        """Score funding signals"""
        if not self.signals.get("funding"):
            return 0.5  # Neutral if not required
        
        has_funding = signals.get("new_funding", False)
        funding_stage = signals.get("funding_stage")
        
        if has_funding or funding_stage:
            return 1.0
        return 0.0
    
    def _score_hiring(self, signals: Dict[str, Any]) -> float:
        """Score hiring signals"""
        if not self.signals.get("hiring_data_roles"):
            return 0.5
        
        recent_hiring = signals.get("recent_hiring", False)
        data_roles_count = signals.get("data_roles_count", 0)
        
        if data_roles_count > 0:
            return min(1.0, data_roles_count / 3)  # Max score at 3+ roles
        elif recent_hiring:
            return 0.5
        return 0.0
    
    def _score_tech_stack(self, signals: Dict[str, Any]) -> float:
        """Score tech stack match"""
        if not self.icp_tech_stack:
            return 0.5
        
        company_tech = [t.lower() for t in signals.get("tech_stack", [])]
        
        if not company_tech:
            return 0.5
        
        matches = sum(1 for tech in self.icp_tech_stack if tech in company_tech)
        return matches / len(self.icp_tech_stack)


class Deduplicator:
    """Remove duplicate companies and contacts"""
    
    @staticmethod
    def deduplicate_companies(
        companies: List[Dict[str, Any]],
        threshold: float = 0.85
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate companies based on domain and name similarity
        
        Args:
            companies: List of company dicts
            threshold: Similarity threshold for fuzzy matching
        
        Returns:
            Deduplicated list of companies
        """
        if not companies:
            return []
        
        unique_companies = []
        seen_domains: Set[str] = set()
        seen_names: List[str] = []
        
        for company in companies:
            domain = (company.get("domain") or "").lower().strip()
            name = (company.get("company_name") or "").lower().strip()
            
            # Check domain
            if domain and domain in seen_domains:
                continue
            
            # Check name similarity
            is_duplicate = False
            if name:
                for seen_name in seen_names:
                    similarity = SequenceMatcher(None, name, seen_name).ratio()
                    if similarity >= threshold:
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                unique_companies.append(company)
                if domain:
                    seen_domains.add(domain)
                if name:
                    seen_names.append(name)
        
        logger.info(f"Deduplicated {len(companies)} companies to {len(unique_companies)}")
        return unique_companies
    
    @staticmethod
    def deduplicate_contacts(
        contacts: List[Dict[str, Any]],
        threshold: float = 0.9
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate contacts based on email and name
        
        Args:
            contacts: List of contact dicts
            threshold: Similarity threshold for name matching
        
        Returns:
            Deduplicated list of contacts
        """
        if not contacts:
            return []
        
        unique_contacts = []
        seen_emails: Set[str] = set()
        seen_combinations: Set[str] = set()
        
        for contact in contacts:
            email = (contact.get("email") or "").lower().strip()
            name = (contact.get("name") or "").lower().strip()
            
            # Email is unique identifier
            if email and email in seen_emails:
                continue
            
            # Check name + company combination for contacts without email
            if not email and name:
                combination = name
                if combination in seen_combinations:
                    continue
                seen_combinations.add(combination)
            
            unique_contacts.append(contact)
            if email:
                seen_emails.add(email)
        
        logger.info(f"Deduplicated {len(contacts)} contacts to {len(unique_contacts)}")
        return unique_contacts
    
    @staticmethod
    def normalize_email(email: str) -> str:
        """Normalize email address"""
        if not email:
            return ""
        
        email = email.lower().strip()
        # Remove +tags from gmail addresses
        if "@gmail.com" in email:
            local, domain = email.split("@")
            local = local.split("+")[0]
            email = f"{local}@{domain}"
        
        return email
