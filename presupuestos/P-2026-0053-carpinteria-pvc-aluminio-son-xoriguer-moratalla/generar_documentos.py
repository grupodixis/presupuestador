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
    
    # Colores corporativos ALUFAC
    BLUE_MAIN = "0284C7"
    NAVY_DARK = "0F172A"
    SLATE_LIGHT = "F8FAFC"
    BORDER_COLOR = "CBD5E1"
    TOTAL_FILL = "EFF6FF"
    GREEN_LIGHT = "F0FDF4"
    HEADER_ACCENT = "1E3A8A"

    fill_header = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
    fill_sub = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    fill_green = PatternFill(start_color=GREEN_LIGHT, end_color=GREEN_LIGHT, fill_type="solid")

    font_title = Font(name="Segoe UI", size=14, bold=True, color=NAVY_DARK)
    font_sub = Font(name="Segoe UI", size=10, bold=True, color=BLUE_MAIN)
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

    # ====================================================
    # HOJA 1: RESUMEN EJECUTIVO Y COMPARATIVA
    # ====================================================
    ws1 = wb.active
    ws1.title = "Resumen y Comparativa"
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "ALUFAC · Carpintería de Aluminio y PVC"
    ws1["A1"].font = font_title
    ws1["A2"] = f"{DATA['expediente']['empresa']['razon_social']} · CIF: {DATA['expediente']['empresa']['cif']} · Tel: {DATA['expediente']['empresa']['telefono']} · {DATA['expediente']['empresa']['email']}"
    ws1["A2"].font = font_italic

    ws1["A4"] = f"PRESUPUESTO TÉCNICO-COMERCIAL COMPARATIVO: {DATA['expediente']['codigo']}"
    ws1["A4"].font = font_sub
    ws1["F4"] = f"Fecha: {DATA['expediente']['fecha_formateada']}"
    ws1["F4"].font = font_italic
    ws1["F4"].alignment = Alignment(horizontal="right")

    ws1["A5"] = f"Cliente: {DATA['cliente']['nombre']} | Proyecto: {DATA['cliente']['proyecto']}"
    ws1["A5"].font = font_bold
    ws1["F5"] = f"Ref: {DATA['expediente']['referencia']}"
    ws1["F5"].font = font_italic
    ws1["F5"].alignment = Alignment(horizontal="right")

    ws1["A6"] = f"Ubicación: {DATA['cliente']['ubicacion']} | Arquitecto: {DATA['cliente']['arquitecto']}"
    ws1["A6"].font = font_reg

    # Tabla resumen comparativa
    r = 8
    ws1.cell(row=r, column=1, value="COMPARATIVA DE OPCIONES DE CARPINTERÍA (13 HUECOS EXTERIORES)").font = font_sub
    r += 1
    headers_comp = ["Concepto Económico", "Opción A: PVC Multicámara ≥ 76 mm", "Opción B: Aluminio con RPT", "Diferencia (€)", "Observaciones Técnicas"]
    for col_idx, h in enumerate(headers_comp, start=1):
        c = ws1.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [2, 3, 4] else "left", vertical="center")
        c.border = border_thin

    comp_data = [
        ("Suministro de 13 carpinterías exteriores (con vidrios de alta seguridad térmica y acústica)", 15000.00, 15540.00, "+540,00 €", "PVC 76 mm vs Cortizo COR 70/4200. Incluye barrotillos Helima en fachada sur."),
        ("Desmontaje y retirada de ventanas actuales", 620.00, 620.00, "0,00 €", "Retirada cuidadosa de los 13 huecos existentes y acopio."),
        ("Instalación profesional y remates perimetrales clipados", 1835.00, 1835.00, "0,00 €", "Fijación mecánica inox, sellado polímero MS marino y remates."),
        ("Transporte taller (Sant Lluís) - obra (Son Xoriguer) y gestión de residuos", 480.00, 480.00, "0,00 €", "Transporte protegido por carretera y entrega en punto limpio oficial."),
        ("Medición definitiva en obra y plantilla rígida arco V6", 0.00, 0.00, "0,00 €", "INCLUIDO sin coste adicional a la aceptación del presupuesto.")
    ]

    for item in comp_data:
        r += 1
        ws1.cell(row=r, column=1, value=item[0]).font = font_reg
        c2 = ws1.cell(row=r, column=2, value=item[1])
        c2.number_format = '#,##0.00 "€"'
        c2.font = font_reg
        c2.alignment = Alignment(horizontal="right")
        
        c3 = ws1.cell(row=r, column=3, value=item[2])
        c3.number_format = '#,##0.00 "€"'
        c3.font = font_reg
        c3.alignment = Alignment(horizontal="right")

        c4 = ws1.cell(row=r, column=4, value=f"=C{r}-B{r}")
        c4.number_format = '#,##0.00 "€"'
        c4.font = font_italic
        c4.alignment = Alignment(horizontal="center")

        ws1.cell(row=r, column=5, value=item[4]).font = font_italic

        for col in range(1, 6):
            ws1.cell(row=r, column=col).border = border_thin

    # Subtotales Comparativa
    r += 1
    ws1.cell(row=r, column=1, value="BASE IMPONIBLE (Subtotal Neto):").font = font_tot
    c_b1 = ws1.cell(row=r, column=2, value=f"=SUM(B10:B{r-1})")
    c_b1.number_format = '#,##0.00 "€"'
    c_b1.font = font_tot
    c_b1.alignment = Alignment(horizontal="right")

    c_b2 = ws1.cell(row=r, column=3, value=f"=SUM(C10:C{r-1})")
    c_b2.number_format = '#,##0.00 "€"'
    c_b2.font = font_tot
    c_b2.alignment = Alignment(horizontal="right")

    c_b_diff = ws1.cell(row=r, column=4, value=f"=C{r}-B{r}")
    c_b_diff.number_format = '#,##0.00 "€"'
    c_b_diff.font = font_tot
    c_b_diff.alignment = Alignment(horizontal="center")

    for col in range(1, 6):
        ws1.cell(row=r, column=col).border = border_thin
        ws1.cell(row=r, column=col).fill = fill_sub

    r += 1
    ws1.cell(row=r, column=1, value="I.V.A. Régimen General (21%):").font = font_reg
    c_iva1 = ws1.cell(row=r, column=2, value=f"=B{r-1}*0.21")
    c_iva1.number_format = '#,##0.00 "€"'
    c_iva1.font = font_reg
    c_iva1.alignment = Alignment(horizontal="right")

    c_iva2 = ws1.cell(row=r, column=3, value=f"=C{r-1}*0.21")
    c_iva2.number_format = '#,##0.00 "€"'
    c_iva2.font = font_reg
    c_iva2.alignment = Alignment(horizontal="right")

    c_iva_diff = ws1.cell(row=r, column=4, value=f"=C{r}-B{r}")
    c_iva_diff.number_format = '#,##0.00 "€"'
    c_iva_diff.font = font_italic
    c_iva_diff.alignment = Alignment(horizontal="center")

    for col in range(1, 6):
        ws1.cell(row=r, column=col).border = border_thin

    r += 1
    ws1.cell(row=r, column=1, value="TOTAL PRESUPUESTO (I.V.A. INCLUIDO):").font = font_tot_big
    c_tot1 = ws1.cell(row=r, column=2, value=f"=B{r-2}+B{r-1}")
    c_tot1.number_format = '#,##0.00 "€"'
    c_tot1.font = font_tot_big
    c_tot1.alignment = Alignment(horizontal="right")
    c_tot1.border = border_total

    c_tot2 = ws1.cell(row=r, column=3, value=f"=C{r-2}+C{r-1}")
    c_tot2.number_format = '#,##0.00 "€"'
    c_tot2.font = font_tot_big
    c_tot2.alignment = Alignment(horizontal="right")
    c_tot2.border = border_total

    c_tot_diff = ws1.cell(row=r, column=4, value=f"=C{r}-B{r}")
    c_tot_diff.number_format = '#,##0.00 "€"'
    c_tot_diff.font = font_tot_big
    c_tot_diff.alignment = Alignment(horizontal="center")

    for col in range(1, 6):
        ws1.cell(row=r, column=col).fill = fill_tot
        if col not in [2, 3]:
            ws1.cell(row=r, column=col).border = border_thin

    # Partida Separada de Mosquiteras
    r += 2
    ws1.cell(row=r, column=1, value="PARTIDA SEPARADA: MOSQUITERAS (5 UNIDADES)").font = font_sub
    r += 1
    ws1.cell(row=r, column=1, value="• 2 Mosquiteras plisadas laterales (B1, B2) + 3 Mosquiteras enrollables verticales (V1, V2, V3):").font = font_reg
    ws1.cell(row=r, column=2, value="Base: 820,00 €").font = font_bold
    ws1.cell(row=r, column=3, value="IVA (21%): 172,20 €").font = font_reg
    ws1.cell(row=r, column=4, value="TOTAL: 992,20 €").font = font_bold

    # Condiciones y plazos
    r += 2
    ws1.cell(row=r, column=1, value="CONDICIONES COMERCIALES Y DE EJECUCIÓN:").font = font_bold
    conds = [
      "• Plazo de fabricación: 6 a 8 semanas desde replanteo de medidas in situ y confirmación de muestras de color.",
      "• Plazo de montaje: 3 a 4 jornadas de trabajo por equipo oficial de ALUFAC en Son Xoriguer.",
      "• Planificación para Abril 2027: Toma de medidas en obra en enero/febrero 2027, fabricación en febrero/marzo y montaje en marzo/abril 2027.",
      "• Forma de pago: 40% al encargo y replanteo de medidas, 40% a la llegada de material a taller, 20% a la finalización y ajuste en obra.",
      "• Exclusiones: No se incluye obra civil, albañilería (recebados o mochetas) ni repasos de pintura en paredes.",
      "• Garantía: 5 años en perfiles de PVC/aluminio y estanqueidad de doble acristalamiento, 2 años en herrajes según normativa vigente."
    ]
    for c_text in conds:
        r += 1
        ws1.cell(row=r, column=1, value=c_text).font = font_reg

    ws1.column_dimensions["A"].width = 46
    ws1.column_dimensions["B"].width = 24
    ws1.column_dimensions["C"].width = 24
    ws1.column_dimensions["D"].width = 16
    ws1.column_dimensions["E"].width = 42

    # ====================================================
    # HOJA 2: DESGLOSE OPCIÓN A (PVC 76 MM)
    # ====================================================
    ws2 = wb.create_sheet(title="Opción A - PVC 76mm")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "ALUFAC · Opción A: Carpintería de PVC Multicámara ≥ 76 mm"
    ws2["A1"].font = font_title
    ws2["A2"] = "Acabado: Bicolor (Exterior Roble Dorado veteado / Interior Blanco) · Vidrio: 6 templado / 16 Argón / 44.2 BE (Solar en V8)"
    ws2["A2"].font = font_italic

    headers_items = ["Hueco", "Planta", "Dimensiones (mm)", "Uds", "Descripción Técnica y Apertura", "Barrotillos", "Suministro Unit. (€)", "Retirada Unit. (€)", "Instalación Unit. (€)", "Total Hueco (€)"]
    r = 4
    for col_idx, h in enumerate(headers_items, start=1):
        c = ws2.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [1, 2, 4] else ("right" if col_idx >= 7 else "left"), vertical="center")
        c.border = border_thin

    start_row = 5
    curr_row = start_row
    for item in DATA["elementos"]:
        ws2.cell(row=curr_row, column=1, value=item["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=curr_row, column=2, value=item["planta"]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=curr_row, column=3, value=f"{item['ancho_mm']} × {item['alto_mm']}").alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=curr_row, column=4, value=item["unidades"]).alignment = Alignment(horizontal="center", vertical="top")
        
        c_desc = ws2.cell(row=curr_row, column=5, value=f"{item['denominacion']}\n• Configuración: {item['configuracion']}\n• Vidrio: {item['vidrio']}")
        c_desc.alignment = Alignment(wrap_text=True, vertical="top")

        ws2.cell(row=curr_row, column=6, value=item["barrotillos"]).alignment = Alignment(vertical="top")

        c_sum = ws2.cell(row=curr_row, column=7, value=item["pvc_suministro_unit"])
        c_sum.number_format = '#,##0.00 "€"'
        c_sum.alignment = Alignment(horizontal="right", vertical="top")

        c_ret = ws2.cell(row=curr_row, column=8, value=item["retirada_unit"])
        c_ret.number_format = '#,##0.00 "€"'
        c_ret.alignment = Alignment(horizontal="right", vertical="top")

        c_inst = ws2.cell(row=curr_row, column=9, value=item["instalacion_unit"])
        c_inst.number_format = '#,##0.00 "€"'
        c_inst.alignment = Alignment(horizontal="right", vertical="top")

        c_tot = ws2.cell(row=curr_row, column=10, value=f"=D{curr_row}*(G{curr_row}+H{curr_row}+I{curr_row})")
        c_tot.number_format = '#,##0.00 "€"'
        c_tot.alignment = Alignment(horizontal="right", vertical="top")
        c_tot.font = font_bold

        for col in range(1, 11):
            ws2.cell(row=curr_row, column=col).border = border_thin
            ws2.cell(row=curr_row, column=col).font = font_reg if col != 10 else font_bold

        curr_row += 1

    # Servicios generales (transporte)
    ws2.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=6)
    ws2.cell(row=curr_row, column=1, value="Transporte taller (Sant Lluís) - Son Xoriguer (Ciutadella) y gestión autorizada de residuos:").font = font_bold
    ws2.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_tr = ws2.cell(row=curr_row, column=10, value=480.00)
    c_tr.number_format = '#,##0.00 "€"'
    c_tr.font = font_bold
    c_tr.alignment = Alignment(horizontal="right")
    for col in range(1, 11):
        ws2.cell(row=curr_row, column=col).border = border_thin
        ws2.cell(row=curr_row, column=col).fill = fill_sub

    curr_row += 1
    # Totales PVC
    ws2.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=9)
    ws2.cell(row=curr_row, column=1, value="BASE IMPONIBLE TOTAL OPCIÓN A (PVC 76 MM):").font = font_tot
    ws2.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_base_pvc = ws2.cell(row=curr_row, column=10, value=f"=SUM(J{start_row}:J{curr_row-1})")
    c_base_pvc.number_format = '#,##0.00 "€"'
    c_base_pvc.font = font_tot
    c_base_pvc.alignment = Alignment(horizontal="right")
    for col in range(1, 11):
        ws2.cell(row=curr_row, column=col).border = border_thin
        ws2.cell(row=curr_row, column=col).fill = fill_sub

    curr_row += 1
    ws2.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=9)
    ws2.cell(row=curr_row, column=1, value="I.V.A. Régimen General (21%):").font = font_reg
    ws2.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_iva_pvc = ws2.cell(row=curr_row, column=10, value=f"=J{curr_row-1}*0.21")
    c_iva_pvc.number_format = '#,##0.00 "€"'
    c_iva_pvc.font = font_reg
    c_iva_pvc.alignment = Alignment(horizontal="right")
    for col in range(1, 11):
        ws2.cell(row=curr_row, column=col).border = border_thin

    curr_row += 1
    ws2.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=9)
    ws2.cell(row=curr_row, column=1, value="TOTAL PRESUPUESTO OPCIÓN A - PVC (I.V.A. INCLUIDO):").font = font_tot_big
    ws2.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_tot_pvc = ws2.cell(row=curr_row, column=10, value=f"=J{curr_row-2}+J{curr_row-1}")
    c_tot_pvc.number_format = '#,##0.00 "€"'
    c_tot_pvc.font = font_tot_big
    c_tot_pvc.alignment = Alignment(horizontal="right")
    c_tot_pvc.border = border_total
    for col in range(1, 11):
        ws2.cell(row=curr_row, column=col).fill = fill_tot
        if col != 10:
            ws2.cell(row=curr_row, column=col).border = border_thin

    ws2.column_dimensions["A"].width = 8
    ws2.column_dimensions["B"].width = 14
    ws2.column_dimensions["C"].width = 18
    ws2.column_dimensions["D"].width = 6
    ws2.column_dimensions["E"].width = 46
    ws2.column_dimensions["F"].width = 24
    ws2.column_dimensions["G"].width = 18
    ws2.column_dimensions["H"].width = 16
    ws2.column_dimensions["I"].width = 18
    ws2.column_dimensions["J"].width = 18

    # ====================================================
    # HOJA 3: DESGLOSE OPCIÓN B (ALUMINIO RPT CORTIZO)
    # ====================================================
    ws3 = wb.create_sheet(title="Opción B - Aluminio RPT")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "ALUFAC · Opción B: Carpintería de Aluminio con RPT (Sistemas CORTIZO)"
    ws3["A1"].font = font_title
    ws3["A2"] = "Sistemas: Cortizo COR 70 Industrial / COR 4200 / Millenium · Acabado: Bicolor Roble Dorado exterior / Blanco interior"
    ws3["A2"].font = font_italic

    r = 4
    for col_idx, h in enumerate(headers_items, start=1):
        c = ws3.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [1, 2, 4] else ("right" if col_idx >= 7 else "left"), vertical="center")
        c.border = border_thin

    start_row = 5
    curr_row = start_row
    for item in DATA["elementos"]:
        ws3.cell(row=curr_row, column=1, value=item["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
        ws3.cell(row=curr_row, column=2, value=item["planta"]).alignment = Alignment(horizontal="center", vertical="top")
        ws3.cell(row=curr_row, column=3, value=f"{item['ancho_mm']} × {item['alto_mm']}").alignment = Alignment(horizontal="center", vertical="top")
        ws3.cell(row=curr_row, column=4, value=item["unidades"]).alignment = Alignment(horizontal="center", vertical="top")
        
        c_desc = ws3.cell(row=curr_row, column=5, value=f"{item['denominacion']}\n• Configuración: {item['configuracion']}\n• Vidrio: {item['vidrio']}")
        c_desc.alignment = Alignment(wrap_text=True, vertical="top")

        ws3.cell(row=curr_row, column=6, value=item["barrotillos"]).alignment = Alignment(vertical="top")

        c_sum = ws3.cell(row=curr_row, column=7, value=item["alu_suministro_unit"])
        c_sum.number_format = '#,##0.00 "€"'
        c_sum.alignment = Alignment(horizontal="right", vertical="top")

        c_ret = ws3.cell(row=curr_row, column=8, value=item["retirada_unit"])
        c_ret.number_format = '#,##0.00 "€"'
        c_ret.alignment = Alignment(horizontal="right", vertical="top")

        c_inst = ws3.cell(row=curr_row, column=9, value=item["instalacion_unit"])
        c_inst.number_format = '#,##0.00 "€"'
        c_inst.alignment = Alignment(horizontal="right", vertical="top")

        c_tot = ws3.cell(row=curr_row, column=10, value=f"=D{curr_row}*(G{curr_row}+H{curr_row}+I{curr_row})")
        c_tot.number_format = '#,##0.00 "€"'
        c_tot.alignment = Alignment(horizontal="right", vertical="top")
        c_tot.font = font_bold

        for col in range(1, 11):
            ws3.cell(row=curr_row, column=col).border = border_thin
            ws3.cell(row=curr_row, column=col).font = font_reg if col != 10 else font_bold

        curr_row += 1

    # Servicios generales (transporte)
    ws3.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=6)
    ws3.cell(row=curr_row, column=1, value="Transporte taller (Sant Lluís) - Son Xoriguer (Ciutadella) y gestión autorizada de residuos:").font = font_bold
    ws3.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_tr = ws3.cell(row=curr_row, column=10, value=480.00)
    c_tr.number_format = '#,##0.00 "€"'
    c_tr.font = font_bold
    c_tr.alignment = Alignment(horizontal="right")
    for col in range(1, 11):
        ws3.cell(row=curr_row, column=col).border = border_thin
        ws3.cell(row=curr_row, column=col).fill = fill_sub

    curr_row += 1
    # Totales Alu
    ws3.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=9)
    ws3.cell(row=curr_row, column=1, value="BASE IMPONIBLE TOTAL OPCIÓN B (ALUMINIO RPT):").font = font_tot
    ws3.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_base_alu = ws3.cell(row=curr_row, column=10, value=f"=SUM(J{start_row}:J{curr_row-1})")
    c_base_alu.number_format = '#,##0.00 "€"'
    c_base_alu.font = font_tot
    c_base_alu.alignment = Alignment(horizontal="right")
    for col in range(1, 11):
        ws3.cell(row=curr_row, column=col).border = border_thin
        ws3.cell(row=curr_row, column=col).fill = fill_sub

    curr_row += 1
    ws3.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=9)
    ws3.cell(row=curr_row, column=1, value="I.V.A. Régimen General (21%):").font = font_reg
    ws3.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_iva_alu = ws3.cell(row=curr_row, column=10, value=f"=J{curr_row-1}*0.21")
    c_iva_alu.number_format = '#,##0.00 "€"'
    c_iva_alu.font = font_reg
    c_iva_alu.alignment = Alignment(horizontal="right")
    for col in range(1, 11):
        ws3.cell(row=curr_row, column=col).border = border_thin

    curr_row += 1
    ws3.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=9)
    ws3.cell(row=curr_row, column=1, value="TOTAL PRESUPUESTO OPCIÓN B - ALUMINIO RPT (I.V.A. INCLUIDO):").font = font_tot_big
    ws3.cell(row=curr_row, column=1).alignment = Alignment(horizontal="right")
    c_tot_alu = ws3.cell(row=curr_row, column=10, value=f"=J{curr_row-2}+J{curr_row-1}")
    c_tot_alu.number_format = '#,##0.00 "€"'
    c_tot_alu.font = font_tot_big
    c_tot_alu.alignment = Alignment(horizontal="right")
    c_tot_alu.border = border_total
    for col in range(1, 11):
        ws3.cell(row=curr_row, column=col).fill = fill_tot
        if col != 10:
            ws3.cell(row=curr_row, column=col).border = border_thin

    ws3.column_dimensions["A"].width = 8
    ws3.column_dimensions["B"].width = 14
    ws3.column_dimensions["C"].width = 18
    ws3.column_dimensions["D"].width = 6
    ws3.column_dimensions["E"].width = 46
    ws3.column_dimensions["F"].width = 24
    ws3.column_dimensions["G"].width = 18
    ws3.column_dimensions["H"].width = 16
    ws3.column_dimensions["I"].width = 18
    ws3.column_dimensions["J"].width = 18

    # ====================================================
    # HOJA 4: MOSQUITERAS
    # ====================================================
    ws4 = wb.create_sheet(title="Mosquiteras")
    ws4.views.sheetView[0].showGridLines = True

    ws4["A1"] = "ALUFAC · Partida Separada de Mosquiteras a Medida"
    ws4["A1"].font = font_title
    ws4["A2"] = "Ubicación: Dormitorios y baños según solicitud del cliente · Perfilería de aluminio lacado a juego e instalación incluida"
    ws4["A2"].font = font_italic

    headers_mosq = ["Hueco", "Tipo de Mosquitera", "Dimensiones", "Uds", "Descripción y Acabado", "Precio Unit. (€)", "Subtotal Neto (€)"]
    r = 4
    for col_idx, h in enumerate(headers_mosq, start=1):
        c = ws4.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [1, 3, 4] else ("right" if col_idx >= 6 else "left"), vertical="center")
        c.border = border_thin

    r_mosq_start = 5
    curr_r = r_mosq_start
    for m in DATA["mosquiteras"]:
        ws4.cell(row=curr_r, column=1, value=m["hueco"]).alignment = Alignment(horizontal="center")
        ws4.cell(row=curr_r, column=2, value=m["tipo"]).font = font_bold
        ws4.cell(row=curr_r, column=3, value=m["dimension"]).alignment = Alignment(horizontal="center")
        ws4.cell(row=curr_r, column=4, value=m["unidades"]).alignment = Alignment(horizontal="center")
        ws4.cell(row=curr_r, column=5, value=m["descripcion"]).font = font_reg
        
        c_u = ws4.cell(row=curr_r, column=6, value=m["precio_unit"])
        c_u.number_format = '#,##0.00 "€"'
        c_u.alignment = Alignment(horizontal="right")

        c_sub = ws4.cell(row=curr_r, column=7, value=f"=D{curr_r}*F{curr_r}")
        c_sub.number_format = '#,##0.00 "€"'
        c_sub.alignment = Alignment(horizontal="right")
        c_sub.font = font_bold

        for col in range(1, 8):
            ws4.cell(row=curr_r, column=col).border = border_thin
        curr_r += 1

    # Totales Mosquiteras
    ws4.merge_cells(start_row=curr_r, start_column=1, end_row=curr_r, end_column=6)
    ws4.cell(row=curr_r, column=1, value="SUBTOTAL NETO MOSQUITERAS:").font = font_tot
    ws4.cell(row=curr_r, column=1).alignment = Alignment(horizontal="right")
    c_mosq_tot = ws4.cell(row=curr_r, column=7, value=f"=SUM(G{r_mosq_start}:G{curr_r-1})")
    c_mosq_tot.number_format = '#,##0.00 "€"'
    c_mosq_tot.font = font_tot
    c_mosq_tot.alignment = Alignment(horizontal="right")
    for col in range(1, 8):
        ws4.cell(row=curr_r, column=col).border = border_thin
        ws4.cell(row=curr_r, column=col).fill = fill_sub

    curr_r += 1
    ws4.merge_cells(start_row=curr_r, start_column=1, end_row=curr_r, end_column=6)
    ws4.cell(row=curr_r, column=1, value="I.V.A. Régimen General (21%):").font = font_reg
    ws4.cell(row=curr_r, column=1).alignment = Alignment(horizontal="right")
    c_mosq_iva = ws4.cell(row=curr_r, column=7, value=f"=G{curr_r-1}*0.21")
    c_mosq_iva.number_format = '#,##0.00 "€"'
    c_mosq_iva.font = font_reg
    c_mosq_iva.alignment = Alignment(horizontal="right")
    for col in range(1, 8):
        ws4.cell(row=curr_r, column=col).border = border_thin

    curr_r += 1
    ws4.merge_cells(start_row=curr_r, start_column=1, end_row=curr_r, end_column=6)
    ws4.cell(row=curr_r, column=1, value="TOTAL PARTIDA MOSQUITERAS (I.V.A. INCLUIDO):").font = font_tot_big
    ws4.cell(row=curr_r, column=1).alignment = Alignment(horizontal="right")
    c_mosq_final = ws4.cell(row=curr_r, column=7, value=f"=G{curr_r-2}+G{curr_r-1}")
    c_mosq_final.number_format = '#,##0.00 "€"'
    c_mosq_final.font = font_tot_big
    c_mosq_final.alignment = Alignment(horizontal="right")
    c_mosq_final.border = border_total
    for col in range(1, 8):
        ws4.cell(row=curr_r, column=col).fill = fill_tot
        if col != 7:
            ws4.cell(row=curr_r, column=col).border = border_thin

    ws4.column_dimensions["A"].width = 10
    ws4.column_dimensions["B"].width = 26
    ws4.column_dimensions["C"].width = 24
    ws4.column_dimensions["D"].width = 8
    ws4.column_dimensions["E"].width = 50
    ws4.column_dimensions["F"].width = 18
    ws4.column_dimensions["G"].width = 20

    # ====================================================
    # HOJA 5: ESCANDALLO INTERNO TÉCNICO
    # ====================================================
    ws5 = wb.create_sheet(title="Escandallo Técnico Interno")
    ws5.views.sheetView[0].showGridLines = True

    ws5["A1"] = "ALUFAC · Escandallo Técnico de Costes y Rentabilidad (Uso Interno)"
    ws5["A1"].font = font_title
    ws5["A2"] = f"Expediente: {DATA['expediente']['codigo']} | Cliente: {DATA['cliente']['nombre']} | Son Xoriguer, Ciutadella"
    ws5["A2"].font = font_italic

    headers_cost = ["Capítulo de Coste", "Detalle Técnico y Materiales", "Medición", "Ud.", "Coste Ud. (€)", "Subtotal (€)"]
    r = 4
    for col_idx, h in enumerate(headers_cost, start=1):
        c = ws5.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [3, 4] else ("right" if col_idx >= 5 else "left"), vertical="center")
        c.border = border_thin

    cost_breakdown = [
        ("Perfiles y refuerzos de acero", "Sistemas multicámara 76 mm con refuerzo galvanizado y foliado exterior roble", 240.0, "kg", 8.80),
        ("Vidrios seguridad y acústicos", "6 templado / c16 argón 90% / 44.2 laminado bajo emisivo con warm-edge", 17.2, "m²", 115.00),
        ("Vidrios control solar V8", "6 templado control solar selectivo / c16 argón / 44.2 bajo emisivo", 3.9, "m²", 155.00),
        ("Herrajes perimetrales y cierres", "Cremonas, compases oscilobatientes y cerraderos anticorrosivos balear Grado 5", 13.0, "cjto", 72.00),
        ("Barrotillos Helima en cámara", "Barrotillo 18×8 mm bicolor montado en cámara de 16 mm con cruces y sujeciones", 18.0, "m", 18.50),
        ("Solera telescópica y arco V6", "Mecanizado y curvado especial CNC en dintel y carril embutido con drenaje", 1.0, "ud", 950.00),
        ("Mano de Obra Taller ALUFAC", "Corte, termosoldadura, herraje, engomado, acristalado y control calidad (35 €/h)", 62.0, "h", 35.00),
        ("Mano de Obra Montaje en Obra", "Desmontaje ventanas previas, aplomado, fijación mecánica, calzos y sellado MS (35 €/h)", 48.0, "h", 35.00),
        ("Selladores y remates perimetrales", "Cartuchos polímero MS marino, calzos neopreno, anclajes inox A2 y solapes", 1.0, "pa", 460.00),
        ("Logística y gestión de residuos", "Portes taller Sant Lluís - Son Xoriguer (camión carrozado) y canon de reciclaje vertedero", 1.0, "pa", 310.00)
    ]

    r_cost_start = 5
    curr_rc = r_cost_start
    for cb in cost_breakdown:
        ws5.cell(row=curr_rc, column=1, value=cb[0]).font = font_bold
        ws5.cell(row=curr_rc, column=2, value=cb[1]).font = font_reg
        ws5.cell(row=curr_rc, column=3, value=cb[2]).alignment = Alignment(horizontal="center")
        ws5.cell(row=curr_rc, column=4, value=cb[3]).alignment = Alignment(horizontal="center")
        
        cu = ws5.cell(row=curr_rc, column=5, value=cb[4])
        cu.number_format = '#,##0.00 "€"'
        cu.alignment = Alignment(horizontal="right")

        c_sub = ws5.cell(row=curr_rc, column=6, value=f"=C{curr_rc}*E{curr_rc}")
        c_sub.number_format = '#,##0.00 "€"'
        c_sub.alignment = Alignment(horizontal="right")
        c_sub.font = font_bold

        for col in range(1, 7):
            ws5.cell(row=curr_rc, column=col).border = border_thin
        curr_rc += 1

    # Totales de Coste y Margen
    ws5.merge_cells(start_row=curr_rc, start_column=1, end_row=curr_rc, end_column=5)
    ws5.cell(row=curr_rc, column=1, value="COSTE DIRECTO TOTAL TÉCNICO:").font = font_tot
    ws5.cell(row=curr_rc, column=1).alignment = Alignment(horizontal="right")
    c_coste_tot = ws5.cell(row=curr_rc, column=6, value=f"=SUM(F{r_cost_start}:F{curr_rc-1})")
    c_coste_tot.number_format = '#,##0.00 "€"'
    c_coste_tot.font = font_tot
    c_coste_tot.alignment = Alignment(horizontal="right")
    for col in range(1, 7):
        ws5.cell(row=curr_rc, column=col).border = border_thin
        ws5.cell(row=curr_rc, column=col).fill = fill_sub

    curr_rc += 1
    ws5.merge_cells(start_row=curr_rc, start_column=1, end_row=curr_rc, end_column=5)
    ws5.cell(row=curr_rc, column=1, value="PRECIO DE VENTA NETO (Opción A - PVC):").font = font_tot
    ws5.cell(row=curr_rc, column=1).alignment = Alignment(horizontal="right")
    c_pv = ws5.cell(row=curr_rc, column=6, value=17935.00)
    c_pv.number_format = '#,##0.00 "€"'
    c_pv.font = font_tot
    c_pv.alignment = Alignment(horizontal="right")
    for col in range(1, 7):
        ws5.cell(row=curr_rc, column=col).border = border_thin

    curr_rc += 1
    ws5.merge_cells(start_row=curr_rc, start_column=1, end_row=curr_rc, end_column=5)
    ws5.cell(row=curr_rc, column=1, value="MARGEN BRUTO DE CONTRIBUCIÓN (€):").font = font_tot_big
    ws5.cell(row=curr_rc, column=1).alignment = Alignment(horizontal="right")
    c_mb = ws5.cell(row=curr_rc, column=6, value=f"=F{curr_rc-1}-F{curr_rc-2}")
    c_mb.number_format = '#,##0.00 "€"'
    c_mb.font = font_tot_big
    c_mb.alignment = Alignment(horizontal="right")
    for col in range(1, 7):
        ws5.cell(row=curr_rc, column=col).border = border_thin
        ws5.cell(row=curr_rc, column=col).fill = fill_green

    curr_rc += 1
    ws5.merge_cells(start_row=curr_rc, start_column=1, end_row=curr_rc, end_column=5)
    ws5.cell(row=curr_rc, column=1, value="MARGEN SOBRE VENTA (%):").font = font_tot_big
    ws5.cell(row=curr_rc, column=1).alignment = Alignment(horizontal="right")
    c_mb_pct = ws5.cell(row=curr_rc, column=6, value=f"=F{curr_rc-1}/F{curr_rc-2}")
    c_mb_pct.number_format = '0.0%'
    c_mb_pct.font = font_tot_big
    c_mb_pct.alignment = Alignment(horizontal="right")
    c_mb_pct.border = border_total
    for col in range(1, 7):
        ws5.cell(row=curr_rc, column=col).fill = fill_green
        if col != 6:
            ws5.cell(row=curr_rc, column=col).border = border_thin

    ws5.column_dimensions["A"].width = 30
    ws5.column_dimensions["B"].width = 56
    ws5.column_dimensions["C"].width = 12
    ws5.column_dimensions["D"].width = 8
    ws5.column_dimensions["E"].width = 16
    ws5.column_dimensions["F"].width = 18

    excel_file = os.path.join(BASE_DIR, "Presupuesto_P2026_0053_Carpinteria_Son_Xoriguer_Moratalla.xlsx")
    wb.save(excel_file)
    print(f"Excel generado con éxito en: {excel_file}")
    return excel_file

