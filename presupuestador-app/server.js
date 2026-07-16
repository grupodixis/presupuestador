const http = require("http");
const fs = require("fs/promises");
const fsSync = require("fs");
const path = require("path");
const { DatabaseSync } = require("node:sqlite");

const PORT = Number(process.env.PORT || 4177);
const BASE_PATH = normalizeBasePath(process.env.BASE_PATH || "");
const ROOT = path.resolve(__dirname, "..");
const PUBLIC_DIR = path.join(__dirname, "public");
const CONFIG_FILE = path.join(__dirname, "config.local.json");
const TOKEN_USAGE_FILE = path.join(__dirname, "token-usage.local.json");
const DB_DIR = path.join(__dirname, "data");
const DB_FILE = path.join(DB_DIR, "presupuestador.sqlite");
const LEARNING_FILE = path.join(ROOT, "skills", "aprendizaje_presupuestador_app.md");
const EDITABLE_DIRS = ["skills", "presupuestacion", "productos", "plantillas", "proveedores", "glosario"];
const EDITABLE_EXTENSIONS = new Set([".md", ".yaml", ".yml", ".json"]);

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".pdf": "application/pdf",
  ".md": "text/markdown; charset=utf-8",
};

function normalizeBasePath(value) {
  const normalized = String(value || "").trim().replace(/\/+$/, "");
  if (!normalized || normalized === "/") return "";
  return normalized.startsWith("/") ? normalized : `/${normalized}`;
}

function stripBasePath(pathname) {
  if (!BASE_PATH) return pathname;
  if (pathname === BASE_PATH) return "/";
  if (pathname.startsWith(`${BASE_PATH}/`)) return pathname.slice(BASE_PATH.length) || "/";
  return null;
}

let database = null;

function db() {
  if (database) return database;
  fsSync.mkdirSync(DB_DIR, { recursive: true });
  database = new DatabaseSync(DB_FILE);
  database.exec(`
    PRAGMA journal_mode = WAL;
    CREATE TABLE IF NOT EXISTS app_settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS token_usage (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      at TEXT NOT NULL,
      provider TEXT NOT NULL,
      model TEXT NOT NULL,
      input_tokens INTEGER NOT NULL DEFAULT 0,
      output_tokens INTEGER NOT NULL DEFAULT 0,
      total_tokens INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS budgets (
      folder TEXT PRIMARY KEY,
      code TEXT NOT NULL,
      year TEXT NOT NULL,
      number INTEGER NOT NULL,
      title TEXT NOT NULL,
      client_name TEXT NOT NULL DEFAULT '',
      total REAL NOT NULL DEFAULT 0,
      data_json TEXT NOT NULL,
      html_path TEXT NOT NULL DEFAULT '',
      updated_at TEXT NOT NULL
    );
  `);
  return database;
}

function dbGetJson(key, fallback = null) {
  const row = db().prepare("SELECT value FROM app_settings WHERE key = ?").get(key);
  if (!row) return fallback;
  try {
    return JSON.parse(row.value);
  } catch {
    return fallback;
  }
}

function dbSetJson(key, value) {
  db().prepare(`
    INSERT INTO app_settings (key, value, updated_at)
    VALUES (?, ?, ?)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
  `).run(key, JSON.stringify(value), new Date().toISOString());
}

function budgetCodeParts(code) {
  const match = String(code || "").match(/^P-(\d{4})-(\d{4})$/);
  return { year: match?.[1] || new Date().getFullYear().toString(), number: Number(match?.[2] || 0) };
}

function budgetTotal(payload) {
  return (payload.lineas || []).reduce((sum, line) => sum + Number(line.importe || 0), 0);
}

function saveBudgetRecord({ folder, code, payload, htmlPath }) {
  const relFolder = path.relative(ROOT, folder).replaceAll("\\", "/");
  const parts = budgetCodeParts(code);
  db().prepare(`
    INSERT INTO budgets (folder, code, year, number, title, client_name, total, data_json, html_path, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(folder) DO UPDATE SET
      code = excluded.code,
      year = excluded.year,
      number = excluded.number,
      title = excluded.title,
      client_name = excluded.client_name,
      total = excluded.total,
      data_json = excluded.data_json,
      html_path = excluded.html_path,
      updated_at = excluded.updated_at
  `).run(
    relFolder,
    code,
    parts.year,
    parts.number,
    payload.titulo || "Presupuesto",
    payload.cliente?.nombre || "",
    budgetTotal(payload),
    JSON.stringify(payload),
    htmlPath || `${relFolder}/presupuesto-final.html`,
    new Date().toISOString(),
  );
  return relFolder;
}

function getBudgetRecord(relativeFolder) {
  return db().prepare("SELECT * FROM budgets WHERE folder = ?").get(String(relativeFolder || "").replaceAll("\\", "/"));
}

function dbStatus() {
  const budgetCount = db().prepare("SELECT COUNT(*) AS count FROM budgets").get().count;
  const tokenCount = db().prepare("SELECT COUNT(*) AS count FROM token_usage").get().count;
  return { file: DB_FILE, budgetCount, tokenUsageCount: tokenCount };
}
function send(res, status, body, contentType = "application/json; charset=utf-8") {
  res.writeHead(status, { "Content-Type": contentType });
  if (Buffer.isBuffer(body)) {
    res.end(body);
    return;
  }
  res.end(typeof body === "string" ? body : JSON.stringify(body));
}

async function readJson(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString("utf8");
  if (!raw) return {};
  return JSON.parse(raw);
}

async function fileExists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function readLimited(file, max = 16000) {
  const content = await fs.readFile(file, "utf8");
  return content.length > max ? `${content.slice(0, max)}\n\n[Contenido truncado]` : content;
}

async function listFiles(dir, predicate) {
  const out = [];
  async function walk(current) {
    const entries = await fs.readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) await walk(full);
      if (entry.isFile() && predicate(full)) out.push(full);
    }
  }
  if (await fileExists(dir)) await walk(dir);
  return out.sort();
}

function defaultConfig() {
  return {
    defaultProvider: "fallback",
    openaiApiKey: "",
    openaiModel: "",
    geminiApiKey: "",
    geminiModel: "",
    modelTokenBudgets: { openai: {}, gemini: {} },
  };
}

async function readConfig() {
  const defaults = defaultConfig();
  let config = dbGetJson("config", null);
  if (!config && (await fileExists(CONFIG_FILE))) {
    config = JSON.parse(await fs.readFile(CONFIG_FILE, "utf8"));
    dbSetJson("config", { ...defaults, ...config });
  }
  config = config || defaults;
  return {
    ...defaults,
    ...config,
    modelTokenBudgets: {
      openai: config.modelTokenBudgets?.openai || {},
      gemini: config.modelTokenBudgets?.gemini || {},
    },
  };
}

function maskedConfig(config) {
  return {
    defaultProvider: config.defaultProvider || "fallback",
    openaiApiKeySet: Boolean(config.openaiApiKey),
    openaiModel: config.openaiModel || "",
    geminiApiKeySet: Boolean(config.geminiApiKey),
    geminiModel: config.geminiModel || "",
    modelTokenBudgets: config.modelTokenBudgets || { openai: {}, gemini: {} },
  };
}

async function writeConfig(config) {
  const current = await readConfig();
  const next = {
    defaultProvider: ["fallback", "openai", "gemini"].includes(config.defaultProvider) ? config.defaultProvider : current.defaultProvider || "fallback",
    openaiApiKey: config.openaiApiKey ? config.openaiApiKey : current.openaiApiKey,
    openaiModel: config.openaiModel ?? current.openaiModel,
    geminiApiKey: config.geminiApiKey ? config.geminiApiKey : current.geminiApiKey,
    geminiModel: config.geminiModel ?? current.geminiModel,
    modelTokenBudgets: config.modelTokenBudgets || current.modelTokenBudgets || { openai: {}, gemini: {} },
  };
  dbSetJson("config", next);
  await fs.writeFile(CONFIG_FILE, JSON.stringify(next, null, 2), "utf8");
  return maskedConfig(next);
}

