from typing import List, Dict, Optional, Union, Any
from pydantic import BaseModel


class YoutubeDetailsRequest(BaseModel):
    urls: List[str] = []
    ids: List[str] = []


class YoutubeVideoFull(BaseModel):
    id: str
    url: str
    title: str
    description: str
    channel_title: str
    published_at: str
    duration: str
    thumbnails: Dict[str, Optional[str]]
    transcript: Optional[str] = None
    view_count: Optional[int] = None


class YoutubeError(BaseModel):
    id_or_url: str
    message: str


class YoutubeDetailsResponse(BaseModel):
    items: List[YoutubeVideoFull]
    errors: List[YoutubeError]


class YoutubeBulkRequest(BaseModel):
    urls_text: Optional[str] = None  # Plain text, newline-separated URLs/IDs


class ChannelExportRequest(BaseModel):
    channel_id_or_url: str
    include_transcripts: bool = True
    max_videos: Optional[int] = None  # Limit number of videos (optional)
    sort_by: str = "popular"  # "popular" or "latest"


class ChannelExportResponse(BaseModel):
    channel_id: str
    channel_title: str
    total_videos: int
    processed_videos: int
    data: Union[YoutubeDetailsResponse, str]  # Response or CSV string
    errors: List[YoutubeError]


class ScraperRequest(BaseModel):
    channel_url: str
    max_videos: int = 100
    content_type: str = "videos"  # "videos" or "shorts"


class ScraperResponse(BaseModel):
    video_urls: List[str]
    count: int


class JobStatus(BaseModel):
    job_id: str
    status: str  # "running", "completed", "cancelled", "error"
    current: int
    total: int
    message: str
    result: Optional[Union[YoutubeDetailsResponse, ChannelExportResponse, Dict[str, Any]]] = None

