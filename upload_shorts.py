import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuration
VIDEO_FOLDER =r"D:...\video_file"  # Path to your video folder where you have all the videos imported
CLIENT_SECRETS_FILE = r"D:\...\credentials.json"  # Path to OAuth credentials
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]  # this is scope added from gcp (more in readme file)
START_DATE = datetime.datetime(2025, 5, 2, 15, 0)  # Start scheduling from May 2, 2025, 3 PM 
POSTS_PER_DAY = 4 #no of reels i want to publish interval of 24hour
TIME_SLOTS = [21, 22, 23, 20]  # Hours for 9 PM, 10 PM, 11 PM, 8 PM
PRESET_DESCRIPTION = (
    "Your video description here"
    "add any hastags you want to add"
    "add any keywords you want to add"
)
PRESET_TAGS = ["YouTubeShorts", "ABCtags", "Viral"]

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)  #learn more about client_secrets_file from readme file
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
            "categoryId": "1",  # Film & animation (choose the category, follow readme for use)
            "defaultLanguage": "en"
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": schedule_time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "selfDeclaredMadeForKids": False,  #true , if your content is for kids like cartoons and all
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

    while video_index < len(video_files):     #this part is for the looping on video file content on based of the date and time in they created
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
