# YouTube Scraper - Standalone Package

A beautiful web-based application for scraping YouTube video details, transcripts, and channel exports.

## Features

- 🎨 Beautiful modern UI with live progress tracking
- 📊 Export to JSON, CSV, or Excel formats
- 📝 Get video transcripts automatically
- 📺 Bulk video processing
- 📹 Channel export with progress tracking
- ⚡ Fast and efficient processing

## Installation

### Windows

1. Extract the zip file
2. Double-click `install.bat`
3. Enter your YouTube API Key when prompted
4. Wait for installation to complete

### Mac / Linux

1. Extract the zip file
2. Open terminal in the extracted folder
3. Run: `chmod +x install.sh run.sh`
4. Run: `./install.sh`
5. Enter your YouTube API Key when prompted
6. Wait for installation to complete

## Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable "YouTube Data API v3"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy your API key

**Note:** The API key is free and includes 10,000 quota units per day (enough for ~10,000 video metadata requests).

## Running the Application

### Windows

Double-click `run.bat` or run:
```bash
python main.py
```

### Mac / Linux

Run:
```bash
./run.sh
```

Or:
```bash
python3 main.py
```

The application will automatically open in your browser at `http://localhost:8000`

## Usage

1. **Single Video**: Enter a YouTube URL or video ID to get details and transcript
2. **Bulk Videos**: Paste multiple URLs (one per line) to process in bulk
3. **Channel Export**: Enter a channel URL to export all videos with transcripts

## System Requirements

- Python 3.8 or higher
- Internet connection
- YouTube Data API v3 key (free)

## Troubleshooting

### "Python is not installed"
- Download Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### "API Key not working"
- Verify your API key in Google Cloud Console
- Make sure "YouTube Data API v3" is enabled
- Check that your API key has no restrictions (or add localhost to allowed IPs)

### "Transcript is null"
- Some videos don't have captions/transcripts
- Your local IP should work fine (not blocked like cloud servers)
- If you see blocking errors, contact support

## Support

For issues or questions, please check the main repository or create an issue.

## License

This software is provided as-is for educational and research purposes.

