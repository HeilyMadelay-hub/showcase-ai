import sqlite3
import logging
from datetime import datetime
from typing import Optional

class Database:
    def __init__(self, db_path: str = "documents.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializar base de datos y tabla si no existe."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    text TEXT,
                    category TEXT,
                    confidence REAL,
                    compliance TEXT,
                    hash_integrity TEXT,
                    explanation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.info("Base de datos inicializada correctamente.")
        except sqlite3.Error as e:
            logging.error(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()
    
    def insert_document(
        self,
        title: str,
        text: str,
        category: str,
        confidence: float,
        compliance: str,
        hash_integrity: Optional[str] = None,
        explanation: Optional[str] = None
    ) -> Optional[int]:
        """Insertar un documento completo en la base de datos."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO documents 
                (title, text, category, confidence, compliance, hash_integrity, explanation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (title, text, category, confidence, compliance, hash_integrity, explanation)
            )
            conn.commit()
            doc_id = cursor.lastrowid
            logging.info(f"Documento '{title}' insertado correctamente con ID {doc_id}.")
            return doc_id
        except sqlite3.Error as e:
            logging.error(f"Error al insertar documento '{title}': {e}")
            return None
        finally:
            conn.close()
    
    def get_documents(self, category: Optional[str] = None):
        """Obtener todos los documentos, opcionalmente filtrando por categoría."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if category:
                cursor.execute(
                    '''
                    SELECT id, title, text, category, confidence, compliance, hash_integrity, explanation, created_at
                    FROM documents
                    WHERE category = ?
                    ''',
                    (category,)
                )
            else:
                cursor.execute(
                    '''
                    SELECT id, title, text, category, confidence, compliance, hash_integrity, explanation, created_at
                    FROM documents
                    '''
                )
            rows = cursor.fetchall()
            return [
                {
                    "id": r[0],
                    "title": r[1],
                    "text": r[2],
                    "category": r[3],
                    "confidence": r[4],
                    "compliance": r[5],
                    "hash_integrity": r[6],
                    "explanation": r[7],
                    "created_at": r[8]
                }
                for r in rows
            ]
        except sqlite3.Error as e:
            logging.error(f"Error al obtener documentos: {e}")
            return []
        finally:
            conn.close()

    def fetch_documents(self, category: Optional[str] = None, query: Optional[str] = None, page: int = 1, page_size: int = 10):
        """
        Obtener documentos con filtrado, búsqueda por texto y paginación.
        
        Args:
            category: Filtrar por categoría específica
            query: Buscar en el texto del documento
            page: Número de página (inicia en 1)
            page_size: Número de documentos por página
        
        Returns:
            tuple: (documentos, total_count)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calcular offset para paginación,offset es el número de registros que la base de datos debe "saltar" o "omitir" antes de comenzar a devolver resultados. 
            # Se usa junto con LIMIT para implementar paginación.
            # La paginación es cuando tienes muchos resultados y los divides en páginas más pequeñas para que sea más fácil navegar y cargar.
            offset = (page - 1) * page_size
            
            # Construir consulta base
            base_sql = "SELECT id, title, category, compliance, hash_integrity FROM documents"
            count_base_sql = "SELECT COUNT(*) FROM documents"
            
            conditions = []
            params = []
            
            # Agregar condiciones según los filtros
            if category:
                conditions.append("category = ?")
                params.append(category)
                
            if query:
                conditions.append("text LIKE ?")
                params.append(f"%{query}%")
            
            # Construir cláusula WHERE si hay condiciones
            where_clause = ""
            if conditions:
                where_clause = " WHERE " + " AND ".join(conditions)
            
            # Ejecutar consulta de conteo total
            count_sql = count_base_sql + where_clause
            cursor.execute(count_sql, params)
            total = cursor.fetchone()[0]
            
            # Ejecutar consulta principal con paginación
            main_sql = base_sql + where_clause + " ORDER BY id DESC LIMIT ? OFFSET ?"
            main_params = params + [page_size, offset]
            cursor.execute(main_sql, main_params)
            
            # Obtener nombres de columnas
            column_names = [description[0] for description in cursor.description]
            
            # Convertir filas a diccionarios
            rows = cursor.fetchall()
            docs = [dict(zip(column_names, row)) for row in rows]
            
            logging.info(f"Obtenidos {len(docs)} documentos de un total de {total}")
            return docs, total
            
        except sqlite3.Error as e:
            logging.error(f"Error al obtener documentos con filtros: {e}")
            return [], 0
        finally:
            conn.close()
