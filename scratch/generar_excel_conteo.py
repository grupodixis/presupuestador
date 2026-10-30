import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
wb.remove(wb.active)

# Color palette - Corporate Dixis Navy & Steel Blue
HEADER_FILL = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
ACCENT_FILL = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
TOTAL_FILL = PatternFill(start_color="CFDCEE", end_color="CFDCEE", fill_type="solid")
HIGHLIGHT_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

FONT_TITLE = Font(name="Calibri", size=15, bold=True, color="1F497D")
FONT_SUBTITLE = Font(name="Calibri", size=11, italic=True, color="595959")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="1F497D")
FONT_BOLD = Font(name="Calibri", size=10, bold=True)
FONT_REGULAR = Font(name="Calibri", size=10)
FONT_ITALIC = Font(name="Calibri", size=9, italic=True, color="595959")

THIN_BORDER = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
TOTAL_BORDER = Border(
    top=Side(style='thin', color='1F497D'),
    bottom=Side(style='double', color='1F497D')
)

# -------------------------------------------------------------
# SHEET 1: RESUMEN GENERAL VALORADO
# -------------------------------------------------------------
ws_resumen = wb.create_sheet(title="Resumen General")
ws_resumen.views.sheetView[0].showGridLines = True

ws_resumen["B2"] = "PRESUPUESTO VALORADO: ESTRUCTURA, ENVOLVENTE Y CARPINTERÍAS"
ws_resumen["B2"].font = FONT_TITLE
ws_resumen["B3"] = "Nave para Almacén y Oficinas - Av. Santa Marianna 11-13 (Alaior, Menorca) | Obres Gabi Gonyalons S.L.U."
ws_resumen["B3"].font = FONT_SUBTITLE

headers_res = ["Capítulo / Subcapítulo", "Descripción del Trabajo", "Unidad", "Medición Total", "Observaciones principales", "Unitario", "SubTotal"]
for col_num, h in enumerate(headers_res, start=2):
    cell = ws_resumen.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center" if col_num in [4, 7, 8] else "left", vertical="center")

# Rows definition: (Code, Desc, Ud, Qty, Obs, Unitario, Subtotal, is_section_header)
rows_resumen = [
    ("1.3", "ESTRUCTURA METÁLICA (ACERO)", "Kg", 36987.92, "Pórticos IPE 360, pilares HEA 240/320, correas CF y pletinas FL", 5.00, "=E6*G6", True),
    ("  1.3.1", "Acero conformado en frío serie C (Correas de cubierta CF-250x2.5)", "Kg", 4008.34, "84 piezas en cubierta faldones norte y sur", None, None, False),
    ("  1.3.2", "Acero laminado en caliente serie HEA (Pilares HEA 240 y HEA 320)", "Kg", 16639.85, "27 posiciones de pilares en perímetro e interior", None, None, False),
    ("  1.3.3", "Acero laminado en caliente serie IPE (Vigas pórticos y altillos IPE 180 a 360)", "Kg", 15401.73, "Pórticos de cubierta, vigas de forjado y dinteles", None, None, False),
    ("  1.3.4", "Acero laminado pletinas y uniones (Cruces de San Andrés, cartelas y rigidizadores)", "Kg", 938.00, "Rigidizadores y arriostramientos de nave", None, None, False),
    ("", "", "", "", "", None, None, False),
    ("1.8", "CARPINTERÍAS EXTERIORES, INTERIORES Y MAMPARAS", "Ud", 51.00, "Conteo detallado de plano de carpinterias nº 11", None, "=H13+H14", True),
    ("  1.8.1", "Carpintería exterior de aluminio y lamas (Puertas correderas, ventanas y claraboyas)", "Ud", 37.00, "2 puertas correderas 4x3.5m, 23 ventanas batientes/oscilobatientes y 12 claraboyas", None, 22650.00, False),
    ("  1.8.2", "Carpintería interior y mamparas de baño (Puertas batientes roble, correderas y mamparas)", "Ud", 14.00, "9 puertas batientes roble, 3 correderas ocultas y 2 mamparas dobles inox", None, 6750.00, False),
    ("", "", "", "", "", None, None, False),
    ("2.0", "PANELES DE CUBIERTA Y FACHADAS", "m²", 1073.62, "Cerramiento sándwich PUR en fachada y acústico en cubierta", None, "=H17+H18+H19", True),
    ("  2.1", "Fachada de paneles sándwich PUR 50 mm (Fijación oculta, chapa prelacada)", "m²", 346.87, "Franjas superiores en alzados de la nave", 110.00, "=E17*G17", False),
    ("  2.2", "Cobertura de paneles sándwich acústicos e=100 mm (Lana roca 95 kg/m³ fonoabsorbente)", "m²", 711.75, "Cubierta a dos aguas sobre correas CF-250x2.5", 175.00, "=E18*G18", False),
    ("  2.3", "Lucernarios de cubierta en policarbonato celular e=30 mm", "m²", 15.00, "12 unidades de lucernario de 1.00 x 1.20 m (~14.40 m² redondeado)", 176.00, "=E19*G19", False),
]

