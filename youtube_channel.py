import os
from typing import List, Optional
import httpx
from youtube_id import extract_channel_id


YOUTUBE_SEARCH_API_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_CHANNELS_API_URL = "https://www.googleapis.com/youtube/v3/channels"


def get_youtube_api_key() -> str:
    """Get YouTube API key from environment variable."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set")
    return api_key


async def resolve_channel_id(channel_input: str) -> Optional[str]:
    """
    Resolves channel ID from various input formats.
    For @username and /c/username, makes API call to get actual channel ID.
    """
    channel_id = extract_channel_id(channel_input)
    
    if not channel_id:
        return None
    
    # If it's already a channel ID (starts with UC), return it
    if channel_id.startswith('UC') and len(channel_id) == 24:
        return channel_id
    
    # If it's @username or c/username, need to resolve via API
    api_key = get_youtube_api_key()
    
    # Extract username from @username or c/username
    if channel_id.startswith('@'):
        username = channel_id[1:]  # Remove @
        for_username = username
    elif channel_id.startswith('c/'):
        username = channel_id[2:]  # Remove c/
        for_username = username
    else:
        return channel_id  # Already a channel ID
    
    # Try to get channel ID via channels.list with forUsername
    params = {
        "part": "id",
        "forUsername": for_username,
        "key": get_youtube_api_key()
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(YOUTUBE_CHANNELS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data and len(data["items"]) > 0:
                return data["items"][0]["id"]
        except:
            pass
    
    # If forUsername doesn't work, try search.list as fallback
    # Search for channel by handle
    search_params = {
        "part": "snippet",
        "q": username,
        "type": "channel",
        "maxResults": 1,
        "key": get_youtube_api_key()
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(YOUTUBE_SEARCH_API_URL, params=search_params)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data and len(data["items"]) > 0:
                return data["items"][0]["id"]["channelId"]
        except:
            pass
    
    # Return original input as last resort
    return channel_id


async def get_channel_title(channel_id: str) -> str:
    """
    Gets channel title from channel ID.
    """
    try:
        api_key = get_youtube_api_key()
    except ValueError:
        return "Unknown Channel"
    
    params = {
        "part": "snippet",
        "id": channel_id,
        "key": api_key
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(YOUTUBE_CHANNELS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data and len(data["items"]) > 0:
                return data["items"][0]["snippet"]["title"]
        except:
            pass
    
    return "Unknown Channel"


async def fetch_channel_video_ids(channel_id: str, max_videos: Optional[int] = None) -> List[str]:
    """
    Fetches all video IDs from a YouTube channel.
    
    Uses YouTube Data API search.list with pagination.
    Returns list of video IDs.
    """
    api_key = get_youtube_api_key()
    
    # Resolve channel ID if needed
    resolved_id = await resolve_channel_id(channel_id)
    if not resolved_id:
        return []
    
    video_ids = []
    next_page_token = None
    
    while True:
        params = {
            "part": "snippet",
            "channelId": resolved_id,
            "type": "video",
            "maxResults": 50,  # Max per page
            "key": get_youtube_api_key(),
            "order": "date"  # Get newest first
        }
        
        if next_page_token:
            params["pageToken"] = next_page_token
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(YOUTUBE_SEARCH_API_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "items" in data:
                    for item in data["items"]:
                        if "id" in item and "videoId" in item["id"]:
                            video_ids.append(item["id"]["videoId"])
                
                # Check if there are more pages
                next_page_token = data.get("nextPageToken")
                
                # Check if we've reached max_videos limit
                if max_videos and len(video_ids) >= max_videos:
                    video_ids = video_ids[:max_videos]
                    break
                
                # If no next page token, we're done
                if not next_page_token:
                    break
            
            except httpx.HTTPStatusError:
                break
            except Exception:
                break
    
    return video_ids

