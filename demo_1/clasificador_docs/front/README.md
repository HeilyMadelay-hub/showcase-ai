# Frontend - Document Classifier

Modern and responsive web interface developed with HTML5, CSS3 and vanilla JavaScript for the automatic legal document classification system.

## 🎨 Design Features

- **Glassmorphism UI** - Modern interface with glass effects and blur
- **Dark Theme** - Professional dark theme with gradients
- **Responsive Design** - Fully adaptable to mobile and tablets  
- **Fluid Animations** - Smooth transitions and hover effects
- **FontAwesome Iconography** - Vector icons for better UX

## 📁 Frontend Structure

```
front/static/
├── index.html    # Main SPA page
├── script.js     # JavaScript logic (API calls, DOM manipulation)
└── style.css     # Styles with glassmorphism and dark theme
```

## 🖥️ Interface Components

### **Smart Header**
- **Main title** with justice scale icon
- **Real-time API connection status** with visual indicator
- **Backend URL** shown dynamically
- **Sticky design** that remains visible when scrolling

### **Upload Section** 
- **Visual drag zone** for files
- **Type validation** (PDF, DOCX, TXT)
- **Selected filename preview**
- **Analysis button** with loading states

### **Complete Analysis Results**
Shows detailed information after processing:

#### 🏷️ **Main Classification**
- **Category badge** with distinctive colors
- **Animated confidence bar** with percentage
- **Visual classification** by document type

#### ⚖️ **Compliance Status**
- **Visual indicators**: ✅ (compliant), ⚠️ (partial), ❌ (non-compliant)
- **Detailed explanation** of regulatory analysis
- **Semantic colors** for states

#### 📖 **Cited Articles**
- **Interactive pills** with detected articles
- **Dynamic counter** of references
- **Hover effects** for better interaction

#### 📊 **Hits and Misses Analysis**
- **Statistics grid** divided into matches/failures
- **Scrollable list** of detected patterns
- **Contextual icons** (✓ for hits, ✗ for misses)
- **Automatic counters** per section

#### 🔒 **Document Integrity**
- **SHA256 hash** displayed in code format
- **Copy button** to clipboard
- **Metadata** with creation date and ID
- **Special design** with security gradient

### **Search and Filter System**
- **Text search** in document content
- **Category filter** with dropdown options
- **Demo load button** for test data
- **Responsive grid** that adapts to space

### **Advanced Documents Table**
- **Organized columns**: ID, Name, Category, Confidence, Compliance, Date, Actions
- **Visual badges** for categories and compliance
- **Mini confidence bars** in each row
- **"View" button** to open details modal
- **Empty state** when no documents exist

### **Pagination System**
- **Previous/next navigation** with buttons
- **Current and total page** information
- **Disabled states** at limits
- **Auto-scroll** when changing page

### **Details Modal**
- **Expanded view** of selected document
- **Complete information**: ID, title, category, confidence, compliance, explanation, date
- **Close with X** or click outside modal
- **Smooth entrance animation**

### **Toast Notification System**
- **4 notification types**: success, error, warning, info
- **Auto-disappear** after 5 seconds
- **Manual close button**
- **Visual progress bar** of time
- **Fixed positioning** in top-right corner

## ⚙️ JavaScript Functionalities

### **Global Application State**
```javascript
let state = {
  documents: [],           // Current documents list
  currentPage: 1,          // Current page
  pageSize: 10,            // Documents per page
  totalDocuments: 0,       // Total documents
  currentCategory: '',     // Active category filter
  currentQuery: '',        // Active search term
  mode: 'list',           // 'list' or 'search'
  lastUploadResult: null   // Last uploaded document
};
```

### **Backend API Connection**
- **Automatic verification** of connection on page load
- **Configurable URL** via localStorage (`API_BASE_URL`)
- **Visual indicator** of connection status (green/red)
- **Robust handling** of connection errors

### **File Management**
- **Client-side validation** of file types
- **Asynchronous upload** with FormData
- **Visual feedback** during processing
- **Automatic cleanup** of form after success

### **REST API Interaction**
Complete integration with backend endpoints:

| Endpoint | Function | Description |
|----------|----------|-------------|
| `POST /upload_document/` | `handleFileUpload()` | Upload and analyze document |
| `GET /list_documents/` | `loadDocuments()` | Paginated list |
| `GET /search_documents/` | `handleSearch()` | Text search |
| `POST /load_demo/` | `handleLoadDemo()` | Load demo data |

### **Visualization Functions**
- **`displayAnalysisResults()`** - Shows complete analysis results
- **`renderDocumentsTable()`** - Generates HTML table dynamically
- **`displayHitsAndMisses()`** - Visualizes matches and failures
- **`viewDocumentDetails()`** - Opens modal with detailed information

