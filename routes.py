import os
import json
import threading
from urllib.parse import urlparse
from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
from app import app, db
from models import DownloadRequest
from download_manager import DownloadManager
from datetime import datetime
import logging

# Add debug logging for template directory
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

download_manager = DownloadManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get('url', '').strip()
        format_type = request.form.get('format', 'video+audio')
        quality = request.form.get('quality', 'best')

        if not url:
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('index'))

        # Basic URL validation
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('index'))

        # Create download request
        download_request = DownloadRequest(
            url=url,
            format_requested=format_type,
            quality_requested=quality,
            status='pending'
        )

        db.session.add(download_request)
        db.session.commit()

        # Start download in background thread
        thread = threading.Thread(
            target=download_manager.process_download,
            args=(download_request.id,)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'download_id': download_request.id,
            'message': 'Download started successfully'
        })

    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/status/<int:download_id>')
def get_status(download_id):
    try:
        download_request = DownloadRequest.query.get_or_404(download_id)
        return jsonify(download_request.to_dict())
    except Exception as e:
        app.logger.error(f"Status check error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_file/<int:download_id>')
def download_file(download_id):
    try:
        download_request = DownloadRequest.query.get_or_404(download_id)

        if download_request.status != 'completed' or not download_request.file_path:
            flash('File not ready for download', 'error')
            return redirect(url_for('index'))

        file_path = download_request.file_path
        if not os.path.exists(file_path):
            flash('File not found', 'error')
            return redirect(url_for('index'))

        # Get original filename
        filename = os.path.basename(file_path)

        def remove_file_after_send():
            """Remove file after successful download"""
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    app.logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                app.logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")

        # Schedule file cleanup after download
        import threading
        cleanup_thread = threading.Timer(5.0, remove_file_after_send)
        cleanup_thread.daemon = True
        cleanup_thread.start()

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        app.logger.error(f"File download error: {str(e)}")
        flash('Error downloading file', 'error')
        return redirect(url_for('index'))

@app.route('/recent_downloads')
def recent_downloads():
    try:
        downloads = DownloadRequest.query.order_by(DownloadRequest.created_at.desc()).limit(10).all()
        return jsonify([download.to_dict() for download in downloads])
    except Exception as e:
        app.logger.error(f"Recent downloads error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/clear_completed')
def clear_completed():
    try:
        # Delete completed downloads older than 1 hour
        from datetime import datetime, timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=1)

        old_downloads = DownloadRequest.query.filter(
            DownloadRequest.status == 'completed',
            DownloadRequest.completed_at < cutoff_time
        ).all()

        for download in old_downloads:
            if download.file_path and os.path.exists(download.file_path):
                try:
                    os.remove(download.file_path)
                except Exception as e:
                    app.logger.warning(f"Failed to remove file {download.file_path}: {str(e)}")
            db.session.delete(download)

        db.session.commit()
        return jsonify({'success': True, 'cleared': len(old_downloads)})

    except Exception as e:
        app.logger.error(f"Clear completed error: {str(e)}")
        return jsonify({'error': str(e)}), 500