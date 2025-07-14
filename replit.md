# Video Downloader Application

## Overview

This is a Flask-based web application that allows users to download videos from various platforms (YouTube, Facebook, Twitter, Instagram, TikTok, etc.) using yt-dlp. The application provides a clean web interface for submitting download requests and tracks the progress of downloads through a SQLite database.

## User Preferences

Preferred communication style: Simple, everyday language.
File Storage: Store downloaded files outside source code folder (using /tmp/downloads)
Deployment: Prefer Render deployment with automatic cleanup

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM using DeclarativeBase
- **Download Engine**: yt-dlp (YouTube-dl fork) for video extraction and downloading
- **Background Processing**: Python threading for asynchronous download processing
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with Replit dark theme
- **Icons**: Feather Icons
- **JavaScript**: Vanilla JavaScript for dynamic interactions
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

### File Structure
```
├── app.py                 # Flask application initialization and configuration
├── main.py               # Application entry point
├── models.py             # Database models using SQLAlchemy
├── routes.py             # URL routing and request handlers
├── download_manager.py   # Background download processing logic
├── templates/
│   ├── base.html         # Base template with navigation and layout
│   └── index.html        # Main download interface
└── static/
    ├── css/style.css     # Custom styling and gradients
    └── js/main.js        # Frontend JavaScript functionality
```

## Key Components

### Database Model (DownloadRequest)
- **Purpose**: Track download requests and their status
- **Fields**: URL, title, format, quality, status, file path, progress, timestamps
- **Status States**: pending → processing → completed/failed

### Download Manager
- **Responsibility**: Process downloads in background threads
- **Features**: Progress tracking, format selection, quality options
- **Error Handling**: Captures and stores error messages in database

### Route Handlers
- **Index Route**: Serves the main download interface
- **Download Route**: Accepts POST requests, validates URLs, creates database records
- **API Routes**: Provide status updates and file serving (implementation incomplete)

### Frontend Interface
- **Download Form**: URL input with format and quality selection
- **Format Options**: Video+Audio, Video Only, Audio Only, Subtitles Only
- **Quality Selection**: Dynamic options based on format (1080p, 720p, 480p, etc.)
- **Progress Tracking**: JavaScript-based status polling (implementation incomplete)

## Data Flow

1. **User Input**: User enters video URL and selects format/quality preferences
2. **Request Validation**: Backend validates URL format and creates database record
3. **Background Processing**: Download manager processes request using yt-dlp
4. **Progress Updates**: Status and progress are updated in database during download
5. **File Storage**: Downloaded files are saved to `downloads/` directory
6. **Status Retrieval**: Frontend polls for status updates (implementation incomplete)

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-SQLAlchemy**: Database ORM integration
- **yt-dlp**: Video downloading and extraction
- **Werkzeug**: WSGI utilities and proxy fix

### Frontend Dependencies
- **Bootstrap 5**: CSS framework with dark theme
- **Feather Icons**: SVG icon library
- **Custom CSS**: Gradient styling and responsive design

## Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SESSION_SECRET`: Flask session encryption key
- `DOWNLOAD_FOLDER`: File storage location (defaults to `downloads/`)

### Database Configuration
- **Connection Pooling**: 300-second recycle time with pre-ping
- **Auto-creation**: Tables created automatically on startup
- **Migration Strategy**: Not implemented (uses create_all())

## Deployment Strategy

### Development Setup
- **Entry Point**: `main.py` runs Flask development server
- **Host Configuration**: Binds to 0.0.0.0:5000 for Replit compatibility
- **Debug Mode**: Enabled for development with detailed error logging

### Production Considerations
- **Proxy Support**: ProxyFix middleware for reverse proxy deployment
- **Secret Management**: Environment variable for session secret
- **File Storage**: Local filesystem (consider cloud storage for production)
- **Database**: SQLite suitable for development, PostgreSQL recommended for production

### Recent Updates (July 2025)
- **File Storage**: Changed from local `downloads/` to `/tmp/downloads` for cloud deployment
- **Automatic Cleanup**: Added file cleanup after download completion
- **Render Deployment**: Added full deployment configuration and documentation
- **Database Compatibility**: Added PostgreSQL URL format fixing for hosting services
- **Error Handling**: Improved error logging and file cleanup handling

### Known Limitations
- **Authentication**: No user authentication or download history per user
- **File Persistence**: Files stored temporarily and cleaned up automatically
- **Rate Limiting**: No built-in rate limiting for download requests
- **Platform Restrictions**: Some platforms may block server-side downloads

## Security Considerations

- **URL Validation**: Basic URL parsing and validation
- **File Storage**: Downloads stored in controlled directory
- **Session Security**: Configurable secret key for session management
- **Input Sanitization**: Basic form validation implemented