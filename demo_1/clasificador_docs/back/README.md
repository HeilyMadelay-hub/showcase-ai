# Backend - Document Classifier

REST API developed with FastAPI for automatic classification of legal and administrative documents with integrated compliance analysis and auditing.

## 🚀 Main Features

- **Automatic document classification** using keyword analysis
- **Multi-format processing**: PDF, DOCX and TXT
- **Regulatory compliance analysis** with hits/misses detection
- **Audit system** with SHA256 hashing for integrity
- **SQLite database** for persistence
- **Complete REST API** with query and search endpoints
- **Pre-loaded demonstration data**

## 📁 Project Structure

```
back/
├── app/                          # Main application code
│   ├── audit/                    # Audit and traceability system
│   ├── compliance/               # Compliance validation engine
│   │   └── compliance_engine.py  # Document validation by category
│   ├── explanation/              # Explanation and analysis system
│   │   └── explanation.py        # Hits/misses analysis by patterns
│   ├── security/                 # Security utilities
│   │   └── encryption.py         # SHA256 hashing for integrity
│   ├── classification.py         # Keyword-based classifier
│   ├── database.py               # SQLite database management
│   ├── demo_dataset.py           # Demonstration data
│   ├── ingestion.py              # Text processing and extraction
│   └── main.py                   # Main FastAPI application
├── uploads/                      # Folder for uploaded files
├── documents.db                  # SQLite database
├── requirements.txt              # Python dependencies
└── .venv/                        # Python virtual environment
```

## 🔧 System Components

### **main.py** - Main API
FastAPI with 4 main endpoints:
- `POST /upload_document/` - Upload and complete document processing
- `GET /documents` - List all stored documents
- `POST /load_demo/` - Load demonstration data (avoids duplicates)
- `GET /list_documents/` - List with pagination and category filters
- `GET /search_documents/` - Text search with pagination

### **classification.py** - Document Classifier
Keyword-based classification system that recognizes:

| Category | Keyword Examples |
|----------|------------------|
| **contrato** | contract, parties, clause, signatures, contract object |
| **contrato_traspaso** | transfer, functioning business, business assets |
| **contrato_arrendamiento** | lease, lessor, lessee, monthly rent |
| **contrato_compraventa** | sale, seller, buyer, sale price |
| **escritura_publica** | public deed, notary, protocol, public faith |
| **factura** | invoice, issuer RFC, VAT, CFDI, UUID |
| **acta** | minutes, attendees, agenda, agreements |
| **poder_notarial** | notarial power, attorney, powers, representation |
| **estado_financiero** | assets, liabilities, balance sheet, cash flow |
| **sentencia_judicial** | sentence, court, ruling, plaintiff |
| **laboral** | labor contract, employee, salary, benefits |
| **mercantil** | company, corporate purpose, capital, shareholders |

### **database.py** - Data Management
`Database` class that handles:
- **Documents table** with fields: id, title, text, category, confidence, compliance, hash_integrity, explanation, hits, misses, cited_articles, created_at
- **CRUD operations** with methods `insert_document()`, `get_documents()`, `fetch_documents()`
- **Pagination and filters** by category and text search
- **JSON serialization** for array fields (hits, misses, cited_articles)

### **ingestion.py** - File Processing
`DocumentIngestion` class with capabilities for:
- **Text extraction** from PDF (PyMuPDF), DOCX (docx2txt) and TXT
- **File validation** (supported types, maximum size 50MB)
- **Robust error handling** with `ExtractionResult`
- **Multiple encodings** for text files

### **compliance/compliance_engine.py** - Regulatory Validation
Engine that validates documents using:
- **Contextual explanation system** by category
- **Compliance status**: ✅ (compliant), ⚠️ (partial), ❌ (non-compliant)
- **Structured return** with `ExplanationResult`

### **explanation/explanation.py** - Contextual Analysis
Advanced system that generates:
- **Pattern detection** with regex for legal elements
- **Hits and misses** by category keywords
- **Percentage calculation** of compliance (≥60% = ✅, 30-59% = ⚠️, <30% = ❌)
- **Smart fragmentation** of text into sentences
- **Automatically extracted** cited articles

### **security/encryption.py** - Security
`Hasher` utility for:
- **SHA256 hash** of document content
- **Data integrity** to detect modifications
- **Input validation** with error handling

