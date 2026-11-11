import json
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)


def fmt_eur(val):
    s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} €"


def svg_icon(tipo):
    if tipo == "practicable_2_hojas_desiguales":
        return """
        <svg viewBox="0 0 64 64" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
          <rect x="6" y="4" width="52" height="56" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>
          <rect x="10" y="8" width="18" height="48" fill="#e2e8f0" stroke="#64748b" stroke-width="1.4"/>
          <rect x="28" y="8" width="26" height="48" fill="#e2e8f0" stroke="#64748b" stroke-width="1.4"/>
          <polyline points="10,8 28,32 10,56" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
          <polyline points="54,8 28,32 54,56" fill="none" stroke="#64748b" stroke-width="1.1" stroke-dasharray="2,2"/>
          <rect x="29.5" y="29" width="2" height="6" rx="0.8" fill="#475569"/>
        </svg>"""
    if tipo == "practicable_2_hojas":
        return """
        <svg viewBox="0 0 64 64" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
          <rect x="6" y="10" width="52" height="44" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>
          <rect x="10" y="14" width="22" height="36" fill="#e2e8f0" stroke="#64748b" stroke-width="1.4"/>
          <rect x="32" y="14" width="22" height="36" fill="#e2e8f0" stroke="#64748b" stroke-width="1.4"/>
          <polyline points="10,14 32,32 10,50" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
          <polyline points="54,14 32,32 54,50" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
          <rect x="29" y="29" width="2" height="6" rx="0.8" fill="#475569"/>
        </svg>"""
    if tipo == "mallorquina_4_hojas":
        lamas = ""
        for y in range(12, 54, 4):
            lamas += (
                f'<line x1="11" y1="{y}" x2="18" y2="{y}" stroke="#6b8e78" stroke-width="1"/>'
                f'<line x1="22" y1="{y}" x2="29" y2="{y}" stroke="#6b8e78" stroke-width="1"/>'
                f'<line x1="35" y1="{y}" x2="42" y2="{y}" stroke="#6b8e78" stroke-width="1"/>'
                f'<line x1="46" y1="{y}" x2="53" y2="{y}" stroke="#6b8e78" stroke-width="1"/>'
            )
        return f"""
        <svg viewBox="0 0 64 64" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
          <rect x="6" y="4" width="52" height="56" fill="#f1f5f1" stroke="#5b7a66" stroke-width="2"/>
          <rect x="9" y="8" width="11" height="48" fill="#dce6de" stroke="#5b7a66" stroke-width="1.2"/>
          <rect x="20" y="8" width="11" height="48" fill="#dce6de" stroke="#5b7a66" stroke-width="1.2"/>
          <rect x="33" y="8" width="11" height="48" fill="#dce6de" stroke="#5b7a66" stroke-width="1.2"/>
          <rect x="44" y="8" width="11" height="48" fill="#dce6de" stroke="#5b7a66" stroke-width="1.2"/>
          {lamas}
          <circle cx="32" cy="32" r="2.2" fill="#334155"/>
        </svg>"""
    if tipo == "mallorquina_2_hojas":
        lamas = ""
        for y in range(16, 48, 4):
            lamas += (
                f'<line x1="13" y1="{y}" x2="29" y2="{y}" stroke="#6b8e78" stroke-width="1.1"/>'
                f'<line x1="35" y1="{y}" x2="51" y2="{y}" stroke="#6b8e78" stroke-width="1.1"/>'
            )
        return f"""
        <svg viewBox="0 0 64 64" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
          <rect x="6" y="10" width="52" height="44" fill="#f1f5f1" stroke="#5b7a66" stroke-width="2"/>
          <rect x="10" y="14" width="22" height="36" fill="#dce6de" stroke="#5b7a66" stroke-width="1.3"/>
          <rect x="32" y="14" width="22" height="36" fill="#dce6de" stroke="#5b7a66" stroke-width="1.3"/>
          {lamas}
        </svg>"""
    # premarco
    return """
    <svg viewBox="0 0 64 64" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="10" width="44" height="44" fill="none" stroke="#475569" stroke-width="3"/>
      <rect x="14" y="14" width="36" height="36" fill="#f8fafc" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,2"/>
      <line x1="4" y1="16" x2="10" y2="16" stroke="#475569" stroke-width="2"/>
      <line x1="4" y1="48" x2="10" y2="48" stroke="#475569" stroke-width="2"/>
      <line x1="54" y1="16" x2="60" y2="16" stroke="#475569" stroke-width="2"/>
      <line x1="54" y1="48" x2="60" y2="48" stroke="#475569" stroke-width="2"/>
    </svg>"""


