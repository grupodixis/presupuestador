import os
import json
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def eur(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def create_excel():
    wb = Workbook()
    
    NAVY = "0F172A"
    GOLD = "B45309"
    SLATE_LIGHT = "F8FAFC"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"
    EDIT_FILL = "FEF9C3"
    GREEN_DARK = "15803D"

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    fill_edit = PatternFill(start_color=EDIT_FILL, end_color=EDIT_FILL, fill_type="solid")

    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_tot = Font(name="Segoe UI", size=10.5, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=10.5, bold=True, color=GOLD)
    font_green = Font(name="Segoe UI", size=9, bold=True, color=GREEN_DARK)

    border_thin = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1")
    )
    border_total = Border(
        top=Side(style="thin", color=NAVY),
        bottom=Side(style="double", color=NAVY)
    )

    # -------------------------------------------------------------
    # HOJA 1: PRESUPUESTO CLIENTE
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Cliente"
    ws1.views.sheetView[0].showGridLines = True

    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} • SUSTITUCIÓN CHAPA ALUMINIO BOÍNDER (VELSAT II - MAÓ)"
    ws1["B3"].font = font_title

    meta_rows = [
        ("REFERENCIA:", DATA["referencia"]),
        ("CLIENTE:", f"{DATA['cliente']['nombre']} · NIF: {DATA['cliente']['cif']}"),
        ("ADMINISTRADOR:", f"{DATA['cliente']['administrador']}"),
        ("DOMICILIO:", f"{DATA['cliente']['domicilio']}"),
        ("OBRA / UBICACIÓN:", f"{DATA['cliente']['obra']} · {DATA['cliente']['ubicacion']}"),
        ("FECHA DE EMISIÓN:", f"{DATA['fecha']} (Validez: {DATA['validez_dias']} días naturales)")
    ]

    for idx, (label, val) in enumerate(meta_rows, start=5):
        ws1[f"B{idx}"] = label
        ws1[f"B{idx}"].font = font_bold
        ws1[f"C{idx}"] = val
        ws1[f"C{idx}"].font = font_reg

    # Headers tabla cliente
    headers_cli = ["Nº", "DESCRIPCIÓN DEL TRABAJO / PARTIDA", "UD", "CANT.", "PRECIO UD (€)", "IMPORTE (€)"]
    start_row = 12
    for col_idx, h in enumerate(headers_cli, start=2):
        cell = ws1.cell(row=start_row, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if col_idx in [2, 4, 5] else ("right" if col_idx >= 6 else "left"), vertical="center")

    curr_row = start_row + 1
    item_rows = []
    for item in DATA["partidas"]:
        ws1[f"B{curr_row}"] = item["numero"]
        ws1[f"B{curr_row}"].font = font_bold
        ws1[f"B{curr_row}"].alignment = Alignment(horizontal="center", vertical="top")
        ws1[f"B{curr_row}"].border = border_thin

        ws1[f"C{curr_row}"] = f"{item['titulo']}\n{item['descripcion']}"
        ws1[f"C{curr_row}"].font = font_reg
        ws1[f"C{curr_row}"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws1[f"C{curr_row}"].border = border_thin

        ws1[f"D{curr_row}"] = item["unidad"]
        ws1[f"D{curr_row}"].font = font_bold
        ws1[f"D{curr_row}"].alignment = Alignment(horizontal="center", vertical="top")
        ws1[f"D{curr_row}"].border = border_thin

        ws1[f"E{curr_row}"] = item["cantidad"]
        ws1[f"E{curr_row}"].font = font_bold
        ws1[f"E{curr_row}"].alignment = Alignment(horizontal="right", vertical="top")
        ws1[f"E{curr_row}"].number_format = "#,##0.00"
        ws1[f"E{curr_row}"].border = border_thin

        ws1[f"F{curr_row}"] = item["precio_unitario"]
        ws1[f"F{curr_row}"].font = font_bold
        ws1[f"F{curr_row}"].alignment = Alignment(horizontal="right", vertical="top")
        ws1[f"F{curr_row}"].number_format = "#,##0.00 €"
        ws1[f"F{curr_row}"].border = border_thin

        ws1[f"G{curr_row}"] = f"=E{curr_row}*F{curr_row}"
        ws1[f"G{curr_row}"].font = font_bold
        ws1[f"G{curr_row}"].alignment = Alignment(horizontal="right", vertical="top")
        ws1[f"G{curr_row}"].number_format = "#,##0.00 €"
        ws1[f"G{curr_row}"].border = border_thin

        if item["numero"] == "1.01":
            ws1.row_dimensions[curr_row].height = 100
        elif item["numero"] == "1.02":
            ws1.row_dimensions[curr_row].height = 75
        else:
            ws1.row_dimensions[curr_row].height = 75
            
        item_rows.append(curr_row)
        curr_row += 1

    # Totales Cliente
    r_bi = curr_row + 1
    ws1[f"F{r_bi}"] = "BASE IMPONIBLE:"
    ws1[f"F{r_bi}"].font = font_bold
    ws1[f"F{r_bi}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_bi}"] = f"=SUM(G{item_rows[0]}:G{item_rows[-1]})"
    ws1[f"G{r_bi}"].font = font_bold
    ws1[f"G{r_bi}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_bi}"].number_format = "#,##0.00 €"
    ws1[f"G{r_bi}"].border = border_thin

    r_iva21 = r_bi + 1
    ws1[f"F{r_iva21}"] = "IVA General (21%):"
    ws1[f"F{r_iva21}"].font = font_reg
    ws1[f"F{r_iva21}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_iva21}"] = f"=G{r_bi}*0.21"
    ws1[f"G{r_iva21}"].font = font_reg
    ws1[f"G{r_iva21}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_iva21}"].number_format = "#,##0.00 €"
    ws1[f"G{r_iva21}"].border = border_thin

    r_tot21 = r_iva21 + 1
    ws1[f"F{r_tot21}"] = "TOTAL CON IVA (21%):"
    ws1[f"F{r_tot21}"].font = font_tot
    ws1[f"F{r_tot21}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_tot21}"] = f"=G{r_bi}+G{r_iva21}"
    ws1[f"G{r_tot21}"].font = font_tot
    ws1[f"G{r_tot21}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_tot21}"].fill = fill_tot
    ws1[f"G{r_tot21}"].number_format = "#,##0.00 €"
    ws1[f"G{r_tot21}"].border = border_total

    r_opt = r_tot21 + 2
    ws1[f"C{r_opt}"] = "NOTA IVA REDUCIDO (10%): Si la Comunidad aporta la declaración de uso residencial habitual (Art. 91.Uno.2.10º Ley IVA):"
    ws1[f"C{r_opt}"].font = font_sub
    ws1[f"F{r_opt}"] = "TOTAL CON IVA REDUCIDO (10%):"
    ws1[f"F{r_opt}"].font = font_bold
    ws1[f"F{r_opt}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_opt}"] = f"=G{r_bi}*1.10"
    ws1[f"G{r_opt}"].font = font_green
    ws1[f"G{r_opt}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_opt}"].number_format = "#,##0.00 €"
    ws1[f"G{r_opt}"].border = border_thin

    # -------------------------------------------------------------
    # HOJA 2: DESGLOSE INTERNO TÉCNICO Y COSTES
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Desglose Técnico Interno")
    ws2.views.sheetView[0].showGridLines = True

    ws2["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | ESTUDIO INTERNO DE COSTES Y PRODUCCIÓN"
    ws2["B2"].font = font_sub
    ws2["B3"] = f"ANÁLISIS DE COSTES DIRECTOS Y MARGEN • {DATA['codigo']} • CHAPA BOÍNDER VELSAT II"
    ws2["B3"].font = font_title

    h_cost = ["CATEGORÍA", "CONCEPTO DE COSTE", "DETALLE / OPERACIÓN", "UD", "CANT.", "COSTE UD (€)", "COSTE TOTAL (€)", "PROVEEDOR"]
    start_c_row = 6
    for c_idx, h in enumerate(h_cost, start=2):
        c = ws2.cell(row=start_c_row, column=c_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if c_idx in [5, 6] else ("right" if c_idx in [7, 8] else "left"))

    crow = start_c_row + 1
    cost_rows = []

    categories = [
        ("medios_auxiliares", "MEDIOS ELEVACIÓN"),
        ("materiales", "MATERIALES"),
        ("mano_de_obra", "MANO DE OBRA Y TRANS."),
        ("gestion_permisos", "GESTIÓN PERMISOS Y TASAS")
    ]

    for cat_key, cat_name in categories:
        for entry in DATA["desglose_costes_internos"][cat_key]:
            ws2[f"B{crow}"] = cat_name
            ws2[f"B{crow}"].font = font_bold
            ws2[f"B{crow}"].border = border_thin

            ws2[f"C{crow}"] = entry["concepto"]
            ws2[f"C{crow}"].font = font_bold
            ws2[f"C{crow}"].border = border_thin

            ws2[f"D{crow}"] = entry["detalle"]
            ws2[f"D{crow}"].font = font_reg
            ws2[f"D{crow}"].border = border_thin

            ws2[f"E{crow}"] = entry["unidad"]
            ws2[f"E{crow}"].font = font_reg
            ws2[f"E{crow}"].alignment = Alignment(horizontal="center")
            ws2[f"E{crow}"].border = border_thin

            ws2[f"F{crow}"] = entry["cantidad"]
            ws2[f"F{crow}"].font = font_bold
            ws2[f"F{crow}"].alignment = Alignment(horizontal="right")
            ws2[f"F{crow}"].number_format = "#,##0.00"
            ws2[f"F{crow}"].border = border_thin

            ws2[f"G{crow}"] = entry["coste_unitario"]
            ws2[f"G{crow}"].font = font_bold
            ws2[f"G{crow}"].alignment = Alignment(horizontal="right")
            ws2[f"G{crow}"].number_format = "#,##0.00 €"
            ws2[f"G{crow}"].border = border_thin

            ws2[f"H{crow}"] = f"=F{crow}*G{crow}"
            ws2[f"H{crow}"].font = font_bold
            ws2[f"H{crow}"].alignment = Alignment(horizontal="right")
            ws2[f"H{crow}"].number_format = "#,##0.00 €"
            ws2[f"H{crow}"].border = border_thin

            ws2[f"I{crow}"] = entry["proveedor"]
            ws2[f"I{crow}"].font = font_reg
            ws2[f"I{crow}"].border = border_thin

            cost_rows.append(crow)
            crow += 1

    # Totales Internos
    crow += 1
    ws2[f"G{crow}"] = "COSTE DIRECTO TOTAL:"
    ws2[f"G{crow}"].font = font_tot
    ws2[f"G{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"] = f"=SUM(H{cost_rows[0]}:H{cost_rows[-1]})"
    ws2[f"H{crow}"].font = font_tot
    ws2[f"H{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"].fill = fill_edit
    ws2[f"H{crow}"].number_format = "#,##0.00 €"
    ws2[f"H{crow}"].border = border_thin

    crow += 1
    ws2[f"G{crow}"] = "VENTA CLIENTE (BASE):"
    ws2[f"G{crow}"].font = font_tot
    ws2[f"G{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"] = f"='Presupuesto Cliente'!G{r_bi}"
    ws2[f"H{crow}"].font = font_tot
    ws2[f"H{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"].number_format = "#,##0.00 €"
    ws2[f"H{crow}"].border = border_thin

    crow += 1
    ws2[f"G{crow}"] = "BENEFICIO BRUTO HAM:"
    ws2[f"G{crow}"].font = font_tot_gold
    ws2[f"G{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"] = f"=H{crow-1}-H{crow-2}"
    ws2[f"H{crow}"].font = font_tot_gold
    ws2[f"H{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"].fill = fill_tot
    ws2[f"H{crow}"].number_format = "#,##0.00 €"
    ws2[f"H{crow}"].border = border_thin

    crow += 1
    ws2[f"G{crow}"] = "MARGEN S/ VENTA (%):"
    ws2[f"G{crow}"].font = font_green
    ws2[f"G{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"] = f"=(H{crow-1}/H{crow-2})*100"
    ws2[f"H{crow}"].font = font_green
    ws2[f"H{crow}"].alignment = Alignment(horizontal="right")
    ws2[f"H{crow}"].number_format = "0.00 \"%\""
    ws2[f"H{crow}"].border = border_thin

    # Ajustar anchos
    ws1.column_dimensions["B"].width = 8
    ws1.column_dimensions["C"].width = 54
    ws1.column_dimensions["D"].width = 12
    ws1.column_dimensions["E"].width = 12
    ws1.column_dimensions["F"].width = 18
    ws1.column_dimensions["G"].width = 20

    ws2.column_dimensions["B"].width = 24
    ws2.column_dimensions["C"].width = 42
    ws2.column_dimensions["D"].width = 48
    ws2.column_dimensions["E"].width = 10
    ws2.column_dimensions["F"].width = 12
    ws2.column_dimensions["G"].width = 16
    ws2.column_dimensions["H"].width = 18
    ws2.column_dimensions["I"].width = 32

    xlsx_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0064_Boinder_Velsat2_Mahon.xlsx")
    wb.save(xlsx_path)
    return xlsx_path

def create_html_and_pdf():
    tot = DATA["totales"]
    cond = DATA["condiciones_comerciales"]

    partidas_html_cli = ""
    for item in DATA["partidas"]:
        desc_lines = item["descripcion"].split("\n")
        desc_formatted = f"<strong>{desc_lines[0]}</strong><ul style='margin:3px 0 0 14px; padding:0;'>"
        for line in desc_lines[1:]:
            clean = line.strip().lstrip("•").strip()
            if clean:
                desc_formatted += f"<li>{clean}</li>"
        desc_formatted += "</ul>"

        partidas_html_cli += f"""
        <tr>
          <td class="center bold">{item['numero']}</td>
          <td>
            <strong>{item['titulo']}</strong>
            <div class="desc">{desc_formatted}</div>
          </td>
          <td class="center bold">{item['unidad']}</td>
          <td class="right bold">{item['cantidad']:.2f}</td>
          <td class="right">{eur(item['precio_unitario'])}</td>
          <td class="right bold">{eur(item['importe'])}</td>
        </tr>
        """

    html_cliente = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presupuesto {DATA['codigo']} — Chapa Boínder Edificio Velsat II (Maó)</title>
  <style>
    @page {{ size: A4 portrait; margin: 8mm 10mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, Helvetica, sans-serif; color: #1e293b; margin: 0; font-size: 8.5pt; line-height: 1.28; background: #fff; }}
    .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2.5px solid #0f172a; padding-bottom: 5px; margin-bottom: 6px; }}
    .brand-group {{ display: flex; align-items: center; gap: 10px; }}
    .logo {{ width: 40px; height: 40px; }}
    .subbrand {{ font-size: 7.5pt; color: #b45309; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }}
    .brand {{ font-size: 12.5pt; font-weight: 800; color: #0f172a; margin-top: 1px; }}
    .company-info {{ text-align: right; font-size: 7.4pt; color: #475569; line-height: 1.22; }}
    h1 {{ font-size: 10.2pt; color: #0f172a; margin: 0 0 4px 0; font-weight: 800; text-transform: uppercase; }}
    .banner-def {{ background: #f0fdf4; border-left: 4px solid #16a34a; padding: 4px 8px; font-size: 7.8pt; margin-bottom: 6px; color: #166534; }}
    table.meta {{ width: 100%; border-collapse: collapse; margin-bottom: 6px; font-size: 7.8pt; }}
    table.meta td {{ padding: 3px 5px; border: 1px solid #cbd5e1; }}
    table.meta td.lbl {{ background: #f1f5f9; font-weight: 700; width: 18%; color: #334155; }}
    table.items {{ width: 100%; border-collapse: collapse; margin-bottom: 6px; }}
    table.items th {{ background: #0f172a; color: #fff; padding: 4px 6px; font-size: 7.8pt; text-align: left; }}
    table.items td {{ padding: 4.5px 6px; border-bottom: 1px solid #cbd5e1; vertical-align: top; font-size: 7.8pt; }}
    .desc {{ font-size: 7.4pt; color: #475569; margin-top: 2px; line-height: 1.25; }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .totals-wrap {{ display: flex; justify-content: flex-end; margin-bottom: 6px; }}
    table.totals {{ width: 50%; border-collapse: collapse; }}
    table.totals td {{ padding: 3px 6px; border: 1px solid #cbd5e1; font-size: 7.8pt; }}
    table.totals .grand {{ background: #fef3c7; font-weight: 800; font-size: 9pt; color: #0f172a; }}
    table.totals .reducido {{ background: #f0fdf4; color: #166534; font-weight: 700; }}
    .conds {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 5px 8px; font-size: 7.3pt; margin-top: 4px; }}
    .conds h3 {{ margin: 0 0 2px 0; font-size: 7.8pt; color: #0f172a; text-transform: uppercase; letter-spacing: 0.04em; }}
    .conds-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
    .conds ul {{ margin: 2px 0 0 12px; padding: 0; }}
    .conds li {{ margin-bottom: 2px; }}
    .photos-block {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 5px; border: 1px solid #cbd5e1; padding: 5px; border-radius: 4px; background: #fff; }}
    .photos-block img {{ width: 100%; height: 95px; object-fit: cover; border-radius: 3px; border: 1px solid #94a3b8; }}
    .photos-block .caption {{ font-size: 6.8pt; color: #475569; text-align: center; margin-top: 2px; }}
    .footer-note {{ margin-top: 5px; font-size: 6.8pt; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 3px; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand-group">
      <img src="logo-ham.svg" class="logo" alt="HAM">
      <div>
        <div class="subbrand">DIXIS RECURSOS Y SOLUCIONES S.L. · CIF B57825432</div>
        <div class="brand">HAM ESTRUCTURAS METÁLICAS MENORCA</div>
      </div>
    </div>
    <div class="company-info">
      Av. Circunval·lació, 11 · Pol. Ind. Sant Lluís, 07710 (Menorca)<br>
      Tel: +34 971 35 20 18 · WhatsApp: +34 669 769 541<br>
      info@hamenorca.com · www.hamenorca.com
    </div>
  </div>

  <h1>PRESUPUESTO {DATA['codigo']} — REPOSICIÓN DE CHAPA DE ALUMINIO VERDE EN BOÍNDER Y GESTIÓN DE PERMISOS · EDIFICIO VELSAT II (MAÓ)</h1>
  <div class="banner-def">
    <strong>OBJETO DE LOS TRABAJOS:</strong> Suministro, conformado a medida en taller e instalación en altura con <strong>2 días de camión cesta</strong> y <strong>tramitación de permisos y tasas municipales (OVP) ante el Ajuntament de Maó</strong> para el entrepaño/peto del boínder en Camí des Castell, 255.
  </div>

  <table class="meta">
    <tr>
      <td class="lbl">Cliente</td>
      <td><strong>{DATA['cliente']['nombre']}</strong> (NIF: {DATA['cliente']['cif']})</td>
      <td class="lbl">Referencia</td>
      <td><strong>{DATA['referencia']}</strong></td>
    </tr>
    <tr>
      <td class="lbl">Administración</td>
      <td>{DATA['cliente']['administrador']}</td>
      <td class="lbl">Fecha Emisión</td>
      <td>{DATA['fecha']}</td>
    </tr>
    <tr>
      <td class="lbl">Ubicación Obra</td>
      <td>{DATA['cliente']['domicilio']}</td>
      <td class="lbl">Validez Oferta</td>
      <td>{DATA['validez_dias']} días naturales</td>
    </tr>
    <tr>
      <td class="lbl">Medios y Calidad</td>
      <td colspan="3">Chapa aluminio conformada CNC con goterón y rigidizadores · Lacado Qualicoat Seaside marino · Tornillería y remaches inox A2/A4 · Sellador MS alta intemperie · 2 jornadas de cesta PEMP · Tramitación OVP Ajuntament de Maó</td>
    </tr>
  </table>

  <table class="items">
    <thead>
      <tr>
        <th class="center" style="width:6%">Nº</th>
        <th style="width:54%">Concepto y Descripción Técnica Detallada</th>
        <th class="center" style="width:6%">Ud.</th>
        <th class="right" style="width:10%">Cant.</th>
        <th class="right" style="width:12%">Precio Ud.</th>
        <th class="right" style="width:12%">Subtotal</th>
      </tr>
    </thead>
    <tbody>
      {partidas_html_cli}
    </tbody>
  </table>

  <div class="totals-wrap">
    <table class="totals">
      <tr>
        <td class="bold">BASE IMPONIBLE:</td>
        <td class="right bold">{eur(tot['base_imponible'])}</td>
      </tr>
      <tr>
        <td>IVA General ({tot['iva_general_pct']:.0f}%):</td>
        <td class="right">{eur(tot['iva_importe_general'])}</td>
      </tr>
      <tr class="grand">
        <td>TOTAL PRESUPUESTO (IVA 21%):</td>
        <td class="right">{eur(tot['total_con_iva_general'])}</td>
      </tr>
      <tr class="reducido">
        <td>TOTAL CON IVA REDUCIDO (10% - Comunidad)*:</td>
        <td class="right bold">{eur(tot['total_con_iva_reducido'])}</td>
      </tr>
    </table>
  </div>

  <div class="conds">
    <h3>Condiciones de Ejecución, Permisos Municipales y Régimen Fiscal</h3>
    <div class="conds-grid">
      <div>
        <ul>
          <li><strong>Forma de pago:</strong> {cond['forma_pago']}</li>
          <li><strong>Plazos:</strong> {cond['plazo_ejecucion']}</li>
          <li><strong>Garantía:</strong> {cond['garantia']}</li>
        </ul>
      </div>
      <div>
        <ul>
          <li><strong>*Régimen IVA Reducido (10%):</strong> {cond['nota_iva_reducido']}</li>
          <li><strong>Permisos y Vía Pública:</strong> {cond['licencias_permisos']}</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="photos-block">
    <div>
      <img src="foto-nocturna-localizacion.jpg" alt="Localización Fachada Boínder Edificio Velsat II">
      <div class="caption">Localización de la fachada en Camí des Castell, 255 (Zona afectada señalada)</div>
    </div>
    <div>
      <img src="foto-boinder-detalle.jpg" alt="Detalle Chapa Desprendida en Boínder">
      <div class="caption">Detalle del peto/entrepaño del boínder sin chapa (soporte a sanear y reponer)</div>
    </div>
  </div>

  <div class="footer-note">
    HAM Estructuras Metálicas Menorca · Dixis Recursos y Soluciones S.L. · Documento comercial expedido en Mahón el {DATA['fecha']}.
  </div>
</body>
</html>
"""

    # 2. HTML INTERNO TÉCNICO
    filas_costes = ""
    categories = [
        ("medios_auxiliares", "MEDIOS DE ELEVACIÓN (CESTA)"),
        ("materiales", "MATERIALES Y CONSUMIBLES"),
        ("mano_de_obra", "MANO DE OBRA Y LOGÍSTICA"),
        ("gestion_permisos", "GESTIÓN PERMISOS Y TASAS AYTO.")
    ]
    for cat_key, cat_name in categories:
        for c in DATA["desglose_costes_internos"][cat_key]:
            filas_costes += f"""
            <tr>
              <td class="bold">{cat_name}</td>
              <td class="bold">{c['concepto']}</td>
              <td>{c['detalle']}</td>
              <td class="center">{c['unidad']}</td>
              <td class="right bold">{c['cantidad']:.2f}</td>
              <td class="right">{eur(c['coste_unitario'])}</td>
              <td class="right bold">{eur(c['coste_total'])}</td>
              <td>{c['proveedor']}</td>
            </tr>
            """

    html_interno = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Estudio Interno Técnico {DATA['codigo']} — Chapa Boínder Velsat II</title>
  <style>
    @page {{ size: A4 landscape; margin: 8mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; margin: 0; font-size: 8pt; line-height: 1.3; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0f172a; padding-bottom: 4px; margin-bottom: 5px; }}
    .brand {{ font-size: 10.5pt; font-weight: 800; color: #0f172a; }}
    .tag {{ background: #0f172a; color: #fff; padding: 2px 6px; font-size: 7.5pt; font-weight: 700; border-radius: 3px; }}
    h1 {{ font-size: 10.5pt; color: #0f172a; margin: 0 0 3px 0; }}
    h2 {{ font-size: 8.5pt; color: #0f172a; margin: 6px 0 2px 0; border-bottom: 1.5px solid #b45309; padding-bottom: 2px; text-transform: uppercase; }}
    .banner {{ background: #ecfdf5; border-left: 4px solid #10b981; padding: 4px 6px; font-size: 7.5pt; color: #065f46; margin-bottom: 5px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; font-size: 7.4pt; }}
    th {{ background: #0f172a; color: #fff; padding: 4px 5px; font-size: 7.2pt; text-align: left; }}
    td {{ padding: 3px 5px; border-bottom: 1px solid #cbd5e1; vertical-align: top; }}
    .right {{ text-align: right; }}
    .center {{ text-align: center; }}
    .bold {{ font-weight: 700; }}
    .green {{ color: #15803d; font-weight: 700; }}
    .tot {{ background: #fef3c7; font-weight: 800; }}
    .grid-2 {{ display: grid; grid-template-columns: 1.65fr 1fr; gap: 10px; }}
    .card {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 5px 8px; font-size: 7.4pt; border-radius: 4px; margin-bottom: 5px; }}
    .card h3 {{ margin: 0 0 2px 0; font-size: 7.6pt; color: #0f172a; text-transform: uppercase; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand">HAM ESTRUCTURAS METÁLICAS · DOCUMENTO INTERNO DE COSTES Y PRODUCCIÓN</div>
    <div><span class="tag">USO INTERNO EXCLUSIVO</span> <span class="tag">{DATA['codigo']}</span></div>
  </div>

  <h1>ESTUDIO ECONÓMICO Y TÉCNICO: REPOSICIÓN DE CHAPA EN BOÍNDER · CP VELSAT 2 (MAÓ)</h1>
  <div class="banner">
    <strong>CLIENTE: COMUNIDAD DE PROPIETARIOS VELSAT 2 (Camí des Castell 255, Maó)</strong> | Administración: Advocats de Menorca (David Alzina Riera). Presupuesto con <strong>2 días de camión cesta</strong> y <strong>tramitación de permisos y tasas OVP en Ajuntament de Maó</strong>.
  </div>

  <div class="grid-2">
    <div>
      <h2>1. Desglose Detallado de Costes Directos de Ejecución</h2>
      <table>
        <thead>
          <tr>
            <th>Capítulo</th>
            <th>Concepto de Coste</th>
            <th>Detalle Técnico / Operación</th>
            <th class="center">Ud.</th>
            <th class="right">Cant.</th>
            <th class="right">Coste Ud.</th>
            <th class="right">Total Coste</th>
            <th>Proveedor / Asignación</th>
          </tr>
        </thead>
        <tbody>
          {filas_costes}
          <tr class="tot">
            <td colspan="6" class="right bold">TOTAL COSTE DIRECTO DE EJECUCIÓN (A):</td>
            <td class="right bold" style="background:#fef9c3;">{eur(tot['coste_directo_total'])}</td>
            <td>Coste real sin margen</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div>
      <h2>2. Análisis de Rentabilidad y Resumen Económico</h2>
      <div class="card">
        <h3>Métricas de Margen y Precio de Venta</h3>
        <table>
          <tr>
            <td>Coste Directo Total:</td>
            <td class="right bold">{eur(tot['coste_directo_total'])}</td>
          </tr>
          <tr>
            <td>Venta Cliente (Base Imponible):</td>
            <td class="right bold" style="color:#0f172a;">{eur(tot['base_imponible'])}</td>
          </tr>
          <tr style="background:#ecfdf5;">
            <td class="bold green">Beneficio Bruto HAM:</td>
            <td class="right bold green">+{eur(tot['beneficio_bruto'])}</td>
          </tr>
          <tr>
            <td class="bold">Margen Comercial sobre Venta:</td>
            <td class="right bold green">{tot['margen_sobre_venta_pct']:.2f}%</td>
          </tr>
          <tr>
            <td>Recargo sobre Coste Directo:</td>
            <td class="right bold">{tot['recargo_sobre_coste_pct']:.2f}%</td>
          </tr>
          <tr>
            <td>IVA General 21%:</td>
            <td class="right">{eur(tot['iva_importe_general'])} (Total: {eur(tot['total_con_iva_general'])})</td>
          </tr>
          <tr style="background:#f0fdf4;">
            <td class="bold">IVA Reducido 10% (Comunidad):</td>
            <td class="right bold green">{eur(tot['iva_importe_reducido'])} (Total: {eur(tot['total_con_iva_reducido'])})</td>
          </tr>
        </table>
      </div>

      <h2>3. Plan Operativo y Calendario de Trabajos</h2>
      <div class="card">
        <ul>
          <li><strong>Fase 0 (Permisos Municipales):</strong> Tramitación telemática ante el Ajuntament de Maó y la Policía Local de la solicitud de Ocupación de Vía Pública (OVP) con camión cesta en Camí des Castell 255. Memoria, croquis de paso peatonal y abono de tasas. Colocación de placas R-308 con 48h de antelación.</li>
          <li><strong>Jornada 1 (Cesta):</strong> Posicionamiento del camión cesta y balizamiento en Camí des Castell 255. Ascenso de 2 oficiales para replanteo milimétrico de cotas, toma de muestra exacta de color RAL verde de carpintería, saneado y limpieza del soporte existente retirando restos de adhesivos antiguos.</li>
          <li><strong>Intermedio Taller:</strong> Plegado CNC de chapa aluminio marino e=1,5-2 mm tipo bandeja con rigidizadores y goterón, lacado termoendurecible verde Qualicoat Seaside. Preparación de perfilería de rastrelado y fijaciones inox A2/A4.</li>
          <li><strong>Jornada 2 (Cesta):</strong> Retorno del camión cesta y corte/balizamiento vial. Izado de la chapa, anclaje mecánico firme sobre rastreles y sellado perimetral continuo con polímero MS de alta resistencia UV. Retirada de protecciones y limpieza.</li>
        </ul>
      </div>
    </div>
  </div>
</body>
</html>
"""

    cli_html = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    int_html = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    cli_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    int_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")

    with open(cli_html, "w", encoding="utf-8") as f:
        f.write(html_cliente)
    with open(int_html, "w", encoding="utf-8") as f:
        f.write(html_interno)

    if os.path.exists(CHROME_PATH):
        for h_path, p_path in [(cli_html, cli_pdf), (int_html, int_pdf)]:
            subprocess.run([
                CHROME_PATH, "--headless", "--disable-gpu",
                "--no-pdf-header-footer", f"--print-to-pdf={p_path}", h_path
            ], check=False)

    return cli_html, int_html, cli_pdf, int_pdf

def create_readme():
    tot = DATA["totales"]
    content = f"""# Presupuesto {DATA['codigo']} — Reposición de Chapa de Aluminio Verde en Boínder y Gestión de Permisos (Edificio Velsat II, Maó)

## Cliente y Datos Generales
- **Código:** {DATA['codigo']}
- **Referencia:** {DATA['referencia']}
- **Cliente:** {DATA['cliente']['nombre']} (NIF: {DATA['cliente']['cif']})
- **Administrador:** {DATA['cliente']['administrador']}
- **Domicilio Obra:** {DATA['cliente']['domicilio']}
- **Fecha:** {DATA['fecha']}
- **Validez:** {DATA['validez_dias']} días naturales
- **Medios Auxiliares:** 2 jornadas completas de camión cesta / PEMP con operador y balizamiento vial en vía pública
- **Permisos Municipales:** Tramitación completa y abono de tasas de OVP ante el Ajuntament de Maó y reserva de espacio con Policía Local

## Resumen del Trabajo
Reparación de urgencia / reposición de la chapa frontal del entrepaño/peto del boínder de una vivienda del edificio Velsat II, desprendida por los temporales en Camí des Castell, 255 (Maó), incluyendo la gestión integral de permisos municipales.
- **Fase Permisos (Ajuntament de Maó):** Tramitación telemática de licencia de ocupación de vía pública (OVP), memoria, croquis de balizamiento/paso peatonal, abono de tasas municipales y colocación de placas de prohibido estacionar 48h antes.
- **Jornada 1 de Cesta:** Replanteo milimétrico en altura, toma de muestras de color RAL de carpintería existente (verde), saneado y adecuación del soporte y rastrelado.
- **Taller HAM:** Conformado de nueva chapa de aluminio de alta resistencia marina e=1,5/2 mm mediante plegado CNC en bandeja con pestañas de rigidización, engatillado y goterón inferior, con lacado Qualicoat Seaside verde.
- **Jornada 2 de Cesta:** Izado, montaje y anclaje mecánico firme con tornillería/remaches inoxidables A2/A4 y arandelas EPDM, más sellado perimetral estanco continuo con polímero MS de alta intemperie y resistencia UV.

## Resumen Económico

| Partida | Concepto | Coste Directo | Venta Cliente (PVP) | Beneficio Bruto | Margen s/ Venta |
|---|---|---:|---:|---:|---:|
| **1.01** | Suministro, conformado CNC e instalación de chapa aluminio verde boínder | 1.060,00 € | 1.480,00 € | +420,00 € | 28.38% |
| **1.02** | Medios auxiliares de elevación: 2 jornadas de camión cesta / PEMP | 700,00 € | 1.160,00 € | +460,00 € | 39.66% |
| **1.03** | Gestión técnica, tramitación y abono de tasas de OVP en Ajuntament de Maó | 180,00 € | 290,00 € | +110,00 € | 37.93% |
| **TOTAL** | **Presupuesto Completo (Base Imponible)** | **{eur(tot['coste_directo_total'])}** | **{eur(tot['base_imponible'])}** | **+{eur(tot['beneficio_bruto'])}** | **{tot['margen_sobre_venta_pct']:.2f}%** |

- **Base Imponible:** {eur(tot['base_imponible'])}
- **IVA General (21%):** {eur(tot['iva_importe_general'])} → **Total: {eur(tot['total_con_iva_general'])}**
- **Opción IVA Reducido (10% - Comunidad):** {eur(tot['iva_importe_reducido'])} → **Total: {eur(tot['total_con_iva_reducido'])}** *(al amparo del Art. 91.Uno.2.10º Ley IVA)*

## Archivos Generados
- `presupuesto-cliente.html` / `presupuesto-cliente.pdf`: Documento comercial para la Comunidad de Propietarios y Administrador.
- `presupuesto-interno-tecnico.html` / `presupuesto-interno-tecnico.pdf`: Desglose interno técnico y económico para taller y dirección.
- `Presupuesto_P2026_0064_Boinder_Velsat2_Mahon.xlsx`: Hoja de cálculo completa con fórmulas activas, pestaña cliente y pestaña interna de costes.
- `datos.json`: Fuente de datos estructurada del presupuesto.
- `foto-nocturna-localizacion.jpg`: Imagen de localización de la fachada del edificio.
- `foto-boinder-detalle.jpg`: Fotografía de detalle de la zona del boínder afectada.
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    return readme_path

if __name__ == "__main__":
    xlsx = create_excel()
    cli_h, int_h, cli_p, int_p = create_html_and_pdf()
    rd = create_readme()
    print("Archivos generados con éxito:")
    for f in [xlsx, cli_h, cli_p, int_h, int_p, rd]:
        print(f" - {f}")