row_idx = 6
for row in rows_resumen:
    c_code, c_desc, c_ud, c_qty, c_obs, c_unit, c_sub, is_sec = row
    if c_code == "":
        row_idx += 1
        continue
    
    c1 = ws_resumen.cell(row=row_idx, column=2, value=c_code)
    c2 = ws_resumen.cell(row=row_idx, column=3, value=c_desc)
    c3 = ws_resumen.cell(row=row_idx, column=4, value=c_ud)
    c4 = ws_resumen.cell(row=row_idx, column=5, value=c_qty)
    c5 = ws_resumen.cell(row=row_idx, column=6, value=c_obs)
    c6 = ws_resumen.cell(row=row_idx, column=7, value=c_unit)
    c7 = ws_resumen.cell(row=row_idx, column=8, value=c_sub)
    
    for c in [c1, c2, c3, c4, c5, c6, c7]:
        c.font = FONT_SECTION if is_sec else FONT_REGULAR
        c.border = THIN_BORDER
        if is_sec:
            c.fill = SUBHEADER_FILL
    
    c1.alignment = Alignment(horizontal="left", vertical="center")
    c2.alignment = Alignment(horizontal="left", vertical="center")
    c3.alignment = Alignment(horizontal="center", vertical="center")
    c4.alignment = Alignment(horizontal="right", vertical="center")
    c5.alignment = Alignment(horizontal="left", vertical="center")
    c6.alignment = Alignment(horizontal="right", vertical="center")
    c7.alignment = Alignment(horizontal="right", vertical="center")

    if isinstance(c_qty, (int, float)):
        c4.number_format = '#,##0.00' if isinstance(c_qty, float) else '#,##0'
    if c_unit is not None:
        c6.number_format = '#,##0.00 €'
    if c_sub is not None:
        c7.number_format = '#,##0.00 €'
    
    row_idx += 1

# Gran Total PEM
row_idx += 1
tot_label = ws_resumen.cell(row=row_idx, column=6, value="TOTAL PRESUPUESTO EJECUCIÓN MATERIAL (PEM):")
tot_label.font = FONT_TITLE
tot_label.alignment = Alignment(horizontal="right", vertical="center")
tot_label.fill = TOTAL_FILL

tot_val = ws_resumen.cell(row=row_idx, column=8, value="=H6+H12+H16")
tot_val.font = FONT_TITLE
tot_val.alignment = Alignment(horizontal="right", vertical="center")
tot_val.fill = TOTAL_FILL
tot_val.border = TOTAL_BORDER
tot_val.number_format = '#,##0.00 €'

# -------------------------------------------------------------
# SHEET 2: 1.3 ACERO (ESTRUCTURA METÁLICA)
# -------------------------------------------------------------
ws_acero = wb.create_sheet(title="1.3 Estructura Metálica")
ws_acero.views.sheetView[0].showGridLines = True