function resolveEditable(relativePath) {
  const normalized = String(relativePath || "").replaceAll("\\", "/");
  const first = normalized.split("/")[0];
  const ext = path.extname(normalized).toLowerCase();
  if (!EDITABLE_DIRS.includes(first) || !EDITABLE_EXTENSIONS.has(ext)) {
    throw new Error("Archivo fuera de los contextos editables.");
  }
  const full = path.resolve(ROOT, normalized);
  if (!full.startsWith(ROOT)) throw new Error("Ruta no permitida.");
  return full;
}

async function listEditableFiles() {
  const files = [];
  for (const dir of EDITABLE_DIRS) {
    const full = path.join(ROOT, dir);
    const found = await listFiles(full, (file) => EDITABLE_EXTENSIONS.has(path.extname(file).toLowerCase()));
    files.push(...found.map((file) => path.relative(ROOT, file).replaceAll("\\", "/")));
  }
  return files.sort();
}

async function readTokenUsage() {
  const rows = db().prepare(`
    SELECT at, provider, model, input_tokens AS inputTokens, output_tokens AS outputTokens, total_tokens AS totalTokens
    FROM token_usage
    ORDER BY id ASC
  `).all();
  if (rows.length) return rows;
  if (!(await fileExists(TOKEN_USAGE_FILE))) return [];
  const entries = JSON.parse(await fs.readFile(TOKEN_USAGE_FILE, "utf8"));
  for (const entry of entries) {
    db().prepare(`
      INSERT INTO token_usage (at, provider, model, input_tokens, output_tokens, total_tokens)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(entry.at || new Date().toISOString(), entry.provider || "", entry.model || "", Number(entry.inputTokens || 0), Number(entry.outputTokens || 0), Number(entry.totalTokens || 0));
  }
  return entries;
}

async function writeTokenUsage(entries) {
  db().exec("DELETE FROM token_usage");
  for (const entry of entries.slice(-1000)) {
    db().prepare(`
      INSERT INTO token_usage (at, provider, model, input_tokens, output_tokens, total_tokens)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(entry.at || new Date().toISOString(), entry.provider || "", entry.model || "", Number(entry.inputTokens || 0), Number(entry.outputTokens || 0), Number(entry.totalTokens || 0));
  }
  await fs.writeFile(TOKEN_USAGE_FILE, JSON.stringify(entries.slice(-1000), null, 2), "utf8");
}

async function recordTokenUsage(provider, model, usage) {
  if (!usage || !model || provider === "fallback") return;
  db().prepare(`
    INSERT INTO token_usage (at, provider, model, input_tokens, output_tokens, total_tokens)
    VALUES (?, ?, ?, ?, ?, ?)
  `).run(new Date().toISOString(), provider, model, Number(usage.inputTokens || 0), Number(usage.outputTokens || 0), Number(usage.totalTokens || 0));
  const entries = await readTokenUsage();
  await fs.writeFile(TOKEN_USAGE_FILE, JSON.stringify(entries.slice(-1000), null, 2), "utf8");
}

function usedTokensFor(entries, provider, model) {
  return entries
    .filter((entry) => entry.provider === provider && entry.model === model)
    .reduce((sum, entry) => sum + Number(entry.totalTokens || 0), 0);
}

function estimateTokensFromText(text) {
  return Math.ceil(String(text || "").length / 4);
}

function estimateRequestTokens(prompt, attachments = []) {
  const textTokens = estimateTokensFromText(prompt) + attachments.reduce((sum, file) => {
    if (file.kind === "image") return sum + 1100;
    return sum + estimateTokensFromText(file.text || "");
  }, 0);
  return Math.max(1, textTokens);
}

function openAiTokenInfo(id) {
  const model = String(id || "");
  if (model.includes("gpt-4.1")) return { inputTokenLimit: 1047576, outputTokenLimit: 32768, note: "Limites aproximados por familia; OpenAI /v1/models no devuelve ventana de contexto." };
  if (model.includes("gpt-4o")) return { inputTokenLimit: 128000, outputTokenLimit: 16384, note: "Limites aproximados por familia; OpenAI /v1/models no devuelve ventana de contexto." };
  if (model.includes("gpt-5")) return { inputTokenLimit: 400000, outputTokenLimit: 128000, note: "Limites aproximados por familia; OpenAI /v1/models no devuelve ventana de contexto." };
  if (model.includes("o3") || model.includes("o4")) return { inputTokenLimit: 200000, outputTokenLimit: 100000, note: "Limites aproximados por familia; OpenAI /v1/models no devuelve ventana de contexto." };
  return { inputTokenLimit: null, outputTokenLimit: null, note: "Modelo listado por la API; limites no publicados en /v1/models." };
}

function fallbackModels(provider) {
  if (provider === "openai") {
    return ["gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini", "gpt-4o"].map((id) => ({ id, provider, available: false, source: "fallback", ...openAiTokenInfo(id) }));
  }
  if (provider === "gemini") {
    return [
      { id: "gemini-1.5-pro", inputTokenLimit: 2000000, outputTokenLimit: 8192 },
      { id: "gemini-1.5-flash", inputTokenLimit: 1000000, outputTokenLimit: 8192 },
    ].map((model) => ({ ...model, provider, available: false, source: "fallback", note: "Fallback local; pulsa actualizar con API key para lista real." }));
  }
  return [{ id: "fallback", provider: "fallback", available: true, source: "local", inputTokenLimit: null, outputTokenLimit: null, note: "Estimacion local sin API." }];
}

function modelCanGenerate(id) {
  const model = String(id || "");
  return /^(gpt|o\d|chatgpt|gemini)/i.test(model) && !model.includes("embedding") && !model.includes("audio") && !model.includes("tts") && !model.includes("image");
}

async function listOpenAIModels(config) {
  const key = process.env.OPENAI_API_KEY || config.openaiApiKey;
  if (!key) return fallbackModels("openai");
  const response = await fetch("https://api.openai.com/v1/models", { headers: { Authorization: `Bearer ${key}` } });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || `OpenAI models HTTP ${response.status}`);
  return (data.data || [])
    .map((model) => model.id)
    .filter(modelCanGenerate)
    .sort()
    .map((id) => ({ id, provider: "openai", available: true, source: "api", ownedBy: data.data.find((m) => m.id === id)?.owned_by, ...openAiTokenInfo(id) }));
}

async function listGeminiModels(config) {
  const key = process.env.GEMINI_API_KEY || config.geminiApiKey;
  if (!key) return fallbackModels("gemini");
  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000&key=${key}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || `Gemini models HTTP ${response.status}`);
  return (data.models || [])
    .filter((model) => (model.supportedGenerationMethods || []).includes("generateContent"))
    .map((model) => ({
      id: String(model.name || "").replace(/^models\//, ""),
      provider: "gemini",
      available: true,
      source: "api",
      displayName: model.displayName,
      inputTokenLimit: model.inputTokenLimit || null,
      outputTokenLimit: model.outputTokenLimit || null,
      note: "Limites devueltos por Gemini models.list.",
    }))
    .sort((a, b) => a.id.localeCompare(b.id));
}

