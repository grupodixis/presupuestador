import csv
import html
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


IN_FILE = Path("datos-privados/factusol/lineas-clasificadas-factusol.csv")
OUT_DIR = Path("datos-privados/factusol")
CLEAN_CSV = OUT_DIR / "referencia-presupuestacion-limpia.csv"
SUMMARY_CSV = OUT_DIR / "resumen-presupuestacion-limpia.csv"
HTML_FILE = OUT_DIR / "presupuestacion-limpia-factusol.html"

EXCLUDED_FAMILIES = {
    "Web / dominios / hosting",
}

GLOBAL_PATTERNS = [
    "certificacion adjunta",
    "certificación adjunta",
    "s/ certificacion",
    "s/ certificación",
    "segun certificacion",
    "según certificación",
    "anticipo",
    "liquidacion",
    "liquidación",
    "trabajos ejecutados segun expediente",
    "trabajos ejecutados según expediente",
]

NOISE_PATTERNS = [
    "sujeto pasivo",
    "impuesto sobre el valor añadido",
    "tipoimpuesto",
]

UNIT_RULES = [
    ("h", ["hora", "horas", "h.", "hs", "oficial", "peon", "peón", "mano de obra"]),
    ("ml", [" ml", "metro lineal", "metros lineales", "m.l", "m/l"]),
    ("m2", ["m2", "m²", "metro cuadrado", "metros cuadrados"]),
    ("kg", ["kg", "kilo", "kilos"]),
    ("ud", ["ud", "unidad", "unidades"]),
]

COMMERCIAL_FAMILIES = {
    "Barandillas / pasamanos",
    "Puertas / portones / cancelas",
    "Rejas / protecciones",
    "Escaleras / peldaños",
    "Estructuras metalicas",
    "Cerrajeria / herreria general",
    "Acero inoxidable",
    "Chapa / plegado / corte",
    "Aluminio / carpinteria aluminio",
    "Pergolas / marquesinas / cubiertas",
    "Galvanizado / pintura / acabados",
    "Mantenimiento / reparacion",
    "Montaje / instalacion",
    "Mano de obra herreria",
    "Transporte / desplazamientos",
    "Materiales genericos",
    "Pasarelas / plataformas",
}


def clean(value):
    return "" if value is None else str(value).strip()


def norm(value):
    value = clean(value).lower()
    value = value.translate(str.maketrans("áéíóúüñ", "aeiouun"))
    return re.sub(r"\s+", " ", value)


def money(value):
    try:
        return float(clean(value).replace(",", "."))
    except ValueError:
        return 0.0


def probable_unit(row, text):
    qty = money(row.get("cantidad"))
    for unit, tokens in UNIT_RULES:
        if any(norm(token) in text for token in tokens):
            return unit
    if qty == 1:
        return "ud/lote"
    if qty and qty != 1:
        return "cantidad FACTUSOL"
    return "lote"


def reliability(row, text):
    amount = money(row.get("importe_linea"))
    price = money(row.get("precio_unitario"))
    qty = money(row.get("cantidad"))
    family = row.get("tipo_trabajo", "")

    if family in EXCLUDED_FAMILIES:
        return "Excluir", "familia no industrial para este sistema"
    if any(token in text for token in map(norm, NOISE_PATTERNS)):
        return "Excluir", "texto fiscal o ruido contable"
    if any(token in text for token in map(norm, GLOBAL_PATTERNS)):
        return "Baja", "certificacion, anticipo o importe global sin desglose"
    if amount == 0:
        return "Baja", "linea sin importe facturado"
    if family == "Otros / pendiente clasificar":
        return "Media", "importe real pero familia pendiente de revisar"
    if price > 0 and qty > 0 and clean(row.get("texto_partida")):
        return "Alta", "linea con descripcion, cantidad y precio unitario"
    if amount > 0 and clean(row.get("texto_partida")):
        return "Media", "importe real con descripcion pero unidad poco clara"
    return "Baja", "datos insuficientes"


