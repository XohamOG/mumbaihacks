# Content Intake Agent
# Processes all forms of content (video, image, audio, text) and prepares for analysis

import os
import sys
import re
import urllib.parse
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

class ContentIntakeAgent:
    """
    Content Intake Agent - Processes data in all forms and prepares it for analysis
    Handles: video, image, audio, text, URL
    """
    
    def __init__(self):
        self.name = "content_intake_agent"
        self.supported_types = ["text", "image", "video", "audio", "url", "file"]
    
    def __call__(self, input_data):
        return self.process(input_data)
    
    def process(self, input_data):
        """Process different content types and extract relevant information"""
        content = input_data.get("content")
        content_type = input_data.get("content_type", "text")
        
        try:
            if content_type == "text":
                return self.process_text(content)
            elif content_type == "image":
                return self.process_image(content)
            elif content_type == "video":
                return self.process_video(content)
            elif content_type == "audio":
                return self.process_audio(content)
            elif content_type == "url":
                return self.process_url(content)
            else:
                return self.process_unknown(content, content_type)
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "content_type": content_type,
                "timestamp": get_current_time()
            }
    
    def process_text(self, text_content):
        """Process text content"""
        if not text_content:
            return {
                "status": "error",
                "error": "No text content provided",
                "content_type": "text",
                "timestamp": get_current_time()
            }
        
        # Extract basic claims using simple patterns
        claims = self.extract_claims(text_content)
        entities = self.detect_entities(text_content)
        urgency_indicators = self.analyze_urgency(text_content)
        
        return {
            "status": "processed",
            "content_type": "text",
            "extracted_claims": claims,
            "entities": entities,
            "metadata": {
                "word_count": len(text_content.split()),
                "character_count": len(text_content),
                "language": self.detect_language(text_content),
                "urgency_indicators": urgency_indicators,
                "has_urls": bool(re.search(r'https?://\S+', text_content)),
                "has_mentions": bool(re.search(r'@\w+', text_content)),
                "has_hashtags": bool(re.search(r'#\w+', text_content))
            },
            "processed_content": text_content.strip(),
            "timestamp": get_current_time()
        }
    
    def extract_claims(self, text):
        """Extract potential factual claims from text"""
        claims = []
        sentences = re.split(r'[.!?]+', text)
        
        # Patterns that often indicate factual claims
        claim_patterns = [
            r'\d+%',  # Percentages
            r'\d+ (times|people|cases|deaths|studies)',  # Numbers with units
            r'(scientists?|researchers?|doctors?|experts?) (say|found|discovered|claim)',
            r'(study|research|report) (shows?|finds?|reveals?)',
            r'according to',
            r'(proven|confirmed|verified) (to|that)',
            r'(causes?|leads? to|results? in)'
        ]
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) > 15:  # Skip very short sentences
                claim_score = 0
                for pattern in claim_patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        claim_score += 1
                
                if claim_score > 0:
                    claims.append({
                        "text": sentence,
                        "confidence": min(claim_score / len(claim_patterns), 1.0),
                        "position": i
                    })
        
        return sorted(claims, key=lambda x: x["confidence"], reverse=True)[:5]
    
    def detect_entities(self, text):
        """Simple entity detection"""
        entities = {
            "organizations": [],
            "locations": [],
            "persons": [],
            "dates": [],
            "numbers": []
        }
        
        # Simple patterns for entity detection
        org_patterns = [
            r'\b(WHO|CDC|FDA|NASA|FBI|CIA|UN|EU|COVID-19|coronavirus)\b',
            r'\b[A-Z][a-z]+ (University|Hospital|Institute|Organization|Foundation)\b',
            r'\b(Google|Microsoft|Apple|Facebook|Twitter|Amazon)\b'
        ]
        
        location_patterns = [
            r'\b(USA|America|China|India|Europe|Asia|Africa)\b',
            r'\b[A-Z][a-z]+ (City|State|Country|Province)\b'
        ]
        
        person_patterns = [
            r'\b(Dr\.|Professor|President|Minister) [A-Z][a-z]+\b',
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'  # Simple name pattern
        ]
        
        # Extract entities
        for pattern in org_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["organizations"].extend(matches)
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["locations"].extend(matches)
        
        # Extract numbers and percentages
        numbers = re.findall(r'\d+(?:\.\d+)?%?', text)
        entities["numbers"] = numbers[:10]  # Limit to first 10
        
        # Extract dates
        dates = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b\d{4}\b', text)
        entities["dates"] = dates[:5]  # Limit to first 5
        
        return entities
    
    def analyze_urgency(self, text):
        """Analyze urgency indicators in text"""
        urgency_patterns = [
            r'\b(breaking|urgent|alert|warning|emergency|immediate)\b',
            r'\b(now|today|asap|quickly|fast|hurry)\b',
            r'\b(crisis|disaster|catastrophe|panic)\b',
            r'!!+',  # Multiple exclamation marks
            r'\bALL CAPS\b',
            r'\b(must|need to|have to) (know|see|share|act)\b'
        ]
        
        indicators = []
        urgency_score = 0
        
        for pattern in urgency_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                indicators.append(pattern)
                urgency_score += len(matches)
        
        # Check for excessive capitalization
        if text.isupper() and len(text) > 20:
            indicators.append("ALL_CAPS_TEXT")
            urgency_score += 2
        
        return {
            "score": min(urgency_score / 10, 1.0),  # Normalize to 0-1
            "indicators": indicators,
            "level": "high" if urgency_score > 3 else "medium" if urgency_score > 1 else "low"
        }
    
    def detect_language(self, text):
        """Simple language detection (placeholder)"""
        # This is a very basic implementation
        # In production, you'd use a proper language detection library
        
        english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        text_lower = text.lower()
        english_count = sum(1 for word in english_words if word in text_lower)
        
        if english_count >= 3:
            return "en"
        else:
            return "unknown"

    def process_image(self, image_content):
        """Process image content (simulated)"""
        # In production, this would use OCR and image analysis APIs
        return {
            "status": "processed",
            "content_type": "image",
            "extracted_text": "Simulated OCR text extraction would go here",
            "objects_detected": ["person", "text", "logo"],
            "metadata": {
                "format": "jpg",
                "size": "1024x768",
                "has_text": True,
                "confidence": 0.85
            },
            "processed_content": f"Image analysis completed for: {str(image_content)[:50]}...",
            "timestamp": get_current_time()
        }
    
    def process_video(self, video_content):
        """Process video content (simulated)"""
        # In production, this would use video analysis APIs
        return {
            "status": "processed",
            "content_type": "video",
            "transcript": "Simulated video transcript would appear here",
            "key_frames": ["frame_1.jpg", "frame_2.jpg", "frame_3.jpg"],
            "metadata": {
                "duration": "2:30",
                "format": "mp4",
                "quality": "720p",
                "has_audio": True
            },
            "processed_content": f"Video analysis completed for: {str(video_content)[:50]}...",
            "timestamp": get_current_time()
        }
    
    def process_audio(self, audio_content):
        """Process audio content (simulated)"""
        # In production, this would use speech-to-text APIs
        return {
            "status": "processed",
            "content_type": "audio",
            "transcript": "Simulated audio transcript would appear here",
            "speakers": ["speaker_1", "speaker_2"],
            "metadata": {
                "duration": "1:45",
                "format": "mp3",
                "quality": "high",
                "language": "en"
            },
            "processed_content": f"Audio analysis completed for: {str(audio_content)[:50]}...",
            "timestamp": get_current_time()
        }
    
    def process_url(self, url_content):
        """Process URL content"""
        if not url_content:
            return {
                "status": "error",
                "error": "No URL provided",
                "content_type": "url",
                "timestamp": get_current_time()
            }
        
        # Parse URL
        try:
            parsed = urllib.parse.urlparse(url_content)
            domain = parsed.netloc.lower()
            
            # Analyze domain credibility
            trusted_domains = [
                "reuters.com", "ap.org", "bbc.com", "npr.org", "pbs.org",
                "who.int", "cdc.gov", "fda.gov", "nih.gov", "gov.uk"
            ]
            
            suspicious_domains = [
                "naturalnews.com", "infowars.com", "beforeitsnews.com"
            ]
            
            credibility = "unknown"
            if any(trusted in domain for trusted in trusted_domains):
                credibility = "high"
            elif any(suspicious in domain for suspicious in suspicious_domains):
                credibility = "low"
            elif domain.endswith(".gov") or domain.endswith(".edu"):
                credibility = "high"
            
            return {
                "status": "processed",
                "content_type": "url",
                "url": url_content,
                "domain": domain,
                "credibility": credibility,
                "metadata": {
                    "scheme": parsed.scheme,
                    "path": parsed.path,
                    "has_parameters": bool(parsed.query),
                    "is_secure": parsed.scheme == "https"
                },
                "processed_content": f"URL analysis completed for: {domain}",
                "timestamp": get_current_time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Invalid URL format: {str(e)}",
                "content_type": "url",
                "timestamp": get_current_time()
            }
    
    def process_unknown(self, content, content_type):
        """Handle unknown content types"""
        return {
            "status": "unsupported_content_type",
            "content_type": content_type,
            "supported_types": self.supported_types,
            "message": f"Content type '{content_type}' not yet supported",
            "processed_content": str(content)[:100] + "..." if content else "No content",
            "timestamp": get_current_time()
        }

# Example usage
if __name__ == "__main__":
    agent = ContentIntakeAgent()
    
    # Test with text content
    result = agent({
        "content": "Breaking news: Scientists discover new cure!",
        "content_type": "text"
    })
    
    print("Content Intake Result:")
    print(result)
