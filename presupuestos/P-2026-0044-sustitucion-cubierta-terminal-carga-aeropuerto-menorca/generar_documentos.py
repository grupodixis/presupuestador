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
    header_optional_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    title_font = Font(name="Segoe UI", size=15, bold=True, color="0F172A")
    subtitle_font = Font(name="Segoe UI", size=11, bold=True, color="B91C1C")
    regular_font = Font(name="Segoe UI", size=9.5)
    bold_font = Font(name="Segoe UI", size=9.5, bold=True)
    accent_total_font = Font(name="Segoe UI", size=11, bold=True, color="B91C1C")
    grand_total_font = Font(name="Segoe UI", size=11.5, bold=True, color="1E3A8A")
    section_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    subtotal_fill = PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid")
    optional_subtotal_fill = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")

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
    ws1["B9"] = "Panel Sándwich Cubierta PIR 40 mm (B-s1,d0) con acabado especial anticorrosión marina Granite® HDX55 (55 µm) por AMBAS CARAS | Fijaciones bimetálicas inox A2 + EPDM | Opcionales: 2 escalas de gato inox con crinolina (+30%) + Línea de vida permanente LuxTop® (18.000 €)"
    ws1["B9"].font = regular_font
    ws1["B9"].fill = section_fill

    # Tabla de Sectores / Áreas de Cubierta
    ws1["A11"] = "DESGLOSE DE SUPERFICIES DE ACTUACIÓN"
    ws1["A11"].font = bold_font
    sector_headers = ["Zona", "Descripción del Elemento", "Tipología Constructiva", "Superficie (m²)", "Acabado de Protección", "Ambiente"]
    for c_idx, s_head in enumerate(sector_headers, 1):
        cell = ws1.cell(row=12, column=c_idx, value=s_head)
        cell.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        cell.font = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
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

    # Tabla de Partidas Base
    ws1["A18"] = "VALORACIÓN ECONÓMICA DE PARTIDAS BASE"
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

    last_base_row = start_row + len(partidas)

    # Subtotales Base
    r_bi_base = last_base_row + 1
    ws1.cell(row=r_bi_base, column=5, value="Subtotal Base Imponible (Obra Base):").font = bold_font
    ws1.cell(row=r_bi_base, column=5).alignment = Alignment(horizontal="right")
    cell_bi_base = ws1.cell(row=r_bi_base, column=6, value=f"=SUM(F{start_row+1}:F{last_base_row})")
    cell_bi_base.font = bold_font
    cell_bi_base.number_format = '#,##0.00 €'
    ws1.cell(row=r_bi_base, column=5).fill = subtotal_fill
    cell_bi_base.fill = subtotal_fill

    r_iva_base = r_bi_base + 1
    ws1.cell(row=r_iva_base, column=5, value="I.V.A. (21%) Obra Base:").font = regular_font
    ws1.cell(row=r_iva_base, column=5).alignment = Alignment(horizontal="right")
    cell_iva_base = ws1.cell(row=r_iva_base, column=6, value=f"=F{r_bi_base}*0.21")
    cell_iva_base.font = regular_font
    cell_iva_base.number_format = '#,##0.00 €'

    r_tot_base = r_iva_base + 1
    ws1.cell(row=r_tot_base, column=5, value="TOTAL OBRA BASE (IVA incl.):").font = accent_total_font
    ws1.cell(row=r_tot_base, column=5).alignment = Alignment(horizontal="right")
    cell_tot_base = ws1.cell(row=r_tot_base, column=6, value=f"=F{r_bi_base}+F{r_iva_base}")
    cell_tot_base.font = accent_total_font
    cell_tot_base.number_format = '#,##0.00 €'
    ws1.cell(row=r_tot_base, column=5).fill = subtotal_fill
    cell_tot_base.fill = subtotal_fill
    ws1.cell(row=r_tot_base, column=5).border = double_bottom_border
    cell_tot_base.border = double_bottom_border

    # -------------------------------------------------------------
    # BLOQUE DE PARTIDAS OPCIONALES (ESCALERAS INOX + LUXTOP)
    # -------------------------------------------------------------
    r_opc_title = r_tot_base + 2
    ws1.cell(row=r_opc_title, column=1, value="PARTIDAS OPCIONALES INDEPENDIENTES (ACCESOS EN ACERO INOXIDABLE Y LÍNEA DE VIDA LUXTOP)").font = bold_font

    start_opc_row = r_opc_title + 1
    for col_idx, header in enumerate(headers, 1):
        cell = ws1.cell(row=start_opc_row, column=col_idx, value=header)
        cell.fill = header_optional_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx not in [2] else "left", vertical="center")

    opcionales = data["partidasOpcionales"]
    for i, op in enumerate(opcionales, start=start_opc_row + 1):
        ws1.cell(row=i, column=1, value=op["id"]).alignment = Alignment(horizontal="center", vertical="top")
        desc_text = f"{op['concepto']}\n{op['descripcion']}"
        ws1.cell(row=i, column=2, value=desc_text).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws1.cell(row=i, column=3, value=op["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        ws1.cell(row=i, column=4, value=op["cantidad"]).alignment = Alignment(horizontal="right", vertical="top")
        ws1.cell(row=i, column=5, value=op["precioUnitario"]).alignment = Alignment(horizontal="right", vertical="top")
        ws1.cell(row=i, column=6, value=f"=D{i}*E{i}").alignment = Alignment(horizontal="right", vertical="top")

        for col_idx in range(1, 7):
            c = ws1.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if col_idx in [4]:
                c.number_format = '#,##0.00'
            elif col_idx in [5, 6]:
                c.number_format = '#,##0.00 €'

    last_opc_row = start_opc_row + len(opcionales)

    # Subtotales Opcionales
    r_bi_opc = last_opc_row + 1
    ws1.cell(row=r_bi_opc, column=5, value="Subtotal Opcionales (Base Imp.):").font = bold_font
    ws1.cell(row=r_bi_opc, column=5).alignment = Alignment(horizontal="right")
    cell_bi_opc = ws1.cell(row=r_bi_opc, column=6, value=f"=SUM(F{start_opc_row+1}:F{last_opc_row})")
    cell_bi_opc.font = bold_font
    cell_bi_opc.number_format = '#,##0.00 €'
    ws1.cell(row=r_bi_opc, column=5).fill = optional_subtotal_fill
    cell_bi_opc.fill = optional_subtotal_fill

    r_iva_opc = r_bi_opc + 1
    ws1.cell(row=r_iva_opc, column=5, value="I.V.A. (21%) Opcionales:").font = regular_font
    ws1.cell(row=r_iva_opc, column=5).alignment = Alignment(horizontal="right")
    cell_iva_opc = ws1.cell(row=r_iva_opc, column=6, value=f"=F{r_bi_opc}*0.21")
    cell_iva_opc.font = regular_font
    cell_iva_opc.number_format = '#,##0.00 €'

    r_tot_opc = r_iva_opc + 1
    ws1.cell(row=r_tot_opc, column=5, value="TOTAL OPCIONALES (IVA incl.):").font = Font(name="Segoe UI", size=10, bold=True, color="1E3A8A")
    ws1.cell(row=r_tot_opc, column=5).alignment = Alignment(horizontal="right")
    cell_tot_opc = ws1.cell(row=r_tot_opc, column=6, value=f"=F{r_bi_opc}+F{r_iva_opc}")
    cell_tot_opc.font = Font(name="Segoe UI", size=10, bold=True, color="1E3A8A")
    cell_tot_opc.number_format = '#,##0.00 €'
    ws1.cell(row=r_tot_opc, column=5).fill = optional_subtotal_fill
    cell_tot_opc.fill = optional_subtotal_fill
    ws1.cell(row=r_tot_opc, column=5).border = double_bottom_border
    cell_tot_opc.border = double_bottom_border

    # TOTAL GENERAL (BASE + OPCIONALES)
    r_grand_bi = r_tot_opc + 2
    ws1.cell(row=r_grand_bi, column=5, value="TOTAL BASE IMPONIBLE CONJUNTA:").font = grand_total_font
    ws1.cell(row=r_grand_bi, column=5).alignment = Alignment(horizontal="right")
    cell_grand_bi = ws1.cell(row=r_grand_bi, column=6, value=f"=F{r_bi_base}+F{r_bi_opc}")
    cell_grand_bi.font = grand_total_font
    cell_grand_bi.number_format = '#,##0.00 €'

    r_grand_iva = r_grand_bi + 1
    ws1.cell(row=r_grand_iva, column=5, value="I.V.A. (21%) Conjunto:").font = bold_font
    ws1.cell(row=r_grand_iva, column=5).alignment = Alignment(horizontal="right")
    cell_grand_iva = ws1.cell(row=r_grand_iva, column=6, value=f"=F{r_grand_bi}*0.21")
    cell_grand_iva.font = bold_font
    cell_grand_iva.number_format = '#,##0.00 €'

    r_grand_tot = r_grand_iva + 1
    ws1.cell(row=r_grand_tot, column=5, value="TOTAL GENERAL CONTRATO (IVA incl.):").font = Font(name="Segoe UI", size=12, bold=True, color="15803D")
    ws1.cell(row=r_grand_tot, column=5).alignment = Alignment(horizontal="right")
    cell_grand_tot = ws1.cell(row=r_grand_tot, column=6, value=f"=F{r_grand_bi}+F{r_grand_iva}")
    cell_grand_tot.font = Font(name="Segoe UI", size=12, bold=True, color="15803D")
    cell_grand_tot.number_format = '#,##0.00 €'
    ws1.cell(row=r_grand_tot, column=5).fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    cell_grand_tot.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    ws1.cell(row=r_grand_tot, column=5).border = double_bottom_border
    cell_grand_tot.border = double_bottom_border

    # Bloque de Condiciones Comerciales
    r_cond = r_grand_tot + 2
    ws1.cell(row=r_cond, column=1, value="CONDICIONES COMERCIALES Y DE EJECUCIÓN").font = bold_font
    ws1.cell(row=r_cond+1, column=1, value="• Forma de pago:").font = bold_font
    ws1.cell(row=r_cond+1, column=2, value="40% a la formalización (106.588,90 € base), 30% al acopio e inicio montaje (79.941,68 €) y 30% a la recepción final (79.941,67 €). Las partidas opcionales se facturan según aprobación.").font = regular_font
    ws1.cell(row=r_cond+2, column=1, value="• Plazo de ejecución:").font = bold_font
    ws1.cell(row=r_cond+2, column=2, value="5 a 7 semanas laborables desde recepción de paneles en Menorca").font = regular_font
    ws1.cell(row=r_cond+3, column=1, value="• Garantías:").font = bold_font
    ws1.cell(row=r_cond+3, column=2, value="10 años en recubrimiento Granite® HDX55, en acero inoxidable y en sistema LuxTop®; 5 años en estanqueidad; 2 años en montaje").font = regular_font
    ws1.cell(row=r_cond+4, column=1, value="• Validez de oferta:").font = bold_font
    ws1.cell(row=r_cond+4, column=2, value="30 días naturales desde la fecha de emisión").font = regular_font

    ws1.column_dimensions['A'].width = 10
    ws1.column_dimensions['B'].width = 72
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
    ws2["A1"].font = Font(name="Segoe UI", size=14, bold=True, color="1E1B4B")
    ws2["A2"] = "CONFIDENCIAL: USO INTERNO EXCLUSIVO · OBRA BASE + ESCALERAS INOX (+30%) + LÍNEA LUXTOP"
    ws2["A2"].font = Font(name="Segoe UI", size=9.5, bold=True, color="EF4444")

    ws2["A4"] = "PARÁMETROS DE COMPRA DIRECTA HAM:"
    ws2["A4"].font = bold_font
    ws2["A5"] = "Coste compra Panel Sándwich HDX55 2 caras (40 mm PIR):"
    ws2["B5"] = 36.00
    ws2["C5"] = "€/m² (acopio fábrica Península)"
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
        cell.font = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center" if c_idx not in [2] else "left", vertical="center")

    cost_data = [
        ["MAT-01", "Panel sándwich 40 mm PIR con acabado HDX55 en 2 caras cubiertas (1.371 m² + 5% solapes/mermas)", "m²", 1440.00, "=B5"],
        ["MAT-02", "Panel / chapa grecada acabado HDX55 en 2 caras para voladizos (533 m² + 5% mermas)", "m²", 560.00, "=B6"],
        ["MAT-03", "Tornillería bimetálica inox A2 con arandelas EPDM, accesorios fijación y masilla de butilo", "lote", 1.00, 6200.00],
        ["MAT-04", "Rematería troquelada y plegada a medida con revestimiento HDX55 (cumbreras, petos, baberos)", "lote", 1.00, 5800.00],
        ["MAT-05", "Imprimación epoxi anticorrosiva de alto contenido en sólidos para saneado viguetas voladizos", "lote", 1.00, 1450.00],
        ["MAT-06", "Materiales perfiles, peldaños y cancelas en ACERO INOXIDABLE para 2 escalas con crinolina", "lote", 1.00, 3700.00],
        ["MAT-07", "Materiales sistema línea de vida LuxTop® (cable AISI 316, postes absorbedores, tensor y carros)", "lote", 1.00, 10300.00],
        ["MO-01", "Mano de obra especializada montaje HAM obra base (cuadrilla de 4 oficiales ~800 h)", "horas", 800.00, "=B7"],
        ["MO-02", "Mano de obra taller y montaje 2 escalas inox + instalación/ensayo línea LuxTop (~100 h)", "horas", 100.00, "=B7"],
        ["LOG-01", "Fletes marítimos Península-Menorca para transporte de trailers especiales paneles gran formato", "lote", 1.00, 5200.00],
        ["LOG-02", "Camión grúa pluma autopropulsada para descarga e izado distribuido sobre pórticos", "lote", 1.00, 4600.00],
        ["LOG-03", "Alquiler de 2 plataformas elevadoras móviles de personal (PEMP) articuladas para montaje", "lote", 1.00, 3400.00],
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
    ws2.cell(row=r_cdt, column=5, value="COSTE DIRECTO TOTAL GLOBAL (CDT HAM):").font = bold_font
    ws2.cell(row=r_cdt, column=5).alignment = Alignment(horizontal="right")
    cell_cdt = ws2.cell(row=r_cdt, column=6, value=f"=SUM(F11:F{r_cdt-1})")
    cell_cdt.font = bold_font
    cell_cdt.number_format = '#,##0.00 €'
    cell_cdt.fill = section_fill
    ws2.cell(row=r_cdt, column=5).fill = section_fill

    # Cuadro de Comparativa y Rentabilidad
    r_rent = r_cdt + 2
    ws2.cell(row=r_rent, column=1, value="CUADRO DE RENTABILIDAD Y BENEFICIO COMERCIAL").font = bold_font

    headers_comp = ["Concepto Económico", "Obra Base (€)", "Opcionales (€)", "Total Global (€)", "% Margen Global"]
    for col_i, hc in enumerate(headers_comp, 1):
        c = ws2.cell(row=r_rent+1, column=col_i, value=hc)
        c.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        c.font = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")

    comp_rows = [
        ["Precio de Venta al Cliente (Base Imp.):", 220225.00, 30740.00, "=B29+C29", "100.00%"],
        ["Coste Directo Total HAM:", 125530.00, 16800.00, "=B30+C30", "=D30/D29"],
        ["Margen Bruto de Explotación HAM:", "=B29-B30", "=C29-C30", "=D29-D30", "=D31/D29"]
    ]

    for c_idx, c_vals in enumerate(comp_rows, start=r_rent+2):
        ws2.cell(row=c_idx, column=1, value=c_vals[0]).font = bold_font
        for col_j, val in enumerate(c_vals[1:], start=2):
            c_cell = ws2.cell(row=c_idx, column=col_j, value=val)
            c_cell.font = bold_font
            c_cell.alignment = Alignment(horizontal="right")
            if col_j in [2, 3, 4]:
                c_cell.number_format = '#,##0.00 €'
            elif col_j == 5:
                c_cell.number_format = '0.00%'

        for col_i in range(1, 6):
            ws2.cell(row=c_idx, column=col_i).border = thin_border
            if c_idx == r_rent+4:
                ws2.cell(row=c_idx, column=col_i).fill = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")

    ws2.column_dimensions['A'].width = 44
    ws2.column_dimensions['B'].width = 20
    ws2.column_dimensions['C'].width = 20
    ws2.column_dimensions['D'].width = 20
    ws2.column_dimensions['E'].width = 18
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
      margin: 6mm 6mm 6mm 6mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{ 
      margin: 0; 
      background: #eaedf0; 
      color: #1e262c; 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
      font-size: 10px; 
      line-height: 1.3; 
    }}
    .page-container {{
      width: 210mm;
      margin: 0 auto;
      background: #ffffff;
    }}
    .page {{ 
      padding: 7mm 9mm 6mm;
      min-height: 285mm;
      max-height: 286mm;
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
      padding: 8px 14px; 
      border-radius: 7px;
      display: grid; 
      grid-template-columns: 1fr auto; 
      gap: 12px; 
      align-items: center; 
      border-bottom: 3.5px solid #b91c1c;
      margin-bottom: 7px;
    }}
    .brand {{ display: flex; align-items: center; gap: 11px; }}
    .logo {{ width: 40px; height: 40px; border: 1px solid rgba(255,255,255,.2); border-radius: 6px; padding: 3px; background: rgba(255,255,255,0.08); }}
    h1 {{ margin: 0; font-size: 17px; font-weight: 700; letter-spacing: -.02em; color: #ffffff; }}
    .subtitle {{ margin: 2px 0 0; color: #94a3b8; font-size: 10px; font-weight: 500; }}
    .meta {{ text-align: right; color: #cbd5e1; font-size: 9px; line-height: 1.35; }}
    .meta strong {{ color: #ffffff; display: block; font-size: 12px; margin-bottom: 2px; }}

    .client-card {{
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 9px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 7px 11px;
      margin-bottom: 8px;
    }}
    .client-item h4 {{ margin: 0 0 2px; font-size: 8.8px; text-transform: uppercase; color: #64748b; letter-spacing: .05em; }}
    .client-item p {{ margin: 0; font-size: 10.5px; font-weight: 600; color: #0f172a; }}
    .client-item span {{ font-size: 9.5px; color: #475569; font-weight: normal; display: block; }}

    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-bottom: 8px;
    }}
    .kpi-card {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-left: 4px solid #b91c1c;
      border-radius: 6px;
      padding: 6px 8px;
    }}
    .kpi-title {{ font-size: 8.2px; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 1px; }}
    .kpi-val {{ font-size: 14px; font-weight: 800; color: #0f172a; line-height: 1.15; }}
    .kpi-sub {{ font-size: 8.2px; color: #475569; margin-top: 1px; }}

    h2 {{ 
      margin: 7px 0 3px; 
      font-size: 10.2px; 
      text-transform: uppercase; 
      letter-spacing: .05em; 
      color: #0f172a; 
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 2px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    h2 span {{ font-size: 8.2px; color: #64748b; text-transform: none; font-weight: normal; }}

    .solution-box {{
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 7px 9px;
      margin-bottom: 7px;
      font-size: 9.3px;
      line-height: 1.35;
      color: #334155;
    }}
    .solution-box ul {{
      margin: 3px 0 0;
      padding-left: 14px;
    }}
    .solution-box li {{
      margin-bottom: 1.5px;
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 6px;
      font-size: 9.1px;
    }}
    table.data-table th {{
      background: #1e293b;
      color: #fff;
      padding: 3.5px 5.5px;
      text-align: left;
      font-weight: 600;
      font-size: 8.8px;
    }}
    table.data-table.optional th {{
      background: #1e3a8a;
    }}
    table.data-table td {{
      padding: 3px 5.5px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: top;
    }}
    table.data-table tr:nth-child(even) {{
      background: #f8fafc;
    }}
    .td-right {{ text-align: right; white-space: nowrap; }}
    .td-center {{ text-align: center; }}
    .partida-code {{ font-weight: 700; color: #b91c1c; font-size: 8.5px; }}
    .partida-code-opc {{ font-weight: 700; color: #1e3a8a; font-size: 8.5px; }}
    .partida-title {{ font-weight: 600; color: #0f172a; margin-bottom: 1px; }}
    .partida-desc {{ font-size: 8.3px; color: #475569; line-height: 1.25; }}

    .summary-cards-container {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
      margin-top: 3px;
      margin-bottom: 6px;
    }}
    .sum-box {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 5px 8px;
      font-size: 9px;
    }}
    .sum-box.highlight {{
      background: #f0fdf4;
      border-color: #10b981;
      border-left: 4px solid #10b981;
    }}
    .sum-box.optional-box {{
      background: #eff6ff;
      border-color: #3b82f6;
      border-left: 4px solid #3b82f6;
    }}
    .sum-box h6 {{
      margin: 0 0 3px;
      text-transform: uppercase;
      font-size: 8.2px;
      color: #64748b;
      font-weight: 700;
    }}
    .sum-val {{
      font-size: 13px;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.1;
    }}
    .sum-sub {{
      font-size: 8.2px;
      color: #64748b;
      margin-top: 1.5px;
    }}

    .conditions-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-top: 3px;
    }}
    .cond-item {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 5px 7px;
      font-size: 8.8px;
    }}
    .cond-item h5 {{
      margin: 0 0 1.5px;
      color: #0f172a;
      font-size: 9px;
      font-weight: 700;
    }}
    .cond-item p {{ margin: 0; color: #475569; line-height: 1.25; }}

    .signatures {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 6px;
      padding-top: 6px;
      border-top: 1px solid #cbd5e1;
    }}
    .sign-box {{
      text-align: center;
      border: 1px dashed #cbd5e1;
      border-radius: 5px;
      padding: 6px;
      min-height: 42px;
      font-size: 8.5px;
      color: #64748b;
    }}

    footer {{ 
      border-top: 1px solid #cbd5e1; 
      padding-top: 3px; 
      display: flex; 
      justify-content: space-between; 
      font-size: 8px; 
      color: #64748b; 
    }}
    .badge-hdx {{
      background: #fee2e2;
      color: #991b1b;
      padding: 1px 4px;
      border-radius: 3px;
      font-weight: 700;
      font-size: 8.2px;
      display: inline-block;
    }}
    .badge-inox {{
      background: #dbeafe;
      color: #1e40af;
      padding: 1px 4px;
      border-radius: 3px;
      font-weight: 700;
      font-size: 8.2px;
      display: inline-block;
    }}
    .badge-luxtop {{
      background: #fef3c7;
      color: #92400e;
      padding: 1px 4px;
      border-radius: 3px;
      font-weight: 700;
      font-size: 8.2px;
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
          <div class="kpi-title">Seguridad Opcional</div>
          <div class="kpi-val">Inox + LuxTop®</div>
          <div class="kpi-sub">2 escalas crinolina + línea de vida</div>
        </div>
      </div>

      <h2>1. MEMORIA TÉCNICA Y SISTEMA PROPUESTO <span>Protección Marina Severa C5-M, Gases Aeroportuarios y Seguridad</span></h2>
      <div class="solution-box">
        Atendiendo a la solicitud formulada por <strong>UG21 Engineering</strong> para la terminal de carga del Aeropuerto de Menorca, se formula propuesta técnica de renovación integral sustituyendo el cerramiento actual fuertemente oxidado por un sistema de alta durabilidad:
        <ul>
          <li><strong>Panel Sándwich con Recubrimiento Granite® HDX55 (55 micras) en AMBAS CARAS:</strong> Resina de poliuretano termoendurecible de 55 µm modificada con poliamida sobre acero galvanizado estructural Z275. Máxima categoría de resistencia a la corrosión <strong>RC5 / C5-M (Marino Severo)</strong> y radiación UV <strong>RUV4</strong> según UNE-EN 10169. Impide el ataque por niebla salina costera y gases de combustión de turbinas de aeronaves.</li>
          <li><strong>Núcleo Aislante PIR (Poliisocianurato):</strong> Espesor 40 mm, densidad nominal 40 kg/m³, conductividad térmica reducida (λ = 0,022 W/m·K) y excelente clasificación frente al fuego <strong>B-s1,d0</strong> según UNE-EN 13501-1, libre de CFCs/HCFCs.</li>
          <li><strong>Tornillería Bimetálica Inox A2:</strong> Tornillos autotaladrantes con fuste de acero inoxidable austenítico A2 y punta cementada, arandela de estanqueidad vulcanizada EPDM de 19 mm, anulando cualquier riesgo de par galvánico y corrosión bajo cabeza.</li>
          <li><strong>Rehabilitación Integral de Voladizos (533 m²):</strong> Desmontaje de envolvente degradada, saneado mecánico con imprimación epoxi anticorrosiva C5-M de alto espesor y cobertura nueva con idéntico acabado HDX55 en dos caras y rematería con goterón frontal.</li>
          <li><strong>Escaleras de Gato con Crinolina en ACERO INOXIDABLE (Opcionales):</strong> Fabricadas conforme a <strong>UNE-EN ISO 14122-4</strong> íntegramente en acero inoxidable AISI 304/316 para acceso a voladizo y cubierta principal. Jaula dorsal a partir de 2,20-2,50 m, cancela superior batiente con muelle y portón inferior de bloqueo anti-intrusión con candado (específico AENA).</li>
          <li><strong>Línea de Vida Permanente Homologada LUXTOP® (Opcional):</strong> Sistema horizontal continuo de cable de acero inoxidable AISI 316 (Ø 8 mm) conforme a <strong>UNE-EN 795:2012 Tipo C y CEN/TS 16415</strong> para hasta 4 operarios simultáneos, postes absorbedores estancos sobre faldón y carros pasantes continuos sin desconexión.</li>
        </ul>
      </div>

      <h2>2. DESGLOSE DE SUPERFICIES DE ACTUACIÓN <span>Terminal de Carga Aeropuerto de Menorca</span></h2>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 45px;" class="td-center">Sector</th>
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
            <td class="td-right" style="color: #b91c1c; font-size: 10px;">1.904,00 m²</td>
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
            <div class="subtitle">VALORACIÓN ECONÓMICA DE PARTIDAS BASE Y OPCIONALES</div>
          </div>
        </div>
        <div class="meta">
          <strong>PRESUPUESTO {data['numeroPresupuesto']}</strong>
          Ref: {data['referencia']}<br>
          Terminal Carga AENA Menorca
        </div>
      </header>

      <h2>3. CUADRO DE VALORACIÓN ECONÓMICA DE PARTIDAS BASE <span>Obra Principal Cubiertas y Voladizos</span></h2>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 28px;" class="td-center">Nº</th>
            <th>Concepto y Resumen Descriptivo</th>
            <th style="width: 32px;" class="td-center">Ud.</th>
            <th style="width: 55px;" class="td-right">Cantidad</th>
            <th style="width: 65px;" class="td-right">P. Unitario</th>
            <th style="width: 78px;" class="td-right">Importe (€)</th>
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

      <h2>4. PARTIDAS OPCIONALES: SEGURIDAD EN ALTURA (ESCALAS INOX Y LÍNEA LUXTOP®) <span>Homologadas UNE-EN ISO 14122-4 / UNE-EN 795</span></h2>
      <table class="data-table optional">
        <thead>
          <tr>
            <th style="width: 48px;" class="td-center">Código</th>
            <th>Concepto y Elementos de Seguridad Integrados</th>
            <th style="width: 32px;" class="td-center">Ud.</th>
            <th style="width: 55px;" class="td-right">Cantidad</th>
            <th style="width: 65px;" class="td-right">P. Unitario</th>
            <th style="width: 78px;" class="td-right">Importe (€)</th>
          </tr>
        </thead>
        <tbody>
"""

    for op in data["partidasOpcionales"]:
        badge_class = "badge-luxtop" if "LUXTOP" in op['codigo'] else "badge-inox"
        badge_text = "LUXTOP® EN 795" if "LUXTOP" in op['codigo'] else "ACERO INOX"
        html_cliente += f"""          <tr>
            <td class="td-center"><span class="partida-code-opc">{op['id']}</span></td>
            <td>
              <div class="partida-title">{op['concepto']} <span class="{badge_class}">{badge_text}</span></div>
              <div class="partida-desc">{op['descripcion']}</div>
            </td>
            <td class="td-center">{op['unidad']}</td>
            <td class="td-right">{op['cantidad']:,.2f}</td>
            <td class="td-right">{op['precioUnitario']:,.2f} €</td>
            <td class="td-right"><strong>{op['importe']:,.2f} €</strong></td>
          </tr>
"""

    html_cliente += f"""        </tbody>
      </table>

      <div class="summary-cards-container">
        <div class="sum-box">
          <h6>Obra Base (Cubierta + Voladizos)</h6>
          <div class="sum-val">{data['totalesEconomicos']['baseImponibleBase']:,.2f} €</div>
          <div class="sum-sub">+ IVA 21%: {data['totalesEconomicos']['totalBaseConIva']:,.2f} €</div>
        </div>
        <div class="sum-box optional-box">
          <h6>Opcionales (2 Escalas Inox + LuxTop)</h6>
          <div class="sum-val" style="color: #1e3a8a;">+{data['totalesEconomicos']['baseImponibleOpcionales']:,.2f} €</div>
          <div class="sum-sub">+ IVA 21%: {data['totalesEconomicos']['totalOpcionalesConIva']:,.2f} €</div>
        </div>
        <div class="sum-box highlight">
          <h6>Total Conjunto (Base + Opcionales)</h6>
          <div class="sum-val" style="color: #047857;">{data['totalesEconomicos']['baseImponibleGeneral']:,.2f} €</div>
          <div class="sum-sub" style="color: #065f46; font-weight: 700;">TOTAL CON IVA: {data['totalesEconomicos']['totalGeneralConIva']:,.2f} €</div>
        </div>
      </div>

      <h2>5. CONDICIONES COMERCIALES, LOGÍSTICAS Y GARANTÍAS</h2>
      <div class="conditions-grid">
        <div class="cond-item">
          <h5>Hitos de Facturación y Pago</h5>
          <p>• <strong>40% a la formalización:</strong> {data['condicionesComerciales']['hitosPago'][0]['importe']:,.2f} € (IVA incl.) para reserva bobina HDX55 y fletes.<br>
          • <strong>30% al inicio del montaje:</strong> {data['condicionesComerciales']['hitosPago'][1]['importe']:,.2f} € (IVA incl.) a la descarga de materiales.<br>
          • <strong>30% a la recepción:</strong> {data['condicionesComerciales']['hitosPago'][2]['importe']:,.2f} € (IVA incl.). Opcionales facturados s/ aceptación.</p>
        </div>
        <div class="cond-item">
          <h5>Plazos, AENA y Garantías</h5>
          <p>• <strong>Plazo de ejecución:</strong> {data['condicionesComerciales']['plazoEjecucion']}.<br>
          • <strong>Garantías:</strong> 10 años en Granite® HDX55, inox y LuxTop®; 5 años estanqueidad; 2 años montaje.<br>
          • <strong>Seguridad:</strong> Cumplimiento estricto UNE-EN ISO 14122-4, UNE-EN 795 y normativa AENA.</p>
        </div>
      </div>

      <div class="signatures">
        <div class="sign-box">
          <strong>Por la Empresa Contratista:</strong><br>
          HAM ESTRUCTURAS METÁLICAS<br>
          (Dixis Recursos y Soluciones, SL)<br>
          <em>Dpto. Técnico y Dirección de Obra</em>
        </div>
        <div class="sign-box">
          <strong>Conforme el Cliente / Dirección Técnica:</strong><br>
          CONSULTORES DE INGENIERÍA UG21<br>
          (UTE BTG-UG21 / AENA)<br>
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
    print("presupuesto-cliente.html actualizado con éxito.")

    # 2. HTML INTERNO TÉCNICO
    html_interno = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dossier Interno Técnico {data['numeroPresupuesto']} - Costes HAM y Rentabilidad</title>
  <style>
    @page {{ 
      size: A4; 
      margin: 6mm 6mm 6mm 6mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{ 
      margin: 0; 
      background: #f1f5f9; 
      color: #0f172a; 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
      font-size: 10px; 
      line-height: 1.3; 
    }}
    .page-container {{
      width: 210mm;
      margin: 0 auto;
      background: #ffffff;
    }}
    .page {{ 
      padding: 7mm 9mm 6mm;
      min-height: 285mm;
      max-height: 286mm;
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
      padding: 8px 14px; 
      border-radius: 7px;
      display: grid; 
      grid-template-columns: 1fr auto; 
      gap: 12px; 
      align-items: center; 
      border-bottom: 3.5px solid #ef4444;
      margin-bottom: 7px;
    }}
    .brand {{ display: flex; align-items: center; gap: 11px; }}
    .logo {{ width: 40px; height: 40px; border: 1px solid rgba(255,255,255,.2); border-radius: 6px; padding: 3px; background: rgba(255,255,255,0.08); }}
    h1 {{ margin: 0; font-size: 16.5px; font-weight: 700; color: #ffffff; }}
    .confidential-tag {{ background: #ef4444; color: #fff; font-size: 8.2px; font-weight: 700; padding: 1.5px 5px; border-radius: 3px; display: inline-block; margin-top: 2px; }}
    .meta {{ text-align: right; color: #cbd5e1; font-size: 9px; }}

    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-bottom: 8px;
    }}
    .kpi-card {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-left: 4px solid #1e1b4b;
      border-radius: 6px;
      padding: 5px 8px;
    }}
    .kpi-card.green {{ border-left-color: #10b981; }}
    .kpi-title {{ font-size: 8.2px; text-transform: uppercase; color: #64748b; font-weight: 700; }}
    .kpi-val {{ font-size: 13.5px; font-weight: 800; color: #0f172a; line-height: 1.15; }}
    .kpi-sub {{ font-size: 8.2px; color: #475569; margin-top: 1px; }}

    h2 {{ 
      margin: 7px 0 3px; 
      font-size: 10.2px; 
      text-transform: uppercase; 
      letter-spacing: .05em; 
      color: #1e1b4b; 
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 2px;
    }}

    table.cost-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 7px;
      font-size: 9.1px;
    }}
    table.cost-table th {{
      background: #1e1b4b;
      color: #fff;
      padding: 4px 6px;
      text-align: left;
      font-weight: 600;
      font-size: 8.8px;
    }}
    table.cost-table td {{
      padding: 3px 6px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: top;
    }}
    .td-right {{ text-align: right; white-space: nowrap; }}
    .td-center {{ text-align: center; }}

    .margin-card {{
      background: #ecfdf5;
      border: 2px solid #10b981;
      border-radius: 6px;
      padding: 7px 11px;
      margin-top: 5px;
    }}
    .margin-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 9px;
      text-align: center;
    }}
    .margin-val {{ font-size: 14.5px; font-weight: 800; color: #047857; }}
    .margin-label {{ font-size: 8.2px; text-transform: uppercase; color: #065f46; font-weight: 700; }}

    footer {{ 
      border-top: 1px solid #cbd5e1; 
      padding-top: 3px; 
      display: flex; 
      justify-content: space-between; 
      font-size: 8px; 
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
            <h1>HAM ESTRUCTURAS METÁLICAS · ESTUDIO DE COSTES Y RENTABILIDAD</h1>
            <span class="confidential-tag">CONFIDENCIAL · OBRA BASE + ESCALERAS INOX (+30%) + LUXTOP®</span>
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
          <div class="kpi-title">Venta Obra Base</div>
          <div class="kpi-val">{data['totalesEconomicos']['baseImponibleBase']:,.2f} €</div>
          <div class="kpi-sub">115,66 €/m² cubierta y vol.</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Venta Opcionales</div>
          <div class="kpi-val">+{data['totalesEconomicos']['baseImponibleOpcionales']:,.2f} €</div>
          <div class="kpi-sub">2 escalas inox + LuxTop®</div>
        </div>
        <div class="kpi-card green">
          <div class="kpi-title">Margen Bruto Total</div>
          <div class="kpi-val">{data['escandalloCostesInternosHAM']['margenBrutoGlobal']:,.2f} €</div>
          <div class="kpi-sub">{data['escandalloCostesInternosHAM']['margenBrutoPorcentajeVentaGlobal']:.1f}% sobre PVP conjunto</div>
        </div>
        <div class="kpi-card green">
          <div class="kpi-title">Coste Directo Total</div>
          <div class="kpi-val">{data['escandalloCostesInternosHAM']['costeDirectoTotalGlobal']:,.2f} €</div>
          <div class="kpi-sub">CDT Global HAM</div>
        </div>
      </div>

      <h2>DESGLOSE DE COSTES DE COMPRA DIRECTA Y SUBCONTRATACIÓN HAM</h2>
      <table class="cost-table">
        <thead>
          <tr>
            <th style="width: 50px;" class="td-center">Capítulo</th>
            <th>Concepto de Coste Interno</th>
            <th style="width: 38px;" class="td-center">Ud.</th>
            <th style="width: 55px;" class="td-right">Medición</th>
            <th style="width: 65px;" class="td-right">Coste Unit.</th>
            <th style="width: 78px;" class="td-right">Coste Total (€)</th>
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
            <td>Tornillería bimetálica inox A2 con arandela EPDM, accesorios fijación y butilo hidro-expansivo</td>
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
          <tr style="background: #eff6ff;">
            <td class="td-center"><strong style="color: #1e40af;">MAT-06</strong></td>
            <td><strong>Materiales ACERO INOXIDABLE (AISI 304/316)</strong> para 2 escalas de gato con crinolina y cancelas</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">3.700,00 €</td>
            <td class="td-right"><strong style="color: #1e40af;">3.700,00 €</strong></td>
          </tr>
          <tr style="background: #fefce8;">
            <td class="td-center"><strong style="color: #854d0e;">MAT-07</strong></td>
            <td><strong>Materiales y accesorios homologados LUXTOP®</strong> (cable inox 316, postes absorbedores y carros)</td>
            <td class="td-center">lote</td>
            <td class="td-right">1,00</td>
            <td class="td-right">10.300,00 €</td>
            <td class="td-right"><strong style="color: #854d0e;">10.300,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>MO-01</strong></td>
            <td>Mano de obra especializada montaje HAM obra base (cuadrilla de 4 oficiales ~800 horas a 28 €/h)</td>
            <td class="td-center">horas</td>
            <td class="td-right">800,00</td>
            <td class="td-right">28,00 €</td>
            <td class="td-right"><strong>22.400,00 €</strong></td>
          </tr>
          <tr style="background: #eff6ff;">
            <td class="td-center"><strong style="color: #1e40af;">MO-02</strong></td>
            <td><strong>Mano de obra taller y montaje 2 escalas inox + montaje/ensayo LuxTop</strong> (~100 h)</td>
            <td class="td-center">horas</td>
            <td class="td-right">100,00</td>
            <td class="td-right">28,00 €</td>
            <td class="td-right"><strong style="color: #1e40af;">2.800,00 €</strong></td>
          </tr>
          <tr>
            <td class="td-center"><strong>LOG-01</strong></td>
            <td>Fletes marítimos Península-Menorca para transporte de trailers especiales paneles gran formato</td>
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
            <td>Alquiler de 2 plataformas elevadoras móviles de personal (PEMP) articuladas para montaje</td>
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
            <td colspan="5" style="text-align: right; text-transform: uppercase;">COSTE DIRECTO TOTAL GLOBAL (CDT HAM):</td>
            <td class="td-right" style="color: #1e1b4b; font-size: 10px;">{data['escandalloCostesInternosHAM']['costeDirectoTotalGlobal']:,.2f} €</td>
          </tr>
        </tbody>
      </table>

      <div class="margin-card">
        <div class="margin-grid">
          <div>
            <div class="margin-label">Venta Base (BI)</div>
            <div class="margin-val" style="color: #0f172a;">{data['totalesEconomicos']['baseImponibleBase']:,.2f} €</div>
          </div>
          <div>
            <div class="margin-label">Venta Opcionales</div>
            <div class="margin-val" style="color: #1e3a8a;">+{data['totalesEconomicos']['baseImponibleOpcionales']:,.2f} €</div>
          </div>
          <div>
            <div class="margin-label">Coste Directo Total</div>
            <div class="margin-val" style="color: #dc2626;">{data['escandalloCostesInternosHAM']['costeDirectoTotalGlobal']:,.2f} €</div>
          </div>
          <div>
            <div class="margin-label">Margen Bruto HAM</div>
            <div class="margin-val">{data['escandalloCostesInternosHAM']['margenBrutoGlobal']:,.2f} € ({data['escandalloCostesInternosHAM']['margenBrutoPorcentajeVentaGlobal']:.1f}%)</div>
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
    print("presupuesto-interno-tecnico.html actualizado con éxito.")

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
