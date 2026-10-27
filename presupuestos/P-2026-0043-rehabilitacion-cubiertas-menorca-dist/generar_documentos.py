import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from playwright.sync_api import sync_playwright

def create_excel():
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
    ws1["A2"] = "PRESUPUESTO TÉCNICO Y ECONÓMICO: P-2026-0043"
    ws1["A2"].font = subtitle_font

    ws1["A4"] = "Cliente:"
    ws1["B4"] = "Mar Dojan, SL (Nave Dispreu Alaior)"
    ws1["A5"] = "Ubicación:"
    ws1["B5"] = "Avda. Sa Industria 67, Pol. Ind. La Trotxa, 07730 Alaior (Menorca)"
    ws1["A6"] = "Fecha:"
    ws1["B6"] = "27/10/2026"
    ws1["A7"] = "Concepto:"
    ws1["B7"] = "Rehabilitación de Cubiertas de Nave Industrial mediante Sobrecubierta Metálica y Sustitución de Lucernarios"

    for r in range(4, 8):
        ws1[f"A{r}"].font = bold_font
        ws1[f"B{r}"].font = regular_font

    # Resumen de Especificaciones Técnicas
    ws1["A9"] = "PARÁMETROS TÉCNICOS"
    ws1["A9"].font = bold_font
    ws1["A9"].fill = section_fill
    ws1["B9"] = "Superficie total: 4.429 m² | Chapa grecada onda 40 mm (4.303 m²) | Lucernarios policarbonato compacto (126 m²) | 4 cubiertas (exentas zonas de carga)"
    ws1["B9"].font = regular_font
    ws1["B9"].fill = section_fill

    # Tabla de Sectores de Cubierta
    ws1["A11"] = "DESGLOSE DE SUPERFICIES POR SECTORES"
    ws1["A11"].font = bold_font
    sector_headers = ["Sector", "Denominación de la Cubierta", "Tipología Constructiva", "Chapa (m²)", "Translúcido (m²)", "Total (m²)"]
    for c_idx, s_head in enumerate(sector_headers, 1):
        cell = ws1.cell(row=12, column=c_idx, value=s_head)
        cell.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        cell.font = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center" if c_idx not in [2, 3] else "left", vertical="center")

    sectores_data = [
        ["1", "Cubierta a 2 aguas con zona translúcida", "Chapa grecada sobre omegas + policarbonato", 1369.0, 126.0, 1495.0],
        ["2", "Cubierta a 2 aguas Central", "Chapa grecada sobre omegas", 2430.0, 0.0, 2430.0],
        ["3", "Cubierta a 1 agua de oficinas", "Chapa grecada con adaptación y cortes en petos", 104.0, 0.0, 104.0],
        ["4", "Cubierta a 1 agua zona Sur", "Chapa grecada sobre omegas", 400.0, 0.0, 400.0]
    ]

    for s_idx, s_row in enumerate(sectores_data, start=13):
        for col_i in range(1, 7):
            c = ws1.cell(row=s_idx, column=col_i, value=s_row[col_i-1])
            c.font = regular_font
            c.border = thin_border
            if col_i in [4, 5, 6]:
                c.number_format = '#,##0.00'
                c.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i == 1:
                c.alignment = Alignment(horizontal="center", vertical="center")

    # Fila de Totales de Sectores
    ws1.cell(row=17, column=1, value="")
    ws1.cell(row=17, column=2, value="TOTALES MEDICIÓN CUBIERTAS:").font = bold_font
    ws1.cell(row=17, column=3, value="")
    c_chapa = ws1.cell(row=17, column=4, value="=SUM(D13:D16)")
    c_trans = ws1.cell(row=17, column=5, value="=SUM(E13:E16)")
    c_total = ws1.cell(row=17, column=6, value="=SUM(F13:F16)")
    for c in [c_chapa, c_trans, c_total]:
        c.font = bold_font
        c.number_format = '#,##0.00'
        c.alignment = Alignment(horizontal="right", vertical="center")
    for col_i in range(1, 7):
        ws1.cell(row=17, column=col_i).border = thin_border
        ws1.cell(row=17, column=col_i).fill = section_fill

    # Tabla de partidas
    ws1["A19"] = "CUADRO DE VALORACIÓN ECONÓMICA DE PARTIDAS"
    ws1["A19"].font = bold_font
    headers = ["Partida", "Concepto y Descripción Técnica", "Unidad", "Cantidad", "Precio Unitario (€)", "Importe (€)"]
    start_row = 20

    for col_idx, header in enumerate(headers, 1):
        cell = ws1.cell(row=start_row, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx not in [2] else "left", vertical="center")

    data = [
        ["01", "Sobrecubierta metálica con perfil omega y chapa grecada 40 mm / e=0,6 mm prelacada rojo teja o blanco, con fijación en onda alta con arandela de estanqueidad EPDM y sellado continuo de butilo en solapes", "m2", 4303.00, 55.00],
        ["02", "Desmontaje de capa exterior translúcida antigua y sustitución por placas de policarbonato compacto grecado con protección UV doble cara, caballetes de apoyo en cresta y fijación estanca EPDM", "m2", 126.00, 75.00],
        ["03", "Rematería completa en chapa plegada prelacada 0,60 mm: cumbreras troqueladas a dos aguas, coronaciones perimetrales, saltos entre faldones y cortes mecánicos en petos de oficinas", "lote", 1.00, 6850.00],
        ["04", "Transporte marítimo y terrestre a obra en Pol. Ind. La Trotxa (Alaior), medios de elevación (camión grúa pluma para acopio en cubierta) y plataformas elevadoras móviles de personal (PEMP)", "lote", 1.00, 9600.00],
        ["05", "Seguridad y salud en altura: redes anticaídas provisionales bajo lucernarios, líneas de vida de progresión, señalización, EPIs y transporte de sobrantes a gestor autorizado de Menorca", "lote", 1.00, 5800.00]
    ]

    for i, row in enumerate(data, start=start_row + 1):
        ws1.cell(row=i, column=1, value=row[0]).alignment = Alignment(horizontal="center", vertical="top")
        ws1.cell(row=i, column=2, value=row[1]).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws1.cell(row=i, column=3, value=row[2]).alignment = Alignment(horizontal="center", vertical="top")
        ws1.cell(row=i, column=4, value=row[3]).alignment = Alignment(horizontal="right", vertical="top")
        ws1.cell(row=i, column=5, value=row[4]).alignment = Alignment(horizontal="right", vertical="top")
        ws1.cell(row=i, column=6, value=f"=D{i}*E{i}").alignment = Alignment(horizontal="right", vertical="top")

        for col_idx in range(1, 7):
            c = ws1.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if col_idx in [4]:
                c.number_format = '#,##0.00'
            elif col_idx in [5, 6]:
                c.number_format = '#,##0.00 €'

    last_data_row = start_row + len(data)

    # Totales
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
    ws1.cell(row=r_cond+1, column=2, value="40% a la formalización (129.888,66 € IVA incl.), 30% al inicio del montaje (97.416,50 € IVA incl.) y 30% a la finalización (97.416,49 € IVA incl.)").font = regular_font
    ws1.cell(row=r_cond+2, column=1, value="• Plazo de ejecución:").font = bold_font
    ws1.cell(row=r_cond+2, column=2, value="4 a 6 semanas laborables desde recepción de materiales en Menorca").font = regular_font
    ws1.cell(row=r_cond+3, column=1, value="• Garantía:").font = bold_font
    ws1.cell(row=r_cond+3, column=2, value="5 años en estanqueidad y recubrimiento prelacado de chapas; 2 años en montaje y fijaciones").font = regular_font
    ws1.cell(row=r_cond+4, column=1, value="• Validez:").font = bold_font
    ws1.cell(row=r_cond+4, column=2, value="30 días naturales desde la fecha de emisión").font = regular_font
    ws1.cell(row=r_cond+5, column=1, value="• Exclusiones:").font = bold_font
    ws1.cell(row=r_cond+5, column=2, value="Quedan exentas las cubiertas de las zonas de carga según indicación. No incluye refuerzos estructurales mayores si existieran vicios ocultos no visibles.").font = regular_font

    ws1.column_dimensions['A'].width = 10
    ws1.column_dimensions['B'].width = 68
    ws1.column_dimensions['C'].width = 10
    ws1.column_dimensions['D'].width = 14
    ws1.column_dimensions['E'].width = 22
    ws1.column_dimensions['F'].width = 22

    # -------------------------------------------------------------
    # HOJA 2: ESCANDALLO INTERNO Y COSTES HAM
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Escandallo Costes HAM")

    internal_header_fill = PatternFill(start_color="1E1B4B", end_color="1E1B4B", fill_type="solid")
    internal_tag_fill = PatternFill(start_color="EF4444", end_color="EF4444", fill_type="solid")

    ws2["A1"] = "HAM ESTRUCTURAS METÁLICAS - ESTUDIO TÉCNICO INTERNO Y ESCANDALLO DE COMPRA"
    ws2["A1"].font = Font(name="Segoe UI", size=15, bold=True, color="1E1B4B")
    ws2["A2"] = "CONFIDENCIAL: NO ENTREGAR AL CLIENTE · COSTES REALES DE COMPRA Y MÁRGENES"
    ws2["A2"].font = Font(name="Segoe UI", size=10, bold=True, color="EF4444")

    # Parámetros base de cálculo de compra
    ws2["A4"] = "PARÁMETROS DE COMPRA DIRECTA HAM:"
    ws2["A4"].font = bold_font
    ws2["A5"] = "Coste compra Chapa Común:"
    ws2["B5"] = 10.00
    ws2["C5"] = "€/m²"
    ws2["A6"] = "Coste compra Omega Galvanizada:"
    ws2["B6"] = 6.00
    ws2["C6"] = "€/ml"
    ws2["A7"] = "Intereje correas nave Alaior:"
    ws2["B7"] = 1.35
    ws2["C7"] = "m (distancia entre correas)"
    ws2["A8"] = "Ratio lineal de omega necesario:"
    ws2["B8"] = "=1/B7"
    ws2["C8"] = "ml de omega por m² de faldón"
    ws2["A9"] = "Mermas y solapes acopio:"
    ws2["B9"] = 0.05
    ws2["C9"] = "5% estándar"

    for r in range(5, 10):
        ws2[f"A{r}"].font = bold_font
        ws2[f"B{r}"].font = bold_font
        ws2[f"C{r}"].font = regular_font
        if r in [5, 6]:
            ws2[f"B{r}"].number_format = '#,##0.00 €'
        elif r == 7:
            ws2[f"B{r}"].number_format = '#,##0.00'
        elif r == 8:
            ws2[f"B{r}"].number_format = '0.000'
        elif r == 9:
            ws2[f"B{r}"].number_format = '0.0%'

    # Tabla de Costes Directos
    ws2["A11"] = "DESGLOSE DE COSTES DIRECTOS DE EJECUCIÓN (CDT HAM)"
    ws2["A11"].font = bold_font

    cost_headers = ["Capítulo", "Concepto de Coste Interno", "Unidad", "Medición", "Coste Unit. HAM (€)", "Coste Total HAM (€)"]
    for c_idx, head in enumerate(cost_headers, 1):
        cell = ws2.cell(row=12, column=c_idx, value=head)
        cell.fill = internal_header_fill
        cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center" if c_idx not in [2] else "left", vertical="center")

    cost_data = [
        ["MAT-01", "Chapa grecada onda 40 mm / e=0,6 mm prelacada (4.303 m² + 5% solapes/mermas)", "m²", 4518.15, "=B5"],
        ["MAT-02", "Perfil omega galvanizado Z-275 (4.303 m² x 0,741 ml/m² + 5% solapes longitudinales)", "ml", 3350.00, "=B6"],
        ["MAT-03", "Tornillería bicromatada a correas + fijación onda alta arandela EPDM + cordón butilo", "lote", 1.00, 7500.00],
        ["MAT-04", "Placas policarbonato compacto grecado onda 40 mm (126 m² + fijaciones sobreelevadas)", "lote", 1.00, 3978.00],
        ["MAT-05", "Rematería plegada 0,60 mm (cumbreras troqueladas, coronaciones, saltos y petos)", "lote", 1.00, 2400.00],
        ["MO-01", "Mano de obra especializada montaje sobrecubierta HAM (cuadrilla oficial ~800 h)", "horas", 800.00, 28.00],
        ["LOG-01", "Fletes marítimos Península-Menorca + Camión grúa pluma descarga + Alquiler PEMP", "lote", 1.00, 8100.00],
        ["PRL-01", "Redes anticaídas bajo lucernarios + Líneas de vida temporales + Canon residuos vertedero", "lote", 1.00, 3400.00]
    ]

    for idx, c_row in enumerate(cost_data, start=13):
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
    r_cdt = 21
    ws2.cell(row=r_cdt, column=5, value="COSTE DIRECTO TOTAL (CDT):").font = bold_font
    ws2.cell(row=r_cdt, column=5).alignment = Alignment(horizontal="right")
    cell_cdt = ws2.cell(row=r_cdt, column=6, value="=SUM(F13:F20)")
    cell_cdt.font = bold_font
    cell_cdt.number_format = '#,##0.00 €'
    cell_cdt.fill = section_fill
    ws2.cell(row=r_cdt, column=5).fill = section_fill

    # Cuadro de Comparativa y Margen
    ws2["A23"] = "CUADRO DE RENTABILIDAD Y BENEFICIO COMERCIAL"
    ws2["A23"].font = bold_font

    ws2["A24"] = "Concepto Económico"
    ws2["B24"] = "Importe (€)"
    ws2["C24"] = "% sobre Venta"
    ws2["D24"] = "Observaciones"
    for col_i in range(1, 5):
        c = ws2.cell(row=24, column=col_i)
        c.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        c.font = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")

    comp_rows = [
        ["Precio de Venta al Cliente (Base Imponible):", "='Presupuesto Cliente'!F27", 1.0, "PVP ofertado a Mar Dojan, SL"],
        ["Coste Directo Total de Ejecución HAM:", "=F21", "=B26/B25", "Materiales (70%) + MO (20%) + Logística (10%)"],
        ["Margen Bruto de Explotación HAM:", "=B25-B26", "=B27/B25", "Beneficio neto industrial de la operación"]
    ]

    for c_idx, c_vals in enumerate(comp_rows, start=25):
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
            if c_idx == 27:
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

def generate_pdfs():
    dir_path = os.path.dirname(__file__)
    
    # 1. PDF Cliente
    html_cliente = os.path.join(dir_path, "presupuesto-cliente.html")
    pdf_cliente = os.path.join(dir_path, "presupuesto-cliente.pdf")

    # 2. PDF Interno Técnico
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
    generate_pdfs()
