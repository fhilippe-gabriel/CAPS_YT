# 🎬 CAPS - YT Downloader

> Aplicação Web para download de vídeos e áudios do YouTube com suporte a playlists, formatos personalizados e codificações específicas. Ideal para uso educacional, pessoal ou profissional.

---

## 🇧🇷 Instruções em Português

### ⚙️ Funcionalidades

- ✅ Download de **vídeos** com escolha de resolução e formato (MP4/MKV)
- ✅ Download de **áudios** com escolha de formato (MP3/M4A/WAV)
- ✅ Suporte a **playlists completas**
- ✅ Escolha de **codec de vídeo**: H.264 (avc1), VP9, AV1
- ✅ Interface moderna em **dark mode**
- ✅ Rodando automaticamente em **Docker**

---

### 🚀 Como rodar o projeto com Docker

#### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/YT_Downloader_ABC.git
cd YT_Downloader_ABC
```

#### 2. Construa e execute com Docker Compose:

```bash
docker-compose up --build -d
```

#### 3. Acesse no navegador:

```
http://localhost:5000
```

---

### 📁 Estrutura do Projeto

```
YT_Downloader_ABC/
├── app/
│   ├── static/            # Arquivos CSS e ícones
│   ├── templates/         # HTMLs (index.html)
│   ├── downloader/        # Lógica com yt-dlp
│   ├── routes.py          # Rotas principais
│   ├── db.py              # Banco de dados SQLite
│   ├── tasks.py           # Agendador de limpeza de arquivos
│   └── __init__.py        # Inicializador Flask
├── downloads/             # Arquivos baixados
├── metrics.sqlite         # Banco de dados persistente
├── Dockerfile             # Imagem Docker
├── docker-compose.yml     # Orquestração com Docker
├── requirements.txt       # Dependências do projeto
└── run.py                 # Inicializador principal
```

---

## 🇺🇸 English Instructions

### ⚙️ Features

- ✅ Download **videos** with resolution and format choice (MP4/MKV)
- ✅ Download **audio** with format selection (MP3/M4A/WAV)
- ✅ Support for **full playlist downloads**
- ✅ Select **video codec**: H.264 (avc1), VP9, AV1
- ✅ Clean and modern **dark mode interface**
- ✅ Runs automatically using **Docker**

---

### 🚀 How to run this project with Docker

#### 1. Clone this repository:

```bash
git clone https://github.com/your-username/YT_Downloader_ABC.git
cd YT_Downloader_ABC
```

#### 2. Build and start using Docker Compose:

```bash
docker-compose up --build -d
```

#### 3. Open in your browser:

```
http://localhost:5000
```

---

### 📁 Project Structure

See Portuguese section above ☝️

---

🔧 This project uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) under the hood for video and audio downloading.

---

Developed with ❤️ by Fhilippe Silva.
