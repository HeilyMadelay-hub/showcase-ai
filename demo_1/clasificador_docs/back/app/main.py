from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import Database
from .demo_dataset import DemoDataset
from .ingestion import DocumentIngestion
from pathlib import Path 
from dataclasses import dataclass
import logging
import time  
import fitz
import docx2txt
import uvicorn
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
FastAPI: Framework para crear APIs REST.

UploadFile, File: Facilitan la subida de archivos en endpoints POST.

HTTPException: Permite devolver errores HTTP con código y mensaje.

CORSMiddleware: Middleware para CORS, que permite que tu frontend en otro dominio pueda llamar a la API.

JSONResponse: Para devolver respuestas JSON personalizadas (aunque aquí no se usa explícitamente).

uvicorn: Servidor ASGI que corre FastAPI.

os: Para manejar carpetas y archivos en el sistema operativo (crear carpeta uploads, etc.).

"""
app = FastAPI(
    title="Clasificador de Documentos API",
    description="API para clasificación automática de documentos",
    version="1.0.0"
)

"""
Crea la aplicación FastAPI.

Los parámetros (title, description, version) sirven para documentación automática en /docs y /redoc.
"""

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
Esto permite que cualquier frontend pueda hacer llamadas a la API (con *).

allow_methods=["*"] permite GET, POST, PUT, DELETE, etc.

allow_headers=["*"] permite cualquier cabecera HTTP.

Sin esto, si tu frontend está en otro dominio, los navegadores bloquearían las peticiones.
"""

# Instancias
db = Database()
demo = DemoDataset()
document_processor = DocumentIngestion()


@app.get("/")
async def root():
    return {"message": "Backend Clasificador de Documentos funcionando con FastAPI"}

"""
Endpoint / para probar que la API está funcionando.

Devuelve un mensaje simple.
"""
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "clasificador-docs-backend"}
"""
Endpoint /health para monitoreo.

Muy útil en producción para verificar que el backend responde correctamente.
"""
@app.post("/upload_document/")
async def upload_document(file: UploadFile = File(...)) -> JSONResponse:
    """
    Recibir archivo (UploadFile)
    Guardarlo en /uploads/  
    Extraer texto con extract_text_from_file()
    Devolver texto y mensajes de error si aplica
    """
    try:
        #  Validar que se subió un archivo
        if not file.filename:
            raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")
        
        #  Validar extensión del archivo ANTES de guardar
        supported_extensions = {'.pdf', '.docx', '.txt'}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no soportado: {file_extension}. Tipos soportados: {', '.join(supported_extensions)}"
            )
        
        # Crear directorio uploads si no existe
        os.makedirs("uploads", exist_ok=True)
        
        #  Generar nombre único para evitar conflictos
        import time
        timestamp = int(time.time())
        safe_filename = f"{timestamp}_{file.filename.replace(' ', '_')}"
        file_path = f"uploads/{safe_filename}"
    
        #  Guardar archivo subido
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Archivo guardado: {file_path}")
        
        # Extraer texto del archivo con extract_text_from_file()
        extraction_result = document_processor.extract_text_from_file(file_path)
        
        #  Preparar respuesta completa
        response_data = {
            "filename": file.filename,
            "success": extraction_result.success,
            "file_type": extraction_result.file_type,
            "file_size": extraction_result.file_size,
            "text_length": len(extraction_result.text) if extraction_result.text else 0,
            "saved_as": safe_filename
        }
        
        # Devolver texto Y mensajes de error si aplica
        if extraction_result.success:
            response_data["text"] = extraction_result.text
            response_data["message"] = "Archivo subido y texto extraído exitosamente"
            status_code = 200
        else:
            response_data["error"] = extraction_result.error_message
            response_data["message"] = "Archivo subido pero error extrayendo texto"
            status_code = 400
        
        return JSONResponse(
            status_code=status_code,
            content=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando archivo subido: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/classify")
async def classify_document():
    """Endpoint para clasificar documentos"""
    # TODO: Implementar lógica de clasificación con IA
    return {"message": "Funcionalidad de clasificación en desarrollo"}

@app.get("/documents")
async def get_documents():
    """Endpoint para obtener lista de documentos"""
    try:
        documents = db.get_documents()
        return {
            "documents": documents, 
            "count": len(documents),
            "message": "Lista de documentos obtenida exitosamente"
        }
    except Exception as e:
        logger.error(f"Error obteniendo documentos: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo documentos: {str(e)}")

@app.post("/load_demo/")
def load_demo():
    """Carga los 10 documentos de prueba en la base de datos"""
    try:
        # Inicializar base de datos (crea tabla si no existe)
        db.init_db()
        logger.info("Base de datos inicializada correctamente.")
        
        # Verificar si ya hay documentos en la base de datos
        existing_docs = db.get_documents()
        if len(existing_docs) >= 10:
            return {"message": f"Ya hay {len(existing_docs)} documentos en la base de datos. No es necesario cargar más."}
        
        # Cargar datos de demo en la instancia de DemoDataset
        demo.load_demo_data()
        logger.info("Datos de demo cargados en memoria.")
        
        # Insertar documentos de demo en la base de datos
        count = 0
        demo_documents = demo.get_documents()
        
        for doc in demo_documents:
            # Salir del bucle si ya insertamos 10 documentos
            if count >= 10:
                break
            db.insert_document(doc["title"], doc["text"], doc["category"])
            count += 1
            logger.info(f"Documento '{doc['title']}' insertado.")

        return {
            "message": f"{count} documentos cargados correctamente.",
            "total_documents": len(existing_docs) + count
        }
    
    except Exception as e:
        logger.error(f"Error cargando documentos de demo: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
