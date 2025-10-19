# Demo Video Script

## ProspectSearchAgent Demo (2-5 minutes)

### Introduction (30 seconds)
"Hi! I'm demonstrating the ProspectSearchAgent - an AI-powered B2B prospect finder that automatically discovers companies matching your Ideal Customer Profile using multiple data sources."

### Architecture Overview (30 seconds)
"The agent queries three main APIs:
1. Apollo.io - for company and contact data
2. Crunchbase - for funding information
3. SerpAPI - for hiring signals from job postings

It then merges, deduplicates, and scores all prospects based on ICP fit."

### Live Demo (2-3 minutes)

#### 1. Show ICP Configuration
"First, I'll show the ICP configuration file. Here we define our target:
- Revenue range: $20M - $200M
- Industries: B2B Software, FinTech
- Employee count: 100-5000
- Keywords: AI, data analytics, automation
- Signals we care about: recent funding and hiring"

```bash
# Show config file
cat config/icp_example.yaml
```

#### 2. Run the Agent
"Now let's run the agent..."

```bash
python run_agent.py
```

"As you can see, it's:
1. Loading the ICP configuration
2. Querying Apollo for companies
3. Querying Crunchbase for funding data
4. Fetching hiring signals
5. Merging and deduplicating results
6. Calculating confidence scores"

#### 3. Show Results
"And here are the results! We found [X] companies that match our ICP."

```bash
# Show output
cat output/prospects.json | python -m json.tool | head -50
```

"For each prospect, we have:
- Company details (revenue, size, industry)
- Decision-maker contacts with emails
- Signals like recent funding or hiring
- Confidence score from 0 to 1"

#### 4. Highlight Top Prospect
"Let's look at our top match: [Company Name]
- Confidence score: 0.92
- Revenue: $75M (in our range)
- Industry: Software (matches ICP)
- Signals: Recent Series B funding + hiring 3 data scientists
- Contact: VP of Data Science with verified email"

### Technical Highlights (30 seconds)
"Key features:
- Rate limiting and retry logic for API stability
- Smart deduplication across sources
- Multi-factor confidence scoring
- Easily extensible to add more data sources
- Runs entirely on free API tiers"

### Conclusion (30 seconds)
"The agent saved hours of manual research by:
- Automatically querying multiple data sources
- Finding hard-to-get contact information
- Scoring prospects by ICP fit
- Providing actionable, enriched data

Perfect for sales teams, business development, or market research!"

---

## Recording Tips

1. **Screen Setup**
   - Clear desktop
   - Terminal with large font (16pt+)
   - IDE/editor ready with code open

2. **What to Show**
   - Quick code walkthrough (30 seconds)
   - ICP configuration file
   - Running the agent (real-time or sped up)
   - JSON output results
   - Highlight 1-2 good examples

3. **Tools**
   - OBS Studio (free screen recorder)
   - Loom (easy screen recording)
   - Windows Game Bar (Win + G)

4. **Upload**
   - YouTube (unlisted)
   - Google Drive (shareable link)
   - Loom (shareable link)

5. **What NOT to Show**
   - Your actual API keys
   - Personal information
   - Long waiting times (speed up or cut)

## Sample Video Structure

```
00:00 - Title card / Introduction
00:30 - Architecture diagram
01:00 - ICP configuration walkthrough
01:30 - Running the agent (demo)
03:00 - Results showcase
04:00 - Top prospect highlight
04:30 - Conclusion & features recap
05:00 - End screen
```

## Bonus Points

- Show code quality (clean, documented)
- Demonstrate error handling
- Show test suite running
- Explain design decisions
- Discuss scalability

Good luck with your demo! 🎬
