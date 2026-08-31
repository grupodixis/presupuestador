const http = require("http");
const fs = require("fs/promises");
const fsSync = require("fs");
const path = require("path");
const crypto = require("crypto");
const { DatabaseSync } = require("node:sqlite");

const PORT = Number(process.env.PORT || 4177);
const HOST = String(process.env.HOST || "127.0.0.1");
const BASE_PATH = normalizeBasePath(process.env.BASE_PATH || "");
const ROOT = path.resolve(__dirname, "..");
const PUBLIC_DIR = path.join(__dirname, "public");
const CONFIG_FILE = path.join(__dirname, "config.local.json");
const TOKEN_USAGE_FILE = path.join(__dirname, "token-usage.local.json");
const DB_DIR = path.join(__dirname, "data");
const DB_FILE = path.join(DB_DIR, "presupuestador.sqlite");
const SESSION_DAYS = 7;
const FAL_IMAGE_MODEL = "fal-ai/flux/schnell";
const FAL_IMAGE_SIZE = "square";
const FAL_IMAGE_STEPS = 1;
const FAL_IMAGE_ACCELERATION = "none";
const DEFAULT_PROVIDER = "gemini";
const DEFAULT_GEMINI_MODEL = "gemini-3.5-flash";
const LEARNING_DIR = path.join(ROOT, "skills", "aprendizaje");
const LEARNING_STATE_FILE = path.join(LEARNING_DIR, "estado_consolidacion.json");
const LEARNING_RULES_FILE = path.join(LEARNING_DIR, "00_reglas_consolidadas.md");
const LEARNING_RECENT_FILE = path.join(LEARNING_DIR, "00_memoria_reciente.md");
const LEARNING_FILES = {
  general: "aprendizaje_general.md",
  aluminio: "aprendizaje_aluminio.md",
  carpinteria_metalica: "aprendizaje_carpinteria_metalica.md",
  instalaciones_electricas: "aprendizaje_instalaciones_electricas.md",
  fontaneria: "aprendizaje_fontaneria.md",
  clima: "aprendizaje_clima.md",
  otras_industrias: "aprendizaje_otras_industrias.md",
};
const EDITABLE_DIRS = ["skills", "presupuestacion", "productos", "plantillas", "proveedores", "glosario"];
const EDITABLE_EXTENSIONS = new Set([".md", ".yaml", ".yml", ".json"]);
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
const ALUFAC_DOCUMENT_TEMPLATE = {
  logo: "https://alufac.es/assets/alufac-logo.svg",
  headerText: [
    "ALUFAC",
    "Carpinteria de aluminio, PVC, cristal y cerramientos a medida en Menorca.",
    "Circunval·lacio, 11, 07710 Sant Lluis, Menorca",
    "info@alufac.es - +34 669 769 541 - WhatsApp +34 669 769 541",
    "www.alufac.es",
  ].join("\n"),
  footerText: DEFAULT_DOCUMENT_TEMPLATE.footerText,
};

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
    CREATE TABLE IF NOT EXISTS app_users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      role TEXT NOT NULL DEFAULT 'user',
      active INTEGER NOT NULL DEFAULT 1,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS app_sessions (
      token TEXT PRIMARY KEY,
      user_id INTEGER NOT NULL,
      expires_at TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES app_users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS price_items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      category TEXT NOT NULL,
      area TEXT NOT NULL DEFAULT 'general',
      name TEXT NOT NULL,
      description TEXT NOT NULL DEFAULT '',
      unit TEXT NOT NULL DEFAULT 'ud',
      cost_price REAL NOT NULL DEFAULT 0,
      sale_price REAL NOT NULL DEFAULT 0,
      margin_percent REAL NOT NULL DEFAULT 0,
      supplier TEXT NOT NULL DEFAULT '',
      confidence TEXT NOT NULL DEFAULT 'confirmado',
      notes TEXT NOT NULL DEFAULT '',
      active INTEGER NOT NULL DEFAULT 1,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
  `);
  ensureDefaultAdminUser();
  cleanupExpiredSessions();
  return database;
}

function hashPassword(password, salt = crypto.randomBytes(16).toString("hex")) {
  const hash = crypto.pbkdf2Sync(String(password || ""), salt, 120000, 32, "sha256").toString("hex");
  return `${salt}:${hash}`;
}

function verifyPassword(password, stored) {
  const [salt, hash] = String(stored || "").split(":");
  if (!salt || !hash) return false;
  const candidate = hashPassword(password, salt).split(":")[1];
  try { return crypto.timingSafeEqual(Buffer.from(hash, "hex"), Buffer.from(candidate, "hex")); } catch { return false; }
}

function ensureDefaultAdminUser() {
  const row = database.prepare("SELECT COUNT(*) AS count FROM app_users").get();
  if (row.count > 0) return;
  const username = String(process.env.INITIAL_ADMIN_USERNAME || "admin").trim().toLowerCase();
  const password = String(process.env.INITIAL_ADMIN_PASSWORD || "");
  if (!/^[a-z0-9._-]{3,40}$/.test(username)) {
    throw new Error("INITIAL_ADMIN_USERNAME invalido. Usa 3-40 caracteres seguros.");
  }
  if (password.length < 12) {
    throw new Error("Base de datos sin usuarios. Define INITIAL_ADMIN_PASSWORD con al menos 12 caracteres antes de arrancar.");
  }
  const now = new Date().toISOString();
  database.prepare("INSERT INTO app_users (username, password_hash, role, active, created_at, updated_at) VALUES (?, ?, ?, 1, ?, ?)")
    .run(username, hashPassword(password), "admin", now, now);
}

function cleanupExpiredSessions() {
  if (!database) return 0;
  return Number(database.prepare("DELETE FROM app_sessions WHERE expires_at <= ?").run(new Date().toISOString()).changes || 0);
}

function publicUser(user) {
  if (!user) return null;
  return { id: user.id, username: user.username, role: user.role, active: Boolean(user.active) };
}

function parseCookies(req) {
  const out = {};
  for (const part of String(req.headers.cookie || "").split(";")) {
    const index = part.indexOf("=");
    if (index === -1) continue;
    out[part.slice(0, index).trim()] = decodeURIComponent(part.slice(index + 1).trim());
  }
  return out;
}

function sessionCookie(token, req) {
  const host = String(req.headers.host || "");
  const isLocal = host.includes("localhost") || host.startsWith("127.0.0.1") || host.startsWith("[::1]");
  const secure = req.headers["x-forwarded-proto"] === "https" || !isLocal;
  return [`ps_session=${encodeURIComponent(token)}`, "Path=/", "HttpOnly", "SameSite=Lax", `Max-Age=${SESSION_DAYS * 86400}`, secure ? "Secure" : ""].filter(Boolean).join("; ");
}

function clearSessionCookie() {
  return "ps_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0";
}

function currentUser(req) {
  const token = parseCookies(req).ps_session;
  if (!token) return null;
  const row = db().prepare(`SELECT u.id, u.username, u.role, u.active, s.expires_at FROM app_sessions s JOIN app_users u ON u.id = s.user_id WHERE s.token = ?`).get(token);
  if (!row || !row.active || new Date(row.expires_at) <= new Date()) {
    if (row) db().prepare("DELETE FROM app_sessions WHERE token = ?").run(token);
    return null;
  }
  return row;
}

function requireAdmin(user) {
  if (!user || user.role !== "admin") {
    const error = new Error("Permiso denegado. Requiere administrador.");
    error.statusCode = 403;
    throw error;
  }
}

function listUsers() {
  return db().prepare("SELECT id, username, role, active, created_at, updated_at FROM app_users ORDER BY username COLLATE NOCASE").all()
    .map((user) => ({ ...user, active: Boolean(user.active) }));
}

function createUser({ username, password, role = "user", active = true }) {
  const clean = String(username || "").trim().toLowerCase();
  if (!/^[a-z0-9._-]{3,40}$/.test(clean)) throw new Error("Usuario invalido. Usa 3-40 caracteres: letras, numeros, punto, guion o guion bajo.");
  if (String(password || "").length < 12) throw new Error("La contraseña debe tener al menos 12 caracteres.");
  const safeRole = role === "admin" ? "admin" : "user";
  const now = new Date().toISOString();
  db().prepare("INSERT INTO app_users (username, password_hash, role, active, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)")
    .run(clean, hashPassword(password), safeRole, active ? 1 : 0, now, now);
  return listUsers();
}

function updateUser(id, patch) {
  const userId = Number(id);
  const current = db().prepare("SELECT * FROM app_users WHERE id = ?").get(userId);
  if (!current) throw new Error("Usuario no encontrado.");
  const role = patch.role === "admin" ? "admin" : "user";
  const active = patch.active === false ? 0 : 1;
  if (current.role === "admin" && (role !== "admin" || !active)) {
    const admins = db().prepare("SELECT COUNT(*) AS count FROM app_users WHERE role = 'admin' AND active = 1 AND id <> ?").get(userId).count;
    if (admins === 0) throw new Error("Debe quedar al menos un administrador activo.");
  }
  const now = new Date().toISOString();
  if (patch.password) {
    if (String(patch.password).length < 12) throw new Error("La contraseña debe tener al menos 12 caracteres.");
    db().prepare("UPDATE app_users SET password_hash = ?, role = ?, active = ?, updated_at = ? WHERE id = ?")
      .run(hashPassword(patch.password), role, active, now, userId);
    db().prepare("DELETE FROM app_sessions WHERE user_id = ?").run(userId);
  } else {
    db().prepare("UPDATE app_users SET role = ?, active = ?, updated_at = ? WHERE id = ?").run(role, active, now, userId);
    if (!active) db().prepare("DELETE FROM app_sessions WHERE user_id = ?").run(userId);
  }
  return listUsers();
}

function loginPage() {
  return `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Acceso - Presupuestador IA</title><style>*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:#eef1f4;color:#16202a;font-family:Arial,Helvetica,sans-serif}form{width:min(420px,calc(100vw - 32px));background:#fff;border:1px solid #d6dde5;border-radius:8px;padding:24px;box-shadow:0 18px 45px rgba(16,24,40,.12);display:grid;gap:14px}.brand{display:flex;gap:12px;align-items:center;margin-bottom:6px}.mark{display:grid;place-items:center;width:38px;height:38px;border-radius:6px;background:#b9863a;color:white;font-weight:800}h1{margin:0;font-size:24px}p{margin:4px 0 0;color:#667085}label{display:grid;gap:6px;color:#667085;font-size:13px}input{border:1px solid #d6dde5;border-radius:6px;padding:11px;font:inherit}button{border:0;border-radius:6px;padding:11px 14px;background:#16202a;color:#fff;font-weight:700;cursor:pointer}.status{min-height:18px;color:#a33a2b;font-size:13px}</style></head><body><form id="loginForm"><div class="brand"><span class="mark">H</span><div><h1>Presupuestador IA</h1><p>Acceso privado</p></div></div><label>Usuario<input id="username" autocomplete="username" autofocus></label><label>Contraseña<input id="password" type="password" autocomplete="current-password"></label><button>Entrar</button><div id="status" class="status"></div></form><script>loginForm.addEventListener("submit",async e=>{e.preventDefault();status.textContent="Entrando...";const r=await fetch("api/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:username.value,password:password.value})});if(r.ok) location.href="./"; else status.textContent="Usuario o contraseña incorrectos.";});</script></body></html>`;
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

function normalizePriceText(value, fallback = "") {
  return String(value ?? fallback).trim();
}

function normalizePriceNumber(value) {
  const parsed = Number(String(value ?? 0).replace(",", "."));
  return Number.isFinite(parsed) ? Math.round(parsed * 10000) / 10000 : 0;
}

function normalizePriceItem(input = {}) {
  const item = {
    id: input.id ? Number(input.id) : null,
    category: normalizePriceText(input.category, "material").toLowerCase(),
    area: normalizePriceText(input.area, "general").toLowerCase(),
    name: normalizePriceText(input.name),
    description: normalizePriceText(input.description),
    unit: normalizePriceText(input.unit, "ud").toLowerCase(),
    costPrice: normalizePriceNumber(input.costPrice ?? input.cost_price),
    salePrice: normalizePriceNumber(input.salePrice ?? input.sale_price),
    marginPercent: normalizePriceNumber(input.marginPercent ?? input.margin_percent),
    supplier: normalizePriceText(input.supplier),
    confidence: normalizePriceText(input.confidence, "confirmado").toLowerCase(),
    notes: normalizePriceText(input.notes),
    active: input.active === false || input.active === 0 ? 0 : 1,
  };
  if (!item.name) throw new Error("Falta el nombre del precio.");
  if (!item.category) item.category = "material";
  if (!item.area) item.area = "general";
  if (!item.unit) item.unit = "ud";
  if (!["confirmado", "estimado", "antiguo", "pendiente"].includes(item.confidence)) item.confidence = "confirmado";
  if (!item.salePrice && item.costPrice && item.marginPercent) item.salePrice = Math.round(item.costPrice * (1 + item.marginPercent / 100) * 10000) / 10000;
  if (!item.marginPercent && item.costPrice && item.salePrice) item.marginPercent = Math.round(((item.salePrice / item.costPrice) - 1) * 10000) / 100;
  return item;
}

function priceRowToApi(row) {
  return {
    id: row.id,
    category: row.category,
    area: row.area,
    name: row.name,
    description: row.description,
    unit: row.unit,
    costPrice: Number(row.cost_price || 0),
    salePrice: Number(row.sale_price || 0),
    marginPercent: Number(row.margin_percent || 0),
    supplier: row.supplier,
    confidence: row.confidence,
    notes: row.notes,
    active: Boolean(row.active),
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function listPriceItems({ includeInactive = true } = {}) {
  const rows = db().prepare(`
    SELECT * FROM price_items
    ${includeInactive ? "" : "WHERE active = 1"}
    ORDER BY active DESC, area COLLATE NOCASE, category COLLATE NOCASE, name COLLATE NOCASE
  `).all();
  return rows.map(priceRowToApi);
}

function yamlScalar(value) {
  const text = String(value ?? "");
  if (!text) return "''";
  return `'${text.replaceAll("'", "''")}'`;
}

function priceItemsYaml(items) {
  return [
    "# Generado automaticamente desde SQLite. Editar desde Configuracion > Lista de precios.",
    `actualizado: ${yamlScalar(new Date().toISOString())}`,
    "precios:",
    ...items.map((item) => [
      `  - id: ${item.id}`,
      `    activo: ${item.active ? "true" : "false"}`,
      `    categoria: ${yamlScalar(item.category)}`,
      `    area: ${yamlScalar(item.area)}`,
      `    nombre: ${yamlScalar(item.name)}`,
      `    descripcion: ${yamlScalar(item.description)}`,
      `    unidad: ${yamlScalar(item.unit)}`,
      `    precio_coste: ${item.costPrice}`,
      `    precio_venta: ${item.salePrice}`,
      `    margen_porcentaje: ${item.marginPercent}`,
      `    proveedor: ${yamlScalar(item.supplier)}`,
      `    confianza: ${yamlScalar(item.confidence)}`,
      `    notas: ${yamlScalar(item.notes)}`,
      `    actualizado: ${yamlScalar(item.updatedAt)}`,
    ].join("\n")),
    "",
  ].join("\n");
}

function priceItemsMarkdown(items) {
  const active = items.filter((item) => item.active);
  const byArea = new Map();
  for (const item of active) {
    const key = item.area || "general";
    if (!byArea.has(key)) byArea.set(key, []);
    byArea.get(key).push(item);
  }
  const out = [
    "# Lista de precios operativa",
    "",
    "Archivo generado automaticamente desde SQLite cada vez que se actualiza un precio.",
    "Editar los precios desde `Configuracion > Lista de precios`.",
    "",
    `Actualizado: ${new Date().toISOString()}`,
    "",
    "## Uso por el agente",
    "",
    "- Priorizar estos precios frente a supuestos genericos cuando coincidan area, categoria, nombre o unidad.",
    "- Si un precio esta marcado como estimado, antiguo o pendiente, indicar la confianza y proponer validarlo.",
    "- Si no existe precio aplicable, generar la linea como supuesto y sugerir alta en lista de precios.",
    "",
  ];
  for (const [area, areaItems] of [...byArea.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
    out.push(`## ${area}`, "");
    out.push("| Categoria | Nombre | Unidad | Coste | Venta | Margen % | Proveedor | Confianza |");
    out.push("|---|---|---:|---:|---:|---:|---|---|");
    for (const item of areaItems) {
      out.push(`| ${item.category} | ${item.name} | ${item.unit} | ${item.costPrice.toFixed(4)} | ${item.salePrice.toFixed(4)} | ${item.marginPercent.toFixed(2)} | ${item.supplier} | ${item.confidence} |`);
    }
    out.push("");
  }
  if (!active.length) out.push("No hay precios activos definidos todavia.", "");
  return out.join("\n");
}

async function exportPriceKnowledge() {
  const items = listPriceItems({ includeInactive: true });
  const dir = path.join(ROOT, "presupuestacion", "costes");
  await fs.mkdir(dir, { recursive: true });
  await fs.writeFile(path.join(dir, "lista-precios.json"), JSON.stringify({ updatedAt: new Date().toISOString(), prices: items }, null, 2), "utf8");
  await fs.writeFile(path.join(dir, "lista-precios.yaml"), priceItemsYaml(items), "utf8");
  await fs.writeFile(path.join(dir, "lista-precios.md"), priceItemsMarkdown(items), "utf8");
  return {
    files: [
      "presupuestacion/costes/lista-precios.json",
      "presupuestacion/costes/lista-precios.yaml",
      "presupuestacion/costes/lista-precios.md",
    ],
    count: items.length,
    activeCount: items.filter((item) => item.active).length,
  };
}

async function upsertPriceItem(input) {
  const item = normalizePriceItem(input);
  const now = new Date().toISOString();
  if (item.id) {
    const current = db().prepare("SELECT id FROM price_items WHERE id = ?").get(item.id);
    if (!current) throw new Error("Precio no encontrado.");
    db().prepare(`
      UPDATE price_items
      SET category = ?, area = ?, name = ?, description = ?, unit = ?, cost_price = ?, sale_price = ?,
          margin_percent = ?, supplier = ?, confidence = ?, notes = ?, active = ?, updated_at = ?
      WHERE id = ?
    `).run(item.category, item.area, item.name, item.description, item.unit, item.costPrice, item.salePrice, item.marginPercent, item.supplier, item.confidence, item.notes, item.active, now, item.id);
  } else {
    db().prepare(`
      INSERT INTO price_items (category, area, name, description, unit, cost_price, sale_price, margin_percent, supplier, confidence, notes, active, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(item.category, item.area, item.name, item.description, item.unit, item.costPrice, item.salePrice, item.marginPercent, item.supplier, item.confidence, item.notes, item.active, now, now);
  }
  const exportInfo = await exportPriceKnowledge();
  return { prices: listPriceItems(), exportInfo };
}

async function deletePriceItem(id) {
  const priceId = Number(id);
  if (!priceId) throw new Error("ID de precio invalido.");
  db().prepare("DELETE FROM price_items WHERE id = ?").run(priceId);
  const exportInfo = await exportPriceKnowledge();
  return { prices: listPriceItems(), exportInfo };
}

function budgetCodeParts(code) {
  const match = String(code || "").match(/^P-(\d{4})-(\d{4})$/);
  return { year: match?.[1] || new Date().getFullYear().toString(), number: Number(match?.[2] || 0) };
}

function budgetTotal(payload) {
  return (payload.lineas || []).reduce((sum, line) => sum + Number(line.importe || 0), 0);
}

async function readMinimalBudgetPayload(folder, title = "Presupuesto") {
  const payload = { titulo: title, resumen: "", tipoProducto: "presupuesto", cliente: {}, lineas: [], supuestos: [], riesgos: [], preguntas: [], sugerencias: [] };
  const readme = path.join(folder, "README.md");
  if (await fileExists(readme)) {
    const content = await fs.readFile(readme, "utf8");
    const h1 = content.match(/^#\s+(.+)$/m);
    if (h1) payload.titulo = h1[1].replace(/^P-\d{4}-\d{4}\s*/, "").trim() || payload.titulo;
    const resumen = content.match(/##\s+Resumen\s+([\s\S]*?)(?:\n##\s+|$)/i);
    if (resumen) payload.resumen = resumen[1].trim();
  }
  const html = path.join(folder, "presupuesto-final.html");
  if (!payload.resumen && await fileExists(html)) {
    const content = await fs.readFile(html, "utf8");
    const titleMatch = content.match(/<title[^>]*>(.*?)<\/title>/i) || content.match(/<h1[^>]*>(.*?)<\/h1>/i) || content.match(/<h2[^>]*>(.*?)<\/h2>/i);
    if (titleMatch) payload.titulo = stripTags(titleMatch[1]).replace(/^P-\d{4}-\d{4}\s*/, "").trim() || payload.titulo;
    const paragraph = content.match(/<p[^>]*>(.*?)<\/p>/i);
    if (paragraph) payload.resumen = stripTags(paragraph[1]).trim();
  }
  return payload;
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
function send(res, status, body, contentType = "application/json; charset=utf-8", headers = {}) {
  res.writeHead(status, { "Content-Type": contentType, ...headers });
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

async function readLimitedTail(file, max = 16000) {
  const content = await fs.readFile(file, "utf8");
  return content.length > max ? `[Se muestran las observaciones mas recientes]\n\n${content.slice(-max)}` : content;
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

function normalizeDocumentTemplate(template = {}) {
  return {
    logo: String(template.logo || DEFAULT_DOCUMENT_TEMPLATE.logo),
    headerText: String(template.headerText || DEFAULT_DOCUMENT_TEMPLATE.headerText),
    footerText: String(template.footerText || DEFAULT_DOCUMENT_TEMPLATE.footerText),
  };
}

function isAlufacBudget(payload = {}) {
  const explicit = String(payload.documentBrand || "").toLowerCase();
  if (explicit === "ham") return false;
  if (explicit === "alufac") return true;
  return ["carpinteria_aluminio_alufac", "cortizo_abatibles", "cortizo_correderas", "persianas_mallorquinas"].includes(payload.budgetMode)
    || ["ALUFAC", "CORTIZO"].includes(payload.marcaSistema)
    || payload.tipoProducto === "carpinteria_aluminio";
}

function documentTemplateForBudget(payload = {}) {
  return normalizeDocumentTemplate(isAlufacBudget(payload) ? ALUFAC_DOCUMENT_TEMPLATE : payload.documentTemplate);
}

function defaultConfig() {
  return {
    defaultProvider: DEFAULT_PROVIDER,
    openaiApiKey: "",
    openaiModel: "",
    geminiApiKey: "",
    geminiModel: DEFAULT_GEMINI_MODEL,
    falApiKey: "",
    modelTokenBudgets: { openai: {}, gemini: {} },
    documentTemplate: DEFAULT_DOCUMENT_TEMPLATE,
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
    documentTemplate: normalizeDocumentTemplate(config.documentTemplate),
  };
}

function maskedConfig(config) {
  return {
    defaultProvider: config.defaultProvider || DEFAULT_PROVIDER,
    openaiApiKeySet: Boolean(config.openaiApiKey),
    openaiModel: config.openaiModel || "",
    geminiApiKeySet: Boolean(config.geminiApiKey),
    geminiModel: config.geminiModel || DEFAULT_GEMINI_MODEL,
    falApiKeySet: Boolean(config.falApiKey),
    modelTokenBudgets: config.modelTokenBudgets || { openai: {}, gemini: {} },
    documentTemplate: normalizeDocumentTemplate(config.documentTemplate),
  };
}

async function writeConfig(config) {
  const current = await readConfig();
  const next = {
    defaultProvider: ["fallback", "openai", "gemini"].includes(config.defaultProvider) ? config.defaultProvider : current.defaultProvider || DEFAULT_PROVIDER,
    openaiApiKey: config.openaiApiKey ? config.openaiApiKey : current.openaiApiKey,
    openaiModel: config.openaiModel ?? current.openaiModel,
    geminiApiKey: config.geminiApiKey ? config.geminiApiKey : current.geminiApiKey,
    geminiModel: config.geminiModel ?? current.geminiModel,
    falApiKey: config.falApiKey ? config.falApiKey : current.falApiKey,
    modelTokenBudgets: config.modelTokenBudgets || current.modelTokenBudgets || { openai: {}, gemini: {} },
    documentTemplate: normalizeDocumentTemplate(config.documentTemplate || current.documentTemplate),
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
  const skillFiles = (await listFiles(path.join(ROOT, "skills"), (file) => file.endsWith(".md"))).sort((a, b) => {
    const priority = (file) => path.basename(file).startsWith("00_") ? 0 : 1;
    return priority(a) - priority(b) || a.localeCompare(b);
  });
  const compositionFiles = await listFiles(path.join(ROOT, "productos", "composiciones"), (file) => file.endsWith(".yaml"));
  const requirementFiles = await listFiles(path.join(ROOT, "productos", "requisitos"), (file) => file.endsWith(".yaml") || file.endsWith(".yml"));
  const costingFiles = await listFiles(path.join(ROOT, "presupuestacion", "costes"), (file) =>
    file.endsWith(".json") || file.endsWith(".md") || file.endsWith(".yaml") || file.endsWith(".yml")
  );

  const selected = [
    path.join(ROOT, "README.md"),
    path.join(ROOT, "presupuestacion", "criterios-ambientales-menorca.md"),
    path.join(ROOT, "presupuestacion", "criterios-comerciales.md"),
    ...skillFiles,
    ...compositionFiles,
    ...requirementFiles,
    ...costingFiles,
  ];

  const docs = [];
  for (const file of selected) {
    if (!(await fileExists(file))) continue;
    docs.push({
      path: path.relative(ROOT, file).replaceAll("\\", "/"),
      content: file.startsWith(LEARNING_DIR) && path.basename(file).startsWith("aprendizaje_")
        ? await readLimitedTail(file, 12000)
        : await readLimited(file, 12000),
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
- Antes de cerrar un precio exacto, revisar skills y productos/requisitos. Si faltan datos obligatorios, incluir preguntas concretas y marcar confianza baja/media; no inventar medidas criticas.
- Si el usuario rellena una plantilla de producto, usar esos parametros como fuente principal del presupuesto.
- En CORTIZO, validar la variante exacta y aplicar cortizo-validacion-oficial.md; no heredar prestaciones o límites entre Industrial, Hoja Oculta, CC/CC16, Evolution o Passivhaus.
- Prioridad de costes: lista de precios activa u oferta real identificada > tarifa vigente > ratios orientativos. Nunca presentar costes-aluminio-cortizo.md como tarifa oficial.
- Separar dominios: aluminio y herreria no se presupuestan igual.
- En aluminio, cada linea debe representar una abertura/hueco de un tipo por una cantidad de unidades iguales. Incluir perfilSistema y tipoApertura por linea.
- En herreria, no usar tipoApertura ni ilustracionApertura. Cada linea debe indicar productoLinea cuando aplique: barandilla, reja, puerta_metalica, porton_cancela, escalera_metalica, estructura_metalica, pergola_marquesina, dintel_refuerzo, chapa_remate, montaje o transporte.

Formato exacto de respuesta:
{
  "titulo": "string",
  "resumen": "string",
  "tipoProducto": "string",
  "budgetFamily": "aluminio | herreria",
  "lineas": [
    {
      "id": "L1",
      "capitulo": "Diseno | Materiales | Fabricacion | Tratamiento | Transporte | Montaje | Riesgo | Margen",
      "concepto": "string",
      "descripcion": "string",
      "familiaLinea": "aluminio | herreria",
      "productoLinea": "solo herreria: barandilla | reja | puerta_metalica | porton_cancela | escalera_metalica | estructura_metalica | pergola_marquesina | dintel_refuerzo | chapa_remate | montaje | transporte | pendiente",
      "perfilSistema": "solo aluminio: COR 2000 | COR 3000 | COR 3500 | COR 4200 | COR 4500 | COR 4600 | COR 4700 | COR 4900 | COR Vision | CORTIZO Mallorquina | ALUFAC pendiente | pendiente",
      "cantidad": number,
      "unidad": "ud | ml | m2 | kg | h | lote",
      "precioUnitario": number,
      "importe": number,
      "confianza": "alta | media | baja",
      "origen": "skill/coste/supuesto/adjunto",
      "editable": true,
      "tipoApertura": "solo aluminio; usar una opción admitida o pendiente. En herreria omitir",
      "ilustracionApertura": "solo aluminio; mismo identificador que tipoApertura. En herreria omitir"
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
      "skillDestino": "skills/aprendizaje/aprendizaje_general.md",
      "prioridad": "alta | media | baja"
    }
  ]
}

Contexto del repositorio:
${context.map((doc) => `\n--- ${doc.path} ---\n${doc.content}`).join("\n")}`;
}

function isIllustratedOpeningBudget(payload = {}) {
  const explicitBrand = String(payload.documentBrand || "").toLowerCase();
  if (explicitBrand === "ham") return false;
  if (explicitBrand && explicitBrand !== "alufac") return false;
  return ["carpinteria_aluminio_alufac", "cortizo_abatibles", "cortizo_correderas", "persianas_mallorquinas"].includes(payload.budgetMode)
    || ["ALUFAC", "CORTIZO"].includes(payload.marcaSistema);
}

function openingDiagramHtml(value) {
  const labels = {
    pendiente: "Pendiente de definir", fijo: "Fijo", abatible_izquierda: "Abatible izquierda", abatible_derecha: "Abatible derecha",
    oscilobatiente_izquierda: "Oscilobatiente izquierda", oscilobatiente_derecha: "Oscilobatiente derecha",
    practicable_2_hojas: "Practicable 2 hojas", corredera_2_hojas: "Corredera 2 hojas", corredera_3_hojas: "Corredera 3 hojas",
    corredera_4_hojas: "Corredera 4 hojas", corredera_6_hojas: "Corredera 6 hojas", galandage: "Galandage / hoja oculta en muro",
    esquina_90: "Encuentro en esquina 90°", proyectante: "Proyectante", plegable: "Plegable", elevable: "Elevable", pivotante: "Pivotante",
  };
  const key = Object.hasOwn(labels, value) ? value : "pendiente";
  const label = labels[key];
  const leafMatch = key.match(/(3|4|6)_hojas/);
  const leaves = leafMatch ? Number(leafMatch[1]) : key.includes("2_hojas") ? 2 : 1;
  const panelWidth = 100 / leaves;
  let panels = "";
  for (let index = 0; index < leaves; index += 1) {
    panels += `<span style="position:absolute;left:${index * panelWidth + 4}%;top:10px;width:${panelWidth - 8}%;height:42px;border:1.5px solid #16202a;background:#ffffff;border-radius:2px;box-shadow:inset 0 0 0 4px #f8fbfd;"></span>`;
  }
  let symbol = "";
  if (key.includes("corredera") || key === "elevable" || key === "galandage") symbol = '<span style="position:absolute;left:16px;right:16px;bottom:9px;border-top:2px solid #b9863a;"></span><span style="position:absolute;left:10px;bottom:1px;color:#b9863a;font:700 18px Arial;">&larr;</span><span style="position:absolute;right:10px;bottom:1px;color:#b9863a;font:700 18px Arial;">&rarr;</span>';
  else if (key.includes("izquierda")) symbol = '<span style="position:absolute;left:15px;top:32px;width:88px;border-top:2px solid #b9863a;transform:rotate(-15deg);transform-origin:left center;"></span><span style="position:absolute;left:15px;top:32px;width:88px;border-top:2px solid #b9863a;transform:rotate(15deg);transform-origin:left center;"></span><span style="position:absolute;left:12px;top:28px;width:6px;height:6px;border-radius:50%;background:#16202a;"></span>';
  else if (key.includes("derecha")) symbol = '<span style="position:absolute;right:15px;top:32px;width:88px;border-top:2px solid #b9863a;transform:rotate(15deg);transform-origin:right center;"></span><span style="position:absolute;right:15px;top:32px;width:88px;border-top:2px solid #b9863a;transform:rotate(-15deg);transform-origin:right center;"></span><span style="position:absolute;right:12px;top:28px;width:6px;height:6px;border-radius:50%;background:#16202a;"></span>';
  else if (key === "practicable_2_hojas") symbol = '<span style="position:absolute;left:10px;top:34px;width:49px;border-top:2px solid #b9863a;transform:rotate(-24deg);transform-origin:left center;"></span><span style="position:absolute;left:10px;top:34px;width:49px;border-top:2px solid #b9863a;transform:rotate(24deg);transform-origin:left center;"></span><span style="position:absolute;right:10px;top:34px;width:49px;border-top:2px solid #b9863a;transform:rotate(24deg);transform-origin:right center;"></span><span style="position:absolute;right:10px;top:34px;width:49px;border-top:2px solid #b9863a;transform:rotate(-24deg);transform-origin:right center;"></span>';
  else if (key === "proyectante") symbol = '<span style="position:absolute;left:18px;top:37px;width:48px;border-top:2px solid #b9863a;transform:rotate(-42deg);transform-origin:left center;"></span><span style="position:absolute;right:18px;top:37px;width:48px;border-top:2px solid #b9863a;transform:rotate(42deg);transform-origin:right center;"></span>';
  else if (key === "plegable") symbol = '<span style="position:absolute;left:9px;right:9px;top:30px;color:#b9863a;font:700 22px Arial;text-align:center;letter-spacing:2px;">W</span>';
  else if (key === "pivotante") symbol = '<span style="position:absolute;left:57px;top:9px;height:48px;border-left:2px solid #b9863a;"></span><span style="position:absolute;left:47px;top:6px;color:#b9863a;font:700 16px Arial;">&uarr;</span><span style="position:absolute;left:47px;bottom:4px;color:#b9863a;font:700 16px Arial;">&darr;</span>';
  else if (key === "pendiente") symbol = '<span style="position:absolute;left:0;right:0;top:21px;text-align:center;color:#16202a;font:700 24px Arial;">?</span>';
  return `<figure class="opening-diagram"><div role="img" aria-label="${htmlEscape(label)}" style="position:relative;width:116px;height:72px;border:1.5px solid #d6dde5;border-radius:5px;background:#ffffff;overflow:hidden;">${panels}${symbol}</div><figcaption>${htmlEscape(label)} · esquema orientativo</figcaption></figure>`;
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
        skillDestino: "skills/aprendizaje/aprendizaje_general.md",
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
- Si budgetFamily es aluminio, trata la linea como abertura/hueco por cantidad de unidades e incluye perfilSistema y tipoApertura cuando el usuario lo pida.
- Si budgetFamily es herreria, no agregues tipoApertura ni ilustracionApertura; usa productoLinea para clasificar el producto de esa linea.
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

  const explicitUnitPrice = firstNumberAfter(normalized, /(?:precio\s*unitario|precio\/ud|eur\/ud|\u20ac\/ud|unidad|unitario|p\.?\s*u\.?)\D{0,35}(\d+(?:[.,]\d+)?)/i);
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
    skillDestino: "skills/aprendizaje/aprendizaje_general.md",
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
  const geminiModel = model || process.env.GEMINI_MODEL || config.geminiModel || DEFAULT_GEMINI_MODEL;
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
  const fenced = trimmed.match(/^```(?:markdown|md|json)?\s*\n([\s\S]*?)\n```$/i);
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
  const geminiModel = model || process.env.GEMINI_MODEL || config.geminiModel || DEFAULT_GEMINI_MODEL;
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

function yamlScalar(value) {
  return String(value || "")
    .replace(/#.*/, "")
    .trim()
    .replace(/^['"]|['"]$/g, "");
}

function yamlTopValue(content, key) {
  const match = String(content || "").match(new RegExp(`^${key}:\\s*(.+)$`, "m"));
  return match ? yamlScalar(match[1]) : "";
}

function yamlListBlock(content, key) {
  const lines = String(content || "").split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === `${key}:`);
  if (start < 0) return [];
  const out = [];
  for (let i = start + 1; i < lines.length; i += 1) {
    const line = lines[i];
    if (/^\S/.test(line) && line.includes(":")) break;
    const item = line.match(/^\s*-\s+(.+)$/);
    if (!item) continue;
    const raw = yamlScalar(item[1]);
    const [name, hint] = raw.split(":").map((part) => part.trim());
    if (name) out.push({ name, hint: hint || "" });
  }
  return out;
}

function productLabelFromSlug(slug) {
  return String(slug || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function productPromptTemplate(product) {
  const fields = product.variablesTecnicas?.length
    ? product.variablesTecnicas
    : [
        { name: "descripcion", hint: "que se necesita fabricar o instalar" },
        { name: "dimensiones", hint: "medidas principales" },
        { name: "material", hint: "material preferido" },
        { name: "acabado", hint: "tratamiento o terminacion" },
        { name: "ubicacion", hint: "interior/exterior/costa/obra" },
      ];
  return [
    `Producto: ${product.name}`,
    `Tipo interno: ${product.slug}`,
    "",
    "Rellenar parametros para presupuesto exacto:",
    ...fields.map((field) => `- ${field.name}: ${field.hint ? `[${field.hint}]` : "[pendiente]"}`),
    "",
    "Datos de obra:",
    "- ubicacion_obra:",
    "- montaje_en_obra: si/no",
    "- acceso_y_medios_auxiliares:",
    "- fotos_o_planos_adjuntos: si/no",
    "",
    "Objetivo: generar presupuesto tecnico y comercial. Si falta un dato critico, preguntar antes de cerrar precio exacto.",
  ].join("\n");
}

async function listProducts() {
  const dir = path.join(ROOT, "productos", "composiciones");
  const files = await listFiles(dir, (file) => path.extname(file).toLowerCase() === ".yaml");
  const products = [];
  for (const file of files) {
    const content = await fs.readFile(file, "utf8");
    const slug = path.basename(file, ".yaml");
    const product = {
      slug,
      name: yamlTopValue(content, "producto") || productLabelFromSlug(slug),
      unitBase: yamlTopValue(content, "unidad_base") || "",
      compositionPath: path.relative(ROOT, file).replaceAll("\\", "/"),
      skillPath: `skills/skill_${slug}.md`,
      requirementsPath: `productos/requisitos/${slug}.yaml`,
      variablesTecnicas: yamlListBlock(content, "variables_tecnicas"),
    };
    product.promptTemplate = productPromptTemplate(product);
    products.push(product);
  }
  return products.sort((a, b) => a.name.localeCompare(b.name, "es"));
}

function buildProductDocsFallback({ name, area, description }) {
  const slug = slugify(name).replaceAll("-", "_");
  const title = productLabelFromSlug(slug);
  const cleanArea = slugify(area || "otras_industrias").replaceAll("-", "_");
  const cleanDescription = String(description || "").trim() || "Producto a medida pendiente de definir con mas detalle.";
  const required = [
    "tipo_producto",
    "dimensiones_principales",
    "materiales",
    "acabado",
    "ubicacion",
    "montaje_en_obra",
    "acceso_obra",
  ];
  const skill = `# Skill: ${title}

## Cuándo usar esta skill

Cuando el producto a presupuestar sea ${title}. Area sugerida: ${cleanArea}.

## Datos mínimos necesarios

${required.map((item) => `- ${item.replaceAll("_", " ")}.`).join("\n")}

## Datos recomendados

- Fotos, planos o croquis.
- Plazo deseado.
- Restricciones de acceso o montaje.
- Preferencias de marca, acabado o normativa.

## Criterios técnicos

- No cerrar presupuesto exacto si faltan dimensiones, material, acabado o montaje.
- En Menorca, evaluar ambiente salino, viento, corrosion y acceso a obra.
- Documentar supuestos cuando el usuario decida avanzar con datos incompletos.

## Composición habitual del producto

Ver \`/productos/composiciones/${slug}.yaml\`.

## Preguntas que el agente debe hacer antes de presupuestar

${required.map((item) => `- ¿${item.replaceAll("_", " ")}?`).join("\n")}
`;
  const composition = `producto: ${title}
unidad_base: unidad / conjunto

descripcion: ${cleanDescription}

materiales_principales:
  - nombre: Material principal
    tipo: definir

materiales_auxiliares:
  - nombre: Fijaciones y consumibles
    tipo: definir

procesos:
  - medicion_y_replanteo
  - diseno_y_despiece
  - fabricacion
  - tratamiento_superficial
  - transporte
  - montaje_en_obra

variables_tecnicas:
${required.map((item) => `  - ${item}: pendiente`).join("\n")}

costes_a_considerar:
  materiales: true
  mano_obra_taller: true
  mano_obra_montaje: true
  transporte: true
  riesgo: true
  margen: true
`;
  const requirements = `producto: ${title}
slug: ${slug}
area: ${cleanArea}
datos_requeridos:
${required.map((item) => `  - campo: ${item}\n    pregunta: "${item.replaceAll("_", " ")}"\n    obligatorio: true`).join("\n")}
prompt_base: |
  Producto: ${title}
  Rellenar parametros:
${required.map((item) => `  - ${item}: [pendiente]`).join("\n")}
  Si falta un dato obligatorio, preguntar antes de calcular precio exacto.
`;
  return { slug, files: [
    { path: `skills/skill_${slug}.md`, content: skill },
    { path: `productos/composiciones/${slug}.yaml`, content: composition },
    { path: `productos/requisitos/${slug}.yaml`, content: requirements },
  ] };
}

function buildProductDocsPrompt({ name, area, description }) {
  return `Crea archivos de conocimiento para un nuevo producto del presupuestador.

Producto: ${name}
Area: ${area || "otras_industrias"}
Descripcion del usuario:
${description || ""}

Devuelve SOLO JSON valido con esta forma:
{
  "slug": "nombre_en_snake_case",
  "files": [
    {"path": "skills/skill_nombre_en_snake_case.md", "content": "...markdown..."},
    {"path": "productos/composiciones/nombre_en_snake_case.yaml", "content": "...yaml..."},
    {"path": "productos/requisitos/nombre_en_snake_case.yaml", "content": "...yaml..."}
  ]
}

Reglas:
- El slug debe ser snake_case, sin acentos.
- La skill debe incluir Datos minimos necesarios, Datos recomendados, Criterios tecnicos, Preguntas que el agente debe hacer y Checklist final.
- La composicion YAML debe incluir producto, unidad_base, materiales_principales, materiales_auxiliares, procesos, variables_tecnicas y costes_a_considerar.
- El requisitos YAML debe incluir datos_requeridos con campo, pregunta, obligatorio y opciones si aplica, mas prompt_base.
- No inventes precios concretos.
- En productos exteriores en Menorca contempla ambiente marino, viento, corrosion y acceso a obra.`;
}

async function createProductKnowledge(body) {
  const name = String(body.name || "").trim();
  if (!name) throw new Error("Falta el nombre del producto.");
  const context = await loadRepositoryContext();
  const selection = { provider: body.provider || "fallback", model: body.model || "fallback" };
  let result = buildProductDocsFallback(body);
  let warning = null;
  let usage = null;
  if (selection.provider === "openai" || selection.provider === "gemini") {
    const prompt = buildProductDocsPrompt(body);
    try {
      const response = selection.provider === "openai"
        ? await callOpenAIText({ prompt, context, model: selection.model })
        : await callGeminiText({ prompt, context, model: selection.model });
      result = JSON.parse(stripMarkdownEnvelope(response.content));
      usage = response.usage;
    } catch (error) {
      warning = error.message;
      result = buildProductDocsFallback(body);
    }
  }
  const slug = slugify(result.slug || name).replaceAll("-", "_");
  const files = Array.isArray(result.files) ? result.files : buildProductDocsFallback({ ...body, name: slug }).files;
  const written = [];
  for (const file of files) {
    let relative = String(file.path || "").replaceAll("\\", "/").replace(/nombre_en_snake_case/g, slug);
    if (relative.startsWith("skills/")) relative = `skills/skill_${slug}.md`;
    if (relative.includes("/composiciones/")) relative = `productos/composiciones/${slug}.yaml`;
    if (relative.includes("/requisitos/")) relative = `productos/requisitos/${slug}.yaml`;
    if (!/^skills\/skill_[a-z0-9_]+\.md$/.test(relative)
      && !/^productos\/composiciones\/[a-z0-9_]+\.ya?ml$/.test(relative)
      && !/^productos\/requisitos\/[a-z0-9_]+\.ya?ml$/.test(relative)) {
      continue;
    }
    const full = resolveEditable(relative);
    await fs.mkdir(path.dirname(full), { recursive: true });
    await fs.writeFile(full, String(file.content || "").trim() + "\n", "utf8");
    written.push(relative);
  }
  await recordTokenUsage(selection.provider, selection.model, usage);
  return { slug, files: written, warning, usage };
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

function stripTags(value) {
  return String(value || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
}
function totalOf(lines) {
  return (lines || []).reduce((sum, line) => sum + Number(line.importe || 0), 0);
}

function pdfSafeText(value) {
  return String(value ?? "")
    .replace(/[\u2010-\u2015]/g, "-")
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u201c\u201d]/g, '"')
    .replace(/\u2026/g, "...")
    .replace(/[^\x20-\x7e\xa0-\xff]/g, "");
}

function pdfString(value) {
  return pdfSafeText(value).replace(/\\/g, "\\\\").replace(/\(/g, "\\(").replace(/\)/g, "\\)");
}

function wrapPdfText(value, maxChars) {
  const words = pdfSafeText(value).trim().split(/\s+/).filter(Boolean);
  if (!words.length) return [""];
  const lines = [];
  let current = "";
  for (const word of words) {
    if (!current) {
      current = word;
    } else if (`${current} ${word}`.length <= maxChars) {
      current += ` ${word}`;
    } else {
      lines.push(current);
      current = word;
    }
  }
  if (current) lines.push(current);
  return lines;
}

function summarizedBudgetRows(lines = []) {
  const groups = new Map();
  for (const line of lines) {
    const amount = roundMoney(line.importe ?? Number(line.cantidad || 0) * Number(line.precioUnitario || 0));
    if (!amount) continue;
    const chapter = pdfSafeText(line.capitulo || "Otros");
    if (!groups.has(chapter)) groups.set(chapter, { chapter, amount: 0, concepts: [] });
    const group = groups.get(chapter);
    group.amount = roundMoney(group.amount + amount);
    const concept = pdfSafeText(line.concepto || "").trim();
    if (concept && !group.concepts.includes(concept)) group.concepts.push(concept);
  }
  return [...groups.values()];
}

function createSummaryPdf(payload, code) {
  const pageWidth = 595.28;
  const pageHeight = 841.89;
  const margin = 38;
  const contentWidth = pageWidth - margin * 2;
  const illustratedOpenings = isIllustratedOpeningBudget(payload);
  const rows = illustratedOpenings
    ? (payload.lineas || []).filter((item) => Number(item.importe || 0)).map((item) => ({
        chapter: pdfSafeText(item.capitulo || "Carpintería"),
        amount: roundMoney(item.importe ?? Number(item.cantidad || 0) * Number(item.precioUnitario || 0)),
        concepts: [pdfSafeText(item.concepto || "Elemento ALUFAC")],
        tipoApertura: item.tipoApertura || item.ilustracionApertura || "pendiente",
      }))
    : summarizedBudgetRows(payload.lineas || []);
  const total = roundMoney(rows.reduce((sum, row) => sum + row.amount, 0));
  const client = payload.cliente || {};
  const template = documentTemplateForBudget(payload);
  const headerLines = String(template.headerText || DEFAULT_DOCUMENT_TEMPLATE.headerText)
    .split(/\r?\n/)
    .map((line) => pdfSafeText(line.trim()))
    .filter(Boolean);
  const companyTitle = headerLines[0] || "HAM Estructuras Metalicas";
  const companyDetails = headerLines.slice(1);
  const footerLines = String(template.footerText || DEFAULT_DOCUMENT_TEMPLATE.footerText)
    .split(/\r?\n/)
    .map((line) => pdfSafeText(line.trim()))
    .filter(Boolean);
  const pages = [];
  let commands = [];
  let y = pageHeight - 34;

  const color = (r, g, b) => commands.push(`${r} ${g} ${b} rg`);
  const stroke = (r, g, b) => commands.push(`${r} ${g} ${b} RG`);
  const rect = (x, bottom, width, height, fill = [1, 1, 1]) => {
    color(...fill);
    commands.push(`${x.toFixed(2)} ${bottom.toFixed(2)} ${width.toFixed(2)} ${height.toFixed(2)} re f`);
  };
  const strokedRect = (x, bottom, width, height, rgb = [0.84, 0.87, 0.9]) => {
    stroke(...rgb);
    commands.push(`${x.toFixed(2)} ${bottom.toFixed(2)} ${width.toFixed(2)} ${height.toFixed(2)} re S`);
  };
  const line = (x1, y1, x2, y2, r = 0.82, g = 0.84, b = 0.86) => {
    commands.push(`${r} ${g} ${b} RG ${x1.toFixed(2)} ${y1.toFixed(2)} m ${x2.toFixed(2)} ${y2.toFixed(2)} l S`);
  };
  const drawOpening = (value, x, top) => {
    const key = String(value || "pendiente");
    const w = 48;
    const h = 29;
    const bottom = top - h;
    rect(x, bottom, w, h, [1, 1, 1]);
    strokedRect(x, bottom, w, h, [0.84, 0.87, 0.9]);
    rect(x + 4, bottom + 5, w - 8, h - 10, [0.97, 0.99, 1]);
    strokedRect(x + 4, bottom + 5, w - 8, h - 10, [0.09, 0.13, 0.17]);
    stroke(0.73, 0.53, 0.23);
    if (key.includes("corredera") || key === "elevable" || key === "galandage") {
      commands.push(`${x + 8} ${bottom + 4} m ${x + 40} ${bottom + 4} l S`);
      commands.push(`${x + 35} ${bottom + 8} m ${x + 40} ${bottom + 4} l ${x + 35} ${bottom} l S`);
      commands.push(`${x + 13} ${bottom + 8} m ${x + 8} ${bottom + 4} l ${x + 13} ${bottom} l S`);
    } else if (key.includes("izquierda")) {
      commands.push(`${x + w - 4} ${bottom + h - 5} m ${x + 5} ${bottom + h / 2} l ${x + w - 4} ${bottom + 5} l S`);
    } else if (key.includes("derecha")) {
      commands.push(`${x + 4} ${bottom + h - 5} m ${x + w - 5} ${bottom + h / 2} l ${x + 4} ${bottom + 5} l S`);
    } else if (key === "practicable_2_hojas") {
      commands.push(`${x + 4} ${bottom + h - 5} m ${x + w / 2} ${bottom + h / 2} l ${x + 4} ${bottom + 5} l S`);
      commands.push(`${x + w - 4} ${bottom + h - 5} m ${x + w / 2} ${bottom + h / 2} l ${x + w - 4} ${bottom + 5} l S`);
    } else if (key === "proyectante") {
      commands.push(`${x + 6} ${bottom + 5} m ${x + w / 2} ${bottom + h - 5} l ${x + w - 6} ${bottom + 5} l S`);
    } else if (key === "pendiente") {
      color(0.08, 0.13, 0.17);
      text("?", x + w / 2, bottom + 8, 15, "F2", "center");
    }
    stroke(0.84, 0.87, 0.9);
  };
  const measureText = (value, size = 10, font = "F1") => pdfSafeText(value).length * size * (font === "F2" ? 0.64 : 0.52);
  const wrapByWidth = (value, maxWidth, size = 10, font = "F1") => {
    const words = pdfSafeText(value).split(/\s+/).filter(Boolean);
    const lines = [];
    let current = "";
    for (const word of words) {
      const candidate = current ? `${current} ${word}` : word;
      if (!current || measureText(candidate, size, font) <= maxWidth) {
        current = candidate;
      } else {
        lines.push(current);
        current = word;
      }
    }
    if (current) lines.push(current);
    return lines;
  };
  const text = (value, x, baseline, size = 10, font = "F1", align = "left") => {
    const safe = pdfSafeText(value);
    const estimatedWidth = measureText(safe, size, font);
    const tx = align === "right" ? x - estimatedWidth : align === "center" ? x - estimatedWidth / 2 : x;
    commands.push(`BT /${font} ${size} Tf ${tx.toFixed(2)} ${baseline.toFixed(2)} Td (${pdfString(safe)}) Tj ET`);
  };
  const finishPage = () => {
    pages.push(commands.join("\n"));
    commands = [];
    y = pageHeight - 34;
  };
  const footer = (pageNumber) => {
    line(margin, 38, pageWidth - margin, 38);
    color(0.4, 0.43, 0.47);
    text(`${code} - Presupuesto resumido para cliente`, margin, 24, 8);
    text(`Pagina ${pageNumber}`, pageWidth - margin, 24, 8, "F1", "right");
  };
  const drawDocumentHeader = () => {
    rect(margin, y - 6, contentWidth, 4, [0.09, 0.13, 0.17]);
    y -= 32;

    color(0.02, 0.03, 0.04);
    text(isAlufacBudget(payload) ? "ALUFAC" : "HAM", margin + 4, y - 26, isAlufacBudget(payload) ? 22 : 28, "F2");
    color(0.08, 0.13, 0.17);
    text(companyTitle, margin + 108, y, 15, "F2");
    let detailY = y - 13;
    for (const detail of companyDetails.slice(0, 4)) {
      const lines = wrapPdfText(detail, 66).slice(0, 2);
      for (const item of lines) {
        color(0.25, 0.32, 0.42);
        text(item, margin + 108, detailY, 8.5);
        detailY -= 10;
      }
    }

    const rightX = pageWidth - margin;
    color(0.08, 0.13, 0.17);
    text("PRESUPUESTO", rightX, y, 15, "F2", "right");
    rect(rightX - 80, y - 32, 80, 23, [0.96, 0.97, 0.98]);
    strokedRect(rightX - 80, y - 32, 80, 23);
    color(0.08, 0.13, 0.17);
    text("Resumen cliente", rightX - 40, y - 23, 8.5, "F2", "center");
    color(0.25, 0.32, 0.42);
    text(code, rightX, y - 43, 8.5, "F2", "right");
    text(`Fecha: ${new Date().toISOString().slice(0, 10)}`, rightX, y - 54, 8.5, "F1", "right");

    y -= 92;
    line(margin, y, pageWidth - margin, y);
    y -= 14;
  };
  const ensureSpace = (needed) => {
    if (y - needed >= 58) return;
    footer(pages.length + 1);
    finishPage();
    drawDocumentHeader();
  };
  const paragraph = (value, options = {}) => {
    const size = options.size || 10;
    const leading = options.leading || size * 1.4;
    const maxChars = options.maxChars || Math.max(45, Math.floor(contentWidth / (size * 0.5)));
    const lines = wrapPdfText(value, maxChars);
    ensureSpace(lines.length * leading + (options.after || 0));
    color(...(options.color || [0.16, 0.18, 0.21]));
    for (const item of lines) {
      text(item, options.x || margin, y, size, options.bold ? "F2" : "F1");
      y -= leading;
    }
    y -= options.after || 0;
  };

  drawDocumentHeader();

  const heroTextWidth = contentWidth - 34;
  const heroTitleLines = wrapByWidth(payload.titulo || "Presupuesto", heroTextWidth, 17, "F2").slice(0, 4);
  const heroLines = wrapByWidth(payload.resumen || "", heroTextWidth, 9.5, "F1").slice(0, 5);
  const heroHeight = 22 + heroTitleLines.length * 19 + heroLines.length * 11;
  ensureSpace(heroHeight + 12);
  rect(margin, y - heroHeight + 10, contentWidth, heroHeight, [0.96, 0.97, 0.98]);
  rect(margin, y - heroHeight + 10, 4, heroHeight, [0.09, 0.13, 0.17]);
  color(0.08, 0.13, 0.17);
  let heroY = y - 10;
  for (const item of heroTitleLines) {
    text(item, margin + 14, heroY, 17, "F2");
    heroY -= 19;
  }
  y = heroY + 3;
  color(0.29, 0.35, 0.44);
  for (const item of heroLines) {
    text(item, margin + 14, y, 9.5);
    y -= 11;
  }
  y -= 16;

  const meta = [
    `Cliente: ${client.nombre || ""}`,
    `Email: ${client.email || ""} | Tel.: ${client.telefono || ""}`,
    `Obra: ${client.direccion || ""}`,
    `NIF/CIF: ${client.nif || ""} | Referencia: ${client.referencia || ""}`,
  ].filter(Boolean);
  ensureSpace(62);
  rect(margin, y - 52, contentWidth, 52, [0.96, 0.97, 0.98]);
  strokedRect(margin, y - 52, contentWidth, 52);
  color(0.18, 0.2, 0.22);
  let metaY = y - 15;
  for (const item of meta.slice(0, 4)) {
    const [label, ...rest] = item.split(":");
    text(`${label}:`, margin + 12, metaY, 9, "F2");
    text(rest.join(":").trim(), margin + 78, metaY, 9);
    metaY -= 11;
  }
  y -= 68;

  ensureSpace(42);
  rect(margin, y - 24, contentWidth, 24, [0.09, 0.13, 0.17]);
  color(1, 1, 1);
  text("Capitulo", margin + 6, y - 15, 8.5, "F2");
  text("Concepto resumido", margin + 92, y - 15, 8.5, "F2");
  text("Importe", pageWidth - margin - 6, y - 15, 8.5, "F2", "right");
  y -= 38;

  for (const row of rows) {
    const description = row.concepts.slice(0, 3).join(", ");
    const wrapped = wrapPdfText(description, illustratedOpenings ? 58 : 82);
    const rowHeight = Math.max(illustratedOpenings ? 48 : 34, 18 + wrapped.length * 10);
    ensureSpace(rowHeight + 8);
    const topY = y;
    color(0.08, 0.13, 0.17);
    text(row.chapter, margin + 6, topY, 8.5);
    text(`${row.amount.toFixed(2)} EUR`, pageWidth - margin - 6, topY, 9.5, "F2", "right");
    if (illustratedOpenings) drawOpening(row.tipoApertura, margin + 92, topY + 4);
    color(0.4, 0.42, 0.45);
    let descY = topY;
    for (const descriptionLine of wrapped) {
      text(descriptionLine, margin + (illustratedOpenings ? 150 : 92), descY, 8.2);
      descY -= 10;
    }
    y = topY - rowHeight;
    line(margin, y, pageWidth - margin, y, 0.84, 0.87, 0.9);
    y -= 8;
  }

  ensureSpace(92);
  line(margin, y + 10, pageWidth - margin, y + 10, 0.84, 0.87, 0.9);
  y -= 8;
  color(0.1, 0.14, 0.18);
  text(`Total estimado: ${total.toFixed(2)} EUR + IVA`, pageWidth - margin, y, 15, "F2", "right");
  y -= 44;

  if (footerLines.length) {
    ensureSpace(18 + footerLines.length * 12);
    line(margin, y, pageWidth - margin, y);
    y -= 16;
    const half = contentWidth / 2;
    footerLines.slice(0, 4).forEach((item, index) => {
      const x = index % 2 === 0 ? margin : margin + half + 12;
      const itemY = y - Math.floor(index / 2) * 14;
      const [label, ...rest] = item.split(":");
      color(0.22, 0.28, 0.36);
      text(`${label}:`, x, itemY, 8.5, "F2");
      text(rest.join(":").trim(), x + 76, itemY, 8.5);
    });
    y -= Math.ceil(Math.min(footerLines.length, 4) / 2) * 14 + 8;
  }

  footer(pages.length + 1);
  finishPage();

  const objects = [];
  const addObject = (body) => {
    objects.push(body);
    return objects.length;
  };
  const catalogId = addObject("");
  const pagesId = addObject("");
  const regularFontId = addObject("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>");
  const boldFontId = addObject("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>");
  const pageIds = [];
  for (const stream of pages) {
    const streamBuffer = Buffer.from(stream, "latin1");
    const contentId = addObject(`<< /Length ${streamBuffer.length} >>\nstream\n${stream}\nendstream`);
    pageIds.push(addObject(`<< /Type /Page /Parent ${pagesId} 0 R /MediaBox [0 0 ${pageWidth} ${pageHeight}] /Resources << /Font << /F1 ${regularFontId} 0 R /F2 ${boldFontId} 0 R >> >> /Contents ${contentId} 0 R >>`));
  }
  objects[catalogId - 1] = `<< /Type /Catalog /Pages ${pagesId} 0 R >>`;
  objects[pagesId - 1] = `<< /Type /Pages /Kids [${pageIds.map((id) => `${id} 0 R`).join(" ")}] /Count ${pageIds.length} >>`;

  const chunks = [Buffer.from("%PDF-1.4\n%\xff\xff\xff\xff\n", "latin1")];
  const offsets = [0];
  let offset = chunks[0].length;
  objects.forEach((object, index) => {
    offsets.push(offset);
    const chunk = Buffer.from(`${index + 1} 0 obj\n${object}\nendobj\n`, "latin1");
    chunks.push(chunk);
    offset += chunk.length;
  });
  const xrefOffset = offset;
  const xref = [`xref\n0 ${objects.length + 1}\n`, "0000000000 65535 f \n"];
  for (let index = 1; index <= objects.length; index += 1) {
    xref.push(`${String(offsets[index]).padStart(10, "0")} 00000 n \n`);
  }
  xref.push(`trailer\n<< /Size ${objects.length + 1} /Root ${catalogId} 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`);
  chunks.push(Buffer.from(xref.join(""), "latin1"));
  return Buffer.concat(chunks);
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

${payload.imagenConceptual ? `![Imagen conceptual orientativa](${payload.imagenConceptual})\n\n_${payload.imagenConceptualNota || "Imagen orientativa generada por IA."}_\n\n` : ""}## Lineas del compuesto

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

function renderDocumentHeaderText(headerText) {
  const lines = String(headerText || DEFAULT_DOCUMENT_TEMPLATE.headerText).split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const title = lines[0] || "HAM Estructuras Metalicas";
  const details = lines.slice(1);
  return `<h1>${htmlEscape(title)}</h1>${details.map((line) => `<p>${htmlEscape(line)}</p>`).join("")}`;
}

function renderDocumentFooterText(footerText) {
  const lines = String(footerText || DEFAULT_DOCUMENT_TEMPLATE.footerText).split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const effective = lines.length ? lines : DEFAULT_DOCUMENT_TEMPLATE.footerText.split("\n");
  return effective.map((line) => `<div>${htmlEscape(line)}</div>`).join("");
}

function lineTechnicalMetaHtml(line, payload = {}) {
  const isAluminum = String(payload.budgetFamily || "").toLowerCase() === "aluminio" || isAlufacBudget(payload);
  const parts = [];
  if (isAluminum && line.perfilSistema && line.perfilSistema !== "pendiente") parts.push(`Perfil: ${line.perfilSistema}`);
  if (!isAluminum && line.productoLinea && line.productoLinea !== "pendiente") parts.push(`Producto: ${line.productoLinea}`);
  return parts.length ? `<div class="line-technical-meta">${parts.map(htmlEscape).join(" · ")}</div>` : "";
}

function fallbackDocumentTemplateEdit({ documentTemplate, prompt }) {
  const current = normalizeDocumentTemplate(documentTemplate);
  const instruction = String(prompt || "").trim();
  const footerText = instruction ? `${current.footerText.trim()}\n${instruction}`.trim() : current.footerText;
  return { ...current, footerText };
}

function buildDocumentTemplatePrompt({ documentTemplate, instruction }) {
  return `Edita la cabecera y el pie/condiciones predeterminadas del documento de presupuesto.

Reglas:
- Devuelve SOLO JSON valido, sin explicaciones ni cercas de codigo.
- Manten el JSON con las claves logo, headerText y footerText.
- headerText y footerText son textos multilinea.
- Conserva datos reales de HAM si el usuario no pide cambiarlos.
- El pie debe contener condiciones comerciales claras y reutilizables.

Plantilla actual:
${JSON.stringify(normalizeDocumentTemplate(documentTemplate), null, 2)}

Instruccion del usuario:
${instruction}`;
}

function parseDocumentTemplateJson(text, fallback) {
  const cleaned = stripMarkdownEnvelope(text);
  const parsed = JSON.parse(cleaned);
  return normalizeDocumentTemplate({ ...fallback, ...parsed });
}
function budgetImagePublicUrl(payload) {
  const image = payload?.imagenConceptual || payload?.imagenPrincipal || "";
  if (!image) return "";
  if (/^https?:\/\//i.test(image) || image.startsWith("data:")) return image;
  const folder = String(payload?._folder || "").replaceAll("\\", "/");
  if (!folder) return image;
  return `/${folder}/${image}`.replace(/\/+/g, "/");
}

function budgetImageHtml(payload, className = "concept-image") {
  const src = budgetImagePublicUrl(payload);
  if (!src) return "";
  const note = payload.imagenConceptualNota || "Imagen orientativa generada por IA. El diseno final dependera de medidas, materiales, acabados y validacion tecnica.";
  return `<figure class="${className}"><img src="${htmlEscape(src)}" alt="Imagen conceptual del presupuesto" loading="eager" decoding="sync" onerror="this.closest('figure').remove()"><figcaption>${htmlEscape(note)}</figcaption></figure>`;
}

function buildBudgetImagePrompt(payload) {
  const lines = (payload.lineas || [])
    .slice(0, 12)
    .map((line) => `- ${line.capitulo || ""}: ${line.concepto || ""}. ${line.descripcion || ""}. ${line.cantidad || ""} ${line.unidad || ""}`)
    .join("\n");
  return `Imagen conceptual comercial, realista y limpia para un presupuesto tecnico de HAM en Menorca.

Producto: ${payload.titulo || "Presupuesto tecnico"}
Tipo: ${payload.tipoProducto || "producto a medida"}
Resumen: ${payload.resumen || ""}
Cliente/obra: ${payload.cliente?.direccion || "Menorca"}
Partidas principales:
${lines}

Estilo visual:
- Imagen cuadrada, luminosa, profesional, sin texto, sin logotipos, sin marcas de agua.
- Mostrar el producto terminado de forma plausible en su entorno.
- Si es exterior en Menorca, reflejar ambiente mediterraneo y materiales adecuados al ambiente salino.
- Priorizar claridad comercial sobre detalle tecnico milimetrico.
- No incluir planos con cotas ni textos ilegibles.
- No representar personas reconocibles.`;
}
async function callFalImage({ payload }) {
  const config = await readConfig();
  const key = process.env.FAL_KEY || config.falApiKey;
  if (!key) throw new Error("FAL_KEY no configurada.");
  const prompt = buildBudgetImagePrompt(payload);
  const response = await fetch(`https://fal.run/${FAL_IMAGE_MODEL}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Key ${key}` },
    body: JSON.stringify({
      prompt,
      image_size: FAL_IMAGE_SIZE,
      num_inference_steps: FAL_IMAGE_STEPS,
      guidance_scale: 1,
      num_images: 1,
      enable_safety_checker: true,
      output_format: "png",
      acceleration: FAL_IMAGE_ACCELERATION,
    }),
  });
  const data = await response.json();
  const detail = Array.isArray(data.detail) ? data.detail.map((item) => item.msg || item.message || String(item)).join("; ") : data.detail;
  if (!response.ok) throw new Error(detail || data.error?.message || `fal.ai HTTP ${response.status}`);
  const url = data.images?.[0]?.url || data.image?.url || data.url;
  if (!url) throw new Error("fal.ai no devolvio una URL de imagen utilizable.");
  const imageResponse = await fetch(url);
  if (!imageResponse.ok) throw new Error(`No se pudo descargar la imagen generada: HTTP ${imageResponse.status}`);
  return {
    buffer: Buffer.from(await imageResponse.arrayBuffer()),
    prompt,
    usage: null,
    requestId: data.request_id || data.requestId || null,
    remoteUrl: url,
  };
}
function budgetHtml(payload, code) {
  const lines = payload.lineas || [];
  const client = payload.cliente || {};
  const total = totalOf(lines);
  const today = new Date().toISOString().slice(0, 10);
  const documentTemplate = documentTemplateForBudget(payload);
  const documentBrand = isAlufacBudget(payload) ? "ALUFAC" : "HAM";
  return `<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>${htmlEscape(code)} ${htmlEscape(payload.titulo || "Presupuesto")}</title>
  <style>
    @page { size: A4; margin: 0; }
    * { box-sizing: border-box; }
    body { font-family: Arial, Helvetica, sans-serif; color: #111827; margin: 0; line-height: 1.34; background: #eef2f6; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .page { width: 210mm; max-width: 100%; min-height: 297mm; margin: 0 auto; padding: 14mm 15mm; background: white; }
    header { border-top: 6px solid #16202a; padding-top: 12px; display: grid; grid-template-columns: minmax(0, 1fr) 190px; gap: 16px; align-items: start; border-bottom: 1px solid #d6dde5; padding-bottom: 12px; }
    .company { display: flex; gap: 14px; min-width: 0; }
    .logo { width: 130px; flex: 0 0 130px; padding-top: 2px; }
    .logo img { width: 100%; filter: brightness(0) saturate(100%); }
    .company h1 { margin: 0 0 4px; font-size: 18px; color: #16202a; }
    .company p, .meta p { margin: 2px 0; color: #4b5563; font-size: 11px; }
    .meta { text-align: right; color: #4b5563; }
    .meta h2 { margin: 0 0 7px; color: #16202a; font-size: 18px; text-transform: uppercase; letter-spacing: 0; }
    .ref { display: inline-block; padding: 5px 8px; border: 1px solid #d6dde5; background: #f6f8fa; color: #16202a; font-weight: 700; font-size: 12px; }
    .hero { margin: 14px 0; padding: 12px 14px; border-left: 4px solid #16202a; background: #f6f8fa; }
    .hero h2 { margin: 0 0 5px; font-size: 22px; color: #16202a; line-height: 1.12; }
    .hero p { margin: 0; color: #475467; font-size: 12px; }
    .concept-image { margin: 12px 0; page-break-inside: avoid; }
    .concept-image img { width: 100%; max-height: 78mm; object-fit: cover; border: 1px solid #d6dde5; border-radius: 4px; display: block; }
    .concept-image figcaption { margin-top: 5px; color: #667085; font-size: 10px; }
    .box { border: 1px solid #d6dde5; background: #f6f8fa; padding: 10px 12px; margin: 12px 0; font-size: 12px; }
    h3 { margin: 14px 0 7px; font-size: 15px; color: #16202a; }
    table { width: 100%; border-collapse: collapse; margin-top: 8px; table-layout: fixed; font-size: 10px; line-height: 1.2; }
    th { background: #16202a; color: white; text-align: left; padding: 7px 6px; }
    td { border-bottom: 1px solid #d6dde5; padding: 7px 6px; vertical-align: top; overflow-wrap: anywhere; }
    .num { text-align: right; white-space: nowrap; }
    .line-technical-meta { margin-top: 3px; color: #53657a; font-size: 9px; font-weight: 700; }
    .opening-diagram { width: 118px; margin: 7px 0 0; page-break-inside: avoid; }
    .opening-diagram svg { display: block; width: 100%; height: auto; }
    .opening-diagram g { fill: none; stroke: #16202a; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
    .opening-diagram text { fill: #16202a; stroke: none; font: 700 30px Arial; }
    .opening-diagram figcaption { margin-top: 3px; color: #667085; font-size: 8px; }
    .col-chapter { width: 10%; } .col-concept { width: 51%; } .col-qty { width: 8%; } .col-unit { width: 7%; } .col-price { width: 11%; } .col-amount { width: 13%; }
    .total { margin-top: 16px; text-align: right; font-size: 18px; font-weight: 700; }
    .conditions { margin-top: 14px; border-top: 1px solid #d6dde5; padding-top: 9px; color: #4b5563; font-size: 11px; display: grid; gap: 5px; }
    ul { padding-left: 18px; font-size: 11px; color: #4b5563; }
    button { margin-top: 18px; padding: 10px 14px; border: 0; background: #16202a; color: white; border-radius: 6px; font-weight: 700; }
    .opening-diagram > div { display: block; width: 116px; height: 72px; }
    @media print { body { background: white; margin: 0; } .page { width: 210mm; max-width: none; min-height: 297mm; margin: 0; } .no-print { display: none; } }
  </style>
</head>
<body>
<main class="page">
  <header>
    <section class="company">
      <div class="logo"><img src="${htmlEscape(documentTemplate.logo)}" alt="${documentBrand}"></div>
      <div>${renderDocumentHeaderText(documentTemplate.headerText)}</div>
    </section>
    <section class="meta">
      <h2>Presupuesto</h2>
      <div class="ref">${htmlEscape(code)}</div>
      <p>Fecha: ${today}</p>

    </section>
  </header>
  <section class="hero">
    <h2>${htmlEscape(payload.titulo || "Presupuesto")}</h2>
    <p>${htmlEscape(payload.resumen || "")}</p>
  </section>
  <section class="box">
    <strong>Cliente:</strong> ${htmlEscape(client.nombre || "")}<br>
    <strong>Email:</strong> ${htmlEscape(client.email || "")} | <strong>Tel.:</strong> ${htmlEscape(client.telefono || "")}<br>
    <strong>Obra:</strong> ${htmlEscape(client.direccion || "")}<br>
    <strong>NIF/CIF:</strong> ${htmlEscape(client.nif || "")} | <strong>Referencia:</strong> ${htmlEscape(client.referencia || "")}
  </section>
  <h3>Desglose de partidas</h3>
  <table>
    <colgroup><col class="col-chapter"><col class="col-concept"><col class="col-qty"><col class="col-unit"><col class="col-price"><col class="col-amount"></colgroup>
    <thead><tr><th>Capitulo</th><th>Concepto</th><th class="num">Cant.</th><th>Ud.</th><th class="num">EUR/Ud.</th><th class="num">Importe</th></tr></thead>
    <tbody>${lines.map((line) => `<tr><td>${htmlEscape(line.capitulo)}</td><td><strong>${htmlEscape(line.concepto)}</strong>${lineTechnicalMetaHtml(line, payload)}<br>${htmlEscape(line.descripcion)}${isIllustratedOpeningBudget(payload) ? openingDiagramHtml(line.tipoApertura || line.ilustracionApertura || "pendiente") : ""}</td><td class="num">${Number(line.cantidad || 0).toFixed(2)}</td><td>${htmlEscape(line.unidad)}</td><td class="num">${Number(line.precioUnitario || 0).toFixed(2)}</td><td class="num">${Number(line.importe || 0).toFixed(2)}</td></tr>`).join("")}</tbody>
  </table>
  <div class="total">Total estimado: ${total.toFixed(2)} EUR + IVA</div>
  <section class="conditions">${renderDocumentFooterText(documentTemplate.footerText)}</section>
  <h3>Supuestos</h3>
  <ul>${(payload.supuestos || []).map((item) => `<li>${htmlEscape(item)}</li>`).join("")}</ul>
  <h3>Riesgos y datos pendientes</h3>
  <ul>${[...(payload.riesgos || []), ...(payload.preguntas || [])].map((item) => `<li>${htmlEscape(item)}</li>`).join("")}</ul>
  <button class="no-print" onclick="window.print()">Imprimir / PDF</button>
</main>
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
    const imageFile = budgetData?.imagenConceptual || (fileNames.includes("imagen-conceptual-ia.png") ? "imagen-conceptual-ia.png" : "");
    const imageUrl = imageFile ? `/presupuestos/${encodeURIComponent(entry.name)}/${encodeURIComponent(imageFile)}` : "";
    const code = `P-${match[1]}-${match[2]}`;
    const indexedData = budgetData || await readMinimalBudgetPayload(folder, title);
    saveBudgetRecord({ folder, code, payload: indexedData, htmlPath: `presupuestos/${entry.name}/presupuesto-final.html` });
    budgets.push({
      code,
      year: match[1],
      number: Number(match[2]),
      title,
      clientName: client.nombre || "",
      total: budgetData ? totalOf(budgetData.lineas || []) : 0,
      folder: `presupuestos/${entry.name}`,
      imageUrl,
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
  const existingFolders = budgets.map((budget) => budget.folder);
  if (existingFolders.length) {
    const placeholders = existingFolders.map(() => "?").join(",");
    db().prepare(`DELETE FROM budgets WHERE folder NOT IN (${placeholders})`).run(...existingFolders);
  } else {
    db().exec("DELETE FROM budgets");
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
function normalizeForLearning(text) {
  return String(text || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function learningTextForClassification({ payload, suggestion, note, changeLog } = {}) {
  const parts = [
    payload?.titulo,
    payload?.resumen,
    payload?.tipoProducto,
    payload?.cliente?.direccion,
    suggestion?.titulo,
    suggestion?.detalle,
    note,
    ...(payload?.lineas || []).flatMap((line) => [line.capitulo, line.concepto, line.descripcion, line.unidad]),
    ...(Array.isArray(changeLog) ? changeLog : []).map((change) => JSON.stringify(change)),
  ];
  return normalizeForLearning(parts.filter(Boolean).join(" "));
}

function detectLearningArea(input = {}) {
  const text = learningTextForClassification(input);
  const checks = [
    ["instalaciones_electricas", /\b(electric|cuadro|cable|mecanismo|enchufe|luminaria|iluminacion|rebt|boletin|fotovoltaic|domotic)\b/],
    ["fontaneria", /\b(fontaner|tuberia|agua|saneamiento|desague|acs|sanitario|grifer|bomba|presion)\b/],
    ["clima", /\b(clima|climatizacion|split|conducto|ventilacion|extraccion|aeroterm|rite|frigorific)\b/],
    ["aluminio", /\b(aluminio|cerramiento|ventana|mallorquina|persiana|mosquitera|rpt|lacado|anodizado|vidrio|cristal|corredera|abatible)\b/],
    ["carpinteria_metalica", /\b(metal|metalic|acero|inox|hierro|barandilla|reja|puerta|cancela|porton|escalera|estructura|dintel|pergola|marquesina|galvanizado|soldadura|chapa|tubo|s275|s235)\b/],
  ];
  return checks.find(([, pattern]) => pattern.test(text))?.[0] || "general";
}

function learningFileFor(input = {}) {
  const suggested = String(input.suggestion?.skillDestino || "").replaceAll("\\", "/");
  if (/^skills\/aprendizaje\/aprendizaje_[a-z0-9_]+\.md$/.test(suggested)) {
    const full = path.resolve(ROOT, suggested);
    if (full.startsWith(path.resolve(LEARNING_DIR))) return full;
  }
  const area = detectLearningArea(input);
  return path.join(LEARNING_DIR, LEARNING_FILES[area] || LEARNING_FILES.general);
}

async function ensureLearningFile(file, area = "general") {
  await fs.mkdir(path.dirname(file), { recursive: true });
  if (await fileExists(file)) return;
  const title = path.basename(file, ".md").replace(/^aprendizaje_/, "Aprendizaje: ").replaceAll("_", " ");
  await fs.writeFile(file, `# ${title}\n\nArea: ${area}\n\nCriterios observados desde presupuestos reales. Revisar y consolidar en skills, composiciones o costes cuando se repitan.\n`, "utf8");
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

function compactLearningText(value, max = 180) {
  return String(value ?? "").replace(/\s+/g, " ").trim().slice(0, max);
}

function learningFingerprintText(value) {
  return normalizeForLearning(value).replace(/\b\d+(?:[.,]\d+)?\b/g, "#").replace(/\s+/g, " ").trim().slice(0, 220);
}

function changePatternForLearning(change, payload) {
  const sector = compactLearningText(payload.budgetMode || payload.tipoProducto || "general", 80);
  const line = change.after || change.line || change.before || {};
  const concept = compactLearningText(line.concepto || "partida sin concepto", 140);
  const conceptKey = learningFingerprintText(concept);
  if (change.action === "edit-field") {
    const field = compactLearningText(change.field || "campo", 50);
    return {
      key: `campo|${sector}|${field}|${conceptKey}`,
      title: `${sector}: revisar ${field} en ${concept}`,
      rule: `Para partidas equivalentes a "${concept}", revisar el campo ${field}. La correccion mas reciente fue de "${compactLearningText(change.from)}" a "${compactLearningText(change.to)}".`,
    };
  }
  if (change.action === "edit-line" && change.prompt) {
    const prompt = compactLearningText(change.prompt, 260);
    return {
      key: `criterio-ia|${sector}|${learningFingerprintText(prompt)}`,
      title: `${sector}: criterio repetido indicado por el usuario`,
      rule: `Aplicar como comprobacion en trabajos similares: "${prompt}". Validar su aplicabilidad a las medidas y alcance de cada obra.`,
    };
  }
  if (change.action === "edit-opening") {
    return {
      key: `apertura|${sector}|${conceptKey}|${learningFingerprintText(change.to)}`,
      title: `${sector}: apertura corregida en ${concept}`,
      rule: `En elementos equivalentes a "${concept}", comprobar la apertura "${compactLearningText(change.to)}" antes de emitir el documento.`,
    };
  }
  if (["add-line", "delete-line"].includes(change.action)) {
    return {
      key: `${change.action}|${sector}|${conceptKey}`,
      title: `${sector}: ${change.action === "add-line" ? "partida necesaria" : "partida normalmente integrada o eliminada"}`,
      rule: `${change.action === "add-line" ? "Comprobar la inclusion" : "Comprobar si debe integrarse o excluirse"} de la partida "${concept}" en presupuestos similares.`,
    };
  }
  return null;
}

async function readLearningState() {
  if (!(await fileExists(LEARNING_STATE_FILE))) return { version: 1, patterns: {}, recent: [] };
  try {
    const state = JSON.parse(await fs.readFile(LEARNING_STATE_FILE, "utf8"));
    return { version: 1, patterns: state.patterns || {}, recent: Array.isArray(state.recent) ? state.recent : [] };
  } catch {
    return { version: 1, patterns: {}, recent: [] };
  }
}

function renderConsolidatedLearning(state) {
  const patterns = Object.values(state.patterns || {}).sort((a, b) => String(b.lastSeen).localeCompare(String(a.lastSeen)));
  const consolidated = patterns.filter((item) => item.status === "consolidada");
  const candidates = patterns.filter((item) => item.status !== "consolidada").slice(0, 40);
  const section = (items, empty) => items.length ? items.map((item) => [
    `### ${item.title}`,
    `- Regla: ${item.rule}`,
    `- Evidencias: ${item.count} correccion(es) en ${item.budgets.length} presupuesto(s): ${item.budgets.join(", ")}.`,
    `- Ultima observacion: ${item.lastSeen}.`,
  ].join("\n")).join("\n\n") : empty;
  return `# Reglas consolidadas desde presupuestos reales

Este archivo se actualiza automaticamente. Las reglas consolidadas tienen prioridad como comprobaciones en nuevas estimaciones, sin sustituir medidas, tarifas vigentes ni validacion tecnica.

## Reglas consolidadas

${section(consolidated, "Todavia no hay patrones confirmados en dos presupuestos distintos.")}

## Candidatos pendientes de confirmacion

No tratar estos candidatos como reglas universales hasta que aparezcan en otro presupuesto diferente.

${section(candidates, "No hay candidatos registrados.")}
`;
}

function renderRecentLearning(state) {
  const recent = (state.recent || []).slice(-60).reverse();
  return `# Memoria operativa reciente

Correcciones recientes registradas al guardar presupuestos. Usarlas para evitar repetir errores, pero no convertir una observacion aislada en una regla universal.

${recent.length ? recent.map((item) => `- ${item.at} · ${item.code} · ${item.area}: ${item.summary}`).join("\n") : "Todavia no hay correcciones recientes registradas."}
`;
}

let learningUpdateQueue = Promise.resolve();

function updateLearningConsolidation({ payload, code, area, changes }) {
  learningUpdateQueue = learningUpdateQueue.then(async () => {
    const state = await readLearningState();
    for (const change of changes) {
      const summary = summarizeChangeForLearning(change).replace(/^[- ]+/, "");
      const evidenceId = crypto.createHash("sha256").update(`${code}|${learningFingerprintText(summary)}`).digest("hex").slice(0, 24);
      if (!state.recent.some((item) => item.id === evidenceId)) {
        state.recent.push({ id: evidenceId, at: new Date().toISOString(), code, area, summary: compactLearningText(summary, 420) });
      }
      const pattern = changePatternForLearning(change, payload);
      if (!pattern) continue;
      const current = state.patterns[pattern.key] || { ...pattern, count: 0, budgets: [], evidenceIds: [], status: "candidata", firstSeen: new Date().toISOString() };
      if (!current.evidenceIds.includes(evidenceId)) {
        current.evidenceIds.push(evidenceId);
        current.count += 1;
      }
      if (!current.budgets.includes(code)) current.budgets.push(code);
      current.rule = pattern.rule;
      current.title = pattern.title;
      current.lastSeen = new Date().toISOString();
      current.status = current.budgets.length >= 2 ? "consolidada" : "candidata";
      current.evidenceIds = current.evidenceIds.slice(-50);
      current.budgets = current.budgets.slice(-20);
      state.patterns[pattern.key] = current;
    }
    state.recent = state.recent.slice(-200);
    state.patterns = Object.fromEntries(Object.entries(state.patterns).sort((a, b) => String(b[1].lastSeen).localeCompare(String(a[1].lastSeen))).slice(0, 500));
    await fs.mkdir(LEARNING_DIR, { recursive: true });
    await fs.writeFile(LEARNING_STATE_FILE, `${JSON.stringify(state, null, 2)}\n`, "utf8");
    await fs.writeFile(LEARNING_RULES_FILE, renderConsolidatedLearning(state), "utf8");
    await fs.writeFile(LEARNING_RECENT_FILE, renderRecentLearning(state), "utf8");
  }).catch((error) => console.error("No se pudo consolidar el aprendizaje:", error));
  return learningUpdateQueue;
}

async function appendBudgetLearning(payload, code, changeLog = []) {
  const usefulChanges = (Array.isArray(changeLog) ? changeLog : [])
    .filter((change) => change && change.source !== "generacion")
    .slice(-80);
  if (!usefulChanges.length) return null;
  const area = detectLearningArea({ payload, changeLog: usefulChanges });
  const file = learningFileFor({ payload, changeLog: usefulChanges });
  await ensureLearningFile(file, area);
  const total = (payload.lineas || []).reduce((sum, line) => sum + Number(line.importe || 0), 0);
  const lines = usefulChanges.map(summarizeChangeForLearning).join("\n");
  const entry = `\n## ${new Date().toISOString().slice(0, 10)} - Aprendizaje desde presupuesto ${code}\n\n- Área: ${area}\n- Sector: ${payload.tipoProducto || "pendiente de clasificar"}\n- Tipo de conocimiento: cambios reales de presupuesto\n- Estado: observado\n- Origen: cambios realizados durante edición y guardado del presupuesto\n- Presupuesto: ${payload.titulo || "Sin título"}\n- Cliente/obra: ${payload.cliente?.nombre || ""} ${payload.cliente?.direccion ? `- ${payload.cliente.direccion}` : ""}\n- Total final guardado: ${total.toFixed(2)} EUR + IVA\n\n### Cambios observados\n${lines}\n\n### Acción futura\n- Revisar estas correcciones antes de cerrar cantidades, precios unitarios, capítulos y partidas omitidas en trabajos similares.\n- Si el criterio se repite, consolidarlo en la skill, composición o coste correspondiente.\n`;
  await fs.appendFile(file, entry, "utf8");
  await updateLearningConsolidation({ payload, code, area, changes: usefulChanges });
  return path.relative(ROOT, file).replaceAll("\\", "/");
}
async function appendLearning({ suggestion, note }) {
  const area = detectLearningArea({ suggestion, note });
  const file = learningFileFor({ suggestion, note });
  await ensureLearningFile(file, area);
  const entry = `\n## ${new Date().toISOString().slice(0, 10)} - ${suggestion?.titulo || "Aprendizaje"}\n\n- Área: ${area}\n- Sector: pendiente de clasificar\n- Tipo de conocimiento: criterio manual o sugerencia aceptada\n- Estado: observado\n- Origen: sugerencia aceptada en presupuestador-app\n- Prioridad: ${suggestion?.prioridad || "media"}\n- Criterio: ${suggestion?.detalle || note || ""}\n\n### Acción futura\n- Revisar si debe consolidarse en una skill, composición, coste o ficha de proveedor.\n`;
  await fs.appendFile(file, entry, "utf8");
  return path.relative(ROOT, file).replaceAll("\\", "/");
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
  if (req.method === "GET" && url.pathname === "/api/health") return send(res, 200, { ok: true });
  if (req.method === "GET" && url.pathname === "/login.html") return send(res, 200, loginPage(), "text/html; charset=utf-8");
  if (req.method === "POST" && url.pathname === "/api/auth/login") {
    const body = await readJson(req);
    const username = String(body.username || "").trim().toLowerCase();
    const user = db().prepare("SELECT * FROM app_users WHERE username = ? AND active = 1").get(username);
    if (!user || !verifyPassword(body.password, user.password_hash)) return send(res, 401, { error: "Credenciales invalidas." });
    const token = crypto.randomBytes(32).toString("hex");
    const now = new Date();
    const expires = new Date(now.getTime() + SESSION_DAYS * 86400 * 1000).toISOString();
    db().prepare("INSERT INTO app_sessions (token, user_id, expires_at, created_at) VALUES (?, ?, ?, ?)").run(token, user.id, expires, now.toISOString());
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8", "Set-Cookie": sessionCookie(token, req) });
    res.end(JSON.stringify({ user: publicUser(user) }));
    return;
  }
  const user = currentUser(req);
  if (!user) {
    if (url.pathname.startsWith("/api/")) return send(res, 401, { error: "No autenticado." });
    if (req.method === "GET") {
      res.writeHead(302, { Location: `${BASE_PATH}/login.html` });
      res.end();
      return;
    }
    return send(res, 401, { error: "No autenticado." });
  }
  if (req.method === "GET" && url.pathname === "/api/auth/me") return send(res, 200, { user: publicUser(user) });
  if (req.method === "POST" && url.pathname === "/api/auth/logout") {
    const token = parseCookies(req).ps_session;
    if (token) db().prepare("DELETE FROM app_sessions WHERE token = ?").run(token);
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8", "Set-Cookie": clearSessionCookie() });
    res.end(JSON.stringify({ ok: true }));
    return;
  }
  if (req.method === "GET" && url.pathname === "/api/users") {
    requireAdmin(user);
    return send(res, 200, { users: listUsers() });
  }
  if (req.method === "POST" && url.pathname === "/api/users") {
    requireAdmin(user);
    return send(res, 200, { users: createUser(await readJson(req)) });
  }
  const userMatch = url.pathname.match(/^\/api\/users\/(\d+)$/);
  if (userMatch && req.method === "PUT") {
    requireAdmin(user);
    return send(res, 200, { users: updateUser(userMatch[1], await readJson(req)) });
  }
  if (req.method === "GET" && url.pathname === "/api/budgets") return send(res, 200, await listBudgets());
  if (req.method === "GET" && url.pathname === "/api/budget") return send(res, 200, await readBudgetData(url.searchParams.get("folder")));
  if (req.method === "GET" && url.pathname === "/api/context") {
    const context = await loadRepositoryContext();
    return send(res, 200, { files: context.map((doc) => doc.path) });
  }
  if (req.method === "GET" && url.pathname === "/api/settings") return send(res, 200, maskedConfig(await readConfig()));
  if (req.method === "GET" && url.pathname === "/api/db/status") return send(res, 200, dbStatus());
  if (req.method === "POST" && url.pathname === "/api/settings") return send(res, 200, await writeConfig(await readJson(req)));
  if (req.method === "GET" && url.pathname === "/api/prices") {
    requireAdmin(user);
    return send(res, 200, { prices: listPriceItems(), exportFiles: ["presupuestacion/costes/lista-precios.md", "presupuestacion/costes/lista-precios.yaml", "presupuestacion/costes/lista-precios.json"] });
  }
  if (req.method === "POST" && url.pathname === "/api/prices") {
    requireAdmin(user);
    return send(res, 200, await upsertPriceItem(await readJson(req)));
  }
  const priceMatch = url.pathname.match(/^\/api\/prices\/(\d+)$/);
  if (priceMatch && req.method === "DELETE") {
    requireAdmin(user);
    return send(res, 200, await deletePriceItem(priceMatch[1]));
  }
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
  if (req.method === "GET" && url.pathname === "/api/products") {
    return send(res, 200, { products: await listProducts() });
  }
  if (req.method === "POST" && url.pathname === "/api/products") {
    requireAdmin(user);
    const result = await createProductKnowledge(await readJson(req));
    return send(res, 200, { ...result, products: await listProducts(), files: await listEditableFiles() });
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
  if (req.method === "POST" && url.pathname === "/api/document-template/ai") {
    const body = await readJson(req);
    const provider = body.provider || "fallback";
    const model = body.model || "fallback";
    const instruction = String(body.prompt || "").trim();
    const documentTemplate = normalizeDocumentTemplate(body.documentTemplate);
    if (!instruction) return send(res, 400, { error: "Falta instruccion para editar la cabecera o el pie." });
    const context = await loadRepositoryContext();
    const templatePrompt = buildDocumentTemplatePrompt({ documentTemplate, instruction });
    const estimatedTokens = estimateRequestTokens(templatePrompt, []);
    const status = await modelStatus(provider, model, estimatedTokens);
    if (provider !== "fallback" && status.blocked) {
      return send(res, 402, { error: "Saldo local insuficiente para este modelo.", tokenStatus: status });
    }
    let result;
    let usage = null;
    try {
      if (provider === "openai") {
        const response = await callOpenAIText({ prompt: templatePrompt, context, model });
        result = parseDocumentTemplateJson(response.content, documentTemplate);
        usage = response.usage;
      } else if (provider === "gemini") {
        const response = await callGeminiText({ prompt: templatePrompt, context, model });
        result = parseDocumentTemplateJson(response.content, documentTemplate);
        usage = response.usage;
      } else {
        result = fallbackDocumentTemplateEdit({ documentTemplate, prompt: instruction });
      }
      await recordTokenUsage(provider, model, usage);
      return send(res, 200, { provider, model, documentTemplate: result, usage, tokenStatus: await modelStatus(provider, model, estimatedTokens) });
    } catch (error) {
      result = fallbackDocumentTemplateEdit({ documentTemplate, prompt: instruction });
      return send(res, 200, { provider: "fallback", warning: error.message, documentTemplate: result, usage: null, tokenStatus: status });
    }
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
  if (req.method === "POST" && url.pathname === "/api/budget-image") {
    const body = await readJson(req);
    if (!body.folder) return send(res, 400, { error: "Guarda primero el presupuesto para poder almacenar la imagen." });
    const folder = resolveBudgetFolder(body.folder);
    const relFolder = path.relative(ROOT, folder).replaceAll("\\", "/");
    const dataFile = path.join(folder, "datos.json");
    const hasDataFile = await fileExists(dataFile);
    const stored = hasDataFile
      ? JSON.parse(await fs.readFile(dataFile, "utf8"))
      : await readMinimalBudgetPayload(folder, path.basename(folder));
    const payload = { ...stored, ...(body.payload || {}) };
    const prompt = buildBudgetImagePrompt(payload);
    const estimatedTokens = estimateRequestTokens(prompt, []);
    const status = {
      provider: "fal",
      model: FAL_IMAGE_MODEL,
      estimatedInputTokens: estimatedTokens,
      localBudgetTokens: null,
      usedTokens: 0,
      remainingTokens: null,
      blocked: false,
      note: "Imagen generada con fal.ai en modo economico; sin control local por tokens.",
    };
    const image = await callFalImage({ payload });
    const fileName = "imagen-conceptual-ia.png";
    await fs.writeFile(path.join(folder, fileName), image.buffer);
    const code = path.basename(folder).match(/^(P-\d{4}-\d{4})/)?.[1] || await nextBudgetCode();
    const updated = {
      ...payload,
      imagenConceptual: fileName,
      imagenConceptualNota: "Imagen orientativa generada por IA. El diseno final dependera de medidas, materiales, acabados y validacion tecnica.",
      imagenConceptualPrompt: image.prompt,
      imagenConceptualGenerada: new Date().toISOString(),
      imagenConceptualProveedor: "fal.ai",
      imagenConceptualModelo: FAL_IMAGE_MODEL,
      imagenConceptualModo: "economico",
      imagenConceptualRequestId: image.requestId,
      imagenConceptualUrlRemota: image.remoteUrl,
    };
    if (hasDataFile || body.payload) {
      await fs.writeFile(path.join(folder, "README.md"), budgetMarkdown(updated, code), "utf8");
      await fs.writeFile(path.join(folder, "presupuesto-final.html"), budgetHtml(updated, code), "utf8");
      await fs.writeFile(dataFile, JSON.stringify(updated, null, 2), "utf8");
    } else {
      await fs.writeFile(path.join(folder, "imagen-conceptual.json"), JSON.stringify(updated, null, 2), "utf8");
    }
    const rel = saveBudgetRecord({ folder, code, payload: updated, htmlPath: `${relFolder}/presupuesto-final.html` });
    if (image.usage) await recordTokenUsage("fal", FAL_IMAGE_MODEL, image.usage);
    return send(res, 200, {
      ok: true,
      folder: rel,
      image: `${rel}/${fileName}`,
      fileName,
      payload: updated,
      usage: image.usage,
      tokenStatus: status,
    });
  }
  if (req.method === "POST" && url.pathname === "/api/export-summary-pdf") {
    const body = await readJson(req);
    if (!body.folder) return send(res, 400, { error: "Guarda primero el presupuesto para generar su PDF resumido." });
    const folder = resolveBudgetFolder(body.folder);
    const stored = await readBudgetData(body.folder);
    const payload = { ...(stored.data || {}), ...(body.payload || {}) };
    delete payload._folder;
    delete payload._changeLog;
    const code = path.basename(folder).match(/^(P-\d{4}-\d{4})/)?.[1] || "PRESUPUESTO";
    const fileName = "presupuesto-resumido-cliente.pdf";
    const pdf = createSummaryPdf(payload, code);
    await fs.writeFile(path.join(folder, fileName), pdf);
    res.writeHead(200, {
      "Content-Type": "application/pdf",
      "Content-Length": pdf.length,
      "Content-Disposition": `attachment; filename*=UTF-8''${encodeURIComponent(`${code}-resumido-cliente.pdf`)}`,
      "Cache-Control": "no-store",
    });
    return res.end(pdf);
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
  const cacheHeaders = ["/index.html", "/app.js"].includes(requested) ? { "Cache-Control": "no-store" } : {};
  send(res, 200, content, MIME[path.extname(target)] || "application/octet-stream", cacheHeaders);
}

const server = http.createServer((req, res) => {
  route(req, res).catch((error) => {
    console.error(error);
    send(res, error.statusCode || 500, { error: error.message });
  });
});

async function startServer() {
  db();
  const indexed = await listBudgets();
  const sessionCleanupTimer = setInterval(() => cleanupExpiredSessions(), 60 * 60 * 1000);
  sessionCleanupTimer.unref();
  server.listen(PORT, HOST, () => {
    console.log(`Presupuestador app: http://${HOST}:${PORT} (${indexed.budgets.length} presupuestos indexados)`);
  });
}

startServer().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
