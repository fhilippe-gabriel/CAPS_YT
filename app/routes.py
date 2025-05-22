import os
import uuid
import threading
from flask import Blueprint, render_template, request, send_file, jsonify
from datetime import datetime

from downloader.youtube_ytdlp import process_download
from .db import (
    increment_access, increment_download,
    increment_playlist_audio, increment_playlist_video,
    increment_music, increment_format,
    insert_log, get_metrics, reset_all_metrics
)
from .tasks import clear_downloads_folder, update_dependencies  # ✅ IMPORTAR update_dependencies

main = Blueprint('main', __name__)
download_progress = {}

@main.route('/', methods=['GET'])
def index():
    increment_access()
    insert_log("Acesso à página inicial")
    return render_template('index.html')

@main.route('/download', methods=['POST'])
def start_download():
    url = request.form.get('url', '').strip()
    format_type = request.form.get('format')
    resolution = request.form.get('resolution')
    is_playlist = request.form.get('playlist') == 'on'
    video_format = request.form.get('video_format')
    audio_format = request.form.get('audio_format')
    video_codec = request.form.get('video_codec', 'avc1')

    print(f"[DEBUG] URL recebida: '{url}'")

    if not url:
        return jsonify({"error": "URL não fornecida"}), 400

    if "youtube.com" not in url and "youtu.be" not in url:
        return jsonify({"error": "URL inválida. Forneça um link do YouTube."}), 400

    download_id = str(uuid.uuid4())
    download_progress[download_id] = {
        "progress": 0,
        "filename": None,
        "error": None
    }

    def download_task():
        try:
            filepath = process_download(
                url=url,
                format_type=format_type,
                resolution=resolution,
                is_playlist=is_playlist,
                video_format=video_format,
                audio_format=audio_format,
                progress_callback=lambda p: update_progress(download_id, p),
                video_codec=video_codec
            )
            download_progress[download_id]["filename"] = filepath
            increment_download()

            if is_playlist and format_type == "audio":
                increment_playlist_audio()
            elif is_playlist and format_type == "video":
                increment_playlist_video()
            elif format_type == "audio":
                increment_music()

            format_used = audio_format if format_type == "audio" else video_format
            increment_format(format_used)

            insert_log(f"Download concluído com sucesso: {filepath}")
        except Exception as e:
            error_msg = str(e)
            download_progress[download_id]["error"] = error_msg
            download_progress[download_id]["progress"] = -1
            insert_log(f"[ERRO] Falha ao processar download: {error_msg}")
            print(f"[ERRO] {error_msg}")

    threading.Thread(target=download_task).start()
    return jsonify({"download_id": download_id})

@main.route('/progress/<download_id>')
def check_progress(download_id):
    return jsonify(download_progress.get(download_id, {"error": "ID inválido"}))

@main.route('/download/file/<download_id>')
def download_file(download_id):
    progress_data = download_progress.get(download_id)
    if not progress_data:
        return "Download não encontrado", 404

    path = progress_data.get("filename")
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True)

    error = progress_data.get("error")
    if error:
        return f"Erro ao processar download: {error}", 500

    return "Arquivo não encontrado", 404

@main.route('/caps/source/270306/dash/metrics/view')
def show_metrics():
    metrics = get_metrics()
    return render_template('metrics.html', metrics=metrics)

@main.route('/force-clear-downloads', methods=['POST'])
def force_clear_downloads():
    clear_downloads_folder()
    insert_log("[MANUAL] Limpeza da pasta downloads forçada via painel.")
    return jsonify({"message": "Limpeza forçada da pasta downloads concluída com sucesso."}), 200

@main.route('/caps/source/270306/dash/metrics/reset', methods=['POST'])
def reset_metrics():
    reset_all_metrics()
    insert_log("[MANUAL] Todas as métricas e logs foram resetados manualmente.")
    return jsonify({"message": "Métricas e logs zerados com sucesso."}), 200

@main.route('/force-update-dependencies', methods=['POST'])  # ✅ NOVA ROTA
def force_update_dependencies():
    threading.Thread(target=update_dependencies).start()
    insert_log("[MANUAL] Atualização manual de dependências iniciada via painel.")
    return jsonify({"message": "Atualização de dependências iniciada com sucesso."}), 200

def update_progress(download_id, percent):
    if download_id in download_progress:
        download_progress[download_id]["progress"] = percent
