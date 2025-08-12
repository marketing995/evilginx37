# 🚀 Evilginx Campaign Simulator - Implementation Guide

## Step-by-Step Setup and Deployment

### ⚠️ IMPORTANT NOTICE
This guide is for **AUTHORIZED EDUCATIONAL PURPOSES ONLY**. Ensure you have proper written authorization before proceeding with any phishing simulation activities.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Installation Process](#installation-process)
4. [Configuration](#configuration)
5. [Campaign Creation](#campaign-creation)
6. [Running Simulations](#running-simulations)
7. [Monitoring and Management](#monitoring-and-management)
8. [Cleanup and Termination](#cleanup-and-termination)
9. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows with WSL
- **Python**: 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 10GB free space
- **Network**: Stable internet connection

### Required Permissions
- [ ] **Administrative Access**: Local admin rights for installation
- [ ] **Network Access**: Ability to configure local network settings
- [ ] **Firewall Configuration**: Permission to open required ports
- [ ] **Legal Authorization**: Written approval for phishing simulation

### Dependencies
```bash
# System packages (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# For CentOS/RHEL
sudo yum install python3 python3-pip git

# For macOS (with Homebrew)
brew install python3 git
```

---

## 🛠️ Environment Setup

### Step 1: Create Project Directory
```bash
# Create project directory
mkdir evilginx-simulator
cd evilginx-simulator

# Clone repository (if using version control)
git clone <repository-url> .
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import flask, requests, beautifulsoup4; print('Dependencies installed successfully')"
```

---

## 📦 Installation Process

### Step 1: Initialize Project Structure
```bash
# Create directory structure
mkdir -p {src/{simulator,templates,campaigns,analytics},safety,docs,examples,config}

# Copy source files to appropriate directories
# (Files should already be in place if cloned from repository)
```

### Step 2: Initialize Supporting Modules
```bash
# Create __init__.py files for Python modules
touch src/__init__.py
touch src/simulator/__init__.py
```

### Step 3: Set Up Configuration Files
```bash
# Create configuration directory
mkdir -p config

# Initialize default configuration
python -c "
from src.simulator.core import EvilginxSimulator
simulator = EvilginxSimulator()
print('Configuration initialized')
"
```

---

## ⚙️ Configuration

### Step 1: Authorization Setup
```bash
# Create authorization file
cat > config/authorization.json << EOF
{
  "authorized": false,
  "authorized_by": "REQUIRED - Name and title of authorizing person",
  "organization": "REQUIRED - Organization name",
  "purpose": "REQUIRED - Specific purpose (e.g., 'Security Awareness Training')",
  "scope": "REQUIRED - Scope of testing",
  "authorization_date": "REQUIRED - ISO format date",
  "expiry_date": "REQUIRED - ISO format date (max 30 days)",
  "contact_email": "REQUIRED - Contact email for authorization",
  "emergency_contact": "REQUIRED - Emergency contact information"
}
EOF
```

### Step 2: Complete Authorization Form
Edit `config/authorization.json` with proper authorization details:

```json
{
  "authorized": true,
  "authorized_by": "John Smith, CISO",
  "organization": "Acme Corporation",
  "purpose": "Q1 2024 Security Awareness Training",
  "scope": "IT Department phishing simulation (50 employees)",
  "authorization_date": "2024-01-15T09:00:00",
  "expiry_date": "2024-02-15T09:00:00",
  "contact_email": "john.smith@acme.com",
  "emergency_contact": "Security Hotline: +1-555-SECURE"
}
```

### Step 3: Configure Simulator Settings
Edit `config/simulator.json`:

```json
{
  "safety": {
    "require_authorization": true,
    "max_campaign_duration": 24,
    "max_concurrent_campaigns": 3,
    "auto_terminate": true,
    "simulation_mode": true
  },
  "server": {
    "host": "127.0.0.1",
    "port": 8080,
    "debug": false
  },
  "logging": {
    "level": "INFO",
    "log_credentials": false,
    "anonymize_data": true
  }
}
```

---

## 🎯 Campaign Creation

### Step 1: Create Campaign Script
Create `create_campaign.py`:

```python
#!/usr/bin/env python3
"""
Campaign Creation Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.simulator.core import EvilginxSimulator
from datetime import datetime, timedelta

def create_sample_campaign():
    """Create a sample phishing campaign"""
    
    # Initialize simulator
    simulator = EvilginxSimulator()
    
    # Campaign configuration
    campaign_data = {
        "name": "IT Security Training - Microsoft Login",
        "target_domain": "login-secure.training.local",
        "template": "microsoft_login",
        "duration_hours": 8,
        "max_targets": 25,
        "authorized_by": "John Smith, CISO",
        "safety_mode": True,
        "auto_terminate": True
    }
    
    try:
        # Create campaign
        campaign_id = simulator.create_campaign(campaign_data)
        print(f"✅ Campaign created successfully!")
        print(f"Campaign ID: {campaign_id}")
        print(f"Campaign Name: {campaign_data['name']}")
        print(f"Template: {campaign_data['template']}")
        print(f"Duration: {campaign_data['duration_hours']} hours")
        
        return campaign_id
        
    except Exception as e:
        print(f"❌ Error creating campaign: {e}")
        return None

if __name__ == "__main__":
    campaign_id = create_sample_campaign()
    if campaign_id:
        print(f"\n📋 Next steps:")
        print(f"1. Review campaign settings")
        print(f"2. Start campaign: python start_campaign.py {campaign_id}")
        print(f"3. Monitor dashboard: http://localhost:8080")
```

### Step 2: Run Campaign Creation
```bash
# Create campaign
python create_campaign.py

# Expected output:
# ✅ Campaign created successfully!
# Campaign ID: camp_1642234567_abc12345
# Campaign Name: IT Security Training - Microsoft Login
# Template: microsoft_login
# Duration: 8 hours
```

---

## 🏃 Running Simulations

### Step 1: Start Campaign Script
Create `start_campaign.py`:

```python
#!/usr/bin/env python3
"""
Campaign Startup Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.simulator.core import EvilginxSimulator
import threading
import time

def start_campaign(campaign_id):
    """Start a specific campaign"""
    
    # Initialize simulator
    simulator = EvilginxSimulator()
    
    try:
        # Start campaign
        success = simulator.start_campaign(campaign_id)
        
        if success:
            print(f"✅ Campaign {campaign_id} started successfully!")
            
            # Start web server in background
            server_thread = threading.Thread(
                target=simulator.run,
                kwargs={'host': '127.0.0.1', 'port': 8080},
                daemon=True
            )
            server_thread.start()
            
            print(f"🌐 Web server started on http://127.0.0.1:8080")
            print(f"📊 Dashboard: http://127.0.0.1:8080")
            print(f"🎯 Phishing page: http://127.0.0.1:8080/phish/{campaign_id}")
            
            # Keep main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping campaign...")
                simulator.stop_campaign(campaign_id)
                print("✅ Campaign stopped")
                
        else:
            print(f"❌ Failed to start campaign {campaign_id}")
            
    except Exception as e:
        print(f"❌ Error starting campaign: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python start_campaign.py <campaign_id>")
        sys.exit(1)
    
    campaign_id = sys.argv[1]
    start_campaign(campaign_id)
```

### Step 2: Launch Campaign
```bash
# Start campaign (replace with actual campaign ID)
python start_campaign.py camp_1642234567_abc12345

# Expected output:
# ✅ Campaign camp_1642234567_abc12345 started successfully!
# 🌐 Web server started on http://127.0.0.1:8080
# 📊 Dashboard: http://127.0.0.1:8080
# 🎯 Phishing page: http://127.0.0.1:8080/phish/camp_1642234567_abc12345
```

### Step 3: Access Simulation
1. **Dashboard**: Navigate to `http://127.0.0.1:8080`
2. **Phishing Page**: Use the campaign-specific URL
3. **API Endpoints**: Access REST API for automation

---

## 📊 Monitoring and Management

### Real-time Dashboard
Access the web dashboard at `http://127.0.0.1:8080`:

- **Campaign Overview**: Active campaigns and statistics
- **Real-time Metrics**: Visits, captures, and success rates
- **Safety Status**: Current safety controls and interventions
- **System Health**: Server status and performance metrics

### Command Line Monitoring
Create `monitor_campaign.py`:

```python
#!/usr/bin/env python3
"""
Campaign Monitoring Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json
import time
from datetime import datetime

def monitor_campaign(campaign_id, interval=30):
    """Monitor campaign in real-time"""
    
    base_url = "http://127.0.0.1:8080"
    
    print(f"🔍 Monitoring campaign: {campaign_id}")
    print(f"📊 Refresh interval: {interval} seconds")
    print("=" * 60)
    
    try:
        while True:
            # Get campaign status
            response = requests.get(f"{base_url}/api/campaign/{campaign_id}")
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('statistics', {})
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Campaign Status:")
                print(f"  Status: {data.get('status', 'unknown')}")
                print(f"  Visits: {stats.get('visits', 0)}")
                print(f"  Captures: {stats.get('captures', 0)}")
                print(f"  Safety Triggers: {stats.get('safety_triggers', 0)}")
                
                # Calculate success rate
                visits = stats.get('visits', 0)
                captures = stats.get('captures', 0)
                if visits > 0:
                    success_rate = (captures / visits) * 100
                    print(f"  Success Rate: {success_rate:.1f}%")
                
            else:
                print(f"❌ Error fetching campaign data: {response.status_code}")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
    except Exception as e:
        print(f"❌ Monitoring error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python monitor_campaign.py <campaign_id> [interval]")
        sys.exit(1)
    
    campaign_id = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    monitor_campaign(campaign_id, interval)
```

### Run Monitoring
```bash
# Monitor campaign with 30-second updates
python monitor_campaign.py camp_1642234567_abc12345 30

# Expected output:
# 🔍 Monitoring campaign: camp_1642234567_abc12345
# 📊 Refresh interval: 30 seconds
# ============================================================
# 
# [14:30:15] Campaign Status:
#   Status: active
#   Visits: 5
#   Captures: 1
#   Safety Triggers: 0
#   Success Rate: 20.0%
```

---

## 🧹 Cleanup and Termination

### Manual Campaign Termination
Create `stop_campaign.py`:

```python
#!/usr/bin/env python3
"""
Campaign Termination Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json

def stop_campaign(campaign_id):
    """Stop a specific campaign"""
    
    base_url = "http://127.0.0.1:8080"
    
    try:
        # Stop campaign via API
        response = requests.post(f"{base_url}/api/shutdown")
        
        if response.status_code == 200:
            print(f"✅ Campaign {campaign_id} stopped successfully")
            print("📊 Generating final reports...")
            
            # Get final statistics
            stats_response = requests.get(f"{base_url}/api/campaign/{campaign_id}")
            if stats_response.status_code == 200:
                data = stats_response.json()
                stats = data.get('statistics', {})
                
                print("\n📈 Final Campaign Statistics:")
                print(f"  Total Visits: {stats.get('visits', 0)}")
                print(f"  Total Captures: {stats.get('captures', 0)}")
                print(f"  Safety Triggers: {stats.get('safety_triggers', 0)}")
                print(f"  Start Time: {stats.get('start_time', 'Unknown')}")
                print(f"  End Time: {stats.get('end_time', 'Unknown')}")
        else:
            print(f"❌ Error stopping campaign: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error stopping campaign: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python stop_campaign.py <campaign_id>")
        sys.exit(1)
    
    campaign_id = sys.argv[1]
    stop_campaign(campaign_id)
```

### Complete System Cleanup
```bash
# Stop specific campaign
python stop_campaign.py camp_1642234567_abc12345

# Clean up logs and temporary files
rm -f simulator.log analytics.log

# Deactivate virtual environment
deactivate

# Optional: Remove entire project (be careful!)
# cd .. && rm -rf evilginx-simulator
```

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Authorization Errors
```
Error: No valid authorization found. Simulator will not start.
```

**Solution:**
```bash
# Check authorization file
cat config/authorization.json

# Ensure "authorized" is set to true
# Verify expiry_date is in the future
# Check all required fields are filled
```

#### 2. Port Conflicts
```
Error: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find process using port 8080
sudo lsof -i :8080

# Kill conflicting process
sudo kill -9 <PID>

# Or use different port
# Edit config/simulator.json and change "port" value
```

#### 3. Template Not Found
```
Error: Template not found: microsoft_login
```

**Solution:**
```bash
# Check template files exist
ls src/templates/

# Verify templates.json
cat src/templates/templates.json

# Recreate templates if needed
python -c "
from src.simulator.templates import TemplateManager
tm = TemplateManager()
print('Templates reinitialized')
"
```

#### 4. Permission Errors
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Fix file permissions
chmod +x *.py
chmod -R 755 src/

# Check virtual environment
source venv/bin/activate
which python
```

#### 5. Module Import Errors
```
ModuleNotFoundError: No module named 'src.simulator'
```

**Solution:**
```bash
# Add current directory to Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Or run from project root
cd /path/to/evilginx-simulator
python create_campaign.py
```

### Debug Mode
Enable debug mode for detailed logging:

```bash
# Edit config/simulator.json
{
  "server": {
    "debug": true
  },
  "logging": {
    "level": "DEBUG"
  }
}

# Run with verbose output
python -v start_campaign.py <campaign_id>
```

### Log Analysis
```bash
# View simulator logs
tail -f simulator.log

# View analytics logs
tail -f analytics.log

# Check for errors
grep -i error simulator.log
```

---

## 📋 Quick Reference

### Essential Commands
```bash
# Setup
python create_campaign.py

# Start campaign
python start_campaign.py <campaign_id>

# Monitor campaign
python monitor_campaign.py <campaign_id>

# Stop campaign
python stop_campaign.py <campaign_id>
```

### Key URLs
- **Dashboard**: `http://127.0.0.1:8080`
- **Phishing Page**: `http://127.0.0.1:8080/phish/<campaign_id>`
- **API Status**: `http://127.0.0.1:8080/api/campaigns`

### Configuration Files
- **Authorization**: `config/authorization.json`
- **Simulator**: `config/simulator.json`
- **Templates**: `src/templates/templates.json`

### Safety Features
- ✅ Automatic campaign termination
- ✅ Rate limiting and traffic controls
- ✅ Educational disclaimers on all pages
- ✅ No actual credential storage
- ✅ Comprehensive audit logging

---

## 🎓 Next Steps

After successful implementation:

1. **Review Results**: Analyze campaign effectiveness and user responses
2. **Update Training**: Use results to improve security awareness programs
3. **Document Lessons**: Record lessons learned for future campaigns
4. **Plan Follow-up**: Schedule additional training based on results
5. **Continuous Improvement**: Iterate on campaign design and delivery

---

**Remember**: This tool is designed for educational purposes only. Always ensure proper authorization and follow ethical guidelines when conducting phishing simulations.