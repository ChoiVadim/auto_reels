# 🎬 Auto Reels - Automated Instagram Content Creator

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?logo=instagram&logoColor=white)](https://instagram.com)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?logo=youtube&logoColor=white)](https://youtube.com)

An intelligent automation system that creates engaging Instagram Reels by processing popular YouTube videos with AI-powered content analysis and automated video editing.

## 🌟 Features

- **🎯 Smart Content Discovery**: Automatically finds trending YouTube videos and music content
- **🤖 AI-Powered Analysis**: Uses OpenAI GPT-4 to analyze video transcripts and extract engaging segments
- **✂️ Automated Video Editing**: Creates vertical Instagram-ready videos with text overlays
- **📱 Telegram Integration**: Review and approve content before posting via Telegram bot
- **🔄 Instagram Auto-Upload**: Seamlessly uploads approved content to Instagram
- **⏰ Scheduled Posting**: Set custom posting schedules for consistent content delivery
- **🌐 Multi-Language Support**: Supports English content with Russian translations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- ImageMagick (for video processing)
- FFmpeg (for video encoding)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/auto_reels.git
   cd auto_reels
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up ImageMagick**
   - **Linux/macOS**: `sudo apt-get install imagemagick` or `brew install imagemagick`
   - **Windows**: Download from [ImageMagick website](https://imagemagick.org/script/download.php)

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   YOUTUBE_API_KEY=your_youtube_api_key
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   TELEBOT_TOKEN=your_telegram_bot_token
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### API Keys Setup

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and navigate to API keys
3. Generate a new API key and add it to your `.env` file

#### YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the key to your `.env` file

#### Telegram Bot Setup
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token and chat ID
4. Add both to your `.env` file

## 📁 Project Structure

```
auto_reels/
├── modules/
│   ├── conf.py              # Configuration and logging setup
│   ├── editor_module.py     # Video editing and processing
│   ├── instagram_module.py  # Instagram API integration
│   ├── ollama_module.py     # Local LLM integration (optional)
│   ├── openai_module.py     # OpenAI GPT integration
│   ├── telebot_module.py    # Telegram bot for content review
│   ├── utils.py             # Utility functions
│   └── youtube_module.py    # YouTube API and video download
├── images/
│   └── white_frame.png      # Default overlay image
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
└── test.py                 # Testing utilities
```

## 🎯 How It Works

1. **Content Discovery**: Fetches trending videos from YouTube using the YouTube Data API
2. **Transcript Analysis**: Downloads video transcripts and analyzes them with OpenAI GPT-4
3. **Segment Selection**: AI selects the most engaging 10-15 second segments with rich vocabulary
4. **Video Processing**: 
   - Downloads the source video
   - Cuts the selected segment
   - Converts to vertical format (1080x1920)
   - Adds text overlays and background
5. **Review Process**: Sends the processed video to Telegram for manual approval
6. **Auto-Upload**: Uploads approved content to Instagram with generated captions

## 🛠️ Usage Examples

### Basic Usage
```python
from modules.youtube_module import get_top_videos, download_youtube_video
from modules.openai_module import analyze_transcript_openai

# Get trending videos
video_ids = get_top_videos(api_key="your_api_key")

# Download and process
download_youtube_video(video_ids[0])
```

### Custom Scheduling
```python
import schedule
from main import main

# Schedule daily posts at 2 PM
schedule.every().day.at("14:00").do(main)

# Schedule every 6 hours
schedule.every(6).hours.do(main)
```

## 📊 Features Deep Dive

### AI Content Analysis
The system uses OpenAI's GPT-4 to:
- Identify engaging content segments
- Extract vocabulary-rich phrases
- Generate bilingual translations
- Ensure optimal timing for social media

### Video Processing Pipeline
- **Input**: YouTube video (any format)
- **Processing**: Segment extraction, vertical conversion, text overlay
- **Output**: Instagram-ready vertical video (1080x1920)

### Quality Control
- Manual review via Telegram bot
- Automatic retry on failed downloads
- Error logging and recovery
- Session management for Instagram

## 🔒 Security & Privacy

- All API keys stored in environment variables
- Instagram session management with secure token storage
- No hardcoded credentials in source code
- Automatic cleanup of temporary files

## 🐛 Troubleshooting

### Common Issues

**ImageMagick not found**
```bash
# Update the path in modules/editor_module.py
change_settings({"IMAGEMAGICK_BINARY": r"/path/to/convert"})
```

**Instagram login failed**
- Check username/password in `.env`
- Delete `session.json` to force re-authentication
- Ensure 2FA is disabled or use app-specific password

**YouTube API quota exceeded**
- YouTube API has daily quota limits
- Consider implementing caching or reducing request frequency

**Video processing errors**
- Ensure FFmpeg is installed and accessible
- Check video file permissions and disk space

## 📈 Performance Tips

- Use SSD storage for faster video processing
- Implement video caching to avoid re-downloading
- Monitor API usage to stay within quotas
- Use webhook-based Telegram polling for better responsiveness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please ensure you comply with:
- YouTube's Terms of Service
- Instagram's Terms of Service
- Copyright laws and fair use guidelines
- Platform-specific automation policies

Always respect content creators' rights and consider reaching out for permission when using their content.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for GPT-4 API
- [Google](https://developers.google.com/youtube) for YouTube Data API
- [MoviePy](https://zulko.github.io/moviepy/) for video processing
- [InstagramAPI](https://github.com/adw0rd/instagrapi) for Instagram integration

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the logs in `log.log` for detailed error information

---

**Made with ❤️ for content creators who want to automate their social media presence**