# Video Downloader

A modern, Flask-based web application that allows users to download videos from various platforms including YouTube, Facebook, Twitter, Instagram, TikTok, and many more using yt-dlp.

## Features

- **Multiple Platform Support**: Download from YouTube, Facebook, Twitter, Instagram, TikTok, and 1000+ other sites
- **Format Options**: Choose between video+audio, video only, audio only, or subtitles only
- **Quality Selection**: Select from multiple quality options (1080p, 720p, 480p, etc.)
- **Real-time Progress**: Track download progress with live updates
- **Modern UI**: Clean, responsive interface with dark theme
- **Automatic Cleanup**: Files are automatically cleaned up after download
- **Recent Downloads**: View history of recent downloads

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd video-downloader
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the app**
   Open your browser and go to `http://localhost:5000`

### Cloud Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Render, Heroku, or other cloud platforms.

## How to Use

1. **Enter Video URL**: Paste the URL of the video you want to download
2. **Select Format**: Choose your preferred download format:
   - Video + Audio (MP4) - Complete video with sound
   - Video Only - Video without audio
   - Audio Only (MP3) - Extract audio only
   - Subtitles Only (SRT) - Download subtitles in English
3. **Choose Quality**: Select video quality (Best, 1080p, 720p, 480p, 360p)
4. **Start Download**: Click the download button and wait for completion
5. **Download File**: Once complete, click the download link to get your file

## Supported Platforms

- YouTube (including YouTube Shorts)
- Facebook
- Twitter
- Instagram
- TikTok
- Vimeo
- Dailymotion
- Reddit
- And 1000+ more sites supported by yt-dlp

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5 with dark theme
- **Download Engine**: yt-dlp
- **Database**: SQLite (development) / PostgreSQL (production)
- **File Storage**: Temporary storage with automatic cleanup

## Environment Variables

- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Secret key for session management
- `DOWNLOAD_FOLDER`: Directory for temporary file storage (default: `/tmp/downloads`)

## Development

### Project Structure
```
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routing and handlers
├── download_manager.py # Download processing logic
├── templates/          # HTML templates
│   ├── base.html
│   └── index.html
├── static/            # Static assets
│   ├── css/style.css
│   └── js/main.js
└── downloads/         # Temporary download storage
```

### Key Components

- **Download Manager**: Handles yt-dlp integration and progress tracking
- **Database Models**: Stores download requests and status
- **Frontend**: Real-time progress updates and modern UI
- **File Handling**: Automatic cleanup and secure file serving

## Security

- Files are stored temporarily and cleaned up automatically
- No user authentication required (suitable for personal use)
- Session management with secure secret keys
- Input validation and sanitization

## Limitations

- Files are not permanently stored (temporary download only)
- No user accounts or persistent download history
- Some platforms may block server-side downloads
- Performance depends on server resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and personal use. Please respect the terms of service of the platforms you download from.

## Support

For issues and questions:
- Check the deployment guide in [DEPLOYMENT.md](DEPLOYMENT.md)
- Review the technical documentation in [replit.md](replit.md)
- Open an issue on the repository

## Disclaimer

This tool is for personal use only. Users are responsible for complying with the terms of service of the platforms they download from. Please respect copyright and intellectual property rights.