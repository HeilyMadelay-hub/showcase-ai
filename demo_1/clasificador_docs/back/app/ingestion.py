# Módulo de ingestión de documentos
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import docx2txt
import os
import shutil
from pathlib import Path
import mimetypes
from typing import Optional, Dict, Any
import logging
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExtractionResult:
    """Resultado de la extracción de texto"""
    success: bool
    text: str = ""
    error_message: str = ""
    file_type: str = ""
    file_size: int = 0

class DocumentIngestion:
    """Clase para procesamiento e ingesta de documentos"""

    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        
        # Configuración de tipos de archivo soportados
        self.supported_extensions = {'.pdf', '.docx', '.txt'}
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        
    def extract_text_from_pdf(self, path: str) -> ExtractionResult:
        """
        Extrae texto de un archivo PDF usando PyMuPDF (fitz)
        
        Args:
            path: Ruta al archivo PDF
            
        Returns:
            ExtractionResult con el texto extraído o error
        """
        try:
            if not os.path.exists(path):
                return ExtractionResult(
                    success=False,
                    error_message=f"Archivo no encontrado: {path}",
                    file_type="pdf"
                )
            
            text = ""
            file_size = os.path.getsize(path)

            # doc objeto Document de PyMuPDF.
            # len(doc) te devuelve el número total de páginas.

            with fitz.open(path) as doc:
                for page_num in range(len(doc)):
                    page = doc[page_num]    # Obtiene la página actual
                    text += page.get_text() # Extrae el texto de esa página y lo concatena text es una cadena donde vas concatenando todo el texto del PDF.
                    
            # Limpiar texto extraído de espacios en blanco innecesarios
            text = text.strip()
            
            logger.info(f"Texto extraído exitosamente de PDF: {len(text)} caracteres")
            
            return ExtractionResult(
                success=True,
                text=text,
                file_type="pdf",
                file_size=file_size
            )
            
        except Exception as e:
            logger.error(f"Error extrayendo texto de PDF {path}: {str(e)}")
            return ExtractionResult(
                success=False,
                error_message=f"Error procesando PDF: {str(e)}",
                file_type="pdf"
            )
    
    def extract_text_from_docx(self, path: str) -> ExtractionResult:
        """
        Extrae texto de un archivo DOCX usando docx2txt
        
        Args:
            path: Ruta al archivo DOCX
            
        Returns:
            ExtractionResult con el texto extraído o error
        """
        try:
            if not os.path.exists(path):
                return ExtractionResult(
                    success=False,
                    error_message=f"Archivo no encontrado: {path}",
                    file_type="docx"
                )
            
            file_size = os.path.getsize(path)
            text = docx2txt.process(path)
            
            # Limpiar texto extraído
            text = text.strip() if text else ""
            
            logger.info(f"Texto extraído exitosamente de DOCX: {len(text)} caracteres")
            
            return ExtractionResult(
                success=True,
                text=text,
                file_type="docx",
                file_size=file_size
            )
            
        except Exception as e:
            logger.error(f"Error extrayendo texto de DOCX {path}: {str(e)}")
            return ExtractionResult(
                success=False,
                error_message=f"Error procesando DOCX: {str(e)}",
                file_type="docx"
            )
    
    def extract_text_from_txt(self, path: str) -> ExtractionResult:
        """
        Extrae texto de un archivo de texto plano
        
        Args:
            path: Ruta al archivo TXT
            
        Returns:
            ExtractionResult con el texto extraído o error
        """
        try:
            if not os.path.exists(path):
                return ExtractionResult(
                    success=False,
                    error_message=f"Archivo no encontrado: {path}",
                    file_type="txt"
                )
            
            file_size = os.path.getsize(path)
            
            # Intentar diferentes codificaciones
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            text = ""
            
            for encoding in encodings:
                try:
                    with open(path, 'r', encoding=encoding) as file:
                        text = file.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if not text:
                return ExtractionResult(
                    success=False,
                    error_message="No se pudo decodificar el archivo de texto",
                    file_type="txt"
                )
            
            # Limpiar texto extraído
            text = text.strip()
            
            logger.info(f"Texto extraído exitosamente de TXT: {len(text)} caracteres")
            
            return ExtractionResult(
                success=True,
                text=text,
                file_type="txt",
                file_size=file_size
            )
            
        except Exception as e:
            logger.error(f"Error extrayendo texto de TXT {path}: {str(e)}")
            return ExtractionResult(
                success=False,
                error_message=f"Error procesando archivo de texto: {str(e)}",
                file_type="txt"
            )
    
    def extract_text_from_file(self, path: str) -> ExtractionResult:
        """
        Detecta el tipo de archivo y usa la función de extracción adecuada
        
        Args:
            path: Ruta al archivo
            
        Returns:
            ExtractionResult con el texto extraído o error
        """
        try:
            # Validar que el archivo existe
            if not os.path.exists(path):
                return ExtractionResult(
                    success=False,
                    error_message=f"Archivo no encontrado: {path}"
                )
            
            # Validar tamaño del archivo
            file_size = os.path.getsize(path)
            if file_size > self.max_file_size:
                return ExtractionResult(
                    success=False,
                    error_message=f"Archivo demasiado grande. Tamaño máximo permitido: {self.max_file_size / (1024*1024):.1f}MB"
                )
            
            # Detectar extensión del archivo
            file_path = Path(path)
            extension = file_path.suffix.lower()
            
            # Validar extensión soportada
            if extension not in self.supported_extensions:
                return ExtractionResult(
                    success=False,
                    error_message=f"Tipo de archivo no soportado: {extension}. Tipos soportados: {', '.join(self.supported_extensions)}"
                )
            
            # Usar la función de extracción apropiada
            if extension == '.pdf':
                return self.extract_text_from_pdf(path)
            elif extension == '.docx':
                return self.extract_text_from_docx(path)
            elif extension == '.txt':
                return self.extract_text_from_txt(path)
            else:
                return ExtractionResult(
                    success=False,
                    error_message=f"Extensión no reconocida: {extension}"
                )
                
        except Exception as e:
            logger.error(f"Error procesando archivo {path}: {str(e)}")
            return ExtractionResult(
                success=False,
                error_message=f"Error general procesando archivo: {str(e)}"
            )
    
    def ingest_document(self, file_path: str) -> ExtractionResult:
        """
        Procesa e ingiere un documento completo
        
        Args:
            file_path: Ruta al archivo a procesar
            
        Returns:
            ExtractionResult con el resultado del procesamiento
        """
        try:
            # Extraer texto del documento
            result = self.extract_text_from_file(file_path)
            
            if result.success:
                logger.info(f"Documento ingestado exitosamente: {file_path}")
                # Aquí podrías agregar lógica adicional como:
                # - Guardar en base de datos
                # - Generar embeddings
                # - Indexar para búsqueda
                # - Etc.
            
            return result
            
        except Exception as e:
            logger.error(f"Error ingiriendo documento {file_path}: {str(e)}")
            return ExtractionResult(
                success=False,
                error_message=f"Error en ingesta de documento: {str(e)}"
            )