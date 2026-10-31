from fastapi import FastAPI, HTTPException
import yt_dlp
import os

app = FastAPI(title="Translate Player API", version="1.0")

@app.post("/processar-video/")
def processar_video(url: str):
    try:
        # Cria a pasta downloads se ela não existir
        os.makedirs("downloads", exist_ok=True)

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'skip_download': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id', 'video_desconhecido')
            titulo = info.get('title', 'Sem Título')

        return {
            "status": "sucesso",
            "titulo": titulo,
            "video_id": video_id,
            "mensagem": "Vídeo processado com sucesso pelo servidor!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "API do Translate Player Rodando com Sucesso! 🚀"}