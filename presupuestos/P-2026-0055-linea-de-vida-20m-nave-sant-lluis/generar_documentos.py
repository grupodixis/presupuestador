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
    GOLD = "B45309"        # Acento dorado
    SLATE_LIGHT = "F8FAFC" # Fila alterna
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"   # Amarillo suave
    SECTION_FILL = "F1F5F9"
    HIGHLIGHT_FILL = "EFF6FF"
    
    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_sec = PatternFill(start_color=SECTION_FILL, end_color=SECTION_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    fill_hl = PatternFill(start_color=HIGHLIGHT_FILL, end_color=HIGHLIGHT_FILL, fill_type="solid")
    
    font_title = Font(name="Segoe UI", size=14, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_tot = Font(name="Segoe UI", size=10.5, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=10.5, bold=True, color=GOLD)

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
    # HOJA 1: PRESUPUESTO COMERCIAL 100% LUX-TOP (INSTALACIÓN INTEGRAL)
    # -------------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto LUX-TOP"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO: {DATA['codigo']} • SISTEMA ANTICAÍDAS LUX-TOP® FSE 2003 (20 ML)"
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
    ws1["C9"] = "SISTEMA OFICIAL EXCLUSIVO LUX-TOP® (UNE EN 795:2012 Tipo C / CEN/TS 16415:2013)"
    
    for r in range(5, 10):
        ws1[f"B{r}"].font = font_bold
        ws1[f"C{r}"].font = font_reg

    # MODALIDAD 1
    ws1["B11"] = "MODALIDAD 1: LUX-TOP® FSE 2003 PASO MANUAL (CABLE INOX AISI 316 + POSTES PANEL RVT 12)"
    ws1["B11"].font = font_sec
    
    headers_client = ["Nº", "Partida y Descripción Técnica LUX-TOP", "Ud.", "Cantidad", "Precio Unitario", "Subtotal"]
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
        ws1.row_dimensions[row_cur].height = 36
        row_cur += 1

    # Totales Modalidad 1
    ws1.cell(row=row_cur, column=6, value="BASE IMPONIBLE (MODALIDAD 1):").font = font_bold
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_cur, column=7, value=f"=SUM(G13:G{row_cur-1})").font = font_tot
    ws1.cell(row=row_cur, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_cur, column=7).border = border_thin
    base_1 = row_cur

    row_cur += 1
    ws1.cell(row=row_cur, column=6, value="TOTAL CON IVA 21%:").font = font_tot_gold
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_cur, column=7, value=f"=G{base_1}*1.21").font = font_tot_gold
    ws1.cell(row=row_cur, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_cur, column=7).fill = fill_tot
    ws1.cell(row=row_cur, column=7).border = border_total

    # MODALIDAD 2
    row_cur += 2
    ws1.cell(row=row_cur, column=2, value="MODALIDAD 2: LUX-TOP® FSE 2003 PASO CONTINUO / AUTOMÁTICO (CON CARRO RUNNER)").font = font_sec
    row_cur += 1
    ws1.cell(row=row_cur, column=2, value="Incluye pieza intermedia pasante y carro deslizante de acero inox para transitar sin desengancharse de la línea.").font = font_reg
    row_cur += 1
    ws1.cell(row=row_cur, column=6, value="BASE IMPONIBLE (MODALIDAD 2):").font = font_bold
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_cur, column=7, value=DATA["modalidad_2_paso_continuo"]["totales"]["base_imponible"]).font = font_tot
    ws1.cell(row=row_cur, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_cur, column=7).border = border_thin
    base_2 = row_cur

    row_cur += 1
    ws1.cell(row=row_cur, column=6, value="TOTAL CON IVA 21%:").font = font_tot_gold
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    ws1.cell(row=row_cur, column=7, value=f"=G{base_2}*1.21").font = font_tot_gold
    ws1.cell(row=row_cur, column=7).number_format = '#,##0.00 €'
    ws1.cell(row=row_cur, column=7).fill = fill_tot
    ws1.cell(row=row_cur, column=7).border = border_total

    ws1.column_dimensions["A"].width = 3
    ws1.column_dimensions["B"].width = 8
    ws1.column_dimensions["C"].width = 54
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
    ws2["B3"] = f"ESCANDALLO TÉCNICO DE INSTALACIÓN Y MATERIAL LUX-TOP: {DATA['codigo']}"
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
        ["Cable inox Ø8 mm AISI 316 (LUX-top 000011710)", "Material LUX-TOP (-18% dto)", 22.0, 5.658, "=D6*E6", 151.80],
        ["3 Postes panel sándwich RVT 12 + fijaciones EPDM", "Material LUX-TOP (-18% dto)", 3.0, 160.967, "=D7*E7", 588.90],
        ["Kit cierre cáncamo FSE 2003 (SKE II + Tensor)", "Material LUX-TOP (-18% dto)", 1.0, 400.00, "=D8*E8", 487.80],
        ["Instalación en cubierta (2 oficiales x 6,5 h)", "Mano de obra en altura (13,0 h)", 13.0, 22.00, "=D9*E9", 494.00],
        ["Plataforma Elevadora Móvil PEMP (1 jornada Sant Lluís)", "Maquinaria / elevación", 1.0, 140.00, "=D10*E10", 220.00],
        ["Pruebas de tiro dinamómetro, placa y visado técnico", "Ensayos y certificación", 1.0, 70.00, "=D11*E11", 160.00]
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

    ws2.cell(row=12, column=8, value="=G12-F12").font = font_tot_gold
    ws2.cell(row=12, column=8).number_format = '#,##0.00 €'
    ws2.cell(row=12, column=8).border = border_total

    # Resumen rentabilidad
    ws2["B14"] = "INDICADORES CLAVE DE RENTABILIDAD:"
    ws2["B14"].font = font_sec
    ws2["B15"] = "Coste Material LUX-TOP (Neto Dixis con 18% Dto):"
    ws2["C15"] = "=SUM(F6:F8)"
    ws2["C15"].number_format = '#,##0.00 €'
    ws2["B16"] = "Coste Mano de Obra Instalación (13 h x 22 €):"
    ws2["C16"] = "=F9"
    ws2["C16"].number_format = '#,##0.00 €'
    ws2["B17"] = "Coste Directo Total Dixis:"
    ws2["C17"] = "=F12"
    ws2["C17"].number_format = '#,##0.00 €'
    ws2["B18"] = "Precio de Venta Base Imponible:"
    ws2["C18"] = "=G12"
    ws2["C18"].number_format = '#,##0.00 €'
    ws2["B19"] = "Margen Bruto de Contribución:"
    ws2["C19"] = "=H12"
    ws2["C19"].number_format = '#,##0.00 €'
    ws2["B20"] = "Margen sobre Venta (%):"
    ws2["C20"] = "=H12/G12"
    ws2["C20"].number_format = '0.0%'
    ws2["B21"] = "Forma de Pago con Proveedor LUX-TOP:"
    ws2["C21"] = DATA["proveedor_homologado"]["forma_pago_dixis"]

    for r in range(15, 22):
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
    # HOJA 3: FICHA Y MODELOS LUX-TOP WEB
    # -------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="Modelos LUX-TOP Web")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. • PROVEEDOR EXCLUSIVO DE LÍNEAS DE VIDA"
    ws3["B2"].font = font_sub
    ws3["B3"] = "CATÁLOGO DE MODELOS Y SISTEMAS DISPONIBLES EN WEB (LUX-TOP®)"
    ws3["B3"].font = font_title

    models = [
        ("LUX-top® FSE 2003 (Paso Manual)", "Línea horizontal flexible de cable inox AISI 316 Ø8 mm con absorbedor SKE II. Para cubiertas de mantenimiento."),
        ("LUX-top® FSE 2003 (Paso Continuo)", "Línea horizontal flexible con piezas intermedias pasantes y carro runner para desplazamiento sin desengancharse."),
        ("LUX-top® FSA 2010-H (Raíl Horizontal)", "Línea rígida de raíl de aluminio extruido con carro de rodamiento. Flecha de caída cero para bajo gálibo."),
        ("LUX-top® FSA 2010-V (Raíl Vertical)", "Raíl anticaídas para escaleras fijas de acceso y torres según EN 353-1."),
        ("LUX-top® RVT 12 (Poste Panel Sándwich)", "Poste de anclaje para cubiertas de panel sándwich 2G-3G con 12 remaches 7,7 mm y 4 almohadillas EPDM 130 mm."),
        ("LUX-top® SZM / SZ-S (Poste Chapa Grecada)", "Poste para cubiertas de chapa metálica perfilada con fijación estanca certificada."),
        ("LUX-top® STA / STE (Postes para Viga de Acero)", "Soportes estructurales con bridas de apriete a perfiles IPE/HEA sin soldadura ni perforaciones."),
        ("LUX-top® SBE / ASP (Postes para Hormigón)", "Anclajes estructurales con varilla roscada A4 y taco químico viniléster de alta resistencia."),
        ("LUX-top® FALZ (Cubierta de Junta Alzada)", "Fijación por pinzas de apriete a la junta alzada sin perforar la cubierta de zinc/cobre."),
        ("LUX-top® MAS HA-4 (Línea Temporal)", "Línea de vida horizontal transportable de cinta/cable para intervenciones provisionales (16 a 30 m).")
    ]

    ws3.cell(row=5, column=2, value="Modelo / Sistema LUX-TOP").font = font_header
    ws3.cell(row=5, column=2).fill = fill_header
    ws3.cell(row=5, column=2).border = border_thin
    ws3.cell(row=5, column=3, value="Descripción y Ámbito de Aplicación").font = font_header
    ws3.cell(row=5, column=3).fill = fill_header
    ws3.cell(row=5, column=3).border = border_thin

    for i, (k, v) in enumerate(models, start=6):
        ws3.cell(row=i, column=2, value=k).font = font_bold
        ws3.cell(row=i, column=2).border = border_thin
        ws3.cell(row=i, column=3, value=v).font = font_reg
        ws3.cell(row=i, column=3).border = border_thin
        ws3.cell(row=i, column=3).alignment = Alignment(wrap_text=True)
        if i % 2 == 0:
            ws3.cell(row=i, column=2).fill = fill_alt
            ws3.cell(row=i, column=3).fill = fill_alt
        ws3.row_dimensions[i].height = 20

    ws3.column_dimensions["A"].width = 3
    ws3.column_dimensions["B"].width = 34
    ws3.column_dimensions["C"].width = 75

    excel_file = os.path.join(BASE_DIR, "Presupuesto_P2026_0055_Linea_de_Vida_Sant_Lluis.xlsx")
    wb.save(excel_file)
    print(f"Excel generado en: {excel_file}")
    return excel_file

