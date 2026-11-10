import os
import sys
import json
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def create_excel():
    wb = Workbook()
    
    NAVY = "0F172A"        # Cabecera principal
    BLUE = "1D4ED8"        # Acento azul técnico
    SLATE_LIGHT = "F8FAFC" # Fila alterna
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "EFF6FF"   # Azul suave
    SECTION_FILL = "F1F5F9"
    HIGHLIGHT_FILL = "FEF3C7"
    
    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_sec = PatternFill(start_color=SECTION_FILL, end_color=SECTION_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    fill_hl = PatternFill(start_color=HIGHLIGHT_FILL, end_color=HIGHLIGHT_FILL, fill_type="solid")
    
    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9, bold=True, color=BLUE)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=9.5, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=8.5, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_tot = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_tot_blue = Font(name="Segoe UI", size=10, bold=True, color=BLUE)

    border_thin = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    border_total = Border(
        top=Side(style='thin', color=NAVY),
        bottom=Side(style='double', color=NAVY)
    )

    # -------------------------------------------------------------------------
    # HOJA 1: PRESUPUESTO CLIENTE ACCIONA (60 ML - 120,47 €/ML)
    # -------------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Acciona EDAR"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} • LÍNEA DE VIDA LUX-TOP® FSE 2003 (60 ML) • EDAR FERRERIES"
    ws1["B3"].font = font_title
    
    ws1["B5"] = "REFERENCIA:"
    ws1["C5"] = DATA["referencia"]
    ws1["B6"] = "CLIENTE:"
    ws1["C6"] = f"{DATA['cliente']['nombre']} (Atn: {DATA['cliente']['contacto_tecnico']})"
    ws1["B7"] = "UBICACIÓN:"
    ws1["C7"] = DATA["cliente"]["ubicacion"]
    ws1["B8"] = "FECHA:"
    ws1["C8"] = DATA["fecha"]
    ws1["B9"] = "HOMOLOGACIÓN:"
    ws1["C9"] = "SISTEMA OFICIAL EXCLUSIVO LUX-TOP® (UNE-EN 795:2012 Tipo C / CEN/TS 16415:2013)"
    
    for r in range(5, 10):
        ws1[f"B{r}"].font = font_bold
        ws1[f"C{r}"].font = font_reg

    ws1["B11"] = f"DESGLOSE DE PARTIDAS: SISTEMA ANTICAÍDAS EN PISCINA EDAR FERRERIES (60 ML LLAVE EN MANO)"
    ws1["B11"].font = font_sec
    
    headers_client = ["Nº", "Partida y Especificación Técnica Oficial LUX-TOP®", "Ud.", "Cantidad", "Precio Unitario", "Subtotal"]
    for c_idx, h in enumerate(headers_client, start=2):
        cell = ws1.cell(row=12, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[12].height = 22

    row_cur = 13
    for p in DATA["modalidad_1_paso_manual"]["partidas"]:
        ws1.cell(row=row_cur, column=2, value=p["id"]).font = font_bold
        ws1.cell(row=row_cur, column=2).alignment = Alignment(horizontal="center", vertical="top")
        
        desc_cell = ws1.cell(row=row_cur, column=3, value=f"{p['concepto']}\n{p['descripcion']}")
        desc_cell.font = font_reg
        desc_cell.alignment = Alignment(wrap_text=True, vertical="top")
        
        ws1.cell(row=row_cur, column=4, value=p["unidad"]).font = font_reg
        ws1.cell(row=row_cur, column=4).alignment = Alignment(horizontal="center", vertical="top")
        
        cant_cell = ws1.cell(row=row_cur, column=5, value=p["cantidad"])
        cant_cell.font = font_reg
        cant_cell.alignment = Alignment(horizontal="right", vertical="top")
        cant_cell.number_format = '#,##0.00'
        
        p_cell = ws1.cell(row=row_cur, column=6, value=p["precio_cliente"])
        p_cell.font = font_reg
        p_cell.alignment = Alignment(horizontal="right", vertical="top")
        p_cell.number_format = '#,##0.00 €'
        
        sub_cell = ws1.cell(row=row_cur, column=7, value=f"=E{row_cur}*F{row_cur}")
        sub_cell.font = font_bold
        sub_cell.alignment = Alignment(horizontal="right", vertical="top")
        sub_cell.number_format = '#,##0.00 €'
        
        for c_idx in range(2, 8):
            ws1.cell(row=row_cur, column=c_idx).border = border_thin
            if row_cur % 2 == 0:
                ws1.cell(row=row_cur, column=c_idx).fill = fill_alt
        ws1.row_dimensions[row_cur].height = 42
        row_cur += 1

    # Totales
    ws1.cell(row=row_cur, column=6, value="BASE IMPONIBLE (60 ML):").font = font_bold
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_cur, column=7, value=f"=SUM(G13:G{row_cur-1})").font = font_tot
    ws1.cell(row=row_cur, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_cur, column=7).border = border_thin
    base_row = row_cur

    row_cur += 1
    ws1.cell(row=row_cur, column=6, value="I.V.A. APLICABLE (21%):").font = font_reg
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_cur, column=7, value=f"=G{base_row}*0.21").font = font_reg
    ws1.cell(row=row_cur, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_cur, column=7).border = border_thin

    row_cur += 1
    ws1.cell(row=row_cur, column=6, value="TOTAL PRESUPUESTO CON IVA:").font = font_tot_blue
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_cur, column=7, value=f"=G{base_row}*1.21").font = font_tot_blue
    ws1.cell(row=row_cur, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_cur, column=7).fill = fill_tot
    ws1.cell(row=row_cur, column=7).border = border_total

    ws1.column_dimensions["A"].width = 3
    ws1.column_dimensions["B"].width = 8
    ws1.column_dimensions["C"].width = 58
    ws1.column_dimensions["D"].width = 10
    ws1.column_dimensions["E"].width = 12
    ws1.column_dimensions["F"].width = 18
    ws1.column_dimensions["G"].width = 18

    # -------------------------------------------------------------------------
    # HOJA 2: ESTUDIO TÉCNICO INTERNO DIXIS (PROVEEDOR LUX-TOP + INSTALACIÓN)
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Estudio Técnico Interno")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. • USO INTERNO CONFIDENCIAL"
    ws2["B2"].font = font_sub
    ws2["B3"] = f"ESCANDALLO TÉCNICO PROVEEDOR LUX-TOP: {DATA['codigo']} • TARIFA 120,47 €/ML"
    ws2["B3"].font = font_title

    headers_tech = ["Elemento / Concepto de Coste", "Tipo de Recurso", "Medición / Horas", "Coste Unitario", "Coste Directo Total", "PVP Venta", "Margen Bruto"]
    for c_idx, h in enumerate(headers_tech, start=2):
        cell = ws2.cell(row=5, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws2.row_dimensions[5].height = 24

    escandallo = [
        ["Cable inox Ø8 mm AISI 316 (LUX-top 000011710)", "Material LUX-TOP (-18% dto)", 64.0, 5.658, "=D6*E6", 736.00],
        ["24 Soportes hormigón 90º ASP SOKO EV2s/40 + pernos A4", "Material LUX-TOP (-18% dto)", 24.0, 127.51, "=D7*E7", 4200.00],
        ["Kit cierre directo FSE 2003 (SKE II + Tensor PV + Horquilla)", "Material LUX-TOP (-18% dto)", 1.0, 400.00, "=D8*E8", 750.00],
        ["Instalación muro hormigón EDAR (2 oficiales x 12 h = 24 h)", "Mano de obra en altura (24,0 h)", 24.0, 22.00, "=D9*E9", 912.00],
        ["Medios auxiliares y seguridad perimetral piscina EDAR", "Maquinaria / protecciones", 1.0, 280.00, "=D10*E10", 450.00],
        ["Pruebas de tiro dinamómetro in situ, placa y visado oficial", "Ensayos y certificación", 1.0, 70.00, "=D11*E11", 180.00]
    ]

    for idx, row in enumerate(escandallo, start=6):
        ws2.cell(row=idx, column=2, value=row[0]).font = font_reg
        ws2.cell(row=idx, column=3, value=row[1]).font = font_reg
        ws2.cell(row=idx, column=4, value=row[2]).font = font_reg
        ws2.cell(row=idx, column=4).number_format = '#,##0.00'
        ws2.cell(row=idx, column=5, value=row[3]).font = font_reg
        ws2.cell(row=idx, column=5).number_format = '#,##0.00 €'
        ws2.cell(row=idx, column=6, value=row[4]).font = font_bold
        ws2.cell(row=idx, column=6).number_format = '#,##0.00 €'
        ws2.cell(row=idx, column=7, value=row[5]).font = font_bold
        ws2.cell(row=idx, column=7).number_format = '#,##0.00 €'
        ws2.cell(row=idx, column=8, value=f"=G{idx}-F{idx}").font = font_bold
        ws2.cell(row=idx, column=8).number_format = '#,##0.00 €'

        for c_idx in range(2, 9):
            ws2.cell(row=idx, column=c_idx).border = border_thin
            if idx % 2 == 0:
                ws2.cell(row=idx, column=c_idx).fill = fill_alt

    # Totales escandallo
    ws2.cell(row=12, column=5, value="TOTALES:").font = font_bold
    ws2.cell(row=12, column=5).alignment = Alignment(horizontal="right")
    ws2.cell(row=12, column=6, value="=SUM(F6:F11)").font = font_tot
    ws2.cell(row=12, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=12, column=6).border = border_total
    
    ws2.cell(row=12, column=7, value="=SUM(G6:G11)").font = font_tot
    ws2.cell(row=12, column=7).number_format = '#,##0.00 €'
    ws2.cell(row=12, column=7).border = border_total

    ws2.cell(row=12, column=8, value="=G12-F12").font = font_tot_blue
    ws2.cell(row=12, column=8).number_format = '#,##0.00 €'
    ws2.cell(row=12, column=8).border = border_total

    # Resumen rentabilidad
    ws2["B14"] = "INDICADORES CLAVE DE RENTABILIDAD (60 ML EDAR FERRERIES):"
    ws2["B14"].font = font_sec
    ws2["B15"] = "Coste Material LUX-TOP (Neto Dixis con 18% Dto):"
    ws2["C15"] = "=SUM(F6:F8)"
    ws2["C15"].number_format = '#,##0.00 €'
    ws2["B16"] = "Venta Total Materiales LUX-TOP:"
    ws2["C16"] = "=SUM(G6:G8)"
    ws2["C16"].number_format = '#,##0.00 €'
    ws2["B17"] = "Margen Bruto en Materiales (€):"
    ws2["C17"] = "=C16-C15"
    ws2["C17"].number_format = '#,##0.00 €'
    ws2["B18"] = "Coste Directo Total Dixis (Material + MO + Medios + Cert):"
    ws2["C18"] = "=F12"
    ws2["C18"].number_format = '#,##0.00 €'
    ws2["B19"] = "Precio de Venta Base Imponible Total (60 ml):"
    ws2["C19"] = "=G12"
    ws2["C19"].number_format = '#,##0.00 €'
    ws2["B20"] = "Margen Bruto Total Dixis:"
    ws2["C20"] = "=H12"
    ws2["C20"].number_format = '#,##0.00 €'
    ws2["B21"] = "Margen sobre Venta (%):"
    ws2["C21"] = "=H12/G12"
    ws2["C21"].number_format = '0.0%'
    ws2["B22"] = "Margen sobre Coste (%):"
    ws2["C22"] = "=H12/F12"
    ws2["C22"].number_format = '0.0%'

    for r in range(15, 23):
        ws2[f"B{r}"].font = font_bold
        ws2[f"C{r}"].font = font_bold

    ws2.column_dimensions["A"].width = 3
    ws2.column_dimensions["B"].width = 46
    ws2.column_dimensions["C"].width = 25
    ws2.column_dimensions["D"].width = 16
    ws2.column_dimensions["E"].width = 15
    ws2.column_dimensions["F"].width = 18
    ws2.column_dimensions["G"].width = 16
    ws2.column_dimensions["H"].width = 16

    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0056_Linea_de_Vida_EDAR_Ferreries_Acciona.xlsx")
    wb.save(excel_path)
    print(f"Excel generado en: {excel_path}")
    return excel_path

def create_html_client():
    tot = DATA["modalidad_1_paso_manual"]["totales"]
    partidas = DATA["modalidad_1_paso_manual"]["partidas"]
    
    rows_html = ""
    for p in partidas:
        precio_fmt = f"{p['precio_cliente']:.2f} €" if p['precio_cliente'] > 0 else "Incluido"
        subtotal_fmt = f"{p['subtotal']:.2f} €" if p['subtotal'] > 0 else "Incluido"
        rows_html += f"""
        <tr>
          <td class="c bold">{p['id']}</td>
          <td>
            <strong>{p['concepto']}</strong>
            <div class="desc-text">{p['descripcion']}</div>
          </td>
          <td class="c">{p['unidad']}</td>
          <td class="r">{p['cantidad']:.2f}</td>
          <td class="r">{precio_fmt}</td>
          <td class="r bold">{subtotal_fmt}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Presupuesto {DATA['codigo']} • {DATA['cliente']['nombre']}</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
    }}
    :root {{
      --brand: #0f172a;
      --accent: #1d4ed8;
      --accent-light: #eff6ff;
      --line: #cbd5e1;
      --soft: #f8fafc;
      --muted: #475569;
      --ink: #0f172a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 9.2px;
      line-height: 1.25;
    }}
    .sheet {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 7mm 11mm 6mm;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      page-break-inside: avoid;
      page-break-after: always;
    }}
    .sheet:last-child {{
      page-break-after: avoid;
    }}
    header {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      align-items: center;
      border-top: 4px solid var(--accent);
      padding-top: 5px;
      padding-bottom: 5px;
      border-bottom: 1px solid var(--line);
    }}
    .company {{
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .logo {{
      width: 95px;
      flex: 0 0 95px;
    }}
    .logo img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .company-info h1 {{
      margin: 0;
      color: var(--brand);
      font-size: 13px;
      font-weight: 800;
      letter-spacing: -0.2px;
    }}
    .company-info p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 8.5px;
    }}
    .meta {{
      text-align: right;
    }}
    .meta h2 {{
      margin: 0;
      color: var(--accent);
      font-size: 13.5px;
      font-weight: 800;
    }}
    .meta .ref-badge {{
      display: inline-block;
      background: var(--brand);
      color: #fff;
      font-size: 8px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      margin: 2px 0;
    }}
    .meta p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 8px;
    }}
    .hero {{
      margin-top: 4px;
      background: var(--soft);
      border-left: 3px solid var(--accent);
      padding: 4px 8px;
      border-radius: 0 4px 4px 0;
    }}
    .hero h3 {{
      margin: 0 0 1px;
      color: var(--brand);
      font-size: 10.5px;
      font-weight: 700;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 8.5px;
    }}
    .client-block {{
      margin-top: 4px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      background: var(--accent-light);
      border: 1px solid #bfdbfe;
      border-radius: 4px;
      padding: 4px 8px;
    }}
    .client-block div strong {{
      color: var(--brand);
      display: block;
      font-size: 8px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      margin-bottom: 1px;
    }}
    .client-block div p {{
      margin: 0;
      font-size: 8.5px;
      color: var(--ink);
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 5px;
      font-size: 8.5px;
    }}
    table.data-table th {{
      background: var(--brand);
      color: #fff;
      padding: 4px 6px;
      font-size: 8px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      border: 1px solid var(--brand);
    }}
    table.data-table td {{
      padding: 3.5px 5px;
      border: 1px solid var(--line);
      vertical-align: top;
    }}
    table.data-table tbody tr:nth-child(even) {{
      background: var(--soft);
    }}
    .desc-text {{
      color: var(--muted);
      font-size: 7.8px;
      line-height: 1.2;
      margin-top: 1px;
    }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .totals-box {{
      margin-top: 5px;
      display: flex;
      justify-content: flex-end;
    }}
    .totals-table {{
      width: 320px;
      border-collapse: collapse;
      font-size: 8.5px;
    }}
    .totals-table td {{
      padding: 3px 6px;
      border: 1px solid var(--line);
    }}
    .totals-table tr.total-row {{
      background: var(--accent-light);
      font-weight: 800;
      color: var(--accent);
      font-size: 10px;
    }}
    .totals-table tr.total-row td {{
      border: 1px solid var(--accent);
    }}
    .ratio-pill {{
      display: inline-block;
      background: #dbeafe;
      color: #1e40af;
      padding: 1px 6px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 8px;
      margin-left: 4px;
    }}
    .grid-photos {{
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 8px;
      margin-top: 5px;
    }}
    .photo-card {{
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 4px;
      background: #fff;
      text-align: center;
    }}
    .photo-card img {{
      max-width: 100%;
      height: 125px;
      object-fit: contain;
      border-radius: 2px;
    }}
    .photo-card span {{
      display: block;
      font-size: 7.5px;
      color: var(--muted);
      margin-top: 2px;
      font-weight: 600;
    }}
    .specs-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 5px;
    }}
    .spec-card {{
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 5px 7px;
    }}
    .spec-card h4 {{
      margin: 0 0 3px;
      color: var(--brand);
      font-size: 8.5px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    .spec-card ul {{
      margin: 0;
      padding-left: 12px;
      font-size: 8px;
      color: var(--muted);
    }}
    .spec-card li {{
      margin-bottom: 1.5px;
    }}
    footer {{
      margin-top: 5px;
      padding-top: 4px;
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      font-size: 7.5px;
    }}
    .firmas {{
      margin-top: 6px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
    }}
    .firma-box {{
      border: 1px dashed var(--line);
      border-radius: 4px;
      padding: 5px;
      height: 48px;
      background: var(--soft);
    }}
    .firma-box strong {{
      display: block;
      color: var(--brand);
      font-size: 7.5px;
      margin-bottom: 2px;
    }}
  </style>
</head>
<body>

  <!-- PÁGINA 1: OFERTA ECONÓMICA Y DESGLOSE -->
  <div class="sheet">
    <div>
      <header>
        <div class="company">
          <div class="logo">
            <img src="logo-ham.svg" alt="HAM Menorca / Dixis">
          </div>
          <div class="company-info">
            <h1>{DATA['emisor']['razon_social']}</h1>
            <p><strong>{DATA['emisor']['nombre_comercial']}</strong> • CIF: {DATA['emisor']['cif']}</p>
            <p>{DATA['emisor']['domicilio']} • Tel: {DATA['emisor']['telefono']} • {DATA['emisor']['email']}</p>
          </div>
        </div>
        <div class="meta">
          <h2>PRESUPUESTO TÉCNICO</h2>
          <div class="ref-badge">{DATA['codigo']} • {DATA['referencia']}</div>
          <p>Fecha: {DATA['fecha']} • Validez: {DATA['validez_dias']} días</p>
          <p>Instalador Homologado Oficial: <strong>LUX-TOP® SISTEMAS ANTICAÍDAS</strong></p>
        </div>
      </header>

      <div class="hero">
        <h3>{DATA['proyecto']['titulo']}</h3>
        <p>{DATA['proyecto']['geometria']}</p>
      </div>

      <div class="client-block">
        <div>
          <strong>Cliente / Razón Social:</strong>
          <p><strong>{DATA['cliente']['nombre']}</strong></p>
          <p>Atención: {DATA['cliente']['contacto_tecnico']}</p>
        </div>
        <div>
          <strong>Emplazamiento de Obra:</strong>
          <p>{DATA['cliente']['ubicacion']}</p>
          <p>Proyecto: {DATA['cliente']['obra']}</p>
        </div>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 32px;">Nº</th>
            <th>Concepto y Especificación Técnica Oficial LUX-TOP®</th>
            <th style="width: 32px;">Ud.</th>
            <th style="width: 45px;">Cant.</th>
            <th style="width: 65px;">Precio Ud.</th>
            <th style="width: 75px;">Subtotal</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>

      <div class="totals-box">
        <table class="totals-table">
          <tr>
            <td class="r bold">BASE IMPONIBLE (60,00 ML LLAVE EN MANO):</td>
            <td class="r bold" style="width: 85px;">{tot['base_imponible']:.2f} € <span class="ratio-pill">{tot['precio_unitario_ml']:.2f} €/ml</span></td>
          </tr>
          <tr>
            <td class="r">I.V.A. APLICABLE (21%):</td>
            <td class="r">{tot['iva_21']:.2f} €</td>
          </tr>
          <tr class="total-row">
            <td class="r">TOTAL PRESUPUESTO (CON IVA):</td>
            <td class="r">{tot['total_con_iva']:.2f} €</td>
          </tr>
        </table>
      </div>
    </div>

    <div>
      <div class="firmas">
        <div class="firma-box">
          <strong>Por DIXIS RECURSOS Y SOLUCIONES S.L. (Instalador Oficial LUX-TOP):</strong>
          <span style="font-size:7px; color:var(--muted);">Fdo: Pablo Sebastián Sánchez • Dpto. Técnico HAM Menorca</span>
        </div>
        <div class="firma-box">
          <strong>Aceptación Conforme por ACCIONA AGUA S.A. / Cliente:</strong>
          <span style="font-size:7px; color:var(--muted);">Firma, Sello de la Empresa y Fecha de Aceptación:</span>
        </div>
      </div>

      <footer>
        <div>DIXIS RECURSOS Y SOLUCIONES S.L. • www.hamenorca.com • Instalador Autorizado LUX-TOP® Sistemas Anticaídas</div>
        <div>{DATA['codigo']} • Hoja 1 de 2</div>
      </footer>
    </div>
  </div>

  <!-- PÁGINA 2: MEMORIA TÉCNICA, PLANO DE REPLANTEO Y CONDICIONES -->
  <div class="sheet">
    <div>
      <header>
        <div class="company">
          <div class="logo">
            <img src="logo-ham.svg" alt="HAM Menorca / Dixis">
          </div>
          <div class="company-info">
            <h1>{DATA['emisor']['razon_social']}</h1>
            <p><strong>{DATA['emisor']['nombre_comercial']}</strong> • CIF: {DATA['emisor']['cif']}</p>
          </div>
        </div>
        <div class="meta">
          <h2>MEMORIA TÉCNICA Y REPLANTEO</h2>
          <div class="ref-badge">{DATA['codigo']} • EDAR FERRERIES</div>
          <p>Sistema: <strong>LUX-top® FSE 2003 (Muro de Hormigón Armado)</strong></p>
        </div>
      </header>

      <div class="grid-photos">
        <div class="photo-card">
          <img src="img/pagina_3.png" alt="Plano de Replanteo Oficial LUX-TOP">
          <span>Replanteo perimetral circular oficial LUX-top® FSE 2003 (Vanos de ~2,50 m entre soportes)</span>
        </div>
        <div class="photo-card">
          <img src="img/ortofoto-edar-ferreries.jpg" alt="Ortofoto Decantador EDAR Ferreries">
          <span>Ortofoto satelital EDAR Ferreries: D exterior = 18,08 m (Perímetro ~60 ml)</span>
        </div>
      </div>

      <div class="specs-grid">
        <div class="spec-card">
          <h4>1. Memoria Descriptiva del Sistema</h4>
          <ul>
            <li><strong>Línea de Vida Flexible Tipo C:</strong> Homologada según <strong>UNE-EN 795:2012 Tipo C</strong> y <strong>UNE-CEN/TS 16415:2013</strong> para hasta 3 usuarios simultáneos (Certificado DEKRA).</li>
            <li><strong>Cable de Calidad Marina:</strong> Acero inoxidable <strong>AISI 316 Ø8 mm</strong> con carga de rotura superior a 42 kN, resistente a la salinidad y al ambiente clorado de la EDAR.</li>
            <li><strong>Absorbedor e Indicador de Tensión SKE II:</strong> En acero inoxidable AISI 304/316, disipa el impacto dinámico limitando las cargas en extremos a valores seguros (&lt; 10 kN) y visualiza la tensión correcta.</li>
            <li><strong>Tensor y Terminales Autoprensados:</strong> Tensado micrométrico mediante tensor prensado en fábrica y horquilla autoprensada SV sin soldadura.</li>
          </ul>
        </div>
        <div class="spec-card">
          <h4>2. Soportes Especiales SOKO y Fijaciones</h4>
          <ul>
            <li><strong>Soportes a Medida 90º:</strong> 24 unidades `LUX-top® ASP - SOKO EV2s/40` diseñados en taller para librar la coronación del muro de hormigón (20+20 cm, placa 80x150x6 mm).</li>
            <li><strong>Anclajes de Seguridad MKT A4:</strong> 48 pernos de acero inoxidable calidad A4 (`M-12x115/20`) con Evaluación Técnica Europea (ETA Opción 1 para hormigón fisurado).</li>
            <li><strong>Apretado Dinamométrico:</strong> Control estricto de par de apriete mediante llave dinamométrica calibrada para garantizar adherencia mecánica y durabilidad.</li>
            <li><strong>Plazo de Fabricación SOKO:</strong> Mínimo 20-25 días al tratarse de piezas de forja y mecanizado a medida.</li>
          </ul>
        </div>
        <div class="spec-card">
          <h4>3. Protocolo de Ensayos y Certificación</h4>
          <ul>
            <li><strong>Prueba de Tiro Estático in situ:</strong> Ensayo con dinamómetro tarado sobre los anclajes estructurales de hormigón según normativa europea.</li>
            <li><strong>Placa Indeleble CE:</strong> Placa de señalización reglamentaria SB grabada con fecha, número de usuarios, instalador y próxima inspección periódica.</li>
            <li><strong>Dossier Técnico Completo:</strong> Emisión de Certificado Oficial de Instalación emitido por Dixis en la plataforma oficial de LUX-TOP con manual de uso y libro de mantenimiento anual.</li>
          </ul>
        </div>
        <div class="spec-card">
          <h4>4. Condiciones Comerciales y Ejecución</h4>
          <ul>
            <li><strong>Forma de Pago Estándar:</strong> 100% a la aceptación del presupuesto (directiva estándar HAM Menorca).</li>
            <li><strong>Plazo de Montaje:</strong> 2 jornadas laborables tras recepción de los soportes especiales SOKO.</li>
            <li><strong>Garantía:</strong> Cobertura oficial de fabricante LUX-TOP y garantía de montaje Dixis según legislación vigente. Revisiones obligatorias anuales.</li>
            <li><strong>Medios de Acceso:</strong> Incluye medios auxiliares específicos de montaje y línea provisional para trabajos en corona.</li>
          </ul>
        </div>
      </div>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • www.hamenorca.com • Instalador Autorizado LUX-TOP® Sistemas Anticaídas</div>
      <div>{DATA['codigo']} • Hoja 2 de 2</div>
    </footer>
  </div>

</body>
</html>"""

    html_path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Cliente generado en: {html_path}")
    return html_path

def create_html_technical():
    tot = DATA["modalidad_1_paso_manual"]["totales"]

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Estudio Técnico Interno • {DATA['codigo']} • Dixis</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
    }}
    :root {{
      --brand: #0f172a;
      --accent: #1d4ed8;
      --tech-green: #047857;
      --line: #cbd5e1;
      --soft: #f8fafc;
      --muted: #475569;
      --ink: #0f172a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 9px;
      line-height: 1.25;
    }}
    .sheet {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 7mm 11mm 6mm;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      page-break-inside: avoid;
    }}
    header {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      align-items: center;
      border-top: 4px solid var(--brand);
      padding-top: 5px;
      padding-bottom: 5px;
      border-bottom: 1px solid var(--line);
    }}
    .title h1 {{
      margin: 0;
      color: var(--brand);
      font-size: 13px;
      font-weight: 800;
    }}
    .title p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 8.5px;
    }}
    .badge {{
      background: #dc2626;
      color: #fff;
      font-size: 8px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-top: 6px;
    }}
    .kpi-card {{
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 6px 8px;
      text-align: center;
    }}
    .kpi-card strong {{
      display: block;
      color: var(--muted);
      font-size: 7.5px;
      text-transform: uppercase;
      margin-bottom: 2px;
    }}
    .kpi-card .val {{
      font-size: 13px;
      font-weight: 800;
      color: var(--brand);
    }}
    .kpi-card .val.green {{ color: var(--tech-green); }}
    .kpi-card .val.blue {{ color: var(--accent); }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 6px;
      font-size: 8.5px;
    }}
    table.data-table th {{
      background: var(--brand);
      color: #fff;
      padding: 4px 6px;
      font-size: 8px;
      text-transform: uppercase;
      border: 1px solid var(--brand);
    }}
    table.data-table td {{
      padding: 4px 6px;
      border: 1px solid var(--line);
    }}
    table.data-table tbody tr:nth-child(even) {{
      background: var(--soft);
    }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .two-col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 6px;
    }}
    .box {{
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 6px 8px;
    }}
    .box h4 {{
      margin: 0 0 4px;
      color: var(--brand);
      font-size: 9px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    .box ul {{
      margin: 0;
      padding-left: 14px;
      font-size: 8px;
      color: var(--muted);
    }}
    .box li {{
      margin-bottom: 2px;
    }}
    footer {{
      margin-top: 5px;
      padding-top: 4px;
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      font-size: 7.5px;
    }}
  </style>
</head>
<body>

  <div class="sheet">
    <div>
      <header>
        <div class="title">
          <h1>DIXIS RECURSOS Y SOLUCIONES S.L. • ESTUDIO TÉCNICO INTERNO</h1>
          <p>Proyecto {DATA['codigo']} • {DATA['proyecto']['titulo']} (60 ml)</p>
        </div>
        <div>
          <span class="badge">ESTRICTAMENTE CONFIDENCIAL • USO INTERNO</span>
        </div>
      </header>

      <div class="kpi-grid">
        <div class="kpi-card">
          <strong>Coste Directo Total</strong>
          <div class="val">{tot['coste_directo_total']:.2f} €</div>
          <span style="font-size:7px; color:var(--muted);">{tot['coste_directo_total']/60:.2f} €/ml</span>
        </div>
        <div class="kpi-card">
          <strong>Venta Neta Cliente</strong>
          <div class="val blue">{tot['base_imponible']:.2f} €</div>
          <span style="font-size:7px; color:var(--muted);">{tot['precio_unitario_ml']:.2f} €/ml</span>
        </div>
        <div class="kpi-card">
          <strong>Margen Bruto (€)</strong>
          <div class="val green">{tot['margen_euros']:.2f} €</div>
          <span style="font-size:7px; color:var(--muted);">Beneficio neto de proyecto</span>
        </div>
        <div class="kpi-card">
          <strong>Rentabilidad Margen</strong>
          <div class="val green">{tot['margen_porcentaje_venta']:.1f}%</div>
          <span style="font-size:7px; color:var(--muted);">{tot['margen_porcentaje_coste']:.1f}% s/coste</span>
        </div>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>Concepto de Coste / Elemento</th>
            <th>Tipo de Recurso</th>
            <th class="c">Medición</th>
            <th class="r">Coste Unit.</th>
            <th class="r">Coste Directo</th>
            <th class="r">PVP Venta</th>
            <th class="r">Margen (€)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Cable inox AISI 316 Ø8 mm (000011710)</strong></td>
            <td>Material LUX-TOP (-18% dto)</td>
            <td class="c">64,00 m</td>
            <td class="r">5,658 €</td>
            <td class="r bold">{64.0 * 5.658:.2f} €</td>
            <td class="r bold">736,00 €</td>
            <td class="r bold" style="color:var(--tech-green);">{736.00 - (64.0 * 5.658):.2f} €</td>
          </tr>
          <tr>
            <td><strong>24 Soportes muro 90º ASP SOKO + pernos A4</strong></td>
            <td>Material LUX-TOP (-18% dto)</td>
            <td class="c">24,00 ud</td>
            <td class="r">127,51 €</td>
            <td class="r bold">{24.0 * 127.51:.2f} €</td>
            <td class="r bold">4.200,00 €</td>
            <td class="r bold" style="color:var(--tech-green);">{4200.00 - (24.0 * 127.51):.2f} €</td>
          </tr>
          <tr>
            <td><strong>Kit cierre directo FSE 2003 (SKE II + Horquilla)</strong></td>
            <td>Material LUX-TOP (-18% dto)</td>
            <td class="c">1,00 kit</td>
            <td class="r">400,00 €</td>
            <td class="r bold">400,00 €</td>
            <td class="r bold">750,00 €</td>
            <td class="r bold" style="color:var(--tech-green);">{750.00 - 400.00:.2f} €</td>
          </tr>
          <tr>
            <td><strong>Mano de obra especializada (2 operarios x 12 h)</strong></td>
            <td>Mano de obra propia (24 h)</td>
            <td class="c">24,00 h</td>
            <td class="r">22,00 €</td>
            <td class="r bold">{24.0 * 22.0:.2f} €</td>
            <td class="r bold">912,00 €</td>
            <td class="r bold" style="color:var(--tech-green);">{912.00 - (24.0 * 22.0):.2f} €</td>
          </tr>
          <tr>
            <td><strong>Medios auxiliares y seguridad perimetral EDAR</strong></td>
            <td>Medios auxiliares</td>
            <td class="c">1,00 paq.</td>
            <td class="r">280,00 €</td>
            <td class="r bold">280,00 €</td>
            <td class="r bold">450,00 €</td>
            <td class="r bold" style="color:var(--tech-green);">{450.00 - 280.00:.2f} €</td>
          </tr>
          <tr>
            <td><strong>Pruebas estáticas dinamómetro y Certificado LUX-TOP</strong></td>
            <td>Ensayos / certificación</td>
            <td class="c">1,00 ud</td>
            <td class="r">70,00 €</td>
            <td class="r bold">70,00 €</td>
            <td class="r bold">180,00 €</td>
            <td class="r bold" style="color:var(--tech-green);">{180.00 - 70.00:.2f} €</td>
          </tr>
          <tr style="background:var(--accent-light); font-weight:800;">
            <td colspan="4" class="r">TOTALES DE PROYECTO (60,00 ML):</td>
            <td class="r" style="color:var(--brand);">{tot['coste_directo_total']:.2f} €</td>
            <td class="r" style="color:var(--accent);">{tot['base_imponible']:.2f} €</td>
            <td class="r" style="color:var(--tech-green);">{tot['margen_euros']:.2f} €</td>
          </tr>
        </tbody>
      </table>

      <div class="two-col">
        <div class="box">
          <h4>Estructura de Costes y Rentabilidad de Material</h4>
          <ul>
            <li><strong>Coste compra LUX-TOP (Neto):</strong> 3.822,35 € (Tarifa oficial: 4.661,40 € menos 18% descuento directo Dixis).</li>
            <li><strong>Venta cliente materiales:</strong> 5.686,00 € (Recargo comercial: 1.863,65 €).</li>
            <li><strong>Margen en material:</strong> <strong>32,77% sobre venta de producto</strong> (48,76% sobre coste de compra).</li>
            <li><strong>Servicios e instalación:</strong> Facturación MO + Medios + Cert: 1.542,00 € (Coste: 878,00 € -> Margen: 664,00 €).</li>
          </ul>
        </div>
        <div class="box">
          <h4>Condiciones Operativas y Tesorería</h4>
          <ul>
            <li><strong>Ratio de Venta:</strong> <strong>120,47 €/ml llave en mano</strong> (muy competitivo frente al estándar de 145,60 €/ml en cubierta gracias al volumen de 60 ml).</li>
            <li><strong>Tesorería Dixis:</strong> Cobro 100% aceptación cliente vs Pago LUX-TOP mediante <strong>Giro comercial a 60 días</strong> (Asegurado por CESCE).</li>
            <li><strong>Plazo Crítico:</strong> 20 a 25 días para la forja de los 24 soportes especiales SOKO. Coordinar pedido inmediatamente tras aprobación de Acciona.</li>
            <li><strong>Logística Menorca:</strong> Desplazamiento desde taller en Sant Lluís a Ferreries (aprox. 30 minutos).</li>
          </ul>
        </div>
      </div>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • HAM Menorca • Oficina Técnica</div>
      <div>{DATA['codigo']} • Escandallo 120,47 €/ml LUX-TOP • Hoja 1 de 1</div>
    </footer>
  </div>

</body>
</html>"""

    html_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Técnico generado en: {html_path}")
    return html_path

def convert_to_pdf(html_file, pdf_file):
    if not os.path.exists(CHROME_PATH):
        raise FileNotFoundError(f"Chrome no encontrado en: {CHROME_PATH}")
    uri = 'file:///' + html_file.replace('\\', '/')
    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_file}',
        uri
    ]
    subprocess.run(cmd, check=True)
    print(f"PDF generado con éxito en: {pdf_file}")

if __name__ == "__main__":
    excel_path = create_excel()
    client_html = create_html_client()
    client_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    convert_to_pdf(client_html, client_pdf)
    
    tech_html = create_html_technical()
    tech_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")
    convert_to_pdf(tech_html, tech_pdf)
    
    print(f"\nTodos los documentos de {DATA['codigo']} generados con éxito a {DATA['tarifa_objetivo_ml']} €/ml.")