ws_acero["B2"] = "SUBCAPÍTULO 1.3 - ESTRUCTURA METÁLICA (ACERO)"
ws_acero["B2"].font = FONT_TITLE
ws_acero["B3"] = "Desglose por perfiles según modelo CYPECAD y planos E01 a E10 | Alaior"
ws_acero["B3"].font = FONT_SUBTITLE

headers_acero = ["Partida", "Descripción Técnica y Tipo de Perfil", "Norma / Calidad", "Tipo de Elementos", "Uds.", "Peso Total (Kg)", "Precio Unitario (€/kg)", "Importe Total (€)"]
for col_num, h in enumerate(headers_acero, start=2):
    cell = ws_acero.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")

data_acero = [
    ("1.3.1", "Perfiles conformados en frío serie C (CF-250x2.5)", "UNE-EN 10025 S235JR", "Correas de cubierta faldones flector/apoyo", 84, 4008.34, 5.00, "=G6*H6"),
    ("1.3.2", "Perfiles laminados en caliente serie HEA (HEA 240 / HEA 320)", "UNE-EN 10025 S275JR", "Pilares perimetrales, pilares centrales y arranque", 27, 16639.85, 5.00, "=G7*H7"),
    ("1.3.3", "Perfiles laminados en caliente serie IPE (IPE 180 a IPE 360)", "UNE-EN 10025 S275JR", "Dinteles pórticos cubierta, vigas altillos oficinas y zunchos", 76, 15401.73, 5.00, "=G8*H8"),
    ("1.3.4", "Pletinas laminadas serie FL (FL 35x5 a FL 120x5)", "UNE-EN 10025 S275JR", "Cruces de San Andrés, cartelas, rigidizadores de nudos", 56, 938.00, 5.00, "=G9*H9")
]

row_idx = 6
for row in data_acero:
    for c_i, val in enumerate(row, start=2):
        cell = ws_acero.cell(row=row_idx, column=c_i, value=val)
        cell.font = FONT_REGULAR
        cell.border = THIN_BORDER
        if c_i in [2, 4, 5]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_i == 7:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '#,##0.00'
        elif c_i in [8, 9]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '#,##0.00 €'
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")
    row_idx += 1

# Total Acero
total_cell_lbl = ws_acero.cell(row=row_idx, column=6, value="TOTALES:")
total_cell_lbl.font = FONT_BOLD
total_cell_lbl.alignment = Alignment(horizontal="right", vertical="center")
total_cell_lbl.fill = TOTAL_FILL

tot_kg = ws_acero.cell(row=row_idx, column=7, value="=SUM(G6:G9)")
tot_kg.font = FONT_BOLD
tot_kg.alignment = Alignment(horizontal="right", vertical="center")
tot_kg.number_format = '#,##0.00'
tot_kg.fill = TOTAL_FILL
tot_kg.border = TOTAL_BORDER

tot_avg_price = ws_acero.cell(row=row_idx, column=8, value=5.00)
tot_avg_price.font = FONT_BOLD
tot_avg_price.alignment = Alignment(horizontal="right", vertical="center")
tot_avg_price.number_format = '#,##0.00 €'
tot_avg_price.fill = TOTAL_FILL
tot_avg_price.border = TOTAL_BORDER

tot_eur = ws_acero.cell(row=row_idx, column=9, value="=SUM(I6:I9)")
tot_eur.font = FONT_BOLD
tot_eur.alignment = Alignment(horizontal="right", vertical="center")
tot_eur.number_format = '#,##0.00 €'
tot_eur.fill = TOTAL_FILL
tot_eur.border = TOTAL_BORDER

# -------------------------------------------------------------
# SHEET 3: 1.8 CARPINTERÍAS VALORADA ELEMENTO A ELEMENTO
# -------------------------------------------------------------
ws_carp = wb.create_sheet(title="1.8 Conteo Carpinterías")
ws_carp.views.sheetView[0].showGridLines = True

ws_carp["B2"] = "SUBCAPÍTULO 1.8 - CARPINTERÍAS Y CERRAMIENTOS (PLANO Nº 11)"
ws_carp["B2"].font = FONT_TITLE
ws_carp["B3"] = "Presupuesto detallado por tipo de elemento: Aluminio RPT, lamas ciegas, madera roble y mamparas"
ws_carp["B3"].font = FONT_SUBTITLE

