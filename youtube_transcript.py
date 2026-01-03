from typing import Optional, List
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import random
import os
import requests
from unittest.mock import patch

# Webshare proxy configuration
# Can be overridden via environment variables
WEBSHARE_PROXIES = [
    "142.111.48.253:7030",
    "23.95.150.145:6114",
    "198.23.239.134:6540",
    "107.172.163.27:6543",
    "198.105.121.200:6462",
    "64.137.96.74:6641",
    "84.247.60.125:6095",
    "216.10.27.159:6837",
    "23.26.71.145:5628",
    "23.27.208.120:5830",
]

PROXY_USERNAME = os.getenv("WEBSHARE_USERNAME", "edicnojj")
PROXY_PASSWORD = os.getenv("WEBSHARE_PASSWORD", "0t1i5oy4lbfy")

# Load proxies from environment if provided (comma-separated list)
if os.getenv("WEBSHARE_PROXIES"):
    WEBSHARE_PROXIES = [p.strip() for p in os.getenv("WEBSHARE_PROXIES").split(",") if p.strip()]


def get_random_proxy() -> Optional[dict]:
    """Get a random proxy from the list. Returns None if no proxies available."""
    if not WEBSHARE_PROXIES:
        return None
    
    proxy_ip_port = random.choice(WEBSHARE_PROXIES)
    proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{proxy_ip_port}"
    return {
        "http": proxy_url,
        "https": proxy_url,
    }


def fetch_transcript_text(video_id: str, language_codes: List[str] = ["en"]) -> Optional[str]:
    """
    Fetches YouTube video transcript as plain text using proxy rotation.
    
    Tries specified languages, falls back to auto-generated if available.
    Returns plain text transcript or None if not available.
    Uses proxy rotation to bypass IP blocking from cloud providers.
    """
    # Try with proxy first, fallback to no proxy if all proxies fail
    max_proxy_attempts = 3
    proxies_used = []
    
    # Store original requests methods for restoration
    original_get = requests.get
    original_session_request = requests.Session.request
    
    for attempt in range(max_proxy_attempts):
        try:
            # Get a random proxy for this attempt (avoid reusing failed ones)
            available_proxies = [p for p in WEBSHARE_PROXIES if p not in proxies_used]
            if not available_proxies:
                available_proxies = WEBSHARE_PROXIES  # Reset if all tried
                proxies_used = []
            
            proxy_ip_port = random.choice(available_proxies)
            proxies_used.append(proxy_ip_port)
            
            # Create proxy URL with authentication
            proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{proxy_ip_port}"
            
            # Test proxy connectivity first
            try:
                test_response = requests.get(
                    "https://httpbin.org/ip",
                    proxies={"http": proxy_url, "https": proxy_url},
                    timeout=5
                )
                proxy_ip = test_response.json().get('origin', 'unknown')
                print(f"✓ Proxy {proxy_ip_port} is working, IP: {proxy_ip}")
            except Exception as proxy_test_error:
                print(f"⚠️ Proxy {proxy_ip_port} test failed: {str(proxy_test_error)[:100]}")
                # Continue anyway - might still work for YouTube
            
            # Set proxy environment variables
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url
            os.environ['http_proxy'] = proxy_url
            os.environ['https_proxy'] = proxy_url
            
            # Monkey-patch requests.get to ensure proxy is used
            # The youtube-transcript-api library uses requests internally
            def proxied_get(url, **kwargs):
                if 'proxies' not in kwargs:
                    kwargs['proxies'] = {"http": proxy_url, "https": proxy_url}
                return original_get(url, **kwargs)
            
            def proxied_session_request(self, method, url, **kwargs):
                if 'proxies' not in kwargs:
                    kwargs['proxies'] = {"http": proxy_url, "https": proxy_url}
                return original_session_request(self, method, url, **kwargs)
            
            # Patch requests
            requests.get = proxied_get
            requests.Session.request = proxied_session_request
            
            # Create API instance - it will use the proxy
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
                # Clear proxy env vars before returning
                os.environ.pop('HTTP_PROXY', None)
                os.environ.pop('HTTPS_PROXY', None)
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
            
            # Restore original requests methods
            requests.get = original_get
            requests.Session.request = original_session_request
            
            # Clear proxy env vars after successful fetch
            os.environ.pop('HTTP_PROXY', None)
            os.environ.pop('HTTPS_PROXY', None)
            os.environ.pop('http_proxy', None)
            os.environ.pop('https_proxy', None)
            
            print(f"✓ Successfully fetched transcript for {video_id} using proxy {proxy_ip_port}")
            return transcript_text
        
        except Exception as e:
            # Restore original requests methods on error
            try:
                requests.get = original_get
                requests.Session.request = original_session_request
            except:
                pass
            
            # Clear proxy env vars on error
            os.environ.pop('HTTP_PROXY', None)
            os.environ.pop('HTTPS_PROXY', None)
            os.environ.pop('http_proxy', None)
            os.environ.pop('https_proxy', None)
            
            error_type = type(e).__name__
            error_message = str(e)
            
            # If it's a blocking error and we have more attempts, try next proxy
            if error_type in ['IpBlocked', 'RequestBlocked'] and attempt < max_proxy_attempts - 1:
                print(f"⚠️ Proxy {proxy_ip_port} blocked for {video_id}, trying next proxy... (attempt {attempt + 1}/{max_proxy_attempts})")
                continue
            
            # Log IP block/request block errors
            if error_type in ['IpBlocked', 'RequestBlocked']:
                print(f"⚠️ BLOCKED: YouTube is blocking transcript requests for {video_id}")
                print(f"   Error Type: {error_type}")
                print(f"   Proxy used: {proxy_ip_port}")
                print(f"   Message: {error_message[:200]}...")
                if attempt == max_proxy_attempts - 1:
                    print(f"   All {max_proxy_attempts} proxy attempts failed")
                    print(f"   NOTE: These proxies may be datacenter IPs which YouTube blocks.")
                    print(f"   Consider using residential proxies or a third-party transcript API.")
                return "__BLOCKED__"
            # Only log other errors if they're not common "no transcript" errors
            elif error_type not in ['NoTranscriptFound', 'TranscriptsDisabled', 'VideoUnavailable']:
                print(f"❌ Transcript error for {video_id}: {error_type} - {error_message[:200]}")
                # If it's not a blocking error, don't retry with other proxies
                break
            
            # If all proxy attempts failed, return None
            if attempt == max_proxy_attempts - 1:
                return None
    
    # Restore original requests methods if we exit the loop
    try:
        requests.get = original_get
        requests.Session.request = original_session_request
    except:
        pass
    
    # If we exhausted all attempts, return None
    return None

