# Backend - Clasificador de Documentos

API REST desarrollada con FastAPI para la clasificación automática de documentos legales y administrativos con análisis de compliance y auditoría integrada.

## 🚀 Características Principales

- **Clasificación automática** de documentos usando análisis de palabras clave
- **Procesamiento de múltiples formatos**: PDF, DOCX y TXT
- **Análisis de compliance** normativo con detección de hits/misses
- **Sistema de auditoría** con hashing SHA256 para integridad
- **Base de datos SQLite** para persistencia
- **API REST completa** con endpoints de consulta y búsqueda
- **Datos de demostración** precargados

## 📁 Estructura del Proyecto

```
back/
├── app/                          # Código principal de la aplicación
│   ├── audit/                    # Sistema de auditoría y trazabilidad
│   ├── compliance/               # Motor de validación de compliance
│   │   └── compliance_engine.py  # Validación de documentos según categoría
│   ├── explanation/              # Sistema de explicaciones y análisis
│   │   └── explanation.py        # Análisis de hits/misses por patrones
│   ├── security/                 # Utilidades de seguridad
│   │   └── encryption.py         # Hashing SHA256 para integridad
│   ├── classification.py         # Clasificador basado en keywords
│   ├── database.py               # Gestión de base de datos SQLite
│   ├── demo_dataset.py           # Datos de demostración
│   ├── ingestion.py              # Procesamiento y extracción de texto
│   └── main.py                   # Aplicación FastAPI principal
├── uploads/                      # Carpeta para archivos subidos
├── documents.db                  # Base de datos SQLite
├── requirements.txt              # Dependencias de Python
└── .venv/                        # Entorno virtual de Python
```

## 🔧 Componentes del Sistema

### **main.py** - API Principal
FastAPI con 4 endpoints principales:
- `POST /upload_document/` - Subida y procesamiento completo de documentos
- `GET /documents` - Lista todos los documentos almacenados
- `POST /load_demo/` - Carga datos de demostración (evita duplicados)
- `GET /list_documents/` - Lista con paginación y filtros por categoría
- `GET /search_documents/` - Búsqueda de texto con paginación

### **classification.py** - Clasificador de Documentos
Sistema de clasificación basado en palabras clave que reconoce:

| Categoría | Ejemplos de Keywords |
|-----------|---------------------|
| **contrato** | contrato, partes, cláusula, firmas, objeto del contrato |
| **contrato_traspaso** | traspaso, negocio en funcionamiento, fondo de comercio |
| **contrato_arrendamiento** | arrendamiento, arrendador, arrendatario, renta mensual |
| **contrato_compraventa** | compraventa, vendedor, comprador, precio de venta |
| **escritura_publica** | escritura pública, notario, protocolo, fe pública |
| **factura** | factura, RFC emisor, IVA, CFDI, UUID |
| **acta** | acta, asistentes, orden del día, acuerdos |
| **poder_notarial** | poder notarial, apoderado, facultades, representación |
| **estado_financiero** | activo, pasivo, balance general, flujo de efectivo |
| **sentencia_judicial** | sentencia, tribunal, fallo, demandante |
| **laboral** | contrato laboral, empleado, salario, prestaciones |
| **mercantil** | sociedad, objeto social, capital, accionistas |

### **database.py** - Gestión de Datos
Clase `Database` que maneja:
- **Tabla documents** con campos: id, title, text, category, confidence, compliance, hash_integrity, explanation, hits, misses, cited_articles, created_at
- **Operaciones CRUD** con métodos `insert_document()`, `get_documents()`, `fetch_documents()`
- **Paginación y filtros** por categoría y búsqueda de texto
- **Serialización JSON** para campos de arrays (hits, misses, cited_articles)

### **ingestion.py** - Procesamiento de Archivos
Clase `DocumentIngestion` con capacidades de:
- **Extracción de texto** de PDF (PyMuPDF), DOCX (docx2txt) y TXT
- **Validación de archivos** (tipos soportados, tamaño máximo 50MB)
- **Manejo de errores** robusto con `ExtractionResult`
- **Codificaciones múltiples** para archivos de texto

### **compliance/compliance_engine.py** - Validación Normativa
Motor que valida documentos usando:
- **Sistema de explicaciones** contextual por categoría
- **Estado de compliance**: ✅ (cumple), ⚠️ (parcial), ❌ (no cumple)
- **Retorno estructurado** con `ExplanationResult`

### **explanation/explanation.py** - Análisis Contextual
Sistema avanzado que genera:
- **Detección de patrones** con regex para elementos legales
- **Hits y misses** por keywords de la categoría
- **Cálculo de porcentaje** de cumplimiento (≥60% = ✅, 30-59% = ⚠️, <30% = ❌)
- **Fragmentación inteligente** del texto en oraciones
- **Artículos citados** extraídos automáticamente

### **security/encryption.py** - Seguridad
Utilidad `Hasher` para:
- **Hash SHA256** de contenido de documentos
- **Integridad de datos** para detectar modificaciones
- **Validación de inputs** con manejo de errores

