# YouTube Scraper

A FastAPI service that fetches YouTube video metadata and transcripts.

## Features

- Fetches video metadata (title, description, channel, thumbnails, duration) via YouTube Data API v3
- Retrieves video transcripts using `youtube-transcript-api`
- Supports multiple input formats: full URLs, short URLs, or bare video IDs
- Handles errors gracefully - individual video failures don't break the entire request

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variable:
```bash
export YOUTUBE_API_KEY=your_api_key_here
```

Or create a `.env` file:
```
YOUTUBE_API_KEY=your_api_key_here
```

## Running Locally

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /health
Health check endpoint.

### POST /youtube/details
Fetches YouTube video details including metadata and transcripts.

**Request:**
```json
{
  "urls": ["https://www.youtube.com/watch?v=VIDEO_ID"],
  "ids": ["VIDEO_ID"]
}
```

**Response:**
```json
{
  "items": [
    {
      "id": "VIDEO_ID",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "title": "Video Title",
      "description": "Video description",
      "channel_title": "Channel Name",
      "published_at": "2024-01-01T00:00:00Z",
      "duration": "PT10M30S",
      "thumbnails": {
        "default": "url",
        "medium": "url",
        "high": "url",
        "maxres": "url"
      },
      "transcript": "Full transcript text..."
    }
  ],
  "errors": []
}
```

## Deployment on Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variable `YOUTUBE_API_KEY` in Render dashboard
5. Deploy!

## Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key and set it as `YOUTUBE_API_KEY`
