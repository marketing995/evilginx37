#!/bin/bash

# Evilginx Campaign Simulator - Quick Start Script
# EDUCATIONAL USE ONLY - Ensure proper authorization before use

set -e

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    EVILGINX CAMPAIGN SIMULATOR                       ║"
echo "║                         QUICK START SETUP                           ║"
echo "║                                                                      ║"
echo "║  ⚠️  WARNING: EDUCATIONAL USE ONLY                                   ║"
echo "║  Ensure you have proper authorization before proceeding              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo

# Check for required dependencies
echo "🔍 Checking system requirements..."

# Check Python 3.8+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(echo "$PYTHON_VERSION < $REQUIRED_VERSION" | bc -l)" = "1" ]; then
    echo "❌ Python 3.8+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment
echo "🛠️  Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if authorization file exists
echo "🔒 Checking authorization status..."
if [ ! -f "config/authorization.json" ]; then
    echo "⚠️  Authorization file not found"
    echo "📝 Creating authorization template..."
    
    mkdir -p config
    
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
    
    echo "📋 Authorization template created at config/authorization.json"
    echo "🚨 IMPORTANT: You must complete the authorization form before use!"
else
    # Check if authorization is properly filled
    if grep -q "REQUIRED" config/authorization.json; then
        echo "⚠️  Authorization form is incomplete"
        echo "🚨 IMPORTANT: Complete config/authorization.json before use!"
    else
        echo "✅ Authorization file found"
    fi
fi

# Test basic import
echo "🧪 Testing installation..."
if python3 -c "import sys; sys.path.append('.'); from src.simulator import EvilginxSimulator; print('✅ Installation test passed')" 2>/dev/null; then
    echo "✅ Core modules imported successfully"
else
    echo "❌ Installation test failed"
    echo "Check the error messages above and ensure all dependencies are installed"
    exit 1
fi

# Display next steps
echo
echo "🎉 Setup completed successfully!"
echo
echo "📋 Next Steps:"
echo "1. Complete authorization form: config/authorization.json"
echo "2. Review ethical guidelines: docs/ethical-guidelines.md"
echo "3. Review safety guide: docs/safety-guide.md"
echo "4. Create your first campaign: python3 -c 'from examples import create_sample_campaign; create_sample_campaign()'"
echo "5. Read implementation guide: docs/implementation-guide.md"
echo
echo "🔗 Quick Commands:"
echo "  • View documentation: ls docs/"
echo "  • Create sample campaign: python3 examples/sample_campaign.py"
echo "  • Run tests: python3 -m pytest (if tests are available)"
echo
echo "⚠️  CRITICAL REMINDERS:"
echo "  • This tool is for EDUCATIONAL USE ONLY"
echo "  • Obtain written authorization before any testing"
echo "  • Follow all legal and ethical guidelines"
echo "  • Review docs/ethical-guidelines.md thoroughly"
echo
echo "🆘 Support:"
echo "  • Documentation: docs/"
echo "  • Implementation guide: docs/implementation-guide.md"
echo "  • Safety guide: docs/safety-guide.md"
echo
echo "Happy (ethical) hacking! 🛡️"