import yt_dlp
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound


def search_youtube_videos(api_key, query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        videoDuration="medium",
        videoCaption="closedCaption",
        order="relevance"
    )

    response = request.execute()

    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

def download_youtube_video(video_id, output_path="videos/video.mp4"):
    url = "https://www.youtube.com/watch?v=" + video_id
    ydl_opts = {
        "format": "mp4",
        "outtmpl": output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return transcript

    except NoTranscriptFound:
        print(f"No English subtitles found for video: {video_id}")
        return None