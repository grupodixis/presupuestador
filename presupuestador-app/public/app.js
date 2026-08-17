const APP_BASE_PATH = (() => {
  const scriptSrc = document.currentScript?.getAttribute("src") || "";
  const scriptPath = new URL(scriptSrc || "app.js", window.location.href).pathname;
  const basePath = scriptPath.replace(/\/app\.js$/, "").replace(/\/$/, "");
  return basePath === "/" ? "" : basePath;
})();

function appUrl(path) {
  if (!path || !path.startsWith("/")) return path;
  return `${APP_BASE_PATH}${path}`;
}

const DEFAULT_PROVIDER = "gemini";
const DEFAULT_GEMINI_MODEL = "gemini-3.5-flash";
const ACTIVE_VIEW_KEY = "presupuestador.activeView";
const ACTIVE_BUDGET_FOLDER_KEY = "presupuestador.activeBudgetFolder";
const DEFAULT_VIEW = "budgetsView";
const VALID_VIEWS = new Set(["budgetView", "budgetsView", "configView", "contextView", "usersView"]);

const DEFAULT_DOCUMENT_TEMPLATE = {
  logo: "https://www.hamenorca.com/images/logo-hamenorca-dark.svg",
  headerText: [
    "HAM Estructuras Metalicas",
    "Fabricacion y montaje de estructuras metalicas, herreria y soluciones a medida en Menorca.",
    "Av. Circunvalacio, 11, Poligono de Sant Lluis, 07710 Sant Lluis, Menorca",
    "info@hamenorca.com - +34 971 35 20 18 - WhatsApp +34 669 769 541",
    "www.hamenorca.com",
  ].join("\n"),
  footerText: [
    "Validez: 30 dias desde la fecha de emision.",
    "Forma de pago: 100% a la aceptacion del presupuesto.",
  ].join("\n"),
};

const state = {
  attachments: [],
  result: null,
  mdFiles: [],
  activeMdPath: "",
  models: { fallback: [], openai: [], gemini: [] },
  settings: null,
  budgets: [],
  budgetYears: [],
  currentBudgetFolder: null,
  activeLineAiIndex: null,
  lineAiPrompts: {},
  budgetChangeLog: [],
  currentUser: null,
  users: [],
  prices: [],
  activePriceCategory: "",
  products: [],
};

const els = {
  menuToggle: document.querySelector("#menuToggle"),
  appMenu: document.querySelector("#appMenu"),
  provider: document.querySelector("#provider"),
  model: document.querySelector("#model"),
  modelTokenInfo: document.querySelector("#modelTokenInfo"),
  prompt: document.querySelector("#prompt"),
  productSelect: document.querySelector("#productSelect"),
  insertProductPrompt: document.querySelector("#insertProductPrompt"),
  productPromptStatus: document.querySelector("#productPromptStatus"),
  attachments: document.querySelector("#attachments"),
  fileList: document.querySelector("#fileList"),
  generate: document.querySelector("#generate"),
  clear: document.querySelector("#clear"),
  status: document.querySelector("#status"),
  resultPanel: document.querySelector("#resultPanel"),
  title: document.querySelector("#title"),
  summaryText: document.querySelector("#summaryText"),
  productType: document.querySelector("#productType"),
  total: document.querySelector("#total"),
  linesBody: document.querySelector("#linesBody"),
  questions: document.querySelector("#questions"),
  assumptions: document.querySelector("#assumptions"),
  risks: document.querySelector("#risks"),
  suggestionsList: document.querySelector("#suggestionsList"),
  printPreview: document.querySelector("#printPreview"),
  addLine: document.querySelector("#addLine"),
  exportBudget: document.querySelector("#exportBudget"),
  printBudget: document.querySelector("#printBudget"),
  summaryPdfBudget: document.querySelector("#summaryPdfBudget"),
  generateBudgetImage: document.querySelector("#generateBudgetImage"),
  refreshContext: document.querySelector("#refreshContext"),
  contextFiles: document.querySelector("#contextFiles"),
  defaultProvider: document.querySelector("#defaultProvider"),
  openaiKey: document.querySelector("#openaiKey"),
  openaiModel: document.querySelector("#openaiModel"),
  geminiKey: document.querySelector("#geminiKey"),
  falKey: document.querySelector("#falKey"),
  geminiModel: document.querySelector("#geminiModel"),
  openaiBudgets: document.querySelector("#openaiBudgets"),
  geminiBudgets: document.querySelector("#geminiBudgets"),
  refreshModels: document.querySelector("#refreshModels"),
  saveSettings: document.querySelector("#saveSettings"),
  settingsStatus: document.querySelector("#settingsStatus"),
  documentLogo: document.querySelector("#documentLogo"),
  documentHeaderText: document.querySelector("#documentHeaderText"),
  documentFooterText: document.querySelector("#documentFooterText"),
  documentTemplateAiPrompt: document.querySelector("#documentTemplateAiPrompt"),
  applyDocumentTemplateAi: document.querySelector("#applyDocumentTemplateAi"),
  documentTemplateStatus: document.querySelector("#documentTemplateStatus"),
  mdSearch: document.querySelector("#mdSearch"),
  knowledgeMap: document.querySelector("#knowledgeMap"),
  clearMdFilter: document.querySelector("#clearMdFilter"),
  mdFiles: document.querySelector("#mdFiles"),
  mdPath: document.querySelector("#mdPath"),
  mdEditor: document.querySelector("#mdEditor"),
  mdPreview: document.querySelector("#mdPreview"),
  mdEditMode: document.querySelector("#mdEditMode"),
  mdPreviewMode: document.querySelector("#mdPreviewMode"),
  mdAiPrompt: document.querySelector("#mdAiPrompt"),
  applyMdAi: document.querySelector("#applyMdAi"),
  saveMd: document.querySelector("#saveMd"),
  mdStatus: document.querySelector("#mdStatus"),
  newProductName: document.querySelector("#newProductName"),
  newProductArea: document.querySelector("#newProductArea"),
  newProductDescription: document.querySelector("#newProductDescription"),
  createProduct: document.querySelector("#createProduct"),
  productCreateStatus: document.querySelector("#productCreateStatus"),
  clientName: document.querySelector("#clientName"),
  clientEmail: document.querySelector("#clientEmail"),
  clientPhone: document.querySelector("#clientPhone"),
  clientTax: document.querySelector("#clientTax"),
  clientAddress: document.querySelector("#clientAddress"),
  clientRef: document.querySelector("#clientRef"),
  budgetYear: document.querySelector("#budgetYear"),
  budgetSearch: document.querySelector("#budgetSearch"),
  budgetsList: document.querySelector("#budgetsList"),
  budgetsStatus: document.querySelector("#budgetsStatus"),
  refreshBudgets: document.querySelector("#refreshBudgets"),
  newBudget: document.querySelector("#newBudget"),
  currentUser: document.querySelector("#currentUser"),
  logout: document.querySelector("#logout"),
  usersNav: document.querySelector("#usersNav"),
  usersBody: document.querySelector("#usersBody"),
  usersStatus: document.querySelector("#usersStatus"),
  newUsername: document.querySelector("#newUsername"),
  newUserPassword: document.querySelector("#newUserPassword"),
  newUserRole: document.querySelector("#newUserRole"),
  createUser: document.querySelector("#createUser"),
  pricesBody: document.querySelector("#pricesBody"),
  priceSearch: document.querySelector("#priceSearch"),
  refreshPrices: document.querySelector("#refreshPrices"),
  newPriceItem: document.querySelector("#newPriceItem"),
  priceStatus: document.querySelector("#priceStatus"),
};

function formatMoney(value) {
  return new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR" }).format(Number(value || 0));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function setStatus(text) {
  if (els.status) els.status.textContent = text || "";
}

function markdownInline(text) {
  let html = escapeHtml(text);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/__([^_]+)__/g, "<strong>$1</strong>");
  html = html.replace(/(^|\s)\*([^*]+)\*(?=\s|$)/g, "$1<em>$2</em>");
  html = html.replace(/(^|\s)_([^_]+)_(?=\s|$)/g, "$1<em>$2</em>");
  return html;
}

function renderMarkdownTable(lines) {
  const rows = lines.map((line) => line.trim().replace(/^\||\|$/g, "").split("|").map((cell) => markdownInline(cell.trim())));
  const header = rows[0] || [];
  const body = rows.slice(2);
  return `<table><thead><tr>${header.map((cell) => `<th>${cell}</th>`).join("")}</tr></thead><tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}

function renderMarkdown(content) {
  const lines = String(content || "").replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let listType = null;
  let inCode = false;
  let code = [];
  function closeList() {
    if (listType) out.push(`</${listType}>`);
    listType = null;
  }
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    const trimmed = line.trim();
    if (trimmed.startsWith("```")) {
      if (inCode) {
        out.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
        code = [];
        inCode = false;
      } else {
        closeList();
        inCode = true;
      }
      continue;
    }
    if (inCode) {
      code.push(line);
      continue;
    }
    if (!trimmed) {
      closeList();
      continue;
    }
    if (/^\|.+\|$/.test(trimmed) && i + 1 < lines.length && /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(lines[i + 1].trim())) {
      closeList();
      const tableLines = [line, lines[i + 1]];
      i += 2;
      while (i < lines.length && /^\|.+\|$/.test(lines[i].trim())) {
        tableLines.push(lines[i]);
        i += 1;
      }
      i -= 1;
      out.push(renderMarkdownTable(tableLines));
      continue;
    }
    const heading = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      closeList();
      const level = heading[1].length;
      out.push(`<h${level}>${markdownInline(heading[2])}</h${level}>`);
      continue;
    }
    if (/^---+$/.test(trimmed)) {
      closeList();
      out.push("<hr>");
      continue;
    }
    const unordered = trimmed.match(/^[-*]\s+(.*)$/);
    const ordered = trimmed.match(/^\d+\.\s+(.*)$/);
    if (unordered || ordered) {
      const desired = ordered ? "ol" : "ul";
      if (listType !== desired) {
        closeList();
        out.push(`<${desired}>`);
        listType = desired;
      }
      let item = unordered ? unordered[1] : ordered[1];
      item = item.replace(/^\[( |x|X)\]\s*/, (match, checked) => `${checked.trim() ? "☑" : "☐"} `);
      out.push(`<li>${markdownInline(item)}</li>`);
      continue;
    }
    closeList();
    out.push(`<p>${markdownInline(trimmed)}</p>`);
  }
  closeList();
  if (inCode) out.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
  return out.join("\n");
}

function setMdMode(mode) {
  const preview = mode === "preview";
  els.mdEditMode.classList.toggle("active", !preview);
  els.mdPreviewMode.classList.toggle("active", preview);
  els.mdEditor.classList.toggle("hidden", preview);
  els.mdPreview.classList.toggle("hidden", !preview);
  if (preview) els.mdPreview.innerHTML = renderMarkdown(els.mdEditor.value);
}

