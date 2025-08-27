from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import Database
from .demo_dataset import DemoDataset
import logging
import uvicorn
import os

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
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint para subir documentos
    
    Endpoint POST /upload.

    Recibe un archivo (UploadFile) enviado desde un formulario o fetch.
    """
    try:
        # Crear directorio uploads si no existe
        os.makedirs("uploads", exist_ok=True)
        
        # Guardar archivo
        file_path = f"uploads/{file.filename}" # Ruta donde se guardará el archivo
        with open(file_path, "wb") as buffer:  
            # Abre (o crea) el archivo en la ruta 'file_path'  
            # "wb" significa **write binary**, es decir, escribir en modo binario.  
            # 'buffer' es el objeto archivo que usaremos para escribir los datos.

            content = await file.read()  
            # Lee todo el contenido del archivo subido de manera **asíncrona**. 
            # No bloqueando asi el programa mientras espera que termine await indica que indica que FastAPI puede hacer otras cosas
            # mientras se lee el archivo, sin quedarse “congelado” esperando.Esto es útil cuando varios usuarios suben archivos al mismo tiempo; 
            # el servidor puede atender otras peticiones mientras uno se procesa.
            # 'file' es un UploadFile de FastAPI y 'await' se usa porque es async.

            # Si es content = file.read() El servidor se detendría hasta que termine de leer el archivo.Si el archivo es grande o hay muchas solicitudes, la app se volvería lenta o bloqueada.

            buffer.write(content)  
            # Escribe el contenido leído dentro del archivo en disco.  
            # Guarda físicamente el archivo en la carpeta 'uploads'.

        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "message": "Archivo subido exitosamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo archivo: {str(e)}")

@app.post("/classify")
async def classify_document():
    """Endpoint para clasificar documentos"""
    # TODO: Implementar lógica de clasificación con IA
    return {"message": "Funcionalidad de clasificación en desarrollo"}

@app.get("/documents")
async def get_documents():
    """Endpoint para obtener lista de documentos"""
    # TODO: Implementar obtención de documentos desde base de datos
    return {"documents": [], "message": "Lista de documentos"}

@app.post("/load_demo/")
def load_demo():
    """Carga los 10 documentos de prueba en la base de datos"""
    try:
        # Inicializar base de datos (crea tabla si no existe)
        db.init_db()
        logging.info("Base de datos inicializada correctamente.")
        
        # Insertar documentos de demo
        count = 0
        if count >= 10:
            return {"message": "Ya hay 10 documentos en la base de datos."}
        else:
            for doc in demo.get_documents():
                # Salir del bucle si ya insertamos 10 documentos
                if count >= 10:
                    break
                db.insert_document(doc["title"], doc["text"], doc["category"])
                count += 1
                logging.info(f"Documento '{doc['title']}' insertado.")

        return {"message": f"{count} documentos cargados correctamente."}
    
    except Exception as e:
        logging.error(f"Error cargando documentos de demo: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
