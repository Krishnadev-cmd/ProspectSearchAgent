"""
ProspectSearchAgent - AI-powered B2B Prospect Finder
"""
from .agent import ProspectSearchAgent
from .apollo_client import ApolloClient
from .crunchbase_client import CrunchbaseClient
from .serpapi_client import SerpAPIClient
from .data_normalizer import DataNormalizer
from .scoring import ProspectScorer, Deduplicator

__version__ = "1.0.0"
__all__ = [
    "ProspectSearchAgent",
    "ApolloClient",
    "CrunchbaseClient",
    "SerpAPIClient",
    "DataNormalizer",
    "ProspectScorer",
    "Deduplicator"
]