function normalizeDocumentTemplate(template = {}) {
  return {
    logo: String(template.logo || DEFAULT_DOCUMENT_TEMPLATE.logo),
    headerText: String(template.headerText || DEFAULT_DOCUMENT_TEMPLATE.headerText),
    footerText: String(template.footerText || DEFAULT_DOCUMENT_TEMPLATE.footerText),
  };
}

function selectedProduct() {
  const slug = els.productSelect?.value || "";
  return state.products.find((product) => product.slug === slug) || null;
}

function renderProductSelect() {
  if (!els.productSelect) return;
  const current = els.productSelect.value;
  els.productSelect.innerHTML = '<option value="">Selecciona producto para pre-prompt...</option>';
  for (const product of state.products) {
    const option = document.createElement("option");
    option.value = product.slug;
    option.textContent = product.name;
    els.productSelect.appendChild(option);
  }
  if (current && state.products.some((product) => product.slug === current)) els.productSelect.value = current;
}

async function loadProducts() {
  if (!els.productSelect) return;
  try {
    const data = await getJson("/api/products");
    state.products = data.products || [];
    renderProductSelect();
  } catch (error) {
    if (els.productPromptStatus) els.productPromptStatus.textContent = error.message;
  }
}

function insertSelectedProductPrompt() {
  const product = selectedProduct();
  if (!product) {
    els.productPromptStatus.textContent = "Selecciona un producto.";
    return;
  }
  const template = product.promptTemplate || `Producto: ${product.name}\n\nRellenar parametros:\n- dimensiones:\n- material:\n- acabado:\n- ubicacion:\n`;
  const current = els.prompt.value.trim();
  els.prompt.value = current ? `${current}\n\n---\n${template}` : template;
  els.productPromptStatus.textContent = `Pre-prompt insertado: ${product.name}.`;
  els.prompt.focus();
}

async function createProductFromForm() {
  const name = els.newProductName?.value.trim() || "";
  if (!name) {
    els.productCreateStatus.textContent = "Indica el nombre del producto.";
    return;
  }
  const selection = effectiveModelSelection();
  els.createProduct.disabled = true;
  els.productCreateStatus.textContent = "Creando archivos de producto...";
  try {
    const response = await api("/api/products", {
      provider: selection.provider,
      model: selection.model,
      name,
      area: els.newProductArea.value,
      description: els.newProductDescription.value,
    });
    state.products = response.products || [];
    state.mdFiles = response.files || state.mdFiles;
    renderProductSelect();
    renderKnowledgeMap();
    renderMdFiles();
    els.productSelect.value = response.slug || "";
    els.newProductName.value = "";
    els.newProductDescription.value = "";
    const filesText = (response.files || []).join(", ");
    els.productCreateStatus.textContent = response.warning ? `Producto creado en modo local: ${filesText}. Aviso IA: ${response.warning}` : `Producto creado: ${filesText}`;
    if (response.usage) {
      state.result = state.result || {};
      state.result.tokenUsage = response.usage;
      await loadModels(selection.provider, false);
      renderModelTokenInfo();
    }
  } catch (error) {
    try {
      const parsed = JSON.parse(error.message);
      els.productCreateStatus.textContent = parsed.error || error.message;
    } catch {
      els.productCreateStatus.textContent = error.message;
    }
  } finally {
    els.createProduct.disabled = false;
  }
}

const KNOWLEDGE_AREAS = [
  {
    key: "aluminio",
    title: "Aluminio",
    status: "Activa",
    home: "skills/areas/aluminio/README.md",
    learning: "skills/aprendizaje/aprendizaje_aluminio.md",
    sectors: ["ventanas", "puertas", "cerramientos", "mallorquinas", "persianas", "vidrio"],
    missing: "series, herrajes, vidrios y rangos por m2",
    patterns: ["aluminio", "ventana_aluminio", "cerramiento_aluminio", "mallorquina", "pergolas-extrual"],
  },
  {
    key: "carpinteria_metalica",
    title: "Carpinteria metalica",
    status: "Activa",
    home: "skills/areas/carpinteria_metalica/README.md",
    learning: "skills/aprendizaje/aprendizaje_carpinteria_metalica.md",
    sectors: ["barandillas", "rejas", "puertas", "cancelas", "escaleras", "estructuras", "herreria"],
    missing: "variantes, anclajes, calculos y tratamientos por exposicion",
    patterns: ["barandilla", "rejas", "puerta_metalica", "porton", "cancela", "escalera", "estructura_metalica", "herreria", "marquesina", "pergola", "metalica", "metalicas"],
  },
  {
    key: "instalaciones_electricas",
    title: "Instalaciones electricas",
    status: "Preparada",
    home: "skills/areas/instalaciones_electricas/README.md",
    learning: "skills/aprendizaje/aprendizaje_instalaciones_electricas.md",
    sectors: ["vivienda", "local", "nave", "cuadros", "iluminacion", "fotovoltaica"],
    missing: "puntos tipo, boletines, cuadros y legalizacion",
    patterns: ["instalacion_electrica", "electric", "fotovoltaic"],
  },
  {
    key: "fontaneria",
    title: "Fontaneria",
    status: "Preparada",
    home: "skills/areas/fontaneria/README.md",
    learning: "skills/aprendizaje/aprendizaje_fontaneria.md",
    sectors: ["banos", "cocinas", "saneamiento", "ACS", "bombeo"],
    missing: "puntos, pruebas, reposiciones y equipos",
    patterns: ["instalacion_fontaneria", "fontaneria", "saneamiento", "acs"],
  },
  {
    key: "clima",
    title: "Clima",
    status: "Preparada",
    home: "skills/areas/clima/README.md",
    learning: "skills/aprendizaje/aprendizaje_clima.md",
    sectors: ["split", "multisplit", "conductos", "ventilacion", "aerotermia"],
    missing: "potencias, distancias, soportes y puesta en marcha",
    patterns: ["instalacion_clima", "clima", "climatizacion", "ventilacion", "aeroterm"],
  },
  {
    key: "otras_industrias",
    title: "Otras industrias",
    status: "Incubadora",
    home: "skills/areas/otras_industrias/README.md",
    learning: "skills/aprendizaje/aprendizaje_otras_industrias.md",
    sectors: ["pilotos", "nuevos productos", "servicios", "mantenimiento"],
    missing: "primeros ejemplos, proveedores y composiciones repetibles",
    patterns: ["otras_industrias", "producto_compuesto"],
  },
];

function areaFiles(area) {
  const direct = new Set([area.home, area.learning]);
  return state.mdFiles.filter((file) => {
    const lower = file.toLowerCase();
    return direct.has(file) || area.patterns.some((pattern) => lower.includes(pattern));
  });
}

function renderKnowledgeMap() {
  if (!els.knowledgeMap) return;
  const totalLearning = state.mdFiles.filter((file) => file.startsWith("skills/aprendizaje/")).length;
  const totalAreas = state.mdFiles.filter((file) => file.startsWith("skills/areas/")).length;
  els.knowledgeMap.innerHTML = `
    <div class="knowledge-map-head">
      <div>
        <h2>Mapa vivo de conocimiento</h2>
        <p>${totalAreas} mapas de area · ${totalLearning} memorias de aprendizaje · ${state.mdFiles.length} archivos editables</p>
      </div>
      <button class="secondary" data-open-md="skills/00_mapa_conocimiento.md">Mapa general</button>
    </div>
    <div class="knowledge-grid">
      ${KNOWLEDGE_AREAS.map((area) => {
        const files = areaFiles(area);
        const hasHome = state.mdFiles.includes(area.home);
        const hasLearning = state.mdFiles.includes(area.learning);
        return `
          <article class="knowledge-card" data-area="${area.key}">
            <div class="knowledge-card-top">
              <strong>${escapeHtml(area.title)}</strong>
              <span class="knowledge-status">${escapeHtml(area.status)}</span>
            </div>
            <div class="knowledge-metrics">
              <span>${files.length} archivos</span>
              <span>${hasLearning ? "aprendizaje listo" : "sin aprendizaje"}</span>
            </div>
            <div class="sector-list">${area.sectors.map((sector) => `<span>${escapeHtml(sector)}</span>`).join("")}</div>
            <p>${escapeHtml(area.missing)}</p>
            <div class="knowledge-actions">
              <button class="secondary" data-open-md="${escapeHtml(area.home)}" ${hasHome ? "" : "disabled"}>Mapa</button>
              <button class="secondary" data-open-md="${escapeHtml(area.learning)}" ${hasLearning ? "" : "disabled"}>Aprendizaje</button>
              <button class="secondary" data-filter-area="${escapeHtml(area.key)}">Ver archivos</button>
            </div>
          </article>`;
      }).join("")}
    </div>
  `;
  els.knowledgeMap.querySelectorAll("[data-open-md]").forEach((button) => {
    button.addEventListener("click", () => openMd(button.dataset.openMd));
  });
  els.knowledgeMap.querySelectorAll("[data-filter-area]").forEach((button) => {
    button.addEventListener("click", () => {
      const area = KNOWLEDGE_AREAS.find((item) => item.key === button.dataset.filterArea);
      if (!area) return;
      els.mdSearch.value = "";
      renderMdFiles(areaFiles(area));
    });
  });
}
function templateFromSettingsFields() {
  return normalizeDocumentTemplate({
    logo: els.documentLogo?.value,
    headerText: els.documentHeaderText?.value,
    footerText: els.documentFooterText?.value,
  });
}

function currentDocumentTemplate() {
  return normalizeDocumentTemplate(state.result?.documentTemplate || state.settings?.documentTemplate || templateFromSettingsFields());
}

function renderDocumentHeaderText(headerText) {
  const lines = String(headerText || DEFAULT_DOCUMENT_TEMPLATE.headerText).split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const title = lines[0] || "HAM Estructuras Metalicas";
  const details = lines.slice(1);
  return "<h1>" + escapeHtml(title) + "</h1>" + details.map((line) => "<p>" + escapeHtml(line) + "</p>").join("");
}

function renderDocumentFooterText(footerText) {
  const lines = String(footerText || DEFAULT_DOCUMENT_TEMPLATE.footerText).split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const effective = lines.length ? lines : DEFAULT_DOCUMENT_TEMPLATE.footerText.split("\n");
  return effective.map((line) => "<div>" + escapeHtml(line) + "</div>").join("");
}

