import sqlite3
import logging
import json
from datetime import datetime
from typing import Optional, List

class Database:
    def __init__(self, db_path: str = "documents.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializar base de datos y tabla si no existe, incluyendo nuevos campos."""
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
                    hits TEXT,
                    misses TEXT,
                    cited_articles TEXT,
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
        explanation: Optional[str] = None,
        hits: Optional[List[str]] = None,
        misses: Optional[List[str]] = None,
        cited_articles: Optional[List[str]] = None
    ) -> Optional[int]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO documents 
                (title, text, category, confidence, compliance, hash_integrity, explanation, hits, misses, cited_articles)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    title,
                    text,
                    category,
                    confidence,
                    compliance,
                    hash_integrity,
                    explanation,
                    json.dumps(hits or []),
                    json.dumps(misses or []),
                    json.dumps(cited_articles or [])
                )
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
        """Obtener todos los documentos, opcionalmente filtrando por categoría. Deserializa los campos JSON."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if category:
                cursor.execute(
                    '''
                    SELECT id, title, text, category, confidence, compliance, hash_integrity, explanation, hits, misses, cited_articles, created_at
                    FROM documents
                    WHERE category = ?
                    ''',
                    (category,)
                )
            else:
                cursor.execute(
                    '''
                    SELECT id, title, text, category, confidence, compliance, hash_integrity, explanation, hits, misses, cited_articles, created_at
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
                    "hits": json.loads(r[8]) if r[8] else [],
                    "misses": json.loads(r[9]) if r[9] else [],
                    "cited_articles": json.loads(r[10]) if r[10] else [],
                    "created_at": r[11]
                }
                for r in rows
            ]
        except sqlite3.Error as e:
            logging.error(f"Error al obtener documentos: {e}")
            return []
        finally:
            conn.close()

    def fetch_documents(self, category: Optional[str] = None, query: Optional[str] = None, page: int = 1, page_size: int = 10):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            offset = (page - 1) * page_size

            base_sql = "SELECT id, title, category, confidence, compliance, hash_integrity, explanation, hits, misses, cited_articles, created_at FROM documents"
            count_base_sql = "SELECT COUNT(*) FROM documents"
            
            conditions = []
            params = []
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            if query:
                conditions.append("text LIKE ?")
                params.append(f"%{query}%")
            
            where_clause = ""
            if conditions:
                where_clause = " WHERE " + " AND ".join(conditions)
            
            count_sql = count_base_sql + where_clause
            cursor.execute(count_sql, params)
            total = cursor.fetchone()[0]
            
            main_sql = base_sql + where_clause + " ORDER BY id DESC LIMIT ? OFFSET ?"
            main_params = params + [page_size, offset]
            cursor.execute(main_sql, main_params)
            column_names = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            docs = []
            for row in rows:
                doc = dict(zip(column_names, row))
                # Deserializar los campos JSON
                doc["hits"] = json.loads(doc["hits"]) if doc.get("hits") else []
                doc["misses"] = json.loads(doc["misses"]) if doc.get("misses") else []
                doc["cited_articles"] = json.loads(doc["cited_articles"]) if doc.get("cited_articles") else []
                docs.append(doc)
            
            logging.info(f"Obtenidos {len(docs)} documentos de un total de {total}")
            return docs, total
            
        except sqlite3.Error as e:
            logging.error(f"Error al obtener documentos con filtros: {e}")
            return [], 0
        finally:
            conn.close()