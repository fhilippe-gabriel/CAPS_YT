# Usa imagem oficial leve do Python
FROM python:3.11-slim

# Instala dependências do sistema e limpa cache depois
RUN apt update && apt install -y ffmpeg && apt clean && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia apenas os requirements primeiro para aproveitar cache em builds futuros
COPY requirements.txt .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia os demais arquivos da aplicação
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Variáveis de ambiente do Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
