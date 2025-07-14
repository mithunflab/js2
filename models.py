from app import db
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Text, Boolean

class DownloadRequest(db.Model):
    id = db.Column(Integer, primary_key=True)
    url = db.Column(String(2048), nullable=False)
    title = db.Column(String(512))
    format_requested = db.Column(String(50), nullable=False)
    quality_requested = db.Column(String(50), nullable=False)
    status = db.Column(String(50), default='pending')  # pending, processing, completed, failed
    file_path = db.Column(String(512))
    error_message = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    completed_at = db.Column(DateTime)
    progress = db.Column(Integer, default=0)
    file_size = db.Column(String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'format_requested': self.format_requested,
            'quality_requested': self.quality_requested,
            'status': self.status,
            'file_path': self.file_path,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress': self.progress,
            'file_size': self.file_size
        }