headers_carp = ["Código", "Tipo de Elemento", "Uds.", "Ancho (m)", "Alto (m)", "Superficie Ud (m²)", "Superficie Tot (m²)", "Vidrio / Material / Acabado", "Ubicación en Nave", "Precio Ud (€)", "Importe Total (€)"]
for col_num, h in enumerate(headers_carp, start=2):
    cell = ws_carp.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")

# Carpinterias breakdown with unit prices
carpinterias_detailed = [
    # CARPINTERIA EXTERIOR
    ("CE-01", "Puerta corredera exterior ciega", 2, 4.00, 3.50, 14.00, 28.00, "Aluminio extruido e>=2mm, lamas machihembradas lacado verde", "Fachadas Oeste y Sur (Accesos almacén)", 3900.00),
    ("CE-02", "Balconera / puerta acristalada", 1, 1.00, 2.50, 2.50, 2.50, "Aluminio verde, vidrio 6 + 16 argón + 4 BE bajo emisivo", "Fachada Oeste (Acceso peatonal vestibulo 1)", 820.00),
    ("CE-03", "Balconera / puerta acristalada", 1, 1.00, 2.50, 2.50, 2.50, "Aluminio verde, vidrio 6 + 16 argón + 4 BE bajo emisivo", "Fachada Sur (Acceso peatonal vestibulo 2)", 820.00),
    ("CE-04", "Ventana de oficinas", 1, 2.05, 1.20, 2.46, 2.46, "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Planta Primera oficinas", 710.00),
    ("CE-05", "Ventana de oficinas", 1, 1.70, 1.20, 2.04, 2.04, "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Planta Primera oficinas", 620.00),
    ("CE-06", "Ventana estándar oficinas y nave", 16, 1.20, 1.20, 1.44, 23.04, "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Fachadas Norte, Sur, Este y Oeste", 495.00),
    ("CE-07", "Ventana aseos/distribuidor", 1, 0.70, 1.20, 0.84, 0.84, "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Planta Primera aseos", 360.00),
    ("CE-08", "Ventana alta aseos", 2, 0.50, 1.20, 0.60, 1.20, "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Aseos / vestuarios", 300.00),
    ("CE-09", "Claraboya fija de cubierta", 12, 1.00, 1.20, 1.20, 14.40, "Marco aluminio anodizado + policarbonato termoformado + babeta", "Cubierta inclinada faldones norte y sur", 250.00),
    # CARPINTERIA INTERIOR
    ("CI-01", "Puerta de paso interior batiente", 9, 0.87, 2.05, 1.78, 16.05, "Madera acabado roble, herrajes y tirador inox mate modelo DF", "Oficinas, salas reuniones, archivos y baños", 380.00),
    ("CI-02", "Puerta corredera oculta en tabique", 3, 0.80, 2.05, 1.64, 4.92, "Madera roble, casoneto armazón oculto tipo Maydisa", "Aseos y distribuidores altillos", 630.00),
    # MAMPARAS
    ("MV-01", "Mampara divisoria ducha/aseos", 2, 1.70, 2.00, 3.40, 6.80, "Vidrio templado seguridad, bisagras y herrajes inox", "Baño 1 y Baño 2 planta primera", 720.00)
]

row_idx = 6
row_ext_start = 6
row_ext_end = 14
row_int_start = 16
row_int_end = 18

