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
    
    # ----------------------------------------------------
    # Hoja 1: Presupuesto Cliente
    # ----------------------------------------------------
    ws = wb.active
    ws.title = "Presupuesto Cliente"
    ws.views.sheetView[0].showGridLines = True

    # Paleta Corporativa ALUFAC
    BLUE_MAIN = "0284C7"       # Azul Alufac
    NAVY_DARK = "0F172A"       # Azul muy oscuro cabeceras
    SLATE_LIGHT = "F8FAFC"     # Fila alterna
    BORDER_COLOR = "CBD5E1"    # Gris bordes
    TOTAL_FILL = "EFF6FF"      # Azul muy claro total

    fill_header = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
    fill_sub = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")

    font_title = Font(name="Segoe UI", size=14, bold=True, color=NAVY_DARK)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=BLUE_MAIN)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=9, color="1E293B")
    font_italic = Font(name="Segoe UI", size=8.5, italic=True, color="64748B")
    font_tot = Font(name="Segoe UI", size=10, bold=True, color=NAVY_DARK)
    font_tot_big = Font(name="Segoe UI", size=11, bold=True, color=BLUE_MAIN)

    border_thin = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )
    border_total = Border(
        top=Side(style='thin', color=BLUE_MAIN),
        bottom=Side(style='double', color=BLUE_MAIN)
    )

    # Encabezado
    ws["A1"] = "ALUFAC · Carpintería de Aluminio y PVC"
    ws["A1"].font = font_title
    ws["A2"] = "Dixis Recursos y Soluciones S.L. · CIF: B57825432 · Tel: +34 669 769 541 · info@alufac.es · www.alufac.es"
    ws["A2"].font = font_italic

    ws["A4"] = "PRESUPUESTO TÉCNICO-COMERCIAL: " + DATA["expediente"]["codigo"]
    ws["A4"].font = font_sub
    ws["E4"] = "Fecha: " + DATA["expediente"]["fecha_formateada"]
    ws["E4"].font = font_italic
    ws["E4"].alignment = Alignment(horizontal="right")

    ws["A5"] = "Cliente: " + DATA["cliente"]["nombre"] + " | Ubicación: " + DATA["cliente"]["ubicacion"] + " (Instalación Conjunta)"
    ws["A5"].font = font_bold
    ws["E5"] = "Ref: " + DATA["expediente"]["referencia"]
    ws["E5"].font = font_italic
    ws["E5"].alignment = Alignment(horizontal="right")

    headers = ["Ref.", "Descripción de la Partida", "Suministro (€)", "Instalación (€)", "Subtotal Neto (€)"]
    row_idx = 7
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=row_idx, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if col_idx == 1 else ("right" if col_idx >= 3 else "left"), vertical="center")
        cell.border = border_thin

    # Elemento 1: Puerta
    row_idx += 1
    elem1 = DATA["elementos"][0]
    ws.cell(row=row_idx, column=1, value=elem1["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
    c_desc1 = ws.cell(row=row_idx, column=2, value=elem1["denominacion"] + " (" + elem1["dimensiones"] + ")\n" +
                      "• Sistema: " + elem1["sistema_ofertado"] + "\n" +
                      "• Acabado: " + elem1["color"] + "\n" +
                      "• Vidrio: " + elem1["vidrio"] + "\n" +
                      "• Herrajes: " + elem1["herrajes"] + "\n" +
                      "• Instalación: Desmontaje de cerco existente, fijación oculta inox y sellado polímero MS marino.")
    c_desc1.alignment = Alignment(wrap_text=True, vertical="top")
    
    c_sum1 = ws.cell(row=row_idx, column=3, value=elem1["precio_suministro"])
    c_sum1.number_format = '#,##0.00 "€"'
    c_sum1.alignment = Alignment(horizontal="right", vertical="top")
    
    c_inst1 = ws.cell(row=row_idx, column=4, value=elem1["precio_instalacion"])
    c_inst1.number_format = '#,##0.00 "€"'
    c_inst1.alignment = Alignment(horizontal="right", vertical="top")
    
    c_tot1 = ws.cell(row=row_idx, column=5, value=f"=C{row_idx}+D{row_idx}")
    c_tot1.number_format = '#,##0.00 "€"'
    c_tot1.font = font_bold
    c_tot1.alignment = Alignment(horizontal="right", vertical="top")

    for c in range(1, 6):
        ws.cell(row=row_idx, column=c).border = border_thin
        ws.cell(row=row_idx, column=c).font = font_reg if c != 5 else font_bold

    # Elemento 2: Ventana
    row_idx += 1
    elem2 = DATA["elementos"][1]
    ws.cell(row=row_idx, column=1, value=elem2["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
    c_desc2 = ws.cell(row=row_idx, column=2, value=elem2["denominacion"] + " (" + elem2["dimensiones"] + ")\n" +
                      "• Sistema: " + elem2["sistema_ofertado"] + "\n" +
                      "• Acabado: " + elem2["color"] + "\n" +
                      "• Vidrio: " + elem2["vidrio"] + "\n" +
                      "• Herrajes: " + elem2["herrajes"] + "\n" +
                      "• Remates e instalación: Solape curvo 50 mm clipado, desmontaje ventana previa y sellado elástico.")
    c_desc2.alignment = Alignment(wrap_text=True, vertical="top")
    
    c_sum2 = ws.cell(row=row_idx, column=3, value=elem2["precio_suministro"])
    c_sum2.number_format = '#,##0.00 "€"'
    c_sum2.alignment = Alignment(horizontal="right", vertical="top")
    
    c_inst2 = ws.cell(row=row_idx, column=4, value=elem2["precio_instalacion"])
    c_inst2.number_format = '#,##0.00 "€"'
    c_inst2.alignment = Alignment(horizontal="right", vertical="top")
    
    c_tot2 = ws.cell(row=row_idx, column=5, value=f"=C{row_idx}+D{row_idx}")
    c_tot2.number_format = '#,##0.00 "€"'
    c_tot2.font = font_bold
    c_tot2.alignment = Alignment(horizontal="right", vertical="top")

    for c in range(1, 6):
        ws.cell(row=row_idx, column=c).border = border_thin
        ws.cell(row=row_idx, column=c).font = font_reg if c != 5 else font_bold

    # Fila de Totales Suministro e Instalación
    row_idx += 2
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)
    c_sep = ws.cell(row=row_idx, column=1, value="TOTALES SUMINISTRO E INSTALACIÓN CONJUNTA:")
    c_sep.font = font_bold
    c_sep.alignment = Alignment(horizontal="right")
    
    c_sum_tot = ws.cell(row=row_idx, column=3, value=f"=C8+C9")
    c_sum_tot.number_format = '#,##0.00 "€"'
    c_sum_tot.font = font_bold
    c_sum_tot.alignment = Alignment(horizontal="right")
    
    c_inst_tot = ws.cell(row=row_idx, column=4, value=f"=D8+D9")
    c_inst_tot.number_format = '#,##0.00 "€"'
    c_inst_tot.font = font_bold
    c_inst_tot.alignment = Alignment(horizontal="right")
    
    c_subtot_tot = ws.cell(row=row_idx, column=5, value=f"=E8+E9")
    c_subtot_tot.number_format = '#,##0.00 "€"'
    c_subtot_tot.font = font_bold
    c_subtot_tot.alignment = Alignment(horizontal="right")

    for c in range(1, 6):
        ws.cell(row=row_idx, column=c).fill = fill_sub
        ws.cell(row=row_idx, column=c).border = border_thin

    # Resumen Final
    row_idx += 2
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=4)
    ws.cell(row=row_idx, column=1, value="BASE IMPONIBLE (Subtotal Neto Conjunto):").alignment = Alignment(horizontal="right")
    ws.cell(row=row_idx, column=1).font = font_tot
    c_base = ws.cell(row=row_idx, column=5, value=f"=E{row_idx-2}")
    c_base.number_format = '#,##0.00 "€"'
    c_base.font = font_tot
    c_base.alignment = Alignment(horizontal="right")
    for c in range(1, 6):
        ws.cell(row=row_idx, column=c).border = border_thin

    row_idx += 1
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=4)
    ws.cell(row=row_idx, column=1, value="I.V.A. Régimen General (21%):").alignment = Alignment(horizontal="right")
    ws.cell(row=row_idx, column=1).font = font_reg
    c_iva = ws.cell(row=row_idx, column=5, value=f"=E{row_idx-1}*0.21")
    c_iva.number_format = '#,##0.00 "€"'
    c_iva.font = font_reg
    c_iva.alignment = Alignment(horizontal="right")
    for c in range(1, 6):
        ws.cell(row=row_idx, column=c).border = border_thin

    row_idx += 1
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=4)
    ws.cell(row=row_idx, column=1, value="TOTAL PRESUPUESTO CONJUNTO (I.V.A. INCLUIDO):").alignment = Alignment(horizontal="right")
    ws.cell(row=row_idx, column=1).font = font_tot_big
    c_final = ws.cell(row=row_idx, column=5, value=f"=E{row_idx-2}+E{row_idx-1}")
    c_final.number_format = '#,##0.00 "€"'
    c_final.font = font_tot_big
    c_final.alignment = Alignment(horizontal="right")
    c_final.border = border_total
    for c in range(1, 6):
        ws.cell(row=row_idx, column=c).fill = fill_tot

    # Condiciones
    row_idx += 2
    ws.cell(row=row_idx, column=1, value="CONDICIONES Y PLAZOS:").font = font_bold
    row_idx += 1
    ws.cell(row=row_idx, column=1, value="• Modalidad: Instalación conjunta únicamente en Cala Molí, Es Mercadal.").font = font_reg
    row_idx += 1
    ws.cell(row=row_idx, column=1, value="• Plazo de fabricación: 4 a 6 semanas (lacado verde específico) | Montaje conjunto: 1 jornada de trabajo.").font = font_reg
    row_idx += 1
    ws.cell(row=row_idx, column=1, value="• Forma de pago: 100% a la aceptación del presupuesto.").font = font_reg
    row_idx += 1
    ws.cell(row=row_idx, column=1, value="• Exclusiones: No se incluye obra civil ni albañilería en caso de roturas por la extracción de aberturas antiguas, ni pintura.").font = font_reg
    row_idx += 1
    ws.cell(row=row_idx, column=1, value="• Validez de la oferta: 30 días. Incluye desmontaje de existentes, transporte a Cala Molí, montaje, sellado MS y gestión de residuos.").font = font_reg
    row_idx += 1
    ws.cell(row=row_idx, column=1, value="• Vidrio de seguridad según CTE DB-SUA en puerta. Medidas sujetas a verificación in situ antes de corte de perfiles.").font = font_reg

    # Anchos de columna
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 62
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 18

    # ----------------------------------------------------
    # Hoja 2: Escandallo Interno
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="Escandallo Interno")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "ALUFAC · Escandallo Técnico de Costes y Rentabilidad (Confidencial)"
    ws2["A1"].font = font_title
    ws2["A2"] = "Expediente: P-2026-0052 | Cliente: Steve Gubb | Obra: Cala Molí (Instalación Conjunta)"
    ws2["A2"].font = font_italic

    h2 = ["Concepto", "Detalle / Especificación", "Cantidad", "Ud.", "Coste Ud. (€)", "Subtotal (€)"]
    for col_idx, h in enumerate(h2, start=1):
        c = ws2.cell(row=4, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [3, 4] else ("right" if col_idx >= 5 else "left"))
        c.border = border_thin

    cost_items = [
        # Puerta
        ("Perfiles Puerta Cortizo", "Marco 60 mm, hoja y zócalo verde RAL 6009", 18.5, "kg", 18.00),
        ("Panel Machihembrado 20", "Machihembrado aluminio extrusionado verde", 1.2, "m²", 95.00),
        ("Vidrio Seguridad Puerta", "Doble vidrio seguridad 3+3.1/c16/4 con barrotillos", 0.4, "m²", 240.00),
        ("Herrajes Puerta", "Cerradura E35, cilindro 30x65, bisagras Hércules, manilla", 1.0, "cjto", 165.00),
        ("Mano de Obra Taller Puerta", "Corte, mecanizado cerradura, ensamblado, acristalado", 5.0, "h", 35.00),
        ("Mano de Obra Montaje Puerta", "Desmontaje, replanteo, colocación y sellado MS", 4.0, "h", 35.00),
        ("Logística y Residuos Puerta", "Portes taller-Cala Molí y punto limpio", 1.0, "pa", 42.00),
        # Ventana
        ("Perfiles Ventana Cortizo", "Marco COR 4200, hojas y solape curvo 50 mm blanco", 9.8, "kg", 15.00),
        ("Vidrio Ventana", "Doble acristalamiento 4/c20-22/4", 0.75, "m²", 65.00),
        ("Herrajes Ventana", "Multipunto E15, manilla Altair, cremona, rodamientos 200 kg", 1.0, "cjto", 82.00),
        ("Mano de Obra Taller Ventana", "Corte ingletes, ensamblado, colocación carril inox", 2.5, "h", 35.00),
        ("Mano de Obra Montaje Ventana", "Desmontaje ventana previa, solape clipado y sellado", 2.0, "h", 35.00),
        ("Logística y Selladores Ventana", "Cartuchos MS intemperie y transporte", 1.0, "pa", 34.75)
    ]

    r2 = 5
    for item in cost_items:
        ws2.cell(row=r2, column=1, value=item[0]).font = font_reg
        ws2.cell(row=r2, column=2, value=item[1]).font = font_italic
        ws2.cell(row=r2, column=3, value=item[2]).alignment = Alignment(horizontal="center")
        ws2.cell(row=r2, column=4, value=item[3]).alignment = Alignment(horizontal="center")
        c_price = ws2.cell(row=r2, column=5, value=item[4])
        c_price.number_format = '#,##0.00 "€"'
        c_price.alignment = Alignment(horizontal="right")
        c_tot = ws2.cell(row=r2, column=6, value=f"=C{r2}*E{r2}")
        c_tot.number_format = '#,##0.00 "€"'
        c_tot.alignment = Alignment(horizontal="right")
        c_tot.font = font_bold
        for c in range(1, 7):
            ws2.cell(row=r2, column=c).border = border_thin
        r2 += 1

    # Totales Internos
    ws2.merge_cells(start_row=r2, start_column=1, end_row=r2, end_column=5)
    ws2.cell(row=r2, column=1, value="Coste Directo Total Conjunto (con sinergias logísticas):").alignment = Alignment(horizontal="right")
    ws2.cell(row=r2, column=1).font = font_tot
    c_coste_tot = ws2.cell(row=r2, column=6, value=1460.00)
    c_coste_tot.number_format = '#,##0.00 "€"'
    c_coste_tot.font = font_tot
    for c in range(1, 7):
        ws2.cell(row=r2, column=c).border = border_thin
        ws2.cell(row=r2, column=c).fill = fill_sub

    r2 += 1
    ws2.merge_cells(start_row=r2, start_column=1, end_row=r2, end_column=5)
    ws2.cell(row=r2, column=1, value="Precio Venta Neto Total:").alignment = Alignment(horizontal="right")
    ws2.cell(row=r2, column=1).font = font_tot
    c_venta = ws2.cell(row=r2, column=6, value=DATA["resumen_economico"]["base_imponible"])
    c_venta.number_format = '#,##0.00 "€"'
    c_venta.font = font_tot
    for c in range(1, 7):
        ws2.cell(row=r2, column=c).border = border_thin

    r2 += 1
    ws2.merge_cells(start_row=r2, start_column=1, end_row=r2, end_column=5)
    ws2.cell(row=r2, column=1, value="Margen Bruto de Contribución (€):").alignment = Alignment(horizontal="right")
    ws2.cell(row=r2, column=1).font = font_tot_big
    c_margen = ws2.cell(row=r2, column=6, value=f"=F{r2-1}-F{r2-2}")
    c_margen.number_format = '#,##0.00 "€"'
    c_margen.font = font_tot_big
    for c in range(1, 7):
        ws2.cell(row=r2, column=c).border = border_thin

    r2 += 1
    ws2.merge_cells(start_row=r2, start_column=1, end_row=r2, end_column=5)
    ws2.cell(row=r2, column=1, value="Margen Bruto sobre Venta (%):").alignment = Alignment(horizontal="right")
    ws2.cell(row=r2, column=1).font = font_tot_big
    c_margen_pct = ws2.cell(row=r2, column=6, value=f"=F{r2-1}/F{r2-2}")
    c_margen_pct.number_format = '0.0%'
    c_margen_pct.font = font_tot_big
    for c in range(1, 7):
        ws2.cell(row=r2, column=c).border = border_thin

    ws2.column_dimensions["A"].width = 24
    ws2.column_dimensions["B"].width = 44
    ws2.column_dimensions["C"].width = 12
    ws2.column_dimensions["D"].width = 10
    ws2.column_dimensions["E"].width = 15
    ws2.column_dimensions["F"].width = 18

    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0052_Aluminio_Cala_Moli_Steve_Gubb.xlsx")
    wb.save(excel_path)
    print(f"Excel guardado correctamente en: {excel_path}")
    return excel_path

def convert_html_to_pdf():
    cliente_html = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    cliente_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    tecnico_html = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    tecnico_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Presupuesto Cliente
        page = browser.new_page()
        page.goto(f"file:///{cliente_html.replace(os.sep, '/')}")
        page.pdf(
            path=cliente_pdf,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print(f"PDF cliente guardado: {cliente_pdf}")
        page.close()

        # 2. Presupuesto Técnico
        page = browser.new_page()
        page.goto(f"file:///{tecnico_html.replace(os.sep, '/')}")
        page.pdf(
            path=tecnico_pdf,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print(f"PDF técnico guardado: {tecnico_pdf}")
        page.close()

        browser.close()

if __name__ == "__main__":
    create_excel()
    convert_html_to_pdf()
