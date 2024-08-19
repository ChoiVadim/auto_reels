import os
import shutil
from time import sleep

import yt_dlp
import requests
from instagrapi import Client
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import TextClip, CompositeVideoClip


def upload_to_instagram(video_path, caption):
    cl = Client()
    sleep(3)
    cl.login(username=os.environ("INST_USERNAME"), password=os.environ("INST_PASSWORD"))
    sleep(5)
    cl.clip_upload(video_path, caption=caption)


def download_youtube_video(url, output_path="videos/video.mp4"):
    ydl_opts = {
        "format": "mp4",
        "outtmpl": output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript


def cut_video(
    start_time,
    end_time,
    input_video="videos/video.mp4",
    output_video="videos/cut_video.mp4",
):
    video = VideoFileClip(input_video)
    cut_clip = video.subclip(start_time, end_time)
    cut_clip.write_videofile(output_video)


def create_vertical_video_with_text(
    *, video_path="videos/cut_video.mp4", output_path="videos/final_video.mp4", text=""
):
    video = VideoFileClip(video_path)
    vertical_resolution = (1080, 1920)

    video_resized = video.resize(width=1080)

    if video_resized.h > 960:
        video_resized = video_resized.crop(y_center=video_resized.h // 2, height=960)
    else:
        video_resized = video_resized.set_position(("center", 300))

    txt_clip = TextClip(
        text, fontsize=50, color="white", size=(800, None), bg_color="black"
    ).set_duration(video.duration)

    txt_clip_with_margin = txt_clip.set_position(("center", 1920 / 2 + 50))

    video_with_text = CompositeVideoClip(
        [video_resized, txt_clip_with_margin], size=vertical_resolution
    )

    video_with_text.write_videofile(output_path, codec="libx264", fps=30)


def delete_all_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    else:
        print(f"Directory {directory_path} does not exist")