def create_excel():
    wb = Workbook()

    navy = "0F172A"
    blue = "0369A1"
    slate_light = "F8FAFC"
    border_hex = "CBD5E1"
    total_fill = "EFF6FF"
    green_fill = "F0FDF4"

    fill_hdr = PatternFill(start_color=navy, end_color=navy, fill_type="solid")
    fill_alt = PatternFill(start_color=slate_light, end_color=slate_light, fill_type="solid")
    fill_tot = PatternFill(start_color=total_fill, end_color=total_fill, fill_type="solid")
    fill_grn = PatternFill(start_color=green_fill, end_color=green_fill, fill_type="solid")

    f_title = Font(name="Segoe UI", size=14, bold=True, color=navy)
    f_sub = Font(name="Segoe UI", size=10, bold=True, color=blue)
    f_hdr = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    f_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    f_reg = Font(name="Segoe UI", size=9, color="1E293B")
    f_ital = Font(name="Segoe UI", size=8.5, italic=True, color="64748B")
    f_tot = Font(name="Segoe UI", size=10, bold=True, color=navy)

    thin = Side(style="thin", color=border_hex)
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # Sheet 1: Presupuesto Cliente V2
    ws1 = wb.active
    ws1.title = "Presupuesto V2"
    ws1["A1"] = f"ALUFAC · {DATA['expediente']['empresa']['razon_social']}"
    ws1["A1"].font = f_title
    ws1["A2"] = f"CIF: {DATA['expediente']['empresa']['cif']} · {DATA['expediente']['empresa']['direccion']} · Tel: {DATA['expediente']['empresa']['telefono']}"
    ws1["A2"].font = f_ital

    ws1["A4"] = f"Presupuesto: {DATA['expediente']['referencia_alufac']} (Exp. {DATA['expediente']['codigo']})"
    ws1["A4"].font = f_sub
    ws1["E4"] = f"Fecha: {DATA['expediente']['fecha_formateada']}"
    ws1["E4"].font = f_reg
    ws1["E4"].alignment = Alignment(horizontal="right")

    ws1["A5"] = f"Cliente: {DATA['cliente']['nombre']} | Proyecto / Obra: {DATA['cliente']['proyecto']}"
    ws1["A5"].font = f_bold
    ws1["E5"] = f"Sustituye a: {DATA['expediente']['referencia_origen']}"
    ws1["E5"].font = f_ital
    ws1["E5"].alignment = Alignment(horizontal="right")

    r = 7
    headers = ["Nº", "Tipología", "Descripción y especificaciones", "Ud.", "Precio Ud.", "Total"]
    for col, h in enumerate(headers, 1):
        c = ws1.cell(row=r, column=col, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
        c.border = border
        c.alignment = Alignment(horizontal="center" if col in [1, 4, 5, 6] else "left", vertical="center")

    start_data = r + 1
    for idx, p in enumerate(DATA["partidas"]):
        r += 1
        vals = [p["orden"], p["titulo"], p["descripcion"], p["unidades"], p["precio_unitario"]]
        for col, v in enumerate(vals, 1):
            c = ws1.cell(row=r, column=col, value=v)
            c.font = f_reg
            c.border = border
            if idx % 2 == 1:
                c.fill = fill_alt
            if col == 1 or col == 4:
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif col == 5:
                c.number_format = '#,##0.00 "€"'
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        c_tot = ws1.cell(row=r, column=6, value=f"=D{r}*E{r}")
        c_tot.font = f_bold
        c_tot.border = border
        c_tot.number_format = '#,##0.00 "€"'
        c_tot.alignment = Alignment(horizontal="right", vertical="center")
        if idx % 2 == 1:
            c_tot.fill = fill_alt

    end_data = r
    r += 2
    for label, formula in [
        ("Base imponible", f"=SUM(F{start_data}:F{end_data})"),
        ("IVA (21%)", f"=ROUND(F{r}*0.21, 2)"),
        ("Total presupuesto", f"=F{r}+F{r+1}"),
    ]:
        c_lbl = ws1.cell(row=r, column=5, value=label)
        c_val = ws1.cell(row=r, column=6, value=formula)
        c_lbl.font = f_tot if "Total" in label else f_bold
        c_val.font = f_tot if "Total" in label else f_bold
        c_lbl.border = border
        c_val.border = border
        c_val.number_format = '#,##0.00 "€"'
        c_lbl.alignment = Alignment(horizontal="right")
        c_val.alignment = Alignment(horizontal="right")
        if "Total" in label:
            c_lbl.fill = fill_tot
            c_val.fill = fill_tot
        r += 1

    widths = [6, 20, 68, 8, 15, 16]
    for i, w in enumerate(widths, 1):
        ws1.column_dimensions[get_column_letter(i)].width = w

    # Sheet 2: Comparativa V1 vs V2 y Escandallo
    ws2 = wb.create_sheet("Comparativa y Técnico")
    ws2["A1"] = "ANÁLISIS INTERNO Y COMPARATIVA V1 (PRE-56EADEB1) vs V2 (P-2026-0056)"
    ws2["A1"].font = f_title

    ws2["A3"] = "1. Verificación Técnica Cortizo A 70 (Puerta 2000×2000 mm, hojas desiguales 800 + 1200 mm)"
    ws2["A3"].font = f_sub
    ws2["A4"] = DATA["verificacion_tecnica_a70"]["calculo_hoja_mayor_1200x2000"]["conclusion"]
    ws2["A4"].font = f_reg
    ws2["A4"].alignment = Alignment(wrap_text=True)

    r = 6
    ws2.cell(row=r, column=1, value="2. Comparativa Económica por Partida").font = f_sub
    r += 1
    h2 = ["Nº", "Concepto", "V1 Blanco (€)", "V2 Actualizado (€)", "Diferencia (€)", "Justificación Técnica / Cálculo"]
    for col, h in enumerate(h2, 1):
        c = ws2.cell(row=r, column=col, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
        c.border = border

    s2_start = r + 1
    for p in DATA["partidas"]:
        r += 1
        c1 = ws2.cell(row=r, column=1, value=p["orden"])
        c2 = ws2.cell(row=r, column=2, value=p["titulo"])
        c3 = ws2.cell(row=r, column=3, value=p["precio_original"])
        c4 = ws2.cell(row=r, column=4, value=p["total"])
        c5 = ws2.cell(row=r, column=5, value=f"=D{r}-C{r}")
        c6 = ws2.cell(row=r, column=6, value=p["nota_interna"])
        for col, c in enumerate([c1, c2, c3, c4, c5, c6], 1):
            c.font = f_reg
            c.border = border
            if col in [3, 4, 5]:
                c.number_format = '#,##0.00 "€"'
                c.alignment = Alignment(horizontal="right", vertical="center")
            elif col == 6:
                c.alignment = Alignment(wrap_text=True, vertical="center")
    s2_end = r
    r += 1
    ws2.cell(row=r, column=2, value="TOTAL BASE IMPONIBLE").font = f_tot
    for col, let in [(3, "C"), (4, "D"), (5, "E")]:
        c = ws2.cell(row=r, column=col, value=f"=SUM({let}{s2_start}:{let}{s2_end})")
        c.font = f_tot
        c.fill = fill_grn
        c.border = border
        c.number_format = '#,##0.00 "€"'

    for i, w in enumerate([6, 22, 16, 18, 16, 72], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    xlsx_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0056_ALUFAC_Maria_Mora_V2.xlsx")
    wb.save(xlsx_path)
    print(f"Excel guardado: {xlsx_path}")


def generate_html_files():
    emp = DATA["expediente"]["empresa"]
    exp = DATA["expediente"]
    cli = DATA["cliente"]
    tot = DATA["totales"]

    rows_html = ""
    for p in DATA["partidas"]:
        tags_html = "".join(f'<span class="pill">{t}</span>' for t in p["tags"])
        rows_html += f"""
        <tr>
          <td class="col-icon">
            <div class="icon-box">{svg_icon(p["tipo_apertura"])}</div>
          </td>
          <td class="col-desc">
            <div class="item-head"><span class="num-badge">{p["orden"]}</span> <strong>{p["titulo"]}</strong></div>
            <div class="item-text">{p["descripcion"]}</div>
            <div class="pills">{tags_html}</div>
          </td>
          <td class="col-ud">{p["unidades"]}</td>
          <td class="col-pu">{fmt_eur(p["precio_unitario"])}</td>
          <td class="col-tot"><strong>{fmt_eur(p["total"])}</strong></td>
        </tr>"""

    html_cliente = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Alufac · Presupuesto {cli['nombre']} ({exp['referencia_alufac']})</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 11mm 13mm 12mm 13mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      color: #0f172a;
      font-size: 8.8pt;
      line-height: 1.38;
      margin: 0;
      padding: 0;
      background: #ffffff;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 10px;
      margin-bottom: 12px;
    }}
    .brand-left img {{
      height: 36px;
      display: block;
      margin-bottom: 5px;
    }}
    .brand-left .sub {{
      font-size: 8.2pt;
      color: #475569;
    }}
    .brand-right {{
      text-align: right;
      font-size: 8pt;
      color: #334155;
      line-height: 1.4;
    }}
    .brand-right strong {{
      color: #0f172a;
      font-size: 8.6pt;
    }}
    .meta-card {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 10px 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 12px;
    }}
    .meta-col h4 {{
      margin: 0 0 5px 0;
      font-size: 7.5pt;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      color: #0369a1;
    }}
    .meta-col p {{
      margin: 2px 0;
      font-size: 8.4pt;
      color: #1e293b;
    }}
    table.items {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
    }}
    table.items thead th {{
      background: #f1f5f9;
      color: #334155;
      font-size: 7.8pt;
      font-weight: 700;
      text-align: left;
      padding: 6px 8px;
      border-top: 1px solid #cbd5e1;
      border-bottom: 1px solid #cbd5e1;
    }}
    table.items thead th.right {{ text-align: right; }}
    table.items thead th.center {{ text-align: center; }}
    table.items tbody td {{
      padding: 7px 8px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: middle;
    }}
    table.items tbody tr {{ break-inside: avoid; }}
    .col-icon {{ width: 64px; text-align: center; }}
    .icon-box {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 3px;
    }}
    .item-head {{
      font-size: 9pt;
      margin-bottom: 2px;
      color: #0f172a;
    }}
    .num-badge {{
      display: inline-block;
      width: 16px;
      height: 16px;
      line-height: 16px;
      text-align: center;
      border-radius: 50%;
      background: #e2e8f0;
      color: #0f172a;
      font-size: 7.5pt;
      font-weight: 700;
      margin-right: 4px;
    }}
    .item-text {{
      font-size: 8.1pt;
      color: #334155;
      margin-bottom: 4px;
    }}
    .pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }}
    .pill {{
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      color: #475569;
      border-radius: 4px;
      padding: 1px 6px;
      font-size: 7.2pt;
    }}
    .col-ud {{ width: 38px; text-align: center; font-size: 8.6pt; }}
    .col-pu {{ width: 82px; text-align: right; font-size: 8.6pt; white-space: nowrap; }}
    .col-tot {{ width: 88px; text-align: right; font-size: 9pt; white-space: nowrap; }}

    .bottom-block {{
      break-inside: avoid;
      margin-top: 8px;
    }}
    .totals-wrap {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 12px;
    }}
    .totals-box {{
      width: 265px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 9px 12px;
      background: #ffffff;
    }}
    .tot-row {{
      display: flex;
      justify-content: space-between;
      font-size: 8.5pt;
      padding: 2.5px 0;
      color: #334155;
    }}
    .tot-row.final {{
      border-top: 1.5px solid #0f172a;
      margin-top: 5px;
      padding-top: 6px;
      font-size: 11pt;
      font-weight: 800;
      color: #0f172a;
    }}
    .conditions {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 9px 13px;
      margin-bottom: 12px;
    }}
    .conditions h4 {{
      margin: 0 0 5px 0;
      font-size: 7.8pt;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      color: #0f172a;
    }}
    .conditions ol {{
      margin: 0;
      padding-left: 16px;
      font-size: 7.8pt;
      color: #334155;
      line-height: 1.4;
    }}
    .conditions li {{ margin-bottom: 2px; }}
    .signs {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .sign-box {{
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 9px 12px;
      min-height: 64px;
      font-size: 7.9pt;
      color: #475569;
    }}
    .sign-box strong {{ color: #0f172a; display: block; margin-bottom: 2px; }}
    .sign-line {{ margin-top: 18px; color: #64748b; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand-left">
      <img src="{emp['logo_url']}" alt="ALUFAC">
      <div class="sub">{emp['subtitulo']}</div>
    </div>
    <div class="brand-right">
      <strong>{emp['razon_social']}</strong><br>
      NIF: {emp['cif']}<br>
      {emp['direccion']}<br>
      <strong>Tel / WhatsApp:</strong> {emp['telefono']}<br>
      <strong>Email:</strong> {emp['email']} · <strong>Web:</strong> {emp['web']}
    </div>
  </div>

  <div class="meta-card">
    <div class="meta-col">
      <h4>Datos del presupuesto</h4>
      <p><strong>Nº Presupuesto:</strong> {exp['referencia_alufac']} <span style="color:#64748b;font-size:7.6pt;">(Exp. {exp['codigo']} · Sustituye a {exp['referencia_origen']})</span></p>
      <p><strong>Fecha de emisión:</strong> {exp['fecha_formateada']}</p>
      <p><strong>Proyecto / Obra:</strong> {cli['proyecto']}</p>
    </div>
    <div class="meta-col">
      <h4>Cliente / Ubicación</h4>
      <p><strong>Cliente:</strong> {cli['nombre']}</p>
      <p><strong>Dirección de entrega:</strong> {cli['direccion_entrega']}</p>
      <p><strong>Garantía:</strong> {exp['garantia']}</p>
    </div>
  </div>

  <table class="items">
    <thead>
      <tr>
        <th class="center">Tipología</th>
        <th>Descripción y especificaciones</th>
        <th class="center">Ud.</th>
        <th class="right">Precio ud.</th>
        <th class="right">Total</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>

  <div class="bottom-block">
    <div class="totals-wrap">
      <div class="totals-box">
        <div class="tot-row"><span>Base imponible:</span><span><strong>{fmt_eur(tot['base_imponible'])}</strong></span></div>
        <div class="tot-row"><span>IVA (21%):</span><span><strong>{fmt_eur(tot['iva_21'])}</strong></span></div>
        <div class="tot-row final"><span>Total presupuesto:</span><span>{fmt_eur(tot['total_presupuesto'])}</span></div>
      </div>
    </div>

    <div class="conditions">
      <h4>Condiciones generales del presupuesto</h4>
      <ol>
        <li>Validez de la oferta: {exp['validez_dias']} días naturales desde la fecha de emisión del presupuesto.</li>
        <li>Forma de pago: {exp['forma_pago']}.</li>
        <li>Plazo de entrega estimado: {exp['plazo_entrega']}.</li>
        <li>Garantía: 2 años en perfiles de aluminio/PVC, mecanismos de herrajes y estanqueidad conforme a normativa CTE/UNE.</li>
        <li>El presupuesto comprende la fabricación, suministro de premarcos indicados, transporte y colocación en obra accesible en la isla de Menorca.</li>
        <li>El reparto de hojas activas/pasivas, manos de apertura y tipología exacta de premarcos (compartidos o independientes) se confirmará definitivamente en replanteo de obra antes de fabricación.</li>
        <li>No se incluyen trabajos de albañilería, pintura, remates de yeso, medios auxiliares especiales (grúa exterior o andamios) ni desescombro salvo indicación expresa.</li>
      </ol>
    </div>

    <div class="signs">
      <div class="sign-box">
        <strong>Por ALUFAC ({emp['razon_social']})</strong>
        Carpintería de aluminio y PVC · Sant Lluís, Menorca
        <div class="sign-line">Firma y sello de la empresa</div>
      </div>
      <div class="sign-box">
        <strong>Conforme y aceptación del cliente</strong>
        D./Dña: {cli['nombre']}
        <div class="sign-line">Fecha: ___ / ___ / 202_ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Firma del cliente</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

    with open(os.path.join(BASE_DIR, "presupuesto-cliente.html"), "w", encoding="utf-8") as f:
        f.write(html_cliente)

    # Versión Interna Técnica
    v_a70 = DATA["verificacion_tecnica_a70"]
    comp_rows = ""
    for p in DATA["partidas"]:
        diff = p["total"] - p["precio_original"]
        comp_rows += f"""
        <tr>
          <td class="center">{p['orden']}</td>
          <td><strong>{p['titulo']}</strong></td>
          <td class="right">{fmt_eur(p['precio_original'])}</td>
          <td class="right"><strong>{fmt_eur(p['total'])}</strong></td>
          <td class="right">{'+' if diff >= 0 else ''}{fmt_eur(diff)}</td>
          <td>{p['nota_interna']}</td>
        </tr>"""

    html_tecnico = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Informe Interno Técnico · {exp['codigo']} ({exp['referencia_alufac']})</title>
  <style>
    @page {{ size: A4 portrait; margin: 12mm 13mm; }}
    body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt; color: #1e293b; line-height: 1.4; margin: 0; }}
    .hdr {{ border-bottom: 2px solid #0f172a; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; }}
    .hdr h1 {{ margin: 0; font-size: 13pt; color: #0f172a; }}
    .badge {{ background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 8pt; }}
    .box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0284c7; padding: 9px 12px; margin-bottom: 12px; border-radius: 4px; }}
    .box.ok {{ border-left-color: #16a34a; background: #f0fdf4; }}
    h2 {{ font-size: 10pt; color: #0f172a; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px; margin: 12px 0 6px 0; text-transform: uppercase; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 8pt; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 5px 7px; vertical-align: top; }}
    th {{ background: #0f172a; color: #fff; text-align: left; }}
    .right {{ text-align: right; white-space: nowrap; }}
    .center {{ text-align: center; }}
    .tot {{ background: #eff6ff; font-weight: 700; }}
    ul {{ margin: 4px 0; padding-left: 18px; }}
  </style>
</head>
<body>
  <div class="hdr">
    <div>
      <h1>INFORME TÉCNICO INTERNO · {exp['codigo']} ({exp['referencia_alufac']})</h1>
      <div>Cliente: <strong>{cli['nombre']}</strong> · Obra: <strong>{cli['proyecto']}</strong> · Fecha: {exp['fecha_formateada']}</div>
    </div>
    <div><span class="badge">USO INTERNO ALUFAC</span></div>
  </div>

  <h2>1. Verificación Técnica Serie Cortizo A 70 (Puerta 2000 × 2000 mm, hojas 800 + 1200 mm)</h2>
  <div class="box ok">
    <strong>Resultado: APTO TÉCNICAMENTE EN CORTIZO A 70 (PVC 5 cámaras, marco 70 mm)</strong><br>
    • <strong>Límites oficiales por hoja en Cortizo A 70:</strong> Puerta 700–1.300 mm ancho × 600–2.500 mm alto (máx. 160 kg/hoja) | Balconera 360–1.300 mm × 600–2.400 mm (máx. 130 kg/hoja).<br>
    • <strong>Comprobación dimensional:</strong> Hoja pasiva 800 mm y hoja activa 1.200 mm quedan ambas dentro del límite 700–1.300 mm; altura 2.000 mm &le; 2.400/2.500 mm.<br>
    • <strong>Comprobación de peso con vidrio {v_a70['calculo_hoja_mayor_1200x2000']['composicion_vidrio']}:</strong> vidrio neto ≈ 58,2 kg + perfil PVC/refuerzo acero ≈ 30 kg = <strong>~88 kg en la hoja de 1200 mm</strong> (por debajo de 130 kg balconera y 160 kg puerta).<br>
    • <strong>Requisitos de montaje/taller:</strong> Perfil inversor central con falleba en hoja pasiva (800 mm), bisagras regulables de alta carga (130–160 kg) en la hoja de 1.200 mm y validación final del sentido de apertura y zona eólica.
  </div>

  <h2>2. Comparativa Económica V1 ({exp['referencia_origen']}) vs V2 ({exp['referencia_alufac']})</h2>
  <table>
    <thead>
      <tr>
        <th class="center">Nº</th>
        <th>Partida</th>
        <th class="right">V1 Original</th>
        <th class="right">V2 Actualizado</th>
        <th class="right">Delta</th>
        <th>Criterio y Desglose de Cálculo</th>
      </tr>
    </thead>
    <tbody>
      {comp_rows}
      <tr class="tot">
        <td colspan="2">BASE IMPONIBLE</td>
        <td class="right">{fmt_eur(tot['base_imponible_original'])}</td>
        <td class="right">{fmt_eur(tot['base_imponible'])}</td>
        <td class="right">+{fmt_eur(tot['base_imponible'] - tot['base_imponible_original'])}</td>
        <td>Incremento neto base imponible (+48,5%)</td>
      </tr>
      <tr>
        <td colspan="2">IVA (21%)</td>
        <td class="right">{fmt_eur(tot['iva_original'])}</td>
        <td class="right">{fmt_eur(tot['iva_21'])}</td>
        <td class="right">+{fmt_eur(tot['iva_21'] - tot['iva_original'])}</td>
        <td></td>
      </tr>
      <tr class="tot">
        <td colspan="2">TOTAL PRESUPUESTO (IVA INCLUIDO)</td>
        <td class="right">{fmt_eur(tot['total_original'])}</td>
        <td class="right">{fmt_eur(tot['total_presupuesto'])}</td>
        <td class="right">+{fmt_eur(tot['total_presupuesto'] - tot['total_original'])}</td>
        <td></td>
      </tr>
    </tbody>
  </table>

  <h2>3. Puntos a Confirmar en Obra (Replanteo)</h2>
  <ul>
    <li><strong>Premarcos:</strong> Se han incluido 3 premarcos (uno por cada hueco: 2000×2000 a 165 €, 1500×1200 a 120 €, 1200×1200 a 105 € = 390 €). Si los dos huecos dobles (PVC interior + Mallorquina exterior) precisan premarcos independientes separados, añadir +285,00 € (+2 uds).</li>
    <li><strong>Puerta A 70 800+1200:</strong> Confirmar si la hoja activa/paso habitual es la de 1.200 mm o la de 800 mm, y sentido de apertura interior/exterior e izquierda/derecha.</li>
    <li><strong>Mallorquina 4 hojas 2000×2000:</strong> Confirmar si el reparto es simétrico (4×500 mm, 2 hojas plegadas por lado) con cerradura GESA central y Qualicoat Seaside RAL 6021 (ambiente marino Menorca, tornillería inox AISI 316).</li>
  </ul>
</body>
</html>
"""
    with open(os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html"), "w", encoding="utf-8") as f:
        f.write(html_tecnico)


def render_pdfs():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name in ["presupuesto-cliente", "presupuesto-interno-tecnico"]:
            html_path = os.path.join(BASE_DIR, f"{name}.html")
            pdf_path = os.path.join(BASE_DIR, f"{name}.pdf")
            page = browser.new_page()
            page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
            page.pdf(
                path=pdf_path,
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"},
            )
            page.close()
            print(f"PDF guardado: {pdf_path}")
        browser.close()


if __name__ == "__main__":
    create_excel()
    generate_html_files()
    render_pdfs()
