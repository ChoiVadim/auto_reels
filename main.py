import threading
import signal
from time import sleep
from random import randint
from math import floor, ceil

import schedule

from modules.conf import *
from modules.utils import *
from modules.telebot_module import *
from modules.youtube_module import *
from modules.openai_module import *
from modules.editor_module import *
from modules.instagram_module import *

inst_bot = InstagramBot(
    username=os.getenv("INST_USERNAME"),
    password=os.getenv("INST_PASSWORD"),
)

stop_scheduler = False


def start_autoreels() -> None:
    global stop_scheduler
    stop_scheduler = True

    while video_is_verified is False:
        # Delete all previous downloaded files
        delete_all_files_in_directory("videos")

        # Search and download video
        video_id = get_top_videos(os.getenv("YOUTUBE_API_KEY"))
        video_id = video_id[randint(0, len(video_id) - 1)]
        download_youtube_video(video_id)

        # Get transcript
        transcript = get_transcript(video_id)

        # Analyze transcript
        data = analyze_transcript_openai("".join(str(i) for i in transcript))
        logging.info(data)

        # # Create video
        cut_video(floor(data["start"]), ceil(data["end"]))
        create_vertical_video_with_text_and_image(
            text="\n".join(i.capitalize() for i in data["text"]),
            image_path="C:/Users/82102/Desktop/auto_reels/images/white_frame.png",
        )

        # Send video to Telegram for review
        send_video_for_review()

        # Run a short polling loop to check for the response
        poll_for_response()

    if video_is_verified:
        inst_bot.login()
        sleep(5)
        inst_bot.upload_video(
            "C:/Users/82102/Desktop/auto_reels/videos/final_video.mp4",
            "If you like the video, please like and subscribe!",
        )


def run_scheduler():
    schedule.every().day.at("01:27").do(start_autoreels)
    while not stop_scheduler:
        schedule.run_pending()
        sleep(1)
    print("Scheduler stopped.")


def main():
    while True:
        run_scheduler()


if __name__ == "__main__":
    main()