function conceptImageSrc(payload) {
  const image = payload?.imagenConceptual || payload?.imagenPrincipal || "";
  if (!image) return "";
  if (/^https?:\/\//i.test(image) || image.startsWith("data:")) return image;
  const folder = String(payload?._folder || state.currentBudgetFolder || "").replaceAll("\\", "/");
  if (!folder) return image;
  return appUrl(`/${folder}/${image}`.replace(/\/+/g, "/"));
}

function conceptImageFigure(payload, className = "print-concept-image") {
  const src = conceptImageSrc(payload);
  if (!src) return "";
  const note = payload.imagenConceptualNota || "Imagen orientativa generada por IA. El diseno final dependera de medidas, materiales, acabados y validacion tecnica.";
  return `<figure class="${className}"><img src="${escapeHtml(src)}" alt="Imagen conceptual del presupuesto"><figcaption>${escapeHtml(note)}</figcaption></figure>`;
}
function syncBudgetHeaderFromInputs() {
  if (!state.result) return;
  state.result.tipoProducto = els.productType.value.trim();
  state.result.titulo = els.title.value.trim() || "Presupuesto";
  state.result.resumen = els.summaryText.value.trim();
  state.result.documentTemplate = currentDocumentTemplate();
}


async function api(path, payload, method = "POST") {
  const response = await fetch(appUrl(path), {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (response.status === 401) { window.location.href = appUrl("/login.html"); throw new Error("No autenticado."); }
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

async function getJson(path) {
  const response = await fetch(appUrl(path));
  if (response.status === 401) { window.location.href = appUrl("/login.html"); throw new Error("No autenticado."); }
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function clientData() {
  return {
    nombre: els.clientName.value.trim(),
    email: els.clientEmail.value.trim(),
    telefono: els.clientPhone.value.trim(),
    nif: els.clientTax.value.trim(),
    direccion: els.clientAddress.value.trim(),
    referencia: els.clientRef.value.trim(),
  };
}

function resultPayload() {
  syncBudgetHeaderFromInputs();
  const payload = { ...(state.result || {}), cliente: clientData(), documentTemplate: currentDocumentTemplate() };
  if (state.currentBudgetFolder) payload._folder = state.currentBudgetFolder;
  if (state.budgetChangeLog.length) payload._changeLog = state.budgetChangeLog.slice(-120);
  return payload;
}

function recordBudgetChange(change) {
  state.budgetChangeLog.push({
    at: new Date().toISOString(),
    ...change,
  });
  state.budgetChangeLog = state.budgetChangeLog.slice(-200);
}

function lineLearningSnapshot(line) {
  return {
    id: line?.id || "",
    capitulo: line?.capitulo || "",
    concepto: line?.concepto || "",
    cantidad: line?.cantidad ?? 0,
    unidad: line?.unidad || "",
    precioUnitario: line?.precioUnitario ?? 0,
    importe: line?.importe ?? 0,
  };
}

function readFileAsData(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(reader.error);
    reader.onload = () => {
      const result = String(reader.result || "");
      if (file.type.startsWith("image/")) {
        resolve({ kind: "image", name: file.name, type: file.type, dataUrl: result, base64: result.split(",")[1] || "" });
      } else {
        resolve({ kind: "document", name: file.name, type: file.type, text: result });
      }
    };
    if (file.type.startsWith("image/")) reader.readAsDataURL(file);
    else reader.readAsText(file);
  });
}

async function handleFiles(files) {
  const parsed = [];
  for (const file of files) parsed.push(await readFileAsData(file));
  state.attachments = parsed;
  renderFiles();
}

function renderFiles() {
  els.fileList.innerHTML = "";
  for (const file of state.attachments) {
    const chip = document.createElement("span");
    chip.className = "file-chip";
    chip.textContent = `${file.kind === "image" ? "Imagen" : "Doc"}: ${file.name}`;
    els.fileList.appendChild(chip);
  }
}

function parseEditableNumber(value) {
  const normalized = String(value ?? "").trim().replace(/\s/g, "").replace(",", ".");
  if (!normalized) return 0;
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : 0;
}

function recalcLine(line) {
  line.cantidad = parseEditableNumber(line.cantidad);
  line.precioUnitario = parseEditableNumber(line.precioUnitario);
  line.importe = Math.round(line.cantidad * line.precioUnitario * 100) / 100;
}

function refreshResultTotals() {
  if (!state.result) return;
  const total = (state.result.lineas || []).reduce((sum, line) => {
    recalcLine(line);
    return sum + line.importe;
  }, 0);
  els.total.textContent = formatMoney(total);
  renderPrintPreview();
}

function renderList(el, items) {
  el.innerHTML = "";
  for (const item of items || []) {
    const li = document.createElement("li");
    li.textContent = item;
    el.appendChild(li);
  }
}

function toggleLineAi(index) {
  state.activeLineAiIndex = state.activeLineAiIndex === index ? null : index;
  renderLines();
}

function deleteLine(index) {
  if (!state.result?.lineas) return;
  const removed = state.result.lineas[index];
  state.result.lineas.splice(index, 1);
  recordBudgetChange({ source: "manual", action: "delete-line", lineIndex: index, before: lineLearningSnapshot(removed) });
  state.activeLineAiIndex = null;
  state.lineAiPrompts = {};
  renderResult();
}

async function applyLineAi(index, row) {
  const prompt = row.querySelector(".line-ai-prompt")?.value.trim() || "";
  const status = row.querySelector(".line-ai-status");
  if (!prompt) {
    status.textContent = "Escribe un prompt para esta linea.";
    return;
  }
  const selection = effectiveModelSelection();
  if (!selection.selected) {
    status.textContent = "Selecciona un modelo disponible.";
    return;
  }
  const button = row.querySelector(".apply-line-ai");
  button.disabled = true;
  status.textContent = "Aplicando IA sobre el presupuesto actual...";
  try {
    const beforeLine = lineLearningSnapshot(state.result?.lineas?.[index]);
    const response = await api("/api/line-ai", {
      provider: selection.provider,
      model: selection.model,
      prompt,
      lineIndex: index,
      budget: resultPayload(),
    });
    const afterLine = lineLearningSnapshot(response.result?.lineas?.[index]);
    recordBudgetChange({ source: "ia-linea", action: "edit-line", prompt, lineIndex: index, before: beforeLine, after: afterLine });
    state.result = response.result;
    state.result.tokenUsage = response.usage || state.result.tokenUsage || null;
    state.result.tokenStatus = response.tokenStatus || state.result.tokenStatus || null;
    state.activeLineAiIndex = null;
    state.lineAiPrompts = {};
    renderResult();
    await loadModels(selection.provider, false);
    renderModelTokenInfo();
    const usageText = response.usage ? ` Tokens: ${response.usage.inputTokens || 0} entrada / ${response.usage.outputTokens || 0} salida / ${response.usage.totalTokens || 0} total.` : "";
    setStatus(response.warning ? `Edicion local por linea: ${response.warning}` : `Linea actualizada con ${response.provider}.${usageText}`);
  } catch (error) {
    try {
      const parsed = JSON.parse(error.message);
      status.textContent = parsed.error || error.message;
    } catch {
      status.textContent = error.message;
    }
  } finally {
    button.disabled = false;
  }
}
function renderLines() {
  els.linesBody.innerHTML = "";
  const lines = state.result?.lineas || [];
  lines.forEach((line, index) => {
    recalcLine(line);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><input data-field="capitulo" value="${escapeHtml(line.capitulo || "")}"></td>
      <td>
        <input data-field="concepto" value="${escapeHtml(line.concepto || "")}">
        <textarea data-field="descripcion">${escapeHtml(line.descripcion || "")}</textarea>
      </td>
      <td><input data-field="cantidad" data-number="true" inputmode="decimal" value="${line.cantidad}"></td>
      <td><input data-field="unidad" value="${escapeHtml(line.unidad || "")}"></td>
      <td><input data-field="precioUnitario" data-number="true" inputmode="decimal" value="${line.precioUnitario}"></td>
      <td><strong data-line-amount>${formatMoney(line.importe)}</strong><br><small>${escapeHtml(line.confianza || "")}</small></td>
      <td>
        <div class="line-tools">
          <button class="line-ai-toggle" title="Editar esta linea con IA">IA</button>
          <button class="row-delete" title="Eliminar linea">x</button>
        </div>
      </td>
    `;
    const syncLineField = (input, record = false) => {
      const field = input.dataset.field;
      const before = line[field];
      line[field] = input.dataset.number === "true" ? parseEditableNumber(input.value) : input.value;
      recalcLine(line);
      if (record && String(before ?? "") !== String(line[field] ?? "")) {
        recordBudgetChange({
          source: "manual",
          action: "edit-field",
          lineIndex: index,
          field,
          from: before,
          to: line[field],
          line: lineLearningSnapshot(line),
        });
      }
      const amount = tr.querySelector("[data-line-amount]");
      if (amount) amount.textContent = formatMoney(line.importe);
      refreshResultTotals();
    };
    tr.querySelectorAll("[data-field]").forEach((input) => {
      input.addEventListener("input", () => syncLineField(input, false));
      input.addEventListener("change", () => syncLineField(input, true));
      input.addEventListener("blur", () => {
        syncLineField(input, true);
        if (input.dataset.number === "true") input.value = input.dataset.field === "cantidad" ? line.cantidad : line.precioUnitario;
      });
    });
    tr.querySelector(".row-delete").addEventListener("click", () => deleteLine(index));
    tr.querySelector(".line-ai-toggle").addEventListener("click", () => toggleLineAi(index));
    els.linesBody.appendChild(tr);

    if (state.activeLineAiIndex === index) {
      const aiTr = document.createElement("tr");
      aiTr.className = "line-ai-row";
      aiTr.innerHTML = `
        <td colspan="7">
          <div class="line-ai-panel">
            <div>
              <strong>IA sobre linea ${escapeHtml(line.id || String(index + 1))}</strong>
              <p>El agente recibira esta linea y el presupuesto completo actual.</p>
            </div>
            <textarea class="line-ai-prompt" rows="3" placeholder="Ej.: recalcula esta partida con inox 316, separa mano de obra y material, baja margen, cambia unidad a ml...">${escapeHtml(state.lineAiPrompts[index] || "")}</textarea>
            <div class="line-ai-actions">
              <button class="apply-line-ai">Aplicar IA</button>
              <button class="secondary delete-line-ai">Borrar linea</button>
              <button class="ghost close-line-ai">Cerrar</button>
              <span class="line-ai-status status"></span>
            </div>
          </div>
        </td>
      `;
      const promptInput = aiTr.querySelector(".line-ai-prompt");
      promptInput.addEventListener("input", () => {
        state.lineAiPrompts[index] = promptInput.value;
      });
      aiTr.querySelector(".apply-line-ai").addEventListener("click", () => applyLineAi(index, aiTr));
      aiTr.querySelector(".delete-line-ai").addEventListener("click", () => deleteLine(index));
      aiTr.querySelector(".close-line-ai").addEventListener("click", () => {
        state.activeLineAiIndex = null;
        renderLines();
      });
      els.linesBody.appendChild(aiTr);
    }
  });
}
function renderSuggestions() {
  els.suggestionsList.innerHTML = "";
  for (const suggestion of state.result?.sugerencias || []) {
    const card = document.createElement("article");
    card.className = "suggestion";
    card.innerHTML = `
      <div>
        <strong>${escapeHtml(suggestion.titulo || "Sugerencia")}</strong>
        <p>${escapeHtml(suggestion.detalle || "")}</p>
        <small>${escapeHtml(suggestion.skillDestino || "skills/aprendizaje/aprendizaje_general.md")}</small>
      </div>
      <button class="secondary">Memorizar</button>
    `;
    card.querySelector("button").addEventListener("click", async () => {
      card.querySelector("button").disabled = true;
      const response = await api("/api/learn", { suggestion });
      card.querySelector("button").textContent = `Guardado en ${response.file}`;
      await loadContext();
      await loadMdFiles();
loadBudgets();
    });
    els.suggestionsList.appendChild(card);
  }
}

function renderPrintPreview() {
  if (!state.result) return;
  const payload = resultPayload();
  const lines = payload.lineas || [];
  const total = lines.reduce((sum, line) => sum + Number(line.importe || 0), 0);
  const client = payload.cliente || {};
  const documentTemplate = currentDocumentTemplate();
  els.printPreview.innerHTML = `
    <header>
      <section class="print-company">
        <div class="print-logo"><img src="${escapeHtml(documentTemplate.logo)}" alt="HAM"></div>
        <div>${renderDocumentHeaderText(documentTemplate.headerText)}</div>
      </section>
      <section class="print-meta">
        <h2>Presupuesto</h2>
        <p>Fecha: ${new Date().toISOString().slice(0, 10)}</p>
      </section>
    </header>
    <section class="print-hero">
      <h2>${escapeHtml(payload.titulo || "Presupuesto")}</h2>
      <p>${escapeHtml(payload.resumen || "")}</p>
    </section>
    ${conceptImageFigure(payload)}
    <section class="print-box">
      <strong>Cliente:</strong> ${escapeHtml(client.nombre || "")}<br>
      <strong>Email:</strong> ${escapeHtml(client.email || "")} | <strong>Tel.:</strong> ${escapeHtml(client.telefono || "")}<br>
      <strong>Obra:</strong> ${escapeHtml(client.direccion || "")}<br>
      <strong>NIF/CIF:</strong> ${escapeHtml(client.nif || "")} | <strong>Referencia:</strong> ${escapeHtml(client.referencia || "")}
    </section>
    <table class="print-table">
      <colgroup>
        <col class="print-col-chapter">
        <col class="print-col-concept">
        <col class="print-col-qty">
        <col class="print-col-unit">
        <col class="print-col-price">
        <col class="print-col-amount">
      </colgroup>
      <thead><tr><th>Capitulo</th><th>Concepto</th><th>Cant.</th><th>Ud.</th><th>EUR/Ud.</th><th>Importe</th></tr></thead>
      <tbody>${lines.map((line) => `<tr><td>${escapeHtml(line.capitulo || "")}</td><td><strong>${escapeHtml(line.concepto || "")}</strong><br>${escapeHtml(line.descripcion || "")}</td><td class="num">${Number(line.cantidad || 0).toFixed(2)}</td><td>${escapeHtml(line.unidad || "")}</td><td class="num">${Number(line.precioUnitario || 0).toFixed(2)}</td><td class="num">${Number(line.importe || 0).toFixed(2)}</td></tr>`).join("")}</tbody>
    </table>
    <div class="print-total">Total estimado: ${total.toFixed(2)} EUR + IVA</div>
    <section class="print-conditions">${renderDocumentFooterText(documentTemplate.footerText)}</section>
  `;
}

function printDocumentHtml() {
  renderPrintPreview();
  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>${escapeHtml(state.result?.titulo || "Presupuesto")}</title>
  <style>
    @page { size: A4 portrait; margin: 10mm; }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: white; color: #111827; font-family: Arial, Helvetica, sans-serif; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .print-sheet { width: 170mm; max-width: 170mm; margin: 0 auto; overflow: hidden; }
    header { border-top: 5px solid #16202a; padding-top: 5mm; display: grid; grid-template-columns: minmax(0, 1fr) 42mm; gap: 5mm; align-items: start; border-bottom: 1px solid #d6dde5; padding-bottom: 4mm; }
    .print-company { display: flex; gap: 4mm; min-width: 0; }
    .print-logo { width: 30mm; flex: 0 0 30mm; }
    .print-logo img { width: 100%; filter: brightness(0) saturate(100%); }
    h1 { margin: 0 0 1mm; font-size: 12pt; line-height: 1.12; overflow-wrap: anywhere; }
    h2 { margin: 0; }
    p { margin: 0; color: #475467; font-size: 7.8pt; line-height: 1.2; overflow-wrap: anywhere; }
    .print-meta { color: #475467; text-align: right; white-space: normal; font-size: 8pt; }
    .print-meta h2 { color: #16202a; font-size: 11.5pt; text-transform: uppercase; letter-spacing: 0; margin-bottom: 2mm; }
    .print-ref { display: inline-block; padding: 1.6mm 2.2mm; border: 1px solid #d6dde5; background: #f6f8fa; color: #16202a; font-weight: 700; margin-bottom: 1.6mm; }
    .print-hero { margin: 5mm 0; padding: 3mm 4mm; border-left: 3px solid #16202a; background: #f6f8fa; }
    .print-hero h2 { margin: 0 0 1.5mm; font-size: 15pt; line-height: 1.12; color: #16202a; }
    .print-concept-image { margin: 0 0 4mm; page-break-inside: avoid; }
    .print-concept-image img { width: 100%; max-height: 52mm; object-fit: cover; border: 1px solid #d6dde5; border-radius: 3px; display: block; }
    .print-concept-image figcaption { margin-top: 1.5mm; color: #667085; font-size: 7pt; }
    .print-box { border: 1px solid #d6dde5; background: #f6f8fa; padding: 3.3mm; margin: 5mm 0 4mm; font-size: 8.8pt; line-height: 1.2; overflow-wrap: anywhere; }
    table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 7.6pt; line-height: 1.18; }
    th { background: #16202a; color: white; text-align: left; }
    th, td { border-bottom: 1px solid #d6dde5; padding: 2.2mm 1.5mm; vertical-align: top; overflow-wrap: anywhere; }
    .num { text-align: right; white-space: nowrap; }
    .print-col-chapter { width: 10%; }
    .print-col-concept { width: 51%; }
    .print-col-qty { width: 8%; }
    .print-col-unit { width: 7%; }
    .print-col-price { width: 11%; }
    .print-col-amount { width: 13%; }
    .print-total { width: 100%; margin-top: 7mm; padding-right: 2mm; text-align: right; font-size: 12pt; font-weight: 700; overflow-wrap: anywhere; page-break-inside: avoid; }
    .print-conditions { margin-top: 5mm; border-top: 1px solid #d6dde5; padding-top: 3mm; display: grid; gap: 1.8mm; color: #475467; font-size: 8pt; }
    tr { page-break-inside: avoid; page-break-after: auto; }
  </style>
</head>
<body><main class="print-sheet">${els.printPreview.innerHTML}</main></body>
</html>`;
}
window.printDocumentHtml = printDocumentHtml;

function renderResult(renderTable = true) {
  if (!state.result) return;
  const total = (state.result.lineas || []).reduce((sum, line) => {
    recalcLine(line);
    return sum + line.importe;
  }, 0);
  els.resultPanel.classList.remove("hidden");
  els.exportBudget.disabled = false;
  els.printBudget.disabled = false;
  if (els.summaryPdfBudget) els.summaryPdfBudget.disabled = false;
  if (els.generateBudgetImage) els.generateBudgetImage.disabled = false;
  if (!state.result.documentTemplate) state.result.documentTemplate = currentDocumentTemplate();
  els.title.value = state.result.titulo || "Presupuesto";
  els.summaryText.value = state.result.resumen || "";
  els.productType.value = state.result.tipoProducto || "producto_compuesto";
  els.total.textContent = formatMoney(total);
  if (renderTable) renderLines();
  renderList(els.questions, state.result.preguntas);
  renderList(els.assumptions, state.result.supuestos);
  renderList(els.risks, state.result.riesgos);
  renderSuggestions();
  renderPrintPreview();
}

function rememberActiveBudgetFolder(folder) {
  state.currentBudgetFolder = folder || null;
  if (state.currentBudgetFolder) localStorage.setItem(ACTIVE_BUDGET_FOLDER_KEY, state.currentBudgetFolder);
  else localStorage.removeItem(ACTIVE_BUDGET_FOLDER_KEY);
}

function clearBudgetForm() {
  state.attachments = [];
  state.result = null;
  rememberActiveBudgetFolder(null);
  els.prompt.value = "";
  els.attachments.value = "";
  els.fileList.innerHTML = "";
  els.clientName.value = "";
  els.clientEmail.value = "";
  els.clientPhone.value = "";
  els.clientTax.value = "";
  els.clientAddress.value = "";
  els.clientRef.value = "";
  els.resultPanel.classList.add("hidden");
  els.exportBudget.disabled = true;
  els.printBudget.disabled = true;
  if (els.summaryPdfBudget) els.summaryPdfBudget.disabled = true;
  if (els.generateBudgetImage) els.generateBudgetImage.disabled = true;
  setStatus("");
  updateSaveMode();
}

async function loadBudgets() {
  if (!els.budgetsList) return;
  els.budgetsStatus.textContent = "Cargando presupuestos...";
  const data = await getJson("/api/budgets");
  state.budgets = data.budgets || [];
  state.budgetYears = data.years || [];
  renderBudgetYears();
  renderBudgets();
  els.budgetsStatus.textContent = `${state.budgets.length} presupuesto(s).`;
}

function renderBudgetYears() {
  const current = els.budgetYear.value;
  els.budgetYear.innerHTML = "";
  const all = document.createElement("option");
  all.value = "all";
  all.textContent = "Todos";
  els.budgetYear.appendChild(all);
  for (const year of state.budgetYears) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    els.budgetYear.appendChild(option);
  }
  els.budgetYear.value = current && [...els.budgetYear.options].some((option) => option.value === current) ? current : (state.budgetYears[0] || "all");
}

function renderBudgets() {
  const year = els.budgetYear.value || "all";
  const query = (els.budgetSearch?.value || "").trim().toLowerCase();
  const budgets = state.budgets.filter((budget) => {
    const yearMatch = year === "all" || budget.year === year;
    const queryMatch = !query || [budget.code, budget.title, budget.clientName, budget.folder]
      .join(" ")
      .toLowerCase()
      .includes(query);
    return yearMatch && queryMatch;
  });
  els.budgetsList.innerHTML = "";
  if (!budgets.length) {
    els.budgetsList.innerHTML = '<div class="empty-state">No hay presupuestos para este a&ntilde;o.</div>';
    return;
  }
  for (const budget of budgets) {
    const card = document.createElement("article");
    card.className = "budget-card";
    const primary = budget.files.find((file) => file.name === "presupuesto-final.html")
      || budget.files.find((file) => file.name === "presupuesto-cliente.html")
      || budget.files.find((file) => file.name === "README.md")
      || budget.files[0];
    card.innerHTML = `
      <div class="budget-card-main">
        ${budget.imageUrl ? `<img class="budget-thumb" src="${appUrl(budget.imageUrl)}" alt="Imagen conceptual de ${escapeHtml(budget.title || budget.folder)}">` : `<div class="budget-thumb budget-thumb-empty">IA</div>`}
        <div>
          <div class="budget-code">${escapeHtml(budget.code)} &middot; ${escapeHtml(budget.year)}</div>
          <h2>${escapeHtml(budget.title || budget.folder)}</h2>
          <p>${escapeHtml(budget.clientName || "Sin cliente guardado")}</p>
          <div class="budget-meta">
            <span>${budget.total ? formatMoney(budget.total) : "Sin total"}</span>
            <span>${budget.updatedAt ? new Date(budget.updatedAt).toLocaleDateString("es-ES") : "Sin fecha"}</span>
          </div>
          <small>${escapeHtml(budget.folder)}</small>
        </div>
      </div>
      <div class="budget-card-actions">
        ${budget.editable ? `<button class="secondary edit-budget" data-folder="${escapeHtml(budget.folder)}">Editar</button>` : ""}
        <button class="secondary image-budget" data-folder="${escapeHtml(budget.folder)}">Imagen IA</button>
        ${primary ? `<a class="button-link" href="${appUrl(primary.url)}" target="_blank" rel="noreferrer">Abrir</a>` : ""}
        <div class="budget-file-links">${budget.files.map((file) => `<a href="${appUrl(file.url)}" target="_blank" rel="noreferrer">${escapeHtml(file.name)}</a>`).join("")}</div>
      </div>
    `;
    const editButton = card.querySelector(".edit-budget");
    if (editButton) editButton.addEventListener("click", () => editBudget(budget.folder));
    const imageButton = card.querySelector(".image-budget");
    if (imageButton) imageButton.addEventListener("click", () => generateBudgetImageForFolder(budget.folder, imageButton));
    els.budgetsList.appendChild(card);
  }
}

async function ensureCurrentBudgetSaved() {
  if (!state.result) throw new Error("No hay presupuesto activo.");
  if (state.currentBudgetFolder) return state.currentBudgetFolder;
  const response = await api("/api/export", resultPayload());
  rememberActiveBudgetFolder(response.folder);
  updateSaveMode();
  if (response.learningFile) state.budgetChangeLog = [];
  return response.folder;
}

async function generateBudgetImageForCurrent() {
  if (!state.result || !els.generateBudgetImage) return;
  els.generateBudgetImage.disabled = true;
  const selection = effectiveModelSelection();
  setStatus("Generando imagen conceptual con IA...");
  try {
    const folder = await ensureCurrentBudgetSaved();
    const response = await api("/api/budget-image", { folder, payload: resultPayload() });
    rememberActiveBudgetFolder(response.folder);
    state.result = response.payload;
    state.result.tokenStatus = response.tokenStatus || null;
    renderResult(false);
    await loadBudgets();
    await loadModels(selection.provider, false);
    renderModelTokenInfo();
    const usageText = response.usage ? ` Tokens imagen: ${response.usage.inputTokens || 0} entrada / ${response.usage.outputTokens || 0} salida / ${response.usage.totalTokens || 0} total.` : "";
    setStatus(`Imagen generada y guardada en ${response.image}.${usageText}`);
  } catch (error) {
    setStatus(error.message);
  } finally {
    els.generateBudgetImage.disabled = !state.result;
  }
}

async function generateBudgetImageForFolder(folder, button) {
  if (!folder) return;
  if (button) button.disabled = true;
  els.budgetsStatus.textContent = "Generando imagen conceptual...";
  try {
    const response = await api("/api/budget-image", { folder });
    await loadBudgets();
    if (state.currentBudgetFolder === response.folder) {
      state.result = response.payload;
      renderResult(false);
    }
    els.budgetsStatus.textContent = `Imagen generada en ${response.image}.`;
  } catch (error) {
    els.budgetsStatus.textContent = error.message;
  } finally {
    if (button) button.disabled = false;
  }
}
function newBudget() {
  clearBudgetForm();
  if (els.productSelect) els.productSelect.value = "";
  if (els.productPromptStatus) els.productPromptStatus.textContent = "";
  switchView("budgetView");
  els.prompt.focus();
}
function updateSaveMode() {
  els.exportBudget.textContent = state.currentBudgetFolder ? "Actualizar presupuesto" : "Guardar presupuesto";
}

function fillClientForm(cliente = {}) {
  els.clientName.value = cliente.nombre || "";
  els.clientEmail.value = cliente.email || "";
  els.clientPhone.value = cliente.telefono || "";
  els.clientTax.value = cliente.nif || "";
  els.clientAddress.value = cliente.direccion || "";
  els.clientRef.value = cliente.referencia || "";
}

async function editBudget(folder, options = {}) {
  if (!options.restored) els.budgetsStatus.textContent = "Cargando presupuesto...";
  try {
    const response = await getJson(`/api/budget?folder=${encodeURIComponent(folder)}`);
    const data = response.data || {};
    rememberActiveBudgetFolder(response.folder);
    state.result = data;
    fillClientForm(data.cliente || {});
    els.prompt.value = data.prompt || "";
    state.attachments = [];
    els.attachments.value = "";
    els.fileList.innerHTML = "";
    renderResult();
    updateSaveMode();
    switchView("budgetView");
    setStatus(`Editando ${response.code || response.folder}. Al guardar se actualizara la misma carpeta.`);
    els.budgetsStatus.textContent = "";
  } catch (error) {
    if (options.restored) rememberActiveBudgetFolder(null);
    els.budgetsStatus.textContent = error.message;
  }
}
async function generate() {
  if (!els.prompt.value.trim()) {
    setStatus("Describe primero el trabajo a presupuestar.");
    return;
  }
  const selection = effectiveModelSelection();
  if (!selection.selected || selection.selected.disabled) {
    setStatus("Selecciona un modelo disponible con saldo suficiente.");
    return;
  }
  els.generate.disabled = true;
  setStatus("Generando propuesta...");
  try {
    const response = await api("/api/generate", {
      provider: selection.provider,
      model: selection.model,
      prompt: els.prompt.value.trim(),
      attachments: state.attachments,
    });
    rememberActiveBudgetFolder(null);
    state.budgetChangeLog = [];
    state.result = response.result;
    recordBudgetChange({ source: "generacion", provider: response.provider, model: response.model, titulo: response.result?.titulo || "" });
    state.result.tokenUsage = response.usage || null;
    state.result.tokenStatus = response.tokenStatus || null;
    renderResult();
    await loadModels(selection.provider, false);
    renderModelTokenInfo();
    const usageText = response.usage ? ` Tokens: ${response.usage.inputTokens || 0} entrada / ${response.usage.outputTokens || 0} salida / ${response.usage.totalTokens || 0} total.` : "";
    setStatus(response.warning ? `Usando fallback local: ${response.warning}` : `Generado con ${response.provider}.${usageText}`);
  } catch (error) {
    try {
      const parsed = JSON.parse(error.message);
      setStatus(parsed.error || error.message);
    } catch {
      setStatus(error.message);
    }
  } finally {
    els.generate.disabled = false;
  }
}
async function loadContext() {
  els.contextFiles.innerHTML = "<li>Cargando...</li>";
  const data = await getJson("/api/context");
  els.contextFiles.innerHTML = "";
  for (const file of data.files || []) {
    const li = document.createElement("li");
    li.textContent = file;
    els.contextFiles.appendChild(li);
  }
}

async function loadMe() {
  const data = await getJson("/api/auth/me");
  state.currentUser = data.user;
  els.currentUser.textContent = `${state.currentUser.username} (${state.currentUser.role})`;
  const isAdmin = state.currentUser.role === "admin";
  els.usersNav.classList.toggle("hidden", !isAdmin);
}

async function logout() {
  await api("/api/auth/logout", {});
  window.location.href = appUrl("/login.html");
}

async function loadUsers() {
  if (state.currentUser?.role !== "admin") return;
  els.usersStatus.textContent = "Cargando usuarios...";
  const data = await getJson("/api/users");
  state.users = data.users || [];
  renderUsers();
  els.usersStatus.textContent = `${state.users.length} usuario(s).`;
}

function renderUsers() {
  els.usersBody.innerHTML = "";
  for (const user of state.users) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${escapeHtml(user.username)}</strong><br><small>${escapeHtml(user.updated_at || "")}</small></td>
      <td><select data-role><option value="user">Usuario</option><option value="admin">Admin</option></select></td>
      <td><input data-active type="checkbox"></td>
      <td><input data-password type="password" placeholder="Dejar vacio para conservar"></td>
      <td><div class="user-actions"><button class="secondary" data-save>Guardar</button></div></td>
    `;
    tr.querySelector("[data-role]").value = user.role;
    tr.querySelector("[data-active]").checked = Boolean(user.active);
    tr.querySelector("[data-save]").addEventListener("click", () => saveUser(user.id, tr));
    els.usersBody.appendChild(tr);
  }
}

async function createUserFromForm() {
  els.createUser.disabled = true;
  els.usersStatus.textContent = "Creando usuario...";
  try {
    const response = await api("/api/users", { username: els.newUsername.value, password: els.newUserPassword.value, role: els.newUserRole.value, active: true });
    state.users = response.users || [];
    els.newUsername.value = "";
    els.newUserPassword.value = "";
    renderUsers();
    els.usersStatus.textContent = "Usuario creado.";
  } catch (error) {
    els.usersStatus.textContent = error.message;
  } finally {
    els.createUser.disabled = false;
  }
}

async function saveUser(id, row) {
  const button = row.querySelector("[data-save]");
  button.disabled = true;
  els.usersStatus.textContent = "Guardando usuario...";
  try {
    const payload = { role: row.querySelector("[data-role]").value, active: row.querySelector("[data-active]").checked };
    const password = row.querySelector("[data-password]").value;
    if (password) payload.password = password;
    const response = await api(`/api/users/${id}`, payload, "PUT");
    state.users = response.users || [];
    renderUsers();
    els.usersStatus.textContent = "Usuario guardado.";
  } catch (error) {
    els.usersStatus.textContent = error.message;
  } finally {
    button.disabled = false;
  }
}

const PRICE_DEFAULTS = {
  id: null,
  active: true,
  category: "material",
  area: "general",
  name: "",
  description: "",
  unit: "ud",
  costPrice: 0,
  salePrice: 0,
  marginPercent: 0,
  supplier: "",
  confidence: "confirmado",
  notes: "",
};

function priceMatches(price, query) {
  if (!query) return true;
  return [price.category, price.area, price.name, price.description, price.unit, price.supplier, price.confidence, price.notes]
    .join(" ")
    .toLowerCase()
    .includes(query);
}

function priceCategoryLabel(category) {
  const labels = {
    material: "Materiales",
    mano_obra: "Mano de obra",
    insumo: "Insumos",
    transporte: "Transporte",
    maquinaria: "Maquinaria",
    montaje: "Montaje",
    acabado: "Acabados",
    servicio: "Servicios",
  };
  return labels[category] || category.replaceAll("_", " ");
}

function priceAreaLabel(area) {
  return String(area || "general").replaceAll("_", " ");
}

function priceSortLabel(value) {
  return String(value || "").localeCompare("general") === 0 ? "000_general" : String(value || "");
}

function createPriceRow(price) {
  const tr = document.createElement("tr");
  tr.dataset.id = price.id || "";
  tr.dataset.category = price.category || "material";
  tr.dataset.area = price.area || "general";
  if (!price.active) tr.classList.add("inactive");
  tr.innerHTML = `
    <td><input data-price-active type="checkbox" autocomplete="off" ${price.active ? "checked" : ""}></td>
    <td>
      <input data-price-name autocomplete="off" value="${escapeHtml(price.name || "")}" placeholder="Nombre">
      <textarea data-price-description autocomplete="off" rows="2" placeholder="Descripcion tecnica">${escapeHtml(price.description || "")}</textarea>
    </td>
    <td><input data-price-unit autocomplete="off" value="${escapeHtml(price.unit || "ud")}"></td>
    <td><input data-price-cost autocomplete="off" type="number" step="0.01" inputmode="decimal" value="${Number(price.costPrice || 0)}"></td>
    <td><input data-price-sale autocomplete="off" type="number" step="0.01" inputmode="decimal" value="${Number(price.salePrice || 0)}"></td>
    <td><input data-price-margin autocomplete="off" type="number" step="0.01" inputmode="decimal" value="${Number(price.marginPercent || 0)}"></td>
    <td><input data-price-supplier autocomplete="off" value="${escapeHtml(price.supplier || "")}"></td>
    <td>
      <select data-price-confidence autocomplete="off">
        <option value="confirmado">Confirmado</option>
        <option value="estimado">Estimado</option>
        <option value="antiguo">Antiguo</option>
        <option value="pendiente">Pendiente</option>
      </select>
      <textarea data-price-notes autocomplete="off" rows="2" placeholder="Notas">${escapeHtml(price.notes || "")}</textarea>
    </td>
    <td class="price-actions">
      <button data-delete-price class="row-delete" type="button">x</button>
    </td>
  `;
  tr.querySelector("[data-price-confidence]").value = price.confidence || "confirmado";
  tr.dataset.original = pricePayloadKey(pricePayloadFromRow(tr));
  tr.querySelectorAll("input, textarea, select").forEach((field) => {
    field.addEventListener("blur", () => autoSavePriceFromRow(tr), true);
    field.addEventListener("change", () => autoSavePriceFromRow(tr));
  });
  tr.querySelector("[data-delete-price]").addEventListener("click", () => deletePriceFromRow(tr));
  return tr;
}

function pricePayloadFromRow(row) {
  const costPrice = parseEditableNumber(row.querySelector("[data-price-cost]").value);
  const salePrice = parseEditableNumber(row.querySelector("[data-price-sale]").value);
  return {
    id: row.dataset.id ? Number(row.dataset.id) : null,
    active: row.querySelector("[data-price-active]").checked,
    category: row.dataset.category || "material",
    area: row.dataset.area || "general",
    name: row.querySelector("[data-price-name]").value.trim(),
    description: row.querySelector("[data-price-description]").value.trim(),
    unit: row.querySelector("[data-price-unit]").value.trim() || "ud",
    costPrice,
    salePrice,
    marginPercent: parseEditableNumber(row.querySelector("[data-price-margin]").value),
    supplier: row.querySelector("[data-price-supplier]").value.trim(),
    confidence: row.querySelector("[data-price-confidence]").value,
    notes: row.querySelector("[data-price-notes]").value.trim(),
  };
}

function pricePayloadKey(payload) {
  return JSON.stringify({
    active: Boolean(payload.active),
    category: payload.category || "material",
    area: payload.area || "general",
    name: payload.name || "",
    description: payload.description || "",
    unit: payload.unit || "ud",
    costPrice: Number(payload.costPrice || 0),
    salePrice: Number(payload.salePrice || 0),
    marginPercent: Number(payload.marginPercent || 0),
    supplier: payload.supplier || "",
    confidence: payload.confidence || "confirmado",
    notes: payload.notes || "",
  });
}

function renderPrices() {
  if (!els.pricesBody) return;
  const query = (els.priceSearch?.value || "").trim().toLowerCase();
  els.pricesBody.innerHTML = "";
  const prices = state.prices.filter((price) => priceMatches(price, query));
  if (!prices.length) {
    els.pricesBody.innerHTML = `<div class="empty-state">No hay precios para este filtro.</div>`;
    return;
  }
  const categories = [...new Set(prices.map((price) => price.category || "material"))].sort((a, b) => priceCategoryLabel(a).localeCompare(priceCategoryLabel(b)));
  if (!state.activePriceCategory || !categories.includes(state.activePriceCategory)) state.activePriceCategory = categories[0];
  const tabs = document.createElement("div");
  tabs.className = "price-category-tabs";
  for (const category of categories) {
    const count = prices.filter((price) => (price.category || "material") === category).length;
    const button = document.createElement("button");
    button.type = "button";
    button.className = `price-category-tab${category === state.activePriceCategory ? " active" : ""}`;
    button.textContent = `${priceCategoryLabel(category)} (${count})`;
    button.addEventListener("click", () => {
      state.activePriceCategory = category;
      renderPrices();
    });
    tabs.appendChild(button);
  }
  els.pricesBody.appendChild(tabs);

  const current = prices.filter((price) => (price.category || "material") === state.activePriceCategory);
  const areas = [...new Set(current.map((price) => price.area || "general"))].sort((a, b) => priceSortLabel(a).localeCompare(priceSortLabel(b)));
  const accordion = document.createElement("div");
  accordion.className = "price-accordion";
  for (const area of areas) {
    const areaPrices = current.filter((price) => (price.area || "general") === area);
    const details = document.createElement("details");
    details.className = "price-area";
    details.open = true;
    details.innerHTML = `
      <summary><span>${escapeHtml(priceAreaLabel(area))}</span><small>${areaPrices.length} precio(s)</small></summary>
      <div class="table-wrap price-table-wrap">
        <table class="price-table">
          <thead>
            <tr>
              <th>Activo</th><th>Nombre</th><th>Ud.</th><th>Coste</th><th>Venta</th><th>Margen %</th><th>Proveedor</th><th>Confianza</th><th></th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    `;
    const tbody = details.querySelector("tbody");
    for (const price of areaPrices) tbody.appendChild(createPriceRow(price));
    accordion.appendChild(details);
  }
  els.pricesBody.appendChild(accordion);
}

async function loadPrices() {
  if (!els.pricesBody || state.currentUser?.role !== "admin") return;
  els.priceStatus.textContent = "Cargando precios...";
  try {
    const data = await getJson("/api/prices");
    state.prices = data.prices || [];
    renderPrices();
    els.priceStatus.textContent = `${state.prices.length} precio(s).`;
  } catch (error) {
    els.priceStatus.textContent = error.message;
  }
}

function addPriceItem() {
  state.activePriceCategory = "material";
  state.prices = [{ ...PRICE_DEFAULTS, category: state.activePriceCategory }, ...state.prices];
  if (els.priceSearch) els.priceSearch.value = "";
  renderPrices();
}

async function autoSavePriceFromRow(row) {
  if (row.dataset.saving === "1") return;
  const payload = pricePayloadFromRow(row);
  const currentKey = pricePayloadKey(payload);
  if (currentKey === row.dataset.original) return;
  if (!payload.name) {
    if (row.dataset.id) els.priceStatus.textContent = "Falta el nombre del precio.";
    return;
  }
  row.dataset.saving = "1";
  row.classList.add("saving");
  els.priceStatus.textContent = "Guardando cambios...";
  try {
    const response = await api("/api/prices", payload);
    state.prices = response.prices || [];
    renderPrices();
    const info = response.exportInfo;
    els.priceStatus.textContent = info ? `Cambios guardados. Conocimiento actualizado: ${info.activeCount} activos.` : "Cambios guardados.";
  } catch (error) {
    els.priceStatus.textContent = error.message;
  } finally {
    row.dataset.saving = "0";
    row.classList.remove("saving");
  }
}

async function deletePriceFromRow(row) {
  const id = row.dataset.id;
  if (!id) {
    state.prices = state.prices.filter((price) => price.id);
    renderPrices();
    return;
  }
  els.priceStatus.textContent = "Eliminando precio y actualizando conocimiento...";
  try {
    const response = await api(`/api/prices/${id}`, {}, "DELETE");
    state.prices = response.prices || [];
    renderPrices();
    const info = response.exportInfo;
    els.priceStatus.textContent = info ? `Precio eliminado. Conocimiento actualizado: ${info.activeCount} activos.` : "Precio eliminado.";
  } catch (error) {
    els.priceStatus.textContent = error.message;
  }
}

async function loadSettings() {
  const settings = await getJson("/api/settings");
  state.settings = settings;
  els.defaultProvider.value = settings.defaultProvider || DEFAULT_PROVIDER;
  els.openaiKey.placeholder = settings.openaiApiKeySet ? "Clave guardada; escribe otra para cambiar" : "sk-...";
  els.geminiKey.placeholder = settings.geminiApiKeySet ? "Clave guardada; escribe otra para cambiar" : "AIza...";
  els.falKey.placeholder = settings.falApiKeySet ? "Clave fal.ai guardada; escribe otra para cambiar" : "FAL_KEY...";
  els.openaiBudgets.value = JSON.stringify(settings.modelTokenBudgets?.openai || {}, null, 2);
  els.geminiBudgets.value = JSON.stringify(settings.modelTokenBudgets?.gemini || {}, null, 2);
  const documentTemplate = normalizeDocumentTemplate(settings.documentTemplate);
  els.documentLogo.value = documentTemplate.logo;
  els.documentHeaderText.value = documentTemplate.headerText;
  els.documentFooterText.value = documentTemplate.footerText;
  await loadAllModels();
  selectDefaultModels(settings);
  syncBudgetModelFromSettings(settings);
}

async function loadAllModels() {
  await Promise.all([loadModels("fallback", false), loadModels("openai", false), loadModels("gemini", false)]);
}

async function loadModels(provider, showStatus = true) {
  if (showStatus) els.settingsStatus.textContent = `Actualizando modelos ${provider}...`;
  const data = await getJson(`/api/models?provider=${encodeURIComponent(provider)}`);
  state.models[provider] = data.models || [];
  if (showStatus) els.settingsStatus.textContent = `Modelos ${provider} actualizados.`;
}

function selectDefaultModels(settings = state.settings || {}) {
  fillProviderSelect(els.openaiModel, "openai", settings.openaiModel);
  fillProviderSelect(els.geminiModel, "gemini", settings.geminiModel || DEFAULT_GEMINI_MODEL);
}

function modelCostTier(model) {
  const id = String(model?.id || "").toLowerCase();
  if (!id || id === "fallback") return { key: "neutral", label: "local" };
  if (id.includes("nano") || id.includes("mini") || id.includes("lite") || id.includes("flash") || id.includes("haiku")) {
    return { key: "cheap", label: "economico" };
  }
  if (id.includes("pro") || id.includes("opus") || id.includes("o1") || id.includes("o3") || id.includes("o4") || id.includes("reasoning")) {
    return { key: "expensive", label: "caro" };
  }
  if (id.includes("gpt-4") || id.includes("gpt-5") || id.includes("gemini")) {
    return { key: "medium", label: "medio" };
  }
  return { key: "neutral", label: "sin precio" };
}

function applyModelCostStyle(select, model) {
  const tier = modelCostTier(model).key;
  select.classList.remove("model-cost-cheap", "model-cost-medium", "model-cost-expensive", "model-cost-neutral");
  select.classList.add(`model-cost-${tier}`);
}

function decorateModelOption(option, model) {
  const tier = modelCostTier(model).key;
  option.dataset.cost = tier;
  option.className = `model-cost-option-${tier}`;
}
function fillProviderSelect(select, provider, selectedValue) {
  select.innerHTML = "";
  for (const model of state.models[provider] || []) {
    const option = document.createElement("option");
    option.value = model.id;
    option.textContent = modelLabel(model);
    decorateModelOption(option, model);
    option.disabled = !model.available;
    select.appendChild(option);
  }
  if (selectedValue && [...select.options].some((option) => option.value === selectedValue)) {
    select.value = selectedValue;
    return;
  }
  const economical = firstEconomicalModel(provider);
  if (economical && [...select.options].some((option) => option.value === economical.id)) select.value = economical.id;
}

function modelLabel(model) {
  const tier = modelCostTier(model);
  const parts = [`${model.id} (${tier.label})`];
  if (model.inputTokenLimit) parts.push(`ctx ${Number(model.inputTokenLimit).toLocaleString("es-ES")}`);
  if (model.remainingTokens !== null && model.remainingTokens !== undefined) parts.push(`restan ${Number(model.remainingTokens).toLocaleString("es-ES")}`);
  if (!model.available) parts.push("no disponible");
  return parts.join(" - ");
}

function fallbackPreferredModel(provider) {
  if (provider === "gemini") return DEFAULT_GEMINI_MODEL;
  if (provider === "openai") return "gpt-4.1-mini";
  return "fallback";
}

function firstEconomicalModel(provider) {
  return (state.models[provider] || []).find((model) => model.available && modelCostTier(model).key === "cheap")
    || (state.models[provider] || []).find((model) => model.available && String(model.id || "").toLowerCase().includes("flash"))
    || (state.models[provider] || []).find((model) => model.available);
}
function selectedModel() {
  return (state.models[els.provider.value] || []).find((model) => model.id === els.model.value);
}

function settingsDraft() {
  return {
    ...(state.settings || {}),
    defaultProvider: els.defaultProvider?.value || DEFAULT_PROVIDER,
    openaiModel: els.openaiModel?.value || state.settings?.openaiModel || "",
    geminiModel: els.geminiModel?.value || state.settings?.geminiModel || DEFAULT_GEMINI_MODEL,
  };
}

function effectiveModelSelection() {
  const draft = settingsDraft();
  syncBudgetModelFromSettings(draft);
  const provider = els.provider.value;
  const model = els.model.value;
  return { provider, model, selected: selectedModel() };
}

function preferredModelForProvider(provider, settings = state.settings || {}) {
  if (provider === "openai") return settings.openaiModel || els.openaiModel.value || fallbackPreferredModel(provider);
  if (provider === "gemini") return settings.geminiModel || els.geminiModel.value || fallbackPreferredModel(provider);
  return fallbackPreferredModel(provider);
}

function selectBudgetModel(provider, preferred) {
  const options = [...els.model.options];
  const preferredOption = options.find((option) => option.value === preferred && !option.disabled);
  const economical = firstEconomicalModel(provider);
  const economicalOption = economical ? options.find((option) => option.value === economical.id && !option.disabled) : null;
  const firstEnabled = options.find((option) => !option.disabled);
  if (preferredOption) { els.model.value = preferredOption.value; return; }
  if (economicalOption) { els.model.value = economicalOption.value; return; }
  if (firstEnabled) els.model.value = firstEnabled.value;
}

function syncBudgetModelFromSettings(settings = state.settings || {}) {
  const provider = settings.defaultProvider || DEFAULT_PROVIDER;
  els.provider.value = provider;
  updateModelFromProvider(preferredModelForProvider(provider, settings));
}

function closeMenu() {
  if (!els.appMenu || !els.menuToggle) return;
  els.appMenu.classList.add("hidden");
  els.appMenu.removeAttribute("data-open");
  els.menuToggle.setAttribute("aria-expanded", "false");
}
function updateModelFromProvider(preferredOverride = null) {
  const provider = els.provider.value;
  els.model.innerHTML = "";
  const models = state.models[provider] || [];
  for (const model of models) {
    const option = document.createElement("option");
    option.value = model.id;
    option.textContent = modelLabel(model);
    decorateModelOption(option, model);
    option.disabled = !model.available || (model.remainingTokens !== null && model.remainingTokens <= 0);
    els.model.appendChild(option);
  }
  selectBudgetModel(provider, preferredOverride || preferredModelForProvider(provider));
  const model = selectedModel();
  applyModelCostStyle(els.model, model);
  applyModelCostStyle(provider === "openai" ? els.openaiModel : els.geminiModel, model);
  renderModelTokenInfo();
}

function renderModelTokenInfo() {
  if (!els.modelTokenInfo) return;
  const model = selectedModel();
  const visibleSelect = els.provider.value === "openai" ? els.openaiModel : els.geminiModel;
  if (!model) {
    applyModelCostStyle(els.model, null);
    applyModelCostStyle(visibleSelect, null);
    els.modelTokenInfo.textContent = "No hay modelos disponibles para este proveedor.";
    return;
  }
  const tier = modelCostTier(model);
  applyModelCostStyle(els.model, model);
  applyModelCostStyle(visibleSelect, model);
  const lines = [
    `Proveedor activo: ${els.provider.value}`,
    `Modelo activo: ${model.id}`,
    `Coste relativo: ${tier.label}`,
    `Disponible: ${model.available ? "si" : "no"}`,
    `Entrada max.: ${model.inputTokenLimit ? Number(model.inputTokenLimit).toLocaleString("es-ES") : "no informado"}`,
    `Salida max.: ${model.outputTokenLimit ? Number(model.outputTokenLimit).toLocaleString("es-ES") : "no informado"}`,
    `Usado local: ${Number(model.usedTokens || 0).toLocaleString("es-ES")}`,
    `Saldo local: ${model.remainingTokens === null || model.remainingTokens === undefined ? "sin limite" : Number(model.remainingTokens).toLocaleString("es-ES")}`,
  ];
  if (state.result?.tokenUsage) lines.push(`Ultima llamada: ${state.result.tokenUsage.inputTokens} in / ${state.result.tokenUsage.outputTokens} out / ${state.result.tokenUsage.totalTokens} total`);
  if (model.note) lines.push(model.note);
  if (model.error) lines.push(`Error API: ${model.error}`);
  els.modelTokenInfo.textContent = lines.join("\n");
}

function parseBudgetJson(value, label) {
  if (!value.trim()) return {};
  const parsed = JSON.parse(value);
  if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") throw new Error(`${label} debe ser JSON objeto modelo:tokens.`);
  for (const [model, tokens] of Object.entries(parsed)) {
    if (!model || Number(tokens) < 0) throw new Error(`${label}: token invalido en ${model}.`);
    parsed[model] = Number(tokens);
  }
  return parsed;
}

async function applyDocumentTemplateAi() {
  const prompt = els.documentTemplateAiPrompt.value.trim();
  if (!prompt) {
    els.documentTemplateStatus.textContent = "Escribe una instruccion para la IA.";
    return;
  }
  const selection = effectiveModelSelection();
  if (!selection.selected) {
    els.documentTemplateStatus.textContent = "Selecciona un modelo disponible.";
    return;
  }
  els.applyDocumentTemplateAi.disabled = true;
  els.documentTemplateStatus.textContent = "Editando plantilla con IA...";
  try {
    const response = await api("/api/document-template/ai", {
      provider: selection.provider,
      model: selection.model,
      prompt,
      documentTemplate: templateFromSettingsFields(),
    });
    const documentTemplate = normalizeDocumentTemplate(response.documentTemplate);
    els.documentLogo.value = documentTemplate.logo;
    els.documentHeaderText.value = documentTemplate.headerText;
    els.documentFooterText.value = documentTemplate.footerText;
    els.documentTemplateStatus.textContent = response.warning ? "Edicion local: " + response.warning + ". Revisa y pulsa Guardar configuracion." : "Plantilla editada con " + response.provider + ". Revisa y pulsa Guardar configuracion.";
    if (response.usage) {
      state.result = state.result || {};
      state.result.tokenUsage = response.usage;
      await loadModels(selection.provider, false);
      renderModelTokenInfo();
    }
  } catch (error) {
    try {
      const parsed = JSON.parse(error.message);
      els.documentTemplateStatus.textContent = parsed.error || error.message;
    } catch {
      els.documentTemplateStatus.textContent = error.message;
    }
  } finally {
    els.applyDocumentTemplateAi.disabled = false;
  }
}

async function saveSettings() {
  els.saveSettings.disabled = true;
  els.settingsStatus.textContent = "Guardando...";
  try {
    await api("/api/settings", {
      defaultProvider: els.defaultProvider.value,
      openaiApiKey: els.openaiKey.value,
      openaiModel: els.openaiModel.value,
      geminiApiKey: els.geminiKey.value,
      falApiKey: els.falKey.value,
      geminiModel: els.geminiModel.value,
      modelTokenBudgets: {
        openai: parseBudgetJson(els.openaiBudgets.value, "OpenAI"),
        gemini: parseBudgetJson(els.geminiBudgets.value, "Gemini"),
      },
      documentTemplate: templateFromSettingsFields(),
    });
    els.openaiKey.value = "";
    els.geminiKey.value = "";
    els.falKey.value = "";
    await loadSettings();
    els.settingsStatus.textContent = "Configuracion guardada.";
  } catch (error) {
    els.settingsStatus.textContent = error.message;
  } finally {
    els.saveSettings.disabled = false;
  }
}
async function loadMdFiles() {
  const data = await getJson("/api/md");
  state.mdFiles = data.files || [];
  renderKnowledgeMap();
  renderMdFiles();
}

function renderMdFiles(filesOverride = null) {
  const query = els.mdSearch.value.trim().toLowerCase();
  els.mdFiles.innerHTML = "";
  const sourceFiles = filesOverride || state.mdFiles;
  for (const file of sourceFiles.filter((item) => item.toLowerCase().includes(query))) {
    const li = document.createElement("li");
    li.textContent = file;
    li.className = file === state.activeMdPath ? "active" : "";
    li.addEventListener("click", () => openMd(file));
    els.mdFiles.appendChild(li);
  }
}

async function openMd(file) {
  els.mdStatus.textContent = "Cargando...";
  const data = await getJson(`/api/md/read?path=${encodeURIComponent(file)}`);
  state.activeMdPath = data.path;
  els.mdPath.textContent = data.path;
  els.mdEditor.value = data.content;
  els.mdEditor.disabled = false;
  setMdMode("edit");
  els.mdAiPrompt.disabled = false;
  els.applyMdAi.disabled = false;
  els.saveMd.disabled = false;
  els.mdStatus.textContent = "";
  renderMdFiles();
}

async function applyMdAi() {
  if (!state.activeMdPath) return;
  const prompt = els.mdAiPrompt.value.trim();
  if (!prompt) {
    els.mdStatus.textContent = "Escribe una instruccion para la IA.";
    return;
  }
  const selection = effectiveModelSelection();
  if (!selection.selected) {
    els.mdStatus.textContent = "Selecciona un modelo disponible.";
    return;
  }
  els.applyMdAi.disabled = true;
  els.mdStatus.textContent = "Editando MD con IA...";
  try {
    const response = await api("/api/md/ai", {
      provider: selection.provider,
      model: selection.model,
      path: state.activeMdPath,
      content: els.mdEditor.value,
      prompt,
    });
    els.mdEditor.value = response.content || "";
    if (!els.mdPreview.classList.contains("hidden")) els.mdPreview.innerHTML = renderMarkdown(els.mdEditor.value);
    els.mdStatus.textContent = response.warning ? `Edicion local: ${response.warning}` : `MD actualizado con ${response.provider}. Revisa y pulsa Guardar archivo.`;
    if (response.usage) {
      state.result = state.result || {};
      state.result.tokenUsage = response.usage;
      await loadModels(selection.provider, false);
      renderModelTokenInfo();
    }
  } catch (error) {
    try {
      const parsed = JSON.parse(error.message);
      els.mdStatus.textContent = parsed.error || error.message;
    } catch {
      els.mdStatus.textContent = error.message;
    }
  } finally {
    els.applyMdAi.disabled = false;
  }
}
async function saveMd() {
  if (!state.activeMdPath) return;
  els.saveMd.disabled = true;
  els.mdStatus.textContent = "Guardando...";
  try {
    const response = await api("/api/md/write", { path: state.activeMdPath, content: els.mdEditor.value });
    els.mdStatus.textContent = `Guardado: ${response.path}`;
    await loadContext();
  } catch (error) {
    els.mdStatus.textContent = error.message;
  } finally {
    els.saveMd.disabled = false;
  }
}

function switchView(viewId) {
  if (!VALID_VIEWS.has(viewId) || !document.querySelector(`#${viewId}`)) viewId = DEFAULT_VIEW;
  if (viewId === "usersView" && state.currentUser?.role !== "admin") viewId = DEFAULT_VIEW;
  if (viewId === "usersView") loadUsers();
  if (viewId === "configView") loadPrices();
  document.querySelectorAll(".view").forEach((view) => view.classList.add("hidden"));
  document.querySelector(`#${viewId}`).classList.remove("hidden");
  document.querySelectorAll(".nav-btn[data-view]").forEach((button) => button.classList.toggle("active", button.dataset.view === viewId));
  localStorage.setItem(ACTIVE_VIEW_KEY, viewId);
  if (window.location.hash !== `#${viewId}`) history.replaceState(null, "", `#${viewId}`);
  closeMenu();
}

function restoreActiveView() {
  const hashView = window.location.hash.replace(/^#/, "");
  const storedView = localStorage.getItem(ACTIVE_VIEW_KEY);
  const viewId = VALID_VIEWS.has(hashView) ? hashView : (storedView || DEFAULT_VIEW);
  switchView(viewId);
  const folder = localStorage.getItem(ACTIVE_BUDGET_FOLDER_KEY);
  if (viewId === "budgetView" && folder && !state.result) editBudget(folder, { restored: true });
}

function printBudget() {
  if (!state.result) return;
  const frame = document.createElement("iframe");
  frame.title = "Impresion presupuesto";
  frame.style.position = "fixed";
  frame.style.right = "0";
  frame.style.bottom = "0";
  frame.style.width = "0";
  frame.style.height = "0";
  frame.style.border = "0";
  document.body.appendChild(frame);
  const doc = frame.contentDocument || frame.contentWindow.document;
  doc.open();
  doc.write(window.printDocumentHtml());
  doc.close();
  const cleanup = () => setTimeout(() => frame.remove(), 500);
  frame.contentWindow.onafterprint = cleanup;
  setTimeout(() => {
    frame.contentWindow.focus();
    frame.contentWindow.print();
    setTimeout(cleanup, 3000);
  }, 150);
}

async function generateSummaryPdf() {
  if (!state.result || !els.summaryPdfBudget) return;
  els.summaryPdfBudget.disabled = true;
  setStatus("Generando PDF resumido para el cliente...");
  try {
    const folder = await ensureCurrentBudgetSaved();
    const response = await fetch(appUrl("/api/export-summary-pdf"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folder, payload: resultPayload() }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: "No se pudo generar el PDF resumido." }));
      throw new Error(error.error || "No se pudo generar el PDF resumido.");
    }
    const blob = await response.blob();
    const disposition = response.headers.get("Content-Disposition") || "";
    const encodedName = disposition.match(/filename\*=UTF-8''([^;]+)/i)?.[1];
    const fileName = encodedName ? decodeURIComponent(encodedName) : "presupuesto-resumido-cliente.pdf";
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    await loadBudgets();
    setStatus(`PDF resumido generado y guardado en ${folder}/presupuesto-resumido-cliente.pdf.`);
  } catch (error) {
    setStatus(error.message);
  } finally {
    els.summaryPdfBudget.disabled = false;
  }
}

document.querySelectorAll(".nav-btn[data-view]").forEach((button) => button.addEventListener("click", (event) => { event.stopPropagation(); switchView(button.dataset.view); }));
if (els.menuToggle) els.menuToggle.addEventListener("click", (event) => {
  event.preventDefault();
  event.stopPropagation();
  const isHidden = els.appMenu.classList.toggle("hidden");
  els.appMenu.toggleAttribute("data-open", !isHidden);
  els.menuToggle.setAttribute("aria-expanded", String(!isHidden));
});
if (els.appMenu) els.appMenu.addEventListener("click", (event) => event.stopPropagation());
document.addEventListener("click", (event) => {
  if (!els.appMenu || !els.menuToggle) return;
  if (els.appMenu.classList.contains("hidden")) return;
  if (!els.appMenu.contains(event.target) && !els.menuToggle.contains(event.target)) closeMenu();
});
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.add("hidden"));
    tab.classList.add("active");
    document.querySelector(`#${tab.dataset.tab}`).classList.remove("hidden");
    if (tab.dataset.tab === "final") renderPrintPreview();
  });
});

