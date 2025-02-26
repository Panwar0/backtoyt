from flask import Flask, jsonify, request
from flask_cors import CORS
from yt_dlp import YoutubeDL

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    page = int(request.args.get('page', 1))
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                f"ytsearch{page*20}:{query}",
                download=False
            )
        
        videos = []
        for entry in result['entries'][(page-1)*20:page*20]:
            videos.append({
                'id': entry['id'],
                'title': entry.get('title', 'No title'),
                'channel': entry.get('uploader', 'Unknown'),
                'duration': entry.get('duration_string', 'N/A'),
                'thumbnail': f"https://i.ytimg.com/vi/{entry['id']}/hqdefault.jpg"
            })
        
        return jsonify({'videos': videos})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
