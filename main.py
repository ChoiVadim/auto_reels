from time import sleep
from math import floor, ceil

import schedule

from modules.conf import *
from modules.utils import *
from modules.telebot_module import *
from modules.youtube_module import *
from modules.openai_module import *
from modules.editor_module import *
from modules.instagram_module import *


def start_auto_reels() -> None:
    video_path, cut_video_path, final_video_path = None, None, None

    while config.video_is_verified is False:
        # Get a list of id with most popular video on youtube in us
        video_id_list = get_top_music_videos(os.getenv("YOUTUBE_API_KEY"))
        video_id = video_id_list[0]

        # Initiate paths for video processing
        video_path = videos_folder_path + "video" + video_id + ".mp4"
        cut_video_path = videos_folder_path + "cut_video" + video_id + ".mp4"
        final_video_path = videos_folder_path + "final_video" + video_id + ".mp4"

        # Try to download youtube video and take next id if failed
        try:
            download_youtube_video(video_id, output_path=video_path)
        except yt_dlp.utils.DownloadError:
            video_id = video_id_list[1]
            download_youtube_video(video_id=video_id, output_path=video_path)

        # Get transcript from youtube (return list of dictionaries)
        transcript = get_transcript(video_id)
        logging.info(transcript)

        # Analyze transcript with openai (return dictionary)
        data = analyze_transcript_openai("".join(str(i) for i in transcript))
        logging.info(data)

        # Create video with text and image
        cut_video(
            floor(data["start"]),
            ceil(data["end"]),
            input_video=video_path,
            output_video=cut_video_path,
        )
        create_vertical_video_with_text_and_image(
            text="\n".join(i.capitalize() for i in data["text"]),
            image_path="/home/vadim/Desktop/auto_reels/images/white_frame.png",
            video_path=cut_video_path,
            output_path=final_video_path,
        )

        # Send video to Telegram for review
        send_video_for_review(video_path=final_video_path)

        # Wait for user response in Telegram
        poll_for_response()

    config.video_is_verified = False

    with InstagramBot(
        username=os.getenv("INSTAGRAM_USERNAME"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
    ) as inst_bot:
        inst_bot.upload_video(
            final_video_path,
            "If you like the video, please like and subscribe!",
        )


def run_scheduler():
    run_time = input("Enter run time (HH:MM): ")
    schedule.every().day.at(run_time).do(start_auto_reels)
    # schedule.every(5).hours.do(start_auto_reels)
    while True:
        schedule.run_pending()
        sleep(1)


def main():
    run_scheduler()


if __name__ == "__main__":
    main()
