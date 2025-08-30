// ------- util -------
const $ = (s) => document.querySelector(s);
const toaster = $("#toaster");
const toast = (msg, type="ok") => {
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  toaster.appendChild(el);
  setTimeout(()=> el.remove(), 2600);
};

// ------- estado (mock local para la demo de UI) -------
let AUTOINC = 5;
const rows = [
  { id:1, title:"Contrato prestación servicios.pdf", category:"Contratos", text:"cláusulas, honorarios..." },
  { id:2, title:"Sentencia 123-2020.pdf", category:"Sentencias", text:"fundamentos y fallo..." },
  { id:3, title:"RGPD extracto.txt", category:"Normativas", text:"protección de datos..." },
  { id:4, title:"Licencia software X.docx", category:"Licencias", text:"condiciones de uso..." },
];

// ------- render -------
function renderRows(items){
  const tbody = $("#resultsTable tbody");
  tbody.innerHTML = "";
  $("#countBadge").textContent = items.length;
  $("#emptyState").classList.toggle("hidden", items.length !== 0);

  items.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${r.id}</td><td>${r.title}</td><td><span class="pill">${r.category}</span></td>`;
    tbody.appendChild(tr);
  });
}
renderRows(rows);

// ------- acciones UI (con mock) -------
function mockClassify(filename, text=""){
  const f = (filename + " " + text).toLowerCase();
  if (f.match(/contrat|cláusul|honorari/)) return "Contratos";
  if (f.match(/sentenc|juzgad|fallo/)) return "Sentencias";
  if (f.match(/normativ|rgpd|ley|reglament/)) return "Normativas";
  if (f.match(/licenci/)) return "Licencias";
  return "Otros";
}

$("#uploadForm").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const file = $("#fileInput").files[0];
  if(!file){ toast("Selecciona un archivo", "err"); return; }

  $("#uploadStatus").textContent = "Subiendo...";
  // Simulación de latencia
  setTimeout(() => {
    const cat = mockClassify(file.name);
    AUTOINC++;
    rows.unshift({ id: AUTOINC, title: file.name, category: cat, text:"" });
    renderRows(rows);
    $("#uploadResult").innerHTML = `<span class="pill">Detectado: ${cat}</span>`;
    $("#uploadStatus").textContent = "Listo";
    toast("Documento clasificado");
    $("#fileInput").value = "";
  }, 600);
});

$("#listBtn").addEventListener("click", ()=>{
  const cat = $("#categorySelect").value;
  const out = !cat ? rows : rows.filter(r => r.category === cat);
  renderRows(out);
});

$("#searchBtn").addEventListener("click", ()=>{
  const q = $("#searchInput").value.trim().toLowerCase();
  if(!q){ renderRows(rows); return; }
  const out = rows.filter(r => (r.title + " " + (r.text||"")).toLowerCase().includes(q));
  renderRows(out);
});

$("#loadDemoBtn").addEventListener("click", ()=>{
  // mock: simplemente añade algunos
  const demo = [
    {title:"Contrato obra y servicio.txt", category:"Contratos"},
    {title:"Sentencia Audiencia Provincial.pdf", category:"Sentencias"},
  ].map((d, i)=> ({ id: AUTOINC+i+1, ...d, text:"" }));
  AUTOINC += demo.length;
  rows.unshift(...demo);
  renderRows(rows);
  toast("Dataset demo cargado");
});
