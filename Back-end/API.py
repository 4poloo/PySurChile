from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from PySURCHILE import obtener_config, actualizar_folio, actualizar_config, procesar_archivo

# Modelo para la configuración en JSON
class Config(BaseModel):
    ultimo_folio: int
    ultimo_registro: str
    ultima_hora: str

# Router de la API
router = APIRouter()

# Endpoint para consultar la configuración
@router.get("/config", response_model=Config)
def get_config():
    config = obtener_config()
    return config

# Endpoint para actualizar la configuración
@router.put("/config")
def update_config(config: Config):
    try:
        actualizar_folio(config.ultimo_folio)
        actualizar_config(config.ultimo_registro, config.ultima_hora)
        return {"mensaje": "Configuración actualizada exitosamente."}
    except Exception as e:
        return {"error": str(e)}

# Endpoint para procesar el archivo Excel cargado
@router.post("/procesar")
async def procesar_excel(file: UploadFile = File(...)):
    try:
        content = await file.read()
        resultado = procesar_archivo(content)

        if "error" in resultado:
            return {"error": resultado["error"]}
        return {"mensaje": resultado["mensaje"], "archivo_salida": resultado["archivo_salida"]}
    except Exception as e:
        return {"error": str(e)}
