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
    GOLD = "B45309"        # Acento dorado / óxido
    SLATE_LIGHT = "F8FAFC" # Fila alterna
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"   # Amarillo suave
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
    
    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO: {DATA['codigo']} • {DATA['proyecto']['titulo']}"
    ws1["B3"].font = font_title
    
    ws1["B5"] = "REFERENCIA:"
    ws1["C5"] = DATA["referencia"]
    ws1["B6"] = "CLIENTE:"
    ws1["C6"] = f"{DATA['cliente']['nombre']} (Atn: {DATA['cliente']['contacto_tecnico']})"
    ws1["B7"] = "UBICACIÓN:"
    ws1["C7"] = DATA["cliente"]["ubicacion"]
    ws1["B8"] = "FECHA:"
    ws1["C8"] = DATA["fecha"]
    ws1["B9"] = "VALIDEZ:"
    ws1["C9"] = f"{DATA['validez_dias']} días"
    
    for r in range(5, 10):
        ws1[f"B{r}"].font = font_bold
        ws1[f"C{r}"].font = font_reg

    headers_client = ["Nº", "Partida y Descripción Técnica", "Ud.", "Cantidad", "Precio Unitario", "Subtotal"]
    for c_idx, h in enumerate(headers_client, start=2):
        cell = ws1.cell(row=11, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[11].height = 24

    current_row = 12
    for p in DATA["partidas"]:
        ws1.cell(row=current_row, column=2, value=p["id"]).font = font_bold
        ws1.cell(row=current_row, column=2).alignment = Alignment(horizontal="center", vertical="top")
        
        desc_full = f"{p['concepto']}\n{p['descripcion']}"
        desc_cell = ws1.cell(row=current_row, column=3, value=desc_full)
        desc_cell.font = font_reg
        desc_cell.alignment = Alignment(wrap_text=True, vertical="top")
        
        ud_cell = ws1.cell(row=current_row, column=4, value=p["unidad"])
        ud_cell.font = font_reg
        ud_cell.alignment = Alignment(horizontal="center", vertical="top")
        
        cant_cell = ws1.cell(row=current_row, column=5, value=p["cantidad"])
        cant_cell.font = font_reg
        cant_cell.alignment = Alignment(horizontal="right", vertical="top")
        cant_cell.number_format = '#,##0.00'
        
        price_cell = ws1.cell(row=current_row, column=6, value=p["precio_unitario"])
        price_cell.font = font_reg
        price_cell.alignment = Alignment(horizontal="right", vertical="top")
        price_cell.number_format = '#,##0.00 €'
        
        sub_cell = ws1.cell(row=current_row, column=7, value=f"=E{current_row}*F{current_row}")
        sub_cell.font = font_bold
        sub_cell.alignment = Alignment(horizontal="right", vertical="top")
        sub_cell.number_format = '#,##0.00 €'
        
        for c_idx in range(2, 8):
            ws1.cell(row=current_row, column=c_idx).border = border_thin
            if (current_row % 2 == 0):
                ws1.cell(row=current_row, column=c_idx).fill = fill_alt
                
        ws1.row_dimensions[current_row].height = 54
        current_row += 1

    # Totales
    current_row += 1
    ws1.cell(row=current_row, column=6, value="BASE IMPONIBLE:").font = font_bold
    ws1.cell(row=current_row, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=current_row, column=7, value=f"=SUM(G12:G{current_row-2})").font = font_tot
    ws1.cell(row=current_row, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=current_row, column=7).border = border_thin
    base_row = current_row

    current_row += 1
    ws1.cell(row=current_row, column=6, value="I.V.A. (21%):").font = font_bold
    ws1.cell(row=current_row, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=current_row, column=7, value=f"=G{base_row}*0.21").font = font_bold
    ws1.cell(row=current_row, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=current_row, column=7).border = border_thin
    iva_row = current_row

    current_row += 1
    ws1.cell(row=current_row, column=6, value="TOTAL PRESUPUESTO:").font = font_tot_gold
    ws1.cell(row=current_row, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=current_row, column=7, value=f"=G{base_row}+G{iva_row}").font = font_tot_gold
    ws1.cell(row=current_row, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=current_row, column=7).fill = fill_tot
    ws1.cell(row=current_row, column=7).border = border_total

    # Condiciones comerciales
    current_row += 2
    ws1.cell(row=current_row, column=2, value="CONDICIONES COMERCIALES Y DE EJECUCIÓN:").font = font_sec
    current_row += 1
    ws1.cell(row=current_row, column=2, value=f"• Forma de Pago: {DATA['condiciones_comerciales']['forma_pago']}").font = font_reg
    current_row += 1
    ws1.cell(row=current_row, column=2, value=f"• Plazo de Instalación: {DATA['condiciones_comerciales']['plazo_ejecucion']}").font = font_reg
    current_row += 1
    ws1.cell(row=current_row, column=2, value=f"• Garantía: {DATA['condiciones_comerciales']['garantia']}").font = font_reg
    current_row += 1
    ws1.cell(row=current_row, column=2, value=f"• Revisiones Obligatorias: {DATA['condiciones_comerciales']['revisiones']}").font = font_reg

    ws1.column_dimensions["A"].width = 3
    ws1.column_dimensions["B"].width = 6
    ws1.column_dimensions["C"].width = 54
    ws1.column_dimensions["D"].width = 10
    ws1.column_dimensions["E"].width = 12
    ws1.column_dimensions["F"].width = 18
    ws1.column_dimensions["G"].width = 18

    # -------------------------------------------------------------------------
    # HOJA 2: ESTUDIO TÉCNICO INTERNO Y ESCANDALLO
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Estudio Técnico Interno")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. • USO INTERNO CONFIDENCIAL"
    ws2["B2"].font = font_sub
    ws2["B3"] = f"ESCANDALLO TÉCNICO Y RENTABILIDAD: {DATA['codigo']} • LÍNEA DE VIDA SANT LLUÍS"
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
        ["Kit Línea Vida 20m (L-2653 T6, cable 10mm 7x19, tensor, placa)", "Materiales certificados EN 795", 1.0, 380.00, "=D6*E6", 520.00],
        ["Fijaciones estructurales homologadas soporte nave", "Tornillería 8.8 / anclajes ETA", 1.0, 65.00, "=D7*E7", 110.00],
        ["Mano de obra montaje e instalación (2 operarios x 4,5 h)", "Mano de obra en altura (9,0 h)", 9.0, 22.00, "=D8*E8", 342.00],
        ["Plataforma Elevadora Móvil PEMP (1 jornada Sant Lluís)", "Maquinaria / elevación", 1.0, 140.00, "=D9*E9", 220.00],
        ["Pruebas de carga dinamómetro, placa y certificado técnico", "Ensayos y visado", 1.0, 70.00, "=D10*E10", 160.00]
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

    # Resumen rentabilidad
    ws2["B13"] = "INDICADORES CLAVE DE RENTABILIDAD:"
    ws2["B13"].font = font_sec
    ws2["B14"] = "Coste Directo Total:"
    ws2["C14"] = "=F11"
    ws2["C14"].number_format = '#,##0.00 €'
    ws2["B15"] = "Precio de Venta Base Imponible:"
    ws2["C15"] = "=G11"
    ws2["C15"].number_format = '#,##0.00 €'
    ws2["B16"] = "Margen Bruto de Contribución:"
    ws2["C16"] = "=H11"
    ws2["C16"].number_format = '#,##0.00 €'
    ws2["B17"] = "Margen sobre Venta (%):"
    ws2["C17"] = "=H11/G11"
    ws2["C17"].number_format = '0.0%'
    ws2["B18"] = "Margen sobre Coste (%):"
    ws2["C18"] = "=H11/F11"
    ws2["C18"].number_format = '0.0%'

    for r in range(14, 19):
        ws2[f"B{r}"].font = font_bold
        ws2[f"C{r}"].font = font_bold

    ws2.column_dimensions["A"].width = 3
    ws2.column_dimensions["B"].width = 44
    ws2.column_dimensions["C"].width = 25
    ws2.column_dimensions["D"].width = 16
    ws2.column_dimensions["E"].width = 15
    ws2.column_dimensions["F"].width = 18
    ws2.column_dimensions["G"].width = 16
    ws2.column_dimensions["H"].width = 16

    # -------------------------------------------------------------------------
    # HOJA 3: FICHA TÉCNICA Y NORMATIVA
    # -------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="Ficha Técnica UNE-EN 795")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3["B2"] = "DIXIS / HAM MENORCA • ESPECIFICACIONES TÉCNICAS DE DISPOSITIVO"
    ws3["B2"].font = font_sub
    ws3["B3"] = "PARÁMETROS TÉCNICOS Y CONDICIONES DE SEGURIDAD UNE-EN 795 TIPO C"
    ws3["B3"].font = font_title

    params = [
        ("Longitud Total de Línea", f"{DATA['parametros_tecnicos']['longitud_total_ml']} metros"),
        ("Tipo de Sistema Anticaídas", DATA['parametros_tecnicos']['tipo_sistema']),
        ("Disipación de Energía", DATA['parametros_tecnicos']['amortiguador']),
        ("Anclajes Terminales", DATA['parametros_tecnicos']['anclajes_terminales']),
        ("Anclaje Intermedio", DATA['parametros_tecnicos']['anclaje_intermedio']),
        ("Luz entre Apoyos / Vanos", f"{DATA['parametros_tecnicos']['distancia_entre_soportes_m']} m (2 vanos de 10 m)"),
        ("Cable Flexible", DATA['parametros_tecnicos']['cable']),
        ("Tensor y Regulación", DATA['parametros_tecnicos']['tensor']),
        ("Terminal y Guiado", f"{DATA['parametros_tecnicos']['terminal_y_sujecion']} • {DATA['parametros_tecnicos']['protector_cabo']}"),
        ("Fijaciones Estructurales", DATA['parametros_tecnicos']['fijaciones_soporte']),
        ("Usuarios Simultáneos Autorizados", DATA['parametros_tecnicos']['numero_usuarios_admitidos']),
        ("Gálibo Mínimo de Caída Libre", f"{DATA['parametros_tecnicos']['altura_libre_caida_minima_m']} metros"),
        ("Señalización y Precintado", f"{DATA['parametros_tecnicos']['senalizacion']} con {DATA['parametros_tecnicos']['seguridad_adicional']}"),
        ("Centro Operativo y Logística", f"Taller HAM en {DATA['parametros_tecnicos']['taller_base']} (respuesta inmediata en Sant Lluís)")
    ]

    ws3.cell(row=5, column=2, value="Parámetro Técnico").font = font_header
    ws3.cell(row=5, column=2).fill = fill_header
    ws3.cell(row=5, column=2).border = border_thin
    ws3.cell(row=5, column=3, value="Especificación Homologada").font = font_header
    ws3.cell(row=5, column=3).fill = fill_header
    ws3.cell(row=5, column=3).border = border_thin

    for i, (k, v) in enumerate(params, start=6):
        ws3.cell(row=i, column=2, value=k).font = font_bold
        ws3.cell(row=i, column=2).border = border_thin
        ws3.cell(row=i, column=3, value=v).font = font_reg
        ws3.cell(row=i, column=3).border = border_thin
        ws3.cell(row=i, column=3).alignment = Alignment(wrap_text=True)
        if i % 2 == 0:
            ws3.cell(row=i, column=2).fill = fill_alt
            ws3.cell(row=i, column=3).fill = fill_alt
        ws3.row_dimensions[i].height = 22

    ws3.column_dimensions["A"].width = 3
    ws3.column_dimensions["B"].width = 32
    ws3.column_dimensions["C"].width = 75

    excel_file = os.path.join(BASE_DIR, "Presupuesto_P2026_0055_Linea_de_Vida_Sant_Lluis.xlsx")
    wb.save(excel_file)
    print(f"Excel generado en: {excel_file}")
    return excel_file

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
      font-size: 10px;
      line-height: 1.30;
    }}
    .page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 7mm 12mm 5mm;
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
      gap: 12px;
      align-items: center;
      border-top: 4px solid var(--brand);
      padding-top: 6px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--line);
    }}
    .company {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .logo {{
      width: 105px;
      flex: 0 0 105px;
    }}
    .logo img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .company-info h1 {{
      margin: 0;
      color: var(--brand);
      font-size: 14px;
      font-weight: 800;
      letter-spacing: -0.2px;
    }}
    .company-info p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 9.5px;
    }}
    .meta {{
      text-align: right;
    }}
    .meta h2 {{
      margin: 0;
      color: var(--accent);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 0.5px;
    }}
    .meta .ref-badge {{
      display: inline-block;
      background: var(--brand);
      color: #fff;
      font-size: 9px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 3px;
      margin: 2px 0;
    }}
    .meta p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 9px;
    }}
    .hero {{
      margin-top: 6px;
      background: var(--soft);
      border-left: 3px solid var(--accent);
      padding: 5px 9px;
      border-radius: 0 4px 4px 0;
    }}
    .hero h3 {{
      margin: 0 0 2px;
      color: var(--brand);
      font-size: 11.5px;
      font-weight: 700;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 9.5px;
    }}
    .grid-meta {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-top: 6px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 4px 7px;
    }}
    .card .label {{
      display: block;
      font-size: 8px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      color: var(--muted);
      font-weight: 700;
      margin-bottom: 1px;
    }}
    .card .value {{
      font-size: 9.5px;
      font-weight: 700;
      color: var(--brand);
    }}
    h4 {{
      margin: 7px 0 4px;
      color: var(--brand);
      font-size: 10.5px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 9px;
      margin-bottom: 6px;
    }}
    th {{
      background: var(--brand);
      color: #fff;
      padding: 4px 6px;
      font-size: 8.5px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      font-weight: 700;
      border: 1px solid var(--brand);
    }}
    td {{
      padding: 4px 6px;
      border: 1px solid var(--line);
      vertical-align: top;
    }}
    tr:nth-child(even) td {{
      background: var(--soft);
    }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .partida-title {{
      font-weight: 700;
      color: var(--brand);
      margin-bottom: 1px;
    }}
    .partida-desc {{
      color: var(--muted);
      font-size: 8px;
      line-height: 1.25;
    }}
    .price-box {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 6px 10px;
      margin-bottom: 6px;
      align-items: center;
    }}
    .price-base {{
      text-align: left;
    }}
    .price-base .label {{
      font-size: 8.5px;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 700;
    }}
    .price-base .price-amount {{
      font-size: 15px;
      font-weight: 800;
      color: var(--brand);
    }}
    .price-final {{
      text-align: right;
      background: var(--brand);
      color: #fff;
      padding: 6px 10px;
      border-radius: 4px;
    }}
    .price-final .label {{
      font-size: 8.5px;
      text-transform: uppercase;
      font-weight: 700;
      opacity: 0.9;
    }}
    .price-final .price-amount {{
      font-size: 17px;
      font-weight: 800;
      color: #fef08a;
    }}
    .two-col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 6px;
    }}
    .col {{
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 5px 8px;
    }}
    .col h5 {{
      margin: 0 0 3px;
      font-size: 9px;
      color: var(--brand);
      font-weight: 700;
      text-transform: uppercase;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    ul.compact {{
      margin: 0;
      padding-left: 13px;
      font-size: 8px;
      color: var(--muted);
      line-height: 1.25;
    }}
    ul.compact li {{
      margin-bottom: 2px;
    }}
    .sign-section {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 4px;
      padding-top: 4px;
      border-top: 1px solid var(--line);
    }}
    .sign-box {{
      height: 38px;
      border: 1px dashed var(--line);
      border-radius: 4px;
      padding: 4px 6px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      font-size: 8px;
      color: var(--muted);
    }}
    footer {{
      border-top: 1px solid var(--line);
      padding-top: 4px;
      display: flex;
      justify-content: space-between;
      font-size: 8px;
      color: var(--muted);
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
        <p>Suministro integral, fijaciones estructurales certificadas, medios de elevación y montaje completo en altura conforme a UNE-EN 795:2012 Tipo C y UNE-CEN/TS 16415 para nave en Sant Lluís.</p>
      </section>

      <section class="grid-meta">
        <div class="card">
          <span class="label">Cliente / Ubicación</span>
          <span class="value">Nave Sant Lluís</span>
        </div>
        <div class="card">
          <span class="label">Longitud / Vanos</span>
          <span class="value">20,00 ml (2 x 10 m)</span>
        </div>
        <div class="card">
          <span class="label">Normativa / Clase</span>
          <span class="value">EN 795 Tipo C (2 Pers.)</span>
        </div>
        <div class="card">
          <span class="label">Instalación y Pruebas</span>
          <span class="value">Incluida + Ensayo Tiro</span>
        </div>
      </section>

      <h4>Desglose Económico y Valoración de Partidas</h4>
      <table>
        <thead>
          <tr>
            <th class="c" style="width: 24px;">Nº</th>
            <th>Concepto y Especificación Técnica Homologada</th>
            <th class="c" style="width: 28px;">Ud</th>
            <th class="r" style="width: 36px;">Cant.</th>
            <th class="r" style="width: 65px;">Precio Ud</th>
            <th class="r" style="width: 75px;">Importe</th>
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
            <td class="r bold">{p['subtotal']:.2f} €</td>
          </tr>"""

    html_content += f"""
        </tbody>
      </table>

      <section class="price-box">
        <div class="price-base">
          <span class="label">Base Imponible Neta ({DATA['parametros_tecnicos']['longitud_total_ml']} ml a {DATA['totales']['precio_por_metro_lineal_sin_iva']:.2f} €/ml)</span>
          <div class="price-amount">{DATA['totales']['base_imponible']:.2f} €</div>
          <span style="font-size: 8.5px; color: var(--muted);">I.V.A. 21%: {DATA['totales']['iva_importe']:.2f} €</span>
        </div>
        <div class="price-final">
          <span class="label" style="color: #cbd5e1;">Importe Total Llave en Mano</span>
          <div class="price-amount">{DATA['totales']['total_con_iva']:.2f} €</div>
          <span style="font-size: 8.5px; color: #cbd5e1;">Impuestos incluidos (I.V.A. 21%)</span>
        </div>
      </section>

      <div class="two-col">
        <div class="col">
          <h5>Inclusiones y Ventajas en Sant Lluís</h5>
          <ul class="compact">
            <li><strong>Suministro integral:</strong> 2 anclajes terminales y 1 intermedio en aluminio L-2653 T6 epoxi, cable flexible galvanizado Ø10 mm (7x19, rotura > 62 kN), tensor forjado ojo-horquilla, terminales, guardacabos y precintos.</li>
            <li><strong>Fijaciones homologadas:</strong> Tornillería 8.8 cincada con contraplacas para fijación a vigas o anclajes certificados con sellado EPDM.</li>
            <li><strong>Mano de obra y elevación:</strong> Equipo de 2 operarios certificados en altura y plataforma elevadora PEMP (1 jornada).</li>
            <li><strong>Proximidad operativa:</strong> Taller HAM en Sant Lluís (sin recargos por desplazamientos).</li>
          </ul>
        </div>
        <div class="col">
          <h5>Legalización, Garantía y Condiciones</h5>
          <ul class="compact">
            <li><strong>Legalización oficial:</strong> Ensayo in situ con dinamómetro calibrado, marcado de placa indeleble, Certificado de Instalación visado y Libro de Revisiones.</li>
            <li><strong>Garantía:</strong> 2 años de garantía en materiales y montaje.</li>
            <li><strong>Forma de pago:</strong> 100% a la aceptación del presupuesto (directiva estándar HAM).</li>
            <li><strong>Exclusiones:</strong> Equipos EPI individuales (arneses/eslingas), refuerzos estructurales de cubierta ajenos a fijación y licencias municipales.</li>
          </ul>
        </div>
      </div>

      <section class="sign-section">
        <div class="sign-box">
          <span><strong>Por HAM Estructuras Metálicas (DIXIS)</strong></span>
          <span>Pablo Sebastián Sánchez Arnoletto</span>
        </div>
        <div class="sign-box">
          <span><strong>Aceptación de la Propiedad (Nave Sant Lluís)</strong></span>
          <span>Firma y Sello de Aceptación:</span>
        </div>
      </section>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • C.I.F. B57825432 • Sant Lluís, Menorca</div>
      <div>{DATA['codigo']} • Línea de Vida Horizontal Permanente Clase C (20 ml) • Hoja 1 de 1</div>
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
  <title>Estudio Técnico Interno {DATA['codigo']} • {DATA['proyecto']['titulo']}</title>
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
      --tech-red: #b91c1c;
      --tech-green: #15803d;
      --accent: #b45309;
      --card-bg: #f1f5f9;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 10px;
      line-height: 1.30;
    }}
    .page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 7mm 12mm 5mm;
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
      gap: 12px;
      align-items: center;
      border-top: 4px solid var(--tech-red);
      padding-top: 6px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--line);
    }}
    .company {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .logo {{
      width: 105px;
      flex: 0 0 105px;
    }}
    .logo img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .company-info h1 {{
      margin: 0;
      color: var(--brand);
      font-size: 13.5px;
      font-weight: 800;
      letter-spacing: -0.2px;
    }}
    .company-info p {{
      margin: 1px 0;
      color: var(--tech-red);
      font-weight: 700;
      font-size: 9.5px;
    }}
    .meta {{
      text-align: right;
    }}
    .meta h2 {{
      margin: 0;
      color: var(--tech-red);
      font-size: 14px;
      font-weight: 800;
    }}
    .meta .ref-badge {{
      display: inline-block;
      background: var(--brand);
      color: #fff;
      font-size: 9px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 3px;
      margin: 2px 0;
    }}
    .meta p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 9px;
    }}
    .hero {{
      margin-top: 6px;
      background: #fef2f2;
      border-left: 3px solid var(--tech-red);
      padding: 5px 9px;
      border-radius: 0 4px 4px 0;
    }}
    .hero h3 {{
      margin: 0 0 2px;
      color: var(--brand);
      font-size: 11px;
      font-weight: 700;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 9px;
    }}
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-top: 6px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 5px 7px;
      text-align: center;
    }}
    .kpi-label {{
      font-size: 8px;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 700;
      display: block;
      margin-bottom: 2px;
    }}
    .kpi-val {{
      font-size: 13px;
      font-weight: 800;
      color: var(--brand);
    }}
    .kpi-val.green {{ color: var(--tech-green); }}
    .kpi-val.red {{ color: var(--tech-red); }}
    h4 {{
      margin: 7px 0 4px;
      color: var(--brand);
      font-size: 10px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8.5px;
      margin-bottom: 6px;
    }}
    th {{
      background: var(--brand);
      color: #fff;
      padding: 4px 5px;
      font-size: 8px;
      text-transform: uppercase;
      font-weight: 700;
      border: 1px solid var(--brand);
    }}
    td {{
      padding: 4px 5px;
      border: 1px solid var(--line);
      vertical-align: top;
    }}
    tr:nth-child(even) td {{
      background: var(--soft);
    }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .two-col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 4px;
    }}
    .col {{
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 5px 8px;
    }}
    .col h5 {{
      margin: 0 0 3px;
      font-size: 8.5px;
      color: var(--brand);
      font-weight: 700;
      text-transform: uppercase;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    ul.compact {{
      margin: 0;
      padding-left: 13px;
      font-size: 8px;
      color: var(--muted);
      line-height: 1.25;
    }}
    ul.compact li {{
      margin-bottom: 2px;
    }}
    footer {{
      border-top: 1px solid var(--line);
      padding-top: 4px;
      display: flex;
      justify-content: space-between;
      font-size: 8px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="page">
    <div>
      <header>
        <div class="company">
          <div class="logo">
            <img src="logo-ham.svg" alt="HAM Menorca">
          </div>
          <div class="company-info">
            <h1>HAM ESTRUCTURAS METÁLICAS • OFICINA TÉCNICA</h1>
            <p>DOCUMENTO DE CONTROL INTERNO Y ESCANDALLO DE COSTES</p>
          </div>
        </div>
        <div class="meta">
          <h2>ESTUDIO TÉCNICO</h2>
          <div class="ref-badge">{DATA['codigo']} • ESCANDALLO</div>
          <p><strong>Fecha:</strong> {DATA['fecha']}</p>
          <p><strong>Ubicación:</strong> Nave en Sant Lluís</p>
        </div>
      </header>

      <section class="hero">
        <h3>Línea de Vida Horizontal Permanente Clase C (20 ml) • Análisis de Margen y Operativa</h3>
        <p>Montaje de sistema de anclaje de cable flexible sin amortiguador de caídas (UNE-EN 795:2012 Tipo C). Distancia entre apoyos: 10,00 m (1 intermedio). Cable galvanizado Ø10 mm (7x19). Apoyo logístico directo desde taller Sant Lluís.</p>
      </section>

      <section class="kpi-row">
        <div class="kpi-card">
          <span class="kpi-label">Coste Directo</span>
          <span class="kpi-val red">{DATA['totales']['coste_directo_total']:.2f} €</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Venta Base Imp.</span>
          <span class="kpi-val">{DATA['totales']['base_imponible']:.2f} €</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Margen Bruto (€)</span>
          <span class="kpi-val green">{DATA['totales']['margen_bruto_euros']:.2f} €</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Margen sobre Venta</span>
          <span class="kpi-val green">{DATA['totales']['margen_bruto_porcentaje']:.1f}%</span>
        </div>
      </section>

      <h4>Escandallo de Recursos, Costes Internos y Precios de Venta</h4>
      <table>
        <thead>
          <tr>
            <th class="c" style="width: 24px;">ID</th>
            <th>Concepto de Coste / Recurso</th>
            <th class="c" style="width: 28px;">Ud</th>
            <th class="r" style="width: 32px;">Cant.</th>
            <th class="r" style="width: 58px;">Coste Ud</th>
            <th class="r" style="width: 65px;">Coste Total</th>
            <th class="r" style="width: 65px;">Venta PVP</th>
            <th class="r" style="width: 65px;">Margen (€)</th>
          </tr>
        </thead>
        <tbody>"""

    for p in DATA["partidas"]:
        margen = p["subtotal"] - p["subtotal_coste"]
        html_content += f"""
          <tr>
            <td class="c bold">{p['id']}</td>
            <td><strong>{p['concepto']}</strong><br><span style="color:var(--muted); font-size:7.5px;">{p['descripcion'][:130]}...</span></td>
            <td class="c">{p['unidad']}</td>
            <td class="r">{p['cantidad']:.2f}</td>
            <td class="r">{p['coste_unitario_interno']:.2f} €</td>
            <td class="r bold">{p['subtotal_coste']:.2f} €</td>
            <td class="r bold">{p['subtotal']:.2f} €</td>
            <td class="r bold" style="color:var(--tech-green);">{margen:.2f} €</td>
          </tr>"""

    html_content += f"""
          <tr style="background:#fef3c7; font-weight:700;">
            <td colspan="5" class="r" style="padding:5px;">TOTALES GENERALES ESCANDALLO:</td>
            <td class="r" style="color:var(--tech-red); padding:5px;">{DATA['totales']['coste_directo_total']:.2f} €</td>
            <td class="r" style="color:var(--brand); padding:5px;">{DATA['totales']['base_imponible']:.2f} €</td>
            <td class="r" style="color:var(--tech-green); padding:5px;">{DATA['totales']['margen_bruto_euros']:.2f} €</td>
          </tr>
        </tbody>
      </table>

      <div class="two-col">
        <div class="col">
          <h5>Planificación Operativa de Montaje</h5>
          <ul class="compact">
            <li><strong>Equipo de trabajo:</strong> 2 oficiales de primera con homologación técnica para montaje de sistemas anticaídas y trabajos verticales (RD 2177/2004).</li>
            <li><strong>Duración estimada:</strong> 1 jornada laboral de 4,5 horas efectivas (9 horas totales de operario).</li>
            <li><strong>Fases de trabajo:</strong> 1) Replanteo y marcado de fijaciones a cota; 2) Taladro y colocación de placas terminales e intermedia con apriete dinamométrico; 3) Tendido y enhebrado de cable 10 mm; 4) Tensado y colocación de terminales manuales y precintos; 5) Prueba de tiro estático con dinamómetro.</li>
            <li><strong>Logística:</strong> Al estar la nave en Sant Lluís, el tiempo de traslado es prácticamente nulo desde nuestra base central de Circunval·lació 11.</li>
          </ul>
        </div>
        <div class="col">
          <h5>Parámetros Críticos de Seguridad y Pruebas</h5>
          <ul class="compact">
            <li><strong>Tracción en anclajes extremos:</strong> El soporte de hormigón o pórtico metálico debe verificar una capacidad resistente ≥ 15 kN axial según UNE-EN 795:2012.</li>
            <li><strong>Tensión nominal de servicio:</strong> Ajuste a $T_0 \approx 0,8 - 1,2 kN$ para garantizar una flecha mínima sin sobrecargar anclajes por dilatación.</li>
            <li><strong>Flecha de caída estimada:</strong> Flecha dinámica máxima calculada en vano de 10 m: $f_f_max ≈ 1,35 m. Altura libre de seguridad requerida: ≥ 4,50 m.</li>
            <li><strong>Prueba in situ:</strong> Ensayo de precarga con dinamómetro a 5 kN en anclajes antes de certificar y entrega de ficha de inspección periódica obligatoria.</li>
          </ul>
        </div>
      </div>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • HAM Menorca • Oficina Técnica</div>
      <div>{DATA['codigo']} • Memoria Técnica Operativa y Escandallo • Hoja 1 de 1</div>
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
    
    print("\nTodos los documentos de P-2026-0055 han sido generados exitosamente.")
