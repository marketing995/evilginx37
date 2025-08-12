#!/usr/bin/env python3
"""
Evilginx Campaign Simulator - Core Engine
Educational tool for authorized phishing simulation testing
"""

import os
import sys
import time
import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import threading
from flask import Flask, request, render_template_string, redirect, jsonify

from .safety import SafetyManager
from .analytics import AnalyticsEngine
from .templates import TemplateManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simulator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Campaign:
    """Campaign configuration object"""
    id: str
    name: str
    target_domain: str
    template: str
    duration_hours: int
    max_targets: int
    authorized_by: str
    authorization_date: str
    safety_mode: bool = True
    auto_terminate: bool = True
    
class EvilginxSimulator:
    """
    Main simulator class with comprehensive safety controls
    """
    
    def __init__(self, config_path: str = "config/simulator.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.safety_manager = SafetyManager()
        self.analytics = AnalyticsEngine()
        self.template_manager = TemplateManager()
        self.app = Flask(__name__)
        self.active_campaigns: Dict[str, Campaign] = {}
        self.simulation_data: Dict = {}
        self.start_time = None
        self.running = False
        
        # Safety controls
        self.max_campaign_duration = 24  # hours
        self.max_concurrent_campaigns = 3
        self.require_authorization = True
        
        self._setup_routes()
        self._initialize_safety_checks()
        
    def _load_config(self) -> Dict:
        """Load simulator configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            return self._create_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Create default configuration"""
        config = {
            "safety": {
                "require_authorization": True,
                "max_campaign_duration": 24,
                "max_concurrent_campaigns": 3,
                "auto_terminate": True,
                "simulation_mode": True
            },
            "server": {
                "host": "127.0.0.1",
                "port": 8080,
                "debug": False
            },
            "logging": {
                "level": "INFO",
                "log_credentials": False,
                "anonymize_data": True
            }
        }
        
        # Save default config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config
    
    def _initialize_safety_checks(self):
        """Initialize all safety mechanisms"""
        logger.info("Initializing safety checks...")
        
        # Check for authorization
        if self.config["safety"]["require_authorization"]:
            if not self._verify_authorization():
                logger.error("No valid authorization found. Simulator will not start.")
                sys.exit(1)
        
        # Initialize automatic termination
        if self.config["safety"]["auto_terminate"]:
            self._setup_auto_termination()
        
        # Educational warning
        self._display_educational_warning()
    
    def _verify_authorization(self) -> bool:
        """Verify proper authorization is in place"""
        auth_file = "config/authorization.json"
        if not os.path.exists(auth_file):
            logger.warning("No authorization file found. Creating template...")
            self._create_authorization_template()
            return False
        
        try:
            with open(auth_file, 'r') as f:
                auth = json.load(f)
            
            # Check if authorization is valid and not expired
            if auth.get("authorized", False):
                exp_date = datetime.fromisoformat(auth.get("expiry_date", ""))
                if datetime.now() < exp_date:
                    logger.info(f"Valid authorization found. Authorized by: {auth.get('authorized_by', 'Unknown')}")
                    return True
                else:
                    logger.error("Authorization has expired")
            
        except Exception as e:
            logger.error(f"Error verifying authorization: {e}")
        
        return False
    
    def _create_authorization_template(self):
        """Create authorization template"""
        auth_template = {
            "authorized": False,
            "authorized_by": "REQUIRED - Name and title of authorizing person",
            "organization": "REQUIRED - Organization name",
            "purpose": "REQUIRED - Specific purpose (e.g., 'Security Awareness Training')",
            "scope": "REQUIRED - Scope of testing",
            "authorization_date": "REQUIRED - ISO format date",
            "expiry_date": "REQUIRED - ISO format date (max 30 days)",
            "contact_email": "REQUIRED - Contact email for authorization",
            "emergency_contact": "REQUIRED - Emergency contact information"
        }
        
        os.makedirs("config", exist_ok=True)
        with open("config/authorization.json", 'w') as f:
            json.dump(auth_template, f, indent=2)
        
        logger.info("Authorization template created at config/authorization.json")
        logger.info("Please fill out the authorization form before running simulations")
    
    def _setup_auto_termination(self):
        """Setup automatic termination after max duration"""
        def auto_terminate():
            time.sleep(self.max_campaign_duration * 3600)  # Convert hours to seconds
            if self.running:
                logger.warning("Auto-terminating simulator after maximum duration")
                self.stop_all_campaigns()
                self.shutdown()
        
        termination_thread = threading.Thread(target=auto_terminate, daemon=True)
        termination_thread.start()
    
    def _display_educational_warning(self):
        """Display educational warning and disclaimer"""
        warning = """
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
        ║  Unauthorized use is illegal and unethical!                         ║
        ╚══════════════════════════════════════════════════════════════════════╝
        """
        print(warning)
        logger.info("Educational disclaimer displayed")
    
    def create_campaign(self, campaign_data: Dict) -> str:
        """Create a new phishing campaign with safety checks"""
        try:
            # Safety checks
            if len(self.active_campaigns) >= self.max_concurrent_campaigns:
                raise ValueError(f"Maximum concurrent campaigns ({self.max_concurrent_campaigns}) reached")
            
            if campaign_data.get("duration_hours", 0) > self.max_campaign_duration:
                raise ValueError(f"Campaign duration exceeds maximum ({self.max_campaign_duration} hours)")
            
            # Create campaign object
            campaign = Campaign(
                id=self._generate_campaign_id(),
                name=campaign_data["name"],
                target_domain=campaign_data["target_domain"],
                template=campaign_data["template"],
                duration_hours=min(campaign_data["duration_hours"], self.max_campaign_duration),
                max_targets=campaign_data.get("max_targets", 100),
                authorized_by=campaign_data["authorized_by"],
                authorization_date=datetime.now().isoformat(),
                safety_mode=campaign_data.get("safety_mode", True),
                auto_terminate=campaign_data.get("auto_terminate", True)
            )
            
            # Validate campaign
            if not self._validate_campaign(campaign):
                raise ValueError("Campaign validation failed")
            
            # Store campaign
            self.active_campaigns[campaign.id] = campaign
            
            # Log campaign creation
            self.analytics.log_event("campaign_created", {
                "campaign_id": campaign.id,
                "name": campaign.name,
                "authorized_by": campaign.authorized_by
            })
            
            logger.info(f"Campaign created: {campaign.name} (ID: {campaign.id})")
            return campaign.id
            
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            raise
    
    def _generate_campaign_id(self) -> str:
        """Generate unique campaign ID"""
        timestamp = str(int(time.time()))
        random_part = hashlib.md5(os.urandom(16)).hexdigest()[:8]
        return f"camp_{timestamp}_{random_part}"
    
    def _validate_campaign(self, campaign: Campaign) -> bool:
        """Validate campaign configuration"""
        # Check required fields
        required_fields = ["name", "target_domain", "template", "authorized_by"]
        for field in required_fields:
            if not getattr(campaign, field, None):
                logger.error(f"Missing required field: {field}")
                return False
        
        # Check template exists
        if not self.template_manager.template_exists(campaign.template):
            logger.error(f"Template not found: {campaign.template}")
            return False
        
        # Check domain format
        if not self._is_valid_domain(campaign.target_domain):
            logger.error(f"Invalid domain format: {campaign.target_domain}")
            return False
        
        return True
    
    def _is_valid_domain(self, domain: str) -> bool:
        """Validate domain format"""
        import re
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
        return re.match(pattern, domain) is not None
    
    def start_campaign(self, campaign_id: str) -> bool:
        """Start a campaign with safety checks"""
        try:
            if campaign_id not in self.active_campaigns:
                raise ValueError(f"Campaign not found: {campaign_id}")
            
            campaign = self.active_campaigns[campaign_id]
            
            # Safety check
            if not self.safety_manager.can_start_campaign(campaign):
                logger.error("Safety manager blocked campaign start")
                return False
            
            # Initialize campaign data
            self.simulation_data[campaign_id] = {
                "start_time": datetime.now().isoformat(),
                "status": "active",
                "visits": 0,
                "captures": 0,
                "safety_triggers": 0
            }
            
            # Log campaign start
            self.analytics.log_event("campaign_started", {
                "campaign_id": campaign_id,
                "name": campaign.name
            })
            
            logger.info(f"Campaign started: {campaign.name} (ID: {campaign_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error starting campaign {campaign_id}: {e}")
            return False
    
    def stop_campaign(self, campaign_id: str) -> bool:
        """Stop a specific campaign"""
        try:
            if campaign_id not in self.active_campaigns:
                raise ValueError(f"Campaign not found: {campaign_id}")
            
            campaign = self.active_campaigns[campaign_id]
            
            # Update status
            if campaign_id in self.simulation_data:
                self.simulation_data[campaign_id]["status"] = "stopped"
                self.simulation_data[campaign_id]["end_time"] = datetime.now().isoformat()
            
            # Log campaign stop
            self.analytics.log_event("campaign_stopped", {
                "campaign_id": campaign_id,
                "name": campaign.name
            })
            
            logger.info(f"Campaign stopped: {campaign.name} (ID: {campaign_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping campaign {campaign_id}: {e}")
            return False
    
    def stop_all_campaigns(self):
        """Stop all active campaigns"""
        for campaign_id in list(self.active_campaigns.keys()):
            self.stop_campaign(campaign_id)
        logger.info("All campaigns stopped")
    
    def get_campaign_status(self, campaign_id: str) -> Dict:
        """Get campaign status and statistics"""
        if campaign_id not in self.active_campaigns:
            return {"error": "Campaign not found"}
        
        campaign = self.active_campaigns[campaign_id]
        data = self.simulation_data.get(campaign_id, {})
        
        return {
            "campaign": asdict(campaign),
            "status": data.get("status", "unknown"),
            "statistics": {
                "visits": data.get("visits", 0),
                "captures": data.get("captures", 0),
                "safety_triggers": data.get("safety_triggers", 0),
                "start_time": data.get("start_time"),
                "end_time": data.get("end_time")
            }
        }
    
    def _setup_routes(self):
        """Setup Flask routes for the simulator"""
        
        @self.app.route('/')
        def index():
            return self._render_dashboard()
        
        @self.app.route('/phish/<campaign_id>')
        def phishing_page(campaign_id):
            return self._handle_phishing_request(campaign_id)
        
        @self.app.route('/capture/<campaign_id>', methods=['POST'])
        def capture_credentials(campaign_id):
            return self._handle_credential_capture(campaign_id)
        
        @self.app.route('/api/campaigns')
        def api_campaigns():
            return jsonify(list(self.active_campaigns.keys()))
        
        @self.app.route('/api/campaign/<campaign_id>')
        def api_campaign_status(campaign_id):
            return jsonify(self.get_campaign_status(campaign_id))
        
        @self.app.route('/api/shutdown', methods=['POST'])
        def api_shutdown():
            self.stop_all_campaigns()
            return jsonify({"status": "shutdown"})
    
    def _render_dashboard(self) -> str:
        """Render the main dashboard"""
        dashboard_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Phishing Simulator Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .warning { background: #ffebee; border: 1px solid #f44336; padding: 10px; margin: 10px 0; }
                .campaign { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
                .stats { display: inline-block; margin: 0 20px; }
            </style>
        </head>
        <body>
            <h1>🎯 Evilginx Campaign Simulator Dashboard</h1>
            
            <div class="warning">
                <strong>⚠️ EDUCATIONAL USE ONLY</strong><br>
                This simulator is for authorized security testing and education only.
            </div>
            
            <h2>Active Campaigns</h2>
            {% for campaign_id, campaign in campaigns.items() %}
            <div class="campaign">
                <h3>{{ campaign.name }} ({{ campaign_id }})</h3>
                <p><strong>Target:</strong> {{ campaign.target_domain }}</p>
                <p><strong>Template:</strong> {{ campaign.template }}</p>
                <p><strong>Authorized by:</strong> {{ campaign.authorized_by }}</p>
                <div class="stats">
                    <span>Visits: {{ stats.get(campaign_id, {}).get('visits', 0) }}</span>
                    <span>Captures: {{ stats.get(campaign_id, {}).get('captures', 0) }}</span>
                </div>
            </div>
            {% endfor %}
            
            {% if not campaigns %}
            <p>No active campaigns</p>
            {% endif %}
            
            <h2>System Status</h2>
            <p>Running: {{ running }}</p>
            <p>Safety Mode: Enabled</p>
            <p>Start Time: {{ start_time }}</p>
        </body>
        </html>
        '''
        
        from jinja2 import Template
        template = Template(dashboard_html)
        
        return template.render(
            campaigns=self.active_campaigns,
            stats=self.simulation_data,
            running=self.running,
            start_time=self.start_time
        )
    
    def _handle_phishing_request(self, campaign_id: str) -> str:
        """Handle incoming phishing page requests"""
        if campaign_id not in self.active_campaigns:
            return "Campaign not found", 404
        
        campaign = self.active_campaigns[campaign_id]
        
        # Safety check
        if not self.safety_manager.can_serve_page(campaign_id):
            logger.warning(f"Safety manager blocked page serving for campaign {campaign_id}")
            return self._render_safety_page()
        
        # Log visit
        if campaign_id in self.simulation_data:
            self.simulation_data[campaign_id]["visits"] += 1
        
        # Get template
        template_content = self.template_manager.get_template(campaign.template)
        
        # Render phishing page
        return self._render_phishing_page(campaign, template_content)
    
    def _handle_credential_capture(self, campaign_id: str) -> str:
        """Handle credential capture (educational simulation only)"""
        if campaign_id not in self.active_campaigns:
            return jsonify({"error": "Campaign not found"}), 404
        
        # Safety check - never actually store credentials
        if not self.config["logging"]["log_credentials"]:
            logger.info(f"Credential capture simulation for campaign {campaign_id} (not logged)")
        
        # Update statistics
        if campaign_id in self.simulation_data:
            self.simulation_data[campaign_id]["captures"] += 1
        
        # Log event (without credentials)
        self.analytics.log_event("credential_capture_simulation", {
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat(),
            "ip_hash": hashlib.sha256(request.remote_addr.encode()).hexdigest()[:16]
        })
        
        return jsonify({"status": "simulated", "redirect": "/education"})
    
    def _render_phishing_page(self, campaign: Campaign, template_content: str) -> str:
        """Render phishing page with safety notices in source"""
        # Add safety comment to source
        safety_comment = f'''
        <!--
        EDUCATIONAL SIMULATION NOTICE:
        This is a controlled phishing simulation for security training.
        Campaign: {campaign.name}
        Authorized by: {campaign.authorized_by}
        Date: {campaign.authorization_date}
        -->
        '''
        
        return safety_comment + template_content
    
    def _render_safety_page(self) -> str:
        """Render safety intervention page"""
        return '''
        <html>
        <head><title>Security Notice</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🛡️ Security Training Notice</h1>
            <p>This appears to be a phishing simulation for security training.</p>
            <p>If you were not expecting this, please contact your IT security team.</p>
            <p><a href="/education">Learn about phishing protection</a></p>
        </body>
        </html>
        '''
    
    def run(self, host: str = None, port: int = None, debug: bool = False):
        """Run the simulator server"""
        try:
            self.running = True
            self.start_time = datetime.now().isoformat()
            
            host = host or self.config["server"]["host"]
            port = port or self.config["server"]["port"]
            debug = debug or self.config["server"]["debug"]
            
            logger.info(f"Starting Evilginx Simulator on {host}:{port}")
            self.app.run(host=host, port=port, debug=debug)
            
        except Exception as e:
            logger.error(f"Error running simulator: {e}")
            raise
    
    def shutdown(self):
        """Shutdown the simulator"""
        logger.info("Shutting down simulator...")
        self.running = False
        self.stop_all_campaigns()
        
        # Generate final report
        self.analytics.generate_report()
        
        logger.info("Simulator shutdown complete")