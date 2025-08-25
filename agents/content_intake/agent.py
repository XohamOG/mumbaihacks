# Content Intake Agent
# Processes all forms of content (video, image, audio, text) and prepares for analysis

import os
import sys
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

class ContentIntakeAgent:
    """
    Content Intake Agent - Processes data in all forms and prepares it for analysis
    Handles: video, image, audio, text
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
                "content_type": content_type
            }
    
    def process_text(self, text_content):
        """Process text content"""
        from tools.text_processor import extract_claims, detect_entities, analyze_urgency
        
        return {
            "status": "processed",
            "content_type": "text",
            "extracted_claims": extract_claims(text_content),
            "entities": detect_entities(text_content),
            "metadata": {
                "word_count": len(text_content.split()) if text_content else 0,
                "language": "unknown",  # To be implemented with language detection
                "urgency_indicators": analyze_urgency(text_content)
            },
            "processed_content": text_content,
            "timestamp": get_current_time()
        }
    
    def process_image(self, image_content):
        """Process image content"""
        from tools.image_processor import extract_text_ocr, detect_objects, extract_metadata
        
        return {
            "status": "processed",
            "content_type": "image",
            "extracted_text": extract_text_ocr(image_content),
            "objects_detected": detect_objects(image_content),
            "metadata": extract_metadata(image_content),
            "processed_content": "Image processing completed",
            "timestamp": get_current_time()
        }
    
    def process_video(self, video_content):
        """Process video content"""
        from tools.video_processor import extract_transcript, analyze_frames, extract_metadata
        
        return {
            "status": "processed",
            "content_type": "video",
            "transcript": extract_transcript(video_content),
            "key_frames": analyze_frames(video_content),
            "metadata": extract_metadata(video_content),
            "processed_content": "Video processing completed",
            "timestamp": get_current_time()
        }
    
    def process_audio(self, audio_content):
        """Process audio content"""
        from tools.audio_processor import speech_to_text, identify_speakers, analyze_quality
        
        return {
            "status": "processed",
            "content_type": "audio",
            "transcript": speech_to_text(audio_content),
            "speakers": identify_speakers(audio_content),
            "metadata": analyze_quality(audio_content),
            "processed_content": "Audio processing completed",
            "timestamp": get_current_time()
        }
    
    def process_url(self, url_content):
        """Process URL content"""
        from tools.url_processor import fetch_webpage, analyze_domain, extract_metadata
        
        return {
            "status": "processed",
            "content_type": "url",
            "webpage_content": fetch_webpage(url_content),
            "domain": analyze_domain(url_content),
            "metadata": extract_metadata(url_content),
            "processed_content": "URL processing completed",
            "timestamp": get_current_time()
        }
    
    def process_unknown(self, content, content_type):
        """Handle unknown content types"""
        return {
            "status": "unsupported_content_type",
            "content_type": content_type,
            "supported_types": self.supported_types,
            "message": f"Content type '{content_type}' not yet supported",
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