els.attachments.addEventListener("change", (event) => handleFiles(event.target.files));
els.generate.addEventListener("click", generate);
if (els.insertProductPrompt) els.insertProductPrompt.addEventListener("click", insertSelectedProductPrompt);
if (els.productSelect) els.productSelect.addEventListener("change", () => {
  const product = selectedProduct();
  els.productPromptStatus.textContent = product ? `${product.variablesTecnicas?.length || 0} parametro(s) sugeridos.` : "";
});
els.refreshContext.addEventListener("click", loadContext);
els.saveSettings.addEventListener("click", saveSettings);
els.logout.addEventListener("click", logout);
els.createUser.addEventListener("click", createUserFromForm);
if (els.refreshPrices) els.refreshPrices.addEventListener("click", loadPrices);
if (els.newPriceItem) els.newPriceItem.addEventListener("click", addPriceItem);
if (els.priceSearch) els.priceSearch.addEventListener("input", renderPrices);
els.applyDocumentTemplateAi.addEventListener("click", applyDocumentTemplateAi);
els.provider.addEventListener("change", updateModelFromProvider);
els.defaultProvider.addEventListener("change", () => { syncBudgetModelFromSettings({ ...state.settings, defaultProvider: els.defaultProvider.value, openaiModel: els.openaiModel.value, geminiModel: els.geminiModel.value }); });
els.model.addEventListener("change", renderModelTokenInfo);
els.openaiModel.addEventListener("change", () => { if (els.defaultProvider.value === "openai") syncBudgetModelFromSettings({ ...state.settings, defaultProvider: "openai", openaiModel: els.openaiModel.value, geminiModel: els.geminiModel.value }); });
els.geminiModel.addEventListener("change", () => { if (els.defaultProvider.value === "gemini") syncBudgetModelFromSettings({ ...state.settings, defaultProvider: "gemini", openaiModel: els.openaiModel.value, geminiModel: els.geminiModel.value }); });
els.refreshModels.addEventListener("click", async () => { await loadSettings(); els.settingsStatus.textContent = "Modelos actualizados."; });
els.refreshBudgets.addEventListener("click", loadBudgets);
els.budgetYear.addEventListener("change", renderBudgets);
if (els.budgetSearch) els.budgetSearch.addEventListener("input", renderBudgets);
els.newBudget.addEventListener("click", newBudget);
els.mdSearch.addEventListener("input", () => renderMdFiles());
els.clearMdFilter.addEventListener("click", () => { els.mdSearch.value = ""; renderMdFiles(); });
if (els.createProduct) els.createProduct.addEventListener("click", createProductFromForm);
els.applyMdAi.addEventListener("click", applyMdAi);
els.saveMd.addEventListener("click", saveMd);
els.mdEditMode.addEventListener("click", () => setMdMode("edit"));
els.mdPreviewMode.addEventListener("click", () => setMdMode("preview"));
els.mdEditor.addEventListener("input", () => { if (!els.mdPreview.classList.contains("hidden")) els.mdPreview.innerHTML = renderMarkdown(els.mdEditor.value); });
els.printBudget.addEventListener("click", printBudget);
if (els.summaryPdfBudget) els.summaryPdfBudget.addEventListener("click", generateSummaryPdf);
if (els.generateBudgetImage) els.generateBudgetImage.addEventListener("click", generateBudgetImageForCurrent);
[els.clientName, els.clientEmail, els.clientPhone, els.clientTax, els.clientAddress, els.clientRef].forEach((input) => input.addEventListener("input", renderPrintPreview));
[els.title, els.summaryText, els.productType].forEach((input) => input.addEventListener("input", () => { syncBudgetHeaderFromInputs(); renderPrintPreview(); }));