for idx, item in enumerate(carpinterias_detailed):
    cod, desc, uds, w, h, sup_u, sup_t, mat, ubic, p_unit = item
    
    if cod == "CI-01":
        # Subheading for interior
        sub_cell = ws_carp.cell(row=row_idx, column=2, value="CARPINTERÍA INTERIOR DE MADERA Y MAMPARAS")
        sub_cell.font = FONT_SECTION
        for col in range(2, 13):
            ws_carp.cell(row=row_idx, column=col).fill = SUBHEADER_FILL
            ws_carp.cell(row=row_idx, column=col).border = THIN_BORDER
        row_idx += 1
        row_int_start = row_idx

    c_cod = ws_carp.cell(row=row_idx, column=2, value=cod)
    c_desc = ws_carp.cell(row=row_idx, column=3, value=desc)
    c_uds = ws_carp.cell(row=row_idx, column=4, value=uds)
    c_w = ws_carp.cell(row=row_idx, column=5, value=w)
    c_h = ws_carp.cell(row=row_idx, column=6, value=h)
    c_su = ws_carp.cell(row=row_idx, column=7, value=sup_u)
    c_st = ws_carp.cell(row=row_idx, column=8, value=sup_t)
    c_mat = ws_carp.cell(row=row_idx, column=9, value=mat)
    c_ub = ws_carp.cell(row=row_idx, column=10, value=ubic)
    c_pu = ws_carp.cell(row=row_idx, column=11, value=p_unit)
    c_tot = ws_carp.cell(row=row_idx, column=12, value=f"=D{row_idx}*K{row_idx}")

    for c in [c_cod, c_desc, c_uds, c_w, c_h, c_su, c_st, c_mat, c_ub, c_pu, c_tot]:
        c.font = FONT_REGULAR
        c.border = THIN_BORDER
    
    c_cod.alignment = Alignment(horizontal="center", vertical="center")
    c_desc.alignment = Alignment(horizontal="left", vertical="center")
    c_uds.alignment = Alignment(horizontal="center", vertical="center")
    c_w.alignment = Alignment(horizontal="right", vertical="center")
    c_h.alignment = Alignment(horizontal="right", vertical="center")
    c_su.alignment = Alignment(horizontal="right", vertical="center")
    c_st.alignment = Alignment(horizontal="right", vertical="center")
    c_mat.alignment = Alignment(horizontal="left", vertical="center")
    c_ub.alignment = Alignment(horizontal="left", vertical="center")
    c_pu.alignment = Alignment(horizontal="right", vertical="center")
    c_tot.alignment = Alignment(horizontal="right", vertical="center")

    c_w.number_format = '0.00'
    c_h.number_format = '0.00'
    c_su.number_format = '0.00'
    c_st.number_format = '0.00'
    c_pu.number_format = '#,##0.00 €'
    c_tot.number_format = '#,##0.00 €'
    row_idx += 1

row_int_end = row_idx - 1

# Totals row
row_idx += 1
lbl_tot = ws_carp.cell(row=row_idx, column=3, value="TOTAL CARPINTERÍAS Y MAMPARAS:")
lbl_tot.font = FONT_BOLD
lbl_tot.alignment = Alignment(horizontal="right", vertical="center")
lbl_tot.fill = TOTAL_FILL

tot_uds = ws_carp.cell(row=row_idx, column=4, value=f"=SUM(D6:D14)+SUM(D16:D{row_int_end})")
tot_uds.font = FONT_BOLD
tot_uds.alignment = Alignment(horizontal="center", vertical="center")
tot_uds.fill = TOTAL_FILL
tot_uds.border = TOTAL_BORDER

tot_st = ws_carp.cell(row=row_idx, column=8, value=f"=SUM(H6:H14)+SUM(H16:H{row_int_end})")
tot_st.font = FONT_BOLD
tot_st.alignment = Alignment(horizontal="right", vertical="center")
tot_st.number_format = '0.00'
tot_st.fill = TOTAL_FILL
tot_st.border = TOTAL_BORDER

tot_imp = ws_carp.cell(row=row_idx, column=12, value=f"=SUM(L6:L14)+SUM(L16:L{row_int_end})")
tot_imp.font = FONT_BOLD
tot_imp.alignment = Alignment(horizontal="right", vertical="center")
tot_imp.number_format = '#,##0.00 €'
tot_imp.fill = TOTAL_FILL
tot_imp.border = TOTAL_BORDER

# -------------------------------------------------------------
# SHEET 4: CAPÍTULO 2 (PANELES CUBIERTA Y FACHADA)
# -------------------------------------------------------------
ws_paneles = wb.create_sheet(title="2.0 Paneles y Cubierta")
ws_paneles.views.sheetView[0].showGridLines = True

