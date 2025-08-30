from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import Database
from app.demo_dataset import DemoDataset
from app.explanation.explanation import explain_with_context
from app.ingestion import DocumentIngestion
from app.explanation.explanation import explain_with_context, ExplanationResult
from app.compliance.compliance_engine import ComplianceEngine
from app.classification import classify_text
from app.security.encryption import Hasher
from app.audit.audit_trail import AuditTrail
from app.classification import classify_text
from datetime import datetime
from pathlib import Path 
from dataclasses import dataclass
from pydantic import BaseModel
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
compliance_engine = ComplianceEngine()
logging.info("Instancias de Database, DemoDataset, DocumentIngestion y ComplianceEngine creadas.")

@app.post("/upload_document/")
async def upload_document(file: UploadFile = File(...)) -> JSONResponse:
    """
    Recibir archivo (UploadFile)
    Guardarlo en /uploads/  
    Extraer texto, clasificar, explicar, compliance
    Construir hash, guardar en DB y registrar audit trail
    Retornar JSON completo con hits/misses y hash de integridad
    """
    try:
        # 1️ Validar archivo
        if not file.filename:
            raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")

        supported_extensions = {'.pdf', '.docx', '.txt'}
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no soportado: {file_extension}. Tipos soportados: {', '.join(supported_extensions)}"
            )

        # 2️ Guardar archivo
        os.makedirs("uploads", exist_ok=True)
        timestamp = int(time.time())
        safe_filename = f"{timestamp}_{file.filename.replace(' ', '_')}"
        file_path = f"uploads/{safe_filename}"

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        logger.info(f"Archivo guardado: {file_path}")

        # 3️ Extraer texto
        try:
            extraction_result = document_processor.extract_text_from_file(file_path)
            if extraction_result.success:
                text = extraction_result.text
            else:
                raise Exception(extraction_result.error_message)
        except Exception as e:
            logger.exception("Error extrayendo texto")
            raise HTTPException(status_code=500, detail=f"Error extrayendo texto: {str(e)}")

        # 4️ Clasificación
        try:
            classification = classify_text(text)
            category = classification.get("category", "unknown")
            confidence = classification.get("confidence", 0.0)
        except Exception:
            logger.warning("Clasificación fallida, se asigna category='unknown'")
            category = "unknown"
            confidence = 0.0

        # 5️ Explicación / Compliance
        try:
            expl: ExplanationResult = compliance_engine.validate(text, category)
        except Exception:
            logger.warning("Explicación/Compliance fallido, se asigna status='⚠️'")
            expl = ExplanationResult(summary="Error", cited_articles=[], compliance_status="⚠️", hits=[], misses=[])

        # 6️ Construir hash SHA256
        text_hash = Hasher.sha256(text)

        doc_id = db.insert_document(
            title=file.filename,
            text=text,
            category=category if category else "sin clasificar",
            confidence=float(confidence) if confidence is not None else 0.0,
            compliance=expl.compliance_status if hasattr(expl, "compliance_status") else "❌",
            hash_integrity=text_hash if text_hash else None,
            explanation=expl.summary if hasattr(expl, "summary") else None
        )

        if doc_id:
            logging.info(f"Documento guardado correctamente con ID {doc_id}.")
        else:
            logging.error("Error al guardar el documento en la base de datos.")

        # 8️ Registrar audit trail
        try:
            AuditTrail.append_event(
                doc_id=doc_id,
                action="upload_and_classify",
                payload={"category": category, "confidence": confidence, "compliance": expl.compliance_status},
                content_hash=text_hash
            )
        except Exception:
            logger.warning("Audit trail fallido, se continúa flujo")

        # 9️ Retornar JSON completo
        return JSONResponse(status_code=200, content={
            "success": True,
            "document_id": doc_id if doc_id else None,
            "filename": file.filename if file and hasattr(file, "filename") else None,
            "category": category if category else "sin clasificar",
            "confidence": float(confidence) if confidence is not None else 0.0,
            "compliance_status": expl.compliance_status if hasattr(expl, "compliance_status") else "❌",
            "explanation": expl.summary if hasattr(expl, "summary") else "",
            "cited_articles": expl.cited_articles[:10] if hasattr(expl, "cited_articles") else [],
            "hits": expl.hits if hasattr(expl, "hits") else [],
            "misses": expl.misses if hasattr(expl, "misses") else [],
            "hash_integrity": text_hash if text_hash else None,
            "created_at": datetime.now().isoformat()  # opcional, si quieres devolver la fecha actual
        })


    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando archivo subido: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

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
    """Carga los documentos de prueba en la base de datos, evitando duplicados"""
    try:
        # Inicializar base de datos (crea tabla si no existe)
        db.init_db()
        logger.info("Base de datos inicializada correctamente.")
        
        # Obtener documentos ya existentes en la DB
        existing_docs = db.get_documents()
        existing_hashes = {doc["hash_integrity"] for doc in existing_docs if doc["hash_integrity"]}

        # Cargar datos de demo en memoria
        demo.load_demo_data()
        logger.info("Datos de demo cargados en memoria.")
        
        # Insertar documentos de demo evitando duplicados
        count = 0
        demo_documents = demo.get_documents()
        
        for doc in demo_documents:
            demo_hash = Hasher.sha256(doc["text"])

            # Verificar si ya existe en DB
            if demo_hash in existing_hashes:
                logger.warning(f"Documento '{doc['title']}' ya existe en la base de datos. Saltando...")
                continue  # No insertamos duplicado

            doc_id = db.insert_document(
                title=doc.get("title", "sin título"), 
                text=doc.get("text", ""), 
                category=doc.get("category", "sin clasificar"),
                confidence=0.85,  # Confianza por defecto para demos
                compliance="✅",  # Status de compliance por defecto
                hash_integrity=demo_hash,
                explanation="Documento de demostración cargado automáticamente"
            )

            if doc_id:
                count += 1
                logger.info(f"Documento '{doc['title']}' insertado correctamente con ID {doc_id}.")
            else:
                logger.error(f"No se pudo insertar el documento '{doc['title']}'.")

        return {
            "success": True,
            "message": f"{count} documentos cargados correctamente (sin duplicados).",
            "total_documents": len(existing_docs) + count
        }
    
    except Exception as e:
        logger.error(f"Error cargando documentos de demo: {e}")
        return {"success": False, "error": str(e)}


