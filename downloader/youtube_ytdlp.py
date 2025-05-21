import yt_dlp
import os
import uuid
import shutil

DOWNLOAD_PATH = "downloads"

def process_download(
    url,
    format_type='video',
    resolution=None,
    is_playlist=False,
    video_format=None,
    audio_format=None,
    progress_callback=None,
    video_codec=None
):
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    file_ext = audio_format if format_type == 'audio' else video_format
    if not file_ext:
        file_ext = 'mp3' if format_type == 'audio' else 'mp4'

    unique_id = str(uuid.uuid4())

    if is_playlist:
        playlist_temp_dir = os.path.join(DOWNLOAD_PATH, unique_id)
        os.makedirs(playlist_temp_dir, exist_ok=True)
        outtmpl = os.path.join(playlist_temp_dir, "%(title).200s.%(ext)s")
    else:
        outtmpl = os.path.join(DOWNLOAD_PATH, f"{unique_id}.%(ext)s")

    ydl_opts = {
        'outtmpl': outtmpl,
        'quiet': True,
        'merge_output_format': file_ext,
        'postprocessors': [],
        'progress_hooks': [lambda d: handle_progress(d, progress_callback)],
    }

    if format_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format or 'mp3',
            'preferredquality': '192',
        })

    else:
        codec_filter = video_codec if video_codec in ['avc1', 'vp9', 'av01'] else 'avc1'
        ydl_opts['format'] = (
            f"bestvideo[ext=mp4][vcodec^={codec_filter}][height<={resolution}]"
            f"+bestaudio[ext=m4a]/best"
        )

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    # PLAYLIST: compactar e retornar .zip
    if is_playlist:
        playlist_title = info.get('title', f"playlist_{unique_id}").strip().replace(' ', '_')
        playlist_title = ''.join(c for c in playlist_title if c.isalnum() or c in ('_', '-'))
        zip_path = os.path.join(DOWNLOAD_PATH, f"{playlist_title}.zip")
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', playlist_temp_dir)

        if progress_callback:
            progress_callback(100)

        return os.path.abspath(zip_path)

    # VÍDEO OU ÁUDIO ÚNICO
    video_title = info.get('title', f'video_{uuid.uuid4()}').strip().replace(' ', '_')
    video_title = ''.join(c for c in video_title if c.isalnum() or c in ('_', '-'))
    final_path = os.path.join(DOWNLOAD_PATH, f"{video_title}.{file_ext}")

    # Tenta localizar o arquivo com extensão gerada dinamicamente
    possible_files = os.listdir(DOWNLOAD_PATH)
    for f in possible_files:
        if f.startswith(unique_id) or video_title in f:
            real_ext = os.path.splitext(f)[-1].lower()
            full_path = os.path.join(DOWNLOAD_PATH, f)
            os.rename(full_path, final_path)
            if progress_callback:
                progress_callback(100)
            return os.path.abspath(final_path)

    raise FileNotFoundError(f"Arquivo convertido não encontrado com extensão .{file_ext}")


def handle_progress(d, callback):
    if d['status'] == 'downloading' and callback:
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
        downloaded = d.get('downloaded_bytes', 0)
        percent = int(downloaded / total * 100)
        callback(percent)
