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


def start_autoreels() -> None:
    while config.video_is_verified is False:
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
        cut_video(
            floor(data["start"]),
            ceil(data["end"]),
            input_video="videos/video" + video_id + ".mp4",
            output_video="videos/cut_video.mp4",
        )

        create_vertical_video_with_text_and_image(
            text="\n".join(i.capitalize() for i in data["text"]),
            image_path="C:/Users/82102/Desktop/auto_reels/images/white_frame.png",
        )

        # Send video to Telegram for review
        print("Sending video for review...")
        send_video_for_review()

        # Run a short polling loop to check for the response
        print("Polling for response...")
        poll_for_response()

    config.video_is_verified = False

    print("Video verified. Uploading to Instagram...")
    sleep(5)
    inst_bot.login()
    sleep(5)
    inst_bot.upload_video(
        "C:/Users/82102/Desktop/auto_reels/videos/final_video.mp4",
        "If you like the video, please like and subscribe!",
    )
    print("Done!")


def run_scheduler():
    schedule.every().day.at("02:50").do(start_autoreels)
    print("Starting program...")
    # schedule.every(2).minutes.do(start_autoreels)
    while True:
        schedule.run_pending()
        sleep(1)


def main():
    run_scheduler()


if __name__ == "__main__":
    main()
