import os
from apscheduler.schedulers.background import BackgroundScheduler

# Caminho absoluto para a pasta 'downloads' na raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')

def clear_downloads_folder():
    if not os.path.exists(DOWNLOAD_FOLDER):
        print("[INFO] Pasta 'downloads' não encontrada.")
        return

    arquivos_removidos = 0
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                arquivos_removidos += 1
                print(f"[LIMPEZA] Arquivo removido: {file_path}")
        except Exception as e:
            print(f"[ERRO] Falha ao remover {file_path}: {e}")

    print(f"[LIMPEZA] Total de arquivos removidos: {arquivos_removidos}")

def start_scheduler():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=clear_downloads_folder, trigger="interval", hours=12)
    scheduler.start()
    print("[AGENDADOR] Limpeza automática de downloads agendada a cada 12 horas.")
