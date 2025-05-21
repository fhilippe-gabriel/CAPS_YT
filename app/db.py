import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / 'metrics.sqlite'

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Tabela de métricas principais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_accesses INTEGER DEFAULT 0,
                total_downloads INTEGER DEFAULT 0,
                playlist_audio_downloads INTEGER DEFAULT 0,
                playlist_video_downloads INTEGER DEFAULT 0,
                music_downloads INTEGER DEFAULT 0,
                format_mp3 INTEGER DEFAULT 0,
                format_m4a INTEGER DEFAULT 0,
                format_wav INTEGER DEFAULT 0,
                format_mp4 INTEGER DEFAULT 0,
                format_mkv INTEGER DEFAULT 0
            )
        ''')
        # Garante pelo menos uma linha de contagem
        cursor.execute("SELECT COUNT(*) FROM metrics")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO metrics DEFAULT VALUES")

        # Tabela de logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

def update_metric(column):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE metrics SET {column} = {column} + 1 WHERE id = 1")
        conn.commit()

# Funções de incremento específicas
def increment_access():
    update_metric("total_accesses")

def increment_download():
    update_metric("total_downloads")

def increment_playlist_audio():
    update_metric("playlist_audio_downloads")

def increment_playlist_video():
    update_metric("playlist_video_downloads")

def increment_music():
    update_metric("music_downloads")

def increment_format(format_name):
    column = f"format_{format_name.lower()}"
    allowed = ["mp3", "m4a", "wav", "mp4", "mkv"]
    if column in [f"format_{f}" for f in allowed]:
        update_metric(column)

def insert_log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (timestamp, message) VALUES (?, ?)", (timestamp, message))
        conn.commit()

def get_metrics():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                total_accesses, total_downloads, 
                playlist_audio_downloads, playlist_video_downloads, 
                music_downloads, 
                format_mp3, format_m4a, format_wav, format_mp4, format_mkv 
            FROM metrics WHERE id = 1
        """)
        (access, downloads, pa, pv, music, mp3, m4a, wav, mp4, mkv) = cursor.fetchone()

        cursor.execute("SELECT timestamp, message FROM logs ORDER BY id DESC LIMIT 50")
        logs = cursor.fetchall()

        return {
            "access_count": access,
            "total_downloads": downloads,
            "playlist_audio": pa,
            "playlist_video": pv,
            "music_downloads": music,
            "formats": {
                "mp3": mp3,
                "m4a": m4a,
                "wav": wav,
                "mp4": mp4,
                "mkv": mkv
            },
            "logs": logs[::-1]
        }

def reset_all_metrics():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE metrics SET
                total_accesses = 0,
                total_downloads = 0,
                playlist_audio_downloads = 0,
                playlist_video_downloads = 0,
                music_downloads = 0,
                format_mp3 = 0,
                format_m4a = 0,
                format_wav = 0,
                format_mp4 = 0,
                format_mkv = 0
            WHERE id = 1
        ''')
        cursor.execute('DELETE FROM logs')
        conn.commit()