els.clear.addEventListener("click", clearBudgetForm);


els.addLine.addEventListener("click", () => {
  if (!state.result) return;
  const line = {
    id: `L${state.result.lineas.length + 1}`,
    capitulo: "Materiales",
    concepto: "Nueva linea",
    descripcion: "",
    cantidad: 1,
    unidad: "ud",
    precioUnitario: 0,
    importe: 0,
    confianza: "media",
    origen: "usuario",
    editable: true,
  };
  state.result.lineas.push(line);
  recordBudgetChange({ source: "manual", action: "add-line", lineIndex: state.result.lineas.length - 1, after: lineLearningSnapshot(line) });
  renderResult();
});

els.exportBudget.addEventListener("click", async () => {
  if (!state.result) return;
  els.exportBudget.disabled = true;
  const response = await api("/api/export", resultPayload());
  rememberActiveBudgetFolder(response.folder);
  updateSaveMode();
  await loadBudgets();
  if (response.learningFile) state.budgetChangeLog = [];
  const learningText = response.learningFile ? ` Aprendizaje actualizado en ${response.learningFile}.` : "";
  setStatus(`${response.updated ? "Actualizado" : "Guardado"}: ${response.folder}/README.md y presupuesto-final.html.${learningText}`);
  els.exportBudget.disabled = false;
});

loadMe().then(() => {
  restoreActiveView();
  loadContext();
  loadSettings();
  loadMdFiles();
  loadProducts();
  loadBudgets();
});
