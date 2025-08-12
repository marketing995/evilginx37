#!/usr/bin/env python3
"""
Analytics Engine - Campaign tracking and reporting
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib
from collections import defaultdict

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """
    Handles all analytics, metrics, and reporting for campaigns
    """
    
    def __init__(self, log_file: str = "analytics.log"):
        self.log_file = log_file
        self.events: List[Dict] = []
        self.metrics: Dict = defaultdict(int)
        self.session_data: Dict = {}
        
        # Initialize analytics
        self._initialize_analytics()
    
    def _initialize_analytics(self):
        """Initialize analytics system"""
        logger.info("Analytics engine initialized")
        
        # Create analytics directory
        os.makedirs("analytics", exist_ok=True)
        
        # Load existing data if available
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing analytics data"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            event = json.loads(line.strip())
                            self.events.append(event)
        except Exception as e:
            logger.error(f"Error loading analytics data: {e}")
    
    def log_event(self, event_type: str, data: Dict):
        """Log an analytics event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        # Add to memory
        self.events.append(event)
        
        # Write to log file immediately
        self._write_event_to_file(event)
        
        # Update metrics
        self.metrics[event_type] += 1
        self.metrics["total_events"] += 1
        
        logger.debug(f"Analytics event logged: {event_type}")
    
    def _write_event_to_file(self, event: Dict):
        """Write event to log file"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            logger.error(f"Error writing analytics event: {e}")
    
    def get_campaign_metrics(self, campaign_id: str) -> Dict:
        """Get metrics for a specific campaign"""
        campaign_events = [
            e for e in self.events 
            if e.get("data", {}).get("campaign_id") == campaign_id
        ]
        
        metrics = {
            "total_events": len(campaign_events),
            "visits": 0,
            "captures": 0,
            "unique_visitors": set(),
            "timeline": [],
            "success_rate": 0.0
        }
        
        for event in campaign_events:
            event_type = event["event_type"]
            timestamp = event["timestamp"]
            data = event.get("data", {})
            
            if event_type == "page_visit":
                metrics["visits"] += 1
                ip_hash = data.get("ip_hash", "unknown")
                metrics["unique_visitors"].add(ip_hash)
                
            elif event_type == "credential_capture_simulation":
                metrics["captures"] += 1
            
            # Add to timeline
            metrics["timeline"].append({
                "timestamp": timestamp,
                "event": event_type,
                "data": data
            })
        
        # Convert set to count
        metrics["unique_visitors"] = len(metrics["unique_visitors"])
        
        # Calculate success rate
        if metrics["visits"] > 0:
            metrics["success_rate"] = (metrics["captures"] / metrics["visits"]) * 100
        
        return metrics
    
    def get_overall_metrics(self) -> Dict:
        """Get overall system metrics"""
        total_campaigns = len(set(
            e.get("data", {}).get("campaign_id") 
            for e in self.events 
            if e.get("data", {}).get("campaign_id")
        ))
        
        total_visits = sum(1 for e in self.events if e["event_type"] == "page_visit")
        total_captures = sum(1 for e in self.events if e["event_type"] == "credential_capture_simulation")
        
        # Get unique visitors across all campaigns
        unique_visitors = set()
        for event in self.events:
            if event["event_type"] in ["page_visit", "credential_capture_simulation"]:
                ip_hash = event.get("data", {}).get("ip_hash")
                if ip_hash:
                    unique_visitors.add(ip_hash)
        
        return {
            "total_campaigns": total_campaigns,
            "total_visits": total_visits,
            "total_captures": total_captures,
            "unique_visitors": len(unique_visitors),
            "overall_success_rate": (total_captures / total_visits * 100) if total_visits > 0 else 0,
            "event_types": dict(self.metrics),
            "first_event": self.events[0]["timestamp"] if self.events else None,
            "last_event": self.events[-1]["timestamp"] if self.events else None
        }
    
    def get_time_series_data(self, campaign_id: str = None, hours: int = 24) -> Dict:
        """Get time series data for visualization"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter events
        if campaign_id:
            events = [
                e for e in self.events 
                if e.get("data", {}).get("campaign_id") == campaign_id
                and datetime.fromisoformat(e["timestamp"]) > cutoff_time
            ]
        else:
            events = [
                e for e in self.events 
                if datetime.fromisoformat(e["timestamp"]) > cutoff_time
            ]
        
        # Group by hour
        hourly_data = defaultdict(lambda: {"visits": 0, "captures": 0})
        
        for event in events:
            timestamp = datetime.fromisoformat(event["timestamp"])
            hour_key = timestamp.strftime("%Y-%m-%d %H:00")
            
            if event["event_type"] == "page_visit":
                hourly_data[hour_key]["visits"] += 1
            elif event["event_type"] == "credential_capture_simulation":
                hourly_data[hour_key]["captures"] += 1
        
        # Convert to list format
        timeline = []
        for hour in sorted(hourly_data.keys()):
            timeline.append({
                "hour": hour,
                "visits": hourly_data[hour]["visits"],
                "captures": hourly_data[hour]["captures"]
            })
        
        return {"timeline": timeline}
    
    def generate_report(self, campaign_id: str = None) -> Dict:
        """Generate comprehensive analytics report"""
        if campaign_id:
            campaign_metrics = self.get_campaign_metrics(campaign_id)
            time_series = self.get_time_series_data(campaign_id)
            
            report = {
                "report_type": "campaign",
                "campaign_id": campaign_id,
                "generated_at": datetime.now().isoformat(),
                "metrics": campaign_metrics,
                "time_series": time_series,
                "recommendations": self._generate_recommendations(campaign_metrics)
            }
        else:
            overall_metrics = self.get_overall_metrics()
            time_series = self.get_time_series_data()
            
            report = {
                "report_type": "overall",
                "generated_at": datetime.now().isoformat(),
                "metrics": overall_metrics,
                "time_series": time_series,
                "campaign_summaries": self._get_campaign_summaries()
            }
        
        # Save report
        report_filename = f"analytics/report_{campaign_id or 'overall'}_{int(datetime.now().timestamp())}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Analytics report generated: {report_filename}")
        return report
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on campaign metrics"""
        recommendations = []
        
        success_rate = metrics.get("success_rate", 0)
        visits = metrics.get("visits", 0)
        captures = metrics.get("captures", 0)
        
        if success_rate > 30:
            recommendations.append("🚨 High success rate detected - consider additional security awareness training")
        elif success_rate > 15:
            recommendations.append("⚠️ Moderate success rate - review security policies and user education")
        else:
            recommendations.append("✅ Low success rate indicates good security awareness")
        
        if visits < 10:
            recommendations.append("📊 Low engagement - consider reviewing targeting or timing")
        
        if captures > 0:
            recommendations.append("🎯 Users fell for simulation - implement targeted training for affected individuals")
        
        return recommendations
    
    def _get_campaign_summaries(self) -> List[Dict]:
        """Get summaries of all campaigns"""
        campaigns = set(
            e.get("data", {}).get("campaign_id") 
            for e in self.events 
            if e.get("data", {}).get("campaign_id")
        )
        
        summaries = []
        for campaign_id in campaigns:
            metrics = self.get_campaign_metrics(campaign_id)
            summaries.append({
                "campaign_id": campaign_id,
                "visits": metrics["visits"],
                "captures": metrics["captures"],
                "success_rate": metrics["success_rate"],
                "unique_visitors": metrics["unique_visitors"]
            })
        
        return summaries
    
    def export_data(self, format: str = "json", campaign_id: str = None) -> str:
        """Export analytics data in various formats"""
        if campaign_id:
            data = self.get_campaign_metrics(campaign_id)
            filename = f"analytics/export_{campaign_id}_{int(datetime.now().timestamp())}.{format}"
        else:
            data = {
                "overall_metrics": self.get_overall_metrics(),
                "all_events": self.events
            }
            filename = f"analytics/export_all_{int(datetime.now().timestamp())}.{format}"
        
        if format == "json":
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        elif format == "csv":
            # Simple CSV export for events
            import csv
            with open(filename, 'w', newline='') as f:
                if self.events:
                    writer = csv.DictWriter(f, fieldnames=["timestamp", "event_type", "campaign_id", "details"])
                    writer.writeheader()
                    for event in self.events:
                        writer.writerow({
                            "timestamp": event["timestamp"],
                            "event_type": event["event_type"],
                            "campaign_id": event.get("data", {}).get("campaign_id", ""),
                            "details": json.dumps(event.get("data", {}))
                        })
        
        logger.info(f"Analytics data exported to {filename}")
        return filename
    
    def get_security_insights(self) -> Dict:
        """Generate security insights from the data"""
        insights = {
            "risk_indicators": [],
            "user_behavior": {},
            "attack_effectiveness": {},
            "recommendations": []
        }
        
        overall_metrics = self.get_overall_metrics()
        
        # Risk indicators
        if overall_metrics["overall_success_rate"] > 20:
            insights["risk_indicators"].append({
                "level": "high",
                "indicator": "High phishing susceptibility",
                "value": f"{overall_metrics['overall_success_rate']:.1f}%"
            })
        
        # User behavior analysis
        unique_visitors = overall_metrics["unique_visitors"]
        total_captures = overall_metrics["total_captures"]
        
        if unique_visitors > 0:
            repeat_victim_rate = (total_captures / unique_visitors) * 100
            insights["user_behavior"]["repeat_victim_rate"] = repeat_victim_rate
            
            if repeat_victim_rate > 150:  # More captures than unique visitors
                insights["risk_indicators"].append({
                    "level": "medium",
                    "indicator": "Repeat victims detected",
                    "value": f"{repeat_victim_rate:.1f}%"
                })
        
        # Attack effectiveness
        insights["attack_effectiveness"] = {
            "overall_success_rate": overall_metrics["overall_success_rate"],
            "total_targets_reached": overall_metrics["total_visits"],
            "conversion_rate": overall_metrics["overall_success_rate"]
        }
        
        return insights