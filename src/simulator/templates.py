#!/usr/bin/env python3
"""
Template Manager - Handles phishing page templates
"""

import os
import json
import logging
from typing import Dict, List, Optional
from jinja2 import Template, Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class TemplateManager:
    """
    Manages phishing page templates with safety controls
    """
    
    def __init__(self, templates_dir: str = "src/templates"):
        self.templates_dir = templates_dir
        self.templates: Dict[str, Dict] = {}
        self.jinja_env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Initialize template system
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize template system and load templates"""
        # Create templates directory
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Create default templates
        self._create_default_templates()
        
        # Load all templates
        self._load_templates()
        
        logger.info(f"Template manager initialized with {len(self.templates)} templates")
    
    def _create_default_templates(self):
        """Create default phishing templates for educational purposes"""
        templates = {
            "microsoft_login": {
                "name": "Microsoft Login Simulation",
                "description": "Educational simulation of Microsoft login page",
                "category": "business",
                "file": "microsoft_login.html"
            },
            "google_login": {
                "name": "Google Login Simulation", 
                "description": "Educational simulation of Google login page",
                "category": "business",
                "file": "google_login.html"
            },
            "banking_alert": {
                "name": "Banking Security Alert",
                "description": "Educational simulation of banking security alert",
                "category": "financial",
                "file": "banking_alert.html"
            },
            "it_support": {
                "name": "IT Support Request",
                "description": "Educational simulation of IT support phishing",
                "category": "internal",
                "file": "it_support.html"
            }
        }
        
        # Create template metadata file
        metadata_file = os.path.join(self.templates_dir, "templates.json")
        if not os.path.exists(metadata_file):
            with open(metadata_file, 'w') as f:
                json.dump(templates, f, indent=2)
        
        # Create HTML template files
        for template_id, template_info in templates.items():
            template_file = os.path.join(self.templates_dir, template_info["file"])
            if not os.path.exists(template_file):
                self._create_template_file(template_id, template_file)
    
    def _create_template_file(self, template_id: str, filepath: str):
        """Create individual template files"""
        templates_content = {
            "microsoft_login": '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Microsoft Account - Sign In</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f5f5f5; }
        .container { max-width: 400px; margin: 100px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo img { width: 100px; }
        h2 { color: #333; text-align: center; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; color: #333; }
        input[type="email"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .btn { background: #0078d4; color: white; padding: 12px 20px; border: none; border-radius: 4px; width: 100%; cursor: pointer; font-size: 14px; }
        .btn:hover { background: #106ebe; }
        .educational-notice { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 20px 0; border-radius: 4px; font-size: 12px; color: #856404; }
    </style>
</head>
<body>
    <!-- EDUCATIONAL SIMULATION NOTICE -->
    <div class="container">
        <div class="logo">
            <svg width="100" height="24" viewBox="0 0 100 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="100" height="24" fill="#0078d4"/>
                <text x="10" y="16" fill="white" font-family="Arial" font-size="12">Microsoft</text>
            </svg>
        </div>
        
        <h2>Sign in to your account</h2>
        
        <div class="educational-notice">
            🎓 This is an educational phishing simulation for security training purposes.
        </div>
        
        <form id="loginForm" action="/capture/{{ campaign_id }}" method="post">
            <div class="form-group">
                <label for="email">Email or phone</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="btn">Sign in</button>
        </form>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('🎓 EDUCATIONAL SIMULATION: This was a phishing test. Never enter credentials on suspicious sites!');
            window.location.href = '/education';
        });
    </script>
</body>
</html>
            ''',
            
            "google_login": '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Google Account - Sign In</title>
    <style>
        body { font-family: 'Roboto', Arial, sans-serif; margin: 0; padding: 0; background: #f8f9fa; }
        .container { max-width: 400px; margin: 100px auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .logo { text-align: center; margin-bottom: 30px; }
        h1 { color: #202124; text-align: center; margin-bottom: 30px; font-size: 24px; font-weight: 400; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #3c4043; font-size: 14px; }
        input[type="email"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 4px; box-sizing: border-box; font-size: 16px; }
        .btn { background: #1a73e8; color: white; padding: 12px 24px; border: none; border-radius: 4px; width: 100%; cursor: pointer; font-size: 14px; font-weight: 500; }
        .btn:hover { background: #1557b0; }
        .educational-notice { background: #e8f0fe; border: 1px solid #1a73e8; padding: 15px; margin: 20px 0; border-radius: 4px; font-size: 13px; color: #1557b0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg width="75" height="24" viewBox="0 0 75 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" fill="#4285f4"/>
                <text x="25" y="16" fill="#5f6368" font-family="Arial" font-size="14">Google</text>
            </svg>
        </div>
        
        <h1>Sign in</h1>
        
        <div class="educational-notice">
            🎓 Educational Simulation: This is a controlled phishing test for security awareness training.
        </div>
        
        <form id="loginForm" action="/capture/{{ campaign_id }}" method="post">
            <div class="form-group">
                <label for="email">Email or phone</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="password">Enter your password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="btn">Next</button>
        </form>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('🎓 PHISHING SIMULATION DETECTED: This was a security awareness test. Well done for proceeding cautiously!');
            window.location.href = '/education';
        });
    </script>
</body>
</html>
            ''',
            
            "banking_alert": '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Security Alert - Immediate Action Required</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: #dc3545; color: white; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; }
        .alert-icon { font-size: 48px; margin-bottom: 10px; }
        h1 { margin: 0; font-size: 24px; }
        .content { line-height: 1.6; color: #333; }
        .urgent { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .btn { background: #dc3545; color: white; padding: 15px 30px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; width: 100%; }
        .educational-notice { background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; margin: 20px 0; border-radius: 4px; color: #0c5460; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="alert-icon">⚠️</div>
            <h1>SECURITY ALERT</h1>
            <p>Suspicious Activity Detected</p>
        </div>
        
        <div class="educational-notice">
            🎓 Educational Notice: This is a simulated phishing attack for cybersecurity training.
        </div>
        
        <div class="content">
            <div class="urgent">
                <strong>URGENT ACTION REQUIRED:</strong> We have detected unauthorized access attempts on your account. 
                Your account will be suspended in 24 hours unless you verify your identity immediately.
            </div>
            
            <p>Recent suspicious activities:</p>
            <ul>
                <li>Login attempt from unknown device (IP: 203.45.67.89)</li>
                <li>Password change request from different location</li>
                <li>Unusual transaction patterns detected</li>
            </ul>
            
            <p><strong>Please verify your account immediately to prevent suspension:</strong></p>
            
            <form id="verifyForm" action="/capture/{{ campaign_id }}" method="post">
                <div class="form-group">
                    <label for="account">Account Number:</label>
                    <input type="text" id="account" name="account" required>
                </div>
                
                <div class="form-group">
                    <label for="pin">PIN:</label>
                    <input type="password" id="pin" name="pin" required>
                </div>
                
                <div class="form-group">
                    <label for="ssn">Last 4 digits of SSN:</label>
                    <input type="text" id="ssn" name="ssn" maxlength="4" required>
                </div>
                
                <button type="submit" class="btn">VERIFY ACCOUNT NOW</button>
            </form>
        </div>
    </div>
    
    <script>
        document.getElementById('verifyForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('🎓 PHISHING DETECTED: This was a simulated attack! Real banks never ask for sensitive info via email or suspicious websites.');
            window.location.href = '/education';
        });
    </script>
</body>
</html>
            ''',
            
            "it_support": '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>IT Support - Password Reset Required</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: #17a2b8; color: white; padding: 20px; border-radius: 4px; margin-bottom: 20px; }
        .logo { display: flex; align-items: center; margin-bottom: 15px; }
        .logo-icon { width: 40px; height: 40px; background: white; border-radius: 50%; margin-right: 15px; display: flex; align-items: center; justify-content: center; }
        h1 { margin: 0; font-size: 22px; }
        .subtitle { margin: 5px 0 0 0; opacity: 0.9; }
        .content { line-height: 1.6; color: #333; }
        .info-box { background: #e7f3ff; border: 1px solid #b8daff; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: 500; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .btn { background: #17a2b8; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 14px; }
        .educational-notice { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="logo-icon">🔧</div>
                <div>
                    <h1>IT Support Services</h1>
                    <p class="subtitle">Your Company IT Department</p>
                </div>
            </div>
        </div>
        
        <div class="educational-notice">
            🎓 Security Training: This is a controlled phishing simulation for educational purposes.
        </div>
        
        <div class="content">
            <h2>Password Reset Required</h2>
            
            <div class="info-box">
                <strong>System Maintenance Notice:</strong> Due to a recent security update, all users must reset their passwords within 24 hours to maintain system access.
            </div>
            
            <p>Dear Employee,</p>
            
            <p>Our security team has implemented new password requirements as part of our ongoing cybersecurity improvements. To ensure uninterrupted access to your company systems, please update your credentials using the form below.</p>
            
            <p><strong>New Password Requirements:</strong></p>
            <ul>
                <li>Minimum 8 characters</li>
                <li>Must include uppercase and lowercase letters</li>
                <li>Must include at least one number</li>
                <li>Must include at least one special character</li>
            </ul>
            
            <form id="resetForm" action="/capture/{{ campaign_id }}" method="post">
                <div class="form-group">
                    <label for="username">Username/Employee ID:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="current_password">Current Password:</label>
                    <input type="password" id="current_password" name="current_password" required>
                </div>
                
                <div class="form-group">
                    <label for="new_password">New Password:</label>
                    <input type="password" id="new_password" name="new_password" required>
                </div>
                
                <div class="form-group">
                    <label for="confirm_password">Confirm New Password:</label>
                    <input type="password" id="confirm_password" name="confirm_password" required>
                </div>
                
                <button type="submit" class="btn">Update Password</button>
            </form>
            
            <p><small>If you have questions, contact IT Support at extension 4567.</small></p>
        </div>
    </div>
    
    <script>
        document.getElementById('resetForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('🎓 PHISHING AWARENESS: This was a simulated attack! Always verify IT requests through official channels.');
            window.location.href = '/education';
        });
    </script>
</body>
</html>
            '''
        }
        
        # Write the template content
        if template_id in templates_content:
            with open(filepath, 'w') as f:
                f.write(templates_content[template_id])
    
    def _load_templates(self):
        """Load all available templates"""
        metadata_file = os.path.join(self.templates_dir, "templates.json")
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                self.templates = json.load(f)
        
        logger.info(f"Loaded {len(self.templates)} templates")
    
    def get_template(self, template_id: str) -> str:
        """Get template content by ID"""
        if template_id not in self.templates:
            raise ValueError(f"Template not found: {template_id}")
        
        template_info = self.templates[template_id]
        template_file = os.path.join(self.templates_dir, template_info["file"])
        
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"Template file not found: {template_file}")
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Add safety markers
        safety_marker = '''
<!-- EDUCATIONAL PHISHING SIMULATION -->
<!-- This page is part of a controlled security awareness training exercise -->
<!-- Report suspicious emails and websites to your IT security team -->
'''
        
        return safety_marker + content
    
    def render_template(self, template_id: str, context: Dict) -> str:
        """Render template with context variables"""
        template_content = self.get_template(template_id)
        
        # Use Jinja2 for template rendering
        template = Template(template_content)
        return template.render(**context)
    
    def template_exists(self, template_id: str) -> bool:
        """Check if template exists"""
        return template_id in self.templates
    
    def list_templates(self) -> Dict[str, Dict]:
        """List all available templates"""
        return self.templates.copy()
    
    def get_templates_by_category(self, category: str) -> Dict[str, Dict]:
        """Get templates filtered by category"""
        return {
            tid: tinfo for tid, tinfo in self.templates.items()
            if tinfo.get("category") == category
        }
    
    def add_template(self, template_id: str, template_info: Dict, content: str):
        """Add a new template"""
        # Safety check - ensure educational markers
        if "EDUCATIONAL" not in content.upper() or "SIMULATION" not in content.upper():
            logger.warning(f"Template {template_id} lacks proper educational markers")
        
        # Save template file
        template_file = os.path.join(self.templates_dir, template_info["file"])
        with open(template_file, 'w') as f:
            f.write(content)
        
        # Update metadata
        self.templates[template_id] = template_info
        
        # Save metadata
        metadata_file = os.path.join(self.templates_dir, "templates.json")
        with open(metadata_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
        
        logger.info(f"Template added: {template_id}")
    
    def validate_template(self, content: str) -> List[str]:
        """Validate template for safety and educational markers"""
        issues = []
        
        content_upper = content.upper()
        
        # Check for educational markers
        if "EDUCATIONAL" not in content_upper:
            issues.append("Missing 'EDUCATIONAL' marker")
        
        if "SIMULATION" not in content_upper:
            issues.append("Missing 'SIMULATION' marker")
        
        # Check for safety features
        if "PHISHING" not in content_upper and "TRAINING" not in content_upper:
            issues.append("Missing security awareness context")
        
        # Check for form submission handling
        if "<form" in content and "preventDefault" not in content:
            issues.append("Form should prevent actual submission for safety")
        
        return issues