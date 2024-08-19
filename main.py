from math import floor, ceil
from dotenv import load_dotenv

from modules.utils import *
from modules.openai_module import analyze_transcript_openai

load_dotenv()

url = "https://www.youtube.com/watch?v=UHXCSeoU-YM"

delete_all_files_in_directory("videos")
download_youtube_video(url)
transcript = get_transcript(url.split("v=")[1])
data = analyze_transcript_openai("".join(str(i) for i in transcript))
cut_video(floor(data["start"]), ceil(data["end"]))
create_vertical_video_with_text(text="\n".join(data["text"]))
upload_to_instagram("videos/final_video.mp4", "Like this video!")