async function modelStatus(provider, model, estimateTokens = 0) {
  const config = await readConfig();
  const entries = await readTokenUsage();
  const budget = Number(config.modelTokenBudgets?.[provider]?.[model] || 0);
  const used = usedTokensFor(entries, provider, model);
  const remaining = budget > 0 ? Math.max(0, budget - used) : null;
  return {
    provider,
    model,
    estimatedInputTokens: Number(estimateTokens || 0),
    localBudgetTokens: budget || null,
    usedTokens: used,
    remainingTokens: remaining,
    blocked: remaining !== null && remaining < Number(estimateTokens || 0),
    note: remaining === null ? "Sin presupuesto local configurado; la API no expone saldo restante por modelo con una key normal." : "Saldo restante calculado localmente con el uso registrado por esta app.",
  };
}

function normalizeOpenAIUsage(usage) {
  return {
    inputTokens: Number(usage?.input_tokens || 0),
    outputTokens: Number(usage?.output_tokens || 0),
    totalTokens: Number(usage?.total_tokens || usage?.input_tokens + usage?.output_tokens || 0),
  };
}

function normalizeGeminiUsage(usage) {
  return {
    inputTokens: Number(usage?.promptTokenCount || 0),
    outputTokens: Number(usage?.candidatesTokenCount || 0),
    totalTokens: Number(usage?.totalTokenCount || usage?.promptTokenCount + usage?.candidatesTokenCount || 0),
  };
}
async function loadRepositoryContext() {
  const skillFiles = await listFiles(path.join(ROOT, "skills"), (file) => file.endsWith(".md"));
  const compositionFiles = await listFiles(path.join(ROOT, "productos", "composiciones"), (file) => file.endsWith(".yaml"));
  const costingFiles = await listFiles(path.join(ROOT, "presupuestacion", "costes"), (file) =>
    file.endsWith(".json") || file.endsWith(".md")
  );

  const selected = [
    path.join(ROOT, "README.md"),
    path.join(ROOT, "presupuestacion", "criterios-ambientales-menorca.md"),
    path.join(ROOT, "presupuestacion", "criterios-comerciales.md"),
    ...skillFiles,
    ...compositionFiles,
    ...costingFiles,
  ];

  const docs = [];
  for (const file of selected) {
    if (!(await fileExists(file))) continue;
    docs.push({
      path: path.relative(ROOT, file).replaceAll("\\", "/"),
      content: await readLimited(file, 12000),
    });
  }
  return docs;
}

function buildSystemPrompt(context) {
  return `Eres un agente de presupuestacion tecnica y comercial para fabricacion a medida.
Trabajas con el repositorio local de HAM y debes devolver SIEMPRE JSON valido.

Objetivo:
- Convertir el prompt y adjuntos del usuario en lineas de presupuesto editables.
- Descomponer productos compuestos en componentes, interfaces, procesos, riesgos y dudas.
- Proponer sugerencias tecnicas que el usuario pueda aceptar y memorizar en skills Markdown.
- Respetar Menorca por defecto: ambiente salino, corrosivo, tratamientos C4/C5, inox A4/316 cuando aplique.

Formato exacto de respuesta:
{
  "titulo": "string",
  "resumen": "string",
  "tipoProducto": "string",
  "lineas": [
    {
      "id": "L1",
      "capitulo": "Diseno | Materiales | Fabricacion | Tratamiento | Transporte | Montaje | Riesgo | Margen",
      "concepto": "string",
      "descripcion": "string",
      "cantidad": number,
      "unidad": "ud | ml | m2 | kg | h | lote",
      "precioUnitario": number,
      "importe": number,
      "confianza": "alta | media | baja",
      "origen": "skill/coste/supuesto/adjunto",
      "editable": true
    }
  ],
  "preguntas": ["string"],
  "supuestos": ["string"],
  "riesgos": ["string"],
  "sugerencias": [
    {
      "id": "S1",
      "titulo": "string",
      "detalle": "string",
      "skillDestino": "skills/aprendizaje_presupuestador_app.md",
      "prioridad": "alta | media | baja"
    }
  ]
}

Contexto del repositorio:
${context.map((doc) => `\n--- ${doc.path} ---\n${doc.content}`).join("\n")}`;
}

function attachmentSummary(attachments = []) {
  return attachments
    .map((file) => {
      if (file.kind === "image") return `Imagen: ${file.name} (${file.type || "sin tipo"})`;
      return `Documento: ${file.name}\n${String(file.text || "").slice(0, 12000)}`;
    })
    .join("\n\n");
}

function fallbackEstimate(prompt, attachments = []) {
  const lower = prompt.toLowerCase();
  const isPergola = lower.includes("pergola") || lower.includes("pergola") || lower.includes("marquesina");
  const isBarandilla = lower.includes("barandilla");
  const title = isPergola ? "Presupuesto preliminar de pergola/marquesina" : isBarandilla ? "Presupuesto preliminar de barandilla" : "Presupuesto preliminar de producto compuesto";
  const areaMatch = prompt.match(/(\d+(?:[,.]\d+)?)\s*[xX]\s*(\d+(?:[,.]\d+)?)/);
  const area = areaMatch ? Number(areaMatch[1].replace(",", ".")) * Number(areaMatch[2].replace(",", ".")) : 1;
  const baseLines = [
    ["Diseno", "Medicion, replanteo y despiece tecnico", "Preparacion de datos, validacion de medidas, definicion de alcance y dudas.", 2, "h", 55],
    ["Materiales", isPergola ? "Estructura principal y anclajes" : "Materiales principales del compuesto", "Estimacion inicial segun composicion tecnica y ambiente exterior Menorca.", Math.max(1, area), isPergola ? "m2" : "lote", isPergola ? 135 : 420],
    ["Fabricacion", "Corte, mecanizado y ensamblaje en taller", "Horas de taller para preparacion, soldadura/ensamblaje y ajuste.", Math.max(6, area * 1.5), "h", 40],
    ["Tratamiento", "Tratamiento superficial anticorrosivo", "Galvanizado/lacado/sistema C4-C5 o inox segun material definido.", Math.max(1, area), isPergola ? "m2" : "lote", isPergola ? 48 : 260],
    ["Transporte", "Transporte a obra", "Carga, proteccion y desplazamiento local.", 1, "lote", 180],
    ["Montaje", "Montaje en obra y remates", "Equipo de montaje, fijaciones, nivelacion, sellados y verificacion final.", Math.max(4, area), "h", 45],
    ["Riesgo", "Reserva por integracion y datos pendientes", "Partida provisional hasta confirmar planos, accesos, cargas y acabados.", 1, "lote", 350],
  ];
  const lineas = baseLines.map((line, index) => {
    const cantidad = Number(line[3]);
    const precioUnitario = Number(line[5]);
    return {
      id: `L${index + 1}`,
      capitulo: line[0],
      concepto: line[1],
      descripcion: line[2],
      cantidad,
      unidad: line[4],
      precioUnitario,
      importe: Math.round(cantidad * precioUnitario * 100) / 100,
      confianza: "media",
      origen: "fallback local",
      editable: true,
    };
  });
  return {
    titulo: title,
    resumen: "Estimacion local generada sin API key. Sirve como primera descomposicion editable.",
    tipoProducto: isPergola ? "marquesina_pergola" : isBarandilla ? "barandilla" : "producto_compuesto",
    lineas,
    preguntas: [
      "Confirmar dimensiones exactas, ubicacion y accesos de obra.",
      "Confirmar material, acabado y exigencia anticorrosiva.",
      "Adjuntar plano, croquis o fotos si existen.",
    ],
    supuestos: [
      "Menorca por defecto, ambiente salino exterior si no se indica lo contrario.",
      `${attachments.length} adjunto(s) recibido(s), revisados como apoyo si contienen texto legible.`,
    ],
    riesgos: [
      "Precio orientativo hasta validar mediciones y proveedor.",
      "La complejidad puede subir si hay montaje en altura, cargas estructurales o plazos cortos.",
    ],
    sugerencias: [
      {
        id: "S1",
        titulo: "Pedir siempre fotos de acceso y anclajes",
        detalle: "En productos a medida exteriores, guardar como criterio que las fotos de accesos, anclajes y entorno reducen riesgo de montaje.",
        skillDestino: "skills/aprendizaje_presupuestador_app.md",
        prioridad: "media",
      },
    ],
  };
}

