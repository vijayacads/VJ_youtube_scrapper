from typing import Optional, List
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


def fetch_transcript_text(video_id: str, language_codes: List[str] = ["en"]) -> Optional[str]:
    """
    Fetches YouTube video transcript as plain text.
    
    Tries specified languages, falls back to auto-generated if available.
    Returns plain text transcript or None if not available.
    """
    try:
        # Create API instance and get list of available transcripts
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        transcript = None
        
        # Try to find transcript in preferred languages
        for lang_code in language_codes:
            try:
                transcript = transcript_list.find_transcript([lang_code])
                break
            except:
                continue
        
        # If no preferred language found, try auto-generated
        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(language_codes)
            except:
                pass
        
        # If still no transcript, try to get any available transcript
        if transcript is None:
            try:
                available = list(transcript_list)
                if available:
                    transcript = available[0]
            except:
                pass
        
        if transcript is None:
            return None
        
        # Fetch the actual transcript data
        transcript_data = transcript.fetch()
        
        # Format to plain text using TextFormatter
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript_data)
        
        # Clean up the text: remove newlines, backslashes, and extra whitespace
        import re
        # First, remove all backslashes (this handles escaped characters)
        transcript_text = transcript_text.replace('\\', '')
        # Then replace any remaining newlines with spaces
        transcript_text = transcript_text.replace('\n', ' ')
        transcript_text = transcript_text.replace('\r', ' ')
        # Replace multiple spaces with single space
        transcript_text = re.sub(r'\s+', ' ', transcript_text)
        # Strip leading/trailing whitespace
        transcript_text = transcript_text.strip()
        
        return transcript_text
    
    except Exception as e:
        # Log the error for debugging but return None
        # Common errors: NoTranscriptFound, TranscriptsDisabled, VideoUnavailable, IpBlocked, RequestBlocked
        error_type = type(e).__name__
        error_message = str(e)
        
        # Log IP block/request block errors as they're important to know about
        if error_type in ['IpBlocked', 'RequestBlocked']:
            print(f"⚠️ BLOCKED: YouTube is blocking transcript requests for {video_id}")
            print(f"   Error Type: {error_type}")
            print(f"   Message: {error_message[:200]}...")  # Truncate long messages
            print(f"   This usually happens when running on cloud providers (Render, AWS, etc.)")
            # Return a special marker to indicate it was blocked (not just unavailable)
            return "__BLOCKED__"
        # Only log other errors if they're not common "no transcript" errors
        elif error_type not in ['NoTranscriptFound', 'TranscriptsDisabled', 'VideoUnavailable']:
            print(f"❌ Transcript error for {video_id}: {error_type} - {error_message[:200]}")
        return None

