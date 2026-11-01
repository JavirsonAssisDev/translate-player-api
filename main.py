from fastapi import FastAPI, UploadFile, File, HTTPException
from faster_whisper import WhisperModel
import shutil
import os

app = FastAPI(title="Translate Player AI API", version="2.0")

# Carrega o modelo Whisper ("base" é leve, rápido e ideal para servidores gratuitos)
# Ele é descarregado automaticamente na primeira vez que o servidor arranca.
model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

@app.get("/")
def home():
    return {"status": "API do Translate Player (Com Faster-Whisper) Rodando com Sucesso! 🚀"}

@app.post("/traduzir-trecho/")
async def traduzir_trecho(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Guarda temporariamente o pedaço de áudio enviado pelo app Android
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Processa o áudio com o Faster-Whisper traduzindo diretamente para o inglês/português
        # task="translate" traduz o áudio falado para o inglês (ou podemos omitir para manter o idioma original ou traduzir)
        segments, info = model.translate(temp_file_path)
        
        texto_traduzido = " ".join([segment.text for segment in segments])
        
        return {
            "status": "sucesso",
            "idioma_detectado": info.language,
            "texto_traduzido": texto_traduzido.strip()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar áudio com IA: {str(e)}")
        
    finally:
        # Apaga o arquivo temporário do servidor para não ocupar espaço em disco
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)