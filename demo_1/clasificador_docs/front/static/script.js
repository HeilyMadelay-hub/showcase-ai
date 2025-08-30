// ====== CONFIG ======
// Si despliegas, puedes fijarlo en localStorage:
// localStorage.setItem("API_BASE_URL", "https://TU-DOMINIO"); location.reload();
const API_BASE_URL =
  localStorage.getItem("API_BASE_URL") || "http://localhost:8000";

// Mostrar a qué API estamos apuntando (útil para depurar conexión front-back)
const apiUrlSpan = document.getElementById("apiUrl");
if (apiUrlSpan) apiUrlSpan.textContent = API_BASE_URL;

// ====== helpers ======
const $ = (s) => document.querySelector(s);
const qs = (s, el = document) => el.querySelector(s);

const showError = (msg) => {
  const box = $("#errorBox");
  if (box) {
    box.style.display = "block";
    box.textContent = msg;
  }
  toast(msg, "err", 8000);
};

const clearError = () => {
  const box = $("#errorBox");
  if (box) {
    box.style.display = "none";
    box.textContent = "";
  }
};

const toast = (msg, type = "ok", duration = 8000, asHTML = false) => {
  let t = $("#toaster");
  if (!t) {
    t = document.createElement("div");
    t.id = "toaster";
    t.className = "toaster";
    t.setAttribute("role", "status");
    t.setAttribute("aria-live", "polite");
    document.body.appendChild(t);
  }
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  if (asHTML) el.innerHTML = msg;
  else el.textContent = msg;
  el.style.cursor = "pointer";
  el.title = "Clic para cerrar";
  el.addEventListener("click", () => el.remove());
  t.appendChild(el);

  if (duration > 0) setTimeout(() => el.remove(), duration);
};

const withLoading = async (btn, fn) => {
  try {
    clearError();
    if (btn) {
      btn.disabled = true;
      btn.classList.add("disabled");
    }
    return await fn();
  } catch (e) {
    console.error(e);
    showError(e?.message || "Ha ocurrido un error inesperado");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.classList.remove("disabled");
    }
  }
};

