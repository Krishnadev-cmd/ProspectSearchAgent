# 🚀 Quick Start Guide - ProspectSearchAgent

Get up and running in 5 minutes!

## Option 1: Quick Test (No API Keys Required)

Test the agent with mock data:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run test suite
python test_agent.py
```

You should see:
```
✓ All tests completed successfully!
✓ Mock results saved to: output/mock_prospects.json
```

## Option 2: Full Setup (With API Keys)

### Step 1: Get FREE API Keys (10 minutes)

**Apollo.io** (100 free credits)
- Sign up: https://app.apollo.io/
- Go to: Settings → API → Create API Key
- Copy key

**Crunchbase** (Free developer account)
- Sign up: https://www.crunchbase.com/
- Apply for API: https://data.crunchbase.com/docs
- Copy user key

**SerpAPI** (100 free searches)
- Sign up: https://serpapi.com/
- Copy API key from dashboard

### Step 2: Configure (1 minute)

```bash
# Copy template
copy .env.example .env

# Edit .env file and paste your keys
notepad .env
```

Your .env should look like:
```env
APOLLO_API_KEY=actual_key_here_no_quotes
CRUNCHBASE_API_KEY=actual_key_here_no_quotes
SERP_API_KEY=actual_key_here_no_quotes
```

### Step 3: Run (2 minutes)

```bash
python run_agent.py
```

Expected output:
```
ProspectSearchAgent - AI-powered B2B Prospect Finder
====================================================
Initializing ProspectSearchAgent...
✓ ICP loaded successfully

Starting prospect search...
Fetching companies from Apollo...
Fetching companies from Crunchbase...
Processing company: DataIQ Inc
...
Search Complete! Found 15 matching prospects
====================================================
```

### Step 4: View Results

Check `output/prospects.json` for results!

## Common Issues

❌ **"Module not found"**
```bash
# Make sure you're in project root
cd agent_3
python run_agent.py
```

❌ **"API key not provided"**
```bash
# Check .env file exists and has keys
type .env  # Windows
cat .env   # Mac/Linux
```

❌ **Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. ✅ Run test suite: `python test_agent.py`
2. ✅ Get API keys (see Step 1 above)
3. ✅ Configure `.env` file
4. ✅ Run: `python run_agent.py`
5. ✅ Customize `config/icp_example.yaml` for your use case

## Need Help?

- 📖 Full documentation: See README.md
- 🔧 Setup issues: See SETUP.md
- 🎬 Demo video: See DEMO_SCRIPT.md

## Want to Customize?

Edit `config/icp_example.yaml`:

```yaml
icp:
  revenue_min: 50000000     # Change target revenue
  revenue_max: 500000000
  industry:
    - "Your Industry Here"  # Add your industries
  keywords:
    - "your keywords"       # Add relevant keywords
```

Then run again:
```bash
python run_agent.py
```

---

**Happy Prospecting! 🎯**

Questions? Check the README.md for full documentation.
