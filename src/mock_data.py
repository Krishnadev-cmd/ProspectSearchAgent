"""
Mock data generator for demo purposes when APIs are unavailable or limited
"""
import random
from typing import List, Dict, Any


class MockDataGenerator:
    """Generate realistic mock prospect data for demo"""
    
    COMPANIES = [
        {"name": "DataMetrics Pro", "domain": "datametrics.io", "industry": "B2B Software"},
        {"name": "CloudAnalytics Inc", "domain": "cloudanalytics.com", "industry": "Enterprise Software"},
        {"name": "FinTech Insights", "domain": "fintechinsights.com", "industry": "FinTech"},
        {"name": "AI Solutions Group", "domain": "aisolutions.io", "industry": "B2B Software"},
        {"name": "DataDriven Technologies", "domain": "datadriven.com", "industry": "Enterprise Software"},
        {"name": "SmartAutomation Labs", "domain": "smartautomation.io", "industry": "B2B Software"},
        {"name": "AnalytiX Financial", "domain": "analytixfinancial.com", "industry": "FinTech"},
        {"name": "CloudMetrics Solutions", "domain": "cloudmetrics.com", "industry": "Enterprise Software"},
        {"name": "AI Analytics Corp", "domain": "aianalytics.io", "industry": "B2B Software"},
        {"name": "DataFlow Systems", "domain": "dataflow.com", "industry": "Enterprise Software"},
    ]
    
    CONTACTS = [
        {"first": "Sarah", "last": "Johnson", "title": "VP Data Science"},
        {"first": "Michael", "last": "Chen", "title": "Chief Data Officer"},
        {"first": "Emily", "last": "Rodriguez", "title": "Head of Analytics"},
        {"first": "David", "last": "Kim", "title": "Director of Engineering"},
        {"first": "Jennifer", "last": "Martinez", "title": "VP Engineering"},
        {"first": "Robert", "last": "Wilson", "title": "CTO"},
        {"first": "Lisa", "last": "Anderson", "title": "Head of Data Science"},
        {"first": "James", "last": "Taylor", "title": "VP Product"},
    ]
    
    CITIES = ["San Francisco", "New York", "Austin", "Seattle", "Boston", "Chicago"]
    
    @staticmethod
    def generate_companies(count: int = 10, icp_filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate mock company data matching ICP"""
        companies = []
        
        for i in range(min(count, len(MockDataGenerator.COMPANIES))):
            company_template = MockDataGenerator.COMPANIES[i]
            
            # Generate realistic data
            employee_count = random.randint(100, 2000)
            revenue = employee_count * random.randint(150000, 300000)
            
            company = {
                "name": company_template["name"],
                "domain": company_template["domain"],
                "website_url": f"https://{company_template['domain']}",
                "industry": company_template["industry"],
                "primary_industry": company_template["industry"],
                "estimated_num_employees": employee_count,
                "city": random.choice(MockDataGenerator.CITIES),
                "country": "USA",
                "short_description": f"Leading {company_template['industry']} company specializing in AI and data analytics solutions",
                "founded_year": random.randint(2010, 2020),
                "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "id": f"mock_{i}"
            }
            
            companies.append(company)
        
        return companies
    
    @staticmethod
    def generate_contacts(company_domain: str, count: int = 3) -> List[Dict[str, Any]]:
        """Generate mock contact data for a company"""
        contacts = []
        
        for i in range(min(count, len(MockDataGenerator.CONTACTS))):
            contact_template = MockDataGenerator.CONTACTS[i]
            
            contact = {
                "first_name": contact_template["first"],
                "last_name": contact_template["last"],
                "title": contact_template["title"],
                "email": f"{contact_template['first'].lower()}.{contact_template['last'].lower()}@{company_domain}",
                "linkedin_url": f"linkedin.com/in/{contact_template['first'].lower()}{contact_template['last'].lower()}",
                "seniority": "VP" if "VP" in contact_template["title"] else "Director",
                "departments": ["Data Science", "Engineering"] if "Data" in contact_template["title"] else ["Engineering"],
                "id": f"mock_contact_{i}"
            }
            
            contacts.append(contact)
        
        return contacts
    
    @staticmethod
    def generate_funding_data(company_name: str) -> Dict[str, Any]:
        """Generate mock funding data"""
        stages = ["Seed", "Series A", "Series B", "Series C"]
        stage = random.choice(stages)
        
        funding_map = {
            "Seed": random.randint(1000000, 5000000),
            "Series A": random.randint(5000000, 20000000),
            "Series B": random.randint(20000000, 50000000),
            "Series C": random.randint(50000000, 150000000),
        }
        
        return {
            "last_funding_type": stage,
            "funding_total": funding_map[stage],
            "last_funding_at": "2024-06-15",
            "has_funding": True
        }
    
    @staticmethod
    def generate_hiring_signals() -> Dict[str, Any]:
        """Generate mock hiring signals"""
        data_roles = random.randint(0, 5)
        
        return {
            "jobs_found": random.randint(5, 20),
            "data_roles_count": data_roles,
            "recent_postings": [
                {"title": "Senior Data Scientist", "is_data_role": True},
                {"title": "ML Engineer", "is_data_role": True},
                {"title": "Software Engineer", "is_data_role": False},
            ],
            "hiring_signal": data_roles > 0
        }
