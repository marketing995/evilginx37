#!/usr/bin/env python3
"""
Sample Campaign Creation Script
Educational demonstration of Evilginx Campaign Simulator

IMPORTANT: This is for educational purposes only.
Ensure proper authorization before running any campaigns.
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_authorization():
    """Check if proper authorization is in place"""
    auth_file = "config/authorization.json"
    
    if not os.path.exists(auth_file):
        print("❌ Authorization file not found!")
        print("Please run './quick-start.sh' first to set up authorization.")
        return False
    
    try:
        with open(auth_file, 'r') as f:
            auth = json.load(f)
        
        if not auth.get("authorized", False):
            print("❌ Authorization not granted!")
            print("Please complete the authorization form in config/authorization.json")
            return False
        
        if "REQUIRED" in str(auth):
            print("❌ Authorization form incomplete!")
            print("Please fill out all required fields in config/authorization.json")
            return False
        
        # Check expiry
        try:
            expiry = datetime.fromisoformat(auth.get("expiry_date", ""))
            if datetime.now() > expiry:
                print("❌ Authorization has expired!")
                print("Please update the expiry date in config/authorization.json")
                return False
        except:
            print("❌ Invalid expiry date format in authorization!")
            return False
        
        print("✅ Valid authorization found")
        print(f"   Authorized by: {auth.get('authorized_by', 'Unknown')}")
        print(f"   Organization: {auth.get('organization', 'Unknown')}")
        print(f"   Purpose: {auth.get('purpose', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Error reading authorization: {e}")
        return False

def create_sample_campaign():
    """Create a sample educational campaign"""
    
    print("🎯 Creating Sample Educational Campaign")
    print("=" * 50)
    
    # Check authorization first
    if not check_authorization():
        return False
    
    try:
        # Import after authorization check
        from src.simulator.core import EvilginxSimulator
        
        # Initialize simulator
        print("🔧 Initializing simulator...")
        simulator = EvilginxSimulator()
        
        # Campaign configuration
        campaign_data = {
            "name": "Educational Demo - Microsoft Login Simulation",
            "target_domain": "training-demo.local",
            "template": "microsoft_login",
            "duration_hours": 1,  # Short duration for demo
            "max_targets": 10,    # Small target group for demo
            "authorized_by": "Demo Administrator",
            "safety_mode": True,
            "auto_terminate": True
        }
        
        print("📋 Campaign Configuration:")
        for key, value in campaign_data.items():
            print(f"   {key}: {value}")
        print()
        
        # Create campaign
        print("🚀 Creating campaign...")
        campaign_id = simulator.create_campaign(campaign_data)
        
        print("✅ Campaign created successfully!")
        print(f"📝 Campaign ID: {campaign_id}")
        print()
        
        # Display next steps
        print("📋 Next Steps:")
        print(f"1. Start campaign: python3 -c \"")
        print(f"   import sys; sys.path.append('.')")
        print(f"   from src.simulator.core import EvilginxSimulator")
        print(f"   s = EvilginxSimulator()")
        print(f"   s.start_campaign('{campaign_id}')")
        print(f"   s.run()\"")
        print()
        print(f"2. Access dashboard: http://127.0.0.1:8080")
        print(f"3. View phishing page: http://127.0.0.1:8080/phish/{campaign_id}")
        print()
        
        # Safety reminders
        print("🛡️  Safety Reminders:")
        print("• This is a controlled educational simulation")
        print("• All pages include educational disclaimers")
        print("• No actual credentials are stored")
        print("• Campaign will auto-terminate after 1 hour")
        print("• Use Ctrl+C to stop the campaign manually")
        print()
        
        return campaign_id
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error creating campaign: {e}")
        return False

def demonstrate_safety_features():
    """Demonstrate the safety features of the simulator"""
    
    print("🛡️  Safety Feature Demonstration")
    print("=" * 40)
    
    try:
        from src.simulator.safety import SafetyManager
        from src.simulator.analytics import AnalyticsEngine
        
        # Initialize safety manager
        safety = SafetyManager()
        analytics = AnalyticsEngine()
        
        print("✅ Safety Manager initialized")
        print("   - Real-time monitoring active")
        print("   - Rate limiting enabled")
        print("   - Auto-termination scheduled")
        print()
        
        print("✅ Analytics Engine initialized") 
        print("   - Event logging active")
        print("   - Privacy protection enabled")
        print("   - Data anonymization active")
        print()
        
        # Generate safety report
        safety_report = safety.get_safety_report()
        print("📊 Current Safety Status:")
        print(f"   - Total interventions: {safety_report['total_interventions']}")
        print(f"   - Blocked campaigns: {safety_report['blocked_campaigns']}")
        print(f"   - Safety status: {safety_report['safety_status']}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error demonstrating safety features: {e}")
        return False

def main():
    """Main function for sample campaign creation"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    EDUCATIONAL CAMPAIGN SIMULATOR                    ║
║                         SAMPLE DEMONSTRATION                         ║
║                                                                      ║
║  🎓 This is a controlled educational demonstration                   ║
║  📚 Designed for cybersecurity learning purposes                    ║
║  ⚖️  Includes comprehensive safety and ethical controls              ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if this is being run directly
    if len(sys.argv) > 1 and sys.argv[1] == "--safety-demo":
        return demonstrate_safety_features()
    
    # Create sample campaign
    campaign_id = create_sample_campaign()
    
    if campaign_id:
        print("🎉 Sample campaign setup complete!")
        print("📖 Review the documentation in docs/ for more information")
        print("🔒 Remember: Always follow ethical guidelines and legal requirements")
        return True
    else:
        print("❌ Sample campaign creation failed")
        print("Please check the error messages above and try again")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)