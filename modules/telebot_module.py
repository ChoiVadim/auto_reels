import os
from telebot import TeleBot
from telebot import types
from time import sleep

from modules.conf import *

tele_bot = TeleBot(os.getenv("TELEBOT_TOKEN"))


def send_video_for_review():
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    video_path = "videos/final_video.mp4"

    # Sending the video
    with open(video_path, "rb") as video:
        tele_bot.send_video(chat_id, video)

    # Creating the markup for the buttons
    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text="Yes", callback_data="yes")
    no_button = types.InlineKeyboardButton(text="No", callback_data="no")
    markup.add(yes_button, no_button)

    # Sending the message with the buttons
    tele_bot.send_message(chat_id, "Did you like the video?", reply_markup=markup)


@tele_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "yes":
        tele_bot.send_message(call.message.chat.id, "You liked the video!")
        video_is_verified = True
        waiting_for_verification = False
    elif call.data == "no":
        tele_bot.send_message(call.message.chat.id, "You didn't like the video!")
        waiting_for_verification = False


def poll_for_response():
    # Polling loop to wait for user response, but not running indefinitely
    start_time = sleep(1)
    timeout = 60 * 10  # 10 minutes to wait for the response

    while sleep(1) - start_time < timeout:
        tele_bot.process_new_updates(tele_bot.get_updates())
        if waiting_for_verification is False:
            break

    if video_is_verified is None:
        logging.info("No response received in the allotted time.")

    # Stop polling after the response or timeout
    tele_bot.stop_polling()
