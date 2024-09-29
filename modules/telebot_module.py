import os
import requests
from time import sleep

from telebot import TeleBot
from telebot import types

from modules.conf import config


tele_bot = TeleBot(os.getenv("TELEBOT_TOKEN"))

markup = types.InlineKeyboardMarkup()
yes_button = types.InlineKeyboardButton(text="👍", callback_data="yes")
no_button = types.InlineKeyboardButton(text="👎", callback_data="no")
markup.add(yes_button, no_button)

def send_video_for_review(video_path):
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Sending the video
    with open(video_path, "rb") as video:
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                tele_bot.send_video(chat_id, video, caption="Video for review" ,reply_markup=markup)
                break
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}")
                sleep(retry_delay)


@tele_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "yes":
        tele_bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        config.video_is_verified = True
        config.waiting_for_verification = False
    elif call.data == "no":
        config.waiting_for_verification = False
        tele_bot.delete_message(call.message.chat.id, call.message.message_id)


def poll_for_response():
    last_update_id = None  # Track the last processed update ID

    while config.waiting_for_verification is True:
        print("Waiting for response...")

        updates = tele_bot.get_updates(offset=last_update_id)

        if updates:
            for update in updates:
                last_update_id = update.update_id + 1  # Update the offset
                tele_bot.process_new_updates([update])

    config.waiting_for_verification = True
