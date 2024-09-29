import logging
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()

logging.basicConfig(
    filename="log.log",
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


@dataclass
class Config:
    video_is_verified: bool = False
    waiting_for_verification: bool = True


config = Config()

videos_folder_path = "/home/vadim/Desktop/auto_reels/videos/"
