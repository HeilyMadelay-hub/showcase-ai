📄 Clasificador de Documentos Legales

Sistema profesional para subir, clasificar y auditar documentos legales, combinando NLP (Hugging Face), cumplimiento normativo, audit trail y seguridad con cifrado.
Ideal para demostraciones de proyectos legales o pruebas de concepto para despachos o tribunales.

🛠️ Requisitos

Python 3.10+

pip

Sistema operativo: Windows / Mac / Linux

Dependencias principales:

fastapi
uvicorn[standard]
transformers
torch
PyMuPDF
docx2txt
sqlite-utils

📁 Estructura del proyecto
clasificador_docs/
├── back/
│   ├── app/
│   │   ├── audit/                      # Audit trail con hashes
│   │   │   └── audit_trail.py
│   │   ├── classification.py           # Clasificación NLP
│   │   ├── compliance/                 # Validación de documentos
│   │   │   └── compliance_engine.py
│   │   ├── constants.py                # Constantes y configuración
│   │   ├── database.py                 # Conexión SQLite
│   │   ├── demo_dataset.py             # Dataset demo
│   │   ├── ingestion.py                # Extracción de texto
│   │   ├── integration/                # Exportaciones a sistemas externos
│   │   │   └── export_lexnet.py
│   │   ├── main.py                     # Endpoints FastAPI
│   │   ├── search.py                   # Búsqueda y listado
│   │   ├── security/                   # Cifrado y roles
│   │   │   ├── encryption.py
│   │   │   └── roles.py
│   │   └── __init__.py
│   ├── uploads/                        # Archivos subidos
│   ├── documents.db                    # Base de datos SQLite
│   ├── README.md
│   └── requirements.txt
├── front/
│   └── static/
│       ├── index.html                  # Interfaz web
│       ├── script.js                   # JS de interacción
│       └── style.css                   # Estilos
├── test/                               # Tests unitarios
│   ├── test_audit.py
│   ├── test_classification.py
│   ├── test_compliance.py
│   ├── test_ingestion.py
│   └── test_security.py
└── run_demo.py                         # Script principal de demo

⚡ Instalación

Clonar el repositorio:

git clone https://github.com/tuusuario/clasificador_docs.git
cd clasificador_docs/back


Crear y activar entorno virtual:

python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate


Instalar dependencias:

pip install -r requirements.txt


Ejecutar servidor FastAPI:

python -m uvicorn app.main:app --reload

🚀 Endpoints
1. POST /load_demo/

Carga 10 documentos demo en la base de datos.

Respuesta:

{
  "success": true,
  "documents_loaded": 10
}

2. POST /upload_document/

Sube un documento y devuelve categoría y score.

Parametros: archivo (pdf o txt)

Respuesta:

{
  "success": true,
  "document_id": 1,
  "filename": "contrato.pdf",
  "detected_category": "contrato",
  "confidence": 0.92,
  "all_scores": [
    ["contrato", 0.92],
    ["sentencia", 0.05],
    ["normativa", 0.03]
  ],
  "compliance_status": "✅",
  "hash_integrity": "abc123..."
}

3. GET /list_documents/

Lista todos los documentos o filtra por categoría.

Ejemplo:

/list_documents/?category=contrato

4. GET /search_documents/?query=

Búsqueda por palabra clave en los documentos.

Ejemplo:

/search_documents/?query=firma

🧾 Flujo del sistema
Usuario sube documento
   ↓
ingestion.py → extrae texto
   ↓
classification.py → clasifica con NLP
   ↓
compliance_engine.py → valida requisitos legales
   ↓
encryption.py → cifra y guarda
   ↓
audit_trail.py → registra con hash
   ↓
database.py → guarda en SQLite
   ↓
export_lexnet.py → simula exportación externa
   ↓
Frontend → muestra categoría, hash y estado de cumplimiento

🌐 Frontend

Subida de documentos con indicador de carga.

Tabla de resultados filtrable y ordenable.

Estado de cumplimiento legal y hash de integridad.

Exportación simulada a sistemas externos.

Historial de acciones y mini dashboard con ROI y seguridad.

🔒 Seguridad

Archivos cifrados AES-256.

Roles: auditor senior, auditor junior, usuario.

Solo usuarios con permisos pueden ver texto completo.

💡 Extras diferenciales

Historial de acciones con hash encadenado (mini blockchain).

Validación de cumplimiento normativo (contratos, sentencias, etc.).

Exportación simulada a LexNet o gestor documental externo.

Dashboard de control "mini control room".

✅ Tests

extract_text_from_file()

classify_text()

Validación de carga y búsqueda.

📄 Demo rápida
# Cargar dataset demo
curl -X POST http://localhost:8000/load_demo/

# Subir documento
curl -X POST "http://localhost:8000/upload_document/" \
     -F "file=@documento.pdf"

# Listar documentos
curl http://localhost:8000/list_documents/

# Buscar por término
curl http://localhost:8000/search_documents/?query=contrato
