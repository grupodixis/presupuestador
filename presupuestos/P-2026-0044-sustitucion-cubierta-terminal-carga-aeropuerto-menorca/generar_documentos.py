import os
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from playwright.sync_api import sync_playwright

def load_data():
    json_path = os.path.join(os.path.dirname(__file__), "datos.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_excel():
    data = load_data()
    wb = Workbook()

    # -------------------------------------------------------------
    # HOJA 1: PRESUPUESTO CLIENTE
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Cliente"

    # Paleta de colores corporativa técnica
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Segoe UI", size=16, bold=True, color="0F172A")
    subtitle_font = Font(name="Segoe UI", size=11, bold=True, color="B91C1C")
    regular_font = Font(name="Segoe UI", size=10)
    bold_font = Font(name="Segoe UI", size=10, bold=True)
    accent_total_font = Font(name="Segoe UI", size=12, bold=True, color="B91C1C")
    section_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    subtotal_fill = PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    double_bottom_border = Border(
        top=Side(style='thin', color='0F172A'),
        bottom=Side(style='double', color='0F172A')
    )

    # Cabecera Presupuesto
    ws1["A1"] = "HAM ESTRUCTURAS METÁLICAS"
    ws1["A1"].font = title_font
    ws1["A2"] = f"PRESUPUESTO TÉCNICO Y ECONÓMICO: {data['numeroPresupuesto']}"
    ws1["A2"].font = subtitle_font

    ws1["A4"] = "Cliente:"
    ws1["B4"] = f"{data['cliente']['empresa']} (Atn: {data['cliente']['atencion']})"
    ws1["A5"] = "Proyecto:"
    ws1["B5"] = f"{data['cliente']['proyecto']} - Promotor: {data['cliente']['promotorFinal']}"
    ws1["A6"] = "Ubicación:"
    ws1["B6"] = f"{data['cliente']['emplazamiento']}, {data['cliente']['direccion']}, {data['cliente']['codigoPostal']} {data['cliente']['poblacion']} ({data['cliente']['isla']})"
    ws1["A7"] = "Fecha:"
    ws1["B7"] = "27/10/2026"

    for r in range(4, 8):
        ws1[f"A{r}"].font = bold_font
        ws1[f"B{r}"].font = regular_font

    # Resumen de Especificaciones Técnicas
    ws1["A9"] = "SISTEMA TÉCNICO"
    ws1["A9"].font = bold_font
    ws1["A9"].fill = section_fill
    ws1["B9"] = "Panel Sándwich Cubierta PIR 40 mm (B-s1,d0) con acabado especial anticorrosión marina Granite® HDX55 (55 µm) por AMBAS CARAS | Fijaciones inoxidables bimetálicas A2 con arandela EPDM | Sellado continuo de butilo"
    ws1["B9"].font = regular_font
    ws1["B9"].fill = section_fill

    # Tabla de Sectores / Áreas de Cubierta
    ws1["A11"] = "DESGLOSE DE SUPERFICIES DE ACTUACIÓN"
    ws1["A11"].font = bold_font
    sector_headers = ["Zona", "Descripción del Elemento", "Tipología Constructiva", "Superficie (m²)", "Acabado de Protección", "Ambiente"]
    for c_idx, s_head in enumerate(sector_headers, 1):
        cell = ws1.cell(row=12, column=c_idx, value=s_head)
        cell.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        cell.font = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center" if c_idx not in [2, 3] else "left", vertical="center")

    sectores_data = [
        ["1", "Cubierta faldones principales a dos aguas", "Panel sándwich 40 mm PIR (UNE-EN 14509)", 1042.50, "Granite® HDX55 (2 caras)", "Marino C5-M / Aéreo"],
        ["2", "Cubierta faldón a un agua", "Panel sándwich 40 mm PIR adaptado a petos", 328.50, "Granite® HDX55 (2 caras)", "Marino C5-M / Aéreo"],
        ["3", "Voladizos en fachadas (muelles de carga)", "Chapa/panel grecado sobre ménsulas metálicas", 533.00, "Granite® HDX55 (2 caras) + Imprimación", "Marino C5-M / Aéreo"]
    ]

    for s_idx, s_row in enumerate(sectores_data, start=13):
        for col_i in range(1, 7):
            c = ws1.cell(row=s_idx, column=col_i, value=s_row[col_i-1])
            c.font = regular_font
            c.border = thin_border
            if col_i == 4:
                c.number_format = '#,##0.00'
                c.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i in [1, 5, 6]:
                c.alignment = Alignment(horizontal="center", vertical="center")

    # Fila Totales Sectores
    ws1.cell(row=16, column=1, value="")
    ws1.cell(row=16, column=2, value="TOTAL SUPERFICIE DE ACTUACIÓN:").font = bold_font
    ws1.cell(row=16, column=3, value="")
    c_tot_m2 = ws1.cell(row=16, column=4, value="=SUM(D13:D15)")
    c_tot_m2.font = bold_font
    c_tot_m2.number_format = '#,##0.00'
    c_tot_m2.alignment = Alignment(horizontal="right", vertical="center")
    ws1.cell(row=16, column=5, value="m² totales")
    ws1.cell(row=16, column=6, value="")
    for col_i in range(1, 7):
        ws1.cell(row=16, column=col_i).border = thin_border
        ws1.cell(row=16, column=col_i).fill = section_fill

    # Tabla de Partidas
    ws1["A18"] = "VALORACIÓN ECONÓMICA DE PARTIDAS"
    ws1["A18"].font = bold_font
    headers = ["Partida", "Concepto y Descripción Técnica", "Unidad", "Cantidad", "Precio Unitario (€)", "Importe (€)"]
    start_row = 19

    for col_idx, header in enumerate(headers, 1):
        cell = ws1.cell(row=start_row, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx not in [2] else "left", vertical="center")

    partidas = data["partidas"]
    for i, p in enumerate(partidas, start=start_row + 1):
        ws1.cell(row=i, column=1, value=p["id"]).alignment = Alignment(horizontal="center", vertical="top")
        desc_text = f"{p['concepto']}\n{p['descripcion']}"
        ws1.cell(row=i, column=2, value=desc_text).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws1.cell(row=i, column=3, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        ws1.cell(row=i, column=4, value=p["cantidad"]).alignment = Alignment(horizontal="right", vertical="top")
        ws1.cell(row=i, column=5, value=p["precioUnitario"]).alignment = Alignment(horizontal="right", vertical="top")
        ws1.cell(row=i, column=6, value=f"=D{i}*E{i}").alignment = Alignment(horizontal="right", vertical="top")

        for col_idx in range(1, 7):
            c = ws1.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if col_idx in [4]:
                c.number_format = '#,##0.00'
            elif col_idx in [5, 6]:
                c.number_format = '#,##0.00 €'

    last_data_row = start_row + len(partidas)

    # Totales Económicos
    r_bi = last_data_row + 2
    ws1.cell(row=r_bi, column=5, value="Base Imponible:").font = bold_font
    ws1.cell(row=r_bi, column=5).alignment = Alignment(horizontal="right")
    cell_bi = ws1.cell(row=r_bi, column=6, value=f"=SUM(F{start_row+1}:F{last_data_row})")
    cell_bi.font = bold_font
    cell_bi.number_format = '#,##0.00 €'

    r_iva = r_bi + 1
    ws1.cell(row=r_iva, column=5, value="I.V.A. (21%):").font = bold_font
    ws1.cell(row=r_iva, column=5).alignment = Alignment(horizontal="right")
    cell_iva = ws1.cell(row=r_iva, column=6, value=f"=F{r_bi}*0.21")
    cell_iva.font = bold_font
    cell_iva.number_format = '#,##0.00 €'

    r_tot = r_iva + 1
    ws1.cell(row=r_tot, column=5, value="TOTAL PRESUPUESTO:").font = accent_total_font
    ws1.cell(row=r_tot, column=5).alignment = Alignment(horizontal="right")
    ws1.cell(row=r_tot, column=5).fill = subtotal_fill
    ws1.cell(row=r_tot, column=5).border = double_bottom_border
    cell_tot = ws1.cell(row=r_tot, column=6, value=f"=F{r_bi}+F{r_iva}")
    cell_tot.font = accent_total_font
    cell_tot.number_format = '#,##0.00 €'
    cell_tot.fill = subtotal_fill
    cell_tot.border = double_bottom_border

    # Bloque de Condiciones Comerciales
    r_cond = r_tot + 2
    ws1.cell(row=r_cond, column=1, value="CONDICIONES COMERCIALES Y DE EJECUCIÓN").font = bold_font
    ws1.cell(row=r_cond+1, column=1, value="• Forma de pago:").font = bold_font
    ws1.cell(row=r_cond+1, column=2, value="40% a la formalización (106.588,90 € con IVA), 30% a la recepción en obra de materiales (79.941,68 € con IVA) y 30% a la recepción final conforme (79.941,67 € con IVA)").font = regular_font
    ws1.cell(row=r_cond+2, column=1, value="• Plazo de ejecución:").font = bold_font
    ws1.cell(row=r_cond+2, column=2, value="5 a 7 semanas laborables desde recepción y acopio de paneles en Menorca").font = regular_font
    ws1.cell(row=r_cond+3, column=1, value="• Garantías:").font = bold_font
    ws1.cell(row=r_cond+3, column=2, value="10 años en recubrimiento Granite® HDX55 contra corrosión marina y perforación; 5 años en estanqueidad de cubierta; 2 años en montaje y remates").font = regular_font
    ws1.cell(row=r_cond+4, column=1, value="• Validez de oferta:").font = bold_font
    ws1.cell(row=r_cond+4, column=2, value="30 días naturales desde la fecha de emisión").font = regular_font

    ws1.column_dimensions['A'].width = 10
    ws1.column_dimensions['B'].width = 70
    ws1.column_dimensions['C'].width = 10
    ws1.column_dimensions['D'].width = 14
    ws1.column_dimensions['E'].width = 22
    ws1.column_dimensions['F'].width = 22

    # -------------------------------------------------------------
    # HOJA 2: ESCANDALLO INTERNO Y COSTES HAM
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Escandallo Costes HAM")

    internal_header_fill = PatternFill(start_color="1E1B4B", end_color="1E1B4B", fill_type="solid")

    ws2["A1"] = "HAM ESTRUCTURAS METÁLICAS - ESCANDALLO DE COMPRA Y COSTES DIRECTOS INTERNOS"
    ws2["A1"].font = Font(name="Segoe UI", size=15, bold=True, color="1E1B4B")
    ws2["A2"] = "CONFIDENCIAL: USO INTERNO EXCLUSIVO · COSTES DIRECTOS Y ANÁLISIS DE RENTABILIDAD"
    ws2["A2"].font = Font(name="Segoe UI", size=10, bold=True, color="EF4444")

    ws2["A4"] = "PARÁMETROS DE COMPRA DIRECTA HAM:"
    ws2["A4"].font = bold_font
    ws2["A5"] = "Coste compra Panel Sándwich HDX55 2 caras (40 mm PIR):"
    ws2["B5"] = 36.00
    ws2["C5"] = "€/m² (acopio en fábrica Península)"
    ws2["A6"] = "Coste compra Panel/Chapa HDX55 Voladizos 2 caras:"
    ws2["B6"] = 34.00
    ws2["C6"] = "€/m²"
    ws2["A7"] = "Tarifa interna mano de obra oficial montaje:"
    ws2["B7"] = 28.00
    ws2["C7"] = "€/hora"

    for r in range(5, 8):
        ws2[f"A{r}"].font = bold_font
        ws2[f"B{r}"].font = bold_font
        ws2[f"C{r}"].font = regular_font
        ws2[f"B{r}"].number_format = '#,##0.00 €'

    # Tabla de Costes Directos
    ws2["A9"] = "DESGLOSE DE COSTES DIRECTOS DE EJECUCIÓN (CDT HAM)"
    ws2["A9"].font = bold_font

    cost_headers = ["Capítulo", "Concepto de Coste Interno", "Unidad", "Medición", "Coste Unit. HAM (€)", "Coste Total HAM (€)"]
    for c_idx, head in enumerate(cost_headers, 1):
        cell = ws2.cell(row=10, column=c_idx, value=head)
        cell.fill = internal_header_fill
        cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center" if c_idx not in [2] else "left", vertical="center")

    cost_data = [
        ["MAT-01", "Panel sándwich 40 mm PIR con acabado HDX55 en 2 caras para cubiertas (1.371 m² + 5% solapes/mermas)", "m²", 1440.00, "=B5"],
        ["MAT-02", "Panel / chapa autoportante acabado HDX55 en 2 caras para voladizos (533 m² + 5% mermas)", "m²", 560.00, "=B6"],
        ["MAT-03", "Tornillería bimetálica inox A2 con arandelas EPDM, puentes y masilla hidro-expansiva de butilo", "lote", 1.00, 6200.00],
        ["MAT-04", "Rematería troquelada y plegada a medida con revestimiento HDX55 (cumbreras, petos, baberos)", "lote", 1.00, 5800.00],
        ["MAT-05", "Imprimación epoxi anticorrosiva de alto contenido en sólidos para saneado de viguetas voladizos", "lote", 1.00, 1450.00],
        ["MO-01", "Mano de obra especializada desmontaje y montaje HAM (cuadrilla de 4 oficiales ~800 h)", "horas", 800.00, "=B7"],
        ["LOG-01", "Fletes marítimos Península-Menorca para trailers especiales con paneles de gran formato", "lote", 1.00, 5200.00],
        ["LOG-02", "Camión grúa pluma autopropulsada para descarga e izado distribuido sobre pórticos", "lote", 1.00, 4600.00],
        ["LOG-03", "Alquiler de 2 plataformas elevadoras móviles de personal (PEMP) articuladas durante montaje", "lote", 1.00, 3400.00],
        ["PRL-01", "Protecciones colectivas: redes anticaídas bajo faldones UNE-EN 1263-1 y líneas de vida EN 795", "lote", 1.00, 3800.00],
        ["PRL-02", "Canon de vertedero insular y tasas de centro de reciclaje autorizado de Menorca", "lote", 1.00, 1800.00]
    ]

    for idx, c_row in enumerate(cost_data, start=11):
        ws2.cell(row=idx, column=1, value=c_row[0]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=idx, column=2, value=c_row[1]).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws2.cell(row=idx, column=3, value=c_row[2]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=idx, column=4, value=c_row[3]).alignment = Alignment(horizontal="right", vertical="top")
        ws2.cell(row=idx, column=5, value=c_row[4]).alignment = Alignment(horizontal="right", vertical="top")
        ws2.cell(row=idx, column=6, value=f"=D{idx}*E{idx}").alignment = Alignment(horizontal="right", vertical="top")

        for col_i in range(1, 7):
            cell = ws2.cell(row=idx, column=col_i)
            cell.font = regular_font
            cell.border = thin_border
            if col_i == 4:
                cell.number_format = '#,##0.00'
            elif col_i in [5, 6]:
                cell.number_format = '#,##0.00 €'

    # Fila Coste Directo Total
    r_cdt = 11 + len(cost_data)
    ws2.cell(row=r_cdt, column=5, value="COSTE DIRECTO TOTAL (CDT HAM):").font = bold_font
    ws2.cell(row=r_cdt, column=5).alignment = Alignment(horizontal="right")
    cell_cdt = ws2.cell(row=r_cdt, column=6, value=f"=SUM(F11:F{r_cdt-1})")
    cell_cdt.font = bold_font
    cell_cdt.number_format = '#,##0.00 €'
    cell_cdt.fill = section_fill
    ws2.cell(row=r_cdt, column=5).fill = section_fill

    # Cuadro de Comparativa y Rentabilidad
    r_rent = r_cdt + 2
    ws2.cell(row=r_rent, column=1, value="CUADRO DE RENTABILIDAD Y BENEFICIO COMERCIAL").font = bold_font

    headers_comp = ["Concepto Económico", "Importe (€)", "% sobre Venta", "Observaciones"]
    for col_i, hc in enumerate(headers_comp, 1):
        c = ws2.cell(row=r_rent+1, column=col_i, value=hc)
        c.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        c.font = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")

    comp_rows = [
        ["Precio de Venta al Cliente (Base Imponible):", "='Presupuesto Cliente'!F28", 1.0, "PVP ofertado a UG21 / Aena"],
        ["Coste Directo Total de Ejecución HAM:", f"=F{r_cdt}", f"=B{r_rent+3}/B{r_rent+2}", "Materiales (67%) + MO (18%) + Logística y Medios (15%)"],
        ["Margen Bruto de Explotación HAM:", f"=B{r_rent+2}-B{r_rent+3}", f"=B{r_rent+4}/B{r_rent+2}", "Beneficio bruto de explotación de la actuación"]
    ]

    for c_idx, c_vals in enumerate(comp_rows, start=r_rent+2):
        ws2.cell(row=c_idx, column=1, value=c_vals[0]).font = bold_font
        c_imp = ws2.cell(row=c_idx, column=2, value=c_vals[1])
        c_imp.font = bold_font
        c_imp.number_format = '#,##0.00 €'
        c_imp.alignment = Alignment(horizontal="right")

        c_pct = ws2.cell(row=c_idx, column=3, value=c_vals[2])
        c_pct.font = bold_font
        c_pct.number_format = '0.00%'
        c_pct.alignment = Alignment(horizontal="right")

        ws2.cell(row=c_idx, column=4, value=c_vals[3]).font = regular_font

        for col_i in range(1, 5):
            ws2.cell(row=c_idx, column=col_i).border = thin_border
            if c_idx == r_rent+4:
                ws2.cell(row=c_idx, column=col_i).fill = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")

    ws2.column_dimensions['A'].width = 46
    ws2.column_dimensions['B'].width = 24
    ws2.column_dimensions['C'].width = 16
    ws2.column_dimensions['D'].width = 46
    ws2.column_dimensions['E'].width = 22
    ws2.column_dimensions['F'].width = 22

    xlsx_path = os.path.join(os.path.dirname(__file__), "presupuesto.xlsx")
    wb.save(xlsx_path)
    print(f"Excel guardado exitosamente con 2 hojas en: {xlsx_path}")

def generate_html_files():
    data = load_data()
    dir_path = os.path.dirname(__file__)

    # 1. HTML CLIENTE
    html_cliente = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presupuesto {data['numeroPresupuesto']}: Sustitución Cubierta Terminal de Carga - Aeropuerto de Menorca</title>
  <style>
    @page {{ 
      size: A4; 
      margin: 8mm 8mm 8mm 8mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{ 
      margin: 0; 
      background: #eaedf0; 
      color: #1e262c; 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
      font-size: 10.6px; 
      line-height: 1.35; 
    }}
    .page-container {{
      width: 210mm;
      margin: 0 auto;
      background: #ffffff;
    }}
    .page {{ 
      padding: 10mm 12mm 8mm;
      min-height: 282mm;
      max-height: 283mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      position: relative;
      box-sizing: border-box;
    }}
    .page:last-child {{
      page-break-after: avoid;
    }}

    header {{ 
      background: #0f172a; 
      color: #fff; 
      padding: 10px 16px; 
      border-radius: 8px;
      display: grid; 
      grid-template-columns: 1fr auto; 
      gap: 16px; 
      align-items: center; 
      border-bottom: 4px solid #b91c1c;
      margin-bottom: 10px;
    }}
    .brand {{ display: flex; align-items: center; gap: 14px; }}
    .logo {{ width: 44px; height: 44px; border: 1px solid rgba(255,255,255,.2); border-radius: 8px; padding: 4px; background: rgba(255,255,255,0.08); }}
    h1 {{ margin: 0; font-size: 19px; font-weight: 700; letter-spacing: -.02em; color: #ffffff; }}
    .subtitle {{ margin: 3px 0 0; color: #94a3b8; font-size: 11px; font-weight: 500; }}
    .meta {{ text-align: right; color: #cbd5e1; font-size: 10px; line-height: 1.4; }}
    .meta strong {{ color: #ffffff; display: block; font-size: 13px; margin-bottom: 2px; }}

    .client-card {{
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 12px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 9px 13px;
      margin-bottom: 12px;
    }}
    .client-item h4 {{ margin: 0 0 3px; font-size: 9.5px; text-transform: uppercase; color: #64748b; letter-spacing: .05em; }}
    .client-item p {{ margin: 0; font-size: 11px; font-weight: 600; color: #0f172a; }}
    .client-item span {{ font-size: 10px; color: #475569; font-weight: normal; display: block; }}

    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 9px;
      margin-bottom: 12px;
    }}
    .kpi-card {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-left: 4px solid #b91c1c;
      border-radius: 6px;
      padding: 7px 9px;
    }}
    .kpi-title {{ font-size: 9px; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 2px; }}
    .kpi-val {{ font-size: 15px; font-weight: 800; color: #0f172a; line-height: 1.15; }}
    .kpi-sub {{ font-size: 9px; color: #475569; margin-top: 2px; }}

    h2 {{ 
      margin: 10px 0 5px; 
      font-size: 11px; 
      text-transform: uppercase; 
      letter-spacing: .06em; 
      color: #0f172a; 
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 3px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    h2 span {{ font-size: 9px; color: #64748b; text-transform: none; font-weight: normal; }}

    .solution-box {{
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 7px;
      padding: 9px 11px;
      margin-bottom: 11px;
      font-size: 10px;
      line-height: 1.4;
      color: #334155;
    }}
    .solution-box ul {{
      margin: 4px 0 0;
      padding-left: 16px;
    }}
    .solution-box li {{
      margin-bottom: 2px;
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
      font-size: 9.8px;
    }}
    table.data-table th {{
      background: #1e293b;
      color: #fff;
      padding: 5px 7px;
      text-align: left;
      font-weight: 600;
      font-size: 9.3px;
      letter-spacing: .02em;
    }}
    table.data-table td {{
      padding: 5px 7px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: top;
    }}
    table.data-table tr:nth-child(even) {{
      background: #f8fafc;
    }}
    .td-right {{ text-align: right; white-space: nowrap; }}
    .td-center {{ text-align: center; }}
    .partida-code {{ font-weight: 700; color: #b91c1c; font-size: 9px; }}
    .partida-title {{ font-weight: 600; color: #0f172a; margin-bottom: 2px; }}
    .partida-desc {{ font-size: 9px; color: #475569; line-height: 1.35; }}

    .totales-box {{
      margin-left: auto;
      width: 250px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px 10px;
      margin-top: 4px;
      margin-bottom: 8px;
    }}
    .total-row {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 3px;
      font-size: 10px;
    }}
    .total-row.final {{
      border-top: 2px solid #0f172a;
      padding-top: 4px;
      margin-top: 4px;
      font-weight: 800;
      font-size: 12.5px;
      color: #b91c1c;
    }}

    .conditions-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 9px;
      margin-top: 6px;
    }}
    .cond-item {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 7px 9px;
      font-size: 9.5px;
    }}
    .cond-item h5 {{
      margin: 0 0 2px;
      color: #0f172a;
      font-size: 9.8px;
      font-weight: 700;
    }}
    .cond-item p {{ margin: 0; color: #475569; line-height: 1.35; }}

    .signatures {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 25px;
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid #cbd5e1;
    }}
    .sign-box {{
      text-align: center;
      border: 1px dashed #cbd5e1;
      border-radius: 6px;
      padding: 10px;
      min-height: 52px;
      font-size: 9px;
      color: #64748b;
    }}

    footer {{ 
      border-top: 1px solid #cbd5e1; 
      padding-top: 5px; 
      display: flex; 
      justify-content: space-between; 
      font-size: 8.5px; 
      color: #64748b; 
    }}
    .badge-hdx {{
      background: #fee2e2;
      color: #991b1b;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 9px;
      display: inline-block;
    }}
  </style>
</head>
<body>
<div class="page-container">

  <!-- ==================== PÁGINA 1 ==================== -->
  <div class="page">
    <div>
      <header>
        <div class="brand">
          <img src="logo-ham.svg" class="logo" alt="HAM Logo">
          <div>
            <h1>HAM ESTRUCTURAS METÁLICAS</h1>
            <div class="subtitle">DIXIS RECURSOS Y SOLUCIONES, SL · Licitaciones y Envolventes Industriales</div>
          </div>
        </div>
        <div class="meta">
          <strong>OFERTA TÉCNICA {data['numeroPresupuesto']}</strong>
          Ref: {data['referencia']}<br>
          Fecha: 27 de octubre de 2026<br>
          Validez: 30 días naturales
        </div>
      </header>

      <div class="client-card">
        <div class="client-item">
          <h4>Cliente y Proyectista</h4>
          <p>{data['cliente']['empresa']}</p>
          <span>Atn: {data['cliente']['atencion']} | Tlf: {data['cliente']['telefono']}</span>
          <span>Web: {data['cliente']['web']}</span>
        </div>
        <div class="client-item">
          <h4>Proyecto y Emplazamiento</h4>
          <p>{data['cliente']['proyecto']}</p>
          <span>Promotor: {data['cliente']['promotorFinal']}</span>
          <span>Ubicación: {data['cliente']['emplazamiento']}, {data['cliente']['poblacion']} ({data['cliente']['isla']})</span>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-title">Superficie Total</div>
          <div class="kpi-val">1.904,00 m²</div>
          <div class="kpi-sub">1.371 m² cubierta + 533 m² voladizos</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Sistema de Cubierta</div>
          <div class="kpi-val">Panel PIR 40mm</div>
          <div class="kpi-sub">3 grecas con tapajuntas (B-s1,d0)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Acabado Protección</div>
          <div class="kpi-val">Granite® HDX55</div>
          <div class="kpi-sub">55 µm en AMBAS CARAS (C5-M marino)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Fijación Estanca</div>
          <div class="kpi-val">Inox A2 + EPDM</div>
          <div class="kpi-sub">Sin par galvánico + cordón butilo</div>
        </div>
      </div>

      <h2>1. MEMORIA TÉCNICA Y JUSTIFICACIÓN DEL SISTEMA PROPUESTO <span>Protección Marina Severa C5-M y Gases Aeroportuarios</span></h2>
      <div class="solution-box">
        Atendiendo a la solicitud formulada por <strong>UG21 Engineering</strong> para la terminal de carga del Aeropuerto de Menorca, se formula propuesta técnica de renovación integral sustituyendo el cerramiento actual fuertemente oxidado por un sistema de alta durabilidad:
        <ul>
          <li><strong>Panel Sándwich con Recubrimiento Granite® HDX55 (55 micras) en AMBAS CARAS:</strong> Resina de poliuretano termoendurecible de 55 µm modificada con poliamida sobre acero galvanizado estructural Z275. Máxima categoría de resistencia a la corrosión <strong>RC5 / C5-M (Marino Severo)</strong> y radiación UV <strong>RUV4</strong> según UNE-EN 10169. Impide el ataque por niebla salina costera y gases de queroseno de turbinas de aeronaves.</li>
          <li><strong>Núcleo Aislante PIR (Poliisocianurato):</strong> Espesor 40 mm, densidad nominal 40 kg/m³, conductividad térmica reducida (λ = 0,022 W/m·K) y excelente clasificación frente al fuego <strong>B-s1,d0</strong> según UNE-EN 13501-1, libre de CFCs/HCFCs.</li>
          <li><strong>Tornillería Bimetálica Inox A2:</strong> Tornillos autotaladrantes con fuste de acero inoxidable austenítico A2 y punta de penetración cementada, provistos de arandela de estanqueidad de EPDM vulcanizado de 19 mm, anulando cualquier riesgo de par galvánico y corrosión bajo cabeza.</li>
          <li><strong>Rehabilitación Integral de Voladizos (533 m²):</strong> Desmontaje de la envolvente existente, saneado y desoxidado mecánico de viguetas en ménsula con imprimación epoxi anticorrosiva C5-M de alto espesor y colocación de nueva cobertura con idéntico acabado HDX55 en dos caras y remates perimetrales de goterón frontal.</li>
        </ul>
      </div>

      <h2>2. DESGLOSE DE SUPERFICIES DE ACTUACIÓN <span>Terminal de Carga Aeropuerto de Menorca</span></h2>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 50px;" class="td-center">Sector</th>
            <th>Denominación del Elemento</th>
            <th>Tipología Constructiva</th>
            <th class="td-right">Superficie</th>
            <th class="td-center">Acabado Dos Caras</th>
            <th class="td-center">Ambiente Normativo</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="td-center"><strong>01</strong></td>
            <td><strong>Cubierta Principal a Dos Aguas</strong></td>
            <td>Panel Sándwich PIR 40 mm con tapajuntas</td>
            <td class="td-right"><strong>1.042,50 m²</strong></td>
            <td class="td-center"><span class="badge-hdx">HDX55 / HDX55</span></td>
            <td class="td-center">Marino C5-M / AENA</td>
          </tr>
          <tr>
            <td class="td-center"><strong>02</strong></td>
            <td><strong>Cubierta Faldón a Un Agua</strong></td>
            <td>Panel Sándwich PIR 40 mm con cortes y adaptación a petos</td>
            <td class="td-right"><strong>328,50 m²</strong></td>
            <td class="td-center"><span class="badge-hdx">HDX55 / HDX55</span></td>
            <td class="td-center">Marino C5-M / AENA</td>
          </tr>
          <tr>
            <td class="td-center"><strong>03</strong></td>
            <td><strong>Voladizos de Fachadas (Muelles de Carga)</strong></td>
            <td>Chapa/panel grecado sobre ménsulas metálicas saneadas</td>
            <td class="td-right"><strong>533,00 m²</strong></td>
            <td class="td-center"><span class="badge-hdx">HDX55 / HDX55</span></td>
            <td class="td-center">Marino C5-M / AENA</td>
          </tr>
          <tr style="background: #f1f5f9; font-weight: 700;">
            <td colspan="3" style="text-align: right; text-transform: uppercase;">TOTAL SUPERFICIE DE ACTUACIÓN:</td>
            <td class="td-right" style="color: #b91c1c; font-size: 11px;">1.904,00 m²</td>
            <td colspan="2" class="td-center">100% Tratamiento Anticorrosión HDX55</td>
          </tr>
        </tbody>
      </table>
    </div>

    <footer>
      <span>HAM Estructuras Metálicas · Pol. Ind. Sant Lluís, Menorca · Tel: 971 35 20 18</span>
      <span>Página 1 de 2 · Oferta P-2026-0044</span>
    </footer>
  </div>

  <!-- ==================== PÁGINA 2 ==================== -->
  <div class="page">
    <div>
      <header>
        <div class="brand">
          <img src="logo-ham.svg" class="logo" alt="HAM Logo">
          <div>
            <h1>HAM ESTRUCTURAS METÁLICAS</h1>
            <div class="subtitle">VALORACIÓN ECONÓMICA Y CONDICIONES CONTRACTUALES</div>
          </div>
        </div>
        <div class="meta">
          <strong>PRESUPUESTO {data['numeroPresupuesto']}</strong>
          Ref: {data['referencia']}<br>
          Terminal Carga AENA Menorca
        </div>
      </header>

      <h2>3. CUADRO DE VALORACIÓN ECONÓMICA DE PARTIDAS <span>Precios unitarios con materiales, medios y montaje</span></h2>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 35px;" class="td-center">Nº</th>
            <th>Concepto y Resumen Descriptivo</th>
            <th style="width: 45px;" class="td-center">Ud.</th>
            <th style="width: 65px;" class="td-right">Cantidad</th>
            <th style="width: 80px;" class="td-right">P. Unitario</th>
            <th style="width: 90px;" class="td-right">Importe (€)</th>
          </tr>
        </thead>
        <tbody>
"""

    for p in data["partidas"]:
        html_cliente += f"""          <tr>
            <td class="td-center"><span class="partida-code">{p['id']}</span></td>
            <td>
              <div class="partida-title">{p['concepto']}</div>
              <div class="partida-desc">{p['descripcion']}</div>
            </td>
            <td class="td-center">{p['unidad']}</td>
            <td class="td-right">{p['cantidad']:,.2f}</td>
            <td class="td-right">{p['precioUnitario']:,.2f} €</td>
            <td class="td-right"><strong>{p['importe']:,.2f} €</strong></td>
          </tr>
"""

    html_cliente += f"""        </tbody>
      </table>

      <div class="totales-box">
        <div class="total-row">
          <span>Base Imponible:</span>
          <strong>{data['totalesEconomicos']['baseImponible']:,.2f} €</strong>
        </div>
        <div class="total-row">
          <span>I.V.A. (21%):</span>
          <strong>{data['totalesEconomicos']['ivaImporte']:,.2f} €</strong>
        </div>
        <div class="total-row final">
          <span>TOTAL OFERTA:</span>
          <span>{data['totalesEconomicos']['totalPresupuestoConIva']:,.2f} €</span>
        </div>
      </div>

      <h2>4. CONDICIONES COMERCIALES, LOGÍSTICAS Y GARANTÍAS</h2>
      <div class="conditions-grid">
        <div class="cond-item">
          <h5>Hitos de Facturación y Pago</h5>
          <p>• <strong>40% a la formalización:</strong> {data['condicionesComerciales']['hitosPago'][0]['importe']:,.2f} € (IVA incl.) para reserva de fabricación de bobina HDX55 y fletes.<br>
          • <strong>30% al inicio del montaje:</strong> {data['condicionesComerciales']['hitosPago'][1]['importe']:,.2f} € (IVA incl.) tras recepción de materiales en Menorca.<br>
          • <strong>30% a la finalización:</strong> {data['condicionesComerciales']['hitosPago'][2]['importe']:,.2f} € (IVA incl.) tras acta de recepción conforme.</p>
        </div>
        <div class="cond-item">
          <h5>Plazos y Ejecución</h5>
          <p>• <strong>Plazo de ejecución:</strong> {data['condicionesComerciales']['plazoEjecucion']}.<br>
          • <strong>Coordinación Aena:</strong> Trabajos planificados por sectores para compatibilizar la actividad logística y de carga de la terminal.<br>
          • <strong>Validez:</strong> {data['condicionesComerciales']['validezOferta']}.</p>
        </div>
        <div class="cond-item" style="grid-column: span 2;">
          <h5>Garantías y Prestaciones de Calidad</h5>
          <p>• <strong>10 Años de Garantía</strong> en durabilidad del revestimiento Granite® HDX55 frente a corrosión marina severa (C5-M) y perforación por óxido.<br>
          • <strong>5 Años de Garantía</strong> en estanqueidad global de la cubierta y remates frente a filtraciones de agua.<br>
          • <strong>2 Años de Garantía</strong> en montaje, fijaciones mecánicas y medios auxiliares instalados.</p>
        </div>
      </div>

      <div class="signatures">
        <div class="sign-box">
          <strong>Por la Empresa Contratista:</strong><br>
          HAM ESTRUCTURAS METÁLICAS<br>
          (Dixis Recursos y Soluciones, SL)<br><br>
          <em>Dpto. Técnico y Dirección de Obra</em>
        </div>
        <div class="sign-box">
          <strong>Conforme el Cliente / Dirección Técnica:</strong><br>
          CONSULTORES DE INGENIERÍA UG21<br>
          (UTE BTG-UG21 / AENA)<br><br>
          <em>Dña. Marina Gallego Fernández (Arquitecto)</em>
        </div>
      </div>
    </div>

    <footer>
      <span>HAM Estructuras Metálicas · Menorca · info@hamenorca.com</span>
      <span>Página 2 de 2 · Oferta P-2026-0044</span>
    </footer>
  </div>

</div>
</body>
</html>
"""

    with open(os.path.join(dir_path, "presupuesto-cliente.html"), "w", encoding="utf-8") as f:
        f.write(html_cliente)
    print("presupuesto-cliente.html creado con éxito.")

    # 2. HTML INTERNO TÉCNICO
    html_interno = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dossier Interno Técnico {data['numeroPresupuesto']} - Costes HAM y Análisis de Margen</title>
  <style>
    @page {{ 
      size: A4; 
      margin: 8mm 8mm 8mm 8mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{ 
      margin: 0; 
      background: #f1f5f9; 
      color: #0f172a; 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
      font-size: 10.6px; 
      line-height: 1.35; 
    }}
    .page-container {{
      width: 210mm;
      margin: 0 auto;
      background: #ffffff;
    }}
    .page {{ 
      padding: 10mm 12mm 8mm;
      min-height: 282mm;
      max-height: 283mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      position: relative;
      box-sizing: border-box;
    }}
    header {{ 
      background: #1e1b4b; 
      color: #fff; 
      padding: 10px 16px; 
      border-radius: 8px;
      display: grid; 
      grid-template-columns: 1fr auto; 
      gap: 16px; 
      align-items: center; 
      border-bottom: 4px solid #ef4444;
      margin-bottom: 10px;
    }}
    .brand {{ display: flex; align-items: center; gap: 14px; }}
    .logo {{ width: 44px; height: 44px; border: 1px solid rgba(255,255,255,.2); border-radius: 8px; padding: 4px; background: rgba(255,255,255,0.08); }}
    h1 {{ margin: 0; font-size: 18px; font-weight: 700; color: #ffffff; }}
    .confidential-tag {{ background: #ef4444; color: #fff; font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 4px; display: inline-block; margin-top: 3px; }}
    .meta {{ text-align: right; color: #cbd5e1; font-size: 10px; }}

    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 9px;
      margin-bottom: 12px;
    }}
    .kpi-card {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-left: 4px solid #1e1b4b;
      border-radius: 6px;
      padding: 7px 9px;
    }}
    .kpi-card.green {{ border-left-color: #10b981; }}
    .kpi-title {{ font-size: 9px; text-transform: uppercase; color: #64748b; font-weight: 700; }}
    .kpi-val {{ font-size: 15px; font-weight: 800; color: #0f172a; line-height: 1.15; }}
    .kpi-sub {{ font-size: 9px; color: #475569; margin-top: 2px; }}

    h2 {{ 
      margin: 10px 0 5px; 
      font-size: 11px; 
      text-transform: uppercase; 
      letter-spacing: .06em; 
      color: #1e1b4b; 
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 3px;
    }}

    table.cost-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
      font-size: 9.8px;
    }}
    table.cost-table th {{
      background: #1e1b4b;
      color: #fff;
      padding: 5px 7px;
      text-align: left;
      font-weight: 600;
      font-size: 9.3px;
    }}
    table.cost-table td {{
      padding: 5px 7px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: top;
    }}
    .td-right {{ text-align: right; white-space: nowrap; }}
    .td-center {{ text-align: center; }}

    .margin-card {{
      background: #ecfdf5;
      border: 2px solid #10b981;
      border-radius: 8px;
      padding: 10px 14px;
      margin-top: 8px;
    }}
    .margin-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      text-align: center;
    }}
    .margin-val {{ font-size: 18px; font-weight: 800; color: #047857; }}
    .margin-label {{ font-size: 9px; text-transform: uppercase; color: #065f46; font-weight: 700; }}

    footer {{ 
      border-top: 1px solid #cbd5e1; 
      padding-top: 5px; 
      display: flex; 
      justify-content: space-between; 
      font-size: 8.5px; 
      color: #64748b; 
    }}
  </style>
</head>
<body>
<div class="page-container">
  <div class="page">
    <div>
      <header>
        <div class="brand">
          <img src="logo-ham.svg" class="logo" alt="HAM Logo">
          <div>
            <h1>HAM ESTRUCTURAS METÁLICAS · ESTUDIO DE COSTES INTERNOS</h1>
            <span class="confidential-tag">ESTRICTAMENTE CONFIDENCIAL · NO ENTREGAR AL CLIENTE</span>
          </div>
        </div>
        <div class="meta">
          <strong>EXPEDIENTE {data['numeroPresupuesto']}</strong><br>
          Ref: {data['referencia']}<br>
          Fecha: 27/10/2026
        </div>
      </header>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-title">PVP Venta (Base Imp.)</div>
          <div class="kpi-val">{data['totalesEconomicos']['baseImponible']:,.2f} €</div>
          <div class="kpi-sub">115,66 €/m² global obra</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Coste Directo Total</div>
          <div class="kpi-val">{data['escandalloCostesInternosHAM']['costeDirectoTotalCDT']:,.2f} €</div>
          <div class="kpi-sub">65,93 €/m² coste real HAM</div>
        </div>
        <div class="kpi-card green">
          <div class="kpi-title">Margen Bruto (€)</div>
          <div class="kpi-val">{data['escandalloCostesInternosHAM']['margenBrutoEuros']:,.2f} €</div>
          <div class="kpi-sub">+49,73 €/m² neto explotación</div>
        </div>
        <div class="kpi-card green">
          <div class="kpi-title">Margen sobre Venta</div>
          <div class="kpi-val">{data['escandalloCostesInternosHAM']['margenBrutoPorcentajeVenta']:.1f} %</div>
          <div class="kpi-sub">{data['escandalloCostesInternosHAM']['margenBrutoPorcentajeCoste']:.1f} % sobre coste directo</div>
        </div>
      </div>

      <h2>DESGLOSE DE COSTES DE COMPRA DIRECTA Y SUBCONTRATACIÓN HAM</h2>
      <table class="cost-table">
        <thead>
          <tr>
            <th style="width: 60px;" class="td-center">Capítulo</th>
            <th>Concepto de Coste Interno</th>
            <th style="width: 45px;" class="td-center">Ud.</th>
            <th style="width: 65px;" class="td-right">Medición</th>
            <th style="width: 75px;" class="td-right">Coste Unit.</th>
            <th style="width: 85px;" class="td-right">Coste Total (€)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="td-center"><strong>MAT-01</strong></td>
            <td>Panel sándwich 40 mm PIR con acabado HDX55 en 2 caras cubiertas (1.371 m² + 5% solapes/mermas)</td>
            <td class="td-center">m²</td>
            <td class="td-right">1.440,00</td>
            <td class="td-right">36,00 €</td>
            <td class="td-right"><strong>51.840,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>MAT-02</strong></td>
            <td>Panel / chapa grecada acabado HDX55 en 2 caras para voladizos (533 m² + 5% mermas)</td>
            <td class="td-center">m²</td>
            <td class="td-right">560,00</td>
            <td class="td-right">34,00 €</td>
            <td class="td-right"><strong>19.040,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>MAT-03</strong></td>
            <td>Tornillería bimetálica inox A2 con arandela EPDM, accesorios fijación y masilla hidro-expansiva butilo</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">6.200,00 €</td>
            <td class="td-right"><strong>6.200,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>MAT-04</strong></td>
            <td>Rematería troquelada y plegada en chapa HDX55 (cumbreras, coronaciones, baberos y goterones)</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">5.800,00 €</td>
            <td class="td-right"><strong>5.800,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>MAT-05</strong></td>
            <td>Imprimación epoxi anticorrosiva de alto contenido en sólidos para saneado viguetas voladizos</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">1.450,00 €</td>
            <td class="td-right"><strong>1.450,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>MO-01</strong></td>
            <td>Mano de obra especializada montaje HAM (cuadrilla oficial de 4 montadores ~800 horas a 28 €/h)</td>
            <td class="td-center">horas</td>
            <td class="td-right">800,00</td>
            <td class="td-right">28,00 €</td>
            <td class="td-right"><strong>22.400,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>LOG-01</strong></td>
            <td>Fletes marítimos Península-Menorca para transporte de trailers especiales de paneles de gran longitud</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">5.200,00 €</td>
            <td class="td-right"><strong>5.200,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>LOG-02</strong></td>
            <td>Camión grúa pluma autopropulsada para descarga e izado distribuido sobre pórticos en aeropuerto</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">4.600,00 €</td>
            <td class="td-right"><strong>4.600,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>LOG-03</strong></td>
            <td>Alquiler de 2 plataformas elevadoras móviles de personal (PEMP) articuladas para cubierta y voladizos</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">3.400,00 €</td>
            <td class="td-right"><strong>3.400,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>PRL-01</strong></td>
            <td>Protecciones colectivas: redes anticaídas bajo faldones UNE-EN 1263-1 y líneas de vida EN 795</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">3.800,00 €</td>
            <td class="td-right"><strong>3.800,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>PRL-02</strong></td>
            <td>Tasas de centro de reciclaje y canon vertedero insular de Menorca</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">1.800,00 €</td>
            <td class="td-right"><strong>1.800,00 €</strong></td>
          </tr>
          <tr style="background: #f1f5f9; font-weight: 700;">
            <td colspan="5" style="text-align: right; text-transform: uppercase;">COSTE DIRECTO TOTAL (CDT HAM):</td>
            <td class="td-right" style="color: #1e1b4b; font-size: 11px;">{data['escandalloCostesInternosHAM']['costeDirectoTotalCDT']:,.2f} €</td>
          </tr>
        </tbody>
      </table>

      <div class="margin-card">
        <div class="margin-grid">
          <div>
            <div class="margin-label">Venta al Cliente (BI)</div>
            <div class="margin-val" style="color: #0f172a;">{data['totalesEconomicos']['baseImponible']:,.2f} €</div>
          </div>
          <div>
            <div class="margin-label">Coste Directo Ejecución</div>
            <div class="margin-val" style="color: #dc2626;">{data['escandalloCostesInternosHAM']['costeDirectoTotalCDT']:,.2f} €</div>
          </div>
          <div>
            <div class="margin-label">Margen Bruto HAM</div>
            <div class="margin-val">{data['escandalloCostesInternosHAM']['margenBrutoEuros']:,.2f} € ({data['escandalloCostesInternosHAM']['margenBrutoPorcentajeVenta']:.1f}%)</div>
          </div>
        </div>
      </div>
    </div>

    <footer>
      <span>HAM Estructuras Metálicas · Control de Gestión y Costes</span>
      <span>Dossier Técnico Interno Confidencial · P-2026-0044</span>
    </footer>
  </div>
</div>
</body>
</html>
"""

    with open(os.path.join(dir_path, "presupuesto-interno-tecnico.html"), "w", encoding="utf-8") as f:
        f.write(html_interno)
    print("presupuesto-interno-tecnico.html creado con éxito.")

def generate_pdfs():
    dir_path = os.path.dirname(__file__)
    
    html_cliente = os.path.join(dir_path, "presupuesto-cliente.html")
    pdf_cliente = os.path.join(dir_path, "presupuesto-cliente.pdf")

    html_interno = os.path.join(dir_path, "presupuesto-interno-tecnico.html")
    pdf_interno = os.path.join(dir_path, "presupuesto-interno-tecnico.pdf")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Generar Cliente
        page1 = browser.new_page()
        page1.goto(f"file:///{os.path.abspath(html_cliente).replace(os.sep, '/')}")
        page1.pdf(
            path=pdf_cliente,
            format="A4",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True
        )
        print(f"PDF Cliente generado exitosamente en: {pdf_cliente}")

        # Generar Interno
        page2 = browser.new_page()
        page2.goto(f"file:///{os.path.abspath(html_interno).replace(os.sep, '/')}")
        page2.pdf(
            path=pdf_interno,
            format="A4",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True
        )
        print(f"PDF Interno generado exitosamente en: {pdf_interno}")

        browser.close()

if __name__ == "__main__":
    create_excel()
    generate_html_files()
    generate_pdfs()