def usable(reliability_value, family):
    if reliability_value == "Alta":
        return "si"
    if reliability_value == "Media" and family in COMMERCIAL_FAMILIES:
        return "revisar"
    return "no"


def clean_description(value):
    value = clean(value).replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    return value[:500]


def safe(value):
    return html.escape(clean(value))


def write_html(summary_rows, clean_rows):
    summary_html = "\n".join(
        "<tr>"
        f"<td>{safe(row['familia_presupuesto'])}</td>"
        f"<td class='num'>{safe(row['lineas'])}</td>"
        f"<td class='num'>{safe(row['aprovechables_si'])}</td>"
        f"<td class='num'>{safe(row['aprovechables_revisar'])}</td>"
        f"<td class='num'>{float(row['importe_total']):,.2f} €</td>"
        f"<td class='num'>{float(row['mediana_importe_linea']):,.2f} €</td>"
        f"<td>{safe(row['unidades'])}</td>"
        "</tr>"
        for row in summary_rows
    )
    sample_rows = [row for row in clean_rows if row["aprovechable_para_regla"] in {"si", "revisar"}][:500]
    lines_html = "\n".join(
        "<tr>"
        f"<td>{safe(row['familia_presupuesto'])}</td>"
        f"<td>{safe(row['fiabilidad'])}</td>"
        f"<td>{safe(row['unidad_probable'])}</td>"
        f"<td>{safe(row['cliente'])}</td>"
        f"<td>{safe(row['obra_detectada'])}</td>"
        f"<td>{safe(row['descripcion_limpia'])}</td>"
        f"<td class='num'>{float(row['precio_unitario'] or 0):,.2f} €</td>"
        f"<td class='num'>{float(row['importe_linea'] or 0):,.2f} €</td>"
        f"<td>{safe(row['motivo_fiabilidad'])}</td>"
        "</tr>"
        for row in sample_rows
    )
    HTML_FILE.write_text(
        f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FACTUSOL limpio para presupuestacion</title>
  <style>
    body {{ margin:0; background:#f3efe6; color:#18212b; font-family:Arial,sans-serif; }}
    header {{ padding:32px 38px; background:linear-gradient(135deg,#15251f,#7c2d12); color:white; }}
    h1 {{ margin:0 0 8px; font-size:44px; letter-spacing:-.04em; }}
    main {{ padding:26px 38px; }}
    input {{ width:100%; padding:13px 14px; border:1px solid #d8cdbd; border-radius:12px; margin-bottom:16px; font-size:15px; }}
    table {{ width:100%; border-collapse:collapse; background:#fffaf0; box-shadow:0 16px 42px rgba(0,0,0,.08); margin-bottom:30px; }}
    th {{ text-align:left; background:#2d2a24; color:white; padding:11px; position:sticky; top:0; }}
    td {{ border-top:1px solid #e4d9c8; padding:10px; vertical-align:top; }}
    tr:nth-child(even) td {{ background:#fff; }}
    .num {{ text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }}
    .note {{ color:#667085; }}
  </style>
</head>
<body>
  <header>
    <h1>FACTUSOL limpio para presupuestacion</h1>
    <p>Lineas clasificadas por utilidad: alta, media, baja o excluir. Datos locales privados.</p>
  </header>
  <main>
    <input id="q" placeholder="Filtrar por familia, fiabilidad, cliente, obra, texto...">
    <h2>Resumen por familia</h2>
    <table>
      <thead><tr><th>Familia</th><th>Lineas</th><th>Si</th><th>Revisar</th><th>Importe total</th><th>Mediana linea</th><th>Unidades</th></tr></thead>
      <tbody>{summary_html}</tbody>
    </table>
    <h2>Lineas aprovechables o revisables</h2>
    <p class="note">Muestra limitada a 500 lineas para revision rapida. El CSV contiene todo.</p>
    <table>
      <thead><tr><th>Familia</th><th>Fiabilidad</th><th>Unidad</th><th>Cliente</th><th>Obra</th><th>Descripcion</th><th>Precio unit.</th><th>Importe</th><th>Motivo</th></tr></thead>
      <tbody>{lines_html}</tbody>
    </table>
  </main>
  <script>
    const q = document.getElementById('q');
    q.addEventListener('input', () => {{
      const needle = q.value.toLowerCase();
      document.querySelectorAll('tbody tr').forEach(tr => {{ tr.style.display = tr.innerText.toLowerCase().includes(needle) ? '' : 'none'; }});
    }});
  </script>
</body>
</html>
""",
        encoding="utf-8",
    )


def main():
    rows = list(csv.DictReader(IN_FILE.open(encoding="utf-8-sig"), delimiter=";"))
    clean_rows = []
    groups = defaultdict(lambda: {"amounts": [], "units": Counter(), "count": 0, "si": 0, "revisar": 0})

    for row in rows:
        text = norm(" ".join([row.get("texto_partida", ""), row.get("observaciones", "")]))
        unit = probable_unit(row, text)
        fiab, motivo = reliability(row, text)
        family = row.get("tipo_trabajo", "Otros / pendiente clasificar")
        use = usable(fiab, family)
        out = {
            "familia_presupuesto": family,
            "descripcion_limpia": clean_description(row.get("texto_partida")),
            "unidad_probable": unit,
            "fiabilidad": fiab,
            "motivo_fiabilidad": motivo,
            "aprovechable_para_regla": use,
            "anio_backup": row.get("anio_backup", ""),
            "numero_factura": row.get("numero_factura", ""),
            "fecha_factura": row.get("fecha_factura", ""),
            "cliente": row.get("cliente", ""),
            "obra_detectada": row.get("obra_detectada", ""),
            "cantidad": row.get("cantidad", ""),
            "precio_unitario": row.get("precio_unitario", ""),
            "importe_linea": row.get("importe_linea", ""),
            "observaciones": row.get("observaciones", ""),
            "origen_archivo": row.get("origen_archivo", ""),
        }
        clean_rows.append(out)

        group = groups[family]
        group["count"] += 1
        group["units"][unit] += 1
        value = money(row.get("importe_linea"))
        if value:
            group["amounts"].append(value)
        if use == "si":
            group["si"] += 1
        elif use == "revisar":
            group["revisar"] += 1

    clean_rows.sort(key=lambda row: (row["aprovechable_para_regla"] != "si", row["fiabilidad"], -money(row["importe_linea"])))
    with CLEAN_CSV.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(clean_rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(clean_rows)

    summary_rows = []
    for family, data in groups.items():
        amounts = data["amounts"] or [0]
        summary_rows.append(
            {
                "familia_presupuesto": family,
                "lineas": data["count"],
                "aprovechables_si": data["si"],
                "aprovechables_revisar": data["revisar"],
                "importe_total": round(sum(amounts), 2),
                "mediana_importe_linea": round(median(amounts), 2),
                "unidades": " | ".join(f"{unit}:{count}" for unit, count in data["units"].most_common(5)),
            }
        )
    summary_rows.sort(key=lambda row: (row["aprovechables_si"] + row["aprovechables_revisar"], row["lineas"]), reverse=True)

    with SUMMARY_CSV.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(summary_rows)

    write_html(summary_rows, clean_rows)

    print(f"CSV limpio: {CLEAN_CSV}")
    print(f"Resumen: {SUMMARY_CSV}")
    print(f"HTML: {HTML_FILE}")
    print("Fiabilidad:")
    print(Counter(row["fiabilidad"] for row in clean_rows))
    print("Aprovechable:")
    print(Counter(row["aprovechable_para_regla"] for row in clean_rows))


if __name__ == "__main__":
    main()
