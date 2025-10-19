# Setup Guide for ProspectSearchAgent

## Step-by-Step Setup

### 1. Install Python (if not already installed)

Download Python 3.10+ from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
```

### 2. Set Up Project

```bash
# Navigate to project directory
cd agent_3

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

#### Create .env file:
```bash
# Copy template
copy .env.example .env
```

#### Get API Keys:

**Apollo.io** (Free 100 credits)
1. Go to https://app.apollo.io/
2. Sign up for free account
3. Click your avatar → Settings
4. Navigate to Integrations → API
5. Click "Create API Key"
6. Copy the key

**Crunchbase** (Free developer account)
1. Go to https://www.crunchbase.com/
2. Create account
3. Apply for API access at https://data.crunchbase.com/docs
4. Once approved, get your user key from dashboard
5. Copy the key

**SerpAPI** (Free 100 searches/month)
1. Go to https://serpapi.com/
2. Sign up for free account
3. Copy API key from dashboard

#### Add keys to .env:
```env
APOLLO_API_KEY=your_actual_apollo_key_here
CRUNCHBASE_API_KEY=your_actual_crunchbase_key_here
SERP_API_KEY=your_actual_serpapi_key_here
```

### 4. Test Installation

```bash
# Run test suite (works without API keys)
python test_agent.py
```

You should see:
```
✓ All tests completed successfully!
```

### 5. Run Your First Search

```bash
# Run with example ICP
python run_agent.py
```

### 6. Customize Your Search

Edit `config/icp_example.yaml`:
```yaml
icp:
  revenue_min: 20000000  # Change to your target
  revenue_max: 200000000
  industry:
    - "Your Industry"  # Add your industries
  # ... modify other parameters
```

Run again:
```bash
python run_agent.py
```

## Troubleshooting Setup

### Virtual Environment Issues

**Windows**: If you get execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Import errors**: Make sure venv is activated:
```bash
# You should see (venv) in your prompt
(venv) C:\...\agent_3>
```

### API Key Issues

**Test if keys are loaded**:
```python
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('APOLLO_API_KEY'))"
```

Should print your key (not None).

### Dependency Issues

**If installation fails**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

**Missing modules**:
```bash
# Install individually
pip install requests pyyaml python-dotenv
```

## Next Steps

1. ✅ Run `test_agent.py` to verify setup
2. ✅ Add real API keys to `.env`
3. ✅ Customize `config/icp_example.yaml`
4. ✅ Run `run_agent.py`
5. ✅ Check `output/prospects.json` for results

## Need Help?

- Check main README.md for detailed documentation
- Review error messages carefully
- Make sure you're running from project root directory
- Verify API keys are valid and not expired

Happy prospecting! 🎯
