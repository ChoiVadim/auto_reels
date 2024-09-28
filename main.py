from math import floor, ceil

from dotenv import load_dotenv

from modules.utils import *
from modules.youtube_module import *
from modules.openai_module import *

load_dotenv()

delete_all_files_in_directory("videos")

video_id = search_youtube_videos(os.getenv("YOUTUBE_API_KEY"), "ELLE", 1)[0]
print(video_id)
download_youtube_video(video_id)

transcript = get_transcript(video_id)
data = analyze_transcript_openai("".join(str(i) for i in transcript))
print(data)

cut_video(floor(data["start"]), ceil(data["end"]))
create_vertical_video_with_text(text="\n".join(data["text"]))

upload_to_instagram("videos/final_video.mp4", "Like this video!")