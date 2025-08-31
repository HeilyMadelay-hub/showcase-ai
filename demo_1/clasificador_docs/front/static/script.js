// ============================================
// CONFIGURACIÓN GLOBAL
// ============================================
const API_BASE_URL = localStorage.getItem("API_BASE_URL") || "http://localhost:8000";

// Estado global de la aplicación
let state = {
  documents: [],
  currentPage: 1,
  pageSize: 10,
  totalDocuments: 0,
  currentCategory: '',
  currentQuery: '',
  mode: 'list', // 'list' o 'search'
  lastUploadResult: null
};

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Iniciando aplicación...');
  console.log('📡 API URL:', API_BASE_URL);
  
  // Mostrar URL de la API
  const apiUrlElement = document.getElementById('apiUrl');
  if (apiUrlElement) {
    apiUrlElement.textContent = API_BASE_URL;
  }
  
  // Verificar conexión con la API
  await checkAPIConnection();
  
  // Cargar documentos iniciales
  await loadDocuments();
  
  // Configurar event listeners
  setupEventListeners();
});

// ============================================
// VERIFICACIÓN DE CONEXIÓN API
// ============================================
async function checkAPIConnection() {
  const statusIndicator = document.getElementById('apiStatus');
  try {
    const response = await fetch(`${API_BASE_URL}/docs`);
    if (response.ok) {
      statusIndicator.style.background = '#10b981';
      console.log('✅ Conexión con API establecida');
    } else {
      throw new Error('API no responde correctamente');
    }
  } catch (error) {
    statusIndicator.style.background = '#ef4444';
    console.error('❌ Error conectando con API:', error);
    showToast('No se pudo conectar con el servidor', 'error');
  }
}

// ============================================
// EVENT LISTENERS
// ============================================
function setupEventListeners() {
  // Upload de archivo
  const uploadForm = document.getElementById('uploadForm');
  const fileInput = document.getElementById('fileInput');
  const fileName = document.getElementById('fileName');
  
  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        fileName.textContent = file.name;
      }
    });
  }
  
  if (uploadForm) {
    uploadForm.addEventListener('submit', handleFileUpload);
  }
  
  // Búsqueda
  const searchBtn = document.getElementById('searchBtn');
  if (searchBtn) {
    searchBtn.addEventListener('click', handleSearch);
  }
  
  // Filtro por categoría
  const filterBtn = document.getElementById('filterBtn');
  if (filterBtn) {
    filterBtn.addEventListener('click', handleFilter);
  }
  
  // Cargar datos demo
  const loadDemoBtn = document.getElementById('loadDemoBtn');
  if (loadDemoBtn) {
    loadDemoBtn.addEventListener('click', handleLoadDemo);
  }
  
  // Paginación
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  
  if (prevBtn) {
    prevBtn.addEventListener('click', () => changePage(state.currentPage - 1));
  }
  
  if (nextBtn) {
    nextBtn.addEventListener('click', () => changePage(state.currentPage + 1));
  }
  
  // Enter en búsqueda
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        handleSearch();
      }
    });
  }
}

// ============================================
// UPLOAD DE DOCUMENTOS
// ============================================
async function handleFileUpload(e) {
  e.preventDefault();
  
  const fileInput = document.getElementById('fileInput');
  const uploadBtn = document.getElementById('uploadBtn');
  const file = fileInput.files[0];
  
  if (!file) {
    showToast('Por favor selecciona un archivo', 'warning');
    return;
  }
  
  // Validar tipo de archivo
  const validExtensions = ['.pdf', '.docx', '.txt'];
  const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
  
  if (!validExtensions.includes(fileExtension)) {
    showToast(`Tipo de archivo no soportado. Use: ${validExtensions.join(', ')}`, 'error');
    return;
  }
  
  // Preparar FormData
  const formData = new FormData();
  formData.append('file', file);
  
  // Deshabilitar botón y mostrar loading
  setButtonLoading(uploadBtn, true, 'Analizando...');
  
  try {
    const response = await fetch(`${API_BASE_URL}/upload_document/`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'Error al subir el archivo');
    }
    
    const result = await response.json();
    
    if (result.success) {
      // Mostrar resultados detallados
      displayAnalysisResults(result);
      
      // Mostrar notificación de éxito
      showToast(`✅ Documento "${result.filename}" analizado exitosamente`, 'success');
      
      // Limpiar input
      fileInput.value = '';
      document.getElementById('fileName').textContent = 'Seleccionar archivo PDF, DOCX o TXT';
      
      // Recargar lista de documentos
      await loadDocuments();
      
      // Guardar último resultado
      state.lastUploadResult = result;
    } else {
      throw new Error(result.error || 'Error desconocido');
    }
  } catch (error) {
    console.error('Error:', error);
    showToast(`Error: ${error.message}`, 'error');
  } finally {
    setButtonLoading(uploadBtn, false, '<i class="fas fa-upload"></i> Analizar Documento');
  }
}

