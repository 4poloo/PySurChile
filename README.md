# Proyecto de Análisis y Gestión de Datos Excel

Este proyecto tiene como objetivo la automatización del análisis de datos extraídos de archivos Excel. Actualmente, el sistema procesa los datos de un archivo Excel, realiza cálculos específicos, y genera un archivo de salida con los resultados. El sistema también guarda la fecha del último registro procesado y permite la configuración de la ruta de entrada y salida para los archivos.

## Funcionalidades actuales

- **Lectura de archivo Excel**: El programa lee un archivo Excel y procesa los datos de las columnas relevantes como "OT", "PRODUCTO", "FECHA RECIBO" y "UNID. DISP.".
- **Agrupación de datos**: Los registros con el mismo "OT" y "PRODUCTO" se agrupan y se suman los valores de "UNID. DISP." para obtener un total.
- **Fecha del último registro**: El programa guarda la fecha y hora del último registro procesado, asegurándose de analizar correctamente los datos según esta fecha.
- **Generación de archivo de salida**: El sistema genera un nuevo archivo Excel con los datos procesados, exportando la información en un formato específico.

## Funcionalidades 

A continuación, se detallan las funcionalidades que se agregarán al proyecto:

### 1. **Creación de una API RESTful**
Se implementará una API RESTful utilizando **FAST API** para exponer las funcionalidades del sistema. Esto permitirá integrar el proceso de análisis y generación de archivos de manera remota a través de peticiones HTTP. Las funcionalidades que se podrán exponer son:

- Subir archivos Excel para su procesamiento.
- Consultar los resultados procesados en tiempo real.
- Obtener la fecha y hora del último registro procesado.
  
### 2. **Desarrollo de una app web**
Se desarrollará una **aplicación web** que permita a los usuarios interactuar con el sistema de manera intuitiva. Algunas de las funcionalidades de la app web incluirán:

- **Subida de archivos Excel**: Interfaz para cargar archivos de entrada.
- **Visualización de resultados**: Los usuarios podrán ver los resultados procesados y descargarlos en formato Excel.
- **Configuración de parámetros**: Los usuarios podrán ajustar configuraciones como las rutas de entrada y salida de los archivos, la fecha del último registro, etc.
  
La app web se construirá utilizando **React** para el frontend y se comunicará con la API RESTful para gestionar los datos y los archivos.

## Requisitos del sistema

- **Python 3.12**: El proyecto está desarrollado en Python, por lo que es necesario tener instalada una versión de Python 3.
- **Dependencias**:
  - `pandas`: Para procesar los datos de Excel.
  - `openpyxl`: Para leer y escribir archivos Excel.
  - `FastAPI` : Para uso de API RESTful.
  - **Node.js y React**: Para el desarrollo de la app web (para el frontend).

## Desarrollador
-- Desarrollado por [Maximiliano Olave].