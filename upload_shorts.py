import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuration
VIDEO_FOLDER =r"D:\youtube\Anime\shorts\output"  # Path to your video folder
CLIENT_SECRETS_FILE = r"D:\Newfolder\credentials.json"  # Path to OAuth credentials
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
START_DATE = datetime.datetime(2025, 5, 2, 15, 0)  # Start scheduling from May 2, 2025, 3 PM
POSTS_PER_DAY = 4
TIME_SLOTS = [21, 22, 23, 20]  # Hours for 3 PM, 4 PM, 5 PM, 8 PM
PRESET_DESCRIPTION = (
    "Lost in the latest Manhua release or scratching your head at that Anime plot twist? No worries, we've got your back! We're breaking down all the essential info in quick, easy-to-digest Reels. Consider this your go-to spot for everything Manhua and Anime! Keywords: Anime plot explained, Manhua chapter recap, Anime episode summary, Manhua worldbuilding, Anime lore, Must-watch Anime, Top Manhua, Anime theories, Manhua updates, Anime news.    Fair Use: Copyright Disclaimer under Section 107 of the Copyright Act 1976, allowance is made for fair use for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use. "
    "#animeexplained #manhuarecap #animereview #manhuaanalysis #whattowatchanime #bestmanhua #animecommunity #mangaexplained #otakulife #animelover"
    "#YouTubeShorts #DailyShorts Like and comment to share your thoughts!"
)
PRESET_TAGS = ["YouTubeShorts", "Manhua", "Manhuaexplained", "AnimationVideo", "Viral"]

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

def get_sorted_videos(folder):
    # Get all .mp4 files and their creation times
    video_files = [
        (f, os.path.getctime(os.path.join(folder, f)))
        for f in os.listdir(folder)
        if f.lower().endswith(".mp4")
    ]
    # Sort by creation time (oldest first)
    video_files.sort(key=lambda x: x[1])
    # Return just the filenames (limit to 50)
    return [f[0] for f in video_files][:50]

def schedule_video(youtube, video_filename, schedule_time):
    # Use filename (without .mp4) as title
    title = os.path.splitext(video_filename)[0]
    request_body = {
        "snippet": {
            "title": title,
            "description": PRESET_DESCRIPTION,
            "tags": PRESET_TAGS,
            "categoryId": "1",  # Film & animation
            "defaultLanguage": "en"
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": schedule_time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "selfDeclaredMadeForKids": False,
            "embeddable": True
        }
    }

    media = MediaFileUpload(os.path.join(VIDEO_FOLDER, video_filename))
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print(f"Scheduled video {title} for {schedule_time}")

def main():
    youtube = authenticate_youtube()
    video_files = get_sorted_videos(VIDEO_FOLDER)
    
    if not video_files:
        print("No .mp4 files found in the folder.")
        return
    
    current_date = START_DATE
    video_index = 0

    while video_index < len(video_files):
        for slot in TIME_SLOTS:
            if video_index >= len(video_files):
                break
            video_filename = video_files[video_index]
            schedule_time = current_date.replace(hour=slot, minute=0, second=0)
            try:
                schedule_video(youtube, video_filename, schedule_time)
            except Exception as e:
                print(f"Error uploading {video_filename}: {e}")
            video_index += 1
        current_date += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()