def create_html_client():
    mod1 = DATA["modalidad_1_paso_manual"]
    mod2 = DATA["modalidad_2_paso_continuo"]

    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presupuesto Oficial LUX-top® {DATA['codigo']} • Sant Lluís</title>
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
      --blue-bg: #eff6ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 9.5px;
      line-height: 1.28;
    }}
    .page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 6mm 11mm 5mm;
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
      gap: 10px;
      align-items: center;
      border-top: 4px solid var(--brand);
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
      width: 100px;
      flex: 0 0 100px;
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
      color: var(--muted);
      font-size: 9px;
    }}
    .meta {{
      text-align: right;
    }}
    .meta h2 {{
      margin: 0;
      color: var(--accent);
      font-size: 14px;
      font-weight: 800;
    }}
    .meta .ref-badge {{
      display: inline-block;
      background: var(--brand);
      color: #fff;
      font-size: 8.5px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      margin: 2px 0;
    }}
    .meta p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 8.5px;
    }}
    .hero {{
      margin-top: 5px;
      background: var(--soft);
      border-left: 3px solid var(--accent);
      padding: 4px 8px;
      border-radius: 0 4px 4px 0;
    }}
    .hero h3 {{
      margin: 0 0 1px;
      color: var(--brand);
      font-size: 11px;
      font-weight: 700;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 9px;
    }}
    .badge-luxtop {{
      display: inline-block;
      background: #0284c7;
      color: #fff;
      font-size: 8px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
      text-transform: uppercase;
      margin-left: 4px;
    }}
    .grid-meta {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-top: 5px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 4px 6px;
    }}
    .card .label {{
      display: block;
      font-size: 7.5px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      color: var(--muted);
      font-weight: 700;
      margin-bottom: 1px;
    }}
    .card .value {{
      font-size: 9px;
      font-weight: 700;
      color: var(--brand);
    }}
    h4 {{
      margin: 6px 0 3px;
      color: var(--brand);
      font-size: 9.5px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8.5px;
      margin-bottom: 5px;
    }}
    th {{
      background: var(--brand);
      color: #fff;
      padding: 3px 5px;
      font-size: 8px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      font-weight: 700;
      border: 1px solid var(--brand);
    }}
    td {{
      padding: 3px 5px;
      border: 1px solid var(--line);
      vertical-align: top;
    }}
    tr:nth-child(even) td {{
      background: var(--soft);
    }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .price-box {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      background: var(--blue-bg);
      border: 1.5px solid var(--highlight);
      border-radius: 4px;
      padding: 6px 10px;
      margin-bottom: 5px;
      align-items: center;
    }}
    .price-base {{
      text-align: left;
    }}
    .price-base .label {{
      font-size: 8px;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 700;
    }}
    .price-base .price-amount {{
      font-size: 14.5px;
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
      font-size: 8px;
      text-transform: uppercase;
      font-weight: 700;
      opacity: 0.9;
    }}
    .price-final .price-amount {{
      font-size: 16.5px;
      font-weight: 800;
      color: #fef08a;
    }}
    .opt-switch {{
      background: #fff;
      border: 1px dashed var(--highlight);
      border-radius: 4px;
      padding: 4px 8px;
      margin-bottom: 5px;
      font-size: 8px;
      color: var(--brand);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .two-col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 5px;
    }}
    .col {{
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 5px 7px;
    }}
    .col h5 {{
      margin: 0 0 2px;
      font-size: 8.5px;
      color: var(--brand);
      font-weight: 700;
      text-transform: uppercase;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    ul.compact {{
      margin: 0;
      padding-left: 12px;
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
      gap: 10px;
      margin-top: 3px;
      padding-top: 3px;
      border-top: 1px solid var(--line);
    }}
    .sign-box {{
      height: 36px;
      border: 1px dashed var(--line);
      border-radius: 4px;
      padding: 3px 5px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      font-size: 7.5px;
      color: var(--muted);
    }}
    footer {{
      border-top: 1px solid var(--line);
      padding-top: 3px;
      display: flex;
      justify-content: space-between;
      font-size: 7.5px;
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
            <h1>HAM ESTRUCTURAS METÁLICAS <span class="badge-luxtop">INSTALADOR OFICIAL LUX-TOP®</span></h1>
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
        <h3>Suministro, Instalación y Certificación de Línea de Vida Oficial LUX-top® FSE 2003 (20 ml) • Sant Lluís</h3>
        <p>Instalación completa 'llave en mano' sobre cubierta de panel sándwich mediante postes RVT 12 certificados DEKRA, remachado estanco de 36 puntos con juntas EPDM, equipo de 2 operarios en altura (13 h), plataforma PEMP y ensayo de tiro in situ con dinamómetro.</p>
      </section>

      <section class="grid-meta">
        <div class="card">
          <span class="label">Sistema Certificado</span>
          <span class="value">LUX-top® FSE 2003</span>
        </div>
        <div class="card">
          <span class="label">Cable de Seguridad</span>
          <span class="value">Inox AISI 316 Ø8 mm</span>
        </div>
        <div class="card">
          <span class="label">Soporte Cubierta</span>
          <span class="value">3 Postes RVT 12 Panel</span>
        </div>
        <div class="card">
          <span class="label">Instalación y Pruebas</span>
          <span class="value">Incluida + Ensayo Tiro</span>
        </div>
      </section>

      <h4>Desglose Oficial de Partidas • Suministro e Instalación LUX-top® FSE 2003</h4>
      <table>
        <thead>
          <tr>
            <th class="c" style="width: 22px;">Nº</th>
            <th>Concepto y Componente Homologado LUX-TOP®</th>
            <th class="c" style="width: 28px;">Ud</th>
            <th class="r" style="width: 32px;">Cant.</th>
            <th class="r" style="width: 60px;">Precio Ud</th>
            <th class="r" style="width: 70px;">Importe</th>
          </tr>
        </thead>
        <tbody>"""

    for p in mod1["partidas"]:
        html_content += f"""
          <tr>
            <td class="c bold">{p['id']}</td>
            <td><strong>{p['concepto']}</strong><br><span style="color:var(--muted); font-size:7.5px;">{p['descripcion']}</span></td>
            <td class="c">{p['unidad']}</td>
            <td class="r">{p['cantidad']:.2f}</td>
            <td class="r">{p['precio_cliente']:.2f} €</td>
            <td class="r bold">{p['subtotal']:.2f} €</td>
          </tr>"""

    html_content += f"""
        </tbody>
      </table>

      <section class="price-box">
        <div class="price-base">
          <span class="label">Base Imponible Modalidad 1 (20 ml a {mod1['totales']['precio_ml_sin_iva']:.2f} €/ml)</span>
          <div class="price-amount">{mod1['totales']['base_imponible']:.2f} €</div>
          <span style="font-size: 8px; color: var(--muted);">I.V.A. 21%: {mod1['totales']['iva_21']:.2f} € • Deducible -220,00 € si aporta PEMP</span>
        </div>
        <div class="price-final">
          <span class="label" style="color: #cbd5e1;">Importe Total Llave en Mano</span>
          <div class="price-amount">{mod1['totales']['total_con_iva']:.2f} €</div>
          <span style="font-size: 8px; color: #cbd5e1;">Impuestos incluidos (I.V.A. 21%)</span>
        </div>
      </section>

      <div class="opt-switch">
        <span><strong>MODALIDAD 2 OPCIONAL (PASO CONTINUO / AUTOMÁTICO CON CARRO RUNNER):</strong> Con pieza intermedia pasante y carro deslizante de acero inox para transitar los 20 m sin desenganchar el conector.</span>
        <span style="font-weight:800; font-size:9.5px; white-space:nowrap; margin-left:8px;">Base: {mod2['totales']['base_imponible']:.2f} € + IVA ({mod2['totales']['total_con_iva']:.2f} € Total)</span>
      </div>

      <div class="two-col">
        <div class="col">
          <h5>Protocolo Técnico de Instalación Incluido</h5>
          <ul class="compact">
            <li><strong>Montaje en altura homologado:</strong> 2 operarios especialistas con titulación oficial en trabajos en altura (RD 2177/2004) durante 1 jornada (13 h totales).</li>
            <li><strong>Fijación estanca RVT 12:</strong> 36 remaches de bulbo de 7,7 mm de alto par y 12 juntas EPDM impermeables de 130 mm (sin goteras ni perforar correas).</li>
            <li><strong>Tensado dinamométrico:</strong> Calibración exacta con indicador SKE II y precintos de seguridad.</li>
            <li><strong>Medios de elevación:</strong> Plataforma PEMP tijera/articulada para acceso seguro a cota de cubierta.</li>
          </ul>
        </div>
        <div class="col">
          <h5>Certificación Oficial, Garantía y Condiciones</h5>
          <ul class="compact">
            <li><strong>Prueba de tiro in situ:</strong> Ensayo de tracción estática con dinamómetro calibrado a 5 kN según UNE-EN 795.</li>
            <li><strong>Legalización oficial:</strong> Remachado de placa indeleble LUX-TOP y Certificado Oficial de Instalación visado en plataforma LUX-TOP para seguro y PRL.</li>
            <li><strong>Garantía:</strong> Garantía oficial de componentes LUX-TOP y 2 años de montaje HAM.</li>
            <li><strong>Forma de pago:</strong> 100% a la aceptación del presupuesto (directiva estándar HAM).</li>
          </ul>
        </div>
      </div>

      <section class="sign-section">
        <div class="sign-box">
          <span><strong>Por HAM Estructuras Metálicas (DIXIS)</strong></span>
          <span>Pablo Sebastián Sánchez Arnoletto</span>
        </div>
        <div class="sign-box">
          <span><strong>Aceptación del Cliente (Nave Sant Lluís)</strong></span>
          <span>Indicar modalidad (1 / 2) y firma de conformidad:</span>
        </div>
      </section>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • C.I.F. B57825432 • Sant Lluís, Menorca</div>
      <div>{DATA['codigo']} • Suministro, Instalación y Certificación LUX-top® FSE 2003 • Hoja 1 de 1</div>
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
    mod1 = DATA["modalidad_1_paso_manual"]
    prov = DATA["proveedor_homologado"]

    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Estudio Técnico Interno {DATA['codigo']} • LUX-TOP</title>
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
      font-size: 9.5px;
      line-height: 1.28;
    }}
    .page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 6mm 11mm 5mm;
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
      gap: 10px;
      align-items: center;
      border-top: 4px solid var(--tech-red);
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
      width: 100px;
      flex: 0 0 100px;
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
      font-size: 9px;
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
      font-size: 8.5px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      margin: 2px 0;
    }}
    .meta p {{
      margin: 1px 0;
      color: var(--muted);
      font-size: 8.5px;
    }}
    .hero {{
      margin-top: 5px;
      background: #fef2f2;
      border-left: 3px solid var(--tech-red);
      padding: 4px 8px;
      border-radius: 0 4px 4px 0;
    }}
    .hero h3 {{
      margin: 0 0 1px;
      color: var(--brand);
      font-size: 11px;
      font-weight: 700;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 8.5px;
    }}
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-top: 5px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 4px 6px;
      text-align: center;
    }}
    .kpi-label {{
      font-size: 7.5px;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 700;
      display: block;
      margin-bottom: 1px;
    }}
    .kpi-val {{
      font-size: 12.5px;
      font-weight: 800;
      color: var(--brand);
    }}
    .kpi-val.green {{ color: var(--tech-green); }}
    .kpi-val.red {{ color: var(--tech-red); }}
    h4 {{
      margin: 6px 0 3px;
      color: var(--brand);
      font-size: 9.5px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8px;
      margin-bottom: 5px;
    }}
    th {{
      background: var(--brand);
      color: #fff;
      padding: 3px 5px;
      font-size: 7.5px;
      text-transform: uppercase;
      font-weight: 700;
      border: 1px solid var(--brand);
    }}
    td {{
      padding: 3px 5px;
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
      padding: 4px 7px;
    }}
    .col h5 {{
      margin: 0 0 2px;
      font-size: 8.5px;
      color: var(--brand);
      font-weight: 700;
      text-transform: uppercase;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    ul.compact {{
      margin: 0;
      padding-left: 12px;
      font-size: 7.5px;
      color: var(--muted);
      line-height: 1.25;
    }}
    ul.compact li {{
      margin-bottom: 2px;
    }}
    footer {{
      border-top: 1px solid var(--line);
      padding-top: 3px;
      display: flex;
      justify-content: space-between;
      font-size: 7.5px;
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
            <p>ESCANDALLO INTERNO EXCLUSIVO PROVEEDOR LUX-TOP ({prov['presupuesto_referencia']})</p>
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
        <h3>Escandallo de Costes Reales de Compra Dixis con LUX-TOP y Mano de Obra de Instalación</h3>
        <p>Directiva de empresa: Dixis sólo instala LUX-TOP. Descuento oficial del 18% y pago mediante Giro comercial a 60 días. Instalación completa en cubierta: 2 oficiales x 6,5 h (13 h totales), PEMP 1 jornada y ensayo dinamométrico.</p>
      </section>

      <section class="kpi-row">
        <div class="kpi-card">
          <span class="kpi-label">Coste Material LUX-TOP</span>
          <span class="kpi-val red">{mod1['totales']['coste_material_luxtop_dixis']:.2f} €</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Coste Directo Total</span>
          <span class="kpi-val red">{mod1['totales']['coste_directo_total_dixis']:.2f} €</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Venta Base Imponible</span>
          <span class="kpi-val">{mod1['totales']['base_imponible']:.2f} €</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Margen Bruto Total</span>
          <span class="kpi-val green">{mod1['totales']['margen_euros']:.2f} € ({mod1['totales']['margen_porcentaje']:.1f}%)</span>
        </div>
      </section>

      <h4>Escandallo Detallado de Costes de Compra Dixis vs Venta Comercial</h4>
      <table>
        <thead>
          <tr>
            <th class="c" style="width: 20px;">ID</th>
            <th>Concepto de Coste / Recurso LUX-TOP</th>
            <th class="c" style="width: 25px;">Ud</th>
            <th class="r" style="width: 28px;">Cant.</th>
            <th class="r" style="width: 48px;">Tarifa Oficial</th>
            <th class="c" style="width: 32px;">Dto</th>
            <th class="r" style="width: 52px;">Coste Neto</th>
            <th class="r" style="width: 52px;">Venta PVP</th>
            <th class="r" style="width: 52px;">Margen</th>
          </tr>
        </thead>
        <tbody>"""

    for p in mod1["partidas"]:
        margen = p["subtotal"] - p["coste_dixis"]
        dto_txt = f"{int(p['descuento']*100)}%" if p['descuento'] > 0 else "-"
        html_content += f"""
          <tr>
            <td class="c bold">{p['id']}</td>
            <td><strong>{p['concepto']}</strong></td>
            <td class="c">{p['unidad']}</td>
            <td class="r">{p['cantidad']:.2f}</td>
            <td class="r">{p['tarifa_oficial']:.2f} €</td>
            <td class="c">{dto_txt}</td>
            <td class="r bold" style="color:var(--tech-red);">{p['coste_dixis']:.2f} €</td>
            <td class="r bold">{p['subtotal']:.2f} €</td>
            <td class="r bold" style="color:var(--tech-green);">{margen:.2f} €</td>
          </tr>"""

    html_content += f"""
          <tr style="background:#fef3c7; font-weight:700;">
            <td colspan="6" class="r" style="padding:4px;">TOTALES GENERALES ESCANDALLO:</td>
            <td class="r" style="color:var(--tech-red); padding:4px;">{mod1['totales']['coste_directo_total_dixis']:.2f} €</td>
            <td class="r" style="color:var(--brand); padding:4px;">{mod1['totales']['base_imponible']:.2f} €</td>
            <td class="r" style="color:var(--tech-green); padding:4px;">{mod1['totales']['margen_euros']:.2f} €</td>
          </tr>
        </tbody>
      </table>

      <div class="two-col">
        <div class="col">
          <h5>Condiciones Oficiales LUX-TOP</h5>
          <ul class="compact">
            <li><strong>Descuento comercial:</strong> 18% directo concedido a Dixis sobre tarifa oficial.</li>
            <li><strong>Forma de pago:</strong> Giro a 60 días (asegurado por CESCE), excelente apalancamiento financiero.</li>
            <li><strong>Suministro de fábrica:</strong> Fabricación en Herencia (Ciudad Real) y envío protegido.</li>
            <li><strong>Soporte técnico:</strong> Asesoramiento de replanteo y emisión de certificados DEKRA.</li>
          </ul>
        </div>
        <div class="col">
          <h5>Rendimiento y Mano de Obra en Sant Lluís</h5>
          <ul class="compact">
            <li><strong>Equipo técnico:</strong> 2 operarios certificados en altura x 6,5 h de trabajo en cubierta = 13 h totales.</li>
            <li><strong>Coste hora interna:</strong> 22,00 €/h (286,00 €) • Venta oficial: 38,00 €/h (494,00 €).</li>
            <li><strong>Logística taller Sant Lluís:</strong> Distancia mínima (<3 km) desde Circunval·lació 11.</li>
            <li><strong>Margen neto asegurado:</strong> Margen bruto de <strong>599,12 € (28,5%)</strong> cubriendo toda la operativa in situ.</li>
          </ul>
        </div>
      </div>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • HAM Menorca • Oficina Técnica</div>
      <div>{DATA['codigo']} • Escandallo Interno Exclusivo LUX-TOP • Hoja 1 de 1</div>
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
    
    print("\nTodos los documentos de P-2026-0055 han sido generados exitosamente (100% LUX-TOP).")
