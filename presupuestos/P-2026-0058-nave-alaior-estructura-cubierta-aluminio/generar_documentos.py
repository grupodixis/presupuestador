import json
import os
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def fmt_eur(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_num(val, dec=2):
    return f"{val:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def create_excel():
    wb = Workbook()

    NAVY = "0F172A"
    BLUE = "0369A1"
    GOLD = "B45309"
    SLATE = "F8FAFC"
    SUB = "E2E8F0"
    TOT = "FEF3C7"
    HL = "E0F2FE"
    GREEN = "15803D"
    RED = "B91C1C"

    f_hdr = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    f_sub = PatternFill(start_color=SUB, end_color=SUB, fill_type="solid")
    f_alt = PatternFill(start_color=SLATE, end_color=SLATE, fill_type="solid")
    f_tot = PatternFill(start_color=TOT, end_color=TOT, fill_type="solid")
    f_hl = PatternFill(start_color=HL, end_color=HL, fill_type="solid")

    fn_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    fn_brand = Font(name="Segoe UI", size=9.5, bold=True, color=BLUE)
    fn_hdr = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    fn_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    fn_bold = Font(name="Segoe UI", size=9, bold=True, color="0F172A")
    fn_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    fn_tot = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    fn_tot_b = Font(name="Segoe UI", size=10.5, bold=True, color=BLUE)
    fn_green = Font(name="Segoe UI", size=9, bold=True, color=GREEN)
    fn_red = Font(name="Segoe UI", size=9, bold=True, color=RED)

    b_thin = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )
    b_tot = Border(top=Side(style="thin", color=NAVY), bottom=Side(style="double", color=NAVY))

    NUM_EUR = '#,##0.00 "€"'
    NUM_QTY = "#,##0.00"
    NUM_PCT = "0.00%"

    # ------------------------------------------------------------------
    # HOJA 1: RESUMEN EJECUTIVO
    # ------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Resumen Ejecutivo"
    ws1["B2"] = f"{DATA['emisor']['nombre_comercial'].upper()} · {DATA['emisor']['razon_social']} (CIF {DATA['emisor']['cif']})"
    ws1["B2"].font = fn_brand
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} · NAVE INDUSTRIAL ALAIOR (ESTRUCTURA, CUBIERTA Y ALUMINIO)"
    ws1["B3"].font = fn_title

    meta = [
        ("REFERENCIA:", DATA["referencia"]),
        ("CLIENTE:", DATA["cliente"]["nombre"]),
        ("PROYECTO:", DATA["cliente"]["proyecto"]),
        ("UBICACIÓN:", DATA["cliente"]["ubicacion"]),
        ("TÉCNICO AUTOR:", DATA["cliente"]["tecnico"]),
        ("FECHA / VALIDEZ:", f"{DATA['fecha']} · Validez: {DATA['validez_dias']} días"),
    ]
    for i, (k, v) in enumerate(meta, start=5):
        ws1[f"B{i}"] = k
        ws1[f"B{i}"].font = fn_bold
        ws1[f"C{i}"] = v
        ws1[f"C{i}"].font = fn_reg

    ws1["B12"] = "RESUMEN DE CAPÍTULOS PRESUPUESTADOS"
    ws1["B12"].font = fn_sec

    hdrs = ["Cap.", "Capítulo / Alcance", "Unidad", "Medición", "Base Imponible (€)", "IVA (21%)", "Total c/ IVA (€)"]
    for idx, h in enumerate(hdrs, start=2):
        c = ws1.cell(row=13, column=idx, value=h)
        c.font = fn_hdr
        c.fill = f_hdr
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = b_thin
    ws1.row_dimensions[13].height = 24

    res_rows = [
        ("1", "Estructura Metálica S235JR / S275JR (Medición CYPECAD)", "kg", "='1. Estructura Metálica'!E11", "='1. Estructura Metálica'!G11"),
        ("2A", "Cubierta Panel Sándwich Acústico 100 mm y Lucernarios CE-09", "m²", "='2. Cubierta y Paneles'!E8", "='2. Cubierta y Paneles'!G8"),
        ("2B", "Fachada Panel Sándwich PUR 50 mm Fijación Oculta (Parcial 2.1)", "m²", "='2. Cubierta y Paneles'!E11", "='2. Cubierta y Paneles'!G11"),
        ("3", "Aberturas Exteriores de Aluminio RPT Qualicoat Seaside (Plano 11)", "ud", "='3. Aberturas Aluminio'!E15", "='3. Aberturas Aluminio'!G15"),
    ]
    for offset, (cid, cname, unit, qty_f, imp_f) in enumerate(res_rows):
        r = 14 + offset
        ws1.cell(row=r, column=2, value=cid).alignment = Alignment(horizontal="center")
        ws1.cell(row=r, column=3, value=cname)
        ws1.cell(row=r, column=4, value=unit).alignment = Alignment(horizontal="center")
        c_q = ws1.cell(row=r, column=5, value=qty_f)
        c_q.number_format = NUM_QTY
        c_b = ws1.cell(row=r, column=6, value=imp_f)
        c_b.number_format = NUM_EUR
        c_i = ws1.cell(row=r, column=7, value=f"=ROUND(F{r}*0.21,2)")
        c_i.number_format = NUM_EUR
        c_t = ws1.cell(row=r, column=8, value=f"=F{r}+G{r}")
        c_t.number_format = NUM_EUR
        for col in range(2, 9):
            cell = ws1.cell(row=r, column=col)
            cell.font = fn_reg
            cell.border = b_thin
            if offset % 2 == 1:
                cell.fill = f_alt
        ws1.row_dimensions[r].height = 22

    # Subtotal Alcance A (Sin fachada 2B)
    r_a = 18
    ws1.cell(row=r_a, column=2, value="A")
    ws1.cell(row=r_a, column=3, value="TOTAL SOLO ESTRUCTURA + CUBIERTA (2A) + ALUMINIO (Sin Fachada 2B)")
    ws1.cell(row=r_a, column=4, value="-")
    ws1.cell(row=r_a, column=5, value="-")
    ws1.cell(row=r_a, column=6, value="=F14+F15+F17").number_format = NUM_EUR
    ws1.cell(row=r_a, column=7, value=f"=ROUND(F{r_a}*0.21,2)").number_format = NUM_EUR
    ws1.cell(row=r_a, column=8, value=f"=F{r_a}+G{r_a}").number_format = NUM_EUR
    for col in range(2, 9):
        c = ws1.cell(row=r_a, column=col)
        c.font = fn_bold
        c.fill = f_hl
        c.border = b_thin
    ws1.row_dimensions[r_a].height = 22

    # Total Alcance B (Completo)
    r_b = 19
    ws1.cell(row=r_b, column=2, value="B")
    ws1.cell(row=r_b, column=3, value="TOTAL COMPLETO PRESUPUESTO (CAP. 1 + CAP. 2A + CAP. 2B + CAP. 3)")
    ws1.cell(row=r_b, column=4, value="-")
    ws1.cell(row=r_b, column=5, value="-")
    ws1.cell(row=r_b, column=6, value="=SUM(F14:F17)").number_format = NUM_EUR
    ws1.cell(row=r_b, column=7, value=f"=ROUND(F{r_b}*0.21,2)").number_format = NUM_EUR
    ws1.cell(row=r_b, column=8, value=f"=F{r_b}+G{r_b}").number_format = NUM_EUR
    for col in range(2, 9):
        c = ws1.cell(row=r_b, column=col)
        c.font = fn_tot_b
        c.fill = f_tot
        c.border = b_tot
    ws1.row_dimensions[r_b].height = 26

    # Opcional placas anclaje
    r_opt = 21
    ws1.cell(row=r_opt, column=2, value="OPC")
    ws1.cell(row=r_opt, column=3, value="OPCIONAL 1.3.5: Placas de anclaje a cimentación y pernos DIN 976 (27 pilares, Planos E09-E10)")
    ws1.cell(row=r_opt, column=4, value="kg")
    ws1.cell(row=r_opt, column=5, value=DATA["complementarios_opcionales"][0]["cantidad"]).number_format = NUM_QTY
    ws1.cell(row=r_opt, column=6, value="='1. Estructura Metálica'!G14").number_format = NUM_EUR
    ws1.cell(row=r_opt, column=7, value=f"=ROUND(F{r_opt}*0.21,2)").number_format = NUM_EUR
    ws1.cell(row=r_opt, column=8, value=f"=F{r_opt}+G{r_opt}").number_format = NUM_EUR
    for col in range(2, 9):
        c = ws1.cell(row=r_opt, column=col)
        c.font = fn_reg
        c.fill = f_sub
        c.border = b_thin
    ws1.row_dimensions[r_opt].height = 24

    for col, w in [(1, 3), (2, 8), (3, 56), (4, 8), (5, 13), (6, 18), (7, 15), (8, 18)]:
        ws1.column_dimensions[get_column_letter(col)].width = w

    # ------------------------------------------------------------------
    # HOJA 2: 1. ESTRUCTURA METÁLICA
    # ------------------------------------------------------------------
    ws2 = wb.create_sheet("1. Estructura Metálica")
    ws2["B2"] = "CAPÍTULO 1.3 · ESTRUCTURA METÁLICA (ACERO S235JR / S275JR)"
    ws2["B2"].font = fn_title
    ws2["B3"] = "Mediciones según CYPECAD V2 (260706_Alaior) y Planos E01-E11 · Acabado HAM C4/C5 (imprimación epoxi + poliuretano 2C, secado al aire)"
    ws2["B3"].font = fn_reg

    h2 = ["Código", "Descripción de la Partida", "Perfil / Norma", "Ud.", "Medición", "Precio Unit. (€)", "Subtotal (€)"]
    for idx, h in enumerate(h2, start=2):
        c = ws2.cell(row=5, column=idx, value=h)
        c.font = fn_hdr
        c.fill = f_hdr
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = b_thin
    ws2.row_dimensions[5].height = 24

    cap1 = DATA["capitulos"][0]
    for i, p in enumerate(cap1["partidas"]):
        r = 7 + i
        ws2.cell(row=r, column=2, value=p["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=r, column=3, value=f"{p['concepto']}\n{p['descripcion']}").alignment = Alignment(wrap_text=True, vertical="top")
        ws2.cell(row=r, column=4, value=p["perfil"]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=r, column=5, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        cq = ws2.cell(row=r, column=6, value=p["cantidad"])  # Wait: column 5=Ud, col 6=Medición! Let's fix alignment with col letters!
    # Clean rewrite of ws2 columns so Resumen references match exact columns:
    # B=Código(2), C=Descripción(3), D=Ud.(4), E=Medición(5), F=Precio(6), G=Subtotal(7), H=Perfil(8)
    ws2.delete_rows(5, 10)
    h2_clean = ["Código", "Descripción de la Partida", "Ud.", "Medición", "Precio Unit. (€)", "Subtotal (€)", "Perfil / Serie"]
    for idx, h in enumerate(h2_clean, start=2):
        c = ws2.cell(row=5, column=idx, value=h)
        c.font = fn_hdr
        c.fill = f_hdr
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = b_thin
    ws2.row_dimensions[5].height = 24

    for i, p in enumerate(cap1["partidas"]):
        r = 7 + i
        ws2.cell(row=r, column=2, value=p["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=r, column=3, value=f"{p['concepto']}\n{p['descripcion']}").alignment = Alignment(wrap_text=True, vertical="top")
        ws2.cell(row=r, column=4, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        c_q = ws2.cell(row=r, column=5, value=p["cantidad"])
        c_q.number_format = NUM_QTY
        c_p = ws2.cell(row=r, column=6, value=p["precio_unitario"])
        c_p.number_format = NUM_EUR
        c_s = ws2.cell(row=r, column=7, value=f"=ROUND(E{r}*F{r},2)")
        c_s.number_format = NUM_EUR
        ws2.cell(row=r, column=8, value=p["perfil"]).alignment = Alignment(horizontal="center", vertical="top")
        for col in range(2, 9):
            cell = ws2.cell(row=r, column=col)
            cell.font = fn_reg
            cell.border = b_thin
            if i % 2 == 1:
                cell.fill = f_alt
        ws2.row_dimensions[r].height = 42

    # Row 11: Subtotal Cap 1
    ws2.cell(row=11, column=2, value="TOTAL")
    ws2.cell(row=11, column=3, value="SUBTOTAL CAPÍTULO 1: ESTRUCTURA METÁLICA (MEDICIÓN CYPECAD)")
    ws2.cell(row=11, column=4, value="kg")
    ws2.cell(row=11, column=5, value="=SUM(E7:E10)").number_format = NUM_QTY
    ws2.cell(row=11, column=6, value="=G11/E11").number_format = NUM_EUR
    ws2.cell(row=11, column=7, value="=SUM(G7:G10)").number_format = NUM_EUR
    ws2.cell(row=11, column=8, value="S235 / S275")
    for col in range(2, 9):
        c = ws2.cell(row=11, column=col)
        c.font = fn_tot
        c.fill = f_tot
        c.border = b_tot
    ws2.row_dimensions[11].height = 24

    # Row 13 header opcional + Row 14 opcional
    ws2["B13"] = "PARTIDA COMPLEMENTARIA OPCIONAL (NO MEDIDA EN CSV CYPECAD 1.3.1-1.3.4)"
    ws2["B13"].font = fn_sec
    opt = DATA["complementarios_opcionales"][0]
    ws2.cell(row=14, column=2, value=opt["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
    ws2.cell(row=14, column=3, value=f"{opt['concepto']}\n{opt['descripcion']}").alignment = Alignment(wrap_text=True, vertical="top")
    ws2.cell(row=14, column=4, value=opt["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
    ws2.cell(row=14, column=5, value=opt["cantidad"]).number_format = NUM_QTY
    ws2.cell(row=14, column=6, value=opt["precio_unitario"]).number_format = NUM_EUR
    ws2.cell(row=14, column=7, value="=ROUND(E14*F14,2)").number_format = NUM_EUR
    ws2.cell(row=14, column=8, value="Tipo 4 + 10/11")
    for col in range(2, 9):
        c = ws2.cell(row=14, column=col)
        c.font = fn_reg
        c.fill = f_sub
        c.border = b_thin
    ws2.row_dimensions[14].height = 48

    for col, w in [(1, 3), (2, 12), (3, 62), (4, 8), (5, 14), (6, 15), (7, 16), (8, 22)]:
        ws2.column_dimensions[get_column_letter(col)].width = w

    # ------------------------------------------------------------------
    # HOJA 3: 2. CUBIERTA Y PANELES
    # ------------------------------------------------------------------
    ws3 = wb.create_sheet("2. Cubierta y Paneles")
    ws3["B2"] = "CAPÍTULO 2 · CUBIERTA ACÚSTICA, LUCERNARIOS Y FACHADAS PANEL SÁNDWICH"
    ws3["B2"].font = fn_title
    ws3["B3"] = "Presupuesto Parcial nº 2 (260706_Alaior) · Cubierta 2A (2.2 + 2.3) y Fachada 2B (2.1)"
    ws3["B3"].font = fn_reg

    h3 = ["Código", "Descripción de la Partida", "Ud.", "Medición", "Precio Unit. (€)", "Subtotal (€)", "Especificación"]
    for idx, h in enumerate(h3, start=2):
        c = ws3.cell(row=5, column=idx, value=h)
        c.font = fn_hdr
        c.fill = f_hdr
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = b_thin
    ws3.row_dimensions[5].height = 24

    cap2a = DATA["capitulos"][1]["partidas"]
    for i, p in enumerate(cap2a):
        r = 6 + i
        ws3.cell(row=r, column=2, value=p["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
        ws3.cell(row=r, column=3, value=f"{p['concepto']}\n{p['descripcion']}").alignment = Alignment(wrap_text=True, vertical="top")
        ws3.cell(row=r, column=4, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        ws3.cell(row=r, column=5, value=p["cantidad"]).number_format = NUM_QTY
        ws3.cell(row=r, column=6, value=p["precio_unitario"]).number_format = NUM_EUR
        ws3.cell(row=r, column=7, value=f"=ROUND(E{r}*F{r},2)").number_format = NUM_EUR
        ws3.cell(row=r, column=8, value=p["perfil"]).alignment = Alignment(horizontal="center", vertical="top")
        for col in range(2, 9):
            c = ws3.cell(row=r, column=col)
            c.font = fn_reg
            c.border = b_thin
            if i % 2 == 1:
                c.fill = f_alt
        ws3.row_dimensions[r].height = 54

    # Row 8: Subtotal Cubierta 2A
    ws3.cell(row=8, column=2, value="2A")
    ws3.cell(row=8, column=3, value="SUBTOTAL CUBIERTA (PARTIDAS 2.2 + 2.3)")
    ws3.cell(row=8, column=4, value="m²")
    ws3.cell(row=8, column=5, value="=SUM(E6:E7)").number_format = NUM_QTY
    ws3.cell(row=8, column=6, value="=G8/E8").number_format = NUM_EUR
    ws3.cell(row=8, column=7, value="=SUM(G6:G7)").number_format = NUM_EUR
    ws3.cell(row=8, column=8, value="Cubierta 8%")
    for col in range(2, 9):
        c = ws3.cell(row=8, column=col)
        c.font = fn_bold
        c.fill = f_hl
        c.border = b_thin
    ws3.row_dimensions[8].height = 24

    # Row 10: Fachada 2.1
    p21 = DATA["capitulos"][2]["partidas"][0]
    ws3.cell(row=10, column=2, value=p21["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
    ws3.cell(row=10, column=3, value=f"{p21['concepto']}\n{p21['descripcion']}").alignment = Alignment(wrap_text=True, vertical="top")
    ws3.cell(row=10, column=4, value=p21["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
    ws3.cell(row=10, column=5, value=p21["cantidad"]).number_format = NUM_QTY
    ws3.cell(row=10, column=6, value=p21["precio_unitario"]).number_format = NUM_EUR
    ws3.cell(row=10, column=7, value="=ROUND(E10*F10,2)").number_format = NUM_EUR
    ws3.cell(row=10, column=8, value=p21["perfil"]).alignment = Alignment(horizontal="center", vertical="top")
    for col in range(2, 9):
        c = ws3.cell(row=10, column=col)
        c.font = fn_reg
        c.border = b_thin
    ws3.row_dimensions[10].height = 48

    # Row 11: Subtotal Fachada 2B
    ws3.cell(row=11, column=2, value="2B")
    ws3.cell(row=11, column=3, value="SUBTOTAL FACHADA PANEL SÁNDWICH PUR 50 MM (PARTIDA 2.1)")
    ws3.cell(row=11, column=4, value="m²")
    ws3.cell(row=11, column=5, value="=E10").number_format = NUM_QTY
    ws3.cell(row=11, column=6, value="=F10").number_format = NUM_EUR
    ws3.cell(row=11, column=7, value="=G10").number_format = NUM_EUR
    ws3.cell(row=11, column=8, value="Alzados E y O")
    for col in range(2, 9):
        c = ws3.cell(row=11, column=col)
        c.font = fn_bold
        c.fill = f_sub
        c.border = b_thin
    ws3.row_dimensions[11].height = 24

    # Row 12: Total Cap 2
    ws3.cell(row=12, column=2, value="TOTAL")
    ws3.cell(row=12, column=3, value="TOTAL CAPÍTULO 2 COMPLETO (CUBIERTA + FACHADA PANEL SÁNDWICH)")
    ws3.cell(row=12, column=4, value="m²")
    ws3.cell(row=12, column=5, value="=E8+E11").number_format = NUM_QTY
    ws3.cell(row=12, column=6, value="=G12/E12").number_format = NUM_EUR
    ws3.cell(row=12, column=7, value="=G8+G11").number_format = NUM_EUR
    ws3.cell(row=12, column=8, value="Cap. 2 completo")
    for col in range(2, 9):
        c = ws3.cell(row=12, column=col)
        c.font = fn_tot
        c.fill = f_tot
        c.border = b_tot
    ws3.row_dimensions[12].height = 26

    for col, w in [(1, 3), (2, 10), (3, 64), (4, 8), (5, 14), (6, 15), (7, 16), (8, 22)]:
        ws3.column_dimensions[get_column_letter(col)].width = w

    # ------------------------------------------------------------------
    # HOJA 4: 3. ABERTURAS ALUMINIO
    # ------------------------------------------------------------------
    ws4 = wb.create_sheet("3. Aberturas Aluminio")
    ws4["B2"] = "CAPÍTULO 3 · ABERTURAS Y CARPINTERÍA EXTERIOR DE ALUMINIO (PLANO 11 · PARTIDA 1.8.1)"
    ws4["B2"].font = fn_title
    ws4["B3"] = "Aluminio RPT lacado verde Qualicoat Seaside (Umarco < 1,0 W/m²K) · Vidrio 6/16 Argón/4 Bajo Emisivo Chromatech Ultra (Uvidrio < 0,9 W/m²K)"
    ws4["B3"].font = fn_reg

    h4 = ["Marca", "Descripción y Acabado", "Ud.", "Cantidad", "Precio Unit. (€)", "Subtotal (€)", "Dimensiones / Apertura"]
    for idx, h in enumerate(h4, start=2):
        c = ws4.cell(row=5, column=idx, value=h)
        c.font = fn_hdr
        c.fill = f_hdr
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = b_thin
    ws4.row_dimensions[5].height = 24

    cap3 = DATA["capitulos"][3]
    for i, p in enumerate(cap3["partidas"]):
        r = 7 + i
        ws4.cell(row=r, column=2, value=p["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
        ws4.cell(row=r, column=3, value=f"{p['concepto']}\n{p['descripcion']}").alignment = Alignment(wrap_text=True, vertical="top")
        ws4.cell(row=r, column=4, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        ws4.cell(row=r, column=5, value=p["cantidad"]).number_format = "#,##0"
        ws4.cell(row=r, column=6, value=p["precio_unitario"]).number_format = NUM_EUR
        ws4.cell(row=r, column=7, value=f"=ROUND(E{r}*F{r},2)").number_format = NUM_EUR
        ws4.cell(row=r, column=8, value=f"{p['dimensiones']} · {p['apertura']}").alignment = Alignment(wrap_text=True, vertical="top")
        for col in range(2, 9):
            c = ws4.cell(row=r, column=col)
            c.font = fn_reg
            c.border = b_thin
            if i % 2 == 1:
                c.fill = f_alt
        ws4.row_dimensions[r].height = 38

    # Row 15: Subtotal Cap 3
    ws4.cell(row=15, column=2, value="TOTAL")
    ws4.cell(row=15, column=3, value="SUBTOTAL CAPÍTULO 3: CARPINTERÍA EXTERIOR DE ALUMINIO (CE-01 A CE-08)")
    ws4.cell(row=15, column=4, value="ud")
    ws4.cell(row=15, column=5, value="=SUM(E7:E14)").number_format = "#,##0"
    ws4.cell(row=15, column=6, value="=G15/E15").number_format = NUM_EUR
    ws4.cell(row=15, column=7, value="=SUM(G7:G14)").number_format = NUM_EUR
    ws4.cell(row=15, column=8, value="CE-09 en Cap. 2.3")
    for col in range(2, 9):
        c = ws4.cell(row=15, column=col)
        c.font = fn_tot
        c.fill = f_tot
        c.border = b_tot
    ws4.row_dimensions[15].height = 24

    for col, w in [(1, 3), (2, 10), (3, 60), (4, 8), (5, 11), (6, 15), (7, 16), (8, 28)]:
        ws4.column_dimensions[get_column_letter(col)].width = w

    # ------------------------------------------------------------------
    # HOJA 5: ESCANDALLO INTERNO (SOLO USO INTERNO)
    # ------------------------------------------------------------------
    ws5 = wb.create_sheet("Escandallo Interno")
    ws5["B2"] = "ESTUDIO ECONÓMICO INTERNO Y ESCANDALLO DE COSTES DIRECTOS (CONFIDENCIAL HAM / DIXIS)"
    ws5["B2"].font = fn_title
    ws5["B3"] = "Incluye costes de acero puesto en Menorca (+0,20 €/kg porte marítimo), mermas (5%), MO taller (30 €/h), MO montaje (35 €/h), tratamiento C4/C5 y grúas."
    ws5["B3"].font = fn_reg

    h5 = ["Capítulo", "Concepto de Coste Directo / Venta", "Coste Directo (€)", "Precio Venta (€)", "Margen Bruto (€)", "Margen (% s/Venta)"]
    for idx, h in enumerate(h5, start=2):
        c = ws5.cell(row=5, column=idx, value=h)
        c.font = fn_hdr
        c.fill = f_hdr
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = b_thin
    ws5.row_dimensions[5].height = 24

    esc = DATA["escandallo_interno"]
    esc_rows = [
        ("1.3", "Estructura Metálica (40.675 kg c/ placas nudos y 5% merma, 814 h taller, 520 h montaje, pintura C4/C5, grúas)", esc["estructura"]["coste_directo_total"], "='Resumen Ejecutivo'!F14"),
        ("2A+2B", "Cubierta Panel Acústico 100 mm + Claraboyas CE-09 + Fachada PUR 50 mm (440 h montaje + grúa/PEMP)", esc["cubierta_y_fachada"]["coste_directo_total"], "='Resumen Ejecutivo'!F15+'Resumen Ejecutivo'!F16"),
        ("1.8.1", "Aberturas Exteriores de Aluminio (2 portones CE-01 + 23 ventanas/balconeras RPT + montaje/portes)", esc["aberturas_aluminio"]["coste_directo_total"], "='Resumen Ejecutivo'!F17"),
    ]
    for i, (cid, desc, cd, pv) in enumerate(esc_rows):
        r = 6 + i
        ws5.cell(row=r, column=2, value=cid).alignment = Alignment(horizontal="center")
        ws5.cell(row=r, column=3, value=desc)
        ws5.cell(row=r, column=4, value=cd).number_format = NUM_EUR
        ws5.cell(row=r, column=5, value=pv).number_format = NUM_EUR
        ws5.cell(row=r, column=6, value=f"=E{r}-D{r}").number_format = NUM_EUR
        ws5.cell(row=r, column=7, value=f"=F{r}/E{r}").number_format = NUM_PCT
        for col in range(2, 8):
            c = ws5.cell(row=r, column=col)
            c.font = fn_reg
            c.border = b_thin
            if col == 6:
                c.font = fn_green
        ws5.row_dimensions[r].height = 26

    ws5.cell(row=9, column=2, value="TOTAL")
    ws5.cell(row=9, column=3, value="RESUMEN GLOBAL DEL PRESUPUESTO (ALCANCE COMPLETO)")
    ws5.cell(row=9, column=4, value="=SUM(D6:D8)").number_format = NUM_EUR
    ws5.cell(row=9, column=5, value="=SUM(E6:E8)").number_format = NUM_EUR
    ws5.cell(row=9, column=6, value="=E9-D9").number_format = NUM_EUR
    ws5.cell(row=9, column=7, value="=F9/E9").number_format = NUM_PCT
    for col in range(2, 8):
        c = ws5.cell(row=9, column=col)
        c.font = fn_tot
        c.fill = f_tot
        c.border = b_tot
    ws5.row_dimensions[9].height = 26

    # Detalle escandallo estructura
    ws5["B11"] = "DESGLOSE DE COSTES DIRECTOS POR CAPÍTULO"
    ws5["B11"].font = fn_sec
    det_rows = [
        ("1.3 Estructura", "Acero puesto en Menorca (40.675 kg incl. placas nudos + 5% merma a 1,55 €/kg)", esc["estructura"]["coste_acero_material"]),
        ("1.3 Estructura", "Tornillería estructural alta resistencia y casquillos", esc["estructura"]["coste_tornilleria_nudos"]),
        ("1.3 Estructura", "Oficina técnica, planos de taller y despiece de uniones", esc["estructura"]["coste_ingenieria_despiece_taller"]),
        ("1.3 Estructura", "Mano de obra de taller (814 h a 30 €/h)", esc["estructura"]["coste_mo_taller"]),
        ("1.3 Estructura", "Tratamiento superficial C4/C5 (820 m² a 18 €/m²: granallado + epoxi + poliuretano 2C)", esc["estructura"]["coste_tratamiento_superficial"]),
        ("1.3 Estructura", "Mano de obra montaje en obra (520 h a 35 €/h)", esc["estructura"]["coste_mo_montaje"]),
        ("1.3 Estructura", "Grúa autopropulsada, PEMP y transporte local a Alaior", esc["estructura"]["coste_grua_y_pemp"] + esc["estructura"]["coste_transporte_local_alaior"]),
        ("2. Paneles", "Panel sándwich acústico 100 mm puesto en Menorca (711,75 m²)", esc["cubierta_y_fachada"]["coste_panel_acustico_100mm_puesto_menorca"]),
        ("2. Paneles", "Panel sándwich fachada PUR 50 mm puesto en Menorca (346,87 m²)", esc["cubierta_y_fachada"]["coste_panel_fachada_50mm_puesto_menorca"]),
        ("2. Paneles", "Lucernarios / 12 claraboyas CE-09 policarbonato + babetas", esc["cubierta_y_fachada"]["coste_lucernarios_ce09_12uds"]),
        ("2. Paneles", "Rematería estándar, fijaciones bimetálicas y butilo", esc["cubierta_y_fachada"]["coste_remateria_fijaciones_butilo"]),
        ("2. Paneles", "Montaje cubiertas/fachadas (440 h a 35 €/h) + PEMP/grúa", esc["cubierta_y_fachada"]["coste_mo_montaje"] + esc["cubierta_y_fachada"]["coste_medios_elevacion_pemp_grua"]),
        ("3. Aluminio", "Portones CE-01 (2 uds) + Ventanas/Balconeras CE-02 a CE-08 + instalación/portes", esc["aberturas_aluminio"]["coste_directo_total"]),
    ]
    for i, (cat, item, cost) in enumerate(det_rows):
        r = 12 + i
        ws5.cell(row=r, column=2, value=cat)
        ws5.cell(row=r, column=3, value=item)
        ws5.cell(row=r, column=4, value=cost).number_format = NUM_EUR
        for col in range(2, 5):
            c = ws5.cell(row=r, column=col)
            c.font = fn_reg
            c.border = b_thin
            if i % 2 == 1:
                c.fill = f_alt
        ws5.row_dimensions[r].height = 20

    for col, w in [(1, 3), (2, 16), (3, 68), (4, 18), (5, 18), (6, 18), (7, 18)]:
        ws5.column_dimensions[get_column_letter(col)].width = w

    xlsx_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0058_Nave_Alaior_Estructura_Cubierta_Aluminio.xlsx")
    wb.save(xlsx_path)
    print("Excel generado:", xlsx_path)


def build_cliente_html():
    t = DATA["totales"]
    c1, c2a, c2b, c3 = DATA["capitulos"]
    opt = DATA["complementarios_opcionales"][0]

    rows_c1 = ""
    for p in c1["partidas"]:
        rows_c1 += f"""
        <tr>
          <td><strong>{p['codigo']}</strong></td>
          <td><strong>{p['concepto']}</strong><br><span class="desc">{p['descripcion']}</span></td>
          <td class="cen">{p['perfil']}</td>
          <td class="num">{fmt_num(p['cantidad'])} {p['unidad']}</td>
          <td class="num">{fmt_eur(p['precio_unitario'])}</td>
          <td class="num"><strong>{fmt_eur(p['subtotal'])}</strong></td>
        </tr>"""

    rows_c2 = ""
    for p in c2a["partidas"] + c2b["partidas"]:
        rows_c2 += f"""
        <tr>
          <td><strong>{p['codigo']}</strong></td>
          <td><strong>{p['concepto']}</strong><br><span class="desc">{p['descripcion']}</span></td>
          <td class="cen">{p['perfil']}</td>
          <td class="num">{fmt_num(p['cantidad'])} {p['unidad']}</td>
          <td class="num">{fmt_eur(p['precio_unitario'])}</td>
          <td class="num"><strong>{fmt_eur(p['subtotal'])}</strong></td>
        </tr>"""

    rows_c3 = ""
    for p in c3["partidas"]:
        rows_c3 += f"""
        <tr>
          <td><strong>{p['codigo']}</strong></td>
          <td><strong>{p['concepto']}</strong><br><span class="desc">{p['descripcion']}</span></td>
          <td class="cen">{p['dimensiones']}<br><span class="desc">{p['apertura']}</span></td>
          <td class="num">{p['cantidad']} {p['unidad']}</td>
          <td class="num">{fmt_eur(p['precio_unitario'])}</td>
          <td class="num"><strong>{fmt_eur(p['subtotal'])}</strong></td>
        </tr>"""

    excl_li = "".join(f"<li>{e}</li>" for e in DATA["exclusiones"])

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{DATA['codigo']} · Presupuesto Comercial · Nave Industrial Alaior</title>
  <style>
    @page {{ size: A4 portrait; margin: 6mm; }}
    * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    body {{ margin: 0; background: #e2e8f0; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 8.8px; line-height: 1.32; }}
    .sheet {{ width: 210mm; margin: 10px auto; background: #fff; padding: 8mm 10mm; box-shadow: 0 10px 30px rgba(15,23,42,.12); page-break-after: always; }}
    .sheet:last-child {{ page-break-after: auto; }}
    header {{ background: #0f172a; color: #fff; padding: 9px 14px; border-radius: 7px; border-bottom: 3px solid #0284c7; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
    .brand {{ display: flex; align-items: center; gap: 10px; }}
    .logo {{ width: 40px; height: 40px; background: rgba(255,255,255,.1); border-radius: 5px; padding: 4px; filter: brightness(0) invert(1); }}
    h1 {{ margin: 0; font-size: 14px; font-weight: 700; color: #fff; }}
    .subtitle {{ font-size: 9.5px; color: #94a3b8; margin-top: 2px; }}
    .meta {{ text-align: right; font-size: 8.8px; color: #cbd5e1; }}
    .meta strong {{ display: block; color: #38bdf8; font-size: 11px; margin-bottom: 2px; }}
    .summary-card {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; display: grid; grid-template-columns: 1.4fr 1fr; gap: 14px; align-items: center; }}
    .summary-card p {{ margin: 3px 0 0; color: #334155; font-size: 8.8px; }}
    .price-box {{ border-left: 2px solid #cbd5e1; padding-left: 12px; text-align: right; }}
    .price-tag {{ font-size: 8px; text-transform: uppercase; letter-spacing: .5px; color: #64748b; font-weight: 700; }}
    .main-price {{ font-size: 20px; font-weight: 800; color: #0284c7; margin: 2px 0; }}
    .sub-price {{ font-size: 8.8px; color: #0f172a; }}
    h2 {{ font-size: 10.5px; text-transform: uppercase; letter-spacing: .4px; color: #0f172a; border-bottom: 2px solid #cbd5e1; padding-bottom: 3px; margin: 10px 0 6px; display: flex; justify-content: space-between; align-items: center; }}
    .badge {{ background: #e0f2fe; color: #0369a1; font-size: 8.2px; padding: 2px 7px; border-radius: 10px; font-weight: 700; text-transform: none; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
    th {{ background: #f1f5f9; color: #334155; font-size: 8px; text-transform: uppercase; padding: 4px 6px; border-bottom: 1.5px solid #cbd5e1; text-align: left; }}
    td {{ padding: 4px 6px; border-bottom: 1px solid #e2e8f0; vertical-align: top; font-size: 8.3px; }}
    tr:nth-child(even) td {{ background: #fafafa; }}
    .desc {{ font-size: 7.5px; color: #475569; line-height: 1.24; }}
    .num {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
    .cen {{ text-align: center; font-size: 8px; }}
    .total-row td {{ background: #f1f5f9 !important; font-weight: 700; border-top: 1.5px solid #94a3b8; border-bottom: 1.5px solid #94a3b8; color: #0f172a; }}
    .grand-total td {{ background: #0f172a !important; color: #ffffff !important; padding: 7px 10px; }}
    .sub-row td {{ background: #e0f2fe !important; font-weight: 700; color: #0369a1; }}
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px; }}
    .box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 7px 10px; }}
    .box h3 {{ margin: 0 0 4px; font-size: 9px; color: #0369a1; text-transform: uppercase; }}
    .box ul {{ margin: 0; padding-left: 14px; font-size: 8px; color: #334155; }}
    .box li {{ margin-bottom: 2px; }}
    .opt-box {{ background: #fffbeb; border: 1px solid #fcd34d; border-radius: 5px; padding: 7px 10px; margin-top: 6px; font-size: 8.3px; }}
    footer {{ margin-top: 10px; padding-top: 6px; border-top: 1px solid #e2e8f0; font-size: 7.8px; color: #64748b; display: flex; justify-content: space-between; }}
    @media print {{ body {{ background: #fff; }} .sheet {{ box-shadow: none; margin: 0; width: 100%; padding: 5mm 7mm; }} }}
  </style>
</head>
<body>
  <!-- PÁGINA 1: RESUMEN Y CAPÍTULO 1 ESTRUCTURA -->
  <div class="sheet">
    <header>
      <div class="brand">
        <img class="logo" src="logo-ham.svg" alt="HAM">
        <div>
          <h1>HAM ESTRUCTURAS METÁLICAS MENORCA</h1>
          <div class="subtitle">Dixis Recursos y Soluciones S.L. (CIF {DATA['emisor']['cif']}) · Estructuras, Cubiertas y Carpintería de Aluminio</div>
        </div>
      </div>
      <div class="meta">
        <strong>PRESUPUESTO {DATA['codigo']}</strong>
        Ref.: {DATA['referencia']}<br>
        Fecha: {DATA['fecha']} · Validez: {DATA['validez_dias']} días
      </div>
    </header>

    <div class="summary-card">
      <div>
        <strong style="color:#0369a1; font-size:10.5px;">{DATA['cliente']['proyecto']}</strong>
        <p><strong>Cliente:</strong> {DATA['cliente']['nombre']} · <strong>Ubicación:</strong> {DATA['cliente']['ubicacion']}<br>
        <strong>Técnico:</strong> {DATA['cliente']['tecnico']}<br>
        <strong>Referencia:</strong> {DATA['cliente']['mediciones_ref']}</p>
      </div>
      <div class="price-box">
        <div class="price-tag">Oferta Completa (Cap. 1 + Cap. 2 + Cap. 3)</div>
        <div class="main-price">{fmt_eur(t['base_completo_con_fachada_sandwich'])}</div>
        <div class="sub-price">IVA 21%: {fmt_eur(t['iva_completo'])} · <strong>Total: {fmt_eur(t['total_completo'])}</strong></div>
        <div style="font-size:7.8px; color:#475569; margin-top:3px;">Opción sin fachada sándwich 2.1 (solo Estructura + Cubierta + Aluminio): <strong>{fmt_eur(t['base_solo_estructura_cubierta_aluminio'])}</strong> + IVA</div>
      </div>
    </div>

    <h2>1. Estructura Metálica Principal y Secundaria (Cap. 1.3) <span class="badge">36.987,92 kg · Suministro, Fabricación, C4/C5 y Montaje</span></h2>
    <table>
      <thead>
        <tr>
          <th style="width:7%;">Cód.</th>
          <th style="width:49%;">Descripción</th>
          <th style="width:14%; text-align:center;">Serie / Acero</th>
          <th style="width:10%; text-align:right;">Medición</th>
          <th style="width:9%; text-align:right;">Precio</th>
          <th style="width:11%; text-align:right;">Subtotal</th>
        </tr>
      </thead>
      <tbody>
        {rows_c1}
        <tr class="total-row">
          <td colspan="3"><strong>SUBTOTAL CAPÍTULO 1: ESTRUCTURA METÁLICA (SEGÚN MEDICIÓN CYPECAD V2)</strong></td>
          <td class="num"><strong>{fmt_num(c1['peso_total_kg'])} kg</strong></td>
          <td class="num"><strong>5,00 €</strong></td>
          <td class="num"><strong>{fmt_eur(c1['subtotal'])}</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="opt-box">
      <strong>Nota Técnica sobre Placas de Anclaje a Cimentación (Partida Opcional {opt['codigo']}):</strong> Según el criterio literal de medición CYPECAD (capítulos 1.3.1–1.3.4), las placas de anclaje a cimentación no están incluidas en el peso anterior. Si se encarga su suministro completo con pernos DIN 976 (6 conjuntos Tipo 4 + 21 conjuntos Tipo 10/11 según planos E09–E10, ~1.812 kg), su importe adicional es de <strong>{fmt_eur(opt['subtotal'])} + IVA</strong>.
    </div>

    <div class="grid-2">
      <div class="box">
        <h3>Tratamiento Superficial y Fabricación HAM</h3>
        <ul>
          <li><strong>Acero estructural</strong> S275JR (laminado) y S235JR (conformado) según UNE-EN 10025.</li>
          <li><strong>Protección marina C4/C5 Menorca:</strong> Granallado Sa 2,5, imprimación epoxídica rica en fosfato de zinc y esmalte poliuretano alifático 2C de exterior (secado al aire en cabina, <em>nunca al horno</em>).</li>
          <li><strong>Uniones en taller y obra:</strong> Soldadura MAG bajo UNE-EN 1090-2 y atornillado controlado (8.8/5.6) según detalles E09–E11.</li>
        </ul>
      </div>
      <div class="box">
        <h3>Logística y Medios de Elevación Incluidos</h3>
        <ul>
          <li><strong>Transporte marítimo y terrestre:</strong> Portes Península–Menorca y entrega en parcela en Alaior.</li>
          <li><strong>Elevación en obra:</strong> Grúa autopropulsada, camión pluma y plataformas elevadoras PEMP para izado de pórticos y correas.</li>
          <li><strong>Replanteo técnico previo:</strong> Verificación de niveles de cimentación antes de fabricación.</li>
        </ul>
      </div>
    </div>

    <footer>
      <div>{DATA['emisor']['nombre_comercial']} · {DATA['emisor']['direccion']} · {DATA['emisor']['telefono']} · {DATA['emisor']['email']}</div>
      <div>Página 1 de 3</div>
    </footer>
  </div>

  <!-- PÁGINA 2: CAPÍTULO 2 CUBIERTA Y FACHADA PANEL SÁNDWICH -->
  <div class="sheet">
    <header>
      <div class="brand">
        <img class="logo" src="logo-ham.svg" alt="HAM">
        <div>
          <h1>HAM ESTRUCTURAS METÁLICAS MENORCA</h1>
          <div class="subtitle">Capítulo 2 · Cubierta Acústica, Claraboyas y Cerramiento Sándwich de Fachada</div>
        </div>
      </div>
      <div class="meta"><strong>PRESUPUESTO {DATA['codigo']}</strong>Fecha: {DATA['fecha']}</div>
    </header>

    <h2>2. Cubierta Inclinada (Pendiente 8%) y Fachada Panel Sándwich <span class="badge">1.073,62 m² totales</span></h2>
    <table>
      <thead>
        <tr>
          <th style="width:7%;">Cód.</th>
          <th style="width:50%;">Descripción</th>
          <th style="width:14%; text-align:center;">Sistema</th>
          <th style="width:10%; text-align:right;">Medición</th>
          <th style="width:8%; text-align:right;">Precio</th>
          <th style="width:11%; text-align:right;">Subtotal</th>
        </tr>
      </thead>
      <tbody>
        {rows_c2}
        <tr class="sub-row">
          <td colspan="3"><strong>SUBTOTAL CUBIERTA (PARTIDAS 2.2 COBERTURA ACÚSTICA + 2.3 LUCERNARIOS CE-09)</strong></td>
          <td class="num"><strong>726,75 m²</strong></td>
          <td class="num">-</td>
          <td class="num"><strong>{fmt_eur(t['cap2a_cubierta'])}</strong></td>
        </tr>
        <tr class="total-row">
          <td colspan="3"><strong>SUBTOTAL CAPÍTULO 2 COMPLETO (CUBIERTA + FACHADA PANEL SÁNDWICH PUR 50 MM)</strong></td>
          <td class="num"><strong>1.073,62 m²</strong></td>
          <td class="num">-</td>
          <td class="num"><strong>{fmt_eur(t['cap2_total_paneles'])}</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="grid-2">
      <div class="box">
        <h3>Especificaciones Técnicas de Cubierta (2.2 y 2.3)</h3>
        <ul>
          <li>Panel acústico sándwich e=100 mm con núcleo de lana de roca 95 kg/m³, reacción al fuego Euroclase A2-s1,d0 y atenuación acústica Rw = 35 dB.</li>
          <li>Chapa interior microperforada fonoabsorbente (Ø3 mm) y exterior grecada 5 grecas RC3/RUV2 para ambiente exterior.</li>
          <li>12 claraboyas fijas CE-09 (1,00 x 1,00 m) integradas en partida 2.3 con babeta galvanizada y sellado elástico estanco.</li>
        </ul>
      </div>
      <div class="box">
        <h3>Especificaciones Técnicas de Fachada (2.1)</h3>
        <ul>
          <li>Panel sándwich PUR e=50 mm (40 kg/m³, Euroclase B-s1,d0) en franjas superiores de Alzado Este (171,57 m²) y Alzado Oeste (175,30 m²).</li>
          <li>Fijación mecánica oculta sobre estructura metálica, sellado de solapes con cinta de butilo biadhesiva y remates perimetrales.</li>
          <li>Montaje completo en altura mediante plataformas PEMP y medios de seguridad colectiva.</li>
        </ul>
      </div>
    </div>

    <footer>
      <div>{DATA['emisor']['nombre_comercial']} · {DATA['emisor']['web']} · {DATA['emisor']['email']}</div>
      <div>Página 2 de 3</div>
    </footer>
  </div>

  <!-- PÁGINA 3: CAPÍTULO 3 ABERTURAS ALUMINIO + TOTALES Y CONDICIONES -->
  <div class="sheet">
    <header>
      <div class="brand">
        <img class="logo" src="logo-ham.svg" alt="HAM">
        <div>
          <h1>HAM ESTRUCTURAS METÁLICAS MENORCA</h1>
          <div class="subtitle">Capítulo 3 · Aberturas y Carpintería Exterior de Aluminio (Plano 11)</div>
        </div>
      </div>
      <div class="meta"><strong>PRESUPUESTO {DATA['codigo']}</strong>Fecha: {DATA['fecha']}</div>
    </header>

    <h2>3. Aberturas Exteriores de Aluminio RPT (Plano 11 · Partida 1.8.1) <span class="badge">2 Portones + 23 Ventanas/Balconeras</span></h2>
    <table>
      <thead>
        <tr>
          <th style="width:7%;">Marca</th>
          <th style="width:45%;">Descripción Técnica</th>
          <th style="width:20%; text-align:center;">Medidas / Apertura</th>
          <th style="width:7%; text-align:right;">Uds.</th>
          <th style="width:10%; text-align:right;">Precio Ud.</th>
          <th style="width:11%; text-align:right;">Subtotal</th>
        </tr>
      </thead>
      <tbody>
        {rows_c3}
        <tr class="total-row">
          <td colspan="3"><strong>SUBTOTAL CAPÍTULO 3: CARPINTERÍA EXTERIOR DE ALUMINIO (CE-01 A CE-08)</strong><br><span class="desc">Nota: Las 12 claraboyas CE-09 (1,00 x 1,00 m) se presupuestan en Capítulo 2 (Partida 2.3) para evitar duplicidades.</span></td>
          <td class="num"><strong>25 uds</strong></td>
          <td class="num">-</td>
          <td class="num"><strong>{fmt_eur(c3['subtotal'])}</strong></td>
        </tr>
      </tbody>
    </table>

    <table>
      <tbody>
        <tr class="sub-row">
          <td style="padding:6px 10px;"><strong>OPCIÓN ALCANCE A — SOLO ESTRUCTURA + CUBIERTA (2.2-2.3) + ALUMINIO (Sin Fachada Sándwich 2.1)</strong></td>
          <td class="num" style="padding:6px 10px;"><strong>{fmt_eur(t['base_solo_estructura_cubierta_aluminio'])}</strong> <span class="desc">(+IVA: {fmt_eur(t['total_solo_estructura_cubierta_aluminio'])})</span></td>
        </tr>
        <tr class="grand-total">
          <td style="font-size:10px;"><strong>BASE IMPONIBLE TOTAL — ALCANCE COMPLETO (ESTRUCTURA + CUBIERTA + FACHADA SÁNDWICH + ALUMINIO)</strong></td>
          <td class="num" style="font-size:11.5px;"><strong>{fmt_eur(t['base_completo_con_fachada_sandwich'])}</strong></td>
        </tr>
        <tr>
          <td style="padding:5px 10px;">I.V.A. General (21,00%)</td>
          <td class="num" style="padding:5px 10px;">{fmt_eur(t['iva_completo'])}</td>
        </tr>
        <tr style="background:#e0f2fe; color:#0369a1;">
          <td style="padding:7px 10px; font-size:10.5px;"><strong>TOTAL PRESUPUESTO COMPLETO (I.V.A. INCLUIDO)</strong></td>
          <td class="num" style="padding:7px 10px; font-size:13px;"><strong>{fmt_eur(t['total_completo'])}</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="grid-2">
      <div class="box">
        <h3>Condiciones Comerciales</h3>
        <ul>
          <li><strong>Validez de la oferta:</strong> {DATA['condiciones']['validez']}.</li>
          <li><strong>Forma de pago:</strong> {DATA['condiciones']['forma_pago']}.</li>
          <li><strong>Plazo estimado:</strong> {DATA['condiciones']['plazo_ejecucion']}.</li>
          <li><strong>Acabado aluminio:</strong> Lacado verde calidad marina Qualicoat Seaside, RPT y vidrio 6/16 Argón/4 BE Chromatech Ultra.</li>
        </ul>
      </div>
      <div class="box">
        <h3>Exclusiones Expresas</h3>
        <ul>{excl_li}</ul>
      </div>
    </div>

    <footer>
      <div>{DATA['emisor']['razon_social']} · CIF {DATA['emisor']['cif']} · {DATA['emisor']['direccion']}</div>
      <div>Página 3 de 3</div>
    </footer>
  </div>
</body>
</html>"""

    p_html = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(p_html, "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML cliente generado:", p_html)
    return p_html


def build_tecnico_html():
    t = DATA["totales"]
    esc = DATA["escandallo_interno"]
    e1 = esc["estructura"]
    e2 = esc["cubierta_y_fachada"]
    e3 = esc["aberturas_aluminio"]
    eg = esc["resumen_global"]

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{DATA['codigo']} · Estudio Técnico Interno y Escandallo · Alaior</title>
  <style>
    @page {{ size: A4 portrait; margin: 7mm; }}
    * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    body {{ margin: 0; background: #e2e8f0; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 8.8px; line-height: 1.35; }}
    .sheet {{ width: 210mm; margin: 10px auto; background: #fff; padding: 9mm 11mm; box-shadow: 0 10px 30px rgba(15,23,42,.12); page-break-after: always; }}
    .sheet:last-child {{ page-break-after: auto; }}
    header {{ background: #1e293b; color: #fff; padding: 10px 15px; border-radius: 7px; border-bottom: 3px solid #d97706; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
    h1 {{ margin: 0; font-size: 13.5px; color: #fff; }}
    .sub {{ font-size: 9px; color: #cbd5e1; margin-top: 2px; }}
    .tag {{ background: #b45309; color: #fff; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 8.5px; }}
    h2 {{ font-size: 10px; text-transform: uppercase; color: #0f172a; border-bottom: 2px solid #cbd5e1; padding-bottom: 3px; margin: 10px 0 6px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
    th {{ background: #f1f5f9; color: #334155; font-size: 8px; text-transform: uppercase; padding: 5px 6px; border-bottom: 1.5px solid #cbd5e1; text-align: left; }}
    td {{ padding: 4.5px 6px; border-bottom: 1px solid #e2e8f0; font-size: 8.4px; vertical-align: top; }}
    .num {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
    .tot td {{ background: #fef3c7; font-weight: 700; border-top: 1.5px solid #d97706; border-bottom: 1.5px solid #d97706; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px; }}
    .kpi {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 5px; padding: 7px 10px; }}
    .kpi span {{ display: block; font-size: 7.5px; text-transform: uppercase; color: #64748b; font-weight: 700; }}
    .kpi strong {{ font-size: 13px; color: #0f172a; }}
    .alert {{ background: #fff7ed; border-left: 4px solid #ea580c; padding: 7px 10px; margin-bottom: 8px; font-size: 8.3px; }}
    .box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 7px 10px; margin-bottom: 8px; }}
    ul {{ margin: 4px 0 0; padding-left: 15px; font-size: 8.2px; }}
    li {{ margin-bottom: 3px; }}
    footer {{ margin-top: 8px; padding-top: 6px; border-top: 1px solid #e2e8f0; font-size: 7.8px; color: #64748b; display: flex; justify-content: space-between; }}
    @media print {{ body {{ background: #fff; }} .sheet {{ box-shadow: none; margin: 0; width: 100%; padding: 5mm 7mm; }} }}
  </style>
</head>
<body>
  <div class="sheet">
    <header>
      <div>
        <h1>ESTUDIO TÉCNICO INTERNO Y ESCANDALLO · {DATA['codigo']}</h1>
        <div class="sub">Nave Alaior (Obres Gabi Gonyalons S.L.U.) · Documentación confidencial HAM / DIXIS</div>
      </div>
      <div class="tag">USO INTERNO</div>
    </header>

    <div class="kpi-grid">
      <div class="kpi"><span>Coste Directo Total</span><strong>{fmt_eur(eg['coste_directo_total'])}</strong></div>
      <div class="kpi"><span>Precio Venta Neto (Completo)</span><strong>{fmt_eur(eg['venta_total'])}</strong></div>
      <div class="kpi"><span>Margen Bruto (€)</span><strong style="color:#15803d;">{fmt_eur(eg['margen_bruto_total'])}</strong></div>
      <div class="kpi"><span>Margen Bruto (% s/Venta)</span><strong style="color:#15803d;">{fmt_num(eg['margen_bruto_porcentaje'])}%</strong></div>
    </div>

    <h2>1. Resumen Económico Interno por Capítulos</h2>
    <table>
      <thead>
        <tr>
          <th>Capítulo</th>
          <th>Alcance</th>
          <th style="text-align:right;">Coste Directo</th>
          <th style="text-align:right;">Venta Neta</th>
          <th style="text-align:right;">Margen (€)</th>
          <th style="text-align:right;">Margen (%)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Cap. 1 (1.3)</strong></td>
          <td>Estructura metálica CYPECAD (36.987,92 kg netos / ~40.675 kg c/ placas nudos y 5% merma)</td>
          <td class="num">{fmt_eur(e1['coste_directo_total'])}</td>
          <td class="num">{fmt_eur(e1['venta_total'])}</td>
          <td class="num" style="color:#15803d;"><strong>{fmt_eur(e1['margen_euros'])}</strong></td>
          <td class="num">{fmt_num(e1['margen_porcentaje'])}%</td>
        </tr>
        <tr>
          <td><strong>Cap. 2 (2A+2B)</strong></td>
          <td>Cubierta panel acústico 100 mm (711,75 m²) + 12 claraboyas (15 m²) + Fachada PUR 50 mm (346,87 m²)</td>
          <td class="num">{fmt_eur(e2['coste_directo_total'])}</td>
          <td class="num">{fmt_eur(e2['venta_total'])}</td>
          <td class="num" style="color:#15803d;"><strong>{fmt_eur(e2['margen_euros'])}</strong></td>
          <td class="num">{fmt_num(e2['margen_porcentaje'])}%</td>
        </tr>
        <tr>
          <td><strong>Cap. 3 (1.8.1)</strong></td>
          <td>Aberturas exteriores de aluminio (2 portones CE-01 + 23 ventanas/balconeras CE-02 a CE-08)</td>
          <td class="num">{fmt_eur(e3['coste_directo_total'])}</td>
          <td class="num">{fmt_eur(e3['venta_total'])}</td>
          <td class="num" style="color:#15803d;"><strong>{fmt_eur(e3['margen_euros'])}</strong></td>
          <td class="num">{fmt_num(e3['margen_porcentaje'])}%</td>
        </tr>
        <tr class="tot">
          <td colspan="2"><strong>TOTAL CONSOLIDADO (ESTRUCTURA + CUBIERTA + FACHADA SÁNDWICH + ALUMINIO)</strong></td>
          <td class="num">{fmt_eur(eg['coste_directo_total'])}</td>
          <td class="num">{fmt_eur(eg['venta_total'])}</td>
          <td class="num">{fmt_eur(eg['margen_bruto_total'])}</td>
          <td class="num">{fmt_num(eg['margen_bruto_porcentaje'])}%</td>
        </tr>
      </tbody>
    </table>

    <h2>2. Desglose de Costes Directos e Hipótesis de Cálculo</h2>
    <table>
      <thead>
        <tr>
          <th style="width:18%;">Bloque</th>
          <th style="width:52%;">Concepto de Coste e Hipótesis</th>
          <th style="width:15%; text-align:right;">Base / Horas</th>
          <th style="width:15%; text-align:right;">Coste Directo</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>1.3 Acero</td><td>Compra acero puesto Menorca (+0,20 €/kg porte marítimo, 5% merma, +1.750 kg placas nudos E09-E11)</td><td class="num">40.675 kg × 1,55 €</td><td class="num">{fmt_eur(e1['coste_acero_material'])}</td></tr>
        <tr><td>1.3 Acero</td><td>Tornillería alta resistencia (ISO 4017 8.8/5.6), casquillos e ingeniería/planos taller</td><td class="num">Lote</td><td class="num">{fmt_eur(e1['coste_tornilleria_nudos'] + e1['coste_ingenieria_despiece_taller'])}</td></tr>
        <tr><td>1.3 Acero</td><td>Mano de obra taller HAM (corte, preparación, soldadura placas/cartelas, taladrado)</td><td class="num">814 h × 30,00 €</td><td class="num">{fmt_eur(e1['coste_mo_taller'])}</td></tr>
        <tr><td>1.3 Acero</td><td>Tratamiento superficial C4/C5 (granallado Sa 2,5 + imprimación epoxi + poliuretano 2C, secado al aire)</td><td class="num">820 m² × 18,00 €</td><td class="num">{fmt_eur(e1['coste_tratamiento_superficial'])}</td></tr>
        <tr><td>1.3 Acero</td><td>Montaje en obra (520 h × 35 €/h) + grúa/PEMP (8.500 €) + porte local Alaior (1.800 €)</td><td class="num">520 h + medios</td><td class="num">{fmt_eur(e1['coste_mo_montaje'] + e1['coste_grua_y_pemp'] + e1['coste_transporte_local_alaior'])}</td></tr>
        <tr><td>2. Paneles</td><td>Suministro panel acústico 100 mm (44.128,50 €) + fachada PUR 50 mm (11.793,58 €) puestos Menorca</td><td class="num">1.058,62 m²</td><td class="num">{fmt_eur(e2['coste_panel_acustico_100mm_puesto_menorca'] + e2['coste_panel_fachada_50mm_puesto_menorca'])}</td></tr>
        <tr><td>2. Paneles</td><td>12 Claraboyas CE-09 (1.440 €) + rematería estándar, fijaciones bimetálicas y butilo (4.950 €)</td><td class="num">Lote</td><td class="num">{fmt_eur(e2['coste_lucernarios_ce09_12uds'] + e2['coste_remateria_fijaciones_butilo'])}</td></tr>
        <tr><td>2. Paneles</td><td>Montaje en cubierta y fachada (440 h × 35 €/h) + PEMP/grúa adicional</td><td class="num">440 h + PEMP</td><td class="num">{fmt_eur(e2['coste_mo_montaje'] + e2['coste_medios_elevacion_pemp_grua'])}</td></tr>
        <tr><td>3. Aluminio</td><td>2 Portones CE-01 (4.200 €) + 23 ventanas/balconeras RPT (14.330 €) + portes/sellado (1.050 €)</td><td class="num">25 uds</td><td class="num">{fmt_eur(e3['coste_directo_total'])}</td></tr>
      </tbody>
    </table>

    <h2>3. Auditoría de Planos vs Mediciones CYPECAD V2 (Discrepancias Detectadas)</h2>
    <div class="alert">
      <strong>Correcciones aplicadas respecto al borrador previo P-2026-0054 y verificación contra Planos 01-11 y E01-E11:</strong>
      <ul>
        <li><strong>Placas de anclaje excluidas del CSV CYPECAD:</strong> El texto 1.3.1–1.3.4 excluye expresamente las placas de anclaje a cimentación. En planos E09–E10 suman 27 conjuntos (6 Tipo 4 de 650x650x25 + 12 pernos M20x672; 21 Tipo 10/11 de 450x450x25 + 4 pernos M18x470 ≈ 1.812 kg). Se separan como opcional <strong>OPC-1.3.5 (9.060,00 €)</strong> para evitar regalarlas o duplicarlas con obra civil.</li>
        <li><strong>Dimensiones y aperturas corregidas en Plano 11:</strong> <strong>CE-02</strong> es 2,00 × 2,50 m (en P-2026-0054 estaba infravalorada a 820 € → ajustada a 2.150 €); <strong>CE-03</strong> mide 1,00 × 2,00 m con fijo sup. 0,50 m (no 1,50×2,00 m); <strong>CE-06</strong> (16 uds 1,20×1,20) lleva flechas de corredera en plano frente al texto "batientes" (confirmar con DF en replanteo); <strong>CE-08</strong> mide 0,50 × 0,50 m (no 0,50×1,20 m).</li>
        <li><strong>Claraboyas CE-09 vs Partida 2.3:</strong> En plano 11 hay 12 uds de 1,00 × 1,00 m (12 m² reales) y en CYPECAD 15 m² (partida 2.3). Se unifican en 2.3 y se referencian en Cap. 3 sin doble cobro.</li>
        <li><strong>Precios realistas de aluminio RPT Qualicoat Seaside:</strong> El capítulo 3 pasa de 19.650 € (infravalorado) a <strong>30.210 €</strong>, alineado con P-2026-0052 y P-2026-0053.</li>
      </ul>
    </div>

    <div class="box">
      <strong>Riesgos a Validar Antes de Firma de Contrato:</strong>
      <ul>
        <li>Confirmar con el cliente si desea incluir <strong>Fachada panel sándwich 2.1 (41.624,40 €)</strong> y <strong>Placas de anclaje OPC-1.3.5 (9.060,00 €)</strong>.</li>
        <li>Solicitar al cliente / DF confirmación de exigencia de <strong>pintura intumescente</strong> (resistencia al fuego R en estructura según RSCIEI / DB-SI) y vidrio laminar de seguridad en puertas peatonales CE-02 y CE-03 (CTE DB-SUA).</li>
        <li>Verificar si la contrata civil ejecuta los <strong>canalones pluviales y bajantes</strong> de planos 13–15 (excluidos de este presupuesto).</li>
      </ul>
    </div>

    <footer>
      <div>Documento interno confidencial · {DATA['emisor']['nombre_comercial']}</div>
      <div>Página 1 de 1</div>
    </footer>
  </div>
</body>
</html>"""

    p_html = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(p_html, "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML técnico generado:", p_html)
    return p_html


def html_to_pdf(html_path, pdf_name):
    pdf_path = os.path.join(BASE_DIR, pdf_name)
    uri = "file:///" + html_path.replace("\\", "/")
    subprocess.run(
        [CHROME_PATH, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", uri],
        check=True,
    )
    print("PDF generado:", pdf_path)


if __name__ == "__main__":
    create_excel()
    hc = build_cliente_html()
    ht = build_tecnico_html()
    if os.path.exists(CHROME_PATH):
        html_to_pdf(hc, "presupuesto-cliente.pdf")
        html_to_pdf(ht, "presupuesto-interno-tecnico.pdf")
    else:
        print("AVISO: Chrome no encontrado en", CHROME_PATH)
