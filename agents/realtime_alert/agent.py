# Realtime Alert Agent
# Role: Monitor unsolved queries and send alerts when resolved

from datetime import datetime, timedelta
import re
import hashlib

def get_current_time():
    return datetime.now().isoformat()

class RealtimeAlertAgent:
    """
    Realtime Alert Agent
    Role: Monitor unsolved queries and send alerts when they're resolved
    """
    
    def __init__(self):
        self.name = "realtime_alert_agent"
        self.pending_queries = {}  # Store unsolved queries
        self.alert_history = {}    # Track alert history
        self.notification_channels = {
            "email": True,
            "sms": False,
            "push": True,
            "webhook": False
        }
        
        # Alert priority thresholds
        self.priority_thresholds = {
            "critical": {
                "viral_content": True,
                "health_misinformation": True,
                "election_content": True,
                "urgent_keywords": ["breaking", "urgent", "alert", "emergency", "vaccine", "election"]
            },
            "high": {
                "public_figure_mentions": True,
                "high_engagement": 1000,  # shares/views threshold
                "sensitive_topics": ["politics", "health", "finance", "covid"]
            },
            "medium": {
                "general_misinformation": True,
                "pending_time_threshold": 24  # hours
            }
        }
        
        # Resolution patterns to check against new content
        self.resolution_patterns = [
            r"fact.?check",
            r"debunk",
            r"false.?claim",
            r"misinformation",
            r"correction",
            r"update",
            r"clarification"
        ]
        
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Main alert processing with comprehensive monitoring"""
        action = input_data.get("action", "monitor")
        
        try:
            if action == "store_unsolved":
                return self.store_unsolved_query(input_data)
            elif action == "check_resolved":
                return self.check_and_alert_resolved(input_data)
            elif action == "create_alert":
                return self.create_alert(input_data)
            elif action == "get_pending":
                return self.get_pending_queries(input_data)
            elif action == "update_status":
                return self.update_query_status(input_data)
            else:
                return self.monitor_queries(input_data)
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": get_current_time()
            }
    
    def store_unsolved_query(self, input_data):
        """Store query that couldn't be resolved with enhanced metadata"""
        query_id = input_data.get("query_id", self.generate_query_id(input_data))
        user_id = input_data.get("user_id", "anonymous")
        content = input_data.get("content", "")
        content_type = input_data.get("content_type", "text")
        urgency_level = input_data.get("urgency_level", "medium")
        
        # Calculate priority based on content analysis
        priority = self.calculate_priority(content, content_type, urgency_level)
        
        # Extract key metadata
        metadata = self.extract_content_metadata(content, content_type)
        
        self.pending_queries[query_id] = {
            "user_id": user_id,
            "content": content,
            "content_type": content_type,
            "priority": priority,
            "urgency_level": urgency_level,
            "metadata": metadata,
            "stored_at": get_current_time(),
            "status": "pending",
            "attempts": 0,
            "last_check": None,
            "notification_sent": False
        }
        
        # If critical priority, create immediate alert
        if priority == "critical":
            alert_result = self.create_immediate_alert(query_id, content, metadata)
            return {
                "status": "stored_with_alert",
                "query_id": query_id,
                "priority": priority,
                "alert_created": alert_result["alert_id"],
                "message": f"Critical query stored and alert created",
                "timestamp": get_current_time()
            }
        
        return {
            "status": "stored",
            "query_id": query_id,
            "priority": priority,
            "message": f"Query stored for monitoring with {priority} priority",
            "estimated_resolution_time": self.estimate_resolution_time(priority),
            "timestamp": get_current_time()
        }
    
    def calculate_priority(self, content, content_type, urgency_level):
        """Calculate priority level based on content analysis"""
        content_lower = content.lower()
        
        # Critical priority checks
        critical_thresholds = self.priority_thresholds["critical"]
        
        # Check for urgent keywords
        for keyword in critical_thresholds["urgent_keywords"]:
            if keyword in content_lower:
                return "critical"
        
        # Check content patterns
        if any(pattern in content_lower for pattern in ["health", "vaccine", "election", "virus"]):
            if any(indicator in content_lower for indicator in ["false", "fake", "hoax", "conspiracy"]):
                return "critical"
        
        # High priority checks  
        high_thresholds = self.priority_thresholds["high"]
        if any(topic in content_lower for topic in high_thresholds["sensitive_topics"]):
            return "high"
        
        # Use provided urgency level as baseline
        if urgency_level == "high":
            return "high"
        elif urgency_level == "low":
            return "medium"
        
        return urgency_level
    
    def extract_content_metadata(self, content, content_type):
        """Extract relevant metadata from content for monitoring"""
        metadata = {
            "word_count": len(content.split()) if content else 0,
            "char_count": len(content),
            "content_type": content_type,
            "contains_urls": bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)),
            "language_detected": "en",  # Simplified - in production would use language detection
            "extracted_at": get_current_time()
        }
        
        # Extract potential entities or keywords
        if content:
            # Simple keyword extraction
            keywords = []
            common_misinformation_terms = ["vaccine", "election", "covid", "5g", "conspiracy", "fake", "hoax"]
            for term in common_misinformation_terms:
                if term in content.lower():
                    keywords.append(term)
            metadata["keywords"] = keywords
        
        return metadata
    
    def check_and_alert_resolved(self, input_data):
        """Check if any pending queries can now be resolved and send alerts"""
        new_content = input_data.get("new_content", "")
        resolved_queries = []
        alerts_created = []
        
        # Check each pending query against new content
        for query_id, query_data in list(self.pending_queries.items()):
            if query_data["status"] != "pending":
                continue
            
            # Check if new content might resolve this query
            resolution_score = self.calculate_resolution_score(
                query_data["content"], 
                new_content, 
                query_data["metadata"]
            )
            
            if resolution_score > 0.7:  # High confidence threshold
                # Mark as potentially resolved
                query_data["status"] = "potentially_resolved"
                query_data["resolution_content"] = new_content
                query_data["resolution_score"] = resolution_score
                query_data["resolved_at"] = get_current_time()
                
                # Create alert for user
                alert = self.create_resolution_alert(query_id, query_data, new_content)
                alerts_created.append(alert)
                resolved_queries.append(query_id)
        
        return {
            "status": "checked",
            "queries_checked": len(self.pending_queries),
            "potentially_resolved": len(resolved_queries),
            "alerts_created": len(alerts_created),
            "resolved_query_ids": resolved_queries,
            "alert_details": alerts_created,
            "timestamp": get_current_time()
        }
    
    def calculate_resolution_score(self, original_content, new_content, metadata):
        """Calculate how likely the new content resolves the original query"""
        if not new_content or not original_content:
            return 0.0
        
        score = 0.0
        original_lower = original_content.lower()
        new_lower = new_content.lower()
        
        # Check for resolution patterns in new content
        resolution_matches = 0
        for pattern in self.resolution_patterns:
            if re.search(pattern, new_lower):
                resolution_matches += 1
        
        if resolution_matches > 0:
            score += 0.3
        
        # Check for keyword overlap
        original_keywords = set(metadata.get("keywords", []))
        new_keywords = set()
        common_terms = ["vaccine", "election", "covid", "5g", "conspiracy", "fake", "hoax"]
        for term in common_terms:
            if term in new_lower:
                new_keywords.add(term)
        
        keyword_overlap = len(original_keywords.intersection(new_keywords))
        if keyword_overlap > 0:
            score += min(keyword_overlap * 0.2, 0.4)
        
        # Check for direct content similarity (simplified)
        original_words = set(original_lower.split())
        new_words = set(new_lower.split())
        
        if len(original_words) > 0:
            word_overlap = len(original_words.intersection(new_words)) / len(original_words)
            score += min(word_overlap, 0.3)
        
        return min(score, 1.0)
    
    def create_resolution_alert(self, query_id, query_data, new_content):
        """Create alert when a query is potentially resolved"""
        alert_id = self.generate_alert_id(query_id)
        
        alert = {
            "alert_id": alert_id,
            "type": "query_resolved",
            "query_id": query_id,
            "user_id": query_data["user_id"],
            "priority": query_data["priority"],
            "original_content": query_data["content"][:200] + "..." if len(query_data["content"]) > 200 else query_data["content"],
            "resolution_content": new_content[:200] + "..." if len(new_content) > 200 else new_content,
            "resolution_score": query_data.get("resolution_score", 0.0),
            "message": f"Your misinformation query may have been resolved. New information is available.",
            "action_required": "Please review the new information to confirm if your question has been answered.",
            "created_at": get_current_time()
        }
        
        # Store in alert history
        self.alert_history[alert_id] = alert
        
        # Mark notification as sent
        query_data["notification_sent"] = True
        query_data["alert_id"] = alert_id
        
        return alert
    
    def create_immediate_alert(self, query_id, content, metadata):
        """Create immediate alert for critical queries"""
        alert_id = self.generate_alert_id(query_id, "critical")
        
        alert = {
            "alert_id": alert_id,
            "type": "critical_query",
            "query_id": query_id,
            "priority": "critical",
            "content_preview": content[:150] + "..." if len(content) > 150 else content,
            "keywords": metadata.get("keywords", []),
            "message": "Critical misinformation query detected and is being prioritized for fact-checking.",
            "estimated_response_time": "Within 2 hours",
            "created_at": get_current_time()
        }
        
        self.alert_history[alert_id] = alert
        return alert
    
    def create_alert(self, input_data):
        """Create custom alert based on input data"""
        alert_type = input_data.get("alert_type", "general")
        message = input_data.get("message", "New alert created")
        priority = input_data.get("priority", "medium")
        
        alert_id = f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{priority.upper()}"
        
        alert = {
            "alert_id": alert_id,
            "type": alert_type,
            "priority": priority,
            "message": message,
            "created_at": get_current_time(),
            "channels": self.get_notification_channels(priority)
        }
        
        self.alert_history[alert_id] = alert
        
        return {
            "status": "alert_created",
            "alert_id": alert_id,
            "alert": alert,
            "timestamp": get_current_time()
        }
    
    def get_pending_queries(self, input_data):
        """Get list of pending queries with filtering options"""
        priority_filter = input_data.get("priority_filter")
        user_filter = input_data.get("user_filter")
        status_filter = input_data.get("status_filter", "pending")
        
        filtered_queries = {}
        for query_id, query_data in self.pending_queries.items():
            include_query = True
            
            if priority_filter and query_data["priority"] != priority_filter:
                include_query = False
            if user_filter and query_data["user_id"] != user_filter:
                include_query = False
            if status_filter and query_data["status"] != status_filter:
                include_query = False
            
            if include_query:
                # Don't include full content in summary
                summary_data = query_data.copy()
                summary_data["content"] = query_data["content"][:100] + "..." if len(query_data["content"]) > 100 else query_data["content"]
                filtered_queries[query_id] = summary_data
        
        return {
            "status": "success",
            "total_pending": len(self.pending_queries),
            "filtered_count": len(filtered_queries),
            "queries": filtered_queries,
            "timestamp": get_current_time()
        }
    
    def update_query_status(self, input_data):
        """Update the status of a query"""
        query_id = input_data.get("query_id")
        new_status = input_data.get("status", "pending")
        
        if query_id not in self.pending_queries:
            return {
                "status": "error",
                "message": "Query ID not found",
                "timestamp": get_current_time()
            }
        
        old_status = self.pending_queries[query_id]["status"]
        self.pending_queries[query_id]["status"] = new_status
        self.pending_queries[query_id]["last_updated"] = get_current_time()
        
        return {
            "status": "updated",
            "query_id": query_id,
            "old_status": old_status,
            "new_status": new_status,
            "timestamp": get_current_time()
        }
    
    def monitor_queries(self, input_data):
        """Monitor and return comprehensive status of all queries"""
        # Calculate statistics
        stats = {
            "total_queries": len(self.pending_queries),
            "by_status": {},
            "by_priority": {},
            "overdue_queries": []
        }
        
        current_time = datetime.now()
        
        for query_id, query_data in self.pending_queries.items():
            # Count by status
            status = query_data["status"]
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            # Count by priority
            priority = query_data["priority"]
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
            
            # Check for overdue queries
            stored_time = datetime.fromisoformat(query_data["stored_at"].replace('Z', '+00:00').replace('+00:00', ''))
            hours_pending = (current_time - stored_time).total_seconds() / 3600
            
            overdue_threshold = {
                "critical": 2,
                "high": 24,
                "medium": 72
            }.get(priority, 72)
            
            if hours_pending > overdue_threshold:
                stats["overdue_queries"].append({
                    "query_id": query_id,
                    "priority": priority,
                    "hours_pending": round(hours_pending, 1)
                })
        
        return {
            "status": "monitoring",
            "statistics": stats,
            "alert_history_count": len(self.alert_history),
            "active_channels": [channel for channel, active in self.notification_channels.items() if active],
            "timestamp": get_current_time()
        }
    
    def estimate_resolution_time(self, priority):
        """Estimate resolution time based on priority"""
        estimates = {
            "critical": "2-4 hours",
            "high": "4-24 hours", 
            "medium": "1-3 days",
            "low": "3-7 days"
        }
        return estimates.get(priority, "3-7 days")
    
    def get_notification_channels(self, priority):
        """Get appropriate notification channels based on priority"""
        if priority == "critical":
            return ["email", "sms", "push", "webhook"]
        elif priority == "high":
            return ["email", "push"]
        else:
            return ["email"]
    
    def generate_query_id(self, input_data):
        """Generate unique query ID"""
        user_id = input_data.get("user_id", "anonymous")
        content = input_data.get("content", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create hash from user and content
        hash_input = f"{user_id}_{content[:100]}_{timestamp}"
        query_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        
        return f"QUERY_{timestamp}_{query_hash}"
    
    def generate_alert_id(self, query_id, alert_type="standard"):
        """Generate unique alert ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        alert_hash = hashlib.md5(f"{query_id}_{alert_type}_{timestamp}".encode()).hexdigest()[:6]
        
        return f"ALERT_{timestamp}_{alert_hash}"