def generate_html_files():
    cliente_html_path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    tecnico_html_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")

    # Filas de elementos para PVC
    pvc_rows_html = ""
    for item in DATA["elementos"]:
        subt_pvc = item["unidades"] * (item["pvc_suministro_unit"] + item["retirada_unit"] + item["instalacion_unit"])
        pvc_rows_html += f"""
        <tr>
            <td class="code-col">{item['codigo']}</td>
            <td>{item['planta']}</td>
            <td class="num-col">{item['ancho_mm']} × {item['alto_mm']} mm</td>
            <td class="num-col">{item['unidades']}</td>
            <td>
                <strong>{item['denominacion']}</strong><br>
                <small style="color: #475569;">
                    • Apertura: {item['configuracion']}<br>
                    • Vidrio: {item['vidrio']}<br>
                    • Barrotillos: {item['barrotillos']}
                </small>
            </td>
            <td class="currency">{item['pvc_suministro_unit']:,.2f} €</td>
            <td class="currency">{item['retirada_unit']:,.2f} €</td>
            <td class="currency">{item['instalacion_unit']:,.2f} €</td>
            <td class="currency total-cell">{subt_pvc:,.2f} €</td>
        </tr>
        """

    # Filas de elementos para Aluminio RPT
    alu_rows_html = ""
    for item in DATA["elementos"]:
        subt_alu = item["unidades"] * (item["alu_suministro_unit"] + item["retirada_unit"] + item["instalacion_unit"])
        alu_rows_html += f"""
        <tr>
            <td class="code-col">{item['codigo']}</td>
            <td>{item['planta']}</td>
            <td class="num-col">{item['ancho_mm']} × {item['alto_mm']} mm</td>
            <td class="num-col">{item['unidades']}</td>
            <td>
                <strong>{item['denominacion']}</strong><br>
                <small style="color: #475569;">
                    • Apertura: {item['configuracion']}<br>
                    • Vidrio: {item['vidrio']}<br>
                    • Barrotillos: {item['barrotillos']}
                </small>
            </td>
            <td class="currency">{item['alu_suministro_unit']:,.2f} €</td>
            <td class="currency">{item['retirada_unit']:,.2f} €</td>
            <td class="currency">{item['instalacion_unit']:,.2f} €</td>
            <td class="currency total-cell">{subt_alu:,.2f} €</td>
        </tr>
        """

    # Filas mosquiteras
    mosq_rows_html = ""
    for m in DATA["mosquiteras"]:
        mosq_rows_html += f"""
        <tr>
            <td class="code-col">{m['hueco']}</td>
            <td><strong>{m['tipo']}</strong></td>
            <td class="num-col">{m['dimension']}</td>
            <td class="num-col">{m['unidades']}</td>
            <td>{m['descripcion']}</td>
            <td class="currency">{m['precio_unit']:,.2f} €</td>
            <td class="currency total-cell">{m['subtotal']:,.2f} €</td>
        </tr>
        """

    # 1. HTML CLIENTE
    html_cliente = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Presupuesto Carpintería Son Xoriguer · ALUFAC</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 12mm 14mm 14mm 14mm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 8.5pt;
            line-height: 1.35;
            color: #1e293b;
            margin: 0;
            padding: 0;
            background: #ffffff;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 2px solid #0284c7;
            padding-bottom: 8px;
            margin-bottom: 12px;
        }}
        .brand h1 {{
            font-size: 18pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.5px;
        }}
        .brand h1 span {{
            color: #0284c7;
        }}
        .brand p {{
            margin: 2px 0 0 0;
            font-size: 8pt;
            color: #64748b;
        }}
        .doc-meta {{
            text-align: right;
            font-size: 8pt;
            color: #475569;
        }}
        .doc-meta .badge {{
            display: inline-block;
            background: #e0f2fe;
            color: #0369a1;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            margin-bottom: 4px;
            font-size: 8.5pt;
        }}
        .client-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #0284c7;
            border-radius: 4px;
            padding: 8px 12px;
            margin-bottom: 12px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            font-size: 8pt;
        }}
        .client-box div strong {{
            color: #0f172a;
        }}
        h2 {{
            font-size: 10pt;
            color: #0f172a;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 3px;
            margin: 12px 0 6px 0;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        p.intro {{
            margin: 4px 0 8px 0;
            text-align: justify;
            color: #334155;
            font-size: 8pt;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 10px;
            font-size: 7.8pt;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            vertical-align: middle;
        }}
        th {{
            background-color: #0f172a;
            color: #ffffff;
            font-weight: 600;
            text-align: left;
            font-size: 7.5pt;
        }}
        .num-col {{ text-align: center; white-space: nowrap; }}
        .code-col {{ text-align: center; font-weight: 700; color: #0284c7; }}
        .currency {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
        .total-cell {{ font-weight: 700; color: #0f172a; background: #f8fafc; }}
        .table-totals tr td {{
            font-weight: 700;
            background: #f1f5f9;
        }}
        .table-totals tr.grand-total td {{
            background: #e0f2fe;
            color: #0369a1;
            font-size: 9pt;
            border-top: 2px solid #0284c7;
            border-bottom: 2px solid #0284c7;
        }}
        .feature-box {{
            background: #fffbeb;
            border: 1px solid #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 6px 10px;
            margin: 8px 0;
            border-radius: 4px;
            font-size: 7.8pt;
        }}
        .feature-box strong {{
            color: #b45309;
        }}
        .conditions {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 8px 10px;
            font-size: 7.5pt;
            color: #475569;
            margin-top: 8px;
        }}
        .conditions ul {{
            margin: 4px 0 0 16px;
            padding: 0;
        }}
        .conditions li {{
            margin-bottom: 2px;
        }}
        .page-break {{
            page-break-before: always;
        }}
        .signatures {{
            display: flex;
            justify-content: space-between;
            margin-top: 25px;
            padding-top: 10px;
            font-size: 8pt;
        }}
        .sig-block {{
            width: 45%;
            border-top: 1px solid #94a3b8;
            padding-top: 5px;
            text-align: center;
            color: #64748b;
        }}
    </style>
</head>
<body>

    <!-- CABECERA -->
    <div class="header">
        <div class="brand">
            <h1>ALUFAC<span>.</span></h1>
            <p><strong>Dixis Recursos y Soluciones S.L.</strong> · CIF: B57825432</p>
            <p>Circunval·lació, 11, Pol. Ind. de Sant Lluís · 07710 Sant Lluís, Menorca</p>
            <p>Tel / WhatsApp: +34 669 769 541 · Email: info@alufac.es · Web: www.alufac.es</p>
        </div>
        <div class="doc-meta">
            <div class="badge">OFERTA TÉCNICO-COMERCIAL</div><br>
            <strong>Expediente:</strong> P-2026-0053<br>
            <strong>Referencia:</strong> PRE-2026-1103-SONXORIGUER-MORATALLA<br>
            <strong>Fecha de emisión:</strong> 3 de noviembre de 2026<br>
            <strong>Validez:</strong> 30 días naturales
        </div>
    </div>

    <!-- DATOS DEL CLIENTE Y PROYECTO -->
    <div class="client-box">
        <div>
            <strong>Cliente:</strong> Eduardo Moratalla / Karin Eckhard<br>
            <strong>Emplazamiento:</strong> Son Xoriguer 4, Puerta 7, 07769 Ciutadella, Menorca<br>
            <strong>Proyecto:</strong> Reforma Integral CASA 7
        </div>
        <div>
            <strong>Arquitecto:</strong> Alfonso Cort (ACA Arquitectos · Tel. 627 96 97 05)<br>
            <strong>Planos de Referencia:</strong> C03 (Planta Baja) y C04 (Planta Primera), Sept 2026<br>
            <strong>Alcance:</strong> 13 Huecos Exteriores (PVC vs Aluminio RPT) + Mosquiteras
        </div>
    </div>

    <p class="intro">
        Estimado Eduardo: Atendiendo a su solicitud de oferta, desde <strong>ALUFAC</strong> nos complace presentarle nuestra propuesta técnico-económica integral para las ventanas y balconeras exteriores de la reforma en Son Xoriguer (Ciutadella). Hemos preparado el <strong>desglose exacto por hueco</strong>, detallando de forma individual el coste de suministro de carpintería con vidrio de seguridad térmica, retirada de carpinterías actuales, transporte, instalación y remates con el IVA identificado. Asimismo, contrastamos por separado la solución en <strong>PVC Multicámara ≥ 76 mm</strong> y la alternativa en <strong>Aluminio con Rotura de Puente Térmico (CORTIZO)</strong>, junto con la partida independiente de mosquiteras.
    </p>

    <!-- CUADRO RESUMEN COMPARATIVO -->
    <h2>1. Resumen Ejecutivo Comparativo de Opciones (13 Huecos Exteriores)</h2>
    <table>
        <thead>
            <tr>
                <th>Concepto del Presupuesto</th>
                <th style="text-align: right; width: 130px;">Opción A: PVC ≥ 76 mm</th>
                <th style="text-align: right; width: 130px;">Opción B: Aluminio RPT</th>
                <th style="text-align: center; width: 90px;">Diferencia</th>
                <th>Especificaciones Clave</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Suministro de 13 carpinterías exteriores</strong> (Vidrio 6T/16Ar/44.2 BE y Solar V8 + Barrotillos)</td>
                <td class="currency">15.000,00 €</td>
                <td class="currency">15.540,00 €</td>
                <td class="num-col">+540,00 €</td>
                <td>Bicolor: Roble Dorado exterior veteado / Blanco interior. Herrajes costeros balear Grado 5.</td>
            </tr>
            <tr>
                <td><strong>Desmontaje y retirada de carpinterías actuales</strong></td>
                <td class="currency">620,00 €</td>
                <td class="currency">620,00 €</td>
                <td class="num-col">0,00 €</td>
                <td>Desmontaje cuidadoso de 13 huecos existentes sin afección a mampostería.</td>
            </tr>
            <tr>
                <td><strong>Instalación técnica en obra y remates perimetrales clipados</strong></td>
                <td class="currency">1.835,00 €</td>
                <td class="currency">1.835,00 €</td>
                <td class="num-col">0,00 €</td>
                <td>Fijaciones mecánicas inox A2, calzos térmicos, sellado con polímero MS marino y solapes clipados.</td>
            </tr>
            <tr>
                <td><strong>Transporte taller (Sant Lluís) - Son Xoriguer y canon de residuos</strong></td>
                <td class="currency">480,00 €</td>
                <td class="currency">480,00 €</td>
                <td class="num-col">0,00 €</td>
                <td>Desplazamientos protegidos por carretera y tasa ecológica de gestor de residuos autorizado.</td>
            </tr>
            <tr>
                <td><strong>Medición definitiva en obra y plantilla rígida arco V6</strong></td>
                <td class="currency" style="color: #0369a1; font-weight: 700;">INCLUIDO (0,00 €)</td>
                <td class="currency" style="color: #0369a1; font-weight: 700;">INCLUIDO (0,00 €)</td>
                <td class="num-col">—</td>
                <td>Toma de medidas in situ y plantilla física para el dintel arqueado de la V6 sin coste adicional.</td>
            </tr>
        </tbody>
        <tbody class="table-totals">
            <tr>
                <td>BASE IMPONIBLE (Subtotal Neto):</td>
                <td class="currency">17.935,00 €</td>
                <td class="currency">18.475,00 €</td>
                <td class="num-col">+540,00 €</td>
                <td>Ambas opciones incluyen los mismos vidrios de alta prestación y acabados bicolores.</td>
            </tr>
            <tr>
                <td>I.V.A. Régimen General (21%):</td>
                <td class="currency">3.766,35 €</td>
                <td class="currency">3.879,75 €</td>
                <td class="num-col">+113,40 €</td>
                <td>Impuesto sobre el Valor Añadido identificado según normativa fiscal.</td>
            </tr>
            <tr class="grand-total">
                <td>TOTAL PRESUPUESTO PROYECTO (IVA INCLUIDO):</td>
                <td class="currency">21.701,35 €</td>
                <td class="currency">22.354,75 €</td>
                <td class="num-col">+653,40 €</td>
                <td>Garantía de fabricación e instalación directa por ALUFAC en Menorca.</td>
            </tr>
        </tbody>
    </table>

    <!-- PARTIDA MOSQUITERAS -->
    <h2>2. Partida Independiente de Mosquiteras (Dormitorios y Baños)</h2>
    <p class="intro">
        Cumpliendo su indicación expresa, se presupuesta por separado la instalación de mosquiteras en los 5 huecos de descanso y aseo. La perfilería de aluminio se suministra lacada a juego del color exterior de la carpintería:
    </p>
    <table>
        <thead>
            <tr>
                <th style="width: 45px; text-align: center;">Hueco</th>
                <th>Sistema de Mosquitera</th>
                <th style="text-align: center; width: 110px;">Medidas</th>
                <th style="text-align: center; width: 35px;">Ud</th>
                <th>Características Técnicas y Materiales</th>
                <th style="text-align: right; width: 85px;">Precio Ud</th>
                <th style="text-align: right; width: 85px;">Total Neto</th>
            </tr>
        </thead>
        <tbody>
            {mosq_rows_html}
        </tbody>
        <tbody class="table-totals">
            <tr>
                <td colspan="5">SUBTOTAL NETO MOSQUITERAS:</td>
                <td colspan="2" class="currency">820,00 €</td>
            </tr>
            <tr>
                <td colspan="5">I.V.A. Régimen General (21%):</td>
                <td colspan="2" class="currency">172,20 €</td>
            </tr>
            <tr class="grand-total">
                <td colspan="5">TOTAL PARTIDA MOSQUITERAS (IVA INCLUIDO):</td>
                <td colspan="2" class="currency">992,20 €</td>
            </tr>
        </tbody>
    </table>

    <div class="feature-box">
        <strong>Detalle Técnico Singular · Balconera V6 (Telescópica con Fijo Superior en Arco):</strong><br>
        • <strong>Paso libre conseguido:</strong> Sobre el hueco de obra de 1.980 mm, el módulo fijo ocupa ~660 mm. Las 2 hojas correderas móviles se deslizan sobre guías paralelas independientes y se apilan tras el fijo. Con los solapes técnicos y montantes verticales de encuentro (~120–140 mm), el sistema proporciona un <strong>paso libre efectivo de 1.180 a 1.200 mm</strong>, cumpliendo con total fidelidad el intervalo requerido por el arquitecto (1.150–1.250 mm).<br>
        • <strong>Umbral enrasado y drenaje:</strong> Se instala carril inferior de suelo continuo empotrado a cota cero con rotura de puente térmico y ranuras de evacuación canalizadas a la arqueta/canal exterior.<br>
        • <strong>Recomendación técnica ALUFAC:</strong> Aunque es viable en PVC reforzado, la solución en <strong>Aluminio RPT (Cortizo COR 4200 / COR 4700 de 3 carriles)</strong> resulta arquitectónicamente óptima para este elemento: permite una sección de nudos centrales mucho más esbelta, un curvado de precisión milimétrica mediante plantilla en taller sin riesgo de despegue de lámina foliada, y un deslizamiento de rodamientos de acero inoxidable extremadamente suave.
    </div>

    <div class="page-break"></div>

    <!-- CABECERA PÁGINA 2 -->
    <div class="header">
        <div class="brand">
            <h1>ALUFAC<span>.</span></h1>
            <p><strong>Dixis Recursos y Soluciones S.L.</strong> · Circunval·lació, 11, Sant Lluís, Menorca</p>
        </div>
        <div class="doc-meta">
            <strong>Expediente:</strong> P-2026-0053 · Ref: PRE-2026-1103-SONXORIGUER-MORATALLA<br>
            <strong>Desglose Detallado por Hueco:</strong> Opción A (PVC ≥ 76 mm) y Opción B (Aluminio RPT)
        </div>
    </div>

    <!-- DESGLOSE DETALLADO OPCIÓN A: PVC -->
    <h2>3. Desglose Detallado por Hueco · Opción A: PVC Multicámara ≥ 76 mm</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 32px; text-align: center;">Ref</th>
                <th style="width: 65px;">Planta</th>
                <th style="width: 80px; text-align: center;">Medidas</th>
                <th style="width: 25px; text-align: center;">Ud</th>
                <th>Descripción Técnica, Vidrio y Apertura</th>
                <th style="text-align: right; width: 68px;">Suministro</th>
                <th style="text-align: right; width: 55px;">Retirada</th>
                <th style="text-align: right; width: 65px;">Instalación</th>
                <th style="text-align: right; width: 75px;">Total Hueco</th>
            </tr>
        </thead>
        <tbody>
            {pvc_rows_html}
            <tr>
                <td colspan="5" style="text-align: right; font-weight: bold; background: #f8fafc;">Transporte especializado taller (Sant Lluís) - Son Xoriguer y canon oficial de gestión de residuos:</td>
                <td colspan="3" class="currency" style="background: #f8fafc;">Logística y Medio Ambiente</td>
                <td class="currency total-cell">480,00 €</td>
            </tr>
        </tbody>
        <tbody class="table-totals">
            <tr>
                <td colspan="8">BASE IMPONIBLE OPCIÓN A (PVC 76 MM):</td>
                <td class="currency">17.935,00 €</td>
            </tr>
            <tr>
                <td colspan="8">I.V.A. RÉGIMEN GENERAL (21%):</td>
                <td class="currency">3.766,35 €</td>
            </tr>
            <tr class="grand-total">
                <td colspan="8">TOTAL OPCIÓN A - PVC (I.V.A. INCLUIDO):</td>
                <td class="currency">21.701,35 €</td>
            </tr>
        </tbody>
    </table>

    <!-- DESGLOSE DETALLADO OPCIÓN B: ALUMINIO RPT -->
    <h2>4. Desglose Detallado por Hueco · Opción B: Aluminio con RPT (Sistemas CORTIZO)</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 32px; text-align: center;">Ref</th>
                <th style="width: 65px;">Planta</th>
                <th style="width: 80px; text-align: center;">Medidas</th>
                <th style="width: 25px; text-align: center;">Ud</th>
                <th>Descripción Técnica, Vidrio y Apertura</th>
                <th style="text-align: right; width: 68px;">Suministro</th>
                <th style="text-align: right; width: 55px;">Retirada</th>
                <th style="text-align: right; width: 65px;">Instalación</th>
                <th style="text-align: right; width: 75px;">Total Hueco</th>
            </tr>
        </thead>
        <tbody>
            {alu_rows_html}
            <tr>
                <td colspan="5" style="text-align: right; font-weight: bold; background: #f8fafc;">Transporte especializado taller (Sant Lluís) - Son Xoriguer y canon oficial de gestión de residuos:</td>
                <td colspan="3" class="currency" style="background: #f8fafc;">Logística y Medio Ambiente</td>
                <td class="currency total-cell">480,00 €</td>
            </tr>
        </tbody>
        <tbody class="table-totals">
            <tr>
                <td colspan="8">BASE IMPONIBLE OPCIÓN B (ALUMINIO RPT):</td>
                <td class="currency">18.475,00 €</td>
            </tr>
            <tr>
                <td colspan="8">I.V.A. RÉGIMEN GENERAL (21%):</td>
                <td class="currency">3.879,75 €</td>
            </tr>
            <tr class="grand-total">
                <td colspan="8">TOTAL OPCIÓN B - ALUMINIO RPT (I.V.A. INCLUIDO):</td>
                <td class="currency">22.354,75 €</td>
            </tr>
        </tbody>
    </table>

    <!-- CONDICIONES Y PLAZOS PARA TERMINAR EN ABRIL 2027 -->
    <div class="conditions">
        <strong>Condiciones Técnicas, Plazos y Planificación (Finalización en Abril de 2027):</strong>
        <ul>
            <li><strong>Medición definitiva en Son Xoriguer:</strong> Nuestro responsable técnico se desplazará a la vivienda en Ciutadella en cuanto la albañilería tenga definidos los huecos para ratificar cotas al milímetro y elaborar la plantilla física de la V6 sin coste.</li>
            <li><strong>Plazos de fabricación:</strong> Estimados en <strong>6 a 8 semanas</strong> debido a los tratamientos bicolores y vidrios laminados con gas argón y control solar.</li>
            <li><strong>Cronograma propuesto:</strong> Toma de medidas definitiva entre <strong>enero y febrero de 2027</strong>; fabricación en taller durante <strong>febrero y marzo</strong>; instalación y remates en obra en <strong>marzo / primera quincena de abril de 2027</strong> (3-4 días de montaje). Se asegura holgadamente el plazo de finalización de abril de 2027.</li>
            <li><strong>Forma de pago:</strong> 40% al encargo y replanteo de medidas, 40% a la recepción del material en taller y 20% a la terminación y ajuste en obra.</li>
            <li><strong>Exclusiones expresas:</strong> No se incluye obra civil, picado/reconstrucción de albañilería en mochetas ni pintura de paramentos.</li>
        </ul>
    </div>

    <!-- FIRMAS -->
    <div class="signatures">
        <div class="sig-block">
            <strong>Por ALUFAC (Dixis Recursos y Soluciones S.L.)</strong><br>
            Pablo Sebastián Sánchez Arnoletto<br>
            Responsable de Fabricación e Instalación
        </div>
        <div class="sig-block">
            <strong>Conforme la Propiedad</strong><br>
            Eduardo Moratalla / Karin Eckhard<br>
            Fecha: _____ / _____ / 2026
        </div>
    </div>

</body>
</html>
"""

    with open(cliente_html_path, "w", encoding="utf-8") as f:
        f.write(html_cliente)
    print(f"HTML cliente guardado: {cliente_html_path}")

    # 2. HTML TÉCNICO INTERNO
    html_tecnico = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Informe Técnico Interno P-2026-0053 · ALUFAC</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 14mm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 8.5pt;
            line-height: 1.4;
            color: #1e293b;
            margin: 0;
            padding: 0;
            background: #ffffff;
        }}
        .header {{
            border-bottom: 2px solid #0f172a;
            padding-bottom: 10px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
        }}
        .brand h1 {{
            font-size: 16pt;
            margin: 0;
            color: #0f172a;
        }}
        .badge {{
            background: #fee2e2;
            color: #991b1b;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 8pt;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 8pt;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 5px 8px;
        }}
        th {{
            background: #0f172a;
            color: #ffffff;
            font-weight: 600;
        }}
        .currency {{ text-align: right; font-variant-numeric: tabular-nums; }}
        .center {{ text-align: center; }}
        .total-row td {{
            font-weight: 700;
            background: #f1f5f9;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin: 15px 0;
        }}
        .kpi-card {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 10px;
            text-align: center;
        }}
        .kpi-card .val {{
            font-size: 14pt;
            font-weight: 800;
            color: #0284c7;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">
            <h1>ALUFAC · Escandallo Técnico de Costes y Rentabilidad</h1>
            <p style="margin: 3px 0 0 0; color: #64748b; font-size: 8.5pt;">Expediente: P-2026-0053 · Reforma CASA 7 (Son Xoriguer, Ciutadella) · Cliente: Eduardo Moratalla</p>
        </div>
        <div style="text-align: right;">
            <span class="badge">CONFIDENCIAL · USO INTERNO</span><br>
            <small style="color: #64748b;">Fecha: 3 de noviembre de 2026</small>
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div>Coste Técnico Directo</div>
            <div class="val" style="color: #b91c1c;">10.428,60 €</div>
        </div>
        <div class="kpi-card">
            <div>Venta Neta (Opción PVC)</div>
            <div class="val" style="color: #0369a1;">17.935,00 €</div>
        </div>
        <div class="kpi-card">
            <div>Margen Bruto (€)</div>
            <div class="val" style="color: #15803d;">7.506,40 €</div>
        </div>
        <div class="kpi-card">
            <div>Margen Bruto (%)</div>
            <div class="val" style="color: #15803d;">41,9 %</div>
        </div>
    </div>

    <h3>1. Desglose de Escandallo de Materiales y Tiempos de Mano de Obra</h3>
    <table>
        <thead>
            <tr>
                <th>Capítulo de Coste</th>
                <th>Detalle Técnico y Suministros</th>
                <th class="center">Medición</th>
                <th class="center">Ud</th>
                <th class="currency">Coste Ud.</th>
                <th class="currency">Subtotal (€)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Perfiles y refuerzos</strong></td>
                <td>Sistemas multicámara 76 mm con refuerzo galvanizado y foliado roble dorado ext</td>
                <td class="center">240,0</td>
                <td class="center">kg</td>
                <td class="currency">8,80 €</td>
                <td class="currency">2.112,00 €</td>
            </tr>
            <tr>
                <td><strong>Vidrios seguridad y acústicos</strong></td>
                <td>6 templado / c16 argón 90% / 44.2 laminado bajo emisivo con warm-edge</td>
                <td class="center">17,2</td>
                <td class="center">m²</td>
                <td class="currency">115,00 €</td>
                <td class="currency">1.978,00 €</td>
            </tr>
            <tr>
                <td><strong>Vidrios control solar V8</strong></td>
                <td>6 templado control solar selectivo / c16 argón / 44.2 bajo emisivo</td>
                <td class="center">3,9</td>
                <td class="center">m²</td>
                <td class="currency">155,00 €</td>
                <td class="currency">604,50 €</td>
            </tr>
            <tr>
                <td><strong>Herrajes perimetrales</strong></td>
                <td>Cremonas, compases oscilobatientes y cerraderos anticorrosivos balear Grado 5</td>
                <td class="center">13,0</td>
                <td class="center">cjto</td>
                <td class="currency">72,00 €</td>
                <td class="currency">936,00 €</td>
            </tr>
            <tr>
                <td><strong>Barrotillos Helima en cámara</strong></td>
                <td>Barrotillo 18×8 mm bicolor montado en cámara de 16 mm con cruces y sujeciones</td>
                <td class="center">18,0</td>
                <td class="center">m</td>
                <td class="currency">18,50 €</td>
                <td class="currency">333,00 €</td>
            </tr>
            <tr>
                <td><strong>Solera telescópica y arco V6</strong></td>
                <td>Mecanizado y curvado especial CNC en dintel y carril embutido con drenaje</td>
                <td class="center">1,0</td>
                <td class="center">ud</td>
                <td class="currency">950,00 €</td>
                <td class="currency">950,00 €</td>
            </tr>
            <tr>
                <td><strong>Mano de Obra Taller ALUFAC</strong></td>
                <td>Corte, termosoldadura, herraje, engomado, acristalado y control calidad (35 €/h)</td>
                <td class="center">62,0</td>
                <td class="center">h</td>
                <td class="currency">35,00 €</td>
                <td class="currency">2.170,00 €</td>
            </tr>
            <tr>
                <td><strong>Mano de Obra Montaje en Obra</strong></td>
                <td>Desmontaje ventanas previas, aplomado, fijación mecánica, calzos y sellado MS (35 €/h)</td>
                <td class="center">48,0</td>
                <td class="center">h</td>
                <td class="currency">35,00 €</td>
                <td class="currency">1.680,00 €</td>
            </tr>
            <tr>
                <td><strong>Selladores y remates</strong></td>
                <td>Cartuchos polímero MS marino, calzos neopreno, anclajes inox A2 y solapes</td>
                <td class="center">1,0</td>
                <td class="center">pa</td>
                <td class="currency">460,00 €</td>
                <td class="currency">460,00 €</td>
            </tr>
            <tr>
                <td><strong>Logística y gestión de residuos</strong></td>
                <td>Portes taller Sant Lluís - Son Xoriguer (camión carrozado) y canon de reciclaje</td>
                <td class="center">1,0</td>
                <td class="center">pa</td>
                <td class="currency">310,00 €</td>
                <td class="currency">310,00 €</td>
            </tr>
        </tbody>
        <tbody class="total-row">
            <tr>
                <td colspan="5">COSTE TÉCNICO DIRECTO TOTAL:</td>
                <td class="currency" style="color: #b91c1c;">10.428,60 €</td>
            </tr>
            <tr>
                <td colspan="5">VENTA NETA TOTAL (OPCIÓN PVC):</td>
                <td class="currency" style="color: #0369a1;">17.935,00 €</td>
            </tr>
            <tr style="background: #f0fdf4;">
                <td colspan="5">MARGEN BRUTO DE CONTRIBUCIÓN:</td>
                <td class="currency" style="color: #15803d; font-size: 10pt;">7.506,40 € (41,9 %)</td>
            </tr>
        </tbody>
    </table>

    <h3>2. Observaciones de Taller y Riesgos Técnicos</h3>
    <ul style="color: #475569; font-size: 8pt;">
        <li><strong>Arco V6:</strong> El dintel arqueado en PVC con foliado roble exterior requiere termo-conformado mediante plantilla de contrachapado de 10 mm fabricada in situ. Si se fabrica en aluminio con RPT Cortizo, el curvado por rodillos CNC ofrece acabado perfecto y elimina cualquier tensión interna del foliado.</li>
        <li><strong>Vidrios pesados:</strong> Las balconeras B1, B2 y la corredera V6 llevan hojas que superan los 65 kg por el doble laminado 6T/16/44.2. Se precisan ventosas dobles de vacío y equipo de 2 a 3 operarios en el acristalado en obra.</li>
        <li><strong>Control Solar en V8:</strong> Orientación sur en primera planta con alta radiación; el vidrio selectivo templado garantiza el confort interior sin sobrecalentamiento estival.</li>
    </ul>
</body>
</html>
"""

    with open(tecnico_html_path, "w", encoding="utf-8") as f:
        f.write(html_tecnico)
    print(f"HTML técnico guardado: {tecnico_html_path}")

def render_pdfs():
    cliente_html = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    cliente_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    tecnico_html = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    tecnico_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. PDF Cliente
        page1 = browser.new_page()
        page1.goto(f"file:///{cliente_html.replace(os.sep, '/')}")
        page1.pdf(
            path=cliente_pdf,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print(f"PDF cliente guardado: {cliente_pdf}")
        page1.close()

        # 2. PDF Técnico
        page2 = browser.new_page()
        page2.goto(f"file:///{tecnico_html.replace(os.sep, '/')}")
        page2.pdf(
            path=tecnico_pdf,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print(f"PDF técnico guardado: {tecnico_pdf}")
        page2.close()

        browser.close()

if __name__ == "__main__":
    create_excel()
    generate_html_files()
    render_pdfs()
