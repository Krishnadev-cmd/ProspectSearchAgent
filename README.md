# ProspectSearchAgent 🎯# ProspectSearchAgent - AI-powered B2B Prospect Finder 🎯



An AI-powered B2B prospect finder that aggregates data from multiple sources (Apollo.io, Crunchbase, SerpAPI) to identify high-quality leads matching your Ideal Customer Profile (ICP).An autonomous AI agent that discovers B2B companies and contacts matching your Ideal Customer Profile (ICP) using multiple data sources.



![Python](https://img.shields.io/badge/python-3.10+-blue.svg)[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

## 🌟 Features

- **Multi-Source Data Aggregation**: Queries Apollo.io, Crunchbase, and SerpAPI

### Web Interface (Streamlit)- **Intelligent Matching**: Scores prospects based on ICP fit (revenue, industry, size, keywords)

- **Interactive ICP Configuration**: Define your ideal customer profile through an intuitive sidebar- **Signal Detection**: Identifies funding rounds, hiring activity, and tech stack

- **Real-time Search**: Find prospects instantly with live search results- **Smart Deduplication**: Merges data from multiple sources and removes duplicates

- **Confidence Scoring**: See AI-calculated confidence scores (0-100%) for each prospect- **Contact Enrichment**: Finds decision-makers with verified emails

- **Smart Filtering**: Filter by minimum confidence, revenue range, employee count- **Confidence Scoring**: Ranks prospects by ICP match quality (0-1 scale)

- **Contact Details**: View emails, phone numbers, LinkedIn profiles, and job titles

- **Data Export**: Download results as CSV or JSON with one click## 📋 Table of Contents

- **Session Management**: Persist search results during your session

- [Architecture](#architecture)

### Backend Engine- [Installation](#installation)

- **Multi-source Data Aggregation**: Combines Apollo, Crunchbase, and Google search data- [API Setup](#api-setup)

- **Data Normalization**: Unifies different API schemas into a consistent format- [Usage](#usage)

- **Intelligent Deduplication**: Removes duplicates by domain and email- [ICP Configuration](#icp-configuration)

- **6-Factor Confidence Scoring**:- [Output Format](#output-format)

  - Industry match- [Development](#development)

  - Company size match- [Troubleshooting](#troubleshooting)

  - Revenue match

  - Technology stack match## 🏗️ Architecture

  - Funding signals

  - Hiring signals```

- **Mock Data Fallback**: Works with realistic demo data when APIs are unavailable┌─────────────────────────────────────────────────────────────┐

│                    ProspectSearchAgent                       │

## 🚀 Quick Start│                                                               │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │

### Prerequisites│  │   Apollo.io  │  │  Crunchbase  │  │   SerpAPI    │      │

- Python 3.10 or higher│  │   Client     │  │   Client     │  │   Client     │      │

- pip (Python package manager)│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │

- API Keys (optional for demo mode):│         │                  │                  │               │

  - Apollo.io API key│         └──────────────────┼──────────────────┘              │

  - Crunchbase API key│                            │                                  │

  - SerpAPI key│                    ┌───────▼────────┐                        │

│                    │ Data Normalizer│                        │

### Installation│                    └───────┬────────┘                        │

│                            │                                  │

1. **Clone the repository**│                    ┌───────▼────────┐                        │

```bash│                    │  Deduplicator  │                        │

git clone https://github.com/yourusername/ProspectSearchAgent.git│                    └───────┬────────┘                        │

cd ProspectSearchAgent│                            │                                  │

```│                    ┌───────▼────────┐                        │

│                    │Confidence Score│                        │

2. **Create a virtual environment**│                    └───────┬────────┘                        │

```bash│                            │                                  │

python -m venv venv│                    ┌───────▼────────┐                        │

# Windows│                    │  JSON Output   │                        │

venv\Scripts\activate│                    └────────────────┘                        │

# Mac/Linux└─────────────────────────────────────────────────────────────┘

source venv/bin/activate```

```

## 🚀 Installation

3. **Install dependencies**

```bash### Prerequisites

pip install -r requirements.txt

```- Python 3.10 or higher

- pip package manager

4. **Set up API keys** (optional)- API keys (see [API Setup](#api-setup))

Create a `.env` file in the project root:

```env### Quick Start

APOLLO_API_KEY=your_apollo_key_here

CRUNCHBASE_API_KEY=your_crunchbase_key_here```bash

SERPAPI_KEY=your_serpapi_key_here# Clone the repository

```cd agent_3



**Note**: The app works in demo mode with realistic mock data if API keys are not provided.# Create virtual environment

python -m venv venv

### Running the Application

# Activate virtual environment

#### Web Interface (Recommended)# Windows:

```bashvenv\Scripts\activate

streamlit run app.py# macOS/Linux:

```source venv/bin/activate



The web app will open in your browser at `http://localhost:8501`# Install dependencies

pip install -r requirements.txt

#### Command Line Interface

```bash# Copy environment template

python run_agent.pycopy .env.example .env

```

# Edit .env with your API keys

Results will be saved to `output/prospects.json`notepad .env

```

## 📖 Usage Guide

## 🔑 API Setup

### Using the Web Interface

### 1. Apollo.io (Free Tier: 100 credits)

1. **Configure Your ICP** (Ideal Customer Profile):

   - Set minimum/maximum revenue range1. Sign up at [Apollo.io](https://www.apollo.io/)

   - Define employee count range2. Navigate to Settings → Integrations → API

   - Select target industries3. Generate API key

   - Add relevant keywords (technologies, signals)4. Add to `.env`: `APOLLO_API_KEY=your_key_here`



2. **Run Search**:**API Documentation**: https://apolloio.github.io/apollo-api-docs/

   - Click "🔍 Search for Prospects"

   - Wait for results to load### 2. Crunchbase (Free Developer Account)

   - View prospects with confidence scores

1. Sign up at [Crunchbase](https://www.crunchbase.com/)

3. **Filter Results**:2. Request API access at [Crunchbase API](https://data.crunchbase.com/docs)

   - Adjust minimum confidence threshold3. Get your user key

   - Set revenue/employee filters4. Add to `.env`: `CRUNCHBASE_API_KEY=your_key_here`

   - Results update in real-time

**API Documentation**: https://data.crunchbase.com/docs

4. **Export Data**:

   - Click "Download CSV" for spreadsheet format### 3. SerpAPI (Free: 100 searches/month)

   - Click "Download JSON" for structured data

   - Includes all prospect and contact information1. Sign up at [SerpAPI](https://serpapi.com/)

2. Get API key from dashboard

### Using the CLI3. Add to `.env`: `SERP_API_KEY=your_key_here`



1. **Create an ICP configuration file** (YAML or JSON):**API Documentation**: https://serpapi.com/search-api

```yaml

# config/my_icp.yaml### Optional APIs

industry: "Healthcare Technology"

company_size_min: 50- **BuiltWith** (tech stack detection): https://builtwith.com/api

company_size_max: 500- **Hunter.io** (email verification): https://hunter.io/api

revenue_min: 5000000

revenue_max: 50000000## 💻 Usage

keywords:

  - "HIPAA compliant"### Basic Usage

  - "EHR integration"

  - "telemedicine"```python

```from src.agent import ProspectSearchAgent



2. **Run the agent**:# Initialize agent

```bashagent = ProspectSearchAgent()

python run_agent.py --icp config/my_icp.yaml --output output/healthcare_prospects.json

```# Load ICP configuration

agent.load_icp("config/icp_example.yaml")

3. **View results** in `output/healthcare_prospects.json`

# Run search

## 📊 Output Formatprospects = agent.search_prospects()



### Prospect Data Structure# Save results

```jsonagent.save_results(prospects, "output/prospects.json")

{

  "company_name": "HealthTech Solutions",# Clean up

  "domain": "healthtechsolutions.com",agent.close()

  "industry": "Healthcare Technology",```

  "employee_count": 250,

  "revenue": 25000000,### Command Line

  "location": "Boston, MA",

  "description": "Leading provider of EHR solutions",```bash

  "confidence_score": 0.85,# Run with default config

  "technologies": ["Python", "React", "AWS"],python run_agent.py

  "funding": {

    "total_funding": 15000000,# Test without API keys (uses mock data)

    "last_round": "Series B",python test_agent.py

    "investors": ["HealthTech Ventures"]```

  },

  "contacts": [### Advanced Usage

    {

      "name": "Jane Smith",```python

      "title": "VP of Engineering",from src.agent import ProspectSearchAgent

      "email": "jane.smith@healthtechsolutions.com",

      "linkedin": "https://linkedin.com/in/janesmith",# Initialize with custom API keys

      "phone": "+1-555-0123"agent = ProspectSearchAgent(

    }    apollo_api_key="your_key",

  ]    crunchbase_api_key="your_key",

}    serp_api_key="your_key"

```)



## 🏗️ Architecture# Load ICP from JSON

agent.load_icp("config/icp_healthcare.json")

```

ProspectSearchAgent/# Search with custom ICP

├── app.py                      # Streamlit web interfacecustom_icp = {

├── run_agent.py                # CLI entry point    "icp": {

├── src/        "revenue_min": 50000000,

│   ├── agent.py                # Main orchestration logic        "revenue_max": 500000000,

│   ├── apollo_client.py        # Apollo.io API integration        "industry": ["Healthcare Technology"],

│   ├── crunchbase_client.py    # Crunchbase API integration        "geography": ["USA"],

│   ├── serpapi_client.py       # SerpAPI integration        "employee_count_min": 200

│   ├── data_normalizer.py      # Schema unification    },

│   ├── scoring.py              # Confidence scoring & deduplication    "signals": {"funding": True},

│   └── mock_data.py            # Demo data generator    "search_params": {

├── config/        "max_results": 30,

│   ├── icp_example.yaml        # Sample ICP (YAML)        "min_confidence_score": 0.8

│   └── icp_healthcare.json     # Sample ICP (JSON)    }

├── output/                     # Search results}

└── requirements.txt

```prospects = agent.search_prospects(custom_icp)

```

### Data Flow

1. **Input**: ICP configuration (web form or YAML/JSON file)## 📝 ICP Configuration

2. **Data Collection**: Parallel API calls to Apollo, Crunchbase, SerpAPI

3. **Normalization**: Convert all data to unified schema### YAML Format

4. **Deduplication**: Remove duplicates by domain/email

5. **Scoring**: Calculate confidence scores (0-1 scale)```yaml

6. **Output**: Web display or JSON file with ranked prospectsicp:

  revenue_min: 20000000  # $20M

## 🔧 Configuration  revenue_max: 200000000  # $200M

  industry:

### ICP Parameters    - "B2B Software"

    - "FinTech"

| Parameter | Type | Description | Example |  geography:

|-----------|------|-------------|---------|    - "USA"

| `industry` | string | Target industry | "SaaS", "Healthcare" |  employee_count_min: 100

| `company_size_min` | integer | Minimum employees | 50 |  employee_count_max: 5000

| `company_size_max` | integer | Maximum employees | 500 |  keywords:

| `revenue_min` | integer | Minimum annual revenue ($) | 5000000 |    - "AI"

| `revenue_max` | integer | Maximum annual revenue ($) | 50000000 |    - "data analytics"

| `keywords` | list[string] | Technologies, signals | ["AI", "cloud", "hiring"] |    - "automation"

| `location` | string | Geographic focus | "United States" |

signals:

### Confidence Scoring Factors  funding: true  # Filter for funded companies

  hiring_data_roles: true  # Look for data role hiring

1. **Industry Match** (25%): Exact or related industry  tech_stack:

2. **Company Size** (20%): Within specified employee range    - "Snowflake"

3. **Revenue Range** (20%): Within specified revenue range    - "AWS"

4. **Technology Stack** (15%): Uses relevant technologies  job_titles_to_search:

5. **Funding Signals** (10%): Recent funding rounds    - "VP Data"

6. **Hiring Signals** (10%): Active hiring for key roles    - "Chief Data Officer"



## 🎬 Demo Modesearch_params:

  max_results: 50

The app includes a mock data generator that provides realistic demo data when API keys are not available or free tier limits are reached:  min_confidence_score: 0.7

  include_contacts: true

- **10 diverse companies**: SaaS, FinTech, HealthTech, E-commerce  max_contacts_per_company: 5

- **8 realistic contacts**: Executives, VPs, Directors with emails and LinkedIn```

- **Funding data**: Series A/B rounds with investor details

- **Technologies**: Modern stacks (Python, React, AWS, Kubernetes)### JSON Format

- **Hiring signals**: Engineering, sales, marketing roles

See `config/icp_healthcare.json` for JSON example.

Perfect for testing and demonstrations without API costs!

## 📤 Output Format

## 📝 API Notes

```json

### Apollo.io Free Tier Limitations[

- **100 credits/month**  {

- ⚠️ **Company/People search endpoints NOT available on free plan**    "company_name": "DataIQ Inc",

- The app automatically falls back to mock data when free tier is detected    "domain": "dataiq.com",

    "revenue": 75000000,

### Recommended API Plans    "employee_count": 150,

- **Apollo.io**: Basic plan ($49/mo) for company search access    "industry": "Software",

- **Crunchbase**: Basic plan ($29/mo) for 200 API calls/mo    "location": "San Francisco",

- **SerpAPI**: Free tier (100 searches/mo) is sufficient for light use    "description": "AI-powered data analytics platform",

    "funding_stage": "Series B",

## 🛠️ Troubleshooting    "funding_total": 25000000,

    "contacts": [

### "403 Forbidden" from Apollo API      {

- **Cause**: Free tier doesn't support `/mixed_companies/search`        "name": "Sarah Green",

- **Solution**: App automatically uses mock data. Upgrade to Basic plan for full access.        "title": "VP Data Science",

        "email": "sarah@dataiq.com",

### Streamlit not found        "linkedin_url": "linkedin.com/in/sarahgreen",

```bash        "phone": "+1-555-0123"

pip install streamlit>=1.28.0      }

```    ],

    "signals": {

### No prospects found      "new_funding": true,

- Check ICP criteria aren't too restrictive      "recent_hiring": true,

- Verify API keys in `.env` file      "data_roles_count": 3,

- Review logs for API errors      "tech_stack": ["AWS", "Snowflake", "Python"]

    },

### Import errors    "source": ["Apollo", "Crunchbase"],

```bash    "confidence": 0.92

pip install -r requirements.txt --upgrade  }

```]

```

## 📚 Documentation

## 🔍 Confidence Scoring

- **[SETUP.md](SETUP.md)**: Detailed installation and configuration guide

- **[QUICKSTART.md](QUICKSTART.md)**: 5-minute getting started tutorialThe agent calculates a confidence score (0-1) based on:

- **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)**: Complete demo walkthrough with screenshots

| Factor | Weight | Description |

## 🤝 Contributing|--------|--------|-------------|

| Industry Match | 30% | How well industry aligns with ICP |

Contributions are welcome! Please feel free to submit a Pull Request.| Revenue/Size | 20% | Company size within target range |

| Keywords | 15% | Presence of ICP keywords in description |

1. Fork the repository| Funding Signal | 15% | Recent funding activity |

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)| Hiring Signal | 10% | Active hiring for data roles |

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)| Tech Stack | 10% | Use of specified technologies |

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Request**Formula:**

```

## 📄 Licensescore = 0.3 × industry_match 

      + 0.2 × revenue_size_match

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.      + 0.15 × keyword_match

      + 0.15 × funding_signal

## 🙏 Acknowledgments      + 0.1 × hiring_signal

      + 0.1 × tech_stack_match

- **Apollo.io**: Company and contact data API```

- **Crunchbase**: Startup funding and company data

- **SerpAPI**: Google search integration## 🧪 Development

- **Streamlit**: Web application framework

### Project Structure

## 📧 Contact

```

For questions or support, please open an issue on GitHub.agent_3/

├── config/              # ICP configuration files

---│   ├── icp_example.yaml

│   └── icp_healthcare.json

**Built with ❤️ for B2B sales teams and growth hackers**├── src/                 # Source code

│   ├── __init__.py
│   ├── agent.py         # Main agent orchestrator
│   ├── api_client_base.py
│   ├── apollo_client.py
│   ├── crunchbase_client.py
│   ├── serpapi_client.py
│   ├── data_normalizer.py
│   └── scoring.py
├── output/              # Generated results
├── .env                 # API keys (not in git)
├── .env.example         # Template
├── requirements.txt     # Dependencies
├── run_agent.py        # Main entry point
├── test_agent.py       # Test suite
└── README.md           # This file
```

### Running Tests

```bash
# Run test suite with mock data
python test_agent.py

# Test individual components
python -c "from src.scoring import ProspectScorer; print('✓ Scoring module OK')"
```

### Adding New Data Sources

1. Create new client in `src/your_client.py`
2. Inherit from `BaseAPIClient`
3. Add normalization method in `data_normalizer.py`
4. Integrate in `agent.py`

Example:

```python
from .api_client_base import BaseAPIClient

class YourClient(BaseAPIClient):
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://api.yourservice.com",
            calls_per_minute=60
        )
    
    def search_companies(self, filters):
        return self._make_request("GET", "/companies", params=filters)
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
```bash
# Solution: Run from project root
cd agent_3
python run_agent.py
```

**Issue**: `API key not provided`
```bash
# Solution: Check .env file
cat .env  # Linux/Mac
type .env  # Windows
```

**Issue**: `Rate limit exceeded`
```python
# Solution: Adjust rate limits in clients
self.rate_limiter = RateLimiter(calls_per_minute=30)
```

**Issue**: `No prospects found`
- Check ICP criteria aren't too restrictive
- Lower `min_confidence_score` in config
- Verify API keys are valid

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance

- **Average search time**: 2-5 minutes for 50 prospects
- **API calls**: ~10-20 per prospect (depending on sources)
- **Free tier limits**:
  - Apollo: 100 credits
  - Crunchbase: 200 requests/day
  - SerpAPI: 100 searches/month

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add more data sources (LinkedIn Sales Navigator, ZoomInfo)
- [ ] Implement async/parallel API calls
- [ ] Add email verification with Hunter.io
- [ ] Create web dashboard for results
- [ ] Add database storage (PostgreSQL)
- [ ] Implement caching layer
- [ ] Add CI/CD pipeline

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Apollo.io for company and contact data
- Crunchbase for funding information
- SerpAPI for job posting scraping

## 📧 Contact

For questions or issues:
- Create an issue on GitHub
- Email: your-email@example.com

---

**Built with ❤️ for AI-powered sales intelligence**
