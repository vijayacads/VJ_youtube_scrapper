import os
import re
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


async def get_channel_video_count(channel_id: str) -> Optional[int]:
    """
    Gets channel video count from channel ID.
    Uses channels.list API with statistics part.
    Returns None if unavailable.
    """
    try:
        api_key = get_youtube_api_key()
    except ValueError:
        return None
    
    params = {
        "part": "statistics",
        "id": channel_id,
        "key": api_key
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(YOUTUBE_CHANNELS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data and len(data["items"]) > 0:
                statistics = data["items"][0].get("statistics", {})
                video_count_str = statistics.get("videoCount")
                if video_count_str:
                    try:
                        return int(video_count_str)
                    except (ValueError, TypeError):
                        return None
        except:
            pass
    
    return None


async def fetch_channel_video_ids(channel_id: str, max_videos: Optional[int] = None, sort_by: str = "date") -> List[str]:
    """
    Fetches video IDs from a YouTube channel.
    
    Uses YouTube Data API search.list with pagination.
    
    Args:
        channel_id: Channel ID or URL
        max_videos: Maximum number of videos to return
        sort_by: "date" for latest videos, "popular" for fetching all videos (will be sorted by view count)
    
    Returns:
        List of video IDs
    """
    api_key = get_youtube_api_key()
    
    # Resolve channel ID if needed
    resolved_id = await resolve_channel_id(channel_id)
    if not resolved_id:
        return []
    
    video_ids = []
    next_page_token = None
    
    # For popular sorting, fetch ALL videos (no limit) - will be sorted by view count later
    # For date sorting, respect max_videos limit
    fetch_all = (sort_by == "popular")
    
    while True:
        params = {
            "part": "snippet",
            "channelId": resolved_id,
            "type": "video",
            "maxResults": 50,  # Max per page
            "key": get_youtube_api_key(),
            "order": "date"  # API doesn't support viewCount, so we always fetch by date and sort later
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
                
                # For popular: fetch all videos (no limit)
                # For date: respect max_videos limit
                if not fetch_all and max_videos and len(video_ids) >= max_videos:
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


async def scrape_popular_videos(channel_url: str, max_videos: int = 100, content_type: str = "videos") -> List[str]:
    """
    Scrapes YouTube videos using Playwright.
    
    Uses Perplexity's recommended approach:
    - For Popular videos: Uses role-based selectors to click "Sort by" → "Popular"
    - For Search results: Uses ytd-video-renderer a#video-title with longer timeout
    
    Handles:
    - Channel videos (with Popular sorting)
    - Search results (within channel or YouTube-wide)
    
    Returns list of video URLs.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise ImportError("playwright is required for scraping. Install it with: pip install playwright && playwright install chromium")
    
    video_urls = []
    is_search = '/search' in channel_url
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            if is_search:
                # For search URLs, use Perplexity's approach
                await page.goto(channel_url, wait_until="networkidle", timeout=30000)
                
                # Wait for search results with longer timeout (20 seconds)
                await page.wait_for_selector('ytd-video-renderer a#video-title', timeout=20000)
                
                # Scroll to load more videos
                scroll_count = max(1, (max_videos // 20) + 1)
                for _ in range(min(scroll_count, 10)):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)
                
                # Extract video URLs using Perplexity's selector
                anchors = page.locator('ytd-video-renderer a#video-title')
                count = await anchors.count()
                
                for i in range(min(count, max_videos)):
                    href = await anchors.nth(i).get_attribute('href')
                    if href:
                        if href.startswith('/'):
                            video_urls.append(f"https://www.youtube.com{href}")
                        elif 'youtube.com' in href:
                            video_urls.append(href)
                        elif href.startswith('watch?v='):
                            video_urls.append(f"https://www.youtube.com/{href}")
                
            else:
                # Normalize channel URL -> /videos or /shorts
                channel_url = channel_url.rstrip('/')
                if '/videos' in channel_url:
                    channel_url = channel_url.split('/videos')[0]
                if '/shorts' in channel_url:
                    channel_url = channel_url.split('/shorts')[0]
                
                # Use /shorts if content_type is "shorts", otherwise /videos
                if content_type == "shorts":
                    target_url = f"{channel_url}/shorts"
                else:
                    target_url = f"{channel_url}/videos"

                await page.goto(target_url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Check for consent dialog and accept if present
                try:
                    consent_button = page.locator('button:has-text("Accept all"), button:has-text("Accept"), button:has-text("I agree")')
                    if await consent_button.count() > 0:
                        await consent_button.first.click(timeout=3000)
                        await page.wait_for_timeout(2000)
                except:
                    pass

                # Click "Popular" chip directly (it's a button/chip on the page, not a dropdown option)
                sort_success = False
                sort_error = None
                
                try:
                    # Use JavaScript to find and click the "Popular" chip/button directly
                    result = await page.evaluate('''() => {
                        // Find all clickable elements with "Popular" text
                        const allElements = Array.from(document.querySelectorAll('*'));
                        let popularButton = null;
                        
                        for (const el of allElements) {
                            const text = (el.innerText || el.textContent || '').trim().toLowerCase();
                            const tagName = el.tagName;
                            const role = el.getAttribute('role');
                            
                            // Look for elements with "popular" text that are clickable
                            if (text === 'popular' && 
                                el.offsetWidth > 0 && el.offsetHeight > 0 &&
                                (tagName === 'BUTTON' || tagName === 'A' || role === 'button' || 
                                 el.onclick || el.getAttribute('tabindex') !== null ||
                                 el.classList.contains('chip') || el.closest('button') !== null)) {
                                popularButton = el;
                                break;
                            }
                        }
                        
                        if (popularButton) {
                            popularButton.click();
                            return 'clicked popular';
                        }
                        return 'popular button not found';
                    }''')
                    
                    if result == 'clicked popular':
                        await page.wait_for_load_state('networkidle')
                        await page.wait_for_timeout(3000)
                        sort_success = True
                    else:
                        sort_error = f"Could not find Popular chip: {result}"
                        
                except Exception as e:
                    sort_error = f"JavaScript click failed: {str(e)}"
                
                if not sort_success:
                    # Fallback: Try locator with text
                    try:
                        popular_chip = page.locator('text="Popular"').first
                        await popular_chip.click(timeout=5000)
                        await page.wait_for_load_state('networkidle')
                        await page.wait_for_timeout(3000)
                        sort_success = True
                    except Exception as e2:
                        if not sort_error:
                            sort_error = f"Text locator failed: {str(e2)}"
                
                # Try multiple selectors for video grid
                selectors = [
                    "ytd-rich-grid-video-renderer a#video-title",
                    "ytd-rich-item-renderer a#video-title", 
                    "a#video-title-link",
                    "a#video-title",
                    'a[href*="/watch?v="]'
                ]
                
                selector = None
                for sel in selectors:
                    try:
                        await page.wait_for_selector(sel, timeout=5000)
                        selector = sel
                        break
                    except:
                        continue
                
                if not selector:
                    raise Exception("No video elements found on page. The page structure may have changed or videos may not have loaded.")

                # Scroll enough to get up to max_videos
                scroll_count = max(1, (max_videos // 30) + 1)
                for _ in range(min(scroll_count, 10)):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)

                vids = page.locator(selector)
                count = await vids.count()
                if count == 0:
                    raise Exception(f"No videos found with selector '{selector}'. Please check the channel URL.")

                for i in range(min(count, max_videos)):
                    href = await vids.nth(i).get_attribute('href')
                    if not href:
                        continue
                    if href.startswith('/'):
                        video_urls.append(f'https://www.youtube.com{href}')
                    elif 'youtube.com' in href:
                        video_urls.append(href)
                    elif href.startswith('watch?v='):
                        video_urls.append(f'https://www.youtube.com/{href}')
            
            # Remove duplicates while preserving order
            seen = set()
            unique_urls = []
            for url in video_urls:
                if url not in seen:
                    seen.add(url)
                    unique_urls.append(url)
            
            # Take only max_videos
            unique_urls = unique_urls[:max_videos]
            
            return unique_urls
            
        except Exception as e:
            raise Exception(f"Error scraping videos: {str(e)}")
        finally:
            await browser.close()
    
    return video_urls
