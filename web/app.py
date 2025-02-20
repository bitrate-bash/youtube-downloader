from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from youtube_downloader import download_video
import threading
from typing import Dict, List
import time

app = Flask(__name__)
CORS(app)

# Global variables to track downloads
active_downloads: Dict[str, Dict] = {}
download_history: List[Dict] = []

def get_download_path() -> str:
    """Get the download directory path from settings or use default."""
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                return settings.get('output_directory', os.path.join(os.path.dirname(__file__), '..', 'output'))
    except Exception:
        pass
    return os.path.join(os.path.dirname(__file__), '..', 'output')

def download_manager(download_id: str, url: str, output_dir: str):
    """Manage the download process for a single video."""
    try:
        active_downloads[download_id]['status'] = 'downloading'
        success = download_video(url, output_dir)
        
        if success:
            active_downloads[download_id]['status'] = 'completed'
            active_downloads[download_id]['progress'] = 100
        else:
            active_downloads[download_id]['status'] = 'failed'
            active_downloads[download_id]['error'] = 'Download failed'
            
    except Exception as e:
        active_downloads[download_id]['status'] = 'failed'
        active_downloads[download_id]['error'] = str(e)
    
    # Add to history
    download_history.append(active_downloads[download_id])
    # Keep only last 100 downloads in history
    while len(download_history) > 100:
        download_history.pop(0)
    
    # Remove from active downloads after 5 minutes
    time.sleep(300)
    if download_id in active_downloads:
        del active_downloads[download_id]

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def start_download():
    """Start a new download."""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        if not urls:
            return jsonify({'error': 'No URLs provided'}), 400

        output_dir = get_download_path()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        download_ids = []
        for url in urls:
            download_id = str(int(time.time() * 1000))  # Timestamp as ID
            active_downloads[download_id] = {
                'id': download_id,
                'url': url,
                'status': 'starting',
                'progress': 0,
                'timestamp': time.time(),
                'error': None
            }
            download_ids.append(download_id)
            # Start download in background
            threading.Thread(
                target=download_manager,
                args=(download_id, url, output_dir),
                daemon=True
            ).start()

        return jsonify({
            'message': 'Downloads started',
            'download_ids': download_ids
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<download_id>')
def get_status(download_id):
    """Get the status of a specific download."""
    if download_id in active_downloads:
        return jsonify(active_downloads[download_id])
    
    # Check history if not active
    for download in reversed(download_history):
        if download['id'] == download_id:
            return jsonify(download)
    
    return jsonify({'error': 'Download not found'}), 404

@app.route('/api/downloads')
def get_downloads():
    """Get all active downloads and recent history."""
    return jsonify({
        'active': list(active_downloads.values()),
        'history': download_history
    })

@app.route('/api/output-dir')
def get_output_dir():
    """Get the current output directory."""
    return jsonify({'path': get_download_path()})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 