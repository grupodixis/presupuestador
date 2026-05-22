import csv
import json
import re
import sys
from pathlib import Path
from statistics import median

import jaydebeapi


BACKUP_DIR = Path(r"C:\Users\grupo\Desktop\Backup factusol")
OUT_DIR = Path("datos-privados/factusol")
OUT_FILE = OUT_DIR / "historico-facturas-factusol.csv"
REF_FILE = OUT_DIR / "referencia-precios-partidas-factusol.csv"
HTML_FILE = OUT_DIR / "visor-factusol.html"
JAR_DIR = Path(r"C:\Users\grupo\AppData\Local\Temp\opencode\ucanaccess")

JARS = [
    JAR_DIR / "ucanaccess-5.0.1.jar",
    JAR_DIR / "jackcess-3.0.1.jar",
    JAR_DIR / "hsqldb-2.5.0.jar",
    JAR_DIR / "commons-lang3-3.8.1.jar",
    JAR_DIR / "commons-logging-1.2.jar",
]

QUERY = """
SELECT
  f.TIPFAC,
  f.CODFAC,
  f.REFFAC,
  f.FECFAC,
  f.CLIFAC,
  f.CNOFAC,
  f.OBRFAC,
  f.OB1FAC,
  f.OB2FAC,
  f.TOTFAC,
  l.POSLFA,
  l.ARTLFA,
  l.DESLFA,
  l.CANLFA,
  l.PRELFA,
  l.TOTLFA,
  l.MEMLFA
FROM F_FAC f
INNER JOIN F_LFA l
  ON f.TIPFAC = l.TIPLFA
 AND f.CODFAC = l.CODLFA
ORDER BY f.CODFAC, l.POSLFA
"""

WORK_PATTERNS = [
    re.compile(r"Obra\s*[:\-]\s*([^\r\n;]+)", re.IGNORECASE),
    re.compile(r"\{[^}]+\}\s*\[([^\]]+)\]"),
]


def clean(value):
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").replace("\r", "\n").strip()


def extract_work(*texts):
    merged = "\n".join(clean(text) for text in texts if clean(text))
    for pattern in WORK_PATTERNS:
        match = pattern.search(merged)
        if match:
            return clean(match.group(1))
    return ""


def normalize_text(value):
    value = clean(value).lower()
    value = re.sub(r"\s+", " ", value)
    return value.strip(" .;:-")


def number(value):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return 0.0


def compact_number(value):
    return round(number(value), 2)