### **Utilities and Helpers**
- **`formatDate()` / `formatDateTime()`** - Localized date formatting
- **`getConfidencePercent()`** - Confidence to percentage conversion
- **`escapeHtml()`** - XSS prevention in dynamic content
- **`copyHash()`** - Copy hash to clipboard with Clipboard API

## 🎯 User Flow

```
📄 Select File → ⬆️ Upload → 🔄 Processing → 
📊 Visual Results → 📋 Document List → 
🔍 Search/Filters → 👁️ View Details → 📋 Information Modal
```

## 🎨 Styling System

### **Custom CSS Variables**
```css
:root {
  --primary: #4f8cff;        /* Primary blue */
  --secondary: #14b8a6;      /* Secondary green */
  --success: #10b981;        /* Success green */
  --warning: #f59e0b;        /* Warning yellow */
  --danger: #ef4444;         /* Danger red */
  --dark: #0b0f14;           /* Main background */
  --glass: rgba(255,255,255,0.05); /* Glass effect */
}
```

### **Reusable Components**
- **`.glass-card`** - Cards with glassmorphism effect
- **`.btn` variants** - Buttons with animations (primary, secondary, outline)
- **`.category-badge`** - Category badges with colors
- **`.compliance-badge`** - Compliance states with traffic light
- **`.confidence-meter`** - Animated progress bars
- **`.toast`** - Notifications with 4 visual types

### **Special Effects**
- **Shimmer animation** - Shiny effect on card borders
- **Hover transformations** - 3D elevation on cards
- **Loading spinners** - Loading indicators in buttons
- **Slide animations** - Smooth element appearance
- **Backdrop blur** - Background blur in modals

## 📱 Responsive Design

### **Breakpoints**
- **Desktop**: >768px - Complete layout with 3-column grid
- **Tablet**: ≤768px - Adaptive grid and simplified navigation  
- **Mobile**: ≤480px - Vertical layout, full-width buttons

### **Mobile Adaptations**
- **Responsive table** with horizontal scroll
- **Full-screen modal** on small devices
- **Touch-friendly buttons** with minimum size
- **Full-width toast** on small screens
- **Collapsible grid** to single column

## 🔧 Configuration and Installation

### **Prerequisites**
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Backend running on `http://localhost:8000`

### **Installation**
```bash
# Navigate to frontend directory
cd C:\Users\heily\Desktop\demos\demo_1\clasificador_docs\front\static

# Open with local server (optional)
python -m http.server 3000
# Or simply open index.html directly in browser
```

### **API Configuration**
Frontend automatically connects to `http://localhost:8000`. To change URL:

```javascript
// In browser console or localStorage
localStorage.setItem("API_BASE_URL", "http://your-server:port");
```

## 🚀 Application Usage

### **1. Upload and Analyze Document**
1. Click "Select file" or drag file
2. Choose PDF, DOCX or TXT
3. Press "Analyze Document"
4. View complete results with:
   - Identified category
   - Confidence level
   - Compliance status
   - Detailed hits and misses
   - Integrity hash

### **2. Search Documents**
- **By content**: Type term in search box
- **By category**: Select from dropdown
- **Combined**: Use both filters simultaneously

### **3. Navigate Results**
- **View list**: Table with all documents
- **Pagination**: Page navigation
- **View details**: Modal with complete information
- **Copy hash**: Button to copy to clipboard

### **4. Load Demo Data**
- Press "Load Demo Dataset"
- Loads 10 example documents
- Automatically avoids duplicates

## 🎯 Supported Categories

Frontend recognizes and colors the following categories:

| Category | Color | Description |
|----------|-------|-------------|
| **contrato** | 🔵 Blue | General contracts |
| **sentencia** | 🟢 Green | Judicial sentences |
| **normativa** | 🔵 Info | Regulations and norms |
| **fiscal** | 🟡 Yellow | Tax documents |
| **laboral** | 🟢 Green | Labor contracts |
| **licencia** | 🔴 Red | Licenses and permits |
| **auto_resolucion** | ⚫ Gray | Autos and resolutions |
| **poder_notarial** | 🔵 Blue | Notarial powers |

## 🔔 Notification System

### **Toast Types**
- **✅ Success** (green) - Successful operations
- **❌ Error** (red) - Errors and failures
- **⚠️ Warning** (yellow) - Warnings
- **ℹ️ Info** (blue) - General information

### **Events that Generate Notifications**
- Successful/failed document upload
- API connection/disconnection
- Search results
- Demo data loading
- Hash copied to clipboard
- Form validations

## 📊 Visual Metrics

### **Confidence Bar**
- **0-30%**: Short bar, blue gradient color
- **30-70%**: Medium bar, smooth transition
- **70-100%**: Complete bar, bright color
- **Animation**: Smooth 1-second growth

### **Compliance States**
- **✅ Green** - Meets regulations (≥60% keywords)
- **⚠️ Yellow** - Partial compliance (30-59%)
- **❌ Red** - Non-compliant (<30%)