// ============================================
// MOSTRAR RESULTADOS DEL ANÁLISIS
// ============================================
function displayAnalysisResults(data) {
  const resultsSection = document.getElementById('analysisResults');
  if (!resultsSection) return;
  
  // Mostrar sección de resultados
  resultsSection.classList.remove('hidden');
  
  // 1. Categoría y confianza
  const categoryBadge = document.getElementById('categoryBadge');
  const confidenceBar = document.getElementById('confidenceBar');
  const confidenceText = document.getElementById('confidenceText');
  
  if (categoryBadge) {
    categoryBadge.textContent = data.category || 'Sin clasificar';
    categoryBadge.className = `category-badge ${getCategoryClass(data.category)}`;
  }
  
  if (confidenceBar && confidenceText) {
    const confidence = data.confidence || 0;
    const confidencePercent = getConfidencePercent(confidence);
    
    console.log('Confidence data:', {
      raw: data.confidence,
      processed: confidence,
      percent: confidencePercent
    });
    
    // Animar la barra
    setTimeout(() => {
      confidenceBar.style.width = `${confidencePercent}%`;
    }, 100);
    
    confidenceText.textContent = `${confidencePercent}%`;
  }
  
  // 2. Estado de Compliance
  const complianceStatus = document.getElementById('complianceStatus');
  const explanation = document.getElementById('explanation');
  
  if (complianceStatus) {
    complianceStatus.textContent = data.compliance_status || '❌';
    complianceStatus.className = `compliance-badge ${getComplianceClass(data.compliance_status)}`;
  }
  
  if (explanation) {
    explanation.textContent = data.explanation || 'Sin explicación disponible';
  }
  
  // 3. Artículos citados
  const citedArticles = document.getElementById('citedArticles');
  const articlesCount = document.getElementById('articlesCount');
  const citedArticlesCard = document.getElementById('citedArticlesCard');
  
  if (data.cited_articles && data.cited_articles.length > 0) {
    citedArticlesCard.classList.remove('hidden');
    articlesCount.textContent = data.cited_articles.length;
    
    citedArticles.innerHTML = data.cited_articles.map(article => 
      `<span class="article-pill">${escapeHtml(article)}</span>`
    ).join('');
  } else {
    citedArticlesCard.classList.add('hidden');
  }
  
  // 4. Hits y Misses
  displayHitsAndMisses(data.hits || [], data.misses || []);
  
  // 5. Integridad del documento
  const hashIntegrity = document.getElementById('hashIntegrity');
  const createdAt = document.getElementById('createdAt');
  const documentId = document.getElementById('documentId');
  
  if (hashIntegrity) {
    hashIntegrity.textContent = data.hash_integrity || 'No disponible';
  }
  
  if (createdAt) {
    createdAt.textContent = formatDateTime(data.created_at);
  }
  
  if (documentId) {
    documentId.textContent = data.document_id || 'N/A';
  }
  
  // Hacer scroll suave a los resultados
  resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ============================================
// MOSTRAR HITS Y MISSES
// ============================================
function displayHitsAndMisses(hits, misses) {
  const hitsList = document.getElementById('hitsList');
  const missesList = document.getElementById('missesList');
  const hitsCount = document.getElementById('hitsCount');
  const missesCount = document.getElementById('missesCount');
  
  // Actualizar contadores
  if (hitsCount) hitsCount.textContent = hits.length;
  if (missesCount) missesCount.textContent = misses.length;
  
  // Mostrar hits
  if (hitsList) {
    if (hits.length > 0) {
      hitsList.innerHTML = hits.map(hit => `
        <div class="match-item">
          <strong>${escapeHtml(hit.pattern || hit)}</strong>
          ${hit.context ? `<span>${escapeHtml(hit.context)}</span>` : ''}
        </div>
      `).join('');
    } else {
      hitsList.innerHTML = '<div class="match-item">No se encontraron coincidencias</div>';
    }
  }
  
  // Mostrar misses
  if (missesList) {
    if (misses.length > 0) {
      missesList.innerHTML = misses.map(miss => `
        <div class="match-item">
          <strong>${escapeHtml(miss.pattern || miss)}</strong>
          ${miss.reason ? `<span>${escapeHtml(miss.reason)}</span>` : ''}
        </div>
      `).join('');
    } else {
      missesList.innerHTML = '<div class="match-item">Todos los patrones coincidieron</div>';
    }
  }
}

// ============================================
// BÚSQUEDA DE DOCUMENTOS
// ============================================
async function handleSearch() {
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  const query = searchInput.value.trim();
  
  if (!query) {
    showToast('Por favor ingresa un término de búsqueda', 'warning');
    return;
  }
  
  state.mode = 'search';
  state.currentQuery = query;
  state.currentPage = 1;
  
  setButtonLoading(searchBtn, true, 'Buscando...');
  
  try {
    const params = new URLSearchParams({
      query: query,
      category: state.currentCategory,
      page: state.currentPage,
      page_size: state.pageSize
    });
    
    const response = await fetch(`${API_BASE_URL}/search_documents/?${params}`);
    
    if (!response.ok) {
      throw new Error('Error en la búsqueda');
    }
    
    const data = await response.json();
    
    if (data.success) {
      state.documents = data.documents || [];
      state.totalDocuments = data.total || 0;
      
      renderDocumentsTable();
      updatePagination();
      
      showToast(`Se encontraron ${data.total} documentos`, 'info');
    }
  } catch (error) {
    console.error('Error:', error);
    showToast('Error al buscar documentos', 'error');
  } finally {
    setButtonLoading(searchBtn, false, '<i class="fas fa-search"></i> Buscar');
  }
}

// ============================================
// FILTRAR POR CATEGORÍA
// ============================================
async function handleFilter() {
  const categorySelect = document.getElementById('categorySelect');
  const filterBtn = document.getElementById('filterBtn');
  
  state.currentCategory = categorySelect.value;
  state.currentPage = 1;
  state.mode = 'list';
  
  setButtonLoading(filterBtn, true, 'Filtrando...');
  
  await loadDocuments();
  
  setButtonLoading(filterBtn, false, '<i class="fas fa-filter"></i> Filtrar');
  
  const categoryText = state.currentCategory ? 
    `Mostrando categoría: ${state.currentCategory}` : 
    'Mostrando todas las categorías';
  
  showToast(categoryText, 'info');
}

// ============================================
// CARGAR DATOS DEMO
// ============================================
async function handleLoadDemo() {
  const loadDemoBtn = document.getElementById('loadDemoBtn');
  
  setButtonLoading(loadDemoBtn, true, 'Cargando demo...');
  
  try {
    const response = await fetch(`${API_BASE_URL}/load_demo/`, {
      method: 'POST'
    });
    
    if (!response.ok) {
      throw new Error('Error al cargar datos demo');
    }
    
    const result = await response.json();
    
    if (result.success) {
      showToast(result.message || 'Datos demo cargados correctamente', 'success');
      await loadDocuments();
    } else {
      throw new Error(result.error || 'Error desconocido');
    }
  } catch (error) {
    console.error('Error:', error);
    showToast('Error al cargar datos demo', 'error');
  } finally {
    setButtonLoading(loadDemoBtn, false, '<i class="fas fa-download"></i> Cargar Dataset Demo');
  }
}

// ============================================
// CARGAR DOCUMENTOS
// ============================================
async function loadDocuments() {
  try {
    const params = new URLSearchParams({
      page: state.currentPage,
      page_size: state.pageSize
    });
    
    if (state.currentCategory) {
      params.append('category', state.currentCategory);
    }
    
    const endpoint = state.mode === 'search' && state.currentQuery ? 
      `/search_documents/?query=${encodeURIComponent(state.currentQuery)}&${params}` :
      `/list_documents/?${params}`;
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    
    if (!response.ok) {
      throw new Error('Error al cargar documentos');
    }
    
    const data = await response.json();
    
    if (data.success || data.documents) {
      state.documents = data.documents || [];
      state.totalDocuments = data.total || 0;
      
      renderDocumentsTable();
      updatePagination();
    }
  } catch (error) {
    console.error('Error cargando documentos:', error);
    state.documents = [];
    state.totalDocuments = 0;
    renderDocumentsTable();
  }
}

// ============================================
// RENDERIZAR TABLA DE DOCUMENTOS - CORREGIDO
// ============================================
function renderDocumentsTable() {
  const tbody = document.getElementById('resultsBody');
  const emptyState = document.getElementById('emptyState');
  const table = document.getElementById('resultsTable');
  const totalCount = document.getElementById('totalCount');
  
  if (totalCount) {
    totalCount.textContent = `${state.totalDocuments} documentos`;
  }
  
  if (!tbody) return;
  
  if (state.documents.length === 0) {
    tbody.innerHTML = '';
    if (emptyState) emptyState.classList.remove('hidden');
    if (table) table.parentElement.classList.add('hidden');
    return;
  }
  
  if (emptyState) emptyState.classList.add('hidden');
  if (table) table.parentElement.classList.remove('hidden');
  
  tbody.innerHTML = state.documents.map(doc => {
    // Validar y procesar datos del documento
    const docId = doc.id || doc.document_id || 'N/A';
    const docTitle = escapeHtml(doc.title || doc.filename || 'Sin título');
    const docCategory = doc.category || 'Sin clasificar';
    const docConfidence = getConfidencePercent(doc.confidence);
    const docCompliance = doc.compliance_status || doc.compliance || '❌';
    const docDate = formatDate(doc.created_at || doc.date_created);
    
    console.log('Renderizando documento:', {
      id: docId,
      title: docTitle,
      confidence: docConfidence,
      date: docDate,
      raw_confidence: doc.confidence
    });
    
    return `
      <tr>
        <td>${docId}</td>
        <td>${docTitle}</td>
        <td>
          <span class="category-badge ${getCategoryClass(docCategory)}">
            ${docCategory}
          </span>
        </td>
        <td>
          <div class="confidence-meter-small">
            <div class="confidence-bar" style="width: ${docConfidence}%"></div>
          </div>
          <small>${docConfidence}%</small>
        </td>
        <td>
          <span class="compliance-badge ${getComplianceClass(docCompliance)}">
            ${docCompliance}
          </span>
        </td>
        <td>${docDate}</td>
        <td>
          <button class="btn-view" onclick="viewDocumentDetails('${docId}')">
            <i class="fas fa-eye"></i> Ver
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

// ============================================
// VER DETALLES DEL DOCUMENTO - CORREGIDO
// ============================================
function viewDocumentDetails(docId) {
  const doc = state.documents.find(d => 
    d.id == docId || d.document_id == docId
  );
  if (!doc) {
    console.error('Documento no encontrado:', docId);
    return;
  }
  
  const modal = document.getElementById('detailsModal');
  const modalBody = document.getElementById('modalBody');
  
  if (!modal || !modalBody) return;
  
  // Procesar datos del documento
  const docId2 = doc.id || doc.document_id || 'N/A';
  const docTitle = escapeHtml(doc.title || doc.filename || 'Sin título');
  const docCategory = doc.category || 'Sin clasificar';
  const docConfidence = getConfidencePercent(doc.confidence);
  const docCompliance = doc.compliance_status || doc.compliance || '❌';
  const docExplanation = doc.explanation || 'Sin explicación disponible';
  const docCreatedAt = formatDateTime(doc.created_at || doc.date_created);
  
  modalBody.innerHTML = `
    <div class="modal-details">
      <div class="detail-row">
        <span class="detail-label">ID:</span>
        <span>${docId2}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Título:</span>
        <span>${docTitle}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Categoría:</span>
        <span class="category-badge ${getCategoryClass(docCategory)}">
          ${docCategory}
        </span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Confianza:</span>
        <span>${docConfidence}%</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Compliance:</span>
        <span class="compliance-badge ${getComplianceClass(docCompliance)}">
          ${docCompliance}
        </span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Explicación:</span>
        <p>${escapeHtml(docExplanation)}</p>
      </div>
      <div class="detail-row">
        <span class="detail-label">Fecha de creación:</span>
        <span>${docCreatedAt}</span>
      </div>
    </div>
  `;
  
  modal.classList.remove('hidden');
}

// ============================================
// CERRAR MODAL
// ============================================
function closeModal() {
  const modal = document.getElementById('detailsModal');
  if (modal) {
    modal.classList.add('hidden');
  }
}

// ============================================
// COPIAR HASH
// ============================================
async function copyHash() {
  const hashElement = document.getElementById('hashIntegrity');
  if (!hashElement) return;
  
  const hash = hashElement.textContent;
  
  try {
    await navigator.clipboard.writeText(hash);
    showToast('Hash copiado al portapapeles', 'success');
  } catch (error) {
    console.error('Error al copiar:', error);
    showToast('No se pudo copiar el hash', 'error');
  }
}

// ============================================
// PAGINACIÓN
// ============================================
function updatePagination() {
  const pagination = document.getElementById('pagination');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const currentPageSpan = document.getElementById('currentPage');
  const totalPagesSpan = document.getElementById('totalPages');
  
  const totalPages = Math.ceil(state.totalDocuments / state.pageSize) || 1;
  
  if (pagination) {
    if (state.totalDocuments > state.pageSize) {
      pagination.classList.remove('hidden');
    } else {
      pagination.classList.add('hidden');
      return;
    }
  }
  
  if (currentPageSpan) currentPageSpan.textContent = state.currentPage;
  if (totalPagesSpan) totalPagesSpan.textContent = totalPages;
  
  if (prevBtn) {
    prevBtn.disabled = state.currentPage <= 1;
  }
  
  if (nextBtn) {
    nextBtn.disabled = state.currentPage >= totalPages;
  }
}

async function changePage(newPage) {
  const totalPages = Math.ceil(state.totalDocuments / state.pageSize) || 1;
  
  if (newPage < 1 || newPage > totalPages) return;
  
  state.currentPage = newPage;
  await loadDocuments();
  
  // Scroll to top of results
  const resultsSection = document.querySelector('.results-section');
  if (resultsSection) {
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// ============================================
// NOTIFICACIONES TOAST
// ============================================
function showToast(message, type = 'info', duration = 5000) {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  
  const toast = document.createElement('div');
  toast.className = `toast toast-${type} fade-in`;
  
  const icon = {
    success: 'fa-check-circle',
    error: 'fa-exclamation-circle',
    warning: 'fa-exclamation-triangle',
    info: 'fa-info-circle'
  }[type] || 'fa-info-circle';
  
  toast.innerHTML = `
    <i class="fas ${icon}"></i>
    <span>${message}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">
      <i class="fas fa-times"></i>
    </button>
  `;
  
  container.appendChild(toast);
  
  // Auto-remove after duration
  setTimeout(() => {
    toast.remove();
  }, duration);
}

// ============================================
// UTILIDADES - CORREGIDAS
// ============================================
function setButtonLoading(button, isLoading, text = null) {
  if (!button) return;
  
  if (isLoading) {
    button.disabled = true;
    button.classList.add('loading');
    if (text) {
      button.dataset.originalText = button.innerHTML;
      button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`;
    }
  } else {
    button.disabled = false;
    button.classList.remove('loading');
    if (button.dataset.originalText) {
      button.innerHTML = button.dataset.originalText;
      delete button.dataset.originalText;
    }
  }
}

function getCategoryClass(category) {
  const categoryMap = {
    'contrato': 'primary',
    'sentencia': 'secondary',
    'normativa': 'info',
    'fiscal': 'warning',
    'laboral': 'success',
    'licencia': 'danger',
    'auto_resolucion': 'dark',
    'poder_notarial': 'primary'
  };
  
  return categoryMap[category?.toLowerCase()] || 'default';
}

function getComplianceClass(status) {
  if (status === '✅' || status === 'compliant' || status === 'cumple') return 'success';
  if (status === '⚠️' || status === 'warning' || status === 'parcial') return 'warning';
  if (status === '❌' || status === 'non_compliant' || status === 'no_cumple') return 'danger';
  return 'default';
}

// ============================================
// FUNCIÓN CORREGIDA PARA CONFIANZA
// ============================================
function getConfidencePercent(confidence) {
  // Log para debug
  console.log('getConfidencePercent input:', confidence, typeof confidence);
  
  // Manejar casos nulos/undefined
  if (confidence === null || confidence === undefined || confidence === '' || isNaN(confidence)) {
    console.log('Confidence is null/undefined/empty/NaN, returning 0');
    return 0;
  }
  
  // Convertir a número si es string
  const numConfidence = typeof confidence === 'string' ? parseFloat(confidence) : confidence;
  
  // Validar que sea un número válido
  if (isNaN(numConfidence)) {
    console.log('Confidence is not a valid number, returning 0');
    return 0;
  }
  
  // Si confidence es mayor a 1, asumir que ya está en porcentaje
  if (numConfidence > 1) {
    const result = Math.round(Math.min(numConfidence, 100));
    console.log('Confidence > 1, treating as percentage:', result);
    return result;
  }
  
  // Si es menor o igual a 1, convertir a porcentaje
  const result = Math.round(numConfidence * 100);
  console.log('Confidence <= 1, converting to percentage:', result);
  return result;
}

// ============================================
// FUNCIÓN CORREGIDA PARA FECHAS
// ============================================
function formatDate(dateString) {
  console.log('formatDate input:', dateString, typeof dateString);
  
  // Manejar casos nulos/undefined/vacíos
  if (!dateString || dateString === '' || dateString === null || dateString === undefined) {
    console.log('Date is null/undefined/empty, returning -');
    return '-';
  }
  
  try {
    const date = new Date(dateString);
    
    // Verificar si la fecha es válida
    if (isNaN(date.getTime())) {
      console.log('Invalid date, returning original string:', dateString);
      return dateString.toString();
    }
    
    const result = date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
    
    console.log('Formatted date:', result);
    return result;
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateString.toString();
  }
}

function formatDateTime(dateString) {
  console.log('formatDateTime input:', dateString, typeof dateString);
  
  // Manejar casos nulos/undefined/vacíos
  if (!dateString || dateString === '' || dateString === null || dateString === undefined) {
    console.log('DateTime is null/undefined/empty, returning -');
    return '-';
  }
  
  try {
    const date = new Date(dateString);
    
    // Verificar si la fecha es válida
    if (isNaN(date.getTime())) {
      console.log('Invalid datetime, returning original string:', dateString);
      return dateString.toString();
    }
    
    const result = date.toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
    
    console.log('Formatted datetime:', result);
    return result;
  } catch (error) {
    console.error('Error formatting datetime:', error);
    return dateString.toString();
  }
}

function escapeHtml(text) {
  if (!text) return '';
  
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ============================================
// EXPORTAR FUNCIONES GLOBALES
// ============================================
window.viewDocumentDetails = viewDocumentDetails;
window.closeModal = closeModal;
window.copyHash = copyHash;