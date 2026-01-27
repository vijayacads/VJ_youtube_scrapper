from typing import Optional
from urllib.parse import urlparse, parse_qs


def extract_video_id(input_str: str) -> Optional[str]:
    """
    Extracts YouTube video ID from various input formats.
    
    Accepts:
        - full YouTube URLs: https://www.youtube.com/watch?v=VIDEO_ID
        - short URLs: https://youtu.be/VIDEO_ID
        - bare video IDs: VIDEO_ID
    
    Returns video ID or None if invalid.
    """
    if not input_str or not input_str.strip():
        return None
    
    input_str = input_str.strip()
    
    # If it's already a bare ID (simple check: no slashes, no query params)
    if '/' not in input_str and '?' not in input_str and '=' not in input_str:
        # Basic validation: YouTube IDs are typically 11 characters
        if len(input_str) == 11:
            return input_str
    
    # Try parsing as URL
    try:
        parsed = urlparse(input_str)
        
        # Handle youtu.be short URLs
        if parsed.netloc in ('youtu.be', 'www.youtu.be'):
            video_id = parsed.path.lstrip('/')
            if video_id:
                return video_id.split('?')[0]  # Remove any query params
        
        # Handle full youtube.com URLs
        if parsed.netloc in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
            if parsed.path == '/watch':
                query_params = parse_qs(parsed.query)
                if 'v' in query_params:
                    return query_params['v'][0]
            # Handle /embed/VIDEO_ID format
            elif parsed.path.startswith('/embed/'):
                return parsed.path.split('/embed/')[1].split('?')[0]
            # Handle /v/VIDEO_ID format
            elif parsed.path.startswith('/v/'):
                return parsed.path.split('/v/')[1].split('?')[0]
    
    except Exception:
        pass
    
    return None


def extract_channel_id(input_str: str) -> Optional[str]:
    """
    Extracts YouTube channel ID from various input formats.
    
    Accepts:
        - Channel URL: https://www.youtube.com/channel/CHANNEL_ID
        - User URL: https://www.youtube.com/@username
        - Custom URL: https://www.youtube.com/c/username
        - Bare channel ID: CHANNEL_ID
    
    Returns channel ID or None if invalid.
    Note: For @username and /c/username formats, returns the username part.
    The actual channel ID lookup requires YouTube API call.
    """
    if not input_str or not input_str.strip():
        return None
    
    input_str = input_str.strip()
    
    # If it's already a bare channel ID (starts with UC, HC, or similar)
    if '/' not in input_str and '?' not in input_str and '=' not in input_str and '@' not in input_str:
        # YouTube channel IDs typically start with UC (user channel) or HC (handle channel)
        if input_str.startswith('UC') and len(input_str) == 24:
            return input_str
    
    # Try parsing as URL
    try:
        parsed = urlparse(input_str)
        
        # Handle youtube.com URLs
        if parsed.netloc in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
            path = parsed.path.strip('/')
            
            # Handle /channel/CHANNEL_ID format
            if path.startswith('channel/'):
                channel_id = path.split('channel/')[1].split('/')[0]
                return channel_id
            
            # Handle /@username format
            elif path.startswith('@'):
                username = path.split('@')[1].split('/')[0]
                return f"@{username}"  # Return with @ prefix for identification
            
            # Handle /c/username or /user/username format
            elif path.startswith('c/') or path.startswith('user/'):
                parts = path.split('/')
                if len(parts) >= 2:
                    username = parts[1]
                    return f"c/{username}"  # Return with prefix for identification
    
    except Exception:
        pass
    
    return None

