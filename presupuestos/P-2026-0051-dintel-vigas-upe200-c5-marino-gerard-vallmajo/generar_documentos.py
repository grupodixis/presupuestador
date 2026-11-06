import os
import sys
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

def create_excel():
    wb = Workbook()
    
    # Colores corporativos Dixis / HAM
    NAVY = "0F172A"        # Fondo cabecera principal
    GOLD = "B45309"        # Acento dorado / óxido
    SLATE_LIGHT = "F8FAFC" # Fila alterna
    SLATE_HEADER = "1E293B"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"   # Amarillo cálido
    SECTION_FILL = "F1F5F9"
    
    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_sec = PatternFill(start_color=SECTION_FILL, end_color=SECTION_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    
    font_title = Font(name="Segoe UI", size=15, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=10, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=9, color="1E293B")
    font_italic = Font(name="Segoe UI", size=8.5, italic=True, color="64748B")
    font_tot = Font(name="Segoe UI", size=11, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=11, bold=True, color=GOLD)

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
    # HOJA 1: PRESUPUESTO CLIENTE
    # -------------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Comercial"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO: {DATA['codigo']} • {DATA['proyecto']['titulo']}"
    ws1["B3"].font = font_title
    
    # Metadatos del proyecto
    ws1["B5"] = "REFERENCIA:"
    ws1["C5"] = DATA["referencia"]
    ws1["B6"] = "CLIENTE:"
    ws1["C6"] = f"{DATA['cliente']['nombre']} (Contacto técnico: {DATA['cliente']['contacto_tecnico']})"
    ws1["B7"] = "UBICACIÓN:"
    ws1["C7"] = DATA["cliente"]["ubicacion"]
    ws1["B8"] = "FECHA / VALIDEZ:"
    ws1["C8"] = f"{DATA['fecha']} · {DATA['validez_dias']} días de validez"

    for r in range(5, 9):
        ws1[f"B{r}"].font = font_bold
        ws1[f"C{r}"].font = font_reg

    # Resumen técnico
    ws1["B10"] = "CARACTERÍSTICAS TÉCNICAS Y CONDICIONES (REVISIÓN 1)"
    ws1["B10"].font = font_sec
    ws1["B10"].fill = fill_sub
    ws1.merge_cells("B10:G10")

    ws1["B11"] = (
        "• Dintel compuesto por 2 UPE 200 (S275JR) de 3,20 m cada uno (Total: 6,40 ML / 145,92 kg de acero).\n"
        "• Geometría: Sección doble en I unida espalda con espalda según cálculo de Joan (Luz entre apoyos 2,66 m, entrega ~27 cm por apoyo).\n"
        "• Mecanizado de perforaciones pasantes Ø22 mm en alma de uno de los perfiles para botones de soldadura (plug welds) in situ y biselado inferior.\n"
        "• Tratamiento anticorrosivo C5 Marino acabado Blanco (sin horno): Imprimación epoxi + intermedia + esmalte poliuretano alifático 2C (DFT ≥ 240 µm).\n"
        "• Sin logística: Porte a obra y acarreo interior no incluidos en el alcance (a cargo del cliente / retirada en taller).\n"
        "• Montaje in situ en apartamento: protección ignífuga, soldadura de botones y cordón discontinuo, y sellado C5 Marino en obra."
    )
    ws1["B11"].font = font_reg
    ws1["B11"].alignment = Alignment(wrap_text=True, vertical="top")
    ws1.merge_cells("B11:G11")
    ws1.row_dimensions[11].height = 78

    # Tabla de Partidas
    headers = ["Nº", "Concepto y Descripción de la Partida", "Ud", "Cantidad", "Precio Unitario", "Importe"]
    for col_idx, h in enumerate(headers, start=2):
        cell = ws1.cell(row=13, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if col_idx not in [3] else "left", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[13].height = 25

    row_curr = 14
    for idx, p in enumerate(DATA["partidas"], 1):
        ws1.cell(row=row_curr, column=2, value=p["id"]).alignment = Alignment(horizontal="center", vertical="top")
        
        # Descripción compuesta
        desc_text = f"{p['concepto']}\n{p['descripcion']}"
        cell_desc = ws1.cell(row=row_curr, column=3, value=desc_text)
        cell_desc.alignment = Alignment(wrap_text=True, vertical="top")
        
        ws1.cell(row=row_curr, column=4, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        ws1.cell(row=row_curr, column=5, value=p["cantidad"]).alignment = Alignment(horizontal="right", vertical="top")
        ws1.cell(row=row_curr, column=6, value=p["precio_unitario"]).alignment = Alignment(horizontal="right", vertical="top")
        
        # Fórmula importe
        cell_imp = ws1.cell(row=row_curr, column=7, value=f"=E{row_curr}*F{row_curr}")
        cell_imp.alignment = Alignment(horizontal="right", vertical="top")

        for c_idx in range(2, 8):
            c = ws1.cell(row=row_curr, column=c_idx)
            c.font = font_reg
            c.border = border_thin
            if idx % 2 == 0:
                c.fill = fill_alt
            if c_idx in [5]:
                c.number_format = '#,##0.00'
            elif c_idx in [6, 7]:
                c.number_format = '#,##0.00 €'
        
        ws1.row_dimensions[row_curr].height = 42
        row_curr += 1

    # Totales
    row_curr += 1
    ws1.cell(row=row_curr, column=6, value="Base Imponible:").font = font_bold
    ws1.cell(row=row_curr, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_curr, column=7, value=f"=SUM(G14:G{row_curr-2})").font = font_bold
    ws1.cell(row=row_curr, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_curr, column=7).border = border_thin

    row_curr += 1
    ws1.cell(row=row_curr, column=6, value="I.V.A. (21%):").font = font_bold
    ws1.cell(row=row_curr, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_curr, column=7, value=f"=G{row_curr-1}*0.21").font = font_bold
    ws1.cell(row=row_curr, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_curr, column=7).border = border_thin

    row_curr += 1
    ws1.cell(row=row_curr, column=6, value="TOTAL PRESUPUESTO:").font = font_tot
    ws1.cell(row=row_curr, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_curr, column=6).fill = fill_tot
    ws1.cell(row=row_curr, column=7, value=f"=G{row_curr-2}+G{row_curr-1}").font = font_tot
    ws1.cell(row=row_curr, column=7).fill = fill_tot
    ws1.cell(row=row_curr, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_curr, column=7).border = border_total
    ws1.row_dimensions[row_curr].height = 24

    # Condiciones
    row_curr += 2
    ws1.cell(row=row_curr, column=2, value="CONDICIONES Y OBSERVACIONES GENERALES").font = font_sec
    ws1.cell(row=row_curr, column=2).fill = fill_sub
    ws1.merge_cells(f"B{row_curr}:G{row_curr}")
    
    cond_text = (
        f"• Plazo de ejecución: {DATA['condiciones']['plazo_entrega']}\n"
        f"• Forma de pago: {DATA['condiciones']['forma_pago']}\n"
        f"• Garantía: {DATA['condiciones']['garantia']}\n"
        f"• Logística y Transporte: Sin logística incluida (transporte a obra y acarreo interior a cargo del cliente / retirada en taller).\n"
        f"• Exclusiones: {DATA['condiciones']['exclusiones']}"
    )
    row_curr += 1
    ws1.cell(row=row_curr, column=2, value=cond_text).font = font_italic
    ws1.cell(row=row_curr, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws1.merge_cells(f"B{row_curr}:G{row_curr}")
    ws1.row_dimensions[row_curr].height = 55

    ws1.column_dimensions["A"].width = 3
    ws1.column_dimensions["B"].width = 6
    ws1.column_dimensions["C"].width = 58
    ws1.column_dimensions["D"].width = 8
    ws1.column_dimensions["E"].width = 12
    ws1.column_dimensions["F"].width = 18
    ws1.column_dimensions["G"].width = 16

    # -------------------------------------------------------------------------
    # HOJA 2: DESGLOSE TÉCNICO INTERNO Y ESCANDALLO
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Desglose Técnico Interno")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | OFICINA TÉCNICA HAM"
    ws2["B2"].font = font_sub
    ws2["B3"] = f"ESCANDALLO Y CONTROL DE COSTES DIRECTOS • {DATA['codigo']} (REV. 1)"
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
        ["Perfiles UPE 200 (6,40 m / 146 kg)", "Material Acero S275", 146.00, 1.45, "=D6*E6", 320.00],
        ["Mecanizado almas y biselado (35 €/h)", "Mano de obra taller (2,5 h)", 2.50, 28.00, "=D7*E7", 87.50],
        ["Sistema C5 Marino Blanco (a 50 €/m²)", "Tratamiento epoxi + PU 2C", 5.00, 25.00, "=D8*E8", 250.00],
        ["Montaje y soldadura in situ apartamento", "Mano de obra obra (8,0 h)", 8.00, 28.00, "=D9*E9", 320.00],
        ["Retoque in situ y sellado C5 Marino", "Mano de obra y pintura", 2.00, 28.00, "=D10*E10", 100.00]
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
    ws2.cell(row=11, column=5, value="TOTALES:").font = font_bold
    ws2.cell(row=11, column=5).alignment = Alignment(horizontal="right")
    ws2.cell(row=11, column=6, value="=SUM(F6:F10)").font = font_tot
    ws2.cell(row=11, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=11, column=6).border = border_total
    
    ws2.cell(row=11, column=7, value="=SUM(G6:G10)").font = font_tot
    ws2.cell(row=11, column=7).number_format = '#,##0.00 €'
    ws2.cell(row=11, column=7).border = border_total

    ws2.cell(row=11, column=8, value="=G11-F11").font = font_tot_gold
    ws2.cell(row=11, column=8).number_format = '#,##0.00 €'
    ws2.cell(row=11, column=8).border = border_total

    # Resumen margen
    ws2["B13"] = "RESUMEN DE RENTABILIDAD:"
    ws2["B13"].font = font_sec
    ws2["B14"] = "Coste Directo Total:"
    ws2["C14"] = "=F11"
    ws2["C14"].number_format = '#,##0.00 €'
    ws2["B15"] = "Precio de Venta Neto:"
    ws2["C15"] = "=G11"
    ws2["C15"].number_format = '#,##0.00 €'
    ws2["B16"] = "Margen de Contribución Bruto:"
    ws2["C16"] = "=H11"
    ws2["C16"].number_format = '#,##0.00 €'
    ws2["B17"] = "Margen sobre Venta (%):"
    ws2["C17"] = "=H11/G11"
    ws2["C17"].number_format = '0.0%'

    for r in range(14, 18):
        ws2[f"B{r}"].font = font_bold
        ws2[f"C{r}"].font = font_bold

    ws2.column_dimensions["A"].width = 3
    ws2.column_dimensions["B"].width = 38
    ws2.column_dimensions["C"].width = 25
    ws2.column_dimensions["D"].width = 16
    ws2.column_dimensions["E"].width = 15
    ws2.column_dimensions["F"].width = 18
    ws2.column_dimensions["G"].width = 16
    ws2.column_dimensions["H"].width = 16

    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0051_Dintel_UPE200_Vallmajo.xlsx")
    wb.save(excel_path)
    print(f"Excel generado con éxito en: {excel_path}")
    return excel_path

def create_html_client():
    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presupuesto {DATA['codigo']} • {DATA['proyecto']['titulo']}</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 0;
    }}
    :root {{
      --ink: #0f172a;
      --muted: #475569;
      --line: #cbd5e1;
      --soft: #f8fafc;
      --brand: #0f172a;
      --accent: #b45309;
      --accent-light: #fef3c7;
      --card-bg: #f1f5f9;
      --highlight: #0284c7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 11px;
      line-height: 1.32;
    }}
    .page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 8mm 13mm 6mm;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      page-break-inside: avoid;
      page-break-after: avoid;
    }}
    header {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 14px;
      align-items: center;
      border-top: 5px solid var(--brand);
      padding-top: 8px;
      padding-bottom: 7px;
      border-bottom: 1px solid var(--line);
    }}
    .company {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .logo {{
      width: 115px;
      flex: 0 0 115px;
    }}
    .logo img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .company-info h1 {{
      margin: 0;
      color: var(--brand);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: -0.2px;
    }}
    .company-info p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 10px;
    }}
    .meta {{
      text-align: right;
    }}
    .meta h2 {{
      margin: 0 0 2px;
      color: var(--brand);
      font-size: 19px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .ref-badge {{
      display: inline-block;
      padding: 2px 6px;
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 3px;
      font-family: ui-monospace, SFMono-Regular, monospace;
      font-weight: 700;
      font-size: 10.5px;
      color: var(--brand);
      margin-bottom: 2px;
    }}
    .meta p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 10px;
    }}
    .hero {{
      margin: 6px 0 5px;
      padding: 6px 10px;
      border-left: 4px solid var(--accent);
      background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
      border-radius: 0 4px 4px 0;
      border-top: 1px solid #edf2f7;
      border-right: 1px solid #edf2f7;
      border-bottom: 1px solid #edf2f7;
    }}
    .hero h3 {{
      margin: 0 0 2px;
      color: var(--brand);
      font-size: 12.5px;
      font-weight: 700;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 10px;
      line-height: 1.25;
    }}
    .grid-meta {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin: 5px 0 6px;
    }}
    .card {{
      border: 1px solid var(--line);
      background: var(--soft);
      border-radius: 3px;
      padding: 4px 7px;
    }}
    .label {{
      display: block;
      color: var(--muted);
      font-size: 8.5px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      margin-bottom: 1px;
      font-weight: 600;
    }}
    .value {{
      font-weight: 700;
      font-size: 11px;
      color: var(--brand);
    }}
    h4 {{
      margin: 6px 0 3px;
      padding-bottom: 2px;
      border-bottom: 1.5px solid var(--brand);
      color: var(--brand);
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 3px 0 5px;
      page-break-inside: avoid;
    }}
    tr {{
      page-break-inside: avoid;
    }}
    th {{
      background: var(--brand);
      color: #fff;
      text-align: left;
      padding: 4px 6px;
      font-size: 9.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.2px;
    }}
    td {{
      padding: 4px 6px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
      font-size: 10.5px;
    }}
    tr:nth-child(even) td {{
      background: #fafbfc;
    }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .partida-title {{
      font-weight: 700;
      color: var(--brand);
      font-size: 10.5px;
      margin-bottom: 1px;
    }}
    .partida-desc {{
      color: var(--muted);
      font-size: 9.5px;
      line-height: 1.25;
    }}
    .price-box {{
      margin: 5px 0 6px;
      border: 1.5px solid var(--brand);
      border-radius: 4px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      overflow: hidden;
      page-break-inside: avoid;
    }}
    .price-base {{
      padding: 6px 12px;
      background: var(--soft);
    }}
    .price-final {{
      padding: 6px 12px;
      background: var(--brand);
      color: #fff;
      text-align: right;
    }}
    .price-amount {{
      font-size: 19px;
      font-weight: 800;
      margin-top: 1px;
      color: var(--accent-light);
    }}
    .price-base .price-amount {{
      color: var(--brand);
    }}
    .two-col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin: 4px 0 5px;
      page-break-inside: avoid;
    }}
    .two-col .col {{
      border: 1px solid var(--line);
      border-radius: 3px;
      padding: 5px 8px;
      background: #fff;
    }}
    .two-col h5 {{
      margin: 0 0 3px;
      color: var(--brand);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.2px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    ul.compact {{
      margin: 0 0 0 12px;
      padding: 0;
      font-size: 9.5px;
      color: var(--muted);
    }}
    ul.compact li {{
      margin: 1.5px 0;
    }}
    .sign-section {{
      margin-top: 5px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      page-break-inside: avoid;
    }}
    .sign-box {{
      min-height: 38px;
      border: 1px dashed var(--line);
      border-radius: 3px;
      padding: 4px 7px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: var(--muted);
      font-size: 9px;
      background: var(--soft);
    }}
    .sign-box strong {{
      color: var(--brand);
    }}
    footer {{
      margin-top: 6px;
      padding-top: 4px;
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      font-size: 9px;
    }}
    @media print {{
      @page {{
        size: A4 portrait;
        margin: 0;
      }}
      body {{
        background: #fff;
      }}
      .page {{
        width: 210mm;
        height: 297mm;
        max-height: 297mm;
        margin: 0;
        box-shadow: none;
        padding: 8mm 13mm 6mm;
        overflow: hidden;
        page-break-after: avoid;
        page-break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <div>
      <header>
        <div class="company">
          <div class="logo">
            <img src="logo-ham.svg" alt="HAM Estructuras Metálicas">
          </div>
          <div class="company-info">
            <h1>HAM ESTRUCTURAS METÁLICAS</h1>
            <p><strong>Dixis Recursos y Soluciones S.L.</strong> • CIF: B57825432</p>
            <p>Circunval·lació, 11 • Polígono Industrial de Sant Lluís, Menorca</p>
            <p>+34 669 769 541 • pablo@dixis.es • www.hamenorca.com</p>
          </div>
        </div>
        <div class="meta">
          <h2>PRESUPUESTO</h2>
          <div class="ref-badge">{DATA['referencia']}</div>
          <p><strong>Fecha:</strong> {DATA['fecha']}</p>
          <p><strong>Validez:</strong> {DATA['validez_dias']} días</p>
        </div>
      </header>

      <section class="hero">
        <h3>{DATA['proyecto']['titulo']}</h3>
        <p>{DATA['proyecto']['descripcion']}</p>
      </section>

      <section class="grid-meta">
        <div class="card">
          <span class="label">Cliente / Contacto</span>
          <span class="value">{DATA['cliente']['nombre']}</span>
        </div>
        <div class="card">
          <span class="label">Contacto Técnico</span>
          <span class="value">{DATA['cliente']['contacto_tecnico']}</span>
        </div>
        <div class="card">
          <span class="label">Perfil Adoptado</span>
          <span class="value">2 x UPE 200 (S275)</span>
        </div>
        <div class="card">
          <span class="label">Acabado Anticorrosivo</span>
          <span class="value">C5 Marino Blanco</span>
        </div>
      </section>

      <h4>Desglose Económico y Valoración de Partidas</h4>
      <table>
        <thead>
          <tr>
            <th class="c" style="width: 28px;">Nº</th>
            <th>Concepto y Especificación Técnica</th>
            <th class="c" style="width: 32px;">Ud</th>
            <th class="r" style="width: 44px;">Cant.</th>
            <th class="r" style="width: 70px;">Precio Ud</th>
            <th class="r" style="width: 80px;">Importe</th>
          </tr>
        </thead>
        <tbody>"""

    for p in DATA["partidas"]:
        html_content += f"""
          <tr>
            <td class="c bold">{p['id']}</td>
            <td>
              <div class="partida-title">{p['concepto']}</div>
              <div class="partida-desc">{p['descripcion']}</div>
            </td>
            <td class="c">{p['unidad']}</td>
            <td class="r">{p['cantidad']:.2f}</td>
            <td class="r">{p['precio_unitario']:.2f} €</td>
            <td class="r bold">{p['importe']:.2f} €</td>
          </tr>"""

    html_content += f"""
        </tbody>
      </table>

      <section class="price-box">
        <div class="price-base">
          <span class="label">Base Imponible Neta</span>
          <div class="price-amount">{DATA['totales']['base_imponible']:,.2f} €</div>
          <span style="font-size: 9.5px; color: var(--muted);">I.V.A. 21%: {DATA['totales']['iva_importe']:,.2f} €</span>
        </div>
        <div class="price-final">
          <span class="label" style="color: #cbd5e1;">Importe Total (I.V.A. Incluido)</span>
          <div class="price-amount">{DATA['totales']['total_presupuesto']:,.2f} €</div>
          <span style="font-size: 9.5px; color: #cbd5e1;">Impuestos incluidos</span>
        </div>
      </section>

      <div class="two-col">
        <div class="col">
          <h5>Condiciones de Ejecución y Garantía</h5>
          <ul class="compact">
            <li><strong>Fabricación:</strong> Procesos de corte, mecanizado y preparación de taller según normativa.</li>
            <li><strong>Protección C5 Marino:</strong> Aplicación según norma ISO 12944 acabado Blanco (sin horno).</li>
            <li><strong>Plazo:</strong> {DATA['condiciones']['plazo_entrega']}</li>
            <li><strong>Forma de pago:</strong> {DATA['condiciones']['forma_pago']}</li>
          </ul>
        </div>
        <div class="col">
          <h5>Condiciones de Obra y Exclusiones</h5>
          <ul class="compact">
            <li><strong>Logística:</strong> Sin logística incluida (transporte a obra y subida a piso a cargo del cliente).</li>
            <li><strong>Exclusiones:</strong> {DATA['condiciones']['exclusiones']}</li>
            <li><strong>Seguridad interior:</strong> Se emplean mantas ignífugas de fibra de vidrio y extintor a pie de tajo.</li>
          </ul>
        </div>
      </div>

      <section class="sign-section">
        <div class="sign-box">
          <span><strong>Por HAM Estructuras Metálicas (DIXIS)</strong></span>
          <span>Pablo Sebastián Sánchez Arnoletto</span>
        </div>
        <div class="sign-box">
          <span><strong>Aceptación del Cliente</strong></span>
          <span>Firma / Conforme: {DATA['cliente']['nombre']}</span>
        </div>
      </section>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • C.I.F. B57825432 • Sant Lluís, Menorca</div>
      <div>P-2026-0051 (Rev. 1) • Dintel UPE 200 Soldado In Situ • Hoja 1 de 1</div>
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
    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Memoria Técnica Operativa {DATA['codigo']} (Rev 1) • {DATA['proyecto']['titulo']}</title>
  <style>
    :root {{
      --ink: #0f172a;
      --muted: #475569;
      --line: #cbd5e1;
      --soft: #f8fafc;
      --brand: #0f172a;
      --accent: #b45309;
      --card-bg: #f1f5f9;
      --tech-blue: #0369a1;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #cbd5e1;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 13px;
      line-height: 1.45;
    }}
    .page {{
      width: 210mm;
      min-height: 297mm;
      margin: 20px auto;
      background: #fff;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
      padding: 16mm 18mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 6px solid var(--tech-blue);
      padding-top: 12px;
      padding-bottom: 10px;
      border-bottom: 2px solid var(--line);
    }}
    .title-group h1 {{
      margin: 0;
      color: var(--brand);
      font-size: 18px;
      font-weight: 800;
    }}
    .title-group p {{
      margin: 2px 0 0;
      color: var(--muted);
      font-size: 11.5px;
    }}
    .badge-tech {{
      background: #e0f2fe;
      color: #0369a1;
      border: 1px solid #bae6fd;
      padding: 4px 8px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 11.5px;
      font-family: monospace;
    }}
    h3 {{
      margin: 14px 0 6px;
      color: var(--tech-blue);
      font-size: 13.5px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      border-bottom: 1.5px solid var(--line);
      padding-bottom: 3px;
    }}
    .tech-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin: 8px 0 12px;
    }}
    .tech-box {{
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 8px 10px;
    }}
    .tech-box .lbl {{
      display: block;
      color: var(--muted);
      font-size: 10px;
      text-transform: uppercase;
      font-weight: 600;
      margin-bottom: 2px;
    }}
    .tech-box .val {{
      font-weight: 700;
      color: var(--brand);
      font-size: 12px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0 14px;
    }}
    th {{
      background: var(--tech-blue);
      color: #fff;
      font-size: 11px;
      text-align: left;
      padding: 6px 8px;
      text-transform: uppercase;
    }}
    td {{
      padding: 6px 8px;
      border-bottom: 1px solid var(--line);
      font-size: 11.5px;
    }}
    tr:nth-child(even) td {{
      background: #f8fafc;
    }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .alert-box {{
      background: #eff6ff;
      border-left: 4px solid var(--tech-blue);
      padding: 8px 12px;
      margin: 10px 0;
      font-size: 11.5px;
      color: #1e3a8a;
      border-radius: 0 4px 4px 0;
    }}
    .procedure {{
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 10px 12px;
      margin: 8px 0;
    }}
    .procedure ol {{
      margin: 4px 0 4px 18px;
      padding: 0;
      font-size: 11px;
      color: var(--ink);
    }}
    .procedure li {{
      margin: 4px 0;
    }}
    footer {{
      margin-top: 14px;
      padding-top: 8px;
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      font-size: 10px;
    }}
    @media print {{
      @page {{
        size: A4 portrait;
        margin: 0;
      }}
      body {{ background: #fff; }}
      .page {{
        width: 210mm;
        height: 297mm;
        margin: 0;
        box-shadow: none;
        padding: 12mm 15mm;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <div>
      <header>
        <div class="title-group">
          <h1>MEMORIA TÉCNICA Y OPERATIVA DE TALLER Y OBRA (REV. 1)</h1>
          <p>Proyecto {DATA['codigo']} • {DATA['cliente']['nombre']} • Coordinación técnica con Joan</p>
        </div>
        <div class="badge-tech">USO INTERNO / OFICINA TÉCNICA</div>
      </header>

      <h3>1. Justificación Estructural y Dimensionamiento (Cálculo de Joan)</h3>
      <div class="tech-grid">
        <div class="tech-box">
          <span class="lbl">Perfil Estructural</span>
          <span class="val">2 x UPE 200 (S275 EN 10025-2)</span>
        </div>
        <div class="tech-box">
          <span class="lbl">Configuración Seccional</span>
          <span class="val">Doble en I unión soldada</span>
        </div>
        <div class="tech-box">
          <span class="lbl">Luz Cálculo / Longitud Perfil</span>
          <span class="val">L = 2,66 m / Perfiles: 3,20 m</span>
        </div>
        <div class="tech-box">
          <span class="lbl">Peso Acero Total</span>
          <span class="val">145,92 kg (45,6 kg/m compuesto)</span>
        </div>
        <div class="tech-box">
          <span class="lbl">Momento Flector Cálculo</span>
          <span class="val">MEd+ = 2,084 t·m (η = 35,5%)</span>
        </div>
        <div class="tech-box">
          <span class="lbl">Cortante Máximo Cálculo</span>
          <span class="val">VEd = 3,133 t (η = 15,1%)</span>
        </div>
      </div>

      <div class="alert-box">
        <strong>Ajustes Aplicados en Rev. 1:</strong> Tarificación de mano de obra de taller a <strong>35,00 €/h</strong> (2,5 h reales = 87,50 €), tratamiento anticorrosivo C5 Marino a <strong>50,00 €/m²</strong> (5 m² = 250,00 €) y <strong>exclusión total de la logística y transporte</strong> a obra (porte y acarreo a cargo del cliente). Redacción de partidas cliente limpia de fórmulas internas de mano de obra.
      </div>

      <h3>2. Procedimiento Operativo de Fabricación, Montaje y Soldadura</h3>
      <div class="procedure">
        <ol>
          <li><strong>Corte y mecanizado en taller (2,5 h a 35 €/h):</strong> Corte a sierra de cinta de los 2 perfiles UPE 200 a 3.200 mm. Trazado y taladrado de perforaciones pasantes Ø22 mm en el alma de uno de los perfiles con espaciado regular (8-10 uds) para permitir el botón de soldadura (plug weld). Chaflanado inferior de 45° para el cordón discontinuo.</li>
          <li><strong>Pintura C5 Marino Blanco en taller a 50 €/m² (Regla estricta HAM: SIN HORNO):</strong> Granallado/limpieza Sa 2½, imprimación epoxi fosfato de zinc 75-80 µm, capa intermedia epoxi barrera 100-120 µm y acabado esmalte poliuretano alifático 2C color blanco 50-60 µm (DFT ≥ 240 µm).</li>
          <li><strong>Sin logística:</strong> Entrega de los perfiles en taller o acarreo directo a obra gestionado por el cliente.</li>
          <li><strong>Montaje in situ en apartamento:</strong> Despliegue de mantas ignífugas de fibra de vidrio para protección total de solados y cerramientos contiguos. Presentación de perfiles sobre apoyos y prensado con mordazas mecánicas para unión íntima de almas.</li>
          <li><strong>Soldadura in situ:</strong> Ejecución de botones de soldadura por penetración completa a través de las perforaciones del alma y ejecución de cordones discontinuos en la arista inferior.</li>
          <li><strong>Pasivación y retoque C5 Marino:</strong> Desescoriado, esmerilado, aplicación de imprimación rica en zinc y esmalte poliuretano alifático bicomponente blanco para sellar y restituir la protección anticorrosiva marina en todas las zonas soldadas.</li>
        </ol>
      </div>

      <h3>3. Escandallo de Costes Directos y Margen Bruto (Revisión 1)</h3>
      <table>
        <thead>
          <tr>
            <th>Concepto de Coste</th>
            <th>Tipo Recurso</th>
            <th class="r">Medición</th>
            <th class="r">Coste Directo</th>
            <th class="r">PVP Venta</th>
            <th class="r">Margen Bruto</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Perfiles UPE 200 (6,40 m / 146 kg)</td>
            <td>Acero laminado S275</td>
            <td class="r">146,00 kg</td>
            <td class="r">211,70 €</td>
            <td class="r bold">320,00 €</td>
            <td class="r">108,30 €</td>
          </tr>
          <tr>
            <td>Mecanizado de almas y biselado (35 €/h)</td>
            <td>Mano obra taller (2,5 h a 28 €/h coste)</td>
            <td class="r">2,50 h</td>
            <td class="r">70,00 €</td>
            <td class="r bold">87,50 €</td>
            <td class="r">17,50 €</td>
          </tr>
          <tr>
            <td>Sistema C5 Marino Blanco (a 50 €/m²)</td>
            <td>Tratamiento epoxi + PU 2C</td>
            <td class="r">5,00 m²</td>
            <td class="r">125,00 €</td>
            <td class="r bold">250,00 €</td>
            <td class="r">125,00 €</td>
          </tr>
          <tr>
            <td>Montaje, soldadura y protecciones in situ</td>
            <td>Mano obra obra (8,0 h a 28 €/h) + medios</td>
            <td class="r">8,00 h</td>
            <td class="r">249,00 €</td>
            <td class="r bold">320,00 €</td>
            <td class="r">71,00 €</td>
          </tr>
          <tr>
            <td>Sellado y retoque C5 Marino in situ</td>
            <td>Mano obra y pintura (2,0 h a 28 €/h)</td>
            <td class="r">2,00 h</td>
            <td class="r">71,00 €</td>
            <td class="r bold">100,00 €</td>
            <td class="r">29,00 €</td>
          </tr>
          <tr style="background: #f1f5f9; font-weight: 800; border-top: 2px solid var(--tech-blue);">
            <td colspan="3">TOTALES ESCANDALLO DIRECTO:</td>
            <td class="r">726,70 €</td>
            <td class="r" style="color: var(--tech-blue); font-size: 13px;">1.077,50 €</td>
            <td class="r" style="color: #059669; font-size: 13px;">350,80 € (32,6%)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • HAM Menorca • Oficina Técnica</div>
      <div>P-2026-0051 (Rev. 1) • Memoria Técnica Operativa • Hoja 1 de 1</div>
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
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{html_file.replace(os.sep, '/')}")
        page.pdf(
            path=pdf_file,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        browser.close()
    print(f"PDF generado con éxito en: {pdf_file}")

if __name__ == "__main__":
    excel_path = create_excel()
    client_html = create_html_client()
    client_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    convert_to_pdf(client_html, client_pdf)
    
    tech_html = create_html_technical()
    tech_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")
    convert_to_pdf(tech_html, tech_pdf)
    
    print("\nTodos los documentos de P-2026-0051 han sido actualizados exitosamente.")
