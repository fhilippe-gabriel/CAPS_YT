import os
import subprocess
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from .db import insert_log  # Loga ações no banco de dados

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_FOLDER = BASE_DIR / 'downloads'
REQUIREMENTS_FILE = BASE_DIR / 'requirements.txt'

def clear_downloads_folder():
    """Remove todos os arquivos da pasta de downloads."""
    if not DOWNLOAD_FOLDER.exists():
        print("[INFO] Pasta 'downloads' não encontrada.")
        return

    arquivos_removidos = 0
    for file_path in DOWNLOAD_FOLDER.iterdir():
        try:
            if file_path.is_file():
                file_path.unlink()
                arquivos_removidos += 1
                print(f"[LIMPEZA] Arquivo removido: {file_path}")
        except Exception as e:
            print(f"[ERRO] Falha ao remover {file_path}: {e}")

    log_msg = f"[AUTO] Limpeza automática da pasta downloads: {arquivos_removidos} arquivos removidos."
    print(log_msg)
    insert_log(log_msg)

def update_dependencies():
    """Atualiza os pacotes Python com base no requirements.txt."""
    print("[DEPENDÊNCIAS] Iniciando atualização de dependências via requirements.txt...")
    try:
        result = subprocess.run(
            ["pip", "install", "--upgrade", "-r", str(REQUIREMENTS_FILE)],
            check=True,
            capture_output=True,
            text=True
        )
        msg = "[AUTO] Dependências atualizadas com sucesso."
        print(result.stdout)
        print(f"[DEPENDÊNCIAS] {msg}")
        insert_log(msg)
    except subprocess.CalledProcessError as e:
        err_msg = f"[ERRO] Falha ao atualizar dependências: {e.stderr if e.stderr else str(e)}"
        print(err_msg)
        insert_log(err_msg)

def start_scheduler():
    """Inicia as tarefas agendadas de limpeza e atualização."""
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=clear_downloads_folder, trigger="interval", hours=12)
    scheduler.add_job(func=update_dependencies, trigger="interval", hours=24)
    scheduler.start()
    print("[AGENDADOR] Tarefas agendadas: limpeza (12h) e atualização de dependências (24h).")
