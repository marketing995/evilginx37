#!/usr/bin/env python3
"""
Evilginx Campaign Simulator
Educational phishing simulation framework for cybersecurity training

EDUCATIONAL USE ONLY - See ethical-guidelines.md for usage restrictions
"""

__version__ = "1.0.0"
__author__ = "Cybersecurity Portfolio Project"
__email__ = "security@example.com"
__license__ = "Educational Use Only"

# Import main classes for easy access
from .core import EvilginxSimulator, Campaign
from .safety import SafetyManager
from .analytics import AnalyticsEngine
from .templates import TemplateManager

__all__ = [
    'EvilginxSimulator',
    'Campaign', 
    'SafetyManager',
    'AnalyticsEngine',
    'TemplateManager'
]

# Educational warning
print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    EDUCATIONAL PHISHING SIMULATOR                    ║
║                                                                      ║
║  ⚠️  WARNING: This tool is for authorized educational purposes only  ║
║                                                                      ║
║  • Only use in authorized environments                               ║
║  • Obtain written permission before deployment                       ║
║  • Follow responsible disclosure practices                           ║
║  • Comply with local laws and regulations                            ║
║                                                                      ║
║  See docs/ethical-guidelines.md for complete usage restrictions      ║
╚══════════════════════════════════════════════════════════════════════╝
""")