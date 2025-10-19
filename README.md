# ProspectSearchAgent 🎯

An AI-powered B2B prospect finder that identifies high-quality leads matching your Ideal Customer Profile (ICP) by aggregating data from Apollo.io, Crunchbase, and SerpAPI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 How to Run

### Option 1: Web Interface (Recommended)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set Up API Keys** (Optional - works with demo data if not provided)
```bash
# Copy the template
copy .env.example .env

# Edit .env and add your API keys
APOLLO_API_KEY=your_key_here
CRUNCHBASE_API_KEY=your_key_here
SERPAPI_KEY=your_key_here
```

3. **Launch the Streamlit App**
```bash
streamlit run app.py
```

The web interface will open at **http://localhost:8501**

### Option 2: Command Line Interface

```bash
python run_agent.py
```

Results are saved to `output/prospects.json`

---

## 🎯 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ProspectSearchAgent                       │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Apollo.io  │  │  Crunchbase  │  │   SerpAPI    │      │
│  │   Client     │  │   Client     │  │   Client     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │               │
│         └──────────────────┼──────────────────┘              │
│                            │                                  │
│                    ┌───────▼────────┐                        │
│                    │ Data Normalizer│                        │
│                    └───────┬────────┘                        │
│                            │                                  │
│                    ┌───────▼────────┐                        │
│                    │  Deduplicator  │                        │
│                    └───────┬────────┘                        │
│                            │                                  │
│                    ┌───────▼────────┐                        │
│                    │Confidence Score│                        │
│                    └───────┬────────┘                        │
│                            │                                  │
│                    ┌───────▼────────┐                        │
│                    │  JSON Output   │                        │
│                    └────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process

**1. ICP Configuration**
- Define your ideal customer profile with filters:
  - Revenue range ($5M - $200M)
  - Company size (50 - 5,000 employees)
  - Industries (SaaS, FinTech, Healthcare, etc.)
  - Keywords (technologies, signals)

**2. Multi-Source Data Collection**
- **Apollo.io**: Company data, contact information
- **Crunchbase**: Funding rounds, investor details
- **SerpAPI**: Job postings, hiring signals

The agent queries all APIs in parallel to maximize speed.

**3. Data Normalization**
- Each API returns data in different formats
- The `DataNormalizer` converts all data to a unified schema:
  ```python
  {
    "company_name": str,
    "domain": str,
    "revenue": int,
    "employee_count": int,
    "industry": str,
    "contacts": [...]
  }
  ```

**4. Intelligent Deduplication**
- Removes duplicates by:
  - Company domain (e.g., `example.com`)
  - Email addresses for contacts
- Merges data from multiple sources for the same company

**5. Confidence Scoring**

The agent calculates a confidence score (0-1 scale) based on 6 factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Industry Match | 30% | Target industry alignment |
| Revenue/Size | 20% | Within specified ranges |
| Keywords | 15% | Presence of ICP keywords |
| Funding Signal | 15% | Recent funding activity |
| Hiring Signal | 10% | Active hiring for key roles |
| Tech Stack | 10% | Use of specified technologies |

**Formula:**
```
confidence_score = 0.30 × industry_match 
                 + 0.20 × revenue_size_match
                 + 0.15 × keyword_match
                 + 0.15 × funding_signal
                 + 0.10 × hiring_signal
                 + 0.10 × tech_stack_match
```

**6. Output**
- Web Interface: Interactive table with filters, export buttons
- CLI: JSON file with all prospect data

---

## 📊 Output Format

```json
[
  {
    "company_name": "TechCorp AI",
    "domain": "techcorp.ai",
    "revenue": 75000000,
    "employee_count": 250,
    "industry": "Software",
    "location": "San Francisco, CA",
    "description": "AI-powered analytics platform",
    "confidence_score": 0.92,
    "funding": {
      "stage": "Series B",
      "total": 25000000,
      "investors": ["Accel Partners"]
    },
    "contacts": [
      {
        "name": "Jane Smith",
        "title": "VP of Engineering",
        "email": "jane@techcorp.ai",
        "linkedin": "linkedin.com/in/janesmith",
        "phone": "+1-555-0123"
      }
    ],
    "signals": {
      "recent_funding": true,
      "hiring_data_roles": 3,
      "tech_stack": ["AWS", "Python", "React"]
    }
  }
]
```

