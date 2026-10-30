import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
# Remove default sheet
wb.remove(wb.active)

# Color palette
HEADER_FILL = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid") # Dark Navy Blue
SUBHEADER_FILL = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid") # Soft blue
ACCENT_FILL = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid") # Light zebra
TOTAL_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")

FONT_TITLE = Font(name="Calibri", size=15, bold=True, color="1F497D")
FONT_SUBTITLE = Font(name="Calibri", size=11, italic=True, color="595959")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="1F497D")
FONT_BOLD = Font(name="Calibri", size=10, bold=True)
FONT_REGULAR = Font(name="Calibri", size=10)

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
# SHEET 1: RESUMEN EJECUTIVO
# -------------------------------------------------------------
ws_resumen = wb.create_sheet(title="Resumen General")
ws_resumen.views.sheetView[0].showGridLines = True

ws_resumen["B2"] = "ESTUDIO DE MEDICIONES Y CONTEO DE PARTIDAS"
ws_resumen["B2"].font = FONT_TITLE
ws_resumen["B3"] = "Nave para Almacén y Oficinas - Av. Santa Marianna 11-13 (Alaior, Menorca) | Obres Gabi Gonyalons S.L.U."
ws_resumen["B3"].font = FONT_SUBTITLE

headers_res = ["Capítulo / Subcapítulo", "Descripción del Trabajo", "Unidad", "Medición Total", "Observaciones principales"]
for col_num, h in enumerate(headers_res, start=2):
    cell = ws_resumen.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center" if col_num in [4, 5] else "left", vertical="center")

data_resumen = [
    ("1.3", "ESTRUCTURA METÁLICA (ACERO)", "Kg", 36987.92, "Pórticos IPE 360, pilares HEA 240/320, correas CF y pletinas FL"),
    ("  1.3.1", "Acero conformado en frío serie C (Correas de cubierta CF-250x2.5)", "Kg", 4008.34, "84 piezas en cubierta faldones norte y sur"),
    ("  1.3.2", "Acero laminado en caliente serie HEA (Pilares HEA 240 y HEA 320)", "Kg", 16639.85, "27 posiciones de pilares en perímetro e interior"),
    ("  1.3.3", "Acero laminado en caliente serie IPE (Vigas pórticos y altillos IPE 180 a 360)", "Kg", 15401.73, "Pórticos de cubierta, vigas de forjado y dinteles"),
    ("  1.3.4", "Acero laminado pletinas y uniones (Cruces de San Andrés, cartelas y rigidizadores)", "Kg", 938.00, "Rigidizadores y arriostramientos de nave"),
    ("", "", "", "", ""),
    ("1.8", "CARPINTERÍAS EXTERIORES, INTERIORES Y MAMPARAS", "Ud", 51.00, "Conteo detallado de plano de carpinterías nº 11"),
    ("  1.8.1", "Carpintería exterior de aluminio y lamas (Puertas correderas, ventanas y claraboyas)", "Ud", 37.00, "2 puertas correderas 4x3.5m, 23 ventanas batientes/oscilobatientes y 12 claraboyas"),
    ("  1.8.2", "Carpintería interior y mamparas de baño (Puertas batientes roble, correderas y mamparas)", "Ud", 14.00, "9 puertas batientes roble, 3 correderas ocultas y 2 mamparas dobles inox"),
    ("", "", "", "", ""),
    ("2.0", "PANELES DE CUBIERTA Y FACHADAS", "m²", 1073.62, "Cerramiento sándwich PUR en fachada y acústico en cubierta"),
    ("  2.1", "Fachada de paneles sándwich PUR 50 mm (Fijación oculta, chapa prelacada)", "m²", 346.87, "Franjas superiores en alzados de la nave"),
    ("  2.2", "Cobertura de paneles sándwich acústicos e=100 mm (Lana roca 95 kg/m³ fonoabsorbente)", "m²", 711.75, "Cubierta a dos aguas sobre correas CF-250x2.5"),
    ("  2.3", "Lucernarios de cubierta en policarbonato celular e=30 mm", "m²", 15.00, "12 unidades de lucernario de 1.00 x 1.20 m (~14.40 m² redondeado)"),
]

