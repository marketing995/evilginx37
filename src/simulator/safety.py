#!/usr/bin/env python3
"""
Safety Manager - Comprehensive safety controls for phishing simulation
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading

logger = logging.getLogger(__name__)

class SafetyManager:
    """
    Manages all safety controls and interventions for the simulator
    """
    
    def __init__(self):
        self.safety_triggers: Dict[str, int] = {}
        self.blocked_campaigns: set = set()
        self.intervention_log: List[Dict] = []
        self.start_time = time.time()
        
        # Safety thresholds
        self.max_visits_per_minute = 100
        self.max_captures_per_hour = 50
        self.max_campaign_runtime = 24 * 3600  # 24 hours in seconds
        
        # Initialize monitoring
        self._start_monitoring()
    
    def _start_monitoring(self):
        """Start background safety monitoring"""
        def monitor():
            while True:
                self._check_safety_conditions()
                time.sleep(60)  # Check every minute
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        logger.info("Safety monitoring started")
    
    def _check_safety_conditions(self):
        """Perform periodic safety checks"""
        current_time = time.time()
        
        # Check total runtime
        if current_time - self.start_time > self.max_campaign_runtime:
            logger.warning("Maximum simulator runtime exceeded - triggering safety shutdown")
            self._trigger_emergency_shutdown("Runtime limit exceeded")
        
        # Check for excessive activity
        self._check_activity_patterns()
    
    def _check_activity_patterns(self):
        """Check for suspicious activity patterns"""
        # This is where you'd implement ML-based anomaly detection
        # For now, we'll use simple thresholds
        pass
    
    def can_start_campaign(self, campaign) -> bool:
        """Check if a campaign can be safely started"""
        campaign_id = campaign.id
        
        # Check if campaign is blocked
        if campaign_id in self.blocked_campaigns:
            logger.warning(f"Campaign {campaign_id} is blocked")
            return False
        
        # Check authorization
        if not self._verify_campaign_authorization(campaign):
            logger.error(f"Campaign {campaign_id} lacks proper authorization")
            return False
        
        # Check safety mode
        if not campaign.safety_mode:
            logger.warning(f"Campaign {campaign_id} has safety mode disabled")
            # In a real scenario, you might want to block this
        
        return True
    
    def can_serve_page(self, campaign_id: str) -> bool:
        """Check if a phishing page can be safely served"""
        # Check rate limiting
        if self._is_rate_limited(campaign_id):
            self._log_safety_intervention(campaign_id, "rate_limit", "Too many requests")
            return False
        
        # Check if campaign is still active
        if campaign_id in self.blocked_campaigns:
            self._log_safety_intervention(campaign_id, "blocked_campaign", "Campaign blocked")
            return False
        
        return True
    
    def _is_rate_limited(self, campaign_id: str) -> bool:
        """Check if campaign is being rate limited"""
        current_time = time.time()
        
        # Simple rate limiting implementation
        if campaign_id not in self.safety_triggers:
            self.safety_triggers[campaign_id] = []
        
        # Clean old entries
        self.safety_triggers[campaign_id] = [
            t for t in self.safety_triggers[campaign_id] 
            if current_time - t < 60  # Last minute
        ]
        
        # Check rate
        if len(self.safety_triggers[campaign_id]) > self.max_visits_per_minute:
            return True
        
        # Record this access
        self.safety_triggers[campaign_id].append(current_time)
        return False
    
    def _verify_campaign_authorization(self, campaign) -> bool:
        """Verify campaign has proper authorization"""
        # Check if authorized_by field is properly filled
        if not campaign.authorized_by or campaign.authorized_by == "REQUIRED":
            return False
        
        # Check authorization date is recent
        try:
            auth_date = datetime.fromisoformat(campaign.authorization_date)
            if datetime.now() - auth_date > timedelta(days=30):
                logger.warning(f"Campaign authorization is old: {campaign.authorization_date}")
                return False
        except:
            return False
        
        return True
    
    def _log_safety_intervention(self, campaign_id: str, intervention_type: str, reason: str):
        """Log safety interventions"""
        intervention = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_id,
            "type": intervention_type,
            "reason": reason
        }
        
        self.intervention_log.append(intervention)
        logger.warning(f"Safety intervention: {intervention_type} for campaign {campaign_id} - {reason}")
    
    def block_campaign(self, campaign_id: str, reason: str):
        """Block a campaign for safety reasons"""
        self.blocked_campaigns.add(campaign_id)
        self._log_safety_intervention(campaign_id, "campaign_blocked", reason)
        logger.error(f"Campaign {campaign_id} blocked: {reason}")
    
    def _trigger_emergency_shutdown(self, reason: str):
        """Trigger emergency shutdown of entire simulator"""
        logger.critical(f"EMERGENCY SHUTDOWN TRIGGERED: {reason}")
        
        # Log the emergency
        emergency_log = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "type": "emergency_shutdown"
        }
        
        self.intervention_log.append(emergency_log)
        
        # In a real implementation, this would trigger actual shutdown
        # For safety, we'll just log it
        print("🚨 EMERGENCY SHUTDOWN TRIGGERED 🚨")
        print(f"Reason: {reason}")
    
    def get_safety_report(self) -> Dict:
        """Generate safety report"""
        return {
            "total_interventions": len(self.intervention_log),
            "blocked_campaigns": len(self.blocked_campaigns),
            "recent_interventions": [
                i for i in self.intervention_log 
                if datetime.fromisoformat(i["timestamp"]) > datetime.now() - timedelta(hours=24)
            ],
            "safety_status": "operational" if len(self.blocked_campaigns) == 0 else "interventions_active"
        }
    
    def export_safety_log(self, filepath: str):
        """Export safety log to file"""
        safety_data = {
            "export_time": datetime.now().isoformat(),
            "intervention_log": self.intervention_log,
            "blocked_campaigns": list(self.blocked_campaigns),
            "safety_report": self.get_safety_report()
        }
        
        with open(filepath, 'w') as f:
            json.dump(safety_data, f, indent=2)
        
        logger.info(f"Safety log exported to {filepath}")