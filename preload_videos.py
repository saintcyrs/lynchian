import requests
import json
import os
from datetime import datetime

# Load YouTube API Key
API_KEY = os.getenv("API_KEY")
# YouTube Playlist ID
PLAYLIST_ID = "PLTPQcjlcvvXExy6Ti4TccyRvwntL00b2w"

# Path to videos.json inside your React project
JSON_FILE_PATH = "public/videos.json"

# YouTube API URLs
YOUTUBE_PLAYLIST_URL = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
YOUTUBE_VIDEO_DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key=" + API_KEY

### 🔹 SECTION 1: FETCH VIDEOS FROM PLAYLIST ###
def fetch_videos():
    """Fetches all video IDs from the YouTube playlist."""
    video_list = []
    next_page_token = None

    while True:
        response = requests.get(YOUTUBE_PLAYLIST_URL + (f"&pageToken={next_page_token}" if next_page_token else ""))
        data = response.json()

        if "error" in data:
            print(f"❌ Error: {data['error']['message']}")
            return []

        for item in data.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_list.append(video_id)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    print(f"✅ Fetched {len(video_list)} videos from the playlist.")
    return video_list

### 🔹 SECTION 2: FETCH UPLOAD DATES ###
def get_video_upload_date(video_id):
    """Fetches the upload date (YYYY-MM-DD) for a given video ID."""
    response = requests.get(YOUTUBE_VIDEO_DETAILS_URL.format(video_id=video_id))
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        upload_date = data["items"][0]["snippet"]["publishedAt"][:10]  # Extract YYYY-MM-DD
        return upload_date
    return None

### 🔹 SECTION 3: BUILD & SAVE `videos.json` ###
def generate_videos_json():
    """Generates a fully populated videos.json file."""
    video_list = fetch_videos()
    videos = {}

    for video_id in video_list:
        upload_date = get_video_upload_date(video_id)
        if upload_date:
            video_month_day = upload_date[5:]  # Extract MM-DD from YYYY-MM-DD
            video_url = f"https://www.youtube.com/embed/{video_id}"

            if video_month_day not in videos:
                videos[video_month_day] = []
            videos[video_month_day].append(video_url)

    # Save to videos.json
    save_videos_json(videos)
    print("🎉 videos.json has been fully populated!")

def save_videos_json(videos):
    """Saves the videos.json file."""
    with open(JSON_FILE_PATH, "w") as f:
        json.dump(videos, f, indent=4)
    print("💾 videos.json updated successfully.")

### 🔹 SECTION 4: RUN SCRIPT ###
if __name__ == "__main__":
    generate_videos_json()
