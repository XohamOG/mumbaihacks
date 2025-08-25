# Common tools for Content Intake Agent

import datetime

def get_current_time():
    """Get current timestamp"""
    return datetime.datetime.now().isoformat()

def validate_input(content, content_type):
    """Validate input content and type"""
    if not content:
        return False, "Content cannot be empty"
    
    supported_types = ["text", "image", "video", "audio", "url", "file"]
    if content_type not in supported_types:
        return False, f"Unsupported content type: {content_type}"
    
    return True, "Valid input"

def sanitize_content(content):
    """Sanitize content for processing"""
    if isinstance(content, str):
        # Remove excessive whitespace, special characters
        import re
        content = re.sub(r'\s+', ' ', content).strip()
    
    return content