function buildLinePrompt({ prompt, budget, lineIndex }) {
  const line = budget?.lineas?.[lineIndex] || null;
  return `El usuario esta editando un presupuesto ya existente desde la interfaz.

Debes tener consciencia del presupuesto completo actual y de todas las modificaciones manuales ya hechas.

Instruccion del usuario para la linea seleccionada:
${prompt}

Indice de linea seleccionada: ${lineIndex}
Linea seleccionada actual:
${JSON.stringify(line, null, 2)}

Presupuesto completo actual:
${JSON.stringify(budget, null, 2)}

Devuelve SIEMPRE el presupuesto completo en el mismo formato JSON esperado por el sistema.
Reglas:
- Modifica solo la linea seleccionada salvo que el prompt pida expresamente ajustar otras partidas relacionadas.
- Si el usuario pide cambiar precio, precio unitario, cantidad, descuento, subida/bajada, subtotal o importe, actualiza los campos numericos correspondientes; no lo escribas solo en descripcion.
- Conserva datos de cliente, supuestos, riesgos, preguntas y sugerencias si no hay razon para cambiarlos.
- Recalcula importe = cantidad * precioUnitario en las lineas que modifiques.
- Si falta informacion, deja la linea con confianza baja y anade una pregunta concreta.
- No borres lineas salvo que el prompt lo pida literalmente.`;
}

function parseSpanishNumber(raw) {
  if (raw === null || raw === undefined) return null;
  const value = Number(String(raw).trim().replace(/\s/g, "").replace(/\./g, "").replace(",", "."));
  return Number.isFinite(value) ? value : null;
}

function roundMoney(value) {
  return Math.round(Number(value || 0) * 100) / 100;
}

function firstNumberAfter(text, pattern) {
  const match = String(text || "").match(pattern);
  return match ? parseSpanishNumber(match[1]) : null;
}

function applyNumericInstructionToLine(line, prompt) {
  const text = String(prompt || "");
  const normalized = text.toLowerCase();
  let changed = false;

  line.cantidad = Number(line.cantidad || 0);
  line.precioUnitario = Number(line.precioUnitario || 0);

  const qty = firstNumberAfter(normalized, /(?:cantidad|cant\.?)\D{0,25}(\d+(?:[.,]\d+)?)/i);
  if (qty !== null) {
    line.cantidad = qty;
    changed = true;
  }

  const percentMatch = normalized.match(/\b(sube|subir|aumenta|aumentar|incrementa|incrementar|baja|bajar|reduce|reducir|descuenta|descontar)\b[\s\S]{0,30}?(\d+(?:[.,]\d+)?)\s*%/i);
  let percentChanged = false;
  if (percentMatch) {
    const percent = parseSpanishNumber(percentMatch[2]);
    if (percent !== null) {
      const isReduction = /baja|bajar|reduce|reducir|descuenta|descontar/i.test(percentMatch[1]);
      const factor = isReduction ? 1 - percent / 100 : 1 + percent / 100;
      line.precioUnitario = roundMoney(line.precioUnitario * factor);
      changed = true;
      percentChanged = true;
    }
  }

  const explicitUnitPrice = firstNumberAfter(normalized, /(?:precio\s*unitario|precio\/ud|eur\/ud|€\/ud|unidad|unitario|p\.?\s*u\.?)\D{0,35}(\d+(?:[.,]\d+)?)/i);
  const genericUnitPrice = percentChanged ? null : firstNumberAfter(normalized, /(?:precio|coste|valor)\D{0,30}(?:a|en|de)?\D{0,10}(\d+(?:[.,]\d+)?)/i);
  const unitPrice = explicitUnitPrice ?? genericUnitPrice;
  if (unitPrice !== null) {
    line.precioUnitario = unitPrice;
    changed = true;
  }

  const targetTotal = firstNumberAfter(normalized, /(?:subtotal|importe|total\s+de\s+la\s+linea|linea\s+a)\D{0,35}(\d+(?:[.,]\d+)?)/i);
  if (targetTotal !== null && line.cantidad) {
    line.precioUnitario = roundMoney(targetTotal / line.cantidad);
    changed = true;
  }

  if (!changed) {
    const putValue = firstNumberAfter(normalized, /(?:pon(?:lo)?|cambia(?:lo)?|deja(?:lo)?)\D{0,25}(?:a|en)?\D{0,10}(\d+(?:[.,]\d+)?)/i);
    if (putValue !== null) {
      line.precioUnitario = putValue;
      changed = true;
    }
  }

  line.precioUnitario = roundMoney(line.precioUnitario);
  line.importe = roundMoney(line.cantidad * line.precioUnitario);
  return changed;
}

function fallbackLineEdit({ prompt, budget, lineIndex }) {
  const next = JSON.parse(JSON.stringify(budget || {}));
  next.lineas = Array.isArray(next.lineas) ? next.lineas : [];
  const line = next.lineas[lineIndex];
  if (!line) return next;
  const text = String(prompt || "").trim();
  const numericChanged = applyNumericInstructionToLine(line, text);
  if (text && !numericChanged) {
    line.descripcion = `${line.descripcion || ""}\nAjuste solicitado: ${text}`.trim();
    line.origen = "edicion IA local";
    line.confianza = line.confianza || "media";
  } else if (numericChanged) {
    line.origen = "edicion IA local";
    line.confianza = line.confianza || "media";
  }
  line.cantidad = Number(line.cantidad || 0);
  line.precioUnitario = Number(line.precioUnitario || 0);
  line.importe = roundMoney(line.cantidad * line.precioUnitario);
  next.sugerencias = next.sugerencias || [];
  next.sugerencias.push({
    id: `S${next.sugerencias.length + 1}`,
    titulo: "Revision manual de linea",
    detalle: numericChanged ? "El modo local ha aplicado la instruccion sobre los campos numericos de la linea." : "El modo local ha anotado el prompt en la linea. Usa OpenAI o Gemini para recalculo tecnico automatico.",
    skillDestino: "skills/aprendizaje_presupuestador_app.md",
    prioridad: "baja",
  });
  return next;
}
function normalizeAgentJson(text) {
  const trimmed = text.trim();
  if (trimmed.startsWith("{")) return JSON.parse(trimmed);
  const match = trimmed.match(/\{[\s\S]*\}/);
  if (!match) throw new Error("La API no devolvio JSON reconocible.");
  return JSON.parse(match[0]);
}

