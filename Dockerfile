# Usa imagem oficial leve do Python
FROM python:3.11-slim

# Instala dependências do sistema e limpa cache depois
RUN apt update && apt install -y ffmpeg && apt clean && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia todos os arquivos para dentro do container
COPY . .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Flask usa
EXPOSE 5000

# Define variável de ambiente para produção (evita warnings do Flask)
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