### **Dynamic Counters**
- **Total documents** in table header
- **Hits found** in analysis
- **Misses detected** in validation
- **Cited articles** extracted

## 🔍 Search Functionalities

### **Text Search**
- **Responsive input** with descriptive placeholder
- **Real-time search** on Enter press
- **Paginated results** with navigation
- **Visual highlighting** of terms (future)

### **Category Filters**
- **Organized dropdown** with all categories
- **"All" option** to reset filter
- **Combination** with text search
- **Persistent state** during navigation

### **Smart Pagination**
- **10 documents** per page by default
- **Previous/next buttons** with states
- **Current/total page** information
- **Auto-scroll** when changing page
- **Automatic hiding** if <10 documents

## 💻 Backend Interaction

### **API Configuration**
```javascript
const API_BASE_URL = localStorage.getItem("API_BASE_URL") || "http://localhost:8000";
```

### **Used Endpoints**
- **`POST /upload_document/`** - Upload and complete analysis
- **`GET /list_documents/`** - Paginated list with filters
- **`GET /search_documents/`** - Text search
- **`POST /load_demo/`** - Load demo data
- **`GET /docs`** - API status verification

### **Response Handling**
```javascript
// Expected upload response structure
{
  "success": true,
  "document_id": 123,
  "filename": "contract.pdf",
  "category": "contrato",
  "confidence": 0.85,
  "compliance_status": "✅",
  "explanation": "Detailed analysis...",
  "cited_articles": ["art. 1", "art. 2"],
  "hits": ["parties", "contract object"],
  "misses": ["penalty clause"],
  "hash_integrity": "a1b2c3d4...",
  "created_at": "2025-09-01T10:30:00"
}
```

## 🛡️ Frontend Security

### **Client-Side Validations**
- **Allowed file types** (.pdf, .docx, .txt)
- **Maximum size** validated before upload
- **HTML sanitization** with `escapeHtml()`
- **Non-empty search input** validation

### **XSS Prevention**
- **Dynamic content escaping** in DOM
- **Sanitization** of data received from API
- **Type validation** before rendering

## 🎮 Advanced Interactivity

### **Loading States**
- **Buttons with spinner** during operations
- **Dynamic text** ("Analyzing...", "Searching...")
- **Temporary disabling** to prevent double-click
- **Automatic restoration** after completion

### **CSS Animations**
- **fadeIn** - Smooth element appearance
- **slideUp** - Modal entrance from bottom
- **shimmer** - Shiny effect on borders
- **pulse** - API indicator pulsation
- **spin** - Loading icon rotation

### **Hover Effects**
- **3D elevation** on cards
- **Color change** on buttons
- **Smooth transformations** on interactive elements
- **Accessible outline focus** on inputs

## 📱 Mobile Optimization

### **Touch Interactions**
- **Minimum button size** 44px for easy touch
- **Generous spacing** between interactive elements
- **Smooth scroll** in lists and tables
- **Zoom disabled** on inputs to avoid auto-zoom

### **Adaptive Layout**
- **Collapsible grid** from 3 columns to 1 on mobile
- **Horizontal table** with scroll on small screens
- **Full-screen modal** on small devices
- **Vertical stack** of controls on mobile

## 🏃‍♂️ Quick Start

1. **Ensure backend running** on `http://localhost:8000`
2. **Open `index.html`** directly in browser
3. **Verify connection** - green indicator in header
4. **Load demo data** - "Load Demo Dataset" button
5. **Test upload** - select file and analyze
6. **Explore interface** - search, filter, view details

## 🔧 Customization

### **Change Colors**
Modify CSS variables in `style.css`:
```css
:root {
  --primary: #your-primary-color;
  --secondary: #your-secondary-color;
  /* ... more variables ... */
}
```

### **Adjust Pagination**
Change in `script.js`:
```javascript
let state = {
  pageSize: 20, // Change from 10 to 20 documents per page
  // ...
};
```

### **Configure API URL**
```javascript
localStorage.setItem("API_BASE_URL", "https://your-api.com");
```

## 🧪 Testing and Debug

### **Browser Console**
Frontend includes detailed logging:
- **API connection status**
- **Processed document data**
- **Validation and formatting errors**
- **Pagination and search flow**

### **Automatic Verifications**
- **API status** on page load
- **Data validation** before rendering
- **Fallbacks** for missing or incorrect data
- **Error handling** with toast notifications

## 📈 Technical Features

- **SPA (Single Page Application)** - No page reloads
- **Centralized state** - Consistent data management
- **RESTful API** - Standard backend integration
- **CSS Grid/Flexbox** - Modern and flexible layout
- **ES6+** - Modern JavaScript with async/await
- **Font Awesome 6.4.0** - Vector iconography
- **localStorage** - Configuration persistence