def build_html(reference_rows, detail_rows):
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Historico FACTUSOL</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4f1ea;
      --panel: #fffaf0;
      --ink: #1f2933;
      --muted: #667085;
      --line: #dfd6c7;
      --accent: #9a3412;
      --accent-2: #1f766e;
      --shadow: 0 18px 50px rgba(31, 41, 51, .10);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Georgia, 'Times New Roman', serif; background: var(--bg); color: var(--ink); }}
    header {{ padding: 34px 40px 20px; background: linear-gradient(135deg, #fff7ed, #e7f3ef); border-bottom: 1px solid var(--line); }}
    h1 {{ margin: 0 0 8px; font-size: clamp(32px, 5vw, 56px); letter-spacing: -.04em; }}
    .subtitle {{ margin: 0; color: var(--muted); font-family: Arial, sans-serif; }}
    main {{ padding: 26px 40px 44px; }}
    .cards {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-bottom: 18px; }}
    .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 18px; box-shadow: var(--shadow); }}
    .card b {{ display: block; font-size: 28px; line-height: 1; margin-bottom: 7px; }}
    .card span {{ color: var(--muted); font-family: Arial, sans-serif; font-size: 13px; }}
    .toolbar {{ display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 10px; margin: 18px 0; }}
    input, select {{ width: 100%; border: 1px solid var(--line); background: #fff; color: var(--ink); border-radius: 12px; padding: 12px 13px; font: 14px Arial, sans-serif; }}
    .tabs {{ display: flex; gap: 8px; margin: 8px 0 16px; }}
    button {{ border: 1px solid var(--line); border-radius: 999px; background: #fff; padding: 10px 15px; cursor: pointer; font: 700 13px Arial, sans-serif; color: var(--ink); }}
    button.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    .table-wrap {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; overflow: hidden; box-shadow: var(--shadow); }}
    table {{ width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 13px; }}
    th {{ position: sticky; top: 0; z-index: 1; text-align: left; background: #2f2a24; color: #fff; padding: 11px 10px; white-space: nowrap; }}
    td {{ padding: 10px; border-top: 1px solid var(--line); vertical-align: top; }}
    tr:nth-child(even) td {{ background: rgba(255,255,255,.45); }}
    .num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
    .muted {{ color: var(--muted); }}
    .text {{ max-width: 560px; white-space: pre-wrap; }}
    .pager {{ display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 14px; font-family: Arial, sans-serif; color: var(--muted); }}
    .small {{ font-size: 12px; }}
    @media (max-width: 980px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .cards {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .toolbar {{ grid-template-columns: 1fr; }}
      .table-wrap {{ overflow-x: auto; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Historico FACTUSOL</h1>
    <p class="subtitle">Facturas extraidas de backups locales. Datos privados: no subir a GitHub.</p>
  </header>
  <main>
    <section class="cards">
      <div class="card"><b id="metric-lines">0</b><span>lineas de factura con importe</span></div>
      <div class="card"><b id="metric-ref">0</b><span>partidas agrupadas</span></div>
      <div class="card"><b id="metric-clients">0</b><span>clientes distintos</span></div>
      <div class="card"><b id="metric-total">0</b><span>importe historico en lineas</span></div>
    </section>

    <section class="toolbar">
      <input id="q" placeholder="Buscar texto, cliente, obra, factura...">
      <select id="year"><option value="">Todos los anos</option></select>
      <select id="minCount">
        <option value="1">Todas las apariciones</option>
        <option value="2">2+ apariciones</option>
        <option value="3">3+ apariciones</option>
        <option value="5">5+ apariciones</option>
      </select>
      <select id="sort">
        <option value="count">Mas repetidas</option>
        <option value="median_desc">Mediana mayor</option>
        <option value="median_asc">Mediana menor</option>
        <option value="text">Texto A-Z</option>
      </select>
    </section>

    <nav class="tabs">
      <button id="tabRef" class="active">Referencia agrupada</button>
      <button id="tabDetail">Lineas factura</button>
    </nav>

    <section class="table-wrap">
      <table>
        <thead id="thead"></thead>
        <tbody id="tbody"></tbody>
      </table>
      <div class="pager">
        <span id="pageInfo"></span>
        <span>
          <button id="prev">Anterior</button>
          <button id="next">Siguiente</button>
        </span>
      </div>
    </section>
    <p class="small muted">Tip: busca por palabras como barandilla, galvanizado, montaje, acero inox, cliente u obra.</p>
  </main>
  <script id="reference-data" type="application/json">{json.dumps(reference_rows, ensure_ascii=False)}</script>
  <script id="detail-data" type="application/json">{json.dumps(detail_rows, ensure_ascii=False)}</script>
  <script>
    const reference = JSON.parse(document.getElementById('reference-data').textContent);
    const detail = JSON.parse(document.getElementById('detail-data').textContent);
    let mode = 'ref';
    let page = 1;
    const pageSize = 80;
    const els = {{
      q: document.getElementById('q'), year: document.getElementById('year'), minCount: document.getElementById('minCount'), sort: document.getElementById('sort'),
      thead: document.getElementById('thead'), tbody: document.getElementById('tbody'), pageInfo: document.getElementById('pageInfo'),
      prev: document.getElementById('prev'), next: document.getElementById('next'), tabRef: document.getElementById('tabRef'), tabDetail: document.getElementById('tabDetail')
    }};
    const euro = new Intl.NumberFormat('es-ES', {{ style: 'currency', currency: 'EUR' }});
    const num = new Intl.NumberFormat('es-ES');
    function norm(v) {{ return String(v ?? '').toLowerCase(); }}
    function money(v) {{ return euro.format(Number(v || 0)); }}
    function fillYears() {{
      [...new Set(detail.map(r => r.anio_backup).filter(Boolean))].sort().forEach(y => {{
        const o = document.createElement('option'); o.value = y; o.textContent = y; els.year.appendChild(o);
      }});
    }}
    function updateMetrics() {{
      document.getElementById('metric-lines').textContent = num.format(detail.length);
      document.getElementById('metric-ref').textContent = num.format(reference.length);
      document.getElementById('metric-clients').textContent = num.format(new Set(detail.map(r => r.cliente).filter(Boolean)).size);
      document.getElementById('metric-total').textContent = money(detail.reduce((s, r) => s + Number(r.importe_linea || 0), 0));
    }}
    function filteredRef() {{
      const q = norm(els.q.value); const year = els.year.value; const min = Number(els.minCount.value || 1);
      let rows = reference.filter(r => Number(r.apariciones || 0) >= min);
      if (year) rows = rows.filter(r => norm(r.anios).includes(year));
      if (q) rows = rows.filter(r => [r.texto_partida_normalizado, r.texto_partida_ejemplo, r.clientes_ejemplo, r.obras_ejemplo, r.anios].some(v => norm(v).includes(q)));
      const sort = els.sort.value;
      rows.sort((a,b) => sort === 'median_desc' ? b.importe_mediana - a.importe_mediana : sort === 'median_asc' ? a.importe_mediana - b.importe_mediana : sort === 'text' ? a.texto_partida_normalizado.localeCompare(b.texto_partida_normalizado) : b.apariciones - a.apariciones);
      return rows;
    }}
    function filteredDetail() {{
      const q = norm(els.q.value); const year = els.year.value;
      let rows = detail;
      if (year) rows = rows.filter(r => r.anio_backup === year);
      if (q) rows = rows.filter(r => [r.texto_partida, r.cliente, r.obra_detectada, r.numero_factura, r.observaciones].some(v => norm(v).includes(q)));
      rows = [...rows].sort((a,b) => Number(b.importe_linea || 0) - Number(a.importe_linea || 0));
      return rows;
    }}
    function setHead(cols) {{ els.thead.innerHTML = '<tr>' + cols.map(c => `<th>${{c}}</th>`).join('') + '</tr>'; }}
    function cell(v, cls='') {{ return `<td class="${{cls}}">${{String(v ?? '').replace(/[&<>]/g, s => ({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[s]))}}</td>`; }}
    function render() {{
      const rows = mode === 'ref' ? filteredRef() : filteredDetail();
      const pages = Math.max(1, Math.ceil(rows.length / pageSize));
      page = Math.min(page, pages);
      const slice = rows.slice((page - 1) * pageSize, page * pageSize);
      if (mode === 'ref') {{
        setHead(['Partida', 'Apar.', 'Mediana', 'Min', 'Max', 'PU med.', 'Anos', 'Clientes/obras']);
        els.tbody.innerHTML = slice.map(r => '<tr>' +
          cell(r.texto_partida_ejemplo, 'text') + cell(r.apariciones, 'num') + cell(money(r.importe_mediana), 'num') + cell(money(r.importe_min), 'num') + cell(money(r.importe_max), 'num') + cell(money(r.precio_unitario_mediana), 'num') + cell(r.anios) + cell(`${{r.clientes_ejemplo}}\n${{r.obras_ejemplo}}`, 'text muted') + '</tr>').join('');
      }} else {{
        setHead(['Ano', 'Factura', 'Cliente', 'Obra', 'Partida', 'Cant.', 'PU', 'Importe']);
        els.tbody.innerHTML = slice.map(r => '<tr>' +
          cell(r.anio_backup) + cell(r.numero_factura) + cell(r.cliente) + cell(r.obra_detectada) + cell(r.texto_partida, 'text') + cell(r.cantidad, 'num') + cell(money(r.precio_unitario), 'num') + cell(money(r.importe_linea), 'num') + '</tr>').join('');
      }}
      els.pageInfo.textContent = `${{num.format(rows.length)}} resultados - pagina ${{page}}/${{pages}}`;
      els.prev.disabled = page <= 1; els.next.disabled = page >= pages;
    }}
    ['input','change'].forEach(ev => {{ els.q.addEventListener(ev, () => {{ page=1; render(); }}); }});
    [els.year, els.minCount, els.sort].forEach(el => el.addEventListener('change', () => {{ page=1; render(); }}));
    els.prev.onclick = () => {{ page--; render(); }}; els.next.onclick = () => {{ page++; render(); }};
    els.tabRef.onclick = () => {{ mode='ref'; page=1; els.tabRef.classList.add('active'); els.tabDetail.classList.remove('active'); els.minCount.disabled=false; els.sort.disabled=false; render(); }};
    els.tabDetail.onclick = () => {{ mode='detail'; page=1; els.tabDetail.classList.add('active'); els.tabRef.classList.remove('active'); els.minCount.disabled=true; els.sort.disabled=true; render(); }};
    fillYears(); updateMetrics(); render();
  </script>
</body>
</html>"""
    HTML_FILE.write_text(html, encoding="utf-8")


def year_from_file(path):
    match = re.search(r"(20\d{2})", path.stem)
    return match.group(1) if match else ""


def connect(path):
    missing = [str(jar) for jar in JARS if not jar.exists()]
    if missing:
        raise FileNotFoundError("Faltan JARs UCanAccess: " + ", ".join(missing))
    return jaydebeapi.connect(
        "net.ucanaccess.jdbc.UcanaccessDriver",
        f"jdbc:ucanaccess://{path};memory=false",
        jars=[str(jar) for jar in JARS],
    )


def rows_from_database(path):
    conn = connect(path)
    try:
        cur = conn.cursor()
        cur.execute(QUERY)
        for row in cur.fetchall():
            (
                tipo_factura,
                numero_factura,
                referencia,
                fecha,
                codigo_cliente,
                cliente,
                codigo_obra,
                observacion_1,
                observacion_2,
                total_factura,
                posicion_linea,
                codigo_articulo,
                texto_partida,
                cantidad,
                precio_unitario,
                importe_linea,
                memo_linea,
            ) = row

            texto = clean(texto_partida)
            observaciones = "\n".join(
                part for part in [clean(referencia), clean(observacion_1), clean(observacion_2), clean(memo_linea)] if part
            )

            yield {
                "origen_archivo": path.name,
                "empresa_backup": path.stem[:3],
                "anio_backup": year_from_file(path),
                "tipo_factura": clean(tipo_factura),
                "numero_factura": clean(numero_factura),
                "fecha_factura": clean(fecha),
                "codigo_cliente": clean(codigo_cliente),
                "cliente": clean(cliente),
                "codigo_obra": clean(codigo_obra),
                "obra_detectada": extract_work(referencia, observacion_1, observacion_2, texto),
                "posicion_linea": clean(posicion_linea),
                "codigo_articulo": clean(codigo_articulo),
                "texto_partida": texto,
                "cantidad": clean(cantidad),
                "precio_unitario": clean(precio_unitario),
                "importe_linea": clean(importe_linea),
                "total_factura": clean(total_factura),
                "observaciones": observaciones,
            }
    finally:
        conn.close()


def main():
    if not BACKUP_DIR.exists():
        raise FileNotFoundError(BACKUP_DIR)

    files = sorted(BACKUP_DIR.glob("*.accdb"))
    if not files:
        raise FileNotFoundError(f"No hay .accdb en {BACKUP_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "origen_archivo",
        "empresa_backup",
        "anio_backup",
        "tipo_factura",
        "numero_factura",
        "fecha_factura",
        "codigo_cliente",
        "cliente",
        "codigo_obra",
        "obra_detectada",
        "posicion_linea",
        "codigo_articulo",
        "texto_partida",
        "cantidad",
        "precio_unitario",
        "importe_linea",
        "total_factura",
        "observaciones",
    ]

    total = 0
    exported_rows = []
    errors = []
    with OUT_FILE.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for path in files:
            try:
                count = 0
                for row in rows_from_database(path):
                    writer.writerow(row)
                    exported_rows.append(row)
                    count += 1
                total += count
                print(f"{path.name}: {count} lineas")
            except Exception as exc:
                errors.append((path.name, str(exc)))
                print(f"ERROR {path.name}: {exc}", file=sys.stderr)

    print(f"Salida: {OUT_FILE}")
    print(f"Lineas exportadas: {total}")

    groups = {}
    for row in exported_rows:
        text = normalize_text(row["texto_partida"])
        amount = number(row["importe_linea"])
        if not text or amount == 0:
            continue
        item = groups.setdefault(
            text,
            {
                "texto_partida_normalizado": text,
                "texto_partida_ejemplo": row["texto_partida"],
                "importes": [],
                "cantidades": [],
                "precios_unitarios": [],
                "clientes": set(),
                "obras": set(),
                "anios": set(),
            },
        )
        item["importes"].append(amount)
        item["cantidades"].append(number(row["cantidad"]))
        item["precios_unitarios"].append(number(row["precio_unitario"]))
        if row["cliente"]:
            item["clientes"].add(row["cliente"])
        if row["obra_detectada"]:
            item["obras"].add(row["obra_detectada"])
        if row["anio_backup"]:
            item["anios"].add(row["anio_backup"])

    ref_fields = [
        "texto_partida_normalizado",
        "texto_partida_ejemplo",
        "apariciones",
        "importe_min",
        "importe_mediana",
        "importe_max",
        "precio_unitario_mediana",
        "cantidad_mediana",
        "anios",
        "clientes_ejemplo",
        "obras_ejemplo",
    ]

    reference_rows = []
    with REF_FILE.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=ref_fields, delimiter=";")
        writer.writeheader()
        for item in sorted(groups.values(), key=lambda x: (-len(x["importes"]), x["texto_partida_normalizado"])):
            row = {
                "texto_partida_normalizado": item["texto_partida_normalizado"],
                "texto_partida_ejemplo": item["texto_partida_ejemplo"],
                "apariciones": len(item["importes"]),
                "importe_min": round(min(item["importes"]), 2),
                "importe_mediana": round(median(item["importes"]), 2),
                "importe_max": round(max(item["importes"]), 2),
                "precio_unitario_mediana": round(median(item["precios_unitarios"]), 2),
                "cantidad_mediana": round(median(item["cantidades"]), 2),
                "anios": ", ".join(sorted(item["anios"])),
                "clientes_ejemplo": " | ".join(sorted(item["clientes"])[:5]),
                "obras_ejemplo": " | ".join(sorted(item["obras"])[:5]),
            }
            writer.writerow(row)
            reference_rows.append(row)

    detail_rows = [
        {
            "anio_backup": row["anio_backup"],
            "numero_factura": row["numero_factura"],
            "fecha_factura": row["fecha_factura"],
            "cliente": row["cliente"],
            "obra_detectada": row["obra_detectada"],
            "texto_partida": row["texto_partida"],
            "cantidad": compact_number(row["cantidad"]),
            "precio_unitario": compact_number(row["precio_unitario"]),
            "importe_linea": compact_number(row["importe_linea"]),
            "observaciones": row["observaciones"],
        }
        for row in exported_rows
        if row["texto_partida"] and number(row["importe_linea"]) != 0
    ]

    build_html(reference_rows, detail_rows)

    print(f"Referencia: {REF_FILE}")
    print(f"Visor HTML: {HTML_FILE}")
    print(f"Textos de partida agrupados: {len(groups)}")
    if errors:
        print("Errores:")
        for name, error in errors:
            print(f"- {name}: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
