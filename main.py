from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Translate Player AI API", version="2.0")

# Modelo para receber o texto que o app quer traduzir
class TextoRequest(BaseModel):
    texto: str

# Modelo para o catálogo de vídeos online (se quiser usar no futuro)
class VideoDisponivel(BaseModel):
    id: str
    titulo: str
    url_video: str
    url_legenda: str

CATALOGO_VIDEOS = [
    VideoDisponivel(
        id="1",
        titulo="Exemplo de Aula - Lesson 1",
        url_video="https://exemplo.com/videos/lesson1.mp4",
        url_legenda="https://exemplo.com/videos/lesson1.srt"
    )
]

@app.get("/")
def home():
    return {"status": "API do Translate Player (Modo Texto Leve) Rodando com Sucesso! 🚀"}

@app.get("/videos-disponiveis", response_model=List[VideoDisponivel])
def listar_videos():
    return CATALOGO_VIDEOS

@app.post("/traduzir-texto/")
def traduzir_texto(dados: TextoRequest):
    try:
        # Aqui você pode integrar uma biblioteca de tradução simples (como googletrans)
        # ou por enquanto retornar uma resposta simulada para testar a ponte com o app.
        texto_original = dados.texto
        
        # Simulação de tradução (substituiremos por tradução real em breve)
        texto_traduzido = f"[Tradução]: {texto_original}"

        return {
            "status": "sucesso",
            "texto_original": texto_original,
            "texto_traduzido": texto_traduzido
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao traduzir texto: {str(e)}")