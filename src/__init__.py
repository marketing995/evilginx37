#!/usr/bin/env python3
"""
Evilginx Campaign Simulator - Source Package
Educational cybersecurity training framework

CRITICAL NOTICE: EDUCATIONAL USE ONLY
See docs/ethical-guidelines.md for complete usage restrictions and legal requirements.
"""

__version__ = "1.0.0"
__description__ = "Educational phishing simulation framework for cybersecurity training"
__author__ = "Cybersecurity Portfolio Project"
__license__ = "Educational Use Only"

# Safety check - ensure ethical guidelines have been reviewed
import os
import sys

def check_ethical_compliance():
    """Check if ethical guidelines exist and remind users to review them"""
    guidelines_path = os.path.join(os.path.dirname(__file__), "..", "docs", "ethical-guidelines.md")
    
    if not os.path.exists(guidelines_path):
        print("⚠️  WARNING: Ethical guidelines not found!")
        print("Please ensure you have reviewed all ethical and legal requirements before use.")
        return False
    
    return True

# Perform compliance check on import
if not check_ethical_compliance():
    print("🚨 COMPLIANCE WARNING: Please review ethical guidelines before proceeding")

# Educational disclaimer
EDUCATIONAL_DISCLAIMER = """
🎓 EDUCATIONAL NOTICE:
This tool is designed exclusively for authorized cybersecurity education and training.
Unauthorized use is illegal and unethical. Always obtain proper written authorization
before conducting any phishing simulations.
"""

print(EDUCATIONAL_DISCLAIMER)