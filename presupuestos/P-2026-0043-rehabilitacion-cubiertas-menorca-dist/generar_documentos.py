import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from playwright.sync_api import sync_playwright

def create_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "P-2026-0043 Menorca Dist"

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
    ws["A1"] = "HAM ESTRUCTURAS METÁLICAS"
    ws["A1"].font = title_font
    ws["A2"] = "PRESUPUESTO TÉCNICO Y ECONÓMICO: P-2026-0043"
    ws["A2"].font = subtitle_font

    ws["A4"] = "Cliente:"
    ws["B4"] = "Menorca Dist (Distribuciones Menorca)"
    ws["A5"] = "Ubicación:"
    ws["B5"] = "Avda. Sa Industria 67, Pol. Ind. La Trotxa, 07730 Alaior (Menorca)"
    ws["A6"] = "Fecha:"
    ws["B6"] = "26/10/2026"
    ws["A7"] = "Concepto:"
    ws["B7"] = "Rehabilitación de Cubiertas de Nave Industrial mediante Sobrecubierta Metálica y Sustitución de Lucernarios"

    for r in range(4, 8):
        ws[f"A{r}"].font = bold_font
        ws[f"B{r}"].font = regular_font

    # Resumen de Especificaciones Técnicas
    ws["A9"] = "PARÁMETROS TÉCNICOS"
    ws["A9"].font = bold_font
    ws["A9"].fill = section_fill
    ws["B9"] = "Superficie total: 4.429 m² | Chapa grecada onda 40 mm (4.303 m²) | Lucernarios policarbonato compacto (126 m²) | 4 cubiertas (exentas zonas de carga)"
    ws["B9"].font = regular_font
    ws["B9"].fill = section_fill

    # Tabla de Sectores de Cubierta
    ws["A11"] = "DESGLOSE DE SUPERFICIES POR SECTORES"
    ws["A11"].font = bold_font
    sector_headers = ["Sector", "Denominación de la Cubierta", "Tipología Constructiva", "Chapa (m²)", "Translúcido (m²)", "Total (m²)"]
    for c_idx, s_head in enumerate(sector_headers, 1):
        cell = ws.cell(row=12, column=c_idx, value=s_head)
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
            c = ws.cell(row=s_idx, column=col_i, value=s_row[col_i-1])
            c.font = regular_font
            c.border = thin_border
            if col_i in [4, 5, 6]:
                c.number_format = '#,##0.00'
                c.alignment = Alignment(horizontal="right", vertical="center")
            elif col_i == 1:
                c.alignment = Alignment(horizontal="center", vertical="center")

    # Fila de Totales de Sectores
    ws.cell(row=17, column=1, value="")
    ws.cell(row=17, column=2, value="TOTALES MEDICIÓN CUBIERTAS:").font = bold_font
    ws.cell(row=17, column=3, value="")
    c_chapa = ws.cell(row=17, column=4, value="=SUM(D13:D16)")
    c_trans = ws.cell(row=17, column=5, value="=SUM(E13:E16)")
    c_total = ws.cell(row=17, column=6, value="=SUM(F13:F16)")
    for c in [c_chapa, c_trans, c_total]:
        c.font = bold_font
        c.number_format = '#,##0.00'
        c.alignment = Alignment(horizontal="right", vertical="center")
    for col_i in range(1, 7):
        ws.cell(row=17, column=col_i).border = thin_border
        ws.cell(row=17, column=col_i).fill = section_fill

    # Tabla de partidas
    ws["A19"] = "CUADRO DE VALORACIÓN ECONÓMICA DE PARTIDAS"
    ws["A19"].font = bold_font
    headers = ["Partida", "Concepto y Descripción Técnica", "Unidad", "Cantidad", "Precio Unitario (€)", "Importe (€)"]
    start_row = 20

    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx not in [2] else "left", vertical="center")

    data = [
        ["01", "Sobrecubierta metálica con perfil omega y chapa grecada 40 mm / e=0,6 mm prelacada rojo teja o blanco, con fijación en onda alta con arandela de estanqueidad EPDM y sellado continuo de butilo en solapes", "m2", 4303.00, 28.50],
        ["02", "Desmontaje de capa exterior translúcida antigua y sustitución por placas de policarbonato compacto grecado con protección UV doble cara, caballetes de apoyo en cresta y fijación estanca EPDM", "m2", 126.00, 54.00],
        ["03", "Rematería completa en chapa plegada prelacada 0,60 mm: cumbreras troqueladas a dos aguas, coronaciones perimetrales, saltos entre faldones y cortes mecánicos en petos de oficinas", "lote", 1.00, 5850.00],
        ["04", "Transporte marítimo y terrestre a obra en Pol. Ind. La Trotxa (Alaior), medios de elevación (camión grúa pluma para acopio en cubierta) y plataformas elevadoras móviles de personal (PEMP)", "lote", 1.00, 8600.00],
        ["05", "Seguridad y salud en altura: redes anticaídas provisionales bajo lucernarios, líneas de vida de progresión, señalización, EPIs y transporte de sobrantes a gestor autorizado de Menorca", "lote", 1.00, 5400.00]
    ]

    for i, row in enumerate(data, start=start_row + 1):
        ws.cell(row=i, column=1, value=row[0]).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=i, column=2, value=row[1]).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws.cell(row=i, column=3, value=row[2]).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=i, column=4, value=row[3]).alignment = Alignment(horizontal="right", vertical="top")
        ws.cell(row=i, column=5, value=row[4]).alignment = Alignment(horizontal="right", vertical="top")
        ws.cell(row=i, column=6, value=f"=D{i}*E{i}").alignment = Alignment(horizontal="right", vertical="top")

        for col_idx in range(1, 7):
            c = ws.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if col_idx in [4]:
                c.number_format = '#,##0.00'
            elif col_idx in [5, 6]:
                c.number_format = '#,##0.00 €'

    last_data_row = start_row + len(data)

    # Totales
    r_bi = last_data_row + 2
    ws.cell(row=r_bi, column=5, value="Base Imponible:").font = bold_font
    ws.cell(row=r_bi, column=5).alignment = Alignment(horizontal="right")
    cell_bi = ws.cell(row=r_bi, column=6, value=f"=SUM(F{start_row+1}:F{last_data_row})")
    cell_bi.font = bold_font
    cell_bi.number_format = '#,##0.00 €'

    r_iva = r_bi + 1
    ws.cell(row=r_iva, column=5, value="I.V.A. (21%):").font = bold_font
    ws.cell(row=r_iva, column=5).alignment = Alignment(horizontal="right")
    cell_iva = ws.cell(row=r_iva, column=6, value=f"=F{r_bi}*0.21")
    cell_iva.font = bold_font
    cell_iva.number_format = '#,##0.00 €'

    r_tot = r_iva + 1
    ws.cell(row=r_tot, column=5, value="TOTAL PRESUPUESTO:").font = accent_total_font
    ws.cell(row=r_tot, column=5).alignment = Alignment(horizontal="right")
    ws.cell(row=r_tot, column=5).fill = subtotal_fill
    ws.cell(row=r_tot, column=5).border = double_bottom_border
    cell_tot = ws.cell(row=r_tot, column=6, value=f"=F{r_bi}+F{r_iva}")
    cell_tot.font = accent_total_font
    cell_tot.number_format = '#,##0.00 €'
    cell_tot.fill = subtotal_fill
    cell_tot.border = double_bottom_border

    # Bloque de Condiciones Comerciales
    r_cond = r_tot + 2
    ws.cell(row=r_cond, column=1, value="CONDICIONES COMERCIALES Y DE EJECUCIÓN").font = bold_font
    ws.cell(row=r_cond+1, column=1, value="• Forma de pago:").font = bold_font
    ws.cell(row=r_cond+1, column=2, value="40% a la formalización (72.256,12 € IVA incl.), 30% al inicio del montaje (54.192,09 € IVA incl.) y 30% a la finalización (54.192,09 € IVA incl.)").font = regular_font
    ws.cell(row=r_cond+2, column=1, value="• Plazo de ejecución:").font = bold_font
    ws.cell(row=r_cond+2, column=2, value="4 a 6 semanas laborables desde recepción de materiales en Menorca").font = regular_font
    ws.cell(row=r_cond+3, column=1, value="• Garantía:").font = bold_font
    ws.cell(row=r_cond+3, column=2, value="5 años en estanqueidad y recubrimiento prelacado de chapas; 2 años en montaje y fijaciones").font = regular_font
    ws.cell(row=r_cond+4, column=1, value="• Validez:").font = bold_font
    ws.cell(row=r_cond+4, column=2, value="30 días naturales desde la fecha de emisión").font = regular_font
    ws.cell(row=r_cond+5, column=1, value="• Exclusiones:").font = bold_font
    ws.cell(row=r_cond+5, column=2, value="Quedan exentas las cubiertas de las zonas de carga según indicación. No incluye refuerzos estructurales mayores si existieran vicios ocultos no visibles.").font = regular_font

    # Anchos de columna
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 68
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 14
    ws.column_dimensions['E'].width = 22
    ws.column_dimensions['F'].width = 22

    xlsx_path = os.path.join(os.path.dirname(__file__), "presupuesto.xlsx")
    wb.save(xlsx_path)
    print(f"Excel guardado exitosamente en: {xlsx_path}")

def generate_pdf():
    dir_path = os.path.dirname(__file__)
    html_path = os.path.join(dir_path, "presupuesto-cliente.html")
    pdf_path = os.path.join(dir_path, "presupuesto-cliente.pdf")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}")
        page.pdf(
            path=pdf_path,
            format="A4",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True
        )
        browser.close()
    print(f"PDF generado exitosamente en: {pdf_path}")

if __name__ == "__main__":
    create_excel()
    generate_pdf()
