import os
import yt_dlp
import logging
from app import app, db
from models import DownloadRequest
from datetime import datetime

class DownloadManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_download(self, download_id):
        """Process a download request in background"""
        try:
            with app.app_context():
                download_request = DownloadRequest.query.get(download_id)
                if not download_request:
                    self.logger.error(f"Download request {download_id} not found")
                    return
                
                # Update status to processing
                download_request.status = 'processing'
                download_request.progress = 0
                db.session.commit()
                
                # Configure yt-dlp options based on format
                output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], f'%(title)s.%(ext)s')
                
                # Ensure download folder exists
                os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
                
                ydl_opts = {
                    'outtmpl': output_path,
                    'restrictfilenames': True,
                    'progress_hooks': [lambda d: self.progress_hook(d, download_id)],
                }
                
                # Set format based on user selection
                if download_request.format_requested == 'video+audio':
                    if download_request.quality_requested == 'best':
                        ydl_opts['format'] = 'best[ext=mp4]/best'
                    else:
                        ydl_opts['format'] = f'best[height<={download_request.quality_requested}][ext=mp4]/best[height<={download_request.quality_requested}]'
                elif download_request.format_requested == 'video_only':
                    if download_request.quality_requested == 'best':
                        ydl_opts['format'] = 'best[vcodec!=none][acodec=none]/best'
                    else:
                        ydl_opts['format'] = f'best[height<={download_request.quality_requested}][vcodec!=none][acodec=none]'
                elif download_request.format_requested == 'audio_only':
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                elif download_request.format_requested == 'subtitles_only':
                    ydl_opts['writesubtitles'] = True
                    ydl_opts['writeautomaticsub'] = True
                    ydl_opts['subtitleslangs'] = ['en', 'en-US', 'en-GB']
                    ydl_opts['subtitlesformat'] = 'srt'
                    ydl_opts['skip_download'] = True
                
                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract info first
                    info = ydl.extract_info(download_request.url, download=False)
                    
                    # Update title
                    download_request.title = info.get('title', 'Unknown')
                    db.session.commit()
                    
                    # Download
                    ydl.download([download_request.url])
                    
                    # Find the downloaded file
                    downloaded_file = self.find_downloaded_file(info, ydl_opts, download_request.format_requested)
                    
                    if downloaded_file and os.path.exists(downloaded_file):
                        # Get file size
                        file_size = os.path.getsize(downloaded_file)
                        file_size_mb = round(file_size / (1024 * 1024), 2)
                        
                        # Update database
                        download_request.status = 'completed'
                        download_request.file_path = downloaded_file
                        download_request.completed_at = datetime.utcnow()
                        download_request.progress = 100
                        download_request.file_size = f"{file_size_mb} MB"
                        db.session.commit()
                        
                        self.logger.info(f"Download completed: {downloaded_file}")
                    else:
                        raise Exception("Downloaded file not found")
                        
        except Exception as e:
            self.logger.error(f"Download failed for {download_id}: {str(e)}")
            with app.app_context():
                download_request = DownloadRequest.query.get(download_id)
                if download_request:
                    download_request.status = 'failed'
                    download_request.error_message = str(e)
                    db.session.commit()
    
    def progress_hook(self, d, download_id):
        """Update download progress"""
        try:
            if d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    progress = int((d['downloaded_bytes'] / d['total_bytes']) * 100)
                elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                    progress = int((d['downloaded_bytes'] / d['total_bytes_estimate']) * 100)
                else:
                    progress = 50  # Unknown progress
                
                with app.app_context():
                    download_request = DownloadRequest.query.get(download_id)
                    if download_request:
                        download_request.progress = progress
                        db.session.commit()
        except Exception as e:
            self.logger.error(f"Progress update error: {str(e)}")
    
    def find_downloaded_file(self, info, ydl_opts, format_type):
        """Find the downloaded file based on info and options"""
        try:
            base_path = app.config['DOWNLOAD_FOLDER']
            title = info.get('title', 'Unknown')
            
            # Clean title for filename
            import re
            clean_title = re.sub(r'[^\w\s-]', '', title).strip()
            clean_title = re.sub(r'[-\s]+', '-', clean_title)
            
            # Common extensions based on format
            if format_type == 'audio_only':
                extensions = ['.mp3', '.m4a', '.webm', '.ogg']
            elif format_type == 'subtitles_only':
                extensions = ['.srt', '.vtt', '.ass']
            else:
                extensions = ['.mp4', '.webm', '.mkv', '.avi', '.mov']
            
            # Search for files
            for ext in extensions:
                for filename in os.listdir(base_path):
                    if filename.endswith(ext) and (clean_title.lower() in filename.lower() or filename.startswith(clean_title)):
                        return os.path.join(base_path, filename)
            
            # Fallback: return the most recent file with matching extension
            recent_files = []
            for filename in os.listdir(base_path):
                filepath = os.path.join(base_path, filename)
                if os.path.isfile(filepath) and any(filename.endswith(ext) for ext in extensions):
                    recent_files.append((filepath, os.path.getmtime(filepath)))
            
            if recent_files:
                recent_files.sort(key=lambda x: x[1], reverse=True)
                return recent_files[0][0]
            
            return None
            
        except Exception as e:
            self.logger.error(f"File search error: {str(e)}")
            return None
