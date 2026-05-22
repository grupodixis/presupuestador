import csv
import html
import re
from collections import defaultdict
from pathlib import Path
from statistics import median


IN_FILE = Path("datos-privados/factusol/historico-facturas-factusol.csv")
OUT_DIR = Path("datos-privados/factusol")
TYPES_CSV = OUT_DIR / "tipos-trabajo-factusol.csv"
LINES_CSV = OUT_DIR / "lineas-clasificadas-factusol.csv"
HTML_FILE = OUT_DIR / "tipos-trabajo-factusol.html"


CATEGORIES = [
    ("Web / dominios / hosting", ["dominio", "hosting", "alojamiento web", "correo electronico", "correo electrónico", "web evolution", "cuota servicio"]),
    ("Electricidad / telecomunicaciones", ["electric", "cable", "wimax", "nodo", "arqueta", "toma de", "toma tiempo", "toma tiempos", "canalizacion", "canalización", "cuadro", "conmutador"]),
    ("Climatizacion / ventilacion", ["climatizacion", "climatización", "aire acondicionado", "ventilacion", "ventilación", "extractor", "conducto"]),
    ("Equipamiento aeroportuario / electronico", ["aena", "aeropuerto", "twr", "equipaje", "electronico", "electrónico", "equipamiento"]),
    ("Pasarelas / plataformas", ["pasarela", "plataforma", "eds", "ulma"]),
    ("Barandillas / pasamanos", ["barandilla", "pasamanos", "quitamiedos", "baranda"]),
    ("Puertas / portones / cancelas", ["puerta", "porton", "portón", "cancela", "corredera", "batiente", "automatismo"]),
    ("Rejas / protecciones", ["reja", "barrotes", "proteccion", "protección", "antiintrusion", "anti intrusión"]),
    ("Escaleras / peldaños", ["escalera", "peldaño", "peldano", "zanca", "tramex"]),
    ("Estructuras metalicas", ["estructura", "viga", "pilar", "heb", "ipe", "ipn", "perfil laminado", "bastidor", "cercha"]),
    ("Cerrajeria / herreria general", ["cerrajeria", "cerrajería", "herreria", "herrería"]),
    ("Acero inoxidable", ["inox", "inoxidable", "aisi", "316", "304"]),
    ("Chapa / plegado / corte", ["chapa", "plegado", "plegar", "corte", "cortado", "laser", "láser", "desarrollo"]),
    ("Aluminio / carpinteria aluminio", ["aluminio", "ventana", "cerramiento", "mallorquina", "persiana", "lacado", "cristal", "vidrio"]),
    ("Pergolas / marquesinas / cubiertas", ["pergola", "pérgola", "marquesina", "cubierta", "coberta", "panel sandwich", "panel sándwich", "tejado"]),
    ("Galvanizado / pintura / acabados", ["galvanizado", "galvanizar", "pintura", "imprimacion", "imprimación", "epoxi", "lacado", "acabado", "ral "]),
    ("Mantenimiento / reparacion", ["mantenimiento", "reparacion", "reparación", "ajuste", "sustitucion", "sustitución", "recambio"]),
    ("Montaje / instalacion", ["montaje", "instalacion", "instalación", "colocacion", "colocación", "instalar"]),
    ("Mano de obra herreria", ["oficial herreria", "oficial herrería", "mano de obra", "operario", "peon", "peón"]),
    ("Transporte / desplazamientos", ["transporte", "desplazamiento", "portes", "entrega", "camion", "camión"]),
    ("Materiales genericos", ["materiales", "pequeños materiales", "pequenos materiales", "tubo", "perfil", "pletina", "tornilleria", "tornillería"]),
    ("Certificaciones globales sin detalle", ["certificacion adjunta", "certificación adjunta", "certificacio", "certificació", "certificacion nº", "certificación nº", "segun certificacion", "según certificación"]),
]


def clean(value):
    return "" if value is None else str(value).strip()


def normalize(value):
    value = clean(value).lower()
    replacements = str.maketrans("áéíóúüñ", "aeiouun")
    value = value.translate(replacements)
    return re.sub(r"\s+", " ", value)


def amount(value):
    try:
        return float(clean(value).replace(",", "."))
    except ValueError:
        return 0.0


def classify(row):
    text = normalize(" ".join([row.get("texto_partida", ""), row.get("observaciones", ""), row.get("obra_detectada", "")]))
    matches = []
    for name, keywords in CATEGORIES:
        if any(normalize(keyword) in text for keyword in keywords):
            matches.append(name)

    if matches:
        return matches[0], " | ".join(matches)
    return "Otros / pendiente clasificar", ""


def safe(value):
    return html.escape(clean(value))


