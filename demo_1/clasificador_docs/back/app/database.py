# database.py

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self, db_path="documents.db"):
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.info("Base de datos inicializada correctamente.")
        except sqlite3.Error as e:
            logging.error(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()
    
    def insert_document(self, title, text, category):
        """Insertar un documento en la base de datos."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO documents (title, text, category) VALUES (?, ?, ?)",
                (title, text, category)
            )
            conn.commit()
            logging.info(f"Documento '{title}' insertado correctamente.")
        except sqlite3.Error as e:
            logging.error(f"Error al insertar documento '{title}': {e}")
        finally:
            conn.close()
    
    def get_documents(self, category=None):
        """Obtener todos los documentos, opcionalmente filtrando por categoría."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if category:
                cursor.execute(
                    "SELECT id, title, text, category, created_at FROM documents WHERE category = ?",
                    (category,)
                )
            else:
                cursor.execute(
                    "SELECT id, title, text, category, created_at FROM documents"
                )
            rows = cursor.fetchall()
            return [
                {"id": r[0], "title": r[1], "text": r[2], "category": r[3], "created_at": r[4]}
                for r in rows
            ]
        except sqlite3.Error as e:
            logging.error(f"Error al obtener documentos: {e}")
            return []
        finally:
            conn.close()

