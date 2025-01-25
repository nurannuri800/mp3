from flask import Flask, request, render_template, send_file
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    media_type = request.form['media_type']  # video veya audio
    quality = request.form['quality']       # kalite
    format_type = request.form['format']    # format

    if not url:
        return "URL gerekli!", 400

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }

    if media_type == 'audio':
        ydl_opts['format'] = f'bestaudio[abr<={quality}]'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_type,
            'preferredquality': quality,
        }]
    else:
        ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best'
        ydl_opts['merge_output_format'] = format_type

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            if media_type == 'audio':
                filename = filename.replace('.webm', f'.{format_type}')
            else:
                filename = filename.replace('.webm', f'.{format_type}')

            # Dosyayı kullanıcıya gönderirken indirme penceresi aç
            return send_file(
                filename,
                as_attachment=True,
                download_name=os.path.basename(filename),
            )
    except Exception as e:
        return f"Hata: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
