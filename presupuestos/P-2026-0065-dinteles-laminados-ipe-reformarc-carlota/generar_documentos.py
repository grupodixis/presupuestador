import os
import json
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def eur(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

# -------------------------------------------------------------------------
# GENERACIÓN DE EXCEL CON FÓRMULAS ACTIVAS
# -------------------------------------------------------------------------
def create_excel():
    wb = Workbook()

    NAVY = "0F172A"
    GOLD = "B45309"
    SLATE_LIGHT = "F8FAFC"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"
    GREEN_DARK = "15803D"

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")

    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
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
        bottom=Side(style="thin", color="CBD5E1")
    )
    border_total = Border(
        top=Side(style="thin", color=NAVY),
        bottom=Side(style="double", color=NAVY)
    )

    # -------------------------------------------------------------
    # HOJA 1: PRESUPUESTO CLIENTE
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Cliente"
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["A1"].font = font_title
    ws1["A2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. · CIF: B57825432 · Av. Circunval·lació 11, Sant Lluís (Menorca)"
    ws1["A2"].font = font_sub

    ws1["A4"] = f"PRESUPUESTO: {DATA['proyecto']['codigo']} — {DATA['proyecto']['referencia']}"
    ws1["A4"].font = font_sec

    # Bloque de metadatos
    meta_rows = [
        ("Cliente Fiscal:", f"{DATA['cliente']['nombre_fiscal']} (CIF: {DATA['cliente']['nif']})", "Fecha:", DATA['proyecto']['fecha']),
        ("Domicilio:", f"{DATA['cliente']['domicilio']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}", "Validez:", f"{DATA['proyecto']['validez_dias']} días naturales"),
        ("Contacto / Ref.:", f"{DATA['cliente']['referencia_contacto']} · {DATA['cliente']['email']}", "Plazo Entrega:", DATA['proyecto']['plazo_entrega']),
        ("Alcance Técnico:", "3 Dinteles compuestos en perfiles IPE taladrados con varilla pasante M12 e imprimados", "Condiciones:", DATA['proyecto']['forma_pago'])
    ]

    curr_row = 6
    for lbl1, val1, lbl2, val2 in meta_rows:
        ws1[f"A{curr_row}"] = lbl1
        ws1[f"A{curr_row}"].font = font_bold
        ws1[f"A{curr_row}"].fill = fill_sub
        ws1[f"B{curr_row}"] = val1
        ws1[f"B{curr_row}"].font = font_reg
        ws1.merge_cells(f"B{curr_row}:D{curr_row}")

        ws1[f"E{curr_row}"] = lbl2
        ws1[f"E{curr_row}"].font = font_bold
        ws1[f"E{curr_row}"].fill = fill_sub
        ws1[f"F{curr_row}"] = val2
        ws1[f"F{curr_row}"].font = font_reg

        for col_idx in range(1, 7):
            cell = ws1.cell(row=curr_row, column=col_idx)
            cell.border = border_thin
        curr_row += 1

    curr_row += 1

    # Tabla de partidas cliente
    headers_ws1 = ["Nº", "Código", "Concepto y Descripción Técnica", "Ud.", "Cantidad", "Precio Unit. (€)", "Importe (€)"]
    for idx, h in enumerate(headers_ws1, 1):
        cell = ws1.cell(row=curr_row, column=idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if idx in [1, 2, 4] else "left" if idx == 3 else "right", vertical="center")

    curr_row += 1
    start_items_row = curr_row

    for item in DATA["partidas_cliente"]:
        r = curr_row
        ws1[f"A{r}"] = item["num"]
        ws1[f"A{r}"].alignment = Alignment(horizontal="center", vertical="top")
        ws1[f"B{r}"] = item["codigo_partida"]
        ws1[f"B{r}"].alignment = Alignment(horizontal="center", vertical="top")

        # Texto con título y descripción
        ws1[f"C{r}"] = f"{item['concepto']}\n{item['descripcion']}"
        ws1[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")

        ws1[f"D{r}"] = item["unidad"]
        ws1[f"D{r}"].alignment = Alignment(horizontal="center", vertical="top")

        ws1[f"E{r}"] = item["cantidad"]
        ws1[f"E{r}"].alignment = Alignment(horizontal="right", vertical="top")
        ws1[f"E{r}"].number_format = "#,##0.00"

        ws1[f"F{r}"] = item["precio_unitario"]
        ws1[f"F{r}"].alignment = Alignment(horizontal="right", vertical="top")
        ws1[f"F{r}"].number_format = "#,##0.00 €"

        # Fórmula activa: Cantidad * Precio Unitario
        ws1[f"G{r}"] = f"=ROUND(E{r}*F{r}, 2)"
        ws1[f"G{r}"].alignment = Alignment(horizontal="right", vertical="top")
        ws1[f"G{r}"].number_format = "#,##0.00 €"
        ws1[f"G{r}"].font = font_bold

        for col_idx in range(1, 8):
            cell = ws1.cell(row=r, column=col_idx)
            cell.border = border_thin
            if r % 2 == 0:
                cell.fill = fill_alt

        ws1.row_dimensions[r].height = 68
        curr_row += 1

    end_items_row = curr_row - 1

    # Totales con fórmulas
    curr_row += 1
    r_sub = curr_row
    ws1[f"F{r_sub}"] = "BASE IMPONIBLE:"
    ws1[f"F{r_sub}"].font = font_tot
    ws1[f"F{r_sub}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_sub}"] = f"=SUM(G{start_items_row}:G{end_items_row})"
    ws1[f"G{r_sub}"].font = font_tot
    ws1[f"G{r_sub}"].number_format = "#,##0.00 €"
    ws1[f"G{r_sub}"].border = border_thin

    curr_row += 1
    r_iva = curr_row
    ws1[f"F{r_iva}"] = "I.V.A. (21%):"
    ws1[f"F{r_iva}"].font = font_bold
    ws1[f"F{r_iva}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_iva}"] = f"=ROUND(G{r_sub}*0.21, 2)"
    ws1[f"G{r_iva}"].font = font_bold
    ws1[f"G{r_iva}"].number_format = "#,##0.00 €"
    ws1[f"G{r_iva}"].border = border_thin

    curr_row += 1
    r_tot = curr_row
    ws1[f"F{r_tot}"] = "TOTAL PRESUPUESTO:"
    ws1[f"F{r_tot}"].font = font_tot_gold
    ws1[f"F{r_tot}"].alignment = Alignment(horizontal="right")
    ws1[f"G{r_tot}"] = f"=G{r_sub}+G{r_iva}"
    ws1[f"G{r_tot}"].font = font_tot_gold
    ws1[f"G{r_tot}"].fill = fill_tot
    ws1[f"G{r_tot}"].number_format = "#,##0.00 €"
    ws1[f"G{r_tot}"].border = border_total

    # Notas de pie
    curr_row += 2
    ws1[f"A{curr_row}"] = "CONDICIONES Y OBSERVACIONES COMERCIALES:"
    ws1[f"A{curr_row}"].font = font_bold
    curr_row += 1
    cond_texts = [
        "1. Material: Acero estructural laminado en caliente S275JR según norma UNE-EN 10025-2.",
        "2. Tratamiento: Limpieza mecánica profunda e imprimación anticorrosiva de taller de secado rápido (sin horno, norma estricta HAM).",
        "3. Tornillería incluida: Varillas roscadas M12 calidad 8.8 cincadas L=200 mm con tuercas hexagonales DIN 934 y arandelas DIN 9021.",
        "4. Perforaciones pasantes de Ø14 mm en alma de vigas ejecutadas a paso e=500 mm en taller.",
        "5. Transporte: Recogida en taller HAM (Pol. Ind. Sant Lluís) o porte a pie de obra en Menorca a coordinar.",
        "6. No se incluye montaje en obra ni trabajos de albañilería o apertura de muros.",
        "7. Forma de pago: 100% a la confirmación de pedido. Plazo de entrega estimado: 4-6 días laborables."
    ]
    for c in cond_texts:
        ws1[f"A{curr_row}"] = c
        ws1[f"A{curr_row}"].font = font_reg
        curr_row += 1

    # Ajuste de anchos de columna en ws1
    col_widths_ws1 = {1: 6, 2: 15, 3: 56, 4: 8, 5: 12, 6: 18, 7: 18}
    for c_idx, w in col_widths_ws1.items():
        ws1.column_dimensions[get_column_letter(c_idx)].width = w

    # -------------------------------------------------------------
    # HOJA 2: ESCANDALLO INTERNO Y COSTES
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Escandallo Interno")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "ESTUDIO TÉCNICO INTERNO Y ESCANDALLO DE COSTES"
    ws2["A1"].font = font_title
    ws2["A2"] = f"PROYECTO: {DATA['proyecto']['codigo']} · {DATA['proyecto']['referencia']} · REFORMARC & REFORNILLES SL"
    ws2["A2"].font = font_sub

    # Sección 1: Materiales y Suministros
    ws2["A4"] = "1. DESGLOSE DE COSTES DIRECTOS DE MATERIALES Y CONSUMIBLES"
    ws2["A4"].font = font_sec

    headers_mat = ["Concepto Material / Suministro", "Ud.", "Cantidad", "Coste Unit. (€)", "Coste Total (€)"]
    for idx, h in enumerate(headers_mat, 1):
        cell = ws2.cell(row=5, column=idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if idx == 2 else "right" if idx in [3, 4, 5] else "left")

    curr_row = 6
    start_mat_row = curr_row
    for m in DATA["escandallo_interno"]["resumen_materiales"]:
        r = curr_row
        ws2[f"A{r}"] = m["concepto"]
        ws2[f"A{r}"].font = font_reg
        ws2[f"B{r}"] = m["unidad"]
        ws2[f"B{r}"].alignment = Alignment(horizontal="center")
        ws2[f"B{r}"].font = font_reg
        ws2[f"C{r}"] = m["cantidad"]
        ws2[f"C{r}"].alignment = Alignment(horizontal="right")
        ws2[f"C{r}"].number_format = "#,##0.00"
        ws2[f"C{r}"].font = font_reg
        ws2[f"D{r}"] = m["coste_unitario"]
        ws2[f"D{r}"].alignment = Alignment(horizontal="right")
        ws2[f"D{r}"].number_format = "#,##0.00 €"
        ws2[f"D{r}"].font = font_reg
        ws2[f"E{r}"] = f"=ROUND(C{r}*D{r}, 2)"
        ws2[f"E{r}"].alignment = Alignment(horizontal="right")
        ws2[f"E{r}"].number_format = "#,##0.00 €"
        ws2[f"E{r}"].font = font_bold

        for c_idx in range(1, 6):
            ws2.cell(row=r, column=c_idx).border = border_thin
            if r % 2 == 0:
                ws2.cell(row=r, column=c_idx).fill = fill_alt
        curr_row += 1

    end_mat_row = curr_row - 1
    r_tot_mat = curr_row
    ws2[f"D{r_tot_mat}"] = "SUBTOTAL MATERIALES:"
    ws2[f"D{r_tot_mat}"].font = font_bold
    ws2[f"D{r_tot_mat}"].alignment = Alignment(horizontal="right")
    ws2[f"E{r_tot_mat}"] = f"=SUM(E{start_mat_row}:E{end_mat_row})"
    ws2[f"E{r_tot_mat}"].font = font_bold
    ws2[f"E{r_tot_mat}"].number_format = "#,##0.00 €"
    ws2[f"E{r_tot_mat}"].border = border_thin
    ws2[f"E{r_tot_mat}"].fill = fill_sub

    # Sección 2: Mano de Obra
    curr_row += 2
    ws2[f"A{curr_row}"] = "2. MANO DE OBRA DIRECTA EN TALLER (FABRICACIÓN Y ACABADO)"
    ws2[f"A{curr_row}"].font = font_sec
    curr_row += 1

    headers_mo = ["Operación / Categoría de Taller", "Ud.", "Horas", "Tarifa (€/h)", "Coste Total (€)"]
    for idx, h in enumerate(headers_mo, 1):
        cell = ws2.cell(row=curr_row, column=idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if idx == 2 else "right" if idx in [3, 4, 5] else "left")

    curr_row += 1
    start_mo_row = curr_row
    for mo in DATA["escandallo_interno"]["resumen_mano_obra"]:
        r = curr_row
        ws2[f"A{r}"] = mo["concepto"]
        ws2[f"A{r}"].font = font_reg
        ws2[f"B{r}"] = "h"
        ws2[f"B{r}"].alignment = Alignment(horizontal="center")
        ws2[f"B{r}"].font = font_reg
        ws2[f"C{r}"] = mo["horas"]
        ws2[f"C{r}"].alignment = Alignment(horizontal="right")
        ws2[f"C{r}"].number_format = "#,##0.00"
        ws2[f"C{r}"].font = font_reg
        ws2[f"D{r}"] = mo["tarifa_hora"]
        ws2[f"D{r}"].alignment = Alignment(horizontal="right")
        ws2[f"D{r}"].number_format = "#,##0.00 €"
        ws2[f"D{r}"].font = font_reg
        ws2[f"E{r}"] = f"=ROUND(C{r}*D{r}, 2)"
        ws2[f"E{r}"].alignment = Alignment(horizontal="right")
        ws2[f"E{r}"].number_format = "#,##0.00 €"
        ws2[f"E{r}"].font = font_bold

        for c_idx in range(1, 6):
            ws2.cell(row=r, column=c_idx).border = border_thin
            if r % 2 == 0:
                ws2.cell(row=r, column=c_idx).fill = fill_alt
        curr_row += 1

    end_mo_row = curr_row - 1
    r_tot_mo = curr_row
    ws2[f"D{r_tot_mo}"] = "SUBTOTAL MANO DE OBRA:"
    ws2[f"D{r_tot_mo}"].font = font_bold
    ws2[f"D{r_tot_mo}"].alignment = Alignment(horizontal="right")
    ws2[f"E{r_tot_mo}"] = f"=SUM(E{start_mo_row}:E{end_mo_row})"
    ws2[f"E{r_tot_mo}"].font = font_bold
    ws2[f"E{r_tot_mo}"].number_format = "#,##0.00 €"
    ws2[f"E{r_tot_mo}"].border = border_thin
    ws2[f"E{r_tot_mo}"].fill = fill_sub

    # Sección 3: Resumen Económico y Márgenes
    curr_row += 2
    ws2[f"A{curr_row}"] = "3. RENTABILIDAD Y MÁRGENES COMERCIALES"
    ws2[f"A{curr_row}"].font = font_sec
    curr_row += 1

    summary_rows = [
        ("COSTE DIRECTO TOTAL (Materiales + MO):", f"=E{r_tot_mat}+E{r_tot_mo}", False, False),
        ("PRECIO DE VENTA BASE (Sin IVA):", f"='Presupuesto Cliente'!G{r_sub}", False, False),
        ("BENEFICIO BRUTO CONTRIBUCIÓN (€):", f"=E{curr_row+1}-E{curr_row}", True, True),
        ("MARGEN BRUTO S/ VENTA (%):", f"=ROUND(E{curr_row+2}/E{curr_row+1}*100, 2)", True, False)
    ]

    r_c_dir = curr_row
    ws2[f"D{r_c_dir}"] = "COSTE DIRECTO TOTAL:"
    ws2[f"D{r_c_dir}"].font = font_bold
    ws2[f"D{r_c_dir}"].alignment = Alignment(horizontal="right")
    ws2[f"E{r_c_dir}"] = f"=E{r_tot_mat}+E{r_tot_mo}"
    ws2[f"E{r_c_dir}"].font = font_bold
    ws2[f"E{r_c_dir}"].number_format = "#,##0.00 €"
    ws2[f"E{r_c_dir}"].border = border_thin
    curr_row += 1

    r_p_vta = curr_row
    ws2[f"D{r_p_vta}"] = "PRECIO VENTA BASE (Sin IVA):"
    ws2[f"D{r_p_vta}"].font = font_bold
    ws2[f"D{r_p_vta}"].alignment = Alignment(horizontal="right")
    ws2[f"E{r_p_vta}"] = f"='Presupuesto Cliente'!G{r_sub}"
    ws2[f"E{r_p_vta}"].font = font_bold
    ws2[f"E{r_p_vta}"].number_format = "#,##0.00 €"
    ws2[f"E{r_p_vta}"].border = border_thin
    curr_row += 1

    r_b_bru = curr_row
    ws2[f"D{r_b_bru}"] = "BENEFICIO BRUTO (€):"
    ws2[f"D{r_b_bru}"].font = font_tot_gold
    ws2[f"D{r_b_bru}"].alignment = Alignment(horizontal="right")
    ws2[f"E{r_b_bru}"] = f"=E{r_p_vta}-E{r_c_dir}"
    ws2[f"E{r_b_bru}"].font = font_tot_gold
    ws2[f"E{r_b_bru}"].fill = fill_tot
    ws2[f"E{r_b_bru}"].number_format = "#,##0.00 €"
    ws2[f"E{r_b_bru}"].border = border_thin
    curr_row += 1

    r_m_pct = curr_row
    ws2[f"D{r_m_pct}"] = "MARGEN BRUTO S/ VENTA (%):"
    ws2[f"D{r_m_pct}"].font = font_green
    ws2[f"D{r_m_pct}"].alignment = Alignment(horizontal="right")
    ws2[f"E{r_m_pct}"] = f"=E{r_b_bru}/E{r_p_vta}"
    ws2[f"E{r_m_pct}"].font = font_green
    ws2[f"E{r_m_pct}"].fill = fill_tot
    ws2[f"E{r_m_pct}"].number_format = "0.00%"
    ws2[f"E{r_m_pct}"].border = border_total

    # Ajuste anchos en ws2
    col_widths_ws2 = {1: 45, 2: 8, 3: 12, 4: 25, 5: 18}
    for c_idx, w in col_widths_ws2.items():
        ws2.column_dimensions[get_column_letter(c_idx)].width = w

    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0065_Dinteles_Laminados_IPE_Reformarc_Carlota.xlsx")
    wb.save(excel_path)
    print(f"[OK] Excel guardado: {excel_path}")
    return excel_path


# -------------------------------------------------------------------------
# GENERACIÓN DE HTML CLIENTE
# -------------------------------------------------------------------------
def create_cliente_html():
    p = DATA["proyecto"]
    c = DATA["cliente"]
    e = DATA["emisor"]
    t = DATA["totales_economicos"]

    items_html = ""
    for item in DATA["partidas_cliente"]:
        items_html += f"""
        <tr>
          <td class="center bold">{item['num']}</td>
          <td class="center code">{item['codigo_partida']}</td>
          <td>
            <strong>{item['concepto']}</strong>
            <span class="desc">{item['descripcion']}</span>
          </td>
          <td class="center">{item['unidad']}</td>
          <td class="right">{item['cantidad']:,.2f}</td>
          <td class="right">{eur(item['precio_unitario'])}</td>
          <td class="right bold">{eur(item['importe'])}</td>
        </tr>
        """

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presupuesto {p['codigo']} — 3 Dinteles Laminados IPE · {c['nombre_fiscal']}</title>
  <style>
    @page {{ size: A4 portrait; margin: 10mm 12mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, Helvetica, sans-serif; color: #1e293b; margin: 0; font-size: 9.5pt; line-height: 1.35; background: #fff; }}
    .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #0f172a; padding-bottom: 8px; margin-bottom: 12px; }}
    .brand-group {{ display: flex; align-items: center; gap: 12px; }}
    .logo {{ width: 44px; height: 44px; }}
    .subbrand {{ font-size: 8pt; color: #b45309; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }}
    .brand {{ font-size: 13.5pt; font-weight: 800; color: #0f172a; margin-top: 1px; }}
    .company-info {{ text-align: right; font-size: 8pt; color: #475569; line-height: 1.3; }}
    h1 {{ font-size: 11pt; color: #0f172a; margin: 0 0 6px 0; font-weight: 800; text-transform: uppercase; }}
    .banner-def {{ background: #f0fdf4; border-left: 4px solid #16a34a; padding: 6px 10px; font-size: 8.5pt; margin-bottom: 10px; color: #166534; }}
    table.meta {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 8.5pt; }}
    table.meta td {{ padding: 4px 6px; border: 1px solid #cbd5e1; }}
    table.meta td.lbl {{ background: #f1f5f9; font-weight: 700; width: 18%; color: #334155; }}
    table.items {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; }}
    table.items th {{ background: #0f172a; color: #fff; padding: 6px; font-size: 8.5pt; text-align: left; }}
    table.items td {{ padding: 7px 6px; border-bottom: 1px solid #cbd5e1; vertical-align: top; font-size: 8.5pt; }}
    .desc {{ font-size: 8pt; color: #475569; margin-top: 4px; line-height: 1.35; display: block; }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .code {{ font-family: monospace; font-size: 8pt; color: #b45309; font-weight: 600; }}
    .totals-wrap {{ display: flex; justify-content: flex-end; margin-bottom: 12px; }}
    table.totals {{ width: 44%; border-collapse: collapse; }}
    table.totals td {{ padding: 4px 8px; border: 1px solid #cbd5e1; font-size: 8.5pt; }}
    table.totals .grand {{ background: #fef3c7; font-weight: 800; font-size: 10pt; color: #0f172a; }}
    .conds {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px 10px; font-size: 8pt; margin-top: 6px; }}
    .conds h3 {{ margin: 0 0 5px 0; font-size: 8.5pt; color: #0f172a; text-transform: uppercase; letter-spacing: 0.04em; }}
    .conds-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    .conds ul {{ margin: 2px 0 0 16px; padding: 0; }}
    .conds li {{ margin-bottom: 2px; }}
    .footer-note {{ margin-top: 8px; font-size: 7.5pt; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 4px; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand-group">
      <img src="logo-ham.svg" class="logo" alt="HAM">
      <div>
        <div class="subbrand">{e['razon_social']} · CIF {e['cif']}</div>
        <div class="brand">{e['marca_comercial']}</div>
      </div>
    </div>
    <div class="company-info">
      {e['domicilio']}<br>
      {e['codigo_postal']} {e['localidad']} ({e['provincia']})<br>
      Tel: {e['telefono']} · Móvil/WhatsApp: {e['movil']}<br>
      {e['email']} · {e['web']}
    </div>
  </div>

  <h1>PRESUPUESTO {p['codigo']} — FABRICACIÓN DE 3 DINTELES LAMINADOS IPE TALADRADOS E IMPRIMADOS</h1>
  <div class="banner-def">
    <strong>ALCANCE:</strong> Suministro, corte a medida, taladrado pasante en alma a paso 50 cm, suministro y cosido con varilla roscada M12 L=20 cm, arandelas y tuercas, e imprimación anticorrosiva en taller de 3 dinteles estructurales compuestos (2x IPE 160 2m, 2x IPE 160 3m, 2x IPE 240 2m).
  </div>

  <table class="meta">
    <tr>
      <td class="lbl">Cliente Fiscal</td>
      <td><strong>{c['nombre_fiscal']}</strong> (NIF: {c['nif']} · Cód. FactuSol: {c['codigo_factusol']})</td>
      <td class="lbl">Presupuesto Nº</td>
      <td><strong>{p['codigo']}</strong></td>
    </tr>
    <tr>
      <td class="lbl">Domicilio Fiscal</td>
      <td>{c['domicilio']}, {c['codigo_postal']} {c['poblacion']} ({c['provincia']})</td>
      <td class="lbl">Referencia</td>
      <td><strong>{p['referencia']}</strong></td>
    </tr>
    <tr>
      <td class="lbl">Atención / Ref.</td>
      <td><strong>{c['referencia_contacto']}</strong> · {c['email']}</td>
      <td class="lbl">Fecha Emisión</td>
      <td>{p['fecha']}</td>
    </tr>
    <tr>
      <td class="lbl">Destino / Entrega</td>
      <td>{c['destino_obra']} · {p['lugar_entrega']}</td>
      <td class="lbl">Validez Oferta</td>
      <td>{p['validez_dias']} días naturales</td>
    </tr>
  </table>

  <table class="items">
    <thead>
      <tr>
        <th class="center" style="width:4%">Nº</th>
        <th class="center" style="width:13%">Cód. Partida</th>
        <th style="width:51%">Concepto y Descripción Técnica</th>
        <th class="center" style="width:6%">Ud.</th>
        <th class="right" style="width:7%">Cant.</th>
        <th class="right" style="width:10%">Precio (€)</th>
        <th class="right" style="width:9%">Importe (€)</th>
      </tr>
    </thead>
    <tbody>
      {items_html}
    </tbody>
  </table>

  <div class="totals-wrap">
    <table class="totals">
      <tr>
        <td class="bold right">BASE IMPONIBLE:</td>
        <td class="right bold">{eur(t['base_imponible'])}</td>
      </tr>
      <tr>
        <td class="right">I.V.A. ({t['iva_porcentaje']}%):</td>
        <td class="right">{eur(t['iva_importe'])}</td>
      </tr>
      <tr class="grand">
        <td class="bold right">TOTAL PRESUPUESTO:</td>
        <td class="bold right">{eur(t['total_presupuesto'])}</td>
      </tr>
    </table>
  </div>

  <div class="conds">
    <h3>Condiciones Técnicas y Comerciales</h3>
    <div class="conds-grid">
      <div>
        <strong>Especificación de Fabricación:</strong>
        <ul>
          <li>Acero estructural laminado S275JR según norma UNE-EN 10025-2.</li>
          <li>Taladrado en alma con broca Ø14 mm a paso regular cada 50 cm.</li>
          <li>Varillas roscadas M12 de 200 mm de longitud cincadas calidad 8.8, con tuercas hexagonales DIN 934 y arandelas DIN 9021.</li>
          <li>Tratamiento de taller: Limpieza mecánica profunda e imprimación antioxidante de secado rápido (sin horno, norma estricta HAM).</li>
        </ul>
      </div>
      <div>
        <strong>Condiciones de Venta y Suministro:</strong>
        <ul>
          <li><strong>Plazo de entrega:</strong> {p['plazo_entrega']}.</li>
          <li><strong>Forma de pago:</strong> {p['forma_pago']}.</li>
          <li><strong>Disponibilidad:</strong> Entrega sobre camión en taller HAM (Sant Lluís) o transporte a obra a convenir.</li>
          <li><strong>Exclusiones:</strong> Colocación en obra, apeos, gatos, demolición de albañilería o retacado de hormigón.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="footer-note">
    Documento emitido por Dixis Recursos y Soluciones S.L. · HAM Estructuras Metálicas Menorca · CIF B57825432 · Inscrita en el R.M. de Menorca
  </div>
</body>
</html>"""

    html_path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTML Cliente guardado: {html_path}")
    return html_path


# -------------------------------------------------------------------------
# GENERACIÓN DE HTML TÉCNICO INTERNO
# -------------------------------------------------------------------------
def create_interno_html():
    p = DATA["proyecto"]
    c = DATA["cliente"]
    e = DATA["emisor"]
    t = DATA["totales_economicos"]
    esc = DATA["escandallo_interno"]

    mat_rows_html = ""
    for m in esc["resumen_materiales"]:
        mat_rows_html += f"""
        <tr>
          <td>{m['concepto']}</td>
          <td class="center">{m['unidad']}</td>
          <td class="right">{m['cantidad']:,.2f}</td>
          <td class="right">{eur(m['coste_unitario'])}</td>
          <td class="right bold">{eur(m['coste_total'])}</td>
        </tr>
        """

    mo_rows_html = ""
    for mo in esc["resumen_mano_obra"]:
        mo_rows_html += f"""
        <tr>
          <td>{mo['concepto']}</td>
          <td class="center">h</td>
          <td class="right">{mo['horas']:,.2f}</td>
          <td class="right">{eur(mo['tarifa_hora'])}</td>
          <td class="right bold">{eur(mo['coste_total'])}</td>
        </tr>
        """

    elems_html = ""
    for el in DATA["elementos"]:
        elems_html += f"""
        <tr>
          <td class="center bold">{el['id']}</td>
          <td>{el['descripcion']}</td>
          <td class="center bold">{el['tipo_perfil']}</td>
          <td class="right">{el['longitud_viga_m']:,.2f} m ({el['unidades_vigas']} uds)</td>
          <td class="right">{el['total_ml_perfil']:,.2f} ml</td>
          <td class="right">{el['peso_total_kg']:,.2f} kg</td>
          <td class="right">{el['superficie_total_m2']:,.2f} m²</td>
          <td class="center">{el['num_varillas_m12']} varillas ({el['num_taladros_totales']} tal.)</td>
          <td class="right bold">{eur(el['importe'])}</td>
        </tr>
        """

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Estudio Técnico Interno P-2026-0065 — Dinteles Laminados IPE (Reformarc)</title>
  <style>
    @page {{ size: A4 portrait; margin: 10mm 12mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, Helvetica, sans-serif; color: #1e293b; margin: 0; font-size: 9pt; line-height: 1.35; background: #fff; }}
    .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #b45309; padding-bottom: 8px; margin-bottom: 12px; }}
    .brand-group {{ display: flex; align-items: center; gap: 12px; }}
    .logo {{ width: 44px; height: 44px; }}
    .subbrand {{ font-size: 8pt; color: #b45309; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }}
    .brand {{ font-size: 13.5pt; font-weight: 800; color: #0f172a; margin-top: 1px; }}
    .company-info {{ text-align: right; font-size: 8pt; color: #475569; line-height: 1.3; }}
    h1 {{ font-size: 11pt; color: #b45309; margin: 0 0 6px 0; font-weight: 800; text-transform: uppercase; }}
    .badge-internal {{ background: #fef3c7; border: 1px solid #f59e0b; color: #92400e; font-size: 8pt; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }}
    table.meta {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 8.5pt; }}
    table.meta td {{ padding: 4px 6px; border: 1px solid #cbd5e1; }}
    table.meta td.lbl {{ background: #f1f5f9; font-weight: 700; width: 18%; color: #334155; }}
    h2 {{ font-size: 9.5pt; color: #0f172a; margin: 10px 0 4px 0; text-transform: uppercase; border-bottom: 1px solid #cbd5e1; padding-bottom: 2px; }}
    table.data {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 8pt; }}
    table.data th {{ background: #0f172a; color: #fff; padding: 5px; text-align: left; }}
    table.data td {{ padding: 5px 6px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .tot-row {{ background: #f8fafc; font-weight: 700; }}
    .rent-box {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px; margin-top: 10px; margin-bottom: 12px; }}
    .rent-card {{ border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px; text-align: center; background: #f8fafc; }}
    .rent-card.highlight {{ background: #fef3c7; border-color: #f59e0b; }}
    .rent-card.green {{ background: #f0fdf4; border-color: #16a34a; }}
    .rent-title {{ font-size: 7.5pt; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 4px; }}
    .rent-val {{ font-size: 12pt; font-weight: 800; color: #0f172a; }}
    .rent-val.green {{ color: #15803d; }}
    .rent-val.gold {{ color: #b45309; }}
    .footer-note {{ margin-top: 8px; font-size: 7.5pt; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 4px; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand-group">
      <img src="logo-ham.svg" class="logo" alt="HAM">
      <div>
        <div class="subbrand">{e['razon_social']} · CIF {e['cif']}</div>
        <div class="brand">{e['marca_comercial']}</div>
      </div>
    </div>
    <div class="company-info">
      OFICINA TÉCNICA Y TALLER DE FABRICACIÓN<br>
      Sant Lluís · Menorca<br>
      Documento Confidencial de Uso Interno
    </div>
  </div>

  <span class="badge-internal">USO INTERNO / NO ENTREGAR AL CLIENTE · ESCANDALLO Y ESTUDIO TÉCNICO</span>
  <h1>ESTUDIO TÉCNICO Y ESCANDALLO: {p['codigo']} — 3 DINTELES IPE (REFORMARC / CARLOTA)</h1>

  <table class="meta">
    <tr>
      <td class="lbl">Cliente</td>
      <td><strong>{c['nombre_fiscal']}</strong> (NIF: {c['nif']} · FactuSol: {c['codigo_factusol']})</td>
      <td class="lbl">Proyecto</td>
      <td><strong>{p['codigo']}</strong> ({p['referencia']})</td>
    </tr>
    <tr>
      <td class="lbl">Atención / Ref.</td>
      <td>{c['referencia_contacto']} · {c['email']}</td>
      <td class="lbl">Fecha</td>
      <td>{p['fecha']}</td>
    </tr>
  </table>

  <h2>1. Desglose Físico y Dimensional de los 3 Dinteles Compuestos</h2>
  <table class="data">
    <thead>
      <tr>
        <th class="center">ID</th>
        <th>Descripción</th>
        <th class="center">Perfil</th>
        <th class="right">Longitud / Viga</th>
        <th class="right">Total ml</th>
        <th class="right">Peso Total</th>
        <th class="right">Sup. Pintura</th>
        <th class="center">Cosido M12 / Taladros</th>
        <th class="right">PVP (€)</th>
      </tr>
    </thead>
    <tbody>
      {elems_html}
      <tr class="tot-row">
        <td colspan="4" class="bold right">TOTALES ACERO Y PINTURA:</td>
        <td class="right bold">14,00 ml</td>
        <td class="right bold">280,80 kg</td>
        <td class="right bold">9,92 m²</td>
        <td class="center bold">14 varillas (28 taladros)</td>
        <td class="right bold">{eur(t['base_imponible'])}</td>
      </tr>
    </tbody>
  </table>

  <h2>2. Desglose de Costes Directos de Materiales, Suministros y Logística</h2>
  <table class="data">
    <thead>
      <tr>
        <th style="width:55%">Concepto Material / Suministro</th>
        <th class="center" style="width:8%">Ud.</th>
        <th class="right" style="width:12%">Cantidad</th>
        <th class="right" style="width:12%">Coste Unit. (€)</th>
        <th class="right" style="width:13%">Coste Total (€)</th>
      </tr>
    </thead>
    <tbody>
      {mat_rows_html}
      <tr class="tot-row">
        <td colspan="4" class="bold right">SUBTOTAL MATERIALES Y SUMINISTROS:</td>
        <td class="right bold">{eur(esc['totales_escandallo']['coste_materiales'])}</td>
      </tr>
    </tbody>
  </table>

  <h2>3. Mano de Obra Directa en Taller (6,0 Horas a 30,00 €/h)</h2>
  <table class="data">
    <thead>
      <tr>
        <th style="width:55%">Operación de Fabricación en Taller</th>
        <th class="center" style="width:8%">Ud.</th>
        <th class="right" style="width:12%">Horas</th>
        <th class="right" style="width:12%">Tarifa (€/h)</th>
        <th class="right" style="width:13%">Coste Total (€)</th>
      </tr>
    </thead>
    <tbody>
      {mo_rows_html}
      <tr class="tot-row">
        <td colspan="4" class="bold right">SUBTOTAL MANO DE OBRA DIRECTA ({esc['totales_escandallo']['horas_totales']:,.1f} h):</td>
        <td class="right bold">{eur(esc['totales_escandallo']['coste_mano_obra'])}</td>
      </tr>
    </tbody>
  </table>

  <h2>4. Resumen de Rentabilidad y Margen Comercial</h2>
  <div class="rent-box">
    <div class="rent-card">
      <div class="rent-title">Coste Directo Total</div>
      <div class="rent-val">{eur(esc['totales_escandallo']['coste_directo_total'])}</div>
    </div>
    <div class="rent-card">
      <div class="rent-title">Precio Venta (Base)</div>
      <div class="rent-val">{eur(esc['totales_escandallo']['precio_venta'])}</div>
    </div>
    <div class="rent-card highlight">
      <div class="rent-title">Beneficio Bruto</div>
      <div class="rent-val gold">+{eur(esc['totales_escandallo']['margen_bruto_euros'])}</div>
    </div>
    <div class="rent-card green">
      <div class="rent-title">Margen s/ Venta</div>
      <div class="rent-val green">{esc['totales_escandallo']['margen_bruto_porcentaje']:.2f} %</div>
    </div>
  </div>

  <div class="footer-note">
    Estudio Técnico Confidencial · HAM Estructuras Metálicas Menorca · Generado automáticamente
  </div>
</body>
</html>"""

    html_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTML Interno guardado: {html_path}")
    return html_path


# -------------------------------------------------------------------------
# GENERACIÓN DE PDF VIA CHROME HEADLESS
# -------------------------------------------------------------------------
def convert_html_to_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[OK] PDF generado: {pdf_path}")
    else:
        print(f"[ERROR] Error al generar PDF: {res.stderr}")


# -------------------------------------------------------------------------
# GENERACIÓN DE README.MD
# -------------------------------------------------------------------------
def create_readme():
    p = DATA["proyecto"]
    c = DATA["cliente"]
    t = DATA["totales_economicos"]
    esc = DATA["escandallo_interno"]

    md = f"""# Presupuesto {p['codigo']} — {p['titulo']}

## Datos Generales
- **Código de Proyecto:** {p['codigo']}
- **Referencia:** {p['referencia']}
- **Cliente:** {c['nombre_fiscal']} (CIF: {c['nif']} · Cód. FactuSol: {c['codigo_factusol']})
- **Contacto / Referencia:** {c['referencia_contacto']}
- **Email:** {c['email']}
- **Domicilio Fiscal:** {c['domicilio']}, {c['codigo_postal']} {c['poblacion']} ({c['provincia']})
- **Fecha:** {p['fecha']}
- **Validez:** {p['validez_dias']} días naturales
- **Plazo de Entrega:** {p['plazo_entrega']}

---

## Alcance Técnico Solicitado
Fabricación de 3 dinteles estructurales en perfiles laminados en caliente S275JR taladrados en alma cada 50 cm y cosidos mediante varillas pasantes M12 de 200 mm con tuercas y arandelas, e imprimados en taller:
1. **Dintel 1 (L = 2,00 m):** Compuesto por 2 vigas IPE 160 de 2,00 m (4,00 ml / 63,20 kg). Taladros Ø14 mm a paso 50 cm (8 taladros) y 4 varillas M12 x 200 mm cincadas con tuercas y arandelas.
2. **Dintel 2 (L = 3,00 m):** Compuesto por 2 vigas IPE 160 de 3,00 m (6,00 ml / 94,80 kg). Taladros Ø14 mm a paso 50 cm (12 taladros) y 6 varillas M12 x 200 mm cincadas con tuercas y arandelas.
3. **Dintel 3 (L = 2,00 m reforzado):** Compuesto por 2 vigas IPE 240 de 2,00 m (4,00 ml / 122,80 kg). Taladros Ø14 mm a paso 50 cm (8 taladros) y 4 varillas M12 x 200 mm cincadas con tuercas y arandelas.

- **Peso total de acero laminado S275JR:** 280,80 kg
- **Superficie total de tratamiento:** 9,92 m²
- **Pintura en HAM (Norma estricta):** Limpieza mecánica St 3 + imprimación antioxidante alifática/epoxi de taller (NUNCA al horno).

---

## Resumen Económico para el Cliente

| Nº | Código | Concepto | Cant. | Ud. | Precio (€) | Importe (€) |
|:--:|:--:|---|:--:|:--:|---:|---:|
| 01 | DIN-IPE160-2M | Dintel laminado doble IPE 160 (L = 2,00 m) | 1,00 | ud | 360,00 € | 360,00 € |
| 02 | DIN-IPE160-3M | Dintel laminado doble IPE 160 (L = 3,00 m) | 1,00 | ud | 520,00 € | 520,00 € |
| 03 | DIN-IPE240-2M | Dintel laminado doble reforzado IPE 240 (L = 2,00 m) | 1,00 | ud | 540,00 € | 540,00 € |
| | | **SUBTOTAL NETO (Base Imponible):** | | | | **{eur(t['base_imponible'])}** |
| | | **I.V.A. (21%):** | | | | **{eur(t['iva_importe'])}** |
| | | **TOTAL PRESUPUESTO (I.V.A. Inc.):** | | | | **{eur(t['total_presupuesto'])}** |

---

## Escandallo Interno y Rentabilidad
- **Coste Directo Materiales y Suministros:** {eur(esc['totales_escandallo']['coste_materiales'])}
- **Coste Mano de Obra Taller (6,0 h a 30,00 €/h):** {eur(esc['totales_escandallo']['coste_mano_obra'])}
- **Coste Directo Total:** **{eur(esc['totales_escandallo']['coste_directo_total'])}**
- **Precio Venta Base:** **{eur(esc['totales_escandallo']['precio_venta'])}**
- **Beneficio Bruto:** **+{eur(esc['totales_escandallo']['margen_bruto_euros'])}**
- **Margen s/ Venta:** **{esc['totales_escandallo']['margen_bruto_porcentaje']:.2f}%**

---

## Archivos Generados en el Expediente
- [Presupuesto_P2026_0065_Dinteles_Laminados_IPE_Reformarc_Carlota.xlsx](file:///{os.path.join(BASE_DIR, 'Presupuesto_P2026_0065_Dinteles_Laminados_IPE_Reformarc_Carlota.xlsx').replace('\\', '/')})
- [presupuesto-cliente.html](file:///{os.path.join(BASE_DIR, 'presupuesto-cliente.html').replace('\\', '/')})
- [presupuesto-cliente.pdf](file:///{os.path.join(BASE_DIR, 'presupuesto-cliente.pdf').replace('\\', '/')})
- [presupuesto-interno-tecnico.html](file:///{os.path.join(BASE_DIR, 'presupuesto-interno-tecnico.html').replace('\\', '/')})
- [presupuesto-interno-tecnico.pdf](file:///{os.path.join(BASE_DIR, 'presupuesto-interno-tecnico.pdf').replace('\\', '/')})
- [datos.json](file:///{os.path.join(BASE_DIR, 'datos.json').replace('\\', '/')})
- [respuesta-email-cliente.md](file:///{os.path.join(BASE_DIR, 'respuesta-email-cliente.md').replace('\\', '/')})
"""

    md_path = os.path.join(BASE_DIR, "README.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[OK] README.md guardado: {md_path}")
    return md_path


# -------------------------------------------------------------------------
# GENERACIÓN DE RESPUESTA POR EMAIL LISTA PARA ENVIAR
# -------------------------------------------------------------------------
def create_email_draft():
    p = DATA["proyecto"]
    c = DATA["cliente"]
    t = DATA["totales_economicos"]
    e = DATA["emisor"]

    email_md = f"""# Propuesta de Email para el Cliente

**Para:** {c['email']}  
**Asunto:** Presupuesto {p['codigo']} — 3 Dinteles Laminados IPE Taladrados con Varilla M12 e Imprimados ({c['referencia_contacto']})  
**Adjuntos:** `presupuesto-cliente.pdf`

---

Estimada Carlota / Estimados señores de REFORMARC & REFORNILLES SL,

En atención a su solicitud de cotización (Ref: **{c['referencia_contacto']}**), les adjuntamos nuestro presupuesto formal **{p['codigo']}** correspondiente a la fabricación a medida en nuestro taller de Sant Lluís (Menorca) de los **3 dinteles metálicos laminados compuestos**.

### Resumen de la Solución Técnica Ofertada:
- **Dintel 1 (L = 2,00 m):** Compuesto por 2 perfiles laminados en caliente IPE 160 de 2,00 m (4,00 ml / 63,20 kg), perforaciones en alma de Ø14 mm cada 50 cm (8 taladros) y cosido conjunto con 4 varillas roscadas M12 x 200 mm cincadas calidad 8.8, tuercas y arandelas anchas.
- **Dintel 2 (L = 3,00 m):** Compuesto por 2 perfiles laminados en caliente IPE 160 de 3,00 m (6,00 ml / 94,80 kg), perforaciones en alma de Ø14 mm cada 50 cm (12 taladros) y cosido con 6 varillas roscadas M12 x 200 mm cincadas, tuercas y arandelas.
- **Dintel 3 (L = 2,00 m reforzado):** Compuesto por 2 perfiles laminados en caliente IPE 240 de 2,00 m (4,00 ml / 122,80 kg), perforaciones en alma de Ø14 mm cada 50 cm (8 taladros) y cosido con 4 varillas roscadas M12 x 200 mm cincadas, tuercas y arandelas.
- **Tratamiento superficial:** Desengrasado, limpieza mecánica y aplicación en taller de imprimación antioxidante de secado rápido (sin horno, según estándar de fabricación HAM).

### Resumen Económico:
- **Base Imponible:** **{eur(t['base_imponible'])}**
- **I.V.A. (21%):** {eur(t['iva_importe'])}
- **Total Presupuesto:** **{eur(t['total_presupuesto'])}**

### Condiciones del Pedido:
- **Plazo de fabricación:** 4 a 6 días laborables desde la confirmación.
- **Disponibilidad:** Entrega sobre camión en nuestro taller de Sant Lluís (Polígono Industrial) o porte a pie de obra en Menorca a coordinar.
- **Validez de la oferta:** 30 días naturales.
- **Forma de pago:** 100% a la confirmación del pedido.

Quedamos a su entera disposición para cualquier aclaración técnica o para poner en marcha la fabricación tan pronto nos den su conformidad.

Atentamente,

**{e['contacto']}**  
HAM Estructuras Metálicas Menorca  
Dixis Recursos y Soluciones S.L.  
Tel: {e['telefono']} · Móvil/WhatsApp: {e['movil']}  
{e['email']} · {e['web']}  
Av. Circunval·lació, 11 · Pol. Ind. Sant Lluís (Menorca)
"""

    email_path = os.path.join(BASE_DIR, "respuesta-email-cliente.md")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(email_md)
    print(f"[OK] Email draft guardado: {email_path}")
    return email_path


if __name__ == "__main__":
    excel_file = create_excel()
    html_cli = create_cliente_html()
    pdf_cli = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    convert_html_to_pdf(html_cli, pdf_cli)

    html_int = create_interno_html()
    pdf_int = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")
    convert_html_to_pdf(html_int, pdf_int)

    create_readme()
    create_email_draft()
    print("--- Proceso de generación finalizado con éxito ---")
