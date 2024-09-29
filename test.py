from modules.conf import *
from modules.utils import *
from modules.telebot_module import *
from modules.youtube_module import *
from modules.openai_module import *
from modules.editor_module import *
from modules.instagram_module import *

load_dotenv()

def test():
    print(get_top_videos(os.getenv("YOUTUBE_API_KEY")))
    print(get_top_music_videos(os.getenv("YOUTUBE_API_KEY")))
    print(get_transcript("2Rw5Q9qK3kU"))


if __name__ == "__main__":
    test()