row_idx = 6
for row in data_resumen:
    c_code, c_desc, c_ud, c_qty, c_obs = row
    if c_code == "":
        row_idx += 1
        continue
    is_main = not c_code.startswith("  ")
    c1 = ws_resumen.cell(row=row_idx, column=2, value=c_code)
    c2 = ws_resumen.cell(row=row_idx, column=3, value=c_desc)
    c3 = ws_resumen.cell(row=row_idx, column=4, value=c_ud)
    c4 = ws_resumen.cell(row=row_idx, column=5, value=c_qty)
    c5 = ws_resumen.cell(row=row_idx, column=6, value=c_obs)
    
    for c in [c1, c2, c3, c4, c5]:
        c.font = FONT_SECTION if is_main else FONT_REGULAR
        c.border = THIN_BORDER
        if is_main:
            c.fill = SUBHEADER_FILL
    
    c1.alignment = Alignment(horizontal="left", vertical="center")
    c2.alignment = Alignment(horizontal="left", vertical="center")
    c3.alignment = Alignment(horizontal="center", vertical="center")
    c4.alignment = Alignment(horizontal="right", vertical="center")
    c5.alignment = Alignment(horizontal="left", vertical="center")
    if isinstance(c_qty, (int, float)):
        c4.number_format = '#,##0.00' if isinstance(c_qty, float) else '#,##0'
    row_idx += 1

# -------------------------------------------------------------
# SHEET 2: 1.3 ACERO (ESTRUCTURA METÁLICA)
# -------------------------------------------------------------
ws_acero = wb.create_sheet(title="1.3 Estructura Metálica")
ws_acero.views.sheetView[0].showGridLines = True

ws_acero["B2"] = "SUBCAPÍTULO 1.3 - ESTRUCTURA METÁLICA (ACERO)"
ws_acero["B2"].font = FONT_TITLE
ws_acero["B3"] = "Desglose por tipo de perfil, serie y ubicación estructural"
ws_acero["B3"].font = FONT_SUBTITLE

headers_acero = ["Partida", "Descripción Técnica y Tipo de Perfil", "Norma / Calidad", "Tipo de Elementos", "Uds.", "Peso Total (Kg)", "Ratio / Observaciones"]
for col_num, h in enumerate(headers_acero, start=2):
    cell = ws_acero.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")

