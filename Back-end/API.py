from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PySURCHILE import *
import json
import os

app = FastAPI()

class Item(BaseModel):
    nombre: str
    descripcion: str

#FUNCIONES API
# Función para validar que el archivo es un .xlsx
def validar_excel(file: UploadFile):
    # Verificar que el archivo tenga extensión .xlsx
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un archivo Excel (.xlsx)")

    # Validar el tipo MIME del archivo (Excel)
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(status_code=400, detail="El archivo debe ser de tipo Excel (.xlsx)")

###############################################################################################################

# END POINTS

# Endpoint para obtener la fecha del ultimo regristro procesado
@app.get("/ultimo-registro/")
async def get_ultimo_registro():
    try:
        # Llamar a la función obtener_ultimo_registro
        resultado = obtener_ultimo_registro()
        
        if "error" in resultado:
            # Si el resultado contiene un error, devolverlo como respuesta
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        # Si todo está bien, devolver el último registro
        return {"ultimo_registro": resultado["ultimo_registro"]}

    except Exception as e:
        # Capturar cualquier otro error
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

# Endpoint para obtener el folio actual
@app.get("/ultimo-folio/")
async def get_ultimo_folio():
    try:
        # Llamar a la función obtener_ultimo_folio
        resultado = obtener_ultimo_folio()
        
        if "error" in resultado:
            # Si el resultado contiene un error, devolverlo como respuesta
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        # Si todo está bien, devolver el último folio
        return {"ultimo_folio": resultado["ultimo_folio"]}

    except Exception as e:
        # Capturar cualquier otro error
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

# Endpoint para cambiar el folio
@app.put("/folio/")
def cambiar_folio(nuevo_folio: int):
    try:
        with open("config.json", "r+") as file:
            data = json.load(file)
            data["folio"] = nuevo_folio
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        return {"message": "Número de folio actualizado", "nuevo_folio": nuevo_folio}
    except Exception as e:
        return {"error": str(e)}

# Endpoint para cambiar la fecha comparativa
@app.put("/fecha/")
def cambiar_fecha(nueva_fecha: str):
    try:
        with open("config.json", "r+") as file:
            data = json.load(file)
            data["fecha"] = nueva_fecha
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        return {"message": "Fecha actualizada", "nueva_fecha": nueva_fecha}
    except Exception as e:
        return {"error": str(e)}

# Endpoint para procesar Excel
@app.post("/procesar-archivo/")
async def procesar_archivo_api(file: UploadFile):
    try:
        # Validar el archivo
        validar_excel(file)

        # 1. Guardar el archivo subido temporalmente
        ruta_temporal = f"./temp/{file.filename}"
        with open(ruta_temporal, "wb") as f:
            f.write(await file.read())

        # 2. Llamar a la función procesar_archivo_completo desde tu módulo
        resultado = procesar_archivo_completo(ruta_temporal)
        
        # 3. Verificar si hubo procesamiento exitoso
        if "archivo_salida" in resultado:
            archivo_salida = resultado["archivo_salida"]
            return FileResponse(
                archivo_salida,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=os.path.basename(archivo_salida),
            )
        else:
            return {"mensaje": resultado["mensaje"]}
    except HTTPException as http_exc:
        # Manejo de errores específicos de validación
        return {"error": http_exc.detail}
    except Exception as e:
        # Manejo de otros errores
        return {"error": str(e)}