async function callOpenAI({ prompt, attachments, context, model }) {
  const config = await readConfig();
  const key = process.env.OPENAI_API_KEY || config.openaiApiKey;
  if (!key) throw new Error("OPENAI_API_KEY no configurada.");
  const content = [{ type: "input_text", text: `${prompt}\n\nAdjuntos:\n${attachmentSummary(attachments)}` }];
  for (const file of attachments || []) {
    if (file.kind === "image" && file.dataUrl) content.push({ type: "input_image", image_url: file.dataUrl });
  }

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}` },
    body: JSON.stringify({
      model: model || process.env.OPENAI_MODEL || config.openaiModel || "gpt-4.1-mini",
      input: [
        { role: "system", content: buildSystemPrompt(context) },
        { role: "user", content },
      ],
      temperature: 0.2,
    }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || `OpenAI HTTP ${response.status}`);
  const text = data.output_text || data.output?.flatMap((o) => o.content || []).map((c) => c.text).filter(Boolean).join("\n");
  return { result: normalizeAgentJson(text || ""), usage: normalizeOpenAIUsage(data.usage) };
}

async function callGemini({ prompt, attachments, context, model }) {
  const config = await readConfig();
  const key = process.env.GEMINI_API_KEY || config.geminiApiKey;
  if (!key) throw new Error("GEMINI_API_KEY no configurada.");
  const parts = [{ text: `${buildSystemPrompt(context)}\n\nSolicitud del usuario:\n${prompt}\n\nAdjuntos:\n${attachmentSummary(attachments)}` }];
  for (const file of attachments || []) {
    if (file.kind === "image" && file.base64) parts.push({ inlineData: { mimeType: file.type || "image/jpeg", data: file.base64 } });
  }
  const geminiModel = model || process.env.GEMINI_MODEL || config.geminiModel || "gemini-1.5-pro";
  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${geminiModel}:generateContent?key=${key}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ role: "user", parts }],
      generationConfig: { temperature: 0.2, responseMimeType: "application/json" },
    }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || `Gemini HTTP ${response.status}`);
  const text = data.candidates?.[0]?.content?.parts?.map((part) => part.text).join("\n") || "";
  return { result: normalizeAgentJson(text), usage: normalizeGeminiUsage(data.usageMetadata) };
}

function stripMarkdownEnvelope(text) {
  const trimmed = String(text || "").trim();
  const fenced = trimmed.match(/^```(?:markdown|md)?\s*\n([\s\S]*?)\n```$/i);
  return fenced ? fenced[1].trim() : trimmed;
}

function fallbackMdEdit({ path: filePath, content, prompt }) {
  const date = new Date().toISOString().slice(0, 10);
  const entry = [
    "",
    `## Aprendizaje IA local - ${date}`,
    "",
    `- Archivo: ${filePath}`,
    `- Instruccion recibida: ${String(prompt || "").trim()}`,
    "- Criterio: revisar, concretar y conservar este aprendizaje dentro del contexto del presupuestador.",
    "",
  ].join("\n");
  return `${String(content || "").trim()}\n${entry}`.trim() + "\n";
}

function buildMdEditPrompt({ filePath, content, instruction }) {
  return `Edita el siguiente archivo de contexto del presupuestador.

Objetivo: interiorizar el aprendizaje o criterio indicado por el usuario para que futuros presupuestos usen mejor este contexto.

Reglas:
- Devuelve SOLO el contenido completo final del archivo Markdown/YAML/JSON, sin explicaciones ni cercas de codigo.
- Conserva la estructura y el estilo del archivo.
- Integra la instruccion como criterio reutilizable, accionable y claro.
- No inventes precios, proveedores ni normas si no aparecen en la instruccion o en el archivo.
- Si el archivo no es Markdown, respeta su formato original.

Archivo: ${filePath}

Instruccion del usuario:
${instruction}

Contenido actual:
${content}`;
}

async function callOpenAIText({ prompt, context, model }) {
  const config = await readConfig();
  const key = process.env.OPENAI_API_KEY || config.openaiApiKey;
  if (!key) throw new Error("OPENAI_API_KEY no configurada.");
  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}` },
    body: JSON.stringify({
      model: model || process.env.OPENAI_MODEL || config.openaiModel || "gpt-4.1-mini",
      input: [
        { role: "system", content: `Eres un editor tecnico de archivos de contexto del presupuestador. Contexto disponible:\n${context.map((doc) => `\n--- ${doc.path} ---\n${doc.content}`).join("\n")}` },
        { role: "user", content: prompt },
      ],
      temperature: 0.15,
    }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || `OpenAI HTTP ${response.status}`);
  const text = data.output_text || data.output?.flatMap((o) => o.content || []).map((c) => c.text).filter(Boolean).join("\n");
  return { content: stripMarkdownEnvelope(text), usage: normalizeOpenAIUsage(data.usage) };
}

async function callGeminiText({ prompt, context, model }) {
  const config = await readConfig();
  const key = process.env.GEMINI_API_KEY || config.geminiApiKey;
  if (!key) throw new Error("GEMINI_API_KEY no configurada.");
  const geminiModel = model || process.env.GEMINI_MODEL || config.geminiModel || "gemini-1.5-pro";
  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${geminiModel}:generateContent?key=${key}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ role: "user", parts: [{ text: `Eres un editor tecnico de archivos de contexto del presupuestador.\n\nContexto disponible:\n${context.map((doc) => `\n--- ${doc.path} ---\n${doc.content}`).join("\n")}\n\n${prompt}` }] }],
      generationConfig: { temperature: 0.15 },
    }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || `Gemini HTTP ${response.status}`);
  const text = data.candidates?.[0]?.content?.parts?.map((part) => part.text).join("\n") || "";
  return { content: stripMarkdownEnvelope(text), usage: normalizeGeminiUsage(data.usageMetadata) };
}
function slugify(text) {
  return String(text || "presupuesto")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 64) || "presupuesto";
}

async function nextBudgetCode() {
  const year = new Date().getFullYear();
  const dir = path.join(ROOT, "presupuestos");
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const max = entries
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name.match(new RegExp(`^P-${year}-(\\d{4})`)))
    .filter(Boolean)
    .map((match) => Number(match[1]))
    .reduce((a, b) => Math.max(a, b), 0);
  return `P-${year}-${String(max + 1).padStart(4, "0")}`;
}

function htmlEscape(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function totalOf(lines) {
  return (lines || []).reduce((sum, line) => sum + Number(line.importe || 0), 0);
}

function budgetMarkdown(payload, code) {
  const lines = payload.lineas || [];
  const total = totalOf(lines);
  const client = payload.cliente || {};
  return `# ${code} ${payload.titulo || "Presupuesto"}

Fecha: ${new Date().toISOString().slice(0, 10)}
Origen: presupuestador-app

## Cliente

- Nombre: ${client.nombre || ""}
- Email: ${client.email || ""}
- Telefono: ${client.telefono || ""}
- Direccion/obra: ${client.direccion || ""}
- NIF/CIF: ${client.nif || ""}
- Referencia interna: ${client.referencia || ""}

## Resumen

${payload.resumen || ""}

## Lineas del compuesto

| ID | Capitulo | Concepto | Cantidad | Unidad | Precio unitario | Importe | Confianza |
|---|---|---|---:|---|---:|---:|---|
${lines.map((line) => `| ${line.id || ""} | ${line.capitulo || ""} | ${line.concepto || ""} | ${line.cantidad || 0} | ${line.unidad || ""} | ${Number(line.precioUnitario || 0).toFixed(2)} | ${Number(line.importe || 0).toFixed(2)} | ${line.confianza || ""} |`).join("\n")}

**Total estimado:** ${total.toFixed(2)} EUR + IVA

## Supuestos

${(payload.supuestos || []).map((item) => `- ${item}`).join("\n")}

## Riesgos

${(payload.riesgos || []).map((item) => `- ${item}`).join("\n")}

## Preguntas pendientes

${(payload.preguntas || []).map((item) => `- ${item}`).join("\n")}

## Sugerencias generadas

