"""
Columna	Propósito
doc_id	Vincula el evento al documento correspondiente
action	Tipo de acción realizada (ej. upload_and_classify)
payload	Detalle de la acción en formato JSON sin tener que modificar la estructura de la tabla cada vez que quieras registrar un nuevo dato.
content_hash	Hash del contenido para verificar integridad
timestamp	Momento en que ocurrió el evento

"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("documents.db") 

class AuditTrail:
    @staticmethod
    def append_event(doc_id: int, action: str, payload: dict, content_hash: str):
        """
        Inserta un evento de auditoría en la tabla audit_trail.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                action TEXT,
                payload TEXT,
                content_hash TEXT,
                timestamp TEXT
            )
        """)

        timestamp = datetime.now(datetime.UTC).isoformat()

        cursor.execute("""
            INSERT INTO audit_trail (doc_id, action, payload, content_hash, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (doc_id, action, json.dumps(payload), content_hash, timestamp))

        conn.commit()
        conn.close()

