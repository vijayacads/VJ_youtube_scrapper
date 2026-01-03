import os
from typing import Dict, List
import httpx
from models import YoutubeVideoFull


YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/videos"


def get_youtube_api_key() -> str:
    """Get YouTube API key from environment variable."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set")
    return api_key


async def fetch_youtube_metadata(video_ids: List[str]) -> Dict[str, YoutubeVideoFull]:
    """
    Fetches YouTube video metadata using YouTube Data API v3.
    
    Calls videos.list in batches of <=50 IDs.
    Returns dict mapping id -> YoutubeVideoFull (transcript=None for now).
    """
    if not video_ids:
        return {}
    
    results = {}
    
    # Batch IDs into chunks of 50 (YouTube API limit)
    batch_size = 50
    for i in range(0, len(video_ids), batch_size):
        batch = video_ids[i:i + batch_size]
        batch_results = await _fetch_batch(batch)
        results.update(batch_results)
    
    return results


async def _fetch_batch(video_ids: List[str]) -> Dict[str, YoutubeVideoFull]:
    """Fetches metadata for a single batch of video IDs (max 50)."""
    ids_str = ','.join(video_ids)
    api_key = get_youtube_api_key()
    
    params = {
        "part": "snippet,contentDetails",
        "id": ids_str,
        "key": api_key
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(YOUTUBE_API_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = {}
            
            if "items" in data:
                for item in data["items"]:
                    video_id = item["id"]
                    snippet = item.get("snippet", {})
                    content_details = item.get("contentDetails", {})
                    
                    # Extract thumbnails
                    thumbnails = {}
                    thumb_data = snippet.get("thumbnails", {})
                    for size in ["default", "medium", "high", "maxres"]:
                        if size in thumb_data:
                            thumbnails[size] = thumb_data[size].get("url")
                        else:
                            thumbnails[size] = None
                    
                    # Parse duration (ISO 8601 format like PT1H2M10S)
                    duration = content_details.get("duration", "")
                    
                    video = YoutubeVideoFull(
                        id=video_id,
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        title=snippet.get("title", ""),
                        description=snippet.get("description", ""),
                        channel_title=snippet.get("channelTitle", ""),
                        published_at=snippet.get("publishedAt", ""),
                        duration=duration,
                        thumbnails=thumbnails,
                        transcript=None  # Will be filled later
                    )
                    results[video_id] = video
            
            return results
        
        except httpx.HTTPStatusError as e:
            # Log error but return empty dict for this batch
            # Individual errors will be handled at a higher level
            return {}
        except Exception as e:
            # Handle other errors gracefully
            return {}