// ====== API ======
const api = {
  // Consume: POST /upload_document/
  async upload(file) {
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch(`${API_BASE_URL}/upload_document/`, {
      method: "POST",
      body: fd,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json(); // { filename, category, ... }
  },

  // Consume: GET /list_documents/?category=&page=&page_size=
  async list({ category = "", page = 1, page_size = 10 } = {}) {
    const q = new URLSearchParams();
    if (category) q.set("category", category);
    q.set("page", page);
    q.set("page_size", page_size);
    const res = await fetch(`${API_BASE_URL}/list_documents/?${q.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json(); // {success, documents, total, ...}
  },

  // Consume: GET /search_documents/?query=&category=&page=&page_size=
  async search({ query, category = "", page = 1, page_size = 10 }) {
    const q = new URLSearchParams({ query, page, page_size });
    if (category) q.set("category", category);
    const res = await fetch(
      `${API_BASE_URL}/search_documents/?${q.toString()}`
    );
    if (!res.ok) throw new Error(await res.text());
    return res.json(); // {success, documents, total, ...}
  },

  // Consume: POST /load_demo/
  async loadDemo() {
    const res = await fetch(`${API_BASE_URL}/load_demo/`, { method: "POST" });
    if (!res.ok) throw new Error(await res.text());
    return res.json(); // { message?: string, ... }
  },
};

// ====== estado UI ======
let state = {
  rows: [],
  page: 1,
  pageSize: 10,
  total: 0,
  mode: "list", // "list" | "search"
  lastQuery: "",
  lastCategory: "",
};

// ====== render ======
function renderRows(items) {
  const tbody = $("#resultsTable tbody");
  const empty = $("#emptyState");
  const count = $("#countBadge");
  tbody.innerHTML = "";

  items.forEach((r) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${r.id ?? ""}</td><td>${
      r.title ?? ""
    }</td><td><span class="pill">${r.category ?? ""}</span></td>`;
    tbody.appendChild(tr);
  });

  // Estado vacío
  empty?.classList.toggle("hidden", items.length !== 0);
  if (count) count.textContent = state.total ?? items.length;
  renderPager();
}

function renderPager() {
  let pager = $("#pager");
  if (!pager) {
    pager = document.createElement("div");
    pager.id = "pager";
    pager.className = "row gap";
    const host = qs(".card.col-span-2");
    if (host) host.appendChild(pager);
  }
  const totalPages = Math.max(
    1,
    Math.ceil((state.total || 0) / state.pageSize)
  );
  pager.innerHTML = `
    <button id="prevPage" class="btn btn-ghost"${
      state.page <= 1 ? " disabled" : ""
    }>← Anterior</button>
    <span class="muted">Página ${state.page} / ${totalPages}</span>
    <button id="nextPage" class="btn btn-ghost"${
      state.page >= totalPages ? " disabled" : ""
    }>Siguiente →</button>
  `;
  qs("#prevPage", pager)?.addEventListener("click", () =>
    changePage(state.page - 1)
  );
  qs("#nextPage", pager)?.addEventListener("click", () =>
    changePage(state.page + 1)
  );
}

async function changePage(p) {
  state.page = Math.max(1, p);
  await refreshData();
}

// ====== acciones ======
async function refreshData() {
  try {
    clearError();

    if (state.mode === "search") {
      // Consume: GET /search_documents/
      const res = await api.search({
        query: state.lastQuery,
        category: state.lastCategory,
        page: state.page,
        page_size: state.pageSize,
      });
      const documents = res.documents || [];
      const total = res.total ?? documents.length;
      state.rows = documents;
      state.total = total;
    } else {
      const res = await api.list({
        category: state.lastCategory,
        page: state.page,
        page_size: state.pageSize,
      });
      const documents = res.documents || [];
      const total = res.total ?? documents.length;
      state.rows = documents;
      state.total = total;
    }
    renderRows(state.rows);
  } catch (e) {
    console.error(e);
    showError("Error obteniendo datos: " + (e?.message || "desconocido"));
  }
}

// Subida de archivo → POST /upload_document/
$("#uploadForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = $("#fileInput")?.files?.[0];
  if (!file) return showError("Selecciona un archivo");

  $("#uploadStatus").textContent = "Subiendo...";
  const btn = e.submitter;

  await withLoading(btn, async () => {
    try {
      const data = await api.upload(file); // {filename, category, ...}
      $("#uploadStatus").textContent = "Listo";
      // La categoría que pintamos aquí viene del backend
      $("#uploadResult").innerHTML = `<span class="pill">Detectado: ${
        data.category || "—"
      }</span>`;
      setTimeout(() => {
        $("#uploadResult").innerHTML = "";
      }, 5000);

      const name = data.filename || file.name;
      const cat = data.category || "—";
      toast(
        `Documento <strong>${name}</strong> clasificado como <span class="pill">${cat}</span>`,
        "ok",
        10000, // 10 segundos
        true // renderizar como HTML
      );
      await refreshData();
      $("#fileInput").value = "";
    } catch (err) {
      $("#uploadStatus").textContent = "Error";
      toast(err?.message || "Error subiendo el archivo", "err", 8000);
      throw err;
    }
  });
});

// Listado por categoría → GET /list_documents/
$("#listBtn")?.addEventListener("click", async () => {
  state.mode = "list";
  state.page = 1;
  state.lastCategory = $("#categorySelect")?.value || "";
  await withLoading($("#listBtn"), refreshData);
});

// Buscar → GET /search_documents/
$("#searchBtn")?.addEventListener("click", async () => {
  const q = ($("#searchInput")?.value || "").trim();
  if (!q) return showError("Escribe un término de búsqueda");
  state.mode = "search";
  state.page = 1;
  state.lastQuery = q;
  state.lastCategory = $("#categorySelect")?.value || "";
  await withLoading($("#searchBtn"), refreshData);
});

// Precargar dataset → POST /load_demo/
$("#loadDemoBtn")?.addEventListener("click", async () => {
  await withLoading($("#loadDemoBtn"), async () => {
    const r = await api.loadDemo();
    toast(r?.message || "Dataset demo cargado", "ok", 8000);
    await refreshData();
  });
});

// ====== init ======
(async function init() {
  // Estado inicial: lista sin filtro
  state.mode = "list";
  state.page = 1;
  state.pageSize = 10;
  state.lastCategory = "";
  await refreshData();
})();
