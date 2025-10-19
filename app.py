"""
Streamlit Frontend for ProspectSearchAgent
A beautiful web interface to search for B2B prospects
"""
import streamlit as st
import json
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import ProspectSearchAgent
import yaml

# Page config
st.set_page_config(
    page_title="ProspectSearchAgent - B2B Prospect Finder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .prospect-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .confidence-high {
        color: #4CAF50;
        font-weight: bold;
    }
    .confidence-medium {
        color: #FF9800;
        font-weight: bold;
    }
    .confidence-low {
        color: #F44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prospects' not in st.session_state:
    st.session_state.prospects = None
if 'search_complete' not in st.session_state:
    st.session_state.search_complete = False

# Header
st.markdown('<h1 class="main-header">🎯 ProspectSearchAgent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered B2B Prospect Finder</p>', unsafe_allow_html=True)

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Keys
    st.subheader("🔑 API Keys (Optional)")
    
    with st.expander("Configure API Keys", expanded=False):
        apollo_key = st.text_input("Apollo.io API Key", type="password", help="Optional - will use mock data if not provided")
        crunchbase_key = st.text_input("Crunchbase API Key", type="password", help="Optional")
        serp_key = st.text_input("SerpAPI Key", type="password", help="Optional")
    
    st.divider()
    
    # ICP Configuration
    st.subheader("🎯 Ideal Customer Profile")
    
    # Revenue Range
    col1, col2 = st.columns(2)
    with col1:
        revenue_min = st.number_input(
            "Min Revenue ($M)", 
            min_value=1, 
            max_value=1000, 
            value=20,
            step=1
        )
    with col2:
        revenue_max = st.number_input(
            "Max Revenue ($M)", 
            min_value=1, 
            max_value=10000, 
            value=200,
            step=10
        )
    
    # Employee Count
    col1, col2 = st.columns(2)
    with col1:
        employee_min = st.number_input(
            "Min Employees", 
            min_value=1, 
            max_value=10000, 
            value=100,
            step=10
        )
    with col2:
        employee_max = st.number_input(
            "Max Employees", 
            min_value=1, 
            max_value=100000, 
            value=5000,
            step=100
        )
    
    # Industries
    industries = st.multiselect(
        "Industries",
        ["B2B Software", "FinTech", "Enterprise Software", "Healthcare Technology", 
         "SaaS", "Cloud Computing", "Data Analytics", "Cybersecurity"],
        default=["B2B Software", "FinTech", "Enterprise Software"]
    )
    
    # Keywords
    keywords_input = st.text_area(
        "Keywords (comma-separated)",
        value="AI, data analytics, automation, machine learning",
        help="Keywords to search for in company descriptions"
    )
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    # Geography
    geography = st.multiselect(
        "Geography",
        ["USA", "Canada", "UK", "Europe", "Asia"],
        default=["USA"]
    )
    
    st.divider()
    
    # Search Parameters
    st.subheader("🔍 Search Parameters")
    
    max_results = st.slider("Max Results", min_value=5, max_value=100, value=50, step=5)
    min_confidence = st.slider("Min Confidence Score", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    max_contacts = st.slider("Max Contacts per Company", min_value=1, max_value=10, value=5, step=1)
    
    st.divider()
    
    # Search Button
    search_button = st.button("🚀 Search Prospects", type="primary", use_container_width=True)

# Main content area
if search_button:
    # Build ICP config
    icp_config = {
        "icp": {
            "revenue_min": revenue_min * 1000000,
            "revenue_max": revenue_max * 1000000,
            "industry": industries,
            "geography": geography,
            "employee_count_min": employee_min,
            "employee_count_max": employee_max,
            "keywords": keywords
        },
        "signals": {
            "funding": True,
            "hiring_data_roles": True,
            "tech_stack": ["AWS", "Snowflake", "Python"],
            "job_titles_to_search": [
                "VP Data", "Chief Data Officer", "VP Engineering",
                "CTO", "Head of Analytics"
            ]
        },
        "search_params": {
            "max_results": max_results,
            "min_confidence_score": min_confidence,
            "include_contacts": True,
            "max_contacts_per_company": max_contacts
        }
    }
    
    # Show progress
    with st.spinner("🔍 Searching for prospects... This may take a moment."):
        try:
            # Initialize agent
            agent = ProspectSearchAgent(
                apollo_api_key=apollo_key if apollo_key else None,
                crunchbase_api_key=crunchbase_key if crunchbase_key else None,
                serp_api_key=serp_key if serp_key else None
            )
            
            # Run search
            prospects = agent.search_prospects(icp_config)
            
            # Store in session state
            st.session_state.prospects = prospects
            st.session_state.search_complete = True
            
            # Close agent
            agent.close()
            
            st.success(f"✅ Found {len(prospects)} matching prospects!")
            
        except Exception as e:
            st.error(f"❌ Error during search: {str(e)}")
            st.exception(e)

# Display Results
if st.session_state.search_complete and st.session_state.prospects:
    prospects = st.session_state.prospects
    
    # Summary metrics
    st.header("📊 Search Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Prospects", len(prospects))
    
    with col2:
        avg_confidence = sum(p['confidence'] for p in prospects) / len(prospects) if prospects else 0
        st.metric("Avg Confidence", f"{avg_confidence:.2f}")
    
    with col3:
        total_contacts = sum(len(p.get('contacts', [])) for p in prospects)
        st.metric("Total Contacts", total_contacts)
    
    with col4:
        with_funding = sum(1 for p in prospects if p.get('signals', {}).get('new_funding'))
        st.metric("Companies w/ Funding", with_funding)
    
    st.divider()
    
    # Filters
    st.header("🔎 Filter Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_industry = st.multiselect(
            "Filter by Industry",
            options=list(set(p.get('industry', 'Unknown') for p in prospects)),
            default=[]
        )
    
    with col2:
        filter_confidence = st.slider(
            "Min Confidence",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
            key="filter_confidence"
        )
    
    with col3:
        filter_funding = st.checkbox("Only with Funding", value=False)
    
    # Apply filters
    filtered_prospects = prospects
    
    if filter_industry:
        filtered_prospects = [p for p in filtered_prospects if p.get('industry') in filter_industry]
    
    if filter_confidence > 0:
        filtered_prospects = [p for p in filtered_prospects if p.get('confidence', 0) >= filter_confidence]
    
    if filter_funding:
        filtered_prospects = [p for p in filtered_prospects if p.get('signals', {}).get('new_funding')]
    
    st.info(f"Showing {len(filtered_prospects)} of {len(prospects)} prospects")
    
    st.divider()
    
    # Display prospects
    st.header("🎯 Prospects")
    
    for idx, prospect in enumerate(filtered_prospects, 1):
        with st.container():
            # Confidence badge
            confidence = prospect.get('confidence', 0)
            if confidence >= 0.8:
                conf_class = "confidence-high"
                conf_icon = "🟢"
            elif confidence >= 0.6:
                conf_class = "confidence-medium"
                conf_icon = "🟡"
            else:
                conf_class = "confidence-low"
                conf_icon = "🔴"
            
            # Company header
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"{idx}. {prospect.get('company_name', 'Unknown')}")
                st.caption(f"🌐 {prospect.get('domain', 'N/A')} | 🏢 {prospect.get('industry', 'N/A')}")
            
            with col2:
                st.markdown(f"{conf_icon} <span class='{conf_class}'>{confidence:.0%} Match</span>", unsafe_allow_html=True)
            
            # Company details
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                revenue = prospect.get('revenue')
                if revenue:
                    st.metric("Revenue", f"${revenue/1000000:.1f}M")
                else:
                    st.metric("Revenue", "N/A")
            
            with col2:
                employees = prospect.get('employee_count')
                if employees:
                    st.metric("Employees", f"{employees:,}")
                else:
                    st.metric("Employees", "N/A")
            
            with col3:
                funding_stage = prospect.get('funding_stage', 'N/A')
                st.metric("Funding Stage", funding_stage)
            
            with col4:
                location = prospect.get('location', 'N/A')
                st.metric("Location", location)
            
            # Description
            if prospect.get('description'):
                st.write(f"**Description:** {prospect.get('description')}")
            
            # Signals
            signals = prospect.get('signals', {})
            signal_badges = []
            
            if signals.get('new_funding'):
                signal_badges.append("🚀 New Funding")
            if signals.get('recent_hiring'):
                signal_badges.append("👥 Hiring")
            if signals.get('data_roles_count', 0) > 0:
                signal_badges.append(f"📊 {signals.get('data_roles_count')} Data Roles")
            
            if signal_badges:
                st.write("**Signals:** " + " | ".join(signal_badges))
            
            # Contacts
            contacts = prospect.get('contacts', [])
            if contacts:
                with st.expander(f"📇 View {len(contacts)} Contact(s)"):
                    for contact in contacts:
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**{contact.get('name', 'N/A')}**")
                            st.caption(f"{contact.get('title', 'N/A')}")
                        
                        with col2:
                            if contact.get('email'):
                                st.code(contact.get('email'))
                            if contact.get('linkedin_url'):
                                st.markdown(f"[LinkedIn]({contact.get('linkedin_url')})")
            
            # Sources
            sources = prospect.get('source', [])
            if sources:
                st.caption(f"**Data Sources:** {', '.join(sources)}")
            
            st.divider()
    
    # Export options
    st.header("💾 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export to JSON
        json_data = json.dumps(filtered_prospects, indent=2, default=str)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="prospects.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Export to CSV (simple format)
        import csv
        import io
        
        csv_buffer = io.StringIO()
        if filtered_prospects:
            fieldnames = ['company_name', 'domain', 'industry', 'revenue', 'employee_count', 
                         'confidence', 'location', 'funding_stage']
            writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(filtered_prospects)
            
            st.download_button(
                label="📥 Download CSV",
                data=csv_buffer.getvalue(),
                file_name="prospects.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        # Clear results
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.prospects = None
            st.session_state.search_complete = False
            st.rerun()

else:
    # Welcome screen
    st.info("👈 Configure your search parameters in the sidebar and click 'Search Prospects' to begin!")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Smart Matching")
        st.write("Multi-factor confidence scoring based on industry, revenue, keywords, and signals")
    
    with col2:
        st.markdown("### 📊 Rich Data")
        st.write("Company details, contacts, funding info, and hiring signals")
    
    with col3:
        st.markdown("### 🚀 Easy Export")
        st.write("Download results in JSON or CSV format for your CRM")
    
    st.divider()
    
    # Sample output
    st.subheader("📋 Sample Output")
    
    sample_prospect = {
        "company_name": "DataMetrics Pro",
        "domain": "datametrics.io",
        "revenue": 75000000,
        "employee_count": 350,
        "industry": "B2B Software",
        "location": "San Francisco",
        "description": "Leading B2B Software company specializing in AI and data analytics",
        "funding_stage": "Series B",
        "confidence": 0.92,
        "contacts": [
            {
                "name": "Sarah Johnson",
                "title": "VP Data Science",
                "email": "sarah@datametrics.io"
            }
        ],
        "signals": {
            "new_funding": True,
            "recent_hiring": True,
            "data_roles_count": 3
        }
    }
    
    st.json(sample_prospect)

# Footer
st.divider()
st.caption("ProspectSearchAgent v1.0 | Built with ❤️ using Streamlit")
