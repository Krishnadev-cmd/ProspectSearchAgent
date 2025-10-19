"""
Demo script to run the ProspectSearchAgent
"""
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import ProspectSearchAgent


def main():
    """Run the ProspectSearchAgent with example ICP"""
    
    print("=" * 70)
    print("ProspectSearchAgent - AI-powered B2B Prospect Finder")
    print("=" * 70)
    print()
    
    # Initialize the agent
    print("Initializing ProspectSearchAgent...")
    agent = ProspectSearchAgent()
    
    # Load ICP configuration
    icp_path = "config/icp_example.yaml"
    print(f"Loading ICP configuration from: {icp_path}")
    
    if not os.path.exists(icp_path):
        print(f"ERROR: ICP config file not found at {icp_path}")
        print("Please ensure you're running from the project root directory.")
        return
    
    agent.load_icp(icp_path)
    print("✓ ICP loaded successfully")
    print()
    
    # Run the search
    print("Starting prospect search...")
    print("This may take a few minutes as we query multiple APIs...")
    print("-" * 70)
    
    try:
        prospects = agent.search_prospects()
        
        print()
        print("=" * 70)
        print(f"Search Complete! Found {len(prospects)} matching prospects")
        print("=" * 70)
        print()
        
        # Display results
        if prospects:
            print("Top 5 Prospects:")
            print("-" * 70)
            
            for i, prospect in enumerate(prospects[:5], 1):
                print(f"\n{i}. {prospect.get('company_name')}")
                print(f"   Domain: {prospect.get('domain')}")
                print(f"   Industry: {prospect.get('industry')}")
                print(f"   Revenue: ${prospect.get('revenue', 0):,.0f}" if prospect.get('revenue') else "   Revenue: N/A")
                print(f"   Employees: {prospect.get('employee_count')}")
                print(f"   Confidence Score: {prospect.get('confidence')}")
                print(f"   Sources: {', '.join(prospect.get('source', []))}")
                
                # Display contacts
                contacts = prospect.get('contacts', [])
                if contacts:
                    print(f"   Contacts: {len(contacts)} found")
                    for contact in contacts[:2]:  # Show first 2
                        print(f"      - {contact.get('name')} ({contact.get('title')})")
                        if contact.get('email'):
                            print(f"        Email: {contact.get('email')}")
                
                # Display signals
                signals = prospect.get('signals', {})
                signal_list = []
                if signals.get('new_funding'):
                    signal_list.append("🚀 New Funding")
                if signals.get('recent_hiring'):
                    signal_list.append("👥 Hiring")
                if signals.get('data_roles_count', 0) > 0:
                    signal_list.append(f"📊 {signals.get('data_roles_count')} Data Roles")
                
                if signal_list:
                    print(f"   Signals: {' | '.join(signal_list)}")
        
        # Save results
        output_path = "output/prospects.json"
        agent.save_results(prospects, output_path)
        
        print()
        print("=" * 70)
        print(f"✓ Results saved to: {output_path}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        agent.close()
        print("\nAgent closed. Goodbye!")


if __name__ == "__main__":
    main()