### **demo_dataset.py** - Test Data
Dataset with 10 example documents that includes:
- **Variety of categories** (contracts, sentences, invoices, minutes)
- **Different compliance states** (✅, ⚠️, ❌)
- **Complete data** with hash, explanations and analysis

## 🛠️ Installation and Configuration

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone/locate the project**
```bash
cd C:\Users\heily\Desktop\demos\demo_1\clasificador_docs\back
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### 🔄 **POST** `/upload_document/`
Processes a complete file: extraction → classification → compliance → storage

**Request**: File (PDF/DOCX/TXT)

**Response**:
```json
{
  "success": true,
  "document_id": 123,
  "filename": "contract.pdf",
  "category": "contrato",
  "confidence": 0.85,
  "compliance_status": "✅",
  "explanation": "Analysis summary...",
  "cited_articles": ["art. 1", "art. 2"],
  "hits": ["parties", "contract object"],
  "misses": ["penalty clause"],
  "hash_integrity": "a1b2c3d4...",
  "created_at": "2025-09-01T10:30:00"
}
```

### 📄 **GET** `/documents`
Lists all stored documents

**Response**:
```json
{
  "documents": [...],
  "count": 25,
  "message": "Document list obtained successfully"
}
```

### 📋 **GET** `/list_documents/`
List with pagination and filters

**Query Parameters**:
- `category` (optional): Filter by category
- `page` (default=1): Page number
- `page_size` (default=10, max=100): Documents per page

### 🔍 **GET** `/search_documents/`
Text search in documents

**Query Parameters**:
- `query` (required): Search term
- `category` (optional): Filter by category
- `page`, `page_size`: Pagination

### 🎯 **POST** `/load_demo/`
Loads 10 demonstration documents (avoids duplicates by hash)

## 💾 Database

### `documents` Table
| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Auto-incremental ID |
| `title` | TEXT | Document title |
| `text` | TEXT | Extracted content |
| `category` | TEXT | Classified category |
| `confidence` | REAL | Classification confidence (0-1) |
| `compliance` | TEXT | Status: ✅, ⚠️, ❌ |
| `hash_integrity` | TEXT | SHA256 hash of content |
| `explanation` | TEXT | Analysis summary |
| `hits` | TEXT | JSON: found keywords |
| `misses` | TEXT | JSON: missing keywords |
| `cited_articles` | TEXT | JSON: extracted articles |
| `created_at` | TIMESTAMP | Creation date |

## 🔒 Security and Compliance

- **File validation**: Allowed types, maximum size 50MB
- **Integrity hash**: SHA256 to detect modifications
- **Sanitization**: Cleaning of search queries
- **CORS configured**: Allows cross-origin requests
- **Structured logging**: Complete operation traceability

## 📊 Processing Flow

```
📁 File → 🔍 Validation → 📄 Text Extraction → 
🏷️ Classification → ⚖️ Compliance → 🔐 SHA256 Hash → 
💾 Database → 📋 Audit Trail → ✅ JSON Response
```

## 🎮 Demonstration Data

The system includes 10 example documents with:
- **Contracts** (lease, service provision, confidentiality)
- **Judicial sentences** (favorable and dismissive)
- **Regulations** (internal regulations, security)
- **Licenses** (software, image usage)
- **Varied compliance states** for testing

## 🧪 Testing

To test the API:

1. **Interactive documentation**: http://localhost:8000/docs
2. **Load demos**: `POST /load_demo/`
3. **Upload document**: `POST /upload_document/` with file
4. **Search**: `GET /search_documents/?query=contract`

## 📦 Main Dependencies

- **FastAPI** 0.116.1+ - Web framework
- **Transformers** 4.55.4+ - Natural language processing
- **PyMuPDF** 1.26.4+ - PDF text extraction
- **docx2txt** 0.9+ - Word file processing
- **sqlite-utils** 3.38+ - Database utilities
- **uvicorn** 0.35.0+ - ASGI server

## 🏃‍♂️ Quick Start

```bash
# Activate environment
.venv\Scripts\activate

# Run server
python -m uvicorn app.main:app --reload

# Load demo data
curl -X POST http://localhost:8000/load_demo/

# List documents
curl http://localhost:8000/documents
```

## 📝 Development Notes

- **CORS enabled** for frontend development
- **Logging configured** at INFO level
- **Error handling** with HTTPException
- **Automatic timestamps** in database
- **Duplicate prevention** by content hash
