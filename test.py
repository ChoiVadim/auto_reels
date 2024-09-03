from moviepy.config import change_settings
from moviepy.editor import TextClip
from modules.youtube_module import get_top_videos
from dotenv import load_dotenv
import os


load_dotenv()


def test():
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick\magick.exe"})
    print(TextClip.list("font"))


def test2():
    print(get_top_videos(os.getenv("YOUTUBE_API_KEY")))


test2()
