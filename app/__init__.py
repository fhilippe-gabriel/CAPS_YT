from flask import Flask
from .db import init_db           # Inicializa banco de dados
from .tasks import start_scheduler  # Inicia a limpeza da pasta downloads
from .routes import main            # Blueprint com as rotas principais

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Inicializa o banco de dados (caso não exista)
        init_db()
        print("[✔] Banco de dados inicializado com sucesso.")

        # Inicia o agendador de limpeza da pasta de downloads
        start_scheduler()
        print("[✔] Agendador de limpeza da pasta 'downloads' ativado (a cada 12h).")

    # Registra as rotas
    app.register_blueprint(main)
    print("[✔] Blueprint de rotas registrado.")

    return app
