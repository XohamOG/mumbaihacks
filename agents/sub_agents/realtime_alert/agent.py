"""
Realtime Alert Agent
Handles unsolved queries and provides real-time alerts when new information becomes available
Following ADK agent structure requirements
"""

try:
    from google.adk import Agent
except ImportError:
    # Fallback for when google.adk is not available
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from mock_adk import Agent
    except ImportError:
        class Agent:
            def __init__(self, name, model, description, instruction):
                self.name = name
                self.model = model
                self.description = description
                self.instruction = instruction

import time
import hashlib
import json
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
from datetime import datetime, timedelta
import threading
import queue


class QueryStorage:
    """Storage and management system for unsolved queries"""
    
    def __init__(self):
        self.unsolved_queries = {}
        self.query_metadata = {}
        self.query_subscribers = defaultdict(list)
        self.resolution_queue = queue.Queue()
        
    def store_unsolved_query(self, query_data: Dict[str, Any]) -> str:
        """Store an unsolved query for monitoring"""
        
        # Generate unique query ID
        query_id = self._generate_query_id(query_data)
        
        # Store query with metadata
        self.unsolved_queries[query_id] = {
            "original_content": query_data.get("content", ""),
            "content_type": query_data.get("content_type", "text"),
            "claims": query_data.get("claims", []),
            "context": query_data.get("context", {}),
            "user_id": query_data.get("user_id", ""),
            "submission_time": time.time(),
            "priority": query_data.get("priority", "medium"),
            "search_keywords": self._extract_keywords(query_data),
            "monitoring_sources": self._determine_sources(query_data),
            "status": "active"
        }
        
        # Store metadata for tracking
        self.query_metadata[query_id] = {
            "check_count": 0,
            "last_checked": time.time(),
            "alerts_sent": 0,
            "related_queries": [],
            "source_updates": []
        }
        
        return query_id
    
    def get_active_queries(self) -> Dict[str, Any]:
        """Get all active unsolved queries"""
        return {
            qid: data for qid, data in self.unsolved_queries.items()
            if data["status"] == "active"
        }
    
    def mark_query_resolved(self, query_id: str, resolution_data: Dict[str, Any]):
        """Mark a query as resolved with new information"""
        if query_id in self.unsolved_queries:
            self.unsolved_queries[query_id]["status"] = "resolved"
            self.unsolved_queries[query_id]["resolution_data"] = resolution_data
            self.unsolved_queries[query_id]["resolution_time"] = time.time()
            
            # Add to resolution queue for alert processing
            self.resolution_queue.put({
                "query_id": query_id,
                "query_data": self.unsolved_queries[query_id],
                "resolution_data": resolution_data
            })
    
    def subscribe_user(self, query_id: str, user_id: str, notification_preferences: Dict[str, Any]):
        """Subscribe a user to alerts for a specific query"""
        self.query_subscribers[query_id].append({
            "user_id": user_id,
            "preferences": notification_preferences,
            "subscribed_at": time.time()
        })
    
    def _generate_query_id(self, query_data: Dict[str, Any]) -> str:
        """Generate unique ID for a query"""
        content = query_data.get("content", "")
        timestamp = str(time.time())
        combined = f"{content}{timestamp}"
        return hashlib.md5(combined.encode()).hexdigest()[:16]
    
    def _extract_keywords(self, query_data: Dict[str, Any]) -> List[str]:
        """Extract keywords for monitoring"""
        content = query_data.get("content", "")
        claims = query_data.get("claims", [])
        
        # Extract key phrases and entities
        keywords = []
        
        # Simple keyword extraction (in real implementation, use NLP)
        words = content.lower().split()
        
        # Filter for important words (simple approach)
        important_words = [
            word for word in words 
            if len(word) > 4 and word not in ["this", "that", "with", "from", "they", "have", "will", "been"]
        ]
        
        keywords.extend(important_words[:10])  # Top 10 keywords
        
        # Add claim keywords
        for claim in claims:
            claim_words = claim.lower().split()
            keywords.extend([word for word in claim_words if len(word) > 4][:5])
        
        return list(set(keywords))  # Remove duplicates
    
    def _determine_sources(self, query_data: Dict[str, Any]) -> List[str]:
        """Determine which sources to monitor for this query"""
        content_type = query_data.get("content_type", "text")
        context = query_data.get("context", {})
        
        sources = ["news_feeds", "fact_check_sites", "government_updates"]
        
        # Add specific sources based on content
        if "health" in str(query_data).lower():
            sources.extend(["who_updates", "cdc_updates", "medical_journals"])
        
        if "politics" in str(query_data).lower():
            sources.extend(["government_sites", "election_data", "policy_updates"])
        
        if "science" in str(query_data).lower():
            sources.extend(["scientific_journals", "research_databases"])
        
        return sources


