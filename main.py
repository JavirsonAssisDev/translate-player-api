from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = FastAPI(title="Translate Player API", version="1.0")

def extrair_video_id(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None

@app.post("/processar-video/")
def processar_video(url: str):
    video_id = extrair_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Link do YouTube inválido.")
    
    try:
        dados_legenda = None
        
        # Tenta a abordagem padrão de obter transcrição
        try:
            dados_legenda = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-orig'])
        except Exception:
            try:
                # Tenta listar se o método estiver disponível
                lista = YouTubeTranscriptApi.list_transcripts(video_id)
                for tr in lista:
                    dados_legenda = tr.fetch()
                    break
            except Exception as inner_e:
                raise HTTPException(status_code=500, detail=f"Falha interna na biblioteca: {str(inner_e)}")
                
        if not dados_legenda:
            raise HTTPException(status_code=404, detail="Nenhuma legenda encontrada para este vídeo.")
            
        texto_completo = " ".join([item['text'] for item in dados_legenda])
        
        return {
            "status": "sucesso",
            "titulo": f"Vídeo YouTube ({video_id})",
            "video_id": video_id,
            "legenda": dados_legenda,
            "texto_plano": texto_completo,
            "mensagem": "Legendas extraídas com sucesso pelo servidor!"
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter legendas: {str(e)}")

@app.get("/")
def home():
    return {"status": "API do Translate Player Rodando com Sucesso! 🚀"}