### **demo_dataset.py** - Datos de Prueba
Dataset con 10 documentos de ejemplo que incluye:
- **Variedad de categorías** (contratos, sentencias, facturas, actas)
- **Diferentes estados de compliance** (✅, ⚠️, ❌)
- **Datos completos** con hash, explicaciones y análisis

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip

### Instalación

1. **Clonar/ubicar el proyecto**
```bash
cd C:\Users\heily\Desktop\demos\demo_1\clasificador_docs\back
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### 🔄 **POST** `/upload_document/`
Procesa un archivo completo: extracción → clasificación → compliance → almacenamiento

**Request**: Archivo (PDF/DOCX/TXT)

**Response**:
```json
{
  "success": true,
  "document_id": 123,
  "filename": "contrato.pdf",
  "category": "contrato",
  "confidence": 0.85,
  "compliance_status": "✅",
  "explanation": "Resumen del análisis...",
  "cited_articles": ["art. 1", "art. 2"],
  "hits": ["partes", "objeto del contrato"],
  "misses": ["cláusula penal"],
  "hash_integrity": "a1b2c3d4...",
  "created_at": "2025-09-01T10:30:00"
}
```

### 📄 **GET** `/documents`
Lista todos los documentos almacenados

**Response**:
```json
{
  "documents": [...],
  "count": 25,
  "message": "Lista de documentos obtenida exitosamente"
}
```

### 📋 **GET** `/list_documents/`
Lista con paginación y filtros

**Query Parameters**:
- `category` (opcional): Filtrar por categoría
- `page` (default=1): Número de página
- `page_size` (default=10, max=100): Documentos por página

### 🔍 **GET** `/search_documents/`
Búsqueda de texto en documentos

**Query Parameters**:
- `query` (requerido): Término de búsqueda
- `category` (opcional): Filtrar por categoría
- `page`, `page_size`: Paginación

### 🎯 **POST** `/load_demo/`
Carga 10 documentos de demostración (evita duplicados por hash)

## 💾 Base de Datos

### Tabla `documents`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID autoincremental |
| `title` | TEXT | Título del documento |
| `text` | TEXT | Contenido extraído |
| `category` | TEXT | Categoría clasificada |
| `confidence` | REAL | Confianza de clasificación (0-1) |
| `compliance` | TEXT | Estado: ✅, ⚠️, ❌ |
| `hash_integrity` | TEXT | Hash SHA256 del contenido |
| `explanation` | TEXT | Resumen del análisis |
| `hits` | TEXT | JSON: keywords encontradas |
| `misses` | TEXT | JSON: keywords faltantes |
| `cited_articles` | TEXT | JSON: artículos extraídos |
| `created_at` | TIMESTAMP | Fecha de creación |

## 🔒 Seguridad y Compliance

- **Validación de archivos**: Tipos permitidos, tamaño máximo 50MB
- **Hash de integridad**: SHA256 para detectar modificaciones
- **Sanitización**: Limpieza de queries de búsqueda
- **CORS configurado**: Permite peticiones cross-origin
- **Logging estructurado**: Trazabilidad completa de operaciones

## 📊 Flujo de Procesamiento

```
📁 Archivo → 🔍 Validación → 📄 Extracción de Texto → 
🏷️ Clasificación → ⚖️ Compliance → 🔐 Hash SHA256 → 
💾 Base de Datos → 📋 Audit Trail → ✅ Respuesta JSON
```

## 🎮 Datos de Demostración

El sistema incluye 10 documentos de ejemplo con:
- **Contratos** (arrendamiento, prestación servicios, confidencialidad)
- **Sentencias judiciales** (favorable y desestimatoria)
- **Normativas** (reglamento interno, seguridad)
- **Licencias** (software, uso de imagen)
- **Estados variados** de compliance para testing

## 🧪 Testing

Para probar la API:

1. **Documentación interactiva**: http://localhost:8000/docs
2. **Cargar demos**: `POST /load_demo/`
3. **Subir documento**: `POST /upload_document/` con archivo
4. **Buscar**: `GET /search_documents/?query=contrato`

## 📦 Dependencias Principales

- **FastAPI** 0.116.1+ - Framework web
- **Transformers** 4.55.4+ - Procesamiento de lenguaje natural
- **PyMuPDF** 1.26.4+ - Extracción de texto de PDF
- **docx2txt** 0.9+ - Procesamiento de archivos Word
- **sqlite-utils** 3.38+ - Utilidades de base de datos
- **uvicorn** 0.35.0+ - Servidor ASGI

## 🏃‍♂️ Inicio Rápido

```bash
# Activar entorno
.venv\Scripts\activate

# Ejecutar servidor
python -m uvicorn app.main:app --reload

# Cargar datos de demo
curl -X POST http://localhost:8000/load_demo/

# Listar documentos
curl http://localhost:8000/documents
```

## 📝 Notas de Desarrollo

- **CORS habilitado** para desarrollo frontend
- **Logging configurado** a nivel INFO
- **Manejo de errores** con HTTPException
- **Timestamps automáticos** en base de datos
- **Prevención de duplicados** por hash de contenido