def write_html(summary_rows, classified_rows):
    top_examples = classified_rows[:200]
    rows_html = "\n".join(
        "<tr>"
        f"<td>{safe(row['tipo_trabajo'])}</td>"
        f"<td class='num'>{safe(row['lineas'])}</td>"
        f"<td class='num'>{safe(row['facturas'])}</td>"
        f"<td class='num'>{float(row['importe_total']):,.2f} €</td>"
        f"<td class='num'>{float(row['importe_mediana']):,.2f} €</td>"
        f"<td>{safe(row['ejemplos'])}</td>"
        "</tr>"
        for row in summary_rows
    )
    examples_html = "\n".join(
        "<tr>"
        f"<td>{safe(row['tipo_trabajo'])}</td>"
        f"<td>{safe(row['cliente'])}</td>"
        f"<td>{safe(row['obra_detectada'])}</td>"
        f"<td>{safe(row['texto_partida'])}</td>"
        f"<td class='num'>{amount(row['importe_linea']):,.2f} €</td>"
        "</tr>"
        for row in top_examples
    )
    HTML_FILE.write_text(
        f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tipos de trabajo FACTUSOL</title>
  <style>
    body {{ margin:0; background:#f6f1e8; color:#202124; font-family:Arial,sans-serif; }}
    header {{ padding:32px 38px; background:#27312f; color:#fff; }}
    h1 {{ margin:0; font-size:42px; letter-spacing:-.04em; }}
    main {{ padding:26px 38px; }}
    input {{ width:100%; padding:13px 14px; border:1px solid #d6cabc; border-radius:12px; margin-bottom:16px; font-size:15px; }}
    table {{ width:100%; border-collapse:collapse; background:#fffaf0; box-shadow:0 15px 45px rgba(0,0,0,.08); margin-bottom:28px; }}
    th {{ text-align:left; background:#9a3412; color:#fff; padding:11px; position:sticky; top:0; }}
    td {{ border-top:1px solid #e7dccb; padding:10px; vertical-align:top; }}
    tr:nth-child(even) td {{ background:#fff; }}
    .num {{ text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }}
    .muted {{ color:#667085; }}
  </style>
</head>
<body>
  <header>
    <h1>Tipos de trabajo detectados</h1>
    <p class="muted">Clasificacion inicial por palabras clave sobre facturas FACTUSOL. Revisable y mejorable.</p>
  </header>
  <main>
    <input id="q" placeholder="Filtrar por tipo, cliente, obra o texto...">
    <h2>Resumen por tipo</h2>
    <table id="summary">
      <thead><tr><th>Tipo</th><th>Lineas</th><th>Facturas</th><th>Importe total</th><th>Importe mediana</th><th>Ejemplos</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    <h2>Ejemplos principales</h2>
    <table id="examples">
      <thead><tr><th>Tipo</th><th>Cliente</th><th>Obra</th><th>Texto partida</th><th>Importe</th></tr></thead>
      <tbody>{examples_html}</tbody>
    </table>
  </main>
  <script>
    const q = document.getElementById('q');
    q.addEventListener('input', () => {{
      const needle = q.value.toLowerCase();
      document.querySelectorAll('tbody tr').forEach(tr => {{
        tr.style.display = tr.innerText.toLowerCase().includes(needle) ? '' : 'none';
      }});
    }});
  </script>
</body>
</html>
""",
        encoding="utf-8",
    )


def main():
    rows = list(csv.DictReader(IN_FILE.open(encoding="utf-8-sig"), delimiter=";"))
    classified_rows = []
    groups = defaultdict(lambda: {"amounts": [], "invoices": set(), "examples": [], "rows": 0})

    for row in rows:
        if amount(row.get("importe_linea")) == 0 and not clean(row.get("texto_partida")):
            continue
        tipo, matches = classify(row)
        out = dict(row)
        out["tipo_trabajo"] = tipo
        out["tipos_detectados"] = matches
        classified_rows.append(out)

        group = groups[tipo]
        value = amount(row.get("importe_linea"))
        if value != 0:
            group["amounts"].append(value)
        group["invoices"].add(f"{row.get('origen_archivo')}:{row.get('tipo_factura')}:{row.get('numero_factura')}")
        group["rows"] += 1
        if len(group["examples"]) < 5 and clean(row.get("texto_partida")):
            group["examples"].append(clean(row.get("texto_partida")).replace("\n", " ")[:160])

    fieldnames = list(classified_rows[0].keys())
    with LINES_CSV.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(classified_rows)

    summary_rows = []
    for tipo, data in groups.items():
        amounts = data["amounts"] or [0]
        summary_rows.append(
            {
                "tipo_trabajo": tipo,
                "lineas": data["rows"],
                "facturas": len(data["invoices"]),
                "importe_total": round(sum(amounts), 2),
                "importe_min": round(min(amounts), 2),
                "importe_mediana": round(median(amounts), 2),
                "importe_max": round(max(amounts), 2),
                "ejemplos": " | ".join(data["examples"]),
            }
        )
    summary_rows.sort(key=lambda row: row["lineas"], reverse=True)

    with TYPES_CSV.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys()), delimiter=";")
        writer.writeheader()
        writer.writerows(summary_rows)

    classified_rows.sort(key=lambda row: amount(row.get("importe_linea")), reverse=True)
    write_html(summary_rows, classified_rows)

    print(f"Tipos: {TYPES_CSV}")
    print(f"Lineas clasificadas: {LINES_CSV}")
    print(f"HTML: {HTML_FILE}")
    for row in summary_rows:
        print(f"{row['lineas']:>5}  {row['tipo_trabajo']}  {row['importe_total']:>12.2f}")


if __name__ == "__main__":
    main()