# ---------- Explain JSON ----------
class ExplainRequest(BaseModel):
    text: str
    category: str

@app.post("/demo_explain_json/")
async def demo_explain_json(req: ExplainRequest):
    """
    Recibe texto y categoría, aplica ComplianceEngine y devuelve JSON
    con hits, misses y status de cumplimiento.
    """
    # Llamamos al wrapper
    result = compliance_engine.validate(req.text, req.category)

    return {
        "success": True,
        "category": req.category if req.category else "sin clasificar",
        "compliance_status": getattr(result, "compliance_status", "❌"),
        "summary": getattr(result, "summary", ""),
        "hits": getattr(result, "hits", []),
        "misses": getattr(result, "misses", []),
        "cited_articles": getattr(result, "cited_articles", []),
        "confidence": getattr(result, "confidence", 0.0)
    }

# ---------- Endpoints de búsqueda y listado ----------

@app.get("/list_documents/")
async def list_documents(
    category: str = Query(None, description="Filtrar por categoría"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Documentos por página")
):
    """
    Lista todos los documentos o filtra por categoría con paginación.
    
    Query params:
    - category: Filtrar por categoría específica (opcional)
    - page: Número de página (default=1)
    - page_size: Cantidad de documentos por página (default=10, máximo=100)
    """
    try:
        docs, total = db.fetch_documents(category=category, page=page, page_size=page_size)
        
        logger.info(f"List documents query: category={category}, page={page}, found={len(docs)} of {total}")
        
        return {
            "success": True,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,  # Calcular páginas totales
            "has_next": page * page_size < total,
            "has_previous": page > 1,
            "documents": docs,
            "message": f"Obtenidos {len(docs)} documentos de {total} totales"
        }
        
    except Exception as e:
        logger.error(f"Error listando documentos: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno del servidor al listar documentos"
        )

@app.get("/search_documents/")
async def search_documents(
    query: str = Query(..., min_length=1, description="Término de búsqueda"),
    category: str = Query(None, description="Filtrar por categoría"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Documentos por página")
):
    """
    Buscar documentos que contengan un término dentro del texto.
    
    Query params:
    - query: Palabra o frase a buscar (requerido)
    - category: Filtrar por categoría específica (opcional)
    - page: Número de página (default=1)
    - page_size: Cantidad de documentos por página (default=10, máximo=100)
    """
    try:
        # Sanitizar query básico (remover caracteres potencialmente peligrosos)
        sanitized_query = query.strip()
        
        if not sanitized_query:
            raise HTTPException(
                status_code=400, 
                detail="El término de búsqueda no puede estar vacío"
            )
        
        results, total = db.fetch_documents(
            query=sanitized_query, 
            category=category, 
            page=page, 
            page_size=page_size
        )
        
        logger.info(f"Search query: '{sanitized_query}', category={category}, page={page}, found={len(results)} of {total}")
        
        return {
            "success": True,
            "query": sanitized_query,
            "category": category,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_previous": page > 1,
            "documents": results,
            "message": f"Encontrados {len(results)} documentos de {total} totales para '{sanitized_query}'"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error buscando documentos: query='{query}', error={e}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno del servidor al buscar documentos"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)