class SourceMonitor:
    """Real-time monitoring of various information sources"""
    
    def __init__(self):
        self.monitoring_active = False
        self.source_handlers = {
            "news_feeds": self._monitor_news_feeds,
            "fact_check_sites": self._monitor_fact_check_sites,
            "government_updates": self._monitor_government_updates,
            "social_media": self._monitor_social_media,
            "scientific_journals": self._monitor_scientific_sources
        }
        self.last_check_times = defaultdict(float)
        self.monitoring_thread = None
    
    def start_monitoring(self, queries: Dict[str, Any]):
        """Start continuous monitoring for active queries"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_loop, args=(queries,))
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
    
    def _monitor_loop(self, queries: Dict[str, Any]):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Check each active query
                for query_id, query_data in queries.items():
                    if query_data["status"] == "active":
                        self._check_query_sources(query_id, query_data)
                
                # Sleep between checks
                time.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)  # Wait a minute before retrying
    
    def _check_query_sources(self, query_id: str, query_data: Dict[str, Any]):
        """Check sources for updates related to a specific query"""
        keywords = query_data["search_keywords"]
        sources = query_data["monitoring_sources"]
        
        for source in sources:
            if source in self.source_handlers:
                try:
                    updates = self.source_handlers[source](keywords)
                    if updates:
                        self._process_source_updates(query_id, source, updates)
                except Exception as e:
                    print(f"Error checking {source}: {e}")
    
    def _monitor_news_feeds(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Monitor news feeds for relevant updates"""
        # Placeholder for news API integration
        # In real implementation, integrate with NewsAPI, Reuters, AP, etc.
        updates = []
        
        # Simulate finding relevant news
        for keyword in keywords[:3]:  # Check top 3 keywords
            # This would be actual API calls
            mock_update = {
                "source": "news_api",
                "title": f"Breaking: New developments regarding {keyword}",
                "content": f"Recent information about {keyword} has emerged...",
                "url": f"https://news.example.com/article/{keyword}",
                "timestamp": time.time(),
                "credibility_score": 0.8,
                "relevance_score": 0.7
            }
            
            # Only add if recent (last 24 hours in real implementation)
            if time.time() - mock_update["timestamp"] < 86400:
                updates.append(mock_update)
        
        return updates
    
    def _monitor_fact_check_sites(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Monitor fact-checking websites"""
        # Integrate with Snopes, PolitiFact, FactCheck.org, etc.
        updates = []
        
        # Placeholder implementation
        for keyword in keywords[:2]:
            mock_update = {
                "source": "fact_check_org",
                "title": f"Fact Check: Claims about {keyword}",
                "content": f"Analysis of recent claims regarding {keyword}...",
                "verdict": "partially_true",
                "url": f"https://factcheck.org/article/{keyword}",
                "timestamp": time.time(),
                "credibility_score": 0.95
            }
            updates.append(mock_update)
        
        return updates
    
    def _monitor_government_updates(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Monitor government and official sources"""
        # Integrate with government APIs, official statements, etc.
        updates = []
        
        # Placeholder for WHO, CDC, FDA, etc.
        return updates
    
    def _monitor_social_media(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Monitor social media for trending topics and corrections"""
        # Integrate with Twitter API, Facebook, etc.
        updates = []
        
        # Placeholder implementation
        return updates
    
    def _monitor_scientific_sources(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Monitor scientific journals and research databases"""
        # Integrate with PubMed, arXiv, etc.
        updates = []
        
        # Placeholder implementation
        return updates
    
    def _process_source_updates(self, query_id: str, source: str, updates: List[Dict[str, Any]]):
        """Process updates found from a source"""
        for update in updates:
            # Check relevance and credibility
            if update.get("relevance_score", 0) > 0.6 and update.get("credibility_score", 0) > 0.7:
                # This would trigger the alert system
                print(f"Relevant update found for query {query_id} from {source}: {update['title']}")


class AlertSystem:
    """System for sending alerts to users when queries are resolved"""
    
    def __init__(self):
        self.alert_queue = queue.Queue()
        self.alert_history = defaultdict(list)
        self.notification_methods = {
            "email": self._send_email_alert,
            "push": self._send_push_notification,
            "in_app": self._send_in_app_notification,
            "webhook": self._send_webhook_alert
        }
        
    def send_alert(self, query_id: str, resolution_data: Dict[str, Any], subscribers: List[Dict[str, Any]]):
        """Send alerts to all subscribers of a query"""
        
        alert_data = {
            "query_id": query_id,
            "resolution_data": resolution_data,
            "timestamp": time.time(),
            "alert_id": self._generate_alert_id(query_id)
        }
        
        for subscriber in subscribers:
            user_id = subscriber["user_id"]
            preferences = subscriber["preferences"]
            
            # Send via preferred methods
            for method in preferences.get("methods", ["in_app"]):
                if method in self.notification_methods:
                    try:
                        self.notification_methods[method](user_id, alert_data)
                        self._log_alert_sent(user_id, query_id, method)
                    except Exception as e:
                        print(f"Failed to send {method} alert to {user_id}: {e}")
    
    def _send_email_alert(self, user_id: str, alert_data: Dict[str, Any]):
        """Send email alert"""
        # Placeholder for email integration
        print(f"📧 Email alert sent to {user_id} for query {alert_data['query_id']}")
    
    def _send_push_notification(self, user_id: str, alert_data: Dict[str, Any]):
        """Send push notification"""
        # Placeholder for push notification service
        print(f"📱 Push notification sent to {user_id} for query {alert_data['query_id']}")
    
    def _send_in_app_notification(self, user_id: str, alert_data: Dict[str, Any]):
        """Send in-app notification"""
        # Placeholder for in-app notification system
        print(f"🔔 In-app notification sent to {user_id} for query {alert_data['query_id']}")
    
    def _send_webhook_alert(self, user_id: str, alert_data: Dict[str, Any]):
        """Send webhook alert"""
        # Placeholder for webhook integration
        print(f"🔗 Webhook alert sent to {user_id} for query {alert_data['query_id']}")
    
    def _generate_alert_id(self, query_id: str) -> str:
        """Generate unique alert ID"""
        timestamp = str(time.time())
        combined = f"{query_id}{timestamp}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    def _log_alert_sent(self, user_id: str, query_id: str, method: str):
        """Log that an alert was sent"""
        self.alert_history[user_id].append({
            "query_id": query_id,
            "method": method,
            "timestamp": time.time()
        })


# Initialize system components
query_storage = QueryStorage()
source_monitor = SourceMonitor()
alert_system = AlertSystem()


# Realtime alert agent for monitoring and alerting
realtime_alert_agent = Agent(
    name="realtime_alert",
    model="gemini-2.0-flash",
    description="Manages unsolved queries and provides real-time alerts when new information becomes available",
    instruction="""You are a sophisticated real-time alert and monitoring agent for a misinformation detection system.

Your primary responsibilities:

1. **Unsolved Query Management**:
   - Store and track queries that couldn't be immediately resolved
   - Categorize queries by priority and urgency
   - Extract key search terms and entities for monitoring
   - Maintain metadata about query status and progress
   - Archive resolved queries with resolution data

2. **Continuous Source Monitoring**:
   - Monitor multiple information sources in real-time
   - Track news feeds, fact-checking sites, government updates
   - Watch scientific journals and research publications
   - Monitor social media for trending corrections
   - Set up automated alerts for relevant content

3. **User Alert System**:
   - Notify users when their queries are resolved
   - Support multiple notification methods (email, push, in-app, webhook)
   - Respect user notification preferences and schedules
   - Provide detailed resolution information
   - Track alert delivery and engagement

4. **Batch Processing & Optimization**:
   - Process multiple related queries efficiently
   - Group similar queries for batch monitoring
   - Optimize source checking frequency based on urgency
   - Minimize redundant API calls and checks
   - Balance thoroughness with resource efficiency

5. **Source Tracking & Credibility**:
   - Maintain source reliability scores
   - Track which sources provide fastest updates
   - Monitor source availability and response times
   - Identify trending misinformation topics
   - Flag potential coordinated disinformation campaigns

**Monitoring Sources**:
- **News Feeds**: Reuters, AP, major news outlets, NewsAPI
- **Fact-Check Sites**: Snopes, PolitiFact, FactCheck.org, AFP Fact Check
- **Government**: WHO, CDC, FDA, government press releases
- **Academic**: PubMed, arXiv, research institutions
- **Social Media**: Twitter trends, viral content analysis
- **Specialized**: Industry-specific sources based on query content

**Query Priority Levels**:
- **Critical**: Health emergencies, public safety, elections
- **High**: Trending misinformation, breaking news claims
- **Medium**: General fact-checking requests, educational queries
- **Low**: Historical claims, non-urgent verification

**Input Format**: You will receive:
- Unsolved queries from the fact-checking agent
- User subscription requests for ongoing monitoring
- Source update notifications and webhooks
- User notification preferences and settings
- System status and monitoring health checks

**Processing Pipeline**:
1. **Query Intake**: Receive and categorize unsolved queries
2. **Keyword Extraction**: Identify monitoring terms and entities
3. **Source Selection**: Choose appropriate monitoring sources
4. **Monitoring Setup**: Configure real-time source checking
5. **Alert Processing**: Handle resolution notifications
6. **User Notification**: Send alerts via preferred methods
7. **Follow-up**: Track alert delivery and user engagement

**Output Format**: Provide comprehensive updates including:
- **Query Status**: Active monitoring status and progress
- **Source Updates**: Relevant new information found
- **Resolution Data**: Detailed fact-check results when available
- **Alert Summary**: Notifications sent and delivery status
- **Monitoring Health**: System status and source availability
- **Recommendations**: Suggested improvements or escalations

**Alert Content Structure**:
1. **Resolution Summary**: Quick overview of findings
2. **Credibility Assessment**: Source reliability and confidence level
3. **Evidence Details**: Specific facts and supporting information
4. **Source Citations**: Links and references to original sources
5. **Impact Assessment**: Significance of the new information
6. **Next Steps**: Recommended user actions

**Quality Assurance**:
- Verify source credibility before sending alerts
- Cross-reference findings with multiple sources
- Flag conflicting information for manual review
- Maintain alert accuracy and relevance standards
- Track false positive rates and user feedback

**Performance Metrics**:
- Query resolution time and success rate
- Source monitoring coverage and reliability
- Alert delivery success and user engagement
- System uptime and monitoring health
- User satisfaction with alert quality

**Guidelines**:
- Prioritize accuracy over speed in alert content
- Respect user notification preferences and quiet hours
- Provide clear, actionable information in alerts
- Maintain privacy and security in all communications
- Be transparent about confidence levels and limitations
- Continuously improve based on user feedback and system performance
- Balance comprehensive monitoring with resource efficiency

Always ensure that alerts provide genuine value to users and help combat misinformation effectively."""
)


if __name__ == "__main__":
    print("✅ Realtime Alert Agent initialized")
    print(f"Agent Name: {realtime_alert_agent.name}")
    print(f"Description: {realtime_alert_agent.description}")
    print(f"Query Storage: ✅ Active")
    print(f"Source Monitor: ✅ Ready")
    print(f"Alert System: ✅ Ready")