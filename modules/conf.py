import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="log.log",
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

video_is_verified: bool = False
waiting_for_verification: bool = True
