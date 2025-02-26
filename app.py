from flask import Flask, jsonify, request
from flask_cors import CORS
from yt_dlp import YoutubeDL
from datetime import datetime

app = Flask(__name__)
CORS(app)

def format_upload_date(upload_date):
    """Convert YouTube upload date (YYYYMMDD) to a readable format."""
    try:
        date_obj = datetime.strptime(upload_date, '%Y%m%d')
        return date_obj.strftime('%b %d, %Y')  # Example: "Oct 15, 2023"
    except:
        return 'N/A'

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    page = int(request.args.get('page', 1))
    
    # Step 1: Fetch search results
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(
            f"ytsearch{page*20}:{query}",
            download=False
        )
    
    videos = []
    for entry in result['entries'][(page-1)*20:page*20]:
        # Step 2: Fetch full details for each video
        video_id = entry['id']
        video_details = get_video_details(video_id)
        
        videos.append({
            'id': video_id,
            'title': entry.get('title', 'No title'),
            'channel': entry.get('uploader', 'Unknown'),
            'duration': entry.get('duration_string', 'N/A'),
            'thumbnail': f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            'upload_date': format_upload_date(video_details.get('upload_date', ''))
        })
    
    return jsonify({'videos': videos})

def get_video_details(video_id):
    """Fetch full details for a single video."""
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )
            return result
        except:
            return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