---

## 🎨 Using the Web Interface

### 1. Configure Your ICP (Left Sidebar)

![ICP Configuration](https://via.placeholder.com/600x400?text=ICP+Configuration+Sidebar)

- **Revenue Range**: Min $5M - Max $200M
- **Employee Count**: 50 - 5,000 employees
- **Industries**: Select from 20+ options
- **Keywords**: Add technologies (AI, cloud, SaaS)

### 2. Search for Prospects

Click **"🔍 Search for Prospects"** button

The agent will:
- Query all data sources
- Show progress indicator
- Display results in real-time

### 3. View & Filter Results

![Results Table](https://via.placeholder.com/600x400?text=Prospects+Results+Table)

- **Confidence Badges**: Color-coded scores (🟢 High, 🟡 Medium, 🔴 Low)
- **Interactive Filters**: Adjust min confidence, revenue, employees
- **Expandable Cards**: Click to see contacts and details

### 4. Export Data

- **CSV Download**: Import into CRM or spreadsheet
- **JSON Download**: Programmatic access

---

## 🔑 API Setup (Optional)

The app works with **realistic mock data** if you don't have API keys. For production use:

| API | Free Tier | Sign Up |
|-----|-----------|---------|
| **Apollo.io** | 100 credits/month | [apollo.io](https://www.apollo.io/) |
| **Crunchbase** | 200 requests/day | [crunchbase.com/api](https://data.crunchbase.com/docs) |
| **SerpAPI** | 100 searches/month | [serpapi.com](https://serpapi.com/) |

Add keys to `.env` file:
```env
APOLLO_API_KEY=your_apollo_key
CRUNCHBASE_API_KEY=your_crunchbase_key
SERPAPI_KEY=your_serpapi_key
```

**Note**: Apollo's free tier doesn't support company search endpoints. The app automatically uses mock data when this is detected.

---

## 📝 ICP Configuration Examples

### Example 1: SaaS Companies (YAML)
```yaml
# config/icp_example.yaml
icp:
  revenue_min: 10000000      # $10M
  revenue_max: 100000000     # $100M
  industry:
    - "B2B Software"
    - "SaaS"
  employee_count_min: 50
  employee_count_max: 500
  keywords:
    - "AI"
    - "machine learning"
    - "cloud platform"

signals:
  funding: true
  tech_stack:
    - "AWS"
    - "Python"
```

### Example 2: HealthTech (JSON)
```json
{
  "icp": {
    "revenue_min": 5000000,
    "revenue_max": 50000000,
    "industry": ["Healthcare Technology"],
    "employee_count_min": 100,
    "keywords": ["HIPAA", "EHR", "telemedicine"]
  },
  "signals": {
    "funding": true,
    "hiring_data_roles": true
  }
}
```

---

## 🛠️ Troubleshooting

### Common Issues

**Issue**: Streamlit not found
```bash
pip install streamlit>=1.28.0
```

**Issue**: No prospects found
- Lower the `min_confidence_score` in filters
- Broaden ICP criteria (wider revenue/employee ranges)
- Check API keys are valid

**Issue**: "403 Forbidden" from Apollo
- **Cause**: Free tier doesn't support company search
- **Solution**: App automatically uses mock data

**Issue**: Import errors
```bash
pip install -r requirements.txt --upgrade
```

---

## 📁 Project Structure

```
agent_3/
├── app.py                    # Streamlit web interface
├── run_agent.py              # CLI entry point
├── src/
│   ├── agent.py              # Main orchestrator
│   ├── apollo_client.py      # Apollo.io integration
│   ├── crunchbase_client.py  # Crunchbase integration
│   ├── serpapi_client.py     # SerpAPI integration
│   ├── data_normalizer.py    # Schema unification
│   ├── scoring.py            # Confidence scoring
│   └── mock_data.py          # Demo data generator
├── config/
│   ├── icp_example.yaml      # Sample ICP (YAML)
│   └── icp_healthcare.json   # Sample ICP (JSON)
├── output/
│   └── prospects.json        # Search results
└── requirements.txt          # Python dependencies
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **Apollo.io** - Company & contact data
- **Crunchbase** - Funding information
- **SerpAPI** - Job posting data
- **Streamlit** - Web framework

---

**Built with ❤️ for B2B sales teams**
