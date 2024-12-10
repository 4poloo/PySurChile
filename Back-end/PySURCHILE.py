import pandas as pd
import openpyxl
import json
import os

# Ruta del archivo de configuración
CONFIG_FILE = "config.json"

# Leer o inicializar archivo de configuración
def obtener_ultimo_folio():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as config:
            json.dump({"ultimo_folio": 1000, "ultimo_registro": ""}, config)
        return {"ultimo_folio": 1000}
    try:
        with open(CONFIG_FILE, "r") as config:
            data = json.load(config)
        return {"ultimo_folio": data.get("ultimo_folio", 1000)}
    except json.JSONDecodeError:
        raise ValueError("Error al leer el archivo de configuración.")

# Obtener última fecha registrada
def obtener_ultimo_registro():
    if not os.path.exists(CONFIG_FILE):
        return {"error": "El archivo de configuración no existe."}
    try:
        with open(CONFIG_FILE, "r") as config:
            data = json.load(config)
        return data.get("ultimo_registro", "")
    except json.JSONDecodeError:
        return {"error": "Error al leer el archivo de configuración."}

# Actualizar el último registro y folio en el JSON
def actualizar_ultimo_folio_y_registro(nuevo_folio, ultimo_registro):
    try:
        if not isinstance(ultimo_registro, str):
            ultimo_registro = ultimo_registro.strftime('%Y-%m-%d %H:%M:%S')
        with open(CONFIG_FILE, "w") as config:
            json.dump({"ultimo_folio": nuevo_folio, "ultimo_registro": ultimo_registro}, config)
    except Exception as e:
        return {"error": f"Error al actualizar el archivo de configuración: {str(e)}"}

def procesar_archivo_excel(ruta_archivo, ultimo_registro):
    try:
        wb = openpyxl.load_workbook(ruta_archivo, data_only=True)  # Ignorar estilos al cargar
        sheet = wb.active
        data = sheet.values
        columns = next(data)
        df = pd.DataFrame(data, columns=columns)
    except Exception as e:
        raise ValueError(f"Error al leer el archivo: {e}")

    columnas_requeridas = ['PRODUCTO', 'OT', 'UNID. DISP.', 'FECHA RECIBO']
    if not all(col in df.columns for col in columnas_requeridas):
        raise ValueError(f"El archivo debe contener las columnas: {', '.join(columnas_requeridas)}")

    # Procesamiento de columnas
    df['UNID. DISP.'] = pd.to_numeric(df['UNID. DISP.'], errors='coerce')
    df['OT'] = df['OT'].apply(lambda x: x[3:] if isinstance(x, str) and x.startswith('OT-') else x)
    df['FECHA RECIBO'] = pd.to_datetime(df['FECHA RECIBO'], errors='coerce')

    # Guardar la primera fecha del archivo
    fecha_primera = df['FECHA RECIBO'].max()

    # Filtrar por fecha
    if ultimo_registro:
        fecha_registrada = pd.to_datetime(ultimo_registro)
        df = df[df['FECHA RECIBO'] > fecha_registrada]

    if df.empty:
        return None, None, fecha_primera

    # Ordenar y agrupar datos
    df = df.sort_values(by='FECHA RECIBO', ascending=False)
    resultado_agrupado = df.groupby(['PRODUCTO', 'OT'], as_index=False).agg({
        'UNID. DISP.': 'sum',
        'FECHA RECIBO': 'min'
    })

    return resultado_agrupado.values.tolist(), fecha_primera.strftime('%Y-%m-%d %H:%M:%S'), fecha_primera

# Rellenar plantilla de Excel
def rellenar_plantilla(datos_array, ruta_plantilla, ruta_salida_base, fecha_primera):
    try:
        wb = openpyxl.load_workbook(ruta_plantilla)
        ws = wb.active
    except Exception as e:
        raise ValueError(f"Error al cargar la plantilla: {e}")

    # Limpiar filas existentes
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=2, max_col=23):
        for cell in row:
            cell.value = None

    # Obtener último folio
    ultimo_folio = obtener_ultimo_folio()["ultimo_folio"]

    # Agregar datos
    for i, (producto, ot, cantidad, fecha) in enumerate(datos_array, start=1):
        fila = 2 + i - 1
        ws[f"B{fila}"] = ultimo_folio + i - 1
        ws[f"U{fila}"] = producto
        ws[f"W{fila}"] = cantidad
        ws[f"O{fila}"] = ot
        ws[f"D{fila}"] = 10
        ws[f"C{fila}"] = pd.to_datetime(fecha).strftime('%d/%m/%Y')
        ws[f"F{fila}"] = 77757460

    # Guardar archivo
    try:
        nuevo_folio = ultimo_folio + len(datos_array)
        
        # Aquí usamos fecha_primera
        fecha_referencia = pd.to_datetime(fecha_primera).strftime('%Y-%m-%d %H:%M:%S')
        
        nombre_salida = f"{ruta_salida_base}_{pd.to_datetime(fecha_referencia).strftime('%d_%m')}.xlsx"
        wb.save(nombre_salida)
        
        # Actualizar el archivo JSON con el nuevo folio y la fecha de referencia correcta
        actualizar_ultimo_folio_y_registro(nuevo_folio, fecha_referencia)
        return nombre_salida
    except Exception as e:
        raise ValueError(f"Error al guardar el archivo: {e}")

# Procesar archivo completo
def procesar_archivo_completo(ruta_entrada):
    try:
        ultimo_registro = obtener_ultimo_registro()
        datos, nuevo_registro, fecha_primera = procesar_archivo_excel(ruta_entrada, ultimo_registro)
        if datos:
            ruta_plantilla = "./plantilla/Plantilla_ERP.xlsx"
            ruta_salida_base = "./plantilla/CARGA_PT"
            archivo_generado = rellenar_plantilla(datos, ruta_plantilla, ruta_salida_base, fecha_primera)
            return {
                "mensaje": "Procesamiento exitoso",
                "ultimo_registro": nuevo_registro,
                "archivo_salida": archivo_generado,
            }
        else:
            return {"mensaje": "No se han procesado datos nuevos."}
    except Exception as e:
        return {"error": str(e)}

# Main
if __name__ == "__main__":
    ruta_entrada = input("Ingresa la ruta al archivo Excel de entrada: ")
    resultado = procesar_archivo_completo(ruta_entrada)
    print(resultado)