ws_paneles["B2"] = "CAPÍTULO 2 - PANELES DE CUBIERTA Y FACHADAS"
ws_paneles["B2"].font = FONT_TITLE
ws_paneles["B3"] = "Presupuesto valorado de envolvente ligera con paneles sándwich y lucernarios"
ws_paneles["B3"].font = FONT_SUBTITLE

headers_paneles = ["Partida", "Descripción de la Unidad", "Unidad", "Medición", "Precio Unitario (€)", "Importe Total (€)", "Espesor / Núcleo", "Acabado Chapa Ext. / Int.", "Detalle de Medición en Proyecto"]
for col_num, h in enumerate(headers_paneles, start=2):
    cell = ws_paneles.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")

data_paneles = [
    ("2.1", "Fachada de paneles sándwich PUR 50 mm con fijación oculta", "m²", 346.87, 110.00, "=E6*F6", "50 mm (Poliuretano densidad media 40 kg/m³, B-s1,d0)", "Chapa ext. 0.5 mm semilisa poliéster / Chapa int. 0.5 mm nervada", "Franja alzado este (171.57 m²) + Franja alzado oeste (175.30 m²)"),
    ("2.2", "Cobertura de paneles sándwich acústicos lana de roca 100 mm", "m²", 711.75, 175.00, "=E7*F7", "100 mm (Lana de roca 95 kg/m³, A2-s1,d0, Rw 35 dB)", "Chapa ext. 0.5 mm grecada (5 grecas) / Chapa int. 0.5 mm microperforada acústica", "Cubierta faldones inclinados nave pendiente >10% (711.75 m²)"),
    ("2.3", "Lucernario a un agua en cubierta con placas policarbonato celular", "m²", 15.00, 176.00, "=E8*F8", "30 mm (Policarbonato celular translúcido con accesorios fijación y sellado)", "Placas planas translúcidas de alta resistencia al impacto y protección UV", "12 claraboyas CE-09 de 1.00x1.20 m sobre cubierta (14.40 m² ~ 15 m²)")
]

row_idx = 6
for row in data_paneles:
    for c_i, val in enumerate(row, start=2):
        cell = ws_paneles.cell(row=row_idx, column=c_i, value=val)
        cell.font = FONT_REGULAR
        cell.border = THIN_BORDER
        if c_i in [2, 4]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_i == 5:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '#,##0.00'
        elif c_i in [6, 7]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '#,##0.00 €'
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")
    row_idx += 1

tot_p = ws_paneles.cell(row=row_idx, column=4, value="TOTAL ENVOLVENTE LIGERA:")
tot_p.font = FONT_BOLD
tot_p.alignment = Alignment(horizontal="right", vertical="center")
tot_p.fill = TOTAL_FILL

tot_p_v = ws_paneles.cell(row=row_idx, column=5, value="=SUM(E6:E8)")
tot_p_v.font = FONT_BOLD
tot_p_v.alignment = Alignment(horizontal="right", vertical="center")
tot_p_v.number_format = '#,##0.00'
tot_p_v.fill = TOTAL_FILL
tot_p_v.border = TOTAL_BORDER

tot_p_eur = ws_paneles.cell(row=row_idx, column=7, value="=SUM(G6:G8)")
tot_p_eur.font = FONT_BOLD
tot_p_eur.alignment = Alignment(horizontal="right", vertical="center")
tot_p_eur.number_format = '#,##0.00 €'
tot_p_eur.fill = TOTAL_FILL
tot_p_eur.border = TOTAL_BORDER

# Auto-adjust column widths
for ws in [ws_resumen, ws_acero, ws_carp, ws_paneles]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        if col[0].column == 1:
            ws.column_dimensions[col_letter].width = 4
            continue
        for cell in col:
            if cell.row in [2, 3]:
                continue
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 58)

output_path = r"c:\Users\pablo\Documents\Presupuestador\presupuestos\Presupuesto_Alaior_Estructura_Paneles_Carpinterias.xlsx"
wb.save(output_path)
print(f"Excel guardado exitosamente en: {output_path}")