${(payload.sugerencias || []).map((item) => `- **${item.titulo || "Sugerencia"}:** ${item.detalle || ""}`).join("\n")}
`;
}

function budgetHtml(payload, code) {
  const lines = payload.lineas || [];
  const client = payload.cliente || {};
  const total = totalOf(lines);
  return `<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>${htmlEscape(code)} ${htmlEscape(payload.titulo || "Presupuesto")}</title>
  <style>
    @page { size: A4; margin: 16mm; }
    body { font-family: Arial, Helvetica, sans-serif; color: #1d242c; margin: 0; line-height: 1.42; }
    header { border-top: 7px solid #16202a; padding-top: 16px; display: flex; justify-content: space-between; gap: 24px; }
    h1 { margin: 0 0 8px; font-size: 26px; color: #16202a; }
    h2 { margin-top: 22px; font-size: 17px; color: #16202a; }
    p { color: #4b5563; }
    .meta { text-align: right; font-size: 13px; color: #4b5563; }
    .box { border: 1px solid #d6dde5; background: #f6f8fa; padding: 12px; margin-top: 14px; }
    table { width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 12px; }
    th { background: #16202a; color: white; text-align: left; padding: 8px; }
    td { border-bottom: 1px solid #d6dde5; padding: 8px; vertical-align: top; }
    .num { text-align: right; white-space: nowrap; }
    .total { margin-top: 18px; text-align: right; font-size: 20px; font-weight: 700; }
    ul { padding-left: 18px; }
    button { margin-top: 18px; padding: 10px 14px; border: 0; background: #16202a; color: white; border-radius: 6px; font-weight: 700; }
    @media print { .no-print { display: none; } }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>${htmlEscape(payload.titulo || "Presupuesto")}</h1>
      <p>${htmlEscape(payload.resumen || "")}</p>
    </div>
    <div class="meta"><strong>${htmlEscape(code)}</strong><br>${new Date().toISOString().slice(0, 10)}</div>
  </header>
  <section class="box">
    <strong>Cliente:</strong> ${htmlEscape(client.nombre || "")}<br>
    <strong>Email:</strong> ${htmlEscape(client.email || "")} | <strong>Tel.:</strong> ${htmlEscape(client.telefono || "")}<br>
    <strong>Obra:</strong> ${htmlEscape(client.direccion || "")}<br>
    <strong>NIF/CIF:</strong> ${htmlEscape(client.nif || "")} | <strong>Referencia:</strong> ${htmlEscape(client.referencia || "")}
  </section>
  <h2>Partidas</h2>
  <table>
    <thead><tr><th>Capitulo</th><th>Concepto</th><th class="num">Cant.</th><th>Ud.</th><th class="num">EUR/Ud.</th><th class="num">Importe</th></tr></thead>
    <tbody>${lines.map((line) => `<tr><td>${htmlEscape(line.capitulo)}</td><td><strong>${htmlEscape(line.concepto)}</strong><br>${htmlEscape(line.descripcion)}</td><td class="num">${Number(line.cantidad || 0).toFixed(2)}</td><td>${htmlEscape(line.unidad)}</td><td class="num">${Number(line.precioUnitario || 0).toFixed(2)}</td><td class="num">${Number(line.importe || 0).toFixed(2)}</td></tr>`).join("")}</tbody>
  </table>
  <div class="total">Total estimado: ${total.toFixed(2)} EUR + IVA</div>
  <h2>Supuestos</h2>
  <ul>${(payload.supuestos || []).map((item) => `<li>${htmlEscape(item)}</li>`).join("")}</ul>
  <h2>Riesgos y datos pendientes</h2>
  <ul>${[...(payload.riesgos || []), ...(payload.preguntas || [])].map((item) => `<li>${htmlEscape(item)}</li>`).join("")}</ul>
  <button class="no-print" onclick="window.print()">Imprimir / PDF</button>
</body>
</html>`;
}

async function listBudgets() {
  const budgetsDir = path.join(ROOT, "presupuestos");
  const entries = await fs.readdir(budgetsDir, { withFileTypes: true });
  const budgets = [];
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const match = entry.name.match(/^P-(\d{4})-(\d{4})(?:-(.*))?$/);
    if (!match) continue;
    const folder = path.join(budgetsDir, entry.name);
    const files = await fs.readdir(folder, { withFileTypes: true });
    const fileNames = files.filter((file) => file.isFile()).map((file) => file.name).sort();
    const readme = path.join(folder, "README.md");
    let title = (match[3] || entry.name).replaceAll("-", " ");
    let client = {};
    let budgetData = null;
    if (await fileExists(readme)) {
      const content = await fs.readFile(readme, "utf8");
      const h1 = content.match(/^#\s+(.+)$/m);
      if (h1) title = h1[1].replace(/^P-\d{4}-\d{4}\s*/, "").trim() || title;
    }
    const dataFile = path.join(folder, "datos.json");
    if (await fileExists(dataFile)) {
      try {
        const data = JSON.parse(await fs.readFile(dataFile, "utf8"));
        budgetData = data;
        client = data.cliente || {};
        if (data.titulo) title = data.titulo;
      } catch {
        client = {};
      }
    }
    const code = `P-${match[1]}-${match[2]}`;
    if (budgetData) saveBudgetRecord({ folder, code, payload: budgetData, htmlPath: `presupuestos/${entry.name}/presupuesto-final.html` });
    budgets.push({
      code,
      year: match[1],
      number: Number(match[2]),
      title,
      clientName: client.nombre || "",
      folder: `presupuestos/${entry.name}`,
      files: fileNames.map((name) => ({
        name,
        url: `/presupuestos/${encodeURIComponent(entry.name)}/${encodeURIComponent(name)}`,
        kind: path.extname(name).slice(1).toLowerCase() || "file",
      })),
      hasFinalHtml: fileNames.includes("presupuesto-final.html") || fileNames.includes("presupuesto-cliente.html"),
      editable: fileNames.includes("datos.json"),
      updatedAt: (await fs.stat(folder)).mtime.toISOString(),
    });
  }
  budgets.sort((a, b) => b.year.localeCompare(a.year) || b.number - a.number);
  const years = [...new Set(budgets.map((budget) => budget.year))].sort((a, b) => b.localeCompare(a));
  return { years, budgets };
}

function resolveBudgetFolder(relativeFolder) {
  const normalized = String(relativeFolder || "").replaceAll("\\", "/");
  if (!/^presupuestos\/P-\d{4}-\d{4}/.test(normalized)) throw new Error("Carpeta de presupuesto no permitida.");
  if (normalized.includes("..")) throw new Error("Carpeta de presupuesto no permitida.");
  const full = path.resolve(ROOT, normalized);
  const budgetsRoot = path.resolve(ROOT, "presupuestos");
  if (!full.startsWith(budgetsRoot)) throw new Error("Carpeta de presupuesto no permitida.");
  return full;
}

async function readBudgetData(relativeFolder) {
  const folder = resolveBudgetFolder(relativeFolder);
  const relFolder = path.relative(ROOT, folder).replaceAll("\\", "/");
  const dbRecord = getBudgetRecord(relFolder);
  const folderName = path.basename(folder);
  const code = dbRecord?.code || folderName.match(/^(P-\d{4}-\d{4})/)?.[1] || "";
  if (dbRecord?.data_json) return { folder: relFolder, code, data: JSON.parse(dbRecord.data_json), source: "sqlite" };
  const dataFile = path.join(folder, "datos.json");
  if (!(await fileExists(dataFile))) throw new Error("Este presupuesto no tiene datos.json editable.");
  const data = JSON.parse(await fs.readFile(dataFile, "utf8"));
  saveBudgetRecord({ folder, code, payload: data, htmlPath: `${relFolder}/presupuesto-final.html` });
  return { folder: relFolder, code, data, source: "file" };
}
function resolveBudgetAsset(urlPath) {
  const prefix = "/presupuestos/";
  if (!urlPath.startsWith(prefix)) throw new Error("Ruta de presupuesto no permitida.");
  const parts = urlPath.slice(prefix.length).split("/").map((part) => decodeURIComponent(part));
  if (parts.some((part) => part.includes("..") || part.includes("\\"))) throw new Error("Ruta de presupuesto no permitida.");
  const full = path.resolve(ROOT, "presupuestos", ...parts);
  const budgetsRoot = path.resolve(ROOT, "presupuestos");
  if (!full.startsWith(budgetsRoot)) throw new Error("Ruta de presupuesto no permitida.");
  return full;
}
function summarizeChangeForLearning(change) {
  const source = change.source || "manual";
  if (change.action === "edit-field") {
    const line = change.line || {};
    return `- ${source}: ${line.capitulo || "Linea"} / ${line.concepto || "sin concepto"}: campo ${change.field} cambio de "${change.from ?? ""}" a "${change.to ?? ""}". Importe resultante ${line.importe ?? ""}.`;
  }
  if (change.action === "edit-line") {
    const before = change.before || {};
    const after = change.after || {};
    return `- ${source}: ${after.capitulo || before.capitulo || "Linea"} / ${after.concepto || before.concepto || "sin concepto"}: IA aplicada con prompt "${change.prompt || ""}". Antes: cant. ${before.cantidad ?? ""}, precio ${before.precioUnitario ?? ""}, importe ${before.importe ?? ""}. Despues: cant. ${after.cantidad ?? ""}, precio ${after.precioUnitario ?? ""}, importe ${after.importe ?? ""}.`;
  }
  if (change.action === "add-line") {
    const line = change.after || {};
    return `- ${source}: linea anadida ${line.capitulo || ""} / ${line.concepto || ""}, cant. ${line.cantidad ?? ""}, precio ${line.precioUnitario ?? ""}, importe ${line.importe ?? ""}.`;
  }
  if (change.action === "delete-line") {
    const line = change.before || {};
    return `- ${source}: linea eliminada ${line.capitulo || ""} / ${line.concepto || ""}, cant. ${line.cantidad ?? ""}, precio ${line.precioUnitario ?? ""}, importe ${line.importe ?? ""}.`;
  }
  return `- ${source}: ${JSON.stringify(change).slice(0, 500)}`;
}

async function appendBudgetLearning(payload, code, changeLog = []) {
  const usefulChanges = (Array.isArray(changeLog) ? changeLog : [])
    .filter((change) => change && change.source !== "generacion")
    .slice(-80);
  if (!usefulChanges.length) return null;
  const exists = await fileExists(LEARNING_FILE);
  if (!exists) {
    await fs.writeFile(LEARNING_FILE, "# Skill: Aprendizaje del Presupuestador App\n\nCriterios aceptados desde la interfaz local de presupuestacion.\n", "utf8");
  }
  const total = (payload.lineas || []).reduce((sum, line) => sum + Number(line.importe || 0), 0);
  const lines = usefulChanges.map(summarizeChangeForLearning).join("\n");
  const entry = `\n## ${new Date().toISOString().slice(0, 10)} - Aprendizaje desde presupuesto ${code}\n\n- Presupuesto: ${payload.titulo || "Sin titulo"}\n- Cliente/obra: ${payload.cliente?.nombre || ""} ${payload.cliente?.direccion ? `- ${payload.cliente.direccion}` : ""}\n- Total final guardado: ${total.toFixed(2)} EUR + IVA\n- Origen: cambios reales realizados durante edicion y guardado del presupuesto.\n\n### Cambios observados\n${lines}\n\n### Criterio de uso futuro\n- Al presupuestar trabajos similares, revisar estas correcciones antes de cerrar cantidades, precios unitarios, capitulos y partidas omitidas.\n`;
  await fs.appendFile(LEARNING_FILE, entry, "utf8");
  return path.relative(ROOT, LEARNING_FILE).replaceAll("\\", "/");
}
async function appendLearning({ suggestion, note }) {
  const exists = await fileExists(LEARNING_FILE);
  if (!exists) {
    await fs.writeFile(LEARNING_FILE, "# Skill: Aprendizaje del Presupuestador App\n\nCriterios aceptados desde la interfaz local de presupuestacion.\n", "utf8");
  }
  const entry = `\n## ${new Date().toISOString().slice(0, 10)} - ${suggestion?.titulo || "Aprendizaje"}\n\n- Prioridad: ${suggestion?.prioridad || "media"}\n- Criterio: ${suggestion?.detalle || note || ""}\n- Origen: sugerencia aceptada en presupuestador-app\n`;
  await fs.appendFile(LEARNING_FILE, entry, "utf8");
  return path.relative(ROOT, LEARNING_FILE).replaceAll("\\", "/");
}

async function route(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (BASE_PATH && req.method === "GET" && url.pathname === BASE_PATH) {
    res.writeHead(308, { Location: `${BASE_PATH}/` });
    res.end();
    return;
  }
  const appPath = stripBasePath(url.pathname);
  if (appPath) url.pathname = appPath;
  if (req.method === "GET" && url.pathname === "/api/budgets") return send(res, 200, await listBudgets());
  if (req.method === "GET" && url.pathname === "/api/budget") return send(res, 200, await readBudgetData(url.searchParams.get("folder")));
  if (req.method === "GET" && url.pathname === "/api/context") {
    const context = await loadRepositoryContext();
    return send(res, 200, { files: context.map((doc) => doc.path) });
  }
  if (req.method === "GET" && url.pathname === "/api/settings") return send(res, 200, maskedConfig(await readConfig()));
  if (req.method === "GET" && url.pathname === "/api/db/status") return send(res, 200, dbStatus());
  if (req.method === "POST" && url.pathname === "/api/settings") return send(res, 200, await writeConfig(await readJson(req)));
  if (req.method === "GET" && url.pathname === "/api/models") {
    const provider = url.searchParams.get("provider") || "fallback";
    const config = await readConfig();
    let models = fallbackModels(provider);
    try {
      if (provider === "openai") models = await listOpenAIModels(config);
      if (provider === "gemini") models = await listGeminiModels(config);
    } catch (error) {
      models = fallbackModels(provider).map((model) => ({ ...model, error: error.message }));
    }
    const entries = await readTokenUsage();
    models = await Promise.all(models.map(async (model) => {
      const budget = Number(config.modelTokenBudgets?.[provider]?.[model.id] || 0);
      const used = usedTokensFor(entries, provider, model.id);
      return { ...model, localBudgetTokens: budget || null, usedTokens: used, remainingTokens: budget > 0 ? Math.max(0, budget - used) : null };
    }));
    return send(res, 200, { provider, models });
  }
  if (req.method === "POST" && url.pathname === "/api/token-status") {
    const body = await readJson(req);
    const estimate = estimateRequestTokens(body.prompt || "", body.attachments || []);
    return send(res, 200, await modelStatus(body.provider || "fallback", body.model || "fallback", estimate));
  }
  if (req.method === "GET" && url.pathname === "/api/md") return send(res, 200, { files: await listEditableFiles() });
  if (req.method === "GET" && url.pathname === "/api/md/read") {
    const file = resolveEditable(url.searchParams.get("path"));
    return send(res, 200, { path: path.relative(ROOT, file).replaceAll("\\", "/"), content: await fs.readFile(file, "utf8") });
  }
  if (req.method === "POST" && url.pathname === "/api/md/write") {
    const body = await readJson(req);
    const file = resolveEditable(body.path);
    await fs.writeFile(file, String(body.content || ""), "utf8");
    return send(res, 200, { ok: true, path: path.relative(ROOT, file).replaceAll("\\", "/") });
  }
  if (req.method === "POST" && url.pathname === "/api/md/ai") {
    const body = await readJson(req);
    const file = resolveEditable(body.path);
    const relativePath = path.relative(ROOT, file).replaceAll("\\", "/");
    const currentContent = String(body.content ?? await fs.readFile(file, "utf8"));
    const instruction = String(body.prompt || "").trim();
    if (!instruction) return send(res, 400, { error: "Falta instruccion para editar el contexto." });
    const context = await loadRepositoryContext();
    const provider = body.provider || "fallback";
    const model = body.model || "fallback";
    const mdPrompt = buildMdEditPrompt({ filePath: relativePath, content: currentContent, instruction });
    const estimatedTokens = estimateRequestTokens(mdPrompt, []);
    const status = await modelStatus(provider, model, estimatedTokens);
    if (provider !== "fallback" && status.blocked) {
      return send(res, 402, { error: "Saldo local insuficiente para este modelo.", tokenStatus: status });
    }
    let content;
    let usage = null;
    try {
      if (provider === "openai") {
        const response = await callOpenAIText({ prompt: mdPrompt, context, model });
        content = response.content;
        usage = response.usage;
      } else if (provider === "gemini") {
        const response = await callGeminiText({ prompt: mdPrompt, context, model });
        content = response.content;
        usage = response.usage;
      } else {
        content = fallbackMdEdit({ path: relativePath, content: currentContent, prompt: instruction });
      }
      await recordTokenUsage(provider, model, usage);
      return send(res, 200, { provider, model, path: relativePath, content, usage, tokenStatus: await modelStatus(provider, model, estimatedTokens) });
    } catch (error) {
      content = fallbackMdEdit({ path: relativePath, content: currentContent, prompt: instruction });
      return send(res, 200, { provider: "fallback", warning: error.message, path: relativePath, content, usage: null, tokenStatus: status });
    }
  }
  if (req.method === "POST" && url.pathname === "/api/line-ai") {
    const body = await readJson(req);
    const context = await loadRepositoryContext();
    const provider = body.provider || "fallback";
    const model = body.model || "fallback";
    const budget = body.budget || {};
    const lineIndex = Number(body.lineIndex || 0);
    const linePrompt = buildLinePrompt({ prompt: body.prompt || "", budget, lineIndex });
    const estimatedTokens = estimateRequestTokens(linePrompt, []);
    const status = await modelStatus(provider, model, estimatedTokens);
    if (provider !== "fallback" && status.blocked) {
      return send(res, 402, { error: "Saldo local insuficiente para este modelo.", tokenStatus: status });
    }
    let result;
    let usage = null;
    try {
      if (provider === "openai") {
        const response = await callOpenAI({ prompt: linePrompt, attachments: [], context, model });
        result = response.result;
        usage = response.usage;
      } else if (provider === "gemini") {
        const response = await callGemini({ prompt: linePrompt, attachments: [], context, model });
        result = response.result;
        usage = response.usage;
      } else {
        result = fallbackLineEdit({ prompt: body.prompt || "", budget, lineIndex });
      }
      await recordTokenUsage(provider, model, usage);
      return send(res, 200, { provider, model, result, usage, tokenStatus: await modelStatus(provider, model, estimatedTokens) });
    } catch (error) {
      result = fallbackLineEdit({ prompt: body.prompt || "", budget, lineIndex });
      return send(res, 200, { provider: "fallback", warning: error.message, result, usage: null, tokenStatus: status });
    }
  }
  if (req.method === "POST" && url.pathname === "/api/generate") {
    const body = await readJson(req);
    const context = await loadRepositoryContext();
    const provider = body.provider || "fallback";
    const model = body.model || "fallback";
    const estimatedTokens = estimateRequestTokens(body.prompt || "", body.attachments || []);
    const status = await modelStatus(provider, model, estimatedTokens);
    if (provider !== "fallback" && status.blocked) {
      return send(res, 402, { error: "Saldo local insuficiente para este modelo.", tokenStatus: status });
    }
    let result;
    let usage = null;
    try {
      if (provider === "openai") {
        const response = await callOpenAI({ ...body, context });
        result = response.result;
        usage = response.usage;
      } else if (provider === "gemini") {
        const response = await callGemini({ ...body, context });
        result = response.result;
        usage = response.usage;
      } else {
        result = fallbackEstimate(body.prompt || "", body.attachments || []);
      }
      await recordTokenUsage(provider, model, usage);
      return send(res, 200, { provider, model, result, usage, tokenStatus: await modelStatus(provider, model, estimatedTokens) });
    } catch (error) {
      result = fallbackEstimate(body.prompt || "", body.attachments || []);
      return send(res, 200, { provider: "fallback", warning: error.message, result, usage: null, tokenStatus: status });
    }
  }
  if (req.method === "POST" && url.pathname === "/api/learn") {
    const file = await appendLearning(await readJson(req));
    return send(res, 200, { ok: true, file });
  }
  if (req.method === "POST" && url.pathname === "/api/export") {
    const body = await readJson(req);
    const editing = Boolean(body._folder);
    const folder = editing ? resolveBudgetFolder(body._folder) : path.join(ROOT, "presupuestos", `${await nextBudgetCode()}-${slugify(body.titulo)}`);
    const code = path.basename(folder).match(/^(P-\d{4}-\d{4})/)?.[1] || await nextBudgetCode();
    const cleanBody = { ...body };
    const changeLog = Array.isArray(cleanBody._changeLog) ? cleanBody._changeLog : [];
    delete cleanBody._folder;
    delete cleanBody._changeLog;
    await fs.mkdir(folder, { recursive: true });
    await fs.writeFile(path.join(folder, "README.md"), budgetMarkdown(cleanBody, code), "utf8");
    await fs.writeFile(path.join(folder, "presupuesto-final.html"), budgetHtml(cleanBody, code), "utf8");
    await fs.writeFile(path.join(folder, "datos.json"), JSON.stringify(cleanBody, null, 2), "utf8");
    const rel = saveBudgetRecord({ folder, code, payload: cleanBody, htmlPath: `${path.relative(ROOT, folder).replaceAll("\\", "/")}/presupuesto-final.html` });
    const learningFile = await appendBudgetLearning(cleanBody, code, changeLog);
    return send(res, 200, { ok: true, updated: editing, folder: rel, code, html: `${rel}/presupuesto-final.html`, learningFile, db: "sqlite" });
  }

  if (req.method === "GET" && url.pathname.startsWith("/presupuestos/")) {
    const asset = resolveBudgetAsset(url.pathname);
    if (!(await fileExists(asset))) return send(res, 404, "Not found", "text/plain; charset=utf-8");
    const content = await fs.readFile(asset);
    return send(res, 200, content, MIME[path.extname(asset)] || "application/octet-stream");
  }

  const requested = url.pathname === "/" ? "/index.html" : url.pathname;
  const target = path.resolve(PUBLIC_DIR, `.${requested}`);
  if (!target.startsWith(PUBLIC_DIR)) return send(res, 403, "Forbidden", "text/plain; charset=utf-8");
  if (!(await fileExists(target))) return send(res, 404, "Not found", "text/plain; charset=utf-8");
  const content = await fs.readFile(target);
  send(res, 200, content, MIME[path.extname(target)] || "application/octet-stream");
}

const server = http.createServer((req, res) => {
  route(req, res).catch((error) => {
    console.error(error);
    send(res, 500, { error: error.message });
  });
});

server.listen(PORT, () => {
  console.log(`Presupuestador app: http://localhost:${PORT}`);
});