data_acero = [
    ("1.3.1", "Perfiles conformados en frío serie C (CF-250x2.5)", "UNE-EN 10025 S235JR", "Correas de cubierta faldones flector/apoyo", 84, 4008.34, "Piezas de ~47.8 a ~48.06 kg c/u"),
    ("1.3.2", "Perfiles laminados en caliente serie HEA (HEA 240 / HEA 320)", "UNE-EN 10025 S275JR", "Pilares perimetrales, pilares centrales y arranque", 27, 16639.85, "Pilares P1 a P27 con placas y cartelas"),
    ("1.3.3", "Perfiles laminados en caliente serie IPE (IPE 180 a IPE 360)", "UNE-EN 10025 S275JR", "Dinteles pórticos cubierta, vigas altillos oficinas y zunchos", 76, 15401.73, "Pórticos tipo IPE 360, vigas IPE 330/270/220/180"),
    ("1.3.4", "Pletinas laminadas serie FL (FL 35x5 a FL 120x5)", "UNE-EN 10025 S275JR", "Cruces de San Andrés, cartelas, rigidizadores de nudos", 56, 938.00, "Arriostramientos en planos E04, E05, E06, E07")
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
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")
    row_idx += 1

# Total Acero
total_cell_lbl = ws_acero.cell(row=row_idx, column=6, value="TOTAL ACERO ESTRUCTURAL (Kg):")
total_cell_lbl.font = FONT_BOLD
total_cell_lbl.alignment = Alignment(horizontal="right", vertical="center")
total_cell_lbl.fill = TOTAL_FILL

total_cell_val = ws_acero.cell(row=row_idx, column=7, value=36987.92)
total_cell_val.font = FONT_BOLD
total_cell_val.alignment = Alignment(horizontal="right", vertical="center")
total_cell_val.number_format = '#,##0.00'
total_cell_val.fill = TOTAL_FILL
total_cell_val.border = TOTAL_BORDER

# -------------------------------------------------------------
# SHEET 3: 1.8 CARPINTERÍAS (CONTEO DE PLANO Nº 11)
# -------------------------------------------------------------
ws_carp = wb.create_sheet(title="1.8 Conteo Carpinterías")
ws_carp.views.sheetView[0].showGridLines = True

ws_carp["B2"] = "SUBCAPÍTULO 1.8 - CARPINTERÍAS Y CERRAMIENTOS (PLANO Nº 11)"
ws_carp["B2"].font = FONT_TITLE
ws_carp["B3"] = "Conteo detallado de carpinterías exteriores (aluminio), interiores (madera roble) y mamparas"
ws_carp["B3"].font = FONT_SUBTITLE

headers_carp = ["Código", "Tipo de Elemento", "Uds.", "Ancho (m)", "Alto (m)", "Superficie Ud (m²)", "Superficie Tot (m²)", "Tipo de Apertura / Mecanismo", "Vidrio / Material / Acabado", "Ubicación en Nave"]
for col_num, h in enumerate(headers_carp, start=2):
    cell = ws_carp.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")

carpinterias_data = [
    # CARPINTERIA EXTERIOR
    ("CE-01", "Puerta corredera exterior ciega", 2, 4.00, 3.50, 14.00, 28.00, "1 hoja corredera", "Aluminio extruido e>=2mm, lamas machihembradas ciegas lacado verde", "Fachadas Oeste y Sur (Accesos nave/vehículos)"),
    ("CE-02", "Balconera / puerta acristalada", 1, 1.00, 2.50, 2.50, 2.50, "1 hoja batiente + 1 hoja fija", "Aluminio verde, vidrio 6 + 16 argón + 4 BE bajo emisivo", "Fachada Oeste (Acceso peatonal vestibulo 1)"),
    ("CE-03", "Balconera / puerta acristalada", 1, 1.00, 2.50, 2.50, 2.50, "1 hoja batiente + 1 hoja fija", "Aluminio verde, vidrio 6 + 16 argón + 4 BE bajo emisivo", "Fachada Sur (Acceso peatonal vestibulo 2)"),
    ("CE-04", "Ventana de oficinas", 1, 2.05, 1.20, 2.46, 2.46, "2 hojas batientes (1.02+1.02m)", "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Planta Primera oficinas"),
    ("CE-05", "Ventana de oficinas", 1, 1.70, 1.20, 2.04, 2.04, "2 hojas batientes (0.85+0.85m)", "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Planta Primera oficinas"),
    ("CE-06", "Ventana estándar oficinas y nave", 16, 1.20, 1.20, 1.44, 23.04, "2 hojas batientes (0.60+0.60m)", "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Fachadas Norte, Sur, Este y Oeste (Oficinas/Nave)"),
    ("CE-07", "Ventana aseos/distribuidor", 1, 0.70, 1.20, 0.84, 0.84, "1 hoja oscilobatiente", "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Planta Primera aseos"),
    ("CE-08", "Ventana alta aseos", 2, 0.50, 1.20, 0.60, 1.20, "1 hoja oscilobatiente + fijo sup 0.5m", "Aluminio verde, vidrio 6 + 16 argón + 4 BE", "Aseos / vestuarios"),
    ("CE-09", "Claraboya fija de cubierta", 12, 1.00, 1.20, 1.20, 14.40, "Fija estanca sobre chapa", "Marco aluminio anodizado + paño policarbonato macizo termoformado + babeta", "Cubierta inclinada faldones norte y sur"),
    # CARPINTERIA INTERIOR
    ("CI-01", "Puerta de paso interior", 9, 0.87, 2.05, 1.78, 16.05, "Batiente 1 hoja (paso libre 77 cm)", "Madera acabado roble, herrajes y tirador inox mate modelo DF", "Oficinas, salas reuniones, archivos y baños"),
    ("CI-02", "Puerta corredera oculta", 3, 0.80, 2.05, 1.64, 4.92, "Corredera oculta en tabique (paso 70 cm)", "Madera acabado roble, casoneto armazón oculto tipo Maydisa", "Aseos y distribuidores altillos"),
    # MAMPARAS
    ("MV-01", "Mampara divisoria ducha/aseos", 2, 1.70, 2.00, 3.40, 6.80, "2 hojas (1 fija 1.10m + 1 abatible 0.60m)", "Vidrio templado de seguridad, bisagras y herrajes acero inox", "Baño 1 y Baño 2 planta primera")
]

row_idx = 6
sec_actual = ""
for item in carpinterias_data:
    cod, desc, uds, w, h, sup_u, sup_t, apert, mat, ubic = item
    
    # Header group if starting interior
    if cod == "CI-01":
        # Subheading for interior
        sub_cell = ws_carp.cell(row=row_idx, column=2, value="CARPINTERÍA INTERIOR DE MADERA Y MAMPARAS")
        sub_cell.font = FONT_SECTION
        for col in range(2, 12):
            ws_carp.cell(row=row_idx, column=col).fill = SUBHEADER_FILL
            ws_carp.cell(row=row_idx, column=col).border = THIN_BORDER
        row_idx += 1

    c_cod = ws_carp.cell(row=row_idx, column=2, value=cod)
    c_desc = ws_carp.cell(row=row_idx, column=3, value=desc)
    c_uds = ws_carp.cell(row=row_idx, column=4, value=uds)
    c_w = ws_carp.cell(row=row_idx, column=5, value=w)
    c_h = ws_carp.cell(row=row_idx, column=6, value=h)
    c_su = ws_carp.cell(row=row_idx, column=7, value=sup_u)
    c_st = ws_carp.cell(row=row_idx, column=8, value=sup_t)
    c_ap = ws_carp.cell(row=row_idx, column=9, value=apert)
    c_mat = ws_carp.cell(row=row_idx, column=10, value=mat)
    c_ub = ws_carp.cell(row=row_idx, column=11, value=ubic)

    for c in [c_cod, c_desc, c_uds, c_w, c_h, c_su, c_st, c_ap, c_mat, c_ub]:
        c.font = FONT_REGULAR
        c.border = THIN_BORDER
    
    c_cod.alignment = Alignment(horizontal="center", vertical="center")
    c_desc.alignment = Alignment(horizontal="left", vertical="center")
    c_uds.alignment = Alignment(horizontal="center", vertical="center")
    c_w.alignment = Alignment(horizontal="right", vertical="center")
    c_h.alignment = Alignment(horizontal="right", vertical="center")
    c_su.alignment = Alignment(horizontal="right", vertical="center")
    c_st.alignment = Alignment(horizontal="right", vertical="center")
    c_ap.alignment = Alignment(horizontal="left", vertical="center")
    c_mat.alignment = Alignment(horizontal="left", vertical="center")
    c_ub.alignment = Alignment(horizontal="left", vertical="center")

    c_w.number_format = '0.00'
    c_h.number_format = '0.00'
    c_su.number_format = '0.00'
    c_st.number_format = '0.00'
    row_idx += 1

# Total Carpinterias
row_tot = ws_carp.cell(row=row_idx, column=3, value="TOTAL CARPINTERÍAS Y MAMPARAS (UDS):")
row_tot.font = FONT_BOLD
row_tot.alignment = Alignment(horizontal="right", vertical="center")
row_tot.fill = TOTAL_FILL

tot_val = ws_carp.cell(row=row_idx, column=4, value=51)
tot_val.font = FONT_BOLD
tot_val.alignment = Alignment(horizontal="center", vertical="center")
tot_val.fill = TOTAL_FILL
tot_val.border = TOTAL_BORDER

tot_st = ws_carp.cell(row=row_idx, column=8, value=104.75)
tot_st.font = FONT_BOLD
tot_st.alignment = Alignment(horizontal="right", vertical="center")
tot_st.number_format = '0.00'
tot_st.fill = TOTAL_FILL
tot_st.border = TOTAL_BORDER

# -------------------------------------------------------------
# SHEET 4: CAPÍTULO 2 (PANELES CUBIERTA Y FACHADA)
# -------------------------------------------------------------
ws_paneles = wb.create_sheet(title="2.0 Paneles y Cubierta")
ws_paneles.views.sheetView[0].showGridLines = True

ws_paneles["B2"] = "CAPÍTULO 2 - PANELES DE CUBIERTA Y FACHADAS"
ws_paneles["B2"].font = FONT_TITLE
ws_paneles["B3"] = "Desglose de cerramientos ligeros, cubiertas y lucernarios"
ws_paneles["B3"].font = FONT_SUBTITLE

headers_paneles = ["Partida", "Descripción de la Unidad", "Unidad", "Medición", "Espesor / Núcleo", "Acabado Chapa Ext. / Int.", "Detalle de Medición en Proyecto"]
for col_num, h in enumerate(headers_paneles, start=2):
    cell = ws_paneles.cell(row=5, column=col_num, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")

data_paneles = [
    ("2.1", "Fachada de paneles sándwich PUR 50 mm con fijación oculta", "m²", 346.87, "50 mm (Poliuretano densidad media 40 kg/m³, Euroclase B-s1,d0)", "Chapa ext. 0.5 mm semilisa poliéster / Chapa int. 0.5 mm nervada", "Franja alzado este (171.57 m²) + Franja alzado oeste (175.30 m²)"),
    ("2.2", "Cobertura de paneles sándwich acústicos lana de roca 100 mm", "m²", 711.75, "100 mm (Lana de roca 95 kg/m³, Euroclase A2-s1,d0, Rw 35 dB)", "Chapa ext. 0.5 mm grecada (5 grecas) / Chapa int. 0.5 mm microperforada acústica", "Cubierta faldones inclinados nave pendiente >10% (711.75 m²)"),
    ("2.3", "Lucernario a un agua en cubierta con placas policarbonato celular", "m²", 15.00, "30 mm (Policarbonato celular translúcido con accesorios fijación y sellado)", "Placas planas translúcidas de alta resistencia al impacto y protección UV", "12 claraboyas CE-09 de 1.00x1.20 m sobre cubierta (14.40 m² ~ 15 m²)")
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
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")
    row_idx += 1

tot_p = ws_paneles.cell(row=row_idx, column=4, value="TOTAL SUPERFICIE ENVOLVENTE LIGERA (m²):")
tot_p.font = FONT_BOLD
tot_p.alignment = Alignment(horizontal="right", vertical="center")
tot_p.fill = TOTAL_FILL

tot_p_v = ws_paneles.cell(row=row_idx, column=5, value=1073.62)
tot_p_v.font = FONT_BOLD
tot_p_v.alignment = Alignment(horizontal="right", vertical="center")
tot_p_v.number_format = '#,##0.00'
tot_p_v.fill = TOTAL_FILL
tot_p_v.border = TOTAL_BORDER

# Auto-adjust column widths
for ws in [ws_resumen, ws_acero, ws_carp, ws_paneles]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        if col[0].column == 1:
            ws.column_dimensions[col_letter].width = 4
            continue
        for cell in col:
            # Ignore title rows when calculating width
            if cell.row in [2, 3]:
                continue
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 55)

output_path = r"c:\Users\pablo\Documents\Presupuestador\presupuestos\Medicion_Alaior_Estructura_Paneles_Carpinterias.xlsx"
wb.save(output_path)
print(f"Excel guardado exitosamente en: {output_path}")
