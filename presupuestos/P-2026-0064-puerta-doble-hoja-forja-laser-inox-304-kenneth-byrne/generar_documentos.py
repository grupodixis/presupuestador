import os
import json
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def eur(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def create_excel():
    wb = Workbook()

    NAVY = "0F172A"
    GOLD = "B45309"
    SLATE_LIGHT = "F8FAFC"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"
    EDIT_FILL = "FEF9C3"
    GREEN_DARK = "15803D"

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    fill_edit = PatternFill(start_color=EDIT_FILL, end_color=EDIT_FILL, fill_type="solid")

    font_title = Font(name="Segoe UI", size=12.5, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_tot = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=10.5, bold=True, color=GOLD)
    font_green = Font(name="Segoe UI", size=9, bold=True, color=GREEN_DARK)

    border_thin = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )
    border_total = Border(
        top=Side(style="thin", color=NAVY),
        bottom=Side(style="double", color=NAVY),
    )

    # -------------------------------------------------------------
    # HOJA 1: PRESUPUESTO CLIENTE
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Cliente"
    ws1.views.sheetView[0].showGridLines = True

    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. · CIF B57825432 | HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_sub
    ws1["B3"] = (
        f"PRESUPUESTO ORIENTATIVO {DATA['codigo']} • PUERTA DOBLE HOJA FORJA LÁSER 10 MM EN INOX AISI 304"
    )
    ws1["B3"].font = font_title

    meta_rows = [
        ("REFERENCIA:", DATA["referencia"]),
        ("ESTADO:", DATA["estado_presupuesto"]),
        ("CLIENTE:", f"{DATA['cliente']['nombre']} · {DATA['cliente']['ubicacion']}"),
        (
            "MEDIDAS APROX.:",
            f"Ancho: {DATA['proyecto']['medidas_aprox']['ancho_total']} | Lateral: {DATA['proyecto']['medidas_aprox']['altura_laterales']} | Centro: {DATA['proyecto']['medidas_aprox']['altura_centro']}",
        ),
        ("FECHA / VALIDEZ:", f"{DATA['fecha']} · Validez: {DATA['validez_dias']} días naturales"),
        ("CALIDAD BASE:", DATA["calidad_base"]),
    ]
    for idx, (k, v) in enumerate(meta_rows, start=5):
        ws1[f"B{idx}"] = k
        ws1[f"B{idx}"].font = font_bold
        ws1[f"C{idx}"] = v
        ws1[f"C{idx}"].font = font_reg

    ws1["B12"] = "DESGLOSE ORIENTATIVO DE PARTIDAS (OPCIÓN BASE ACERO INOXIDABLE AISI 304)"
    ws1["B12"].font = font_sec

    headers_client = ["Nº", "Concepto y Descripción Técnica", "Ud.", "Cantidad", "Precio Unitario", "Subtotal"]
    for c_idx, h in enumerate(headers_client, start=2):
        cell = ws1.cell(row=13, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[13].height = 24

    row_cur = 14
    for p in DATA["partidas_cliente"]:
        ws1.cell(row=row_cur, column=2, value=p["id"]).font = font_bold
        ws1.cell(row=row_cur, column=2).alignment = Alignment(horizontal="center", vertical="top")

        c_desc = ws1.cell(row=row_cur, column=3, value=f"{p['concepto']}\n{p['descripcion']}")
        c_desc.font = font_reg
        c_desc.alignment = Alignment(wrap_text=True, vertical="top")

        ws1.cell(row=row_cur, column=4, value=p["unidad"]).font = font_reg
        ws1.cell(row=row_cur, column=4).alignment = Alignment(horizontal="center", vertical="top")

        c_qty = ws1.cell(row=row_cur, column=5, value=p["cantidad"])
        c_qty.font = font_bold
        c_qty.number_format = "#,##0.00"
        c_qty.alignment = Alignment(horizontal="right", vertical="top")

        c_pu = ws1.cell(row=row_cur, column=6, value=p["precio_unitario"])
        c_pu.font = font_reg
        c_pu.number_format = '#,##0.00 "€"'
        c_pu.alignment = Alignment(horizontal="right", vertical="top")

        c_sub = ws1.cell(row=row_cur, column=7, value=f"=E{row_cur}*F{row_cur}")
        c_sub.font = font_bold
        c_sub.number_format = '#,##0.00 "€"'
        c_sub.alignment = Alignment(horizontal="right", vertical="top")

        for col in range(2, 8):
            ws1.cell(row=row_cur, column=col).border = border_thin
            if row_cur % 2 == 1:
                ws1.cell(row=row_cur, column=col).fill = fill_alt
        ws1.row_dimensions[row_cur].height = 58 if len(p["descripcion"]) > 220 else 44
        row_cur += 1

    # Totales Opción Base
    r_tot = row_cur + 1  # row 20
    ws1.cell(row=r_tot, column=6, value="BASE IMPONIBLE (AISI 304):").font = font_bold
    c_bi = ws1.cell(row=r_tot, column=7, value=f"=SUM(G14:G{row_cur-1})")
    c_bi.font = font_tot
    c_bi.number_format = '#,##0.00 "€"'
    c_bi.border = border_thin

    ws1.cell(row=r_tot + 1, column=6, value="IVA (21%):").font = font_bold
    c_iva = ws1.cell(row=r_tot + 1, column=7, value=f"=G{r_tot}*0.21")
    c_iva.font = font_reg
    c_iva.number_format = '#,##0.00 "€"'
    c_iva.border = border_thin

    ws1.cell(row=r_tot + 2, column=6, value="TOTAL ORIENTATIVO (AISI 304):").font = font_tot_gold
    c_total = ws1.cell(row=r_tot + 2, column=7, value=f"=G{r_tot}+G{r_tot+1}")
    c_total.font = font_tot_gold
    c_total.fill = fill_tot
    c_total.number_format = '#,##0.00 "€"'
    c_total.border = border_total

    # Tabla comparativa AISI 304 vs AISI 316
    r_cmp = r_tot + 4  # row 24
    ws1.cell(
        row=r_cmp,
        column=2,
        value="COMPARATIVA OPCIONAL DE CALIDAD INOXIDABLE (A VALORAR EN VISITA TÉCNICA)",
    ).font = font_sec

    cmp_headers = ["Opción", "Especificación / Ambiente Recomendado", "Supl. Neto", "Base Imponible", "IVA (21%)", "Total IVA Inc."]
    for c_idx, h in enumerate(cmp_headers, start=2):
        cell = ws1.cell(row=r_cmp + 1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[r_cmp + 1].height = 22

    # Fila Opción Base 304
    r_op1 = r_cmp + 2  # row 26
    ws1.cell(row=r_op1, column=2, value="Opción Base").font = font_bold
    ws1.cell(
        row=r_op1,
        column=3,
        value="Acero Inoxidable AISI 304 + adornos láser 10 mm + pintura epoxi/poliuretano negra RAL 9005 (Exterior general en Menorca)",
    ).font = font_reg
    ws1.cell(row=r_op1, column=3).alignment = Alignment(wrap_text=True, vertical="center")
    c_sup1 = ws1.cell(row=r_op1, column=4, value=0.00)
    c_sup1.number_format = '#,##0.00 "€"'
    c_sup1.alignment = Alignment(horizontal="right", vertical="center")
    c_b1 = ws1.cell(row=r_op1, column=5, value=f"=G{r_tot}")
    c_b1.font = font_bold
    c_b1.number_format = '#,##0.00 "€"'
    c_i1 = ws1.cell(row=r_op1, column=6, value=f"=E{r_op1}*0.21")
    c_i1.number_format = '#,##0.00 "€"'
    c_t1 = ws1.cell(row=r_op1, column=7, value=f"=E{r_op1}+F{r_op1}")
    c_t1.font = font_bold
    c_t1.number_format = '#,##0.00 "€"'
    for col in range(2, 8):
        ws1.cell(row=r_op1, column=col).border = border_thin
    ws1.row_dimensions[r_op1].height = 28

    # Fila Opción Alternativa 316
    r_op2 = r_cmp + 3  # row 27
    ws1.cell(row=r_op2, column=2, value="Opción Marina").font = font_bold
    ws1.cell(
        row=r_op2,
        column=3,
        value="Acero Inoxidable AISI 316 Calidad Marina C5-M + adornos láser 10 mm + pintura epoxi/poliuretano negra (Primera línea de mar / exposición salina severa)",
    ).font = font_reg
    ws1.cell(row=r_op2, column=3).alignment = Alignment(wrap_text=True, vertical="center")
    c_sup2 = ws1.cell(row=r_op2, column=4, value=DATA["suplemento_316"]["suplemento_venta_bi"])
    c_sup2.font = font_reg
    c_sup2.number_format = '+#,##0.00 "€"'
    c_sup2.alignment = Alignment(horizontal="right", vertical="center")
    c_b2 = ws1.cell(row=r_op2, column=5, value=f"=G{r_tot}+D{r_op2}")
    c_b2.font = font_bold
    c_b2.number_format = '#,##0.00 "€"'
    c_i2 = ws1.cell(row=r_op2, column=6, value=f"=E{r_op2}*0.21")
    c_i2.number_format = '#,##0.00 "€"'
    c_t2 = ws1.cell(row=r_op2, column=7, value=f"=E{r_op2}+F{r_op2}")
    c_t2.font = font_tot_gold
    c_t2.fill = fill_tot
    c_t2.number_format = '#,##0.00 "€"'
    for col in range(2, 8):
        ws1.cell(row=r_op2, column=col).border = border_thin
    ws1.row_dimensions[r_op2].height = 28

    # Condiciones comerciales
    r_cond = r_op2 + 2
    ws1.cell(row=r_cond, column=2, value="CONDICIONES COMERCIALES, ALCANCE Y VISITA TÉCNICA").font = font_sec
    cond_items = [
        ("Visita técnica:", "Ofrecemos visita a la propiedad en Menorca para medir hueco, revisar pilares/suelo, evaluar exposición salina y definir presupuesto definitivo."),
        ("Forma de pago:", DATA["forma_pago"]),
        ("Plazo de ejecución:", DATA["plazo_entrega"]),
        ("Validez orientativa:", f"{DATA['validez_dias']} días naturales desde la fecha de emisión."),
        ("Exclusiones:", "Obra civil/pilares de piedra o albañilería, retirada de puerta antigua, motorización eléctrica/portero, tasas o licencias."),
    ]
    for c_i, (k_c, v_c) in enumerate(cond_items, start=r_cond + 1):
        ws1.cell(row=c_i, column=2, value=k_c).font = font_bold
        c_val = ws1.cell(row=c_i, column=3, value=v_c)
        c_val.font = font_reg
        c_val.alignment = Alignment(wrap_text=True, vertical="center")
        ws1.row_dimensions[c_i].height = 22

    ws1.column_dimensions["B"].width = 16
    ws1.column_dimensions["C"].width = 68
    ws1.column_dimensions["D"].width = 13
    ws1.column_dimensions["E"].width = 15
    ws1.column_dimensions["F"].width = 18
    ws1.column_dimensions["G"].width = 18

    # -------------------------------------------------------------
    # HOJA 2: ESTUDIO COSTES INTERNO
    # -------------------------------------------------------------
    ws2 = wb.create_sheet("Estudio Costes Interno")
    ws2.views.sheetView[0].showGridLines = True

    ws2["B2"] = f"ESTUDIO TÉCNICO Y ECONÓMICO INTERNO — {DATA['codigo']} (HAM ESTRUCTURAS METÁLICAS)"
    ws2["B2"].font = font_title
    ws2["B3"] = "Puerta Doble Hoja Forja Láser 10 mm Inox 304 (Opción Alternativa Inox 316) — Kenneth Byrne (Menorca)"
    ws2["B3"].font = font_sub

    headers_int = ["ID", "Concepto de Coste", "Descripción Técnica / Operativa", "Ud.", "Cant.", "Coste Unit.", "Coste Total", "Origen / Justificación"]
    for c_idx, h in enumerate(headers_int, start=2):
        cell = ws2.cell(row=5, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws2.row_dimensions[5].height = 24

    r_c = 6
    for item in DATA["costes_internos"]:
        ws2.cell(row=r_c, column=2, value=item["id"]).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_c, column=2).font = font_bold
        ws2.cell(row=r_c, column=3, value=item["concepto"]).font = font_bold
        c_d = ws2.cell(row=r_c, column=4, value=item["descripcion"])
        c_d.font = font_reg
        c_d.alignment = Alignment(wrap_text=True, vertical="center")
        ws2.cell(row=r_c, column=5, value=item["unidad"]).alignment = Alignment(horizontal="center")

        c_q = ws2.cell(row=r_c, column=6, value=item["cantidad"])
        c_q.alignment = Alignment(horizontal="right")
        c_q.number_format = "#,##0.00"

        c_u = ws2.cell(row=r_c, column=7, value=item["coste_unitario"])
        c_u.number_format = '#,##0.00 "€"'
        c_u.fill = fill_edit
        c_u.font = font_bold

        c_t = ws2.cell(row=r_c, column=8, value=f"=F{r_c}*G{r_c}")
        c_t.number_format = '#,##0.00 "€"'
        c_t.font = font_bold

        ws2.cell(row=r_c, column=9, value=item["origen"]).font = font_reg

        for col in range(2, 10):
            ws2.cell(row=r_c, column=col).border = border_thin
        ws2.row_dimensions[r_c].height = 28
        r_c += 1

    # Row 16: Total Coste Directo Base 304
    r_cd304 = r_c
    ws2.cell(row=r_cd304, column=7, value="COSTE DIRECTO BASE (304):").font = font_tot
    c_tot_cost = ws2.cell(row=r_cd304, column=8, value=f"=SUM(H6:H{r_c-1})")
    c_tot_cost.font = font_tot
    c_tot_cost.fill = fill_sub
    c_tot_cost.number_format = '#,##0.00 "€"'
    c_tot_cost.border = border_total

    # Desglose Suplemento 316
    r_s = r_cd304 + 2  # row 18
    ws2.cell(row=r_s, column=2, value="SUPLEMENTO INTERNO PARA CALIDAD MARINA AISI 316 (C5-M)").font = font_sec
    sup_rows = [
        ("S01", "Suplemento chapa 10 mm AISI 316 corte láser CNC", "Diferencial material chapa 10 mm 316 vs 304 (~138 kg brutos)", "lote", 1.0, DATA["suplemento_316"]["desglose_interno"]["chapa_10mm_316"], "Estimado Recam Laser"),
        ("S02", "Suplemento perfilería estructural AISI 316", "Tubos 40x40x2, 40x20x2, barra maciza 14x14 y pletinas en 316", "lote", 1.0, DATA["suplemento_316"]["desglose_interno"]["perfileria_316"], "Tarifa perfiles inox 316"),
        ("S03", "Suplemento herrajes y consumibles AISI 316 / A4", "Bisagras, cerradura, pasador y tornillería integral en 316/A4", "lote", 1.0, DATA["suplemento_316"]["desglose_interno"]["herrajes_316_a4"], "Ferretería marina A4"),
    ]
    r_scur = r_s + 1
    for sr in sup_rows:
        ws2.cell(row=r_scur, column=2, value=sr[0]).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_scur, column=2).font = font_bold
        ws2.cell(row=r_scur, column=3, value=sr[1]).font = font_bold
        ws2.cell(row=r_scur, column=4, value=sr[2]).font = font_reg
        ws2.cell(row=r_scur, column=5, value=sr[3]).alignment = Alignment(horizontal="center")
        c_sq = ws2.cell(row=r_scur, column=6, value=sr[4])
        c_sq.number_format = "#,##0.00"
        c_su = ws2.cell(row=r_scur, column=7, value=sr[5])
        c_su.number_format = '#,##0.00 "€"'
        c_su.fill = fill_edit
        c_su.font = font_bold
        c_st = ws2.cell(row=r_scur, column=8, value=f"=F{r_scur}*G{r_scur}")
        c_st.number_format = '#,##0.00 "€"'
        c_st.font = font_bold
        ws2.cell(row=r_scur, column=9, value=sr[6]).font = font_reg
        for col in range(2, 10):
            ws2.cell(row=r_scur, column=col).border = border_thin
        r_scur += 1

    r_sup_tot = r_scur
    ws2.cell(row=r_sup_tot, column=7, value="SUPLEMENTO COSTE (316):").font = font_bold
    c_st_tot = ws2.cell(row=r_sup_tot, column=8, value=f"=SUM(H{r_s+1}:H{r_scur-1})")
    c_st_tot.font = font_bold
    c_st_tot.number_format = '#,##0.00 "€"'
    c_st_tot.border = border_thin

    r_cd316 = r_sup_tot + 1
    ws2.cell(row=r_cd316, column=7, value="COSTE DIRECTO TOTAL (316):").font = font_tot
    c_316_tot = ws2.cell(row=r_cd316, column=8, value=f"=H{r_cd304}+H{r_sup_tot}")
    c_316_tot.font = font_tot
    c_316_tot.fill = fill_sub
    c_316_tot.number_format = '#,##0.00 "€"'
    c_316_tot.border = border_total

    # Resumen de Rentabilidad Comparativa
    r_k = r_cd316 + 2
    ws2.cell(row=r_k, column=2, value="RESUMEN ECONÓMICO Y RENTABILIDAD COMPARATIVA").font = font_sec
    k_headers = ["Indicador Económico", "Opción Base (AISI 304)", "Opción Marina (AISI 316)", "Observaciones"]
    for idx_h, h_txt in enumerate(k_headers, start=2):
        col_i = idx_h if idx_h <= 2 else (idx_h + 1 if idx_h <= 4 else 6)
    # Use contiguous cols 3..6 for clean table
    col_map = [3, 4, 5, 6]
    for col_i, h_txt in zip(col_map, k_headers):
        cell = ws2.cell(row=r_k + 1, column=col_i, value=h_txt)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin

    kpis = [
        ("Coste Directo Estimado (Taller + Subcontratas + Obra)", f"=H{r_cd304}", f"=H{r_cd316}", '#,##0.00 "€"', "Incluye 55 h totales + corte láser 10 mm"),
        ("Base Imponible Venta Cliente", f"='Presupuesto Cliente'!G{r_tot}", f"='Presupuesto Cliente'!E{r_op2}", '#,##0.00 "€"', "Precios orientativos sujetos a medición y DXF"),
        ("Beneficio Bruto Comercial (€)", f"=D{r_k+3}-D{r_k+2}", f"=E{r_k+3}-E{r_k+2}", '#,##0.00 "€"', "Margen absoluto de contribución"),
        ("Margen Bruto sobre Venta (%)", f"=D{r_k+4}/D{r_k+3}", f"=E{r_k+4}/E{r_k+3}", "0.00%", "Objetivo herrería/puertas especiales: ~35-42%"),
        ("Margen Industrial sobre Coste (%)", f"=D{r_k+4}/D{r_k+2}", f"=E{r_k+4}/E{r_k+2}", "0.00%", "Markup industrial sobre coste directo"),
        ("IVA Repercutido (21%)", f"=D{r_k+3}*0.21", f"=E{r_k+3}*0.21", '#,##0.00 "€"', "IVA Régimen General"),
        ("Total Presupuesto Cliente (IVA Incl.)", f"=D{r_k+3}+D{r_k+7}", f"=E{r_k+3}+E{r_k+7}", '#,##0.00 "€"', "Importe final cliente"),
    ]
    for offset, (lbl, f304, f316, numfmt, obs) in enumerate(kpis, start=2):
        rr = r_k + offset
        ws2.cell(row=rr, column=3, value=lbl).font = font_bold if offset in (3, 4, 5, 8) else font_reg
        c1 = ws2.cell(row=rr, column=4, value=f304)
        c1.number_format = numfmt
        c1.font = font_green if offset in (4, 5) else (font_tot_gold if offset == 8 else font_bold)
        c2 = ws2.cell(row=rr, column=5, value=f316)
        c2.number_format = numfmt
        c2.font = font_green if offset in (4, 5) else (font_tot_gold if offset == 8 else font_bold)
        ws2.cell(row=rr, column=6, value=obs).font = font_reg
        if offset == 8:
            c1.fill = fill_tot
            c2.fill = fill_tot
        for col_i in col_map:
            ws2.cell(row=rr, column=col_i).border = border_thin

    ws2.column_dimensions["B"].width = 8
    ws2.column_dimensions["C"].width = 36
    ws2.column_dimensions["D"].width = 48
    ws2.column_dimensions["E"].width = 22
    ws2.column_dimensions["F"].width = 24
    ws2.column_dimensions["G"].width = 16
    ws2.column_dimensions["H"].width = 16
    ws2.column_dimensions["I"].width = 34

    xlsx_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0064_Puerta_Forja_Laser_Inox_Kenneth_Byrne.xlsx")
    wb.save(xlsx_path)
    return xlsx_path


def create_html_and_pdf():
    tot304 = DATA["totales_base_304"]
    tot316 = DATA["totales_alternativa_316"]
    med = DATA["proyecto"]["medidas_aprox"]
    pesos = DATA["proyecto"]["pesos_estimados"]

    items_html = ""
    for p in DATA["partidas_cliente"]:
        items_html += f"""
      <tr>
        <td class="center bold">{p['id']}</td>
        <td>
          <strong>{p['concepto']}</strong>
          <span class="desc">{p['descripcion']}</span>
        </td>
        <td class="center">{p['unidad']}</td>
        <td class="right bold">{p['cantidad']:.2f}</td>
        <td class="right">{eur(p['precio_unitario'])}</td>
        <td class="right bold">{eur(p['subtotal'])}</td>
      </tr>"""

    specs_html = "".join(f"<li>{s}</li>" for s in DATA["proyecto"]["especificaciones_tecnicas"])
    inc_html = "".join(f"<li>{s}</li>" for s in DATA["incluidos"])
    exc_html = "".join(f"<li>{s}</li>" for s in DATA["exclusiones"])

    # 1. HTML CLIENTE (cero menciones a "horno" o "termolacado", cero costes/márgenes internos)
    html_cliente = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presupuesto Orientativo {DATA['codigo']} — Puerta Doble Hoja Forja Inox 304 · Kenneth Byrne</title>
  <style>
    @page {{ size: A4 portrait; margin: 9mm 11mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, Helvetica, sans-serif; color: #1e293b; margin: 0; font-size: 8.8pt; line-height: 1.32; background: #fff; }}
    .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #0f172a; padding-bottom: 7px; margin-bottom: 9px; }}
    .brand-group {{ display: flex; align-items: center; gap: 11px; }}
    .logo {{ width: 42px; height: 42px; filter: brightness(0) saturate(100%); }}
    .subbrand {{ font-size: 7.5pt; color: #b45309; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }}
    .brand {{ font-size: 13pt; font-weight: 800; color: #0f172a; margin-top: 1px; }}
    .company-info {{ text-align: right; font-size: 7.6pt; color: #475569; line-height: 1.28; }}
    h1 {{ font-size: 10.6pt; color: #0f172a; margin: 0 0 6px 0; font-weight: 800; }}
    .banner-ori {{ background: #fffbeb; border-left: 4px solid #b45309; padding: 6px 9px; font-size: 8.2pt; margin-bottom: 9px; color: #78350f; }}
    table.meta {{ width: 100%; border-collapse: collapse; margin-bottom: 9px; font-size: 8.1pt; }}
    table.meta td {{ padding: 3.5px 6px; border: 1px solid #cbd5e1; }}
    table.meta td.lbl {{ background: #f1f5f9; font-weight: 700; width: 17%; color: #334155; }}
    .tech-grid {{ display: grid; grid-template-columns: 1.45fr 0.85fr; gap: 10px; margin-bottom: 10px; align-items: stretch; }}
    .tech-box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 7px 9px; }}
    .tech-box h2 {{ margin: 0 0 4px 0; font-size: 8.6pt; color: #0f172a; border-bottom: 1.5px solid #b45309; padding-bottom: 2px; text-transform: uppercase; }}
    .tech-box p {{ margin: 0 0 5px 0; font-size: 8pt; color: #334155; }}
    .tech-box ul {{ margin: 3px 0 0 15px; padding: 0; font-size: 7.8pt; color: #1e293b; }}
    .tech-box li {{ margin-bottom: 2px; }}
    .img-box {{ border: 1px solid #cbd5e1; border-radius: 4px; padding: 6px; background: #fff; text-align: center; display: flex; flex-direction: column; justify-content: center; }}
    .img-box img {{ max-width: 100%; max-height: 205px; object-fit: contain; margin: 0 auto; display: block; }}
    .img-cap {{ font-size: 7.3pt; color: #475569; margin-top: 4px; line-height: 1.25; }}
    table.items {{ width: 100%; border-collapse: collapse; margin-bottom: 9px; page-break-inside: auto; }}
    table.items tr {{ page-break-inside: avoid; }}
    table.items th {{ background: #0f172a; color: #fff; padding: 5px 6px; font-size: 8pt; text-align: left; }}
    table.items td {{ padding: 5px 6px; border-bottom: 1px solid #cbd5e1; vertical-align: top; font-size: 8.1pt; }}
    .desc {{ font-size: 7.5pt; color: #475569; margin-top: 2px; line-height: 1.28; display: block; }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; white-space: nowrap; }}
    .bold {{ font-weight: 700; }}
    .totals-wrap {{ display: flex; justify-content: flex-end; margin-bottom: 9px; page-break-inside: avoid; }}
    table.totals {{ width: 46%; border-collapse: collapse; }}
    table.totals td {{ padding: 4px 8px; border: 1px solid #cbd5e1; font-size: 8.4pt; }}
    table.totals .grand {{ background: #fef3c7; font-weight: 800; font-size: 9.6pt; color: #0f172a; }}
    .opt-box {{ margin-bottom: 9px; page-break-inside: avoid; }}
    .opt-box h3 {{ margin: 0 0 4px 0; font-size: 8.4pt; color: #0f172a; text-transform: uppercase; letter-spacing: 0.03em; }}
    table.opts {{ width: 100%; border-collapse: collapse; font-size: 7.9pt; }}
    table.opts th {{ background: #334155; color: #fff; padding: 4.5px 6px; text-align: left; }}
    table.opts td {{ padding: 4.5px 6px; border: 1px solid #cbd5e1; vertical-align: middle; }}
    table.opts tr.alt {{ background: #f8fafc; }}
    .conds {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 7px 9px; font-size: 7.7pt; page-break-inside: avoid; }}
    .conds h3 {{ margin: 0 0 4px 0; font-size: 8.2pt; color: #0f172a; text-transform: uppercase; letter-spacing: 0.03em; }}
    .conds-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    .conds ul {{ margin: 2px 0 0 15px; padding: 0; }}
    .conds li {{ margin-bottom: 2px; }}
    .cond-bar {{ margin-top: 6px; padding-top: 5px; border-top: 1px solid #cbd5e1; font-size: 7.7pt; }}
    .footer-note {{ margin-top: 7px; font-size: 7.2pt; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 4px; }}
    .page-break {{ page-break-before: always; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand-group">
      <img src="logo-ham.svg" class="logo" alt="HAM">
      <div>
        <div class="subbrand">DIXIS RECURSOS Y SOLUCIONES S.L. · CIF B57825432</div>
        <div class="brand">HAM ESTRUCTURAS METÁLICAS MENORCA</div>
      </div>
    </div>
    <div class="company-info">
      Av. Circunval·lació, 11 · Pol. Ind. Sant Lluís, 07710 (Menorca)<br>
      Tel: +34 971 35 20 18 · WhatsApp: +34 669 769 541<br>
      info@hamenorca.com · www.hamenorca.com
    </div>
  </div>

  <h1>PRESUPUESTO ORIENTATIVO {DATA['codigo']} — PUERTA DE DOBLE HOJA ESTILO FORJA EN ACERO INOXIDABLE</h1>
  <div class="banner-ori">
    <strong>PRESUPUESTO ORIENTATIVO SUJETO A VISITA TÉCNICA:</strong> Valoración aproximada para fabricación, acabado e instalación en Menorca según fotografía y medidas facilitadas (≈ 1,83 × 1,52/1,83 m). Incluye desplazamiento a la propiedad para toma de medidas exactas, comprobación de pilares y emisión de oferta definitiva cerrada.
  </div>

  <table class="meta">
    <tr>
      <td class="lbl">Cliente</td>
      <td><strong>{DATA['cliente']['nombre']}</strong></td>
      <td class="lbl">Referencia</td>
      <td><strong>{DATA['referencia']}</strong></td>
    </tr>
    <tr>
      <td class="lbl">Ubicación obra</td>
      <td>{DATA['cliente']['ubicacion']}</td>
      <td class="lbl">Fecha / Validez</td>
      <td>{DATA['fecha']} · {DATA['validez_dias']} días</td>
    </tr>
    <tr>
      <td class="lbl">Dimensiones aprox.</td>
      <td colspan="3">Ancho total: {med['ancho_total']} · Altura laterales: {med['altura_laterales']} · Altura máx. centro: {med['altura_centro']}</td>
    </tr>
  </table>

  <div class="tech-grid">
    <div class="tech-box">
      <h2>Solución Técnica Recomendada para Menorca</h2>
      <p>{DATA['proyecto']['justificacion_menorca']}</p>
      <ul>{specs_html}</ul>
    </div>
    <div class="img-box">
      <img src="referencia-diseno-cliente.png" alt="Referencia diseño puerta doble hoja">
      <div class="img-cap">
        <strong>Diseño de referencia facilitado por el cliente</strong><br>
        Adornos estilo forja clásica ejecutados mediante corte láser CNC en placa maciza de acero inoxidable de 10 mm sobre bastidor inox 304 acabado en negro exterior.
      </div>
    </div>
  </div>

  <table class="items">
    <thead>
      <tr>
        <th class="center" style="width:5%">Nº</th>
        <th style="width:57%">Concepto y Descripción Técnica</th>
        <th class="center" style="width:6%">Ud.</th>
        <th class="right" style="width:8%">Cant.</th>
        <th class="right" style="width:12%">Precio Ud.</th>
        <th class="right" style="width:12%">Subtotal</th>
      </tr>
    </thead>
    <tbody>
      {items_html}
    </tbody>
  </table>

  <div class="totals-wrap">
    <table class="totals">
      <tr>
        <td class="bold">Base Imponible (Opción Base AISI 304)</td>
        <td class="right bold">{eur(tot304['base_imponible'])}</td>
      </tr>
      <tr>
        <td>IVA Régimen General (21%)</td>
        <td class="right">{eur(tot304['iva_importe'])}</td>
      </tr>
      <tr class="grand">
        <td>TOTAL PRESUPUESTO ORIENTATIVO</td>
        <td class="right">{eur(tot304['total_con_iva'])}</td>
      </tr>
    </table>
  </div>

  <div class="opt-box">
    <h3>Opciones de Calidad de Acero Inoxidable (A confirmar según proximidad al mar en visita técnica)</h3>
    <table class="opts">
      <thead>
        <tr>
          <th style="width:18%">Opción</th>
          <th style="width:46%">Especificación y Uso Recomendado en Menorca</th>
          <th class="right" style="width:12%">Base Imp.</th>
          <th class="right" style="width:11%">IVA (21%)</th>
          <th class="right" style="width:13%">Total IVA Inc.</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="bold">Opción Base (AISI 304)</td>
          <td>Puerta completa, adornos láser 10 mm y herrajes en Inox AISI 304 con acabado bicomponente negro. Apta para exterior general e interior de la isla.</td>
          <td class="right bold">{eur(tot304['base_imponible'])}</td>
          <td class="right">{eur(tot304['iva_importe'])}</td>
          <td class="right bold">{eur(tot304['total_con_iva'])}</td>
        </tr>
        <tr class="alt">
          <td class="bold">Opción Marina (AISI 316)</td>
          <td>Suplemento (+{eur(DATA['suplemento_316']['suplemento_venta_bi'])} + IVA) para fabricación íntegra en Inox AISI 316 Calidad Marina C5-M (primera línea de mar o exposición salina directa).</td>
          <td class="right bold">{eur(tot316['base_imponible'])}</td>
          <td class="right">{eur(tot316['iva_importe'])}</td>
          <td class="right bold">{eur(tot316['total_con_iva'])}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="conds">
    <div class="conds-grid">
      <div>
        <h3>Alcance Incluido</h3>
        <ul>{inc_html}</ul>
      </div>
      <div>
        <h3>No Incluido / Exclusiones</h3>
        <ul>{exc_html}</ul>
      </div>
    </div>
    <div class="cond-bar">
      <strong>Condiciones comerciales:</strong> <strong>Visita técnica:</strong> Incluida y disponible bajo cita previa en Menorca ·
      <strong>Plazo estimado:</strong> {DATA['plazo_entrega']} ·
      <strong>Forma de pago:</strong> {DATA['forma_pago']} ·
      <strong>Validez:</strong> {DATA['validez_dias']} días naturales.
    </div>
  </div>

  <div class="footer-note">
    HAM Estructuras Metálicas Menorca · Dixis Recursos y Soluciones S.L. · CIF: B57825432 · Av. Circunval·lació 11, Pol. Sant Lluís, 07710 Menorca
  </div>
</body>
</html>
"""

    # 2. HTML INTERNO TÉCNICO (A4 landscape)
    cost_rows_html = ""
    for item in DATA["costes_internos"]:
        cost_rows_html += f"""
          <tr>
            <td class="center bold">{item['id']}</td>
            <td class="bold">{item['concepto']}</td>
            <td>{item['descripcion']}</td>
            <td class="center">{item['unidad']}</td>
            <td class="right">{item['cantidad']:.2f}</td>
            <td class="right">{eur(item['coste_unitario'])}</td>
            <td class="right bold">{eur(item['coste_total'])}</td>
            <td>{item['origen']}</td>
          </tr>"""

    riesgos_html = "".join(f"<li>{r}</li>" for r in DATA["analisis_interno"]["riesgos"])
    comp_html = "".join(f"<li>{f}</li>" for f in DATA["analisis_interno"]["complejidad"]["factores"])
    chk_html = "".join(f"<li>{c}</li>" for c in DATA["analisis_interno"]["checklist_visita_obra"])

    html_interno = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Estudio Interno Técnico {DATA['codigo']} — Puerta Forja Láser 10 mm Inox 304 · Kenneth Byrne</title>
  <style>
    @page {{ size: A4 landscape; margin: 6mm 8mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; margin: 0; font-size: 7.3pt; line-height: 1.18; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0f172a; padding-bottom: 3px; margin-bottom: 4px; }}
    .brand {{ font-size: 9.8pt; font-weight: 800; color: #0f172a; }}
    .tag {{ background: #0f172a; color: #fff; padding: 1.5px 5px; font-size: 6.8pt; font-weight: 700; border-radius: 3px; }}
    .tag-warn {{ background: #b45309; }}
    h1 {{ font-size: 9.4pt; color: #0f172a; margin: 0 0 3px 0; }}
    h2 {{ font-size: 7.6pt; color: #0f172a; margin: 4px 0 2px 0; border-bottom: 1.5px solid #b45309; padding-bottom: 1px; text-transform: uppercase; }}
    .banner {{ background: #fef3c7; border-left: 4px solid #b45309; padding: 3.5px 6px; font-size: 7.1pt; color: #78350f; margin-bottom: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 4px; font-size: 6.9pt; }}
    th {{ background: #0f172a; color: #fff; padding: 3px 3.5px; font-size: 6.7pt; text-align: left; white-space: nowrap; }}
    td {{ padding: 2.1px 3.5px; border-bottom: 1px solid #cbd5e1; vertical-align: top; }}
    .right {{ text-align: right; white-space: nowrap; }}
    .center {{ text-align: center; white-space: nowrap; }}
    .bold {{ font-weight: 700; }}
    .green {{ color: #15803d; font-weight: 700; }}
    .tot {{ background: #fef3c7; font-weight: 800; }}
    .grid-2 {{ display: grid; grid-template-columns: 1.62fr 1fr; gap: 8px; }}
    .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 7px; margin-top: 3px; page-break-inside: avoid; }}
    .card {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 4px 6px; font-size: 6.6pt; border-radius: 4px; line-height: 1.15; }}
    .card h3 {{ margin: 0 0 2px 0; font-size: 7pt; color: #0f172a; text-transform: uppercase; }}
    .card ul {{ margin: 1.5px 0 0 12px; padding: 0; }}
    .card li {{ margin-bottom: 1px; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand">HAM ESTRUCTURAS METÁLICAS · DOCUMENTO INTERNO DE COSTES, PESOS Y PRODUCCIÓN</div>
    <div><span class="tag tag-warn">ORIENTATIVO · SIN VISITA</span> <span class="tag">USO INTERNO EXCLUSIVO</span> <span class="tag">{DATA['codigo']}</span></div>
  </div>

  <h1>ESTUDIO ECONÓMICO Y TÉCNICO: PUERTA DOBLE HOJA ESTILO FORJA LÁSER 10 MM INOX AISI 304 (≈ 1,83 × 1,52/1,83 M)</h1>
  <div class="banner">
    <strong>CLIENTE: {DATA['cliente']['nombre']} ({DATA['cliente']['ubicacion']})</strong> | Solución ofertada: estructura completa en <strong>AISI 304</strong> + adornos forja en <strong>placa 10 mm cortada a láser CNC</strong> + <strong>pintura epoxi + poliuretano 2C negro RAL 9005 (NUNCA al horno)</strong>. Peso estimado: <strong>~{pesos['peso_hoja_kg']:.0f} kg/hoja (~{pesos['peso_total_conjunto_kg']:.0f} kg total)</strong>. Venta base: <strong>{eur(tot304['base_imponible'])} + IVA</strong>.
  </div>

  <div class="grid-2">
    <div>
      <h2>1. Escandallo Detallado de Costes Directos Internos (Opción Base AISI 304)</h2>
      <table>
        <thead>
          <tr>
            <th class="center">ID</th>
            <th>Concepto de Coste</th>
            <th>Descripción Técnica / Operativa</th>
            <th class="center">Ud.</th>
            <th class="right">Cant.</th>
            <th class="right">Coste Ud.</th>
            <th class="right">Coste Total</th>
            <th>Origen / Proveedor</th>
          </tr>
        </thead>
        <tbody>
          {cost_rows_html}
          <tr class="tot">
            <td colspan="6" class="bold">COSTE DIRECTO TOTAL ESTIMADO (OPCIÓN BASE AISI 304):</td>
            <td class="right bold">{eur(tot304['coste_directo_total'])}</td>
            <td>55,0 h MO totales + subcontrata láser</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div>
      <h2>2. Rentabilidad Comercial Comparativa (304 vs 316)</h2>
      <table>
        <thead>
          <tr>
            <th>Concepto Económico</th>
            <th class="right">Base AISI 304</th>
            <th class="right">Marina AISI 316</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Coste Directo Estimado</td>
            <td class="right">{eur(tot304['coste_directo_total'])}</td>
            <td class="right">{eur(tot316['coste_directo_total'])}</td>
          </tr>
          <tr class="bold">
            <td>Base Imponible Venta Cliente</td>
            <td class="right">{eur(tot304['base_imponible'])}</td>
            <td class="right">{eur(tot316['base_imponible'])}</td>
          </tr>
          <tr class="green">
            <td>BENEFICIO BRUTO COMERCIAL</td>
            <td class="right">+{eur(tot304['beneficio_bruto'])}</td>
            <td class="right">+{eur(tot316['beneficio_bruto'])}</td>
          </tr>
          <tr class="green">
            <td>Margen Bruto sobre Venta (%)</td>
            <td class="right">{tot304['margen_sobre_venta_pct']:.2f}%</td>
            <td class="right">{tot316['margen_sobre_venta_pct']:.2f}%</td>
          </tr>
          <tr>
            <td>Margen Industrial sobre Coste (%)</td>
            <td class="right">+{tot304['margen_sobre_coste_pct']:.2f}%</td>
            <td class="right">+{tot316['margen_sobre_coste_pct']:.2f}%</td>
          </tr>
          <tr>
            <td>IVA (21%)</td>
            <td class="right">{eur(tot304['iva_importe'])}</td>
            <td class="right">{eur(tot316['iva_importe'])}</td>
          </tr>
          <tr class="tot">
            <td>TOTAL CLIENTE (IVA INCLUIDO)</td>
            <td class="right">{eur(tot304['total_con_iva'])}</td>
            <td class="right">{eur(tot316['total_con_iva'])}</td>
          </tr>
        </tbody>
      </table>

      <div class="card">
        <h3>Protocolo Taller, Pesos y Subcontrata Láser</h3>
        <ul>
          <li><strong>Suplemento directo AISI 316:</strong> +{eur(DATA['suplemento_316']['desglose_interno']['total_coste_suplemento'])} (chapa 10 mm +415 €, perfilería +250 €, herrajes +55 €) → venta +{eur(DATA['suplemento_316']['suplemento_venta_bi'])} + IVA.</li>
          <li><strong>Corte láser 10 mm:</strong> Chapa bruta ~1,75 m² (~{pesos['peso_bruto_chapa_10mm_kg']:.0f} kg brutos, ~{pesos['peso_neto_laser_10mm_kg']:.0f} kg netos). Enviar DXF a <strong>Recam Laser</strong> antes de cerrar pedido definitivo.</li>
          <li><strong>Norma Pintura HAM:</strong> Prohibido termolacado o pintura al horno. Realizar desengrasado, matizado mecánico/químico estricto (incluidos cantos cortados por láser con nitrógeno), imprimación epoxi fosfatante para inox y 2 capas de esmalte poliuretano 2C negro RAL 9005.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <h3>Complejidad (Puntuación: {DATA['analisis_interno']['complejidad']['puntuacion']} · {DATA['analisis_interno']['complejidad']['factor_recomendado']})</h3>
      <ul>{comp_html}</ul>
    </div>
    <div class="card">
      <h3>Riesgos Técnicos y Comerciales</h3>
      <ul>{riesgos_html}</ul>
    </div>
    <div class="card">
      <h3>Checklist Obligatorio en Visita Técnica</h3>
      <ul>{chk_html}</ul>
    </div>
  </div>
</body>
</html>
"""

    cli_html = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    int_html = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    cli_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    int_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")

    with open(cli_html, "w", encoding="utf-8") as f:
        f.write(html_cliente)
    with open(int_html, "w", encoding="utf-8") as f:
        f.write(html_interno)

    if os.path.exists(CHROME_PATH):
        for h_path, p_path in [(cli_html, cli_pdf), (int_html, int_pdf)]:
            subprocess.run(
                [
                    CHROME_PATH,
                    "--headless",
                    "--disable-gpu",
                    "--no-pdf-header-footer",
                    f"--print-to-pdf={p_path}",
                    h_path,
                ],
                check=False,
            )

    return cli_html, int_html, cli_pdf, int_pdf


def create_readme():
    tot304 = DATA["totales_base_304"]
    tot316 = DATA["totales_alternativa_316"]
    content = f"""# Presupuesto Orientativo {DATA['codigo']} — Puerta Exterior Doble Hoja Estilo Forja Láser 10 mm Inox AISI 304 (Kenneth Byrne)

## Datos Generales
- **Código:** {DATA['codigo']}
- **Referencia:** {DATA['referencia']}
- **Estado:** {DATA['estado_presupuesto']}
- **Cliente:** {DATA['cliente']['nombre']} ({DATA['cliente']['ubicacion']})
- **Fecha:** {DATA['fecha']}
- **Validez:** {DATA['validez_dias']} días naturales
- **Medidas aproximadas:** Ancho {DATA['proyecto']['medidas_aprox']['ancho_total']} · Laterales {DATA['proyecto']['medidas_aprox']['altura_laterales']} · Centro {DATA['proyecto']['medidas_aprox']['altura_centro']}

## Solución Técnica Ofertada
- **Estructura y perfilería:** Acero Inoxidable AISI 304 (bastidor tubo 40×40×2 mm curvado en arco, arco interior 40×20×2 mm, 12 barrotes macizos 14×14 mm, jambas de fijación y soldadura TIG decapada y pasivada).
- **Adornos estilo forja:** Cortados con láser CNC de precisión en **placa maciza de acero inoxidable de 10 mm de espesor** (crestería superior, cenefas curvas, rizos, anillas y zócalos).
- **Acabado exterior negro (norma HAM, sin horno):** Desengrasado y matizado del acero inoxidable + imprimación epoxi fosfatante especial adherencia inox + 2 capas de esmalte poliuretano alifático bicomponente negro exterior (RAL 9005).
- **Herrajes completos inox:** 6 bisagras reforzadas regulables, cerradura exterior inox con bombín europeo, manilla, pasador al suelo, cazoleta/tope y anclajes químicos A4.
- **Visita técnica:** Incluida disponibilidad de visita a la propiedad en Menorca para toma de medidas exactas, evaluación ambiental (AISI 304 vs AISI 316) y presupuesto definitivo.

## Resumen Económico

| Opción | Coste Directo | Base Imponible | IVA (21%) | Total IVA Inc. | Beneficio Bruto | Margen s/ Venta |
|---|---:|---:|---:|---:|---:|---:|
| **Opción Base (AISI 304)** | {eur(tot304['coste_directo_total'])} | **{eur(tot304['base_imponible'])}** | {eur(tot304['iva_importe'])} | **{eur(tot304['total_con_iva'])}** | +{eur(tot304['beneficio_bruto'])} | {tot304['margen_sobre_venta_pct']:.2f}% |
| **Opción Marina (AISI 316)** | {eur(tot316['coste_directo_total'])} | **{eur(tot316['base_imponible'])}** | {eur(tot316['iva_importe'])} | **{eur(tot316['total_con_iva'])}** | +{eur(tot316['beneficio_bruto'])} | {tot316['margen_sobre_venta_pct']:.2f}% |

## Archivos Generados
- `presupuesto-cliente.html` / `presupuesto-cliente.pdf`: Oferta orientativa limpia para enviar al cliente (incluye foto de referencia y comparativa AISI 304 vs AISI 316).
- `presupuesto-interno-tecnico.html` / `presupuesto-interno-tecnico.pdf`: Estudio interno de costes directos, pesos, riesgos y checklist de visita.
- `Presupuesto_P2026_0064_Puerta_Forja_Laser_Inox_Kenneth_Byrne.xlsx`: Hoja de cálculo con fórmulas activas (cliente + escandallo interno).
- `respuesta-email-cliente.md`: Borrador de correo electrónico listo para enviar a Kenneth Byrne.
- `datos.json`: Datos estructurados del presupuesto.
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    return readme_path


def create_email_draft():
    tot304 = DATA["totales_base_304"]
    tot316 = DATA["totales_alternativa_316"]
    content = f"""# Borrador de Respuesta por Email — Kenneth Byrne (`P-2026-0064`)

**Asunto:** Presupuesto orientativo puerta exterior doble hoja en acero inoxidable estilo forja (Menorca) — Ref. {DATA['codigo']}

---

Buenos días Kenneth,

Muchas gracias por su consulta y por enviarnos la fotografía de referencia junto con las medidas aproximadas.

Respecto a su pregunta sobre qué material y tratamiento recomendamos para garantizar la máxima durabilidad frente a la humedad, el viento y el ambiente salino de Menorca, le detallamos nuestra propuesta técnica:

### 1. Material y sistema de protección recomendado para Menorca
En un entorno insular como Menorca, el hierro forjado tradicional o acero al carbono acaba presentando oxidación con el tiempo en soldaduras, cantos y recovecos decorativos, especialmente con viento y salinidad ambiental. Por ello, nuestra recomendación es fabricar la puerta íntegramente en **Acero Inoxidable AISI 304**, combinando:
- **Adornos decorativos tipo forja cortados con láser CNC en placa maciza de acero inoxidable de 10 mm de espesor** (crestería superior, cenefas curvas, rizos, anillas y zócalos inferiores), logrando la presencia sólida y el diseño clásico de la forja artesanal pero sin puntos débiles frente a la corrosión.
- **Bastidores y barrotes estructurales en acero inoxidable AISI 304** soldados con tecnología TIG y sometidos a decapado y pasivado químico integral, además de **herrajes, bisagras reforzadas regulables, cerradura exterior y anclajes químicos en acero inoxidable**.
- **Acabado protector en negro exterior bicomponente:** preparación mediante desengrasado y matizado específico del acero inoxidable, aplicación de **imprimación epoxi fosfatante de alta adherencia especial para inoxidable** y **dos capas de acabado en esmalte de poliuretano alifático bicomponente negro (RAL 9005, satinado, mate o textura forja fina)** resistente a radiación UV, lluvia y brisa marina.

*(Nota técnica: si la propiedad se encontrara en primera línea de mar o con exposición salina directa severa, valoraríamos durante la visita utilizar **Acero Inoxidable AISI 316 calidad marina** como opción superior.)*

---

### 2. Presupuesto orientativo (fabricación, acabado e instalación en Menorca)
Adjuntamos el documento detallado (**{DATA['codigo']}**) para unas medidas aproximadas de **1,83 m de ancho total** (dos hojas de ~0,91 m), **1,52 m en laterales** y **1,83 m de altura máxima en el centro**:

- **Opción Base — Acero Inoxidable AISI 304** (adornos láser en placa de 10 mm, bastidores, herrajes inox, acabado negro epoxi + poliuretano 2C, transporte e instalación completa en propiedad):
  - **Base imponible:** **{eur(tot304['base_imponible'])}**
  - **IVA (21%):** {eur(tot304['iva_importe'])}
  - **Total orientativo (IVA incluido):** **{eur(tot304['total_con_iva'])}**

- **Opción Alternativa — Acero Inoxidable AISI 316 Calidad Marina** *(solo si la exposición al mar lo hiciera recomendable)*:
  - **Suplemento adicional:** +{eur(DATA['suplemento_316']['suplemento_venta_bi'])} + IVA
  - **Total orientativo AISI 316:** **{eur(tot316['base_imponible'])} + IVA** (**{eur(tot316['total_con_iva'])}** IVA incluido)

---

### 3. Visita técnica a la propiedad para medidas y presupuesto definitivo
**Sí, por supuesto.** Podemos desplazarnos a su propiedad en Menorca sin compromiso adicional dentro de la oferta para:
- Tomar las medidas exactas entre pilares y verificar niveles y sentido de apertura.
- Comprobar el estado y material de los pilares existentes (piedra, marés, hormigón o bloque) para definir el sistema de fijación más seguro.
- Evaluar la exposición al ambiente marino y confirmar si la calidad AISI 304 es suficiente o conviene optar por AISI 316.
- Definir los detalles finales del diseño de forja (que posteriormente plasmaremos en un plano CAD para su aprobación antes de fabricar) y entregarle el **presupuesto definitivo cerrado**.

Si le parece bien, puede indicarnos en qué zona de Menorca se encuentra la vivienda y qué días/horarios le vendrían mejor para concertar la visita.

Quedamos a su entera disposición para cualquier aclaración.

Un cordial saludo,

**HAM Estructuras Metálicas Menorca**
Dixis Recursos y Soluciones S.L. · CIF B57825432
Av. Circunval·lació, 11 · Polígono Industrial de Sant Lluís, 07710 Sant Lluís (Menorca)
Tel.: +34 971 35 20 18 · WhatsApp: +34 669 769 541
info@hamenorca.com · www.hamenorca.com
"""
    email_path = os.path.join(BASE_DIR, "respuesta-email-cliente.md")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(content)
    return email_path


if __name__ == "__main__":
    xlsx = create_excel()
    cli_h, int_h, cli_p, int_p = create_html_and_pdf()
    rd = create_readme()
    em = create_email_draft()
    print("Archivos generados con éxito:")
    for f in [xlsx, cli_h, cli_p, int_h, int_p, rd, em]:
        size = os.path.getsize(f) if os.path.exists(f) else 0
        print(f" - {f} ({size} bytes)")
