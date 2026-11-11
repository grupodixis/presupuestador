import os
import json
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def create_excel():
    wb = Workbook()

    NAVY = "0F172A"
    GOLD = "B45309"
    SLATE_LIGHT = "F8FAFC"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"
    HIGHLIGHT_FILL = "EFF6FF"
    RED_DARK = "B91C1C"
    GREEN_DARK = "15803D"

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    fill_hl = PatternFill(start_color=HIGHLIGHT_FILL, end_color=HIGHLIGHT_FILL, fill_type="solid")

    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_tot = Font(name="Segoe UI", size=10.5, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=10.5, bold=True, color=GOLD)
    font_red = Font(name="Segoe UI", size=9, bold=True, color=RED_DARK)
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

    # ------------------------------------------------------------------
    # HOJA 1: PRESUPUESTO CLIENTE (LIMPIO)
    # ------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Cliente"
    ws1.views.sheetView[0].showGridLines = True

    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS · INSTALADOR HOMOLOGADO LUX-TOP®"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} • LÍNEA DE VIDA LUX-TOP® FSE 2003 (50 ML) · EDAR ACCIONA"
    ws1["B3"].font = font_title

    meta_rows = [
        ("REFERENCIA:", DATA["referencia"]),
        ("CLIENTE:", f"{DATA['cliente']['nombre']} ({DATA['cliente']['obra']})"),
        ("UBICACIÓN:", DATA["cliente"]["ubicacion"]),
        ("FECHA / VALIDEZ:", f"{DATA['fecha']} • Validez: {DATA['validez_dias']} días naturales"),
        ("SISTEMA OFICIAL:", "LUX-top® FSE 2003 Paso Manual (UNE-EN 795:2012 Tipo C / CEN/TS 16415:2013)"),
    ]
    for idx, (k, v) in enumerate(meta_rows, start=5):
        ws1[f"B{idx}"] = k
        ws1[f"B{idx}"].font = font_bold
        ws1[f"C{idx}"] = v
        ws1[f"C{idx}"].font = font_reg

    ws1["B11"] = "DESGLOSE DE SUMINISTRO, INSTALACIÓN HOMOLOGADA Y CERTIFICACIÓN (LLAVE EN MANO)"
    ws1["B11"].font = font_sec

    headers_client = ["Nº", "Partida y Descripción Técnica Homologada LUX-TOP®", "Ud.", "Cantidad", "Precio Unitario", "Subtotal"]
    for c_idx, h in enumerate(headers_client, start=2):
        cell = ws1.cell(row=12, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[12].height = 24

    row_cur = 13
    for p in DATA["partidas"]:
        c_id = ws1.cell(row=row_cur, column=2, value=p["id"])
        c_id.font = font_bold
        c_id.alignment = Alignment(horizontal="center", vertical="top")

        c_desc = ws1.cell(row=row_cur, column=3, value=f"{p['concepto']}\n{p['descripcion']}")
        c_desc.font = font_reg
        c_desc.alignment = Alignment(wrap_text=True, vertical="top")

        c_ud = ws1.cell(row=row_cur, column=4, value=p["unidad"])
        c_ud.font = font_reg
        c_ud.alignment = Alignment(horizontal="center", vertical="top")

        c_cant = ws1.cell(row=row_cur, column=5, value=p["cantidad"])
        c_cant.font = font_reg
        c_cant.alignment = Alignment(horizontal="right", vertical="top")
        c_cant.number_format = "#,##0.00"

        c_pu = ws1.cell(row=row_cur, column=6, value=p["precio_cliente"])
        c_pu.font = font_reg
        c_pu.alignment = Alignment(horizontal="right", vertical="top")
        c_pu.number_format = "#,##0.00 €"

        c_sub = ws1.cell(row=row_cur, column=7, value=f"=E{row_cur}*F{row_cur}")
        c_sub.font = font_bold
        c_sub.alignment = Alignment(horizontal="right", vertical="top")
        c_sub.number_format = "#,##0.00 €"

        for c_idx in range(2, 8):
            ws1.cell(row=row_cur, column=c_idx).border = border_thin
            if row_cur % 2 == 0:
                ws1.cell(row=row_cur, column=c_idx).fill = fill_alt
        ws1.row_dimensions[row_cur].height = 44
        row_cur += 1

    last_item_row = row_cur - 1

    ws1.cell(row=row_cur, column=6, value="BASE IMPONIBLE (50 ML LLAVE EN MANO):").font = font_bold
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    c_base = ws1.cell(row=row_cur, column=7, value=f"=SUM(G13:G{last_item_row})")
    c_base.font = font_tot
    c_base.number_format = "#,##0.00 €"
    c_base.border = border_thin
    base_row = row_cur

    row_cur += 1
    ws1.cell(row=row_cur, column=6, value="I.V.A. (21%):").font = font_reg
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    c_iva = ws1.cell(row=row_cur, column=7, value=f"=G{base_row}*0.21")
    c_iva.font = font_bold
    c_iva.number_format = "#,##0.00 €"
    c_iva.border = border_thin

    row_cur += 1
    ws1.cell(row=row_cur, column=6, value="TOTAL PRESUPUESTO CON IVA:").font = font_tot_gold
    ws1.cell(row=row_cur, column=6).alignment = Alignment(horizontal="right")
    c_tot = ws1.cell(row=row_cur, column=7, value=f"=G{base_row}*1.21")
    c_tot.font = font_tot_gold
    c_tot.number_format = "#,##0.00 €"
    c_tot.fill = fill_tot
    c_tot.border = border_total

    row_cur += 2
    ws1.cell(row=row_cur, column=2, value="CONDICIONES COMERCIALES Y PLAZO DE EJECUCIÓN").font = font_sec
    notes = [
        f"• Plazo de ejecución: {DATA['condiciones_comerciales']['plazo_ejecucion']}",
        "• Verificación previa in situ: Incluida visita técnica de comprobación de medidas reales del muro (H+V 20+20 cm y posición placa H) antes de emitir orden de fabricación SOKO.",
        f"• Forma de pago: {DATA['condiciones_comerciales']['forma_pago']}",
        f"• Garantía y mantenimiento: {DATA['condiciones_comerciales']['garantia']} {DATA['condiciones_comerciales']['revisiones']}",
        "• Exclusiones: Obra civil/reparación si el hormigón existente no cumple resistencia, vaciado/parada de depósito, permisos internos planta, EPIs personales de uso posterior.",
    ]
    for n in notes:
        row_cur += 1
        ws1.cell(row=row_cur, column=3, value=n).font = font_reg

    widths_1 = {1: 3, 2: 8, 3: 68, 4: 8, 5: 11, 6: 16, 7: 16}
    for col_i, w in widths_1.items():
        ws1.column_dimensions[chr(64 + col_i)].width = w

    # ------------------------------------------------------------------
    # HOJA 2: ESCANDALLO INTERNO DIXIS
    # ------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Escandallo Interno DIXIS")
    ws2.views.sheetView[0].showGridLines = True

    ws2["B2"] = "DOCUMENTO INTERNO CONFIDENCIAL · NO ENTREGAR AL CLIENTE"
    ws2["B2"].font = font_red
    ws2["B3"] = f"ESCANDALLO TÉCNICO Y RENTABILIDAD • {DATA['codigo']} (Ref. Proveedor LUX-TOP 3074/26)"
    ws2["B3"].font = font_title

    headers_int = [
        "Nº", "Concepto / Recurso", "Ud.", "Cant.",
        "Tarifa Oficial", "Dto.", "Coste Neto DIXIS",
        "PVP Unit.", "Venta Cliente", "Margen (€)", "Margen (%)"
    ]
    for c_idx, h in enumerate(headers_int, start=2):
        cell = ws2.cell(row=5, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_thin
    ws2.row_dimensions[5].height = 24

    r2 = 6
    for p in DATA["partidas"]:
        ws2.cell(row=r2, column=2, value=p["id"]).font = font_bold
        ws2.cell(row=r2, column=2).alignment = Alignment(horizontal="center")

        ws2.cell(row=r2, column=3, value=p["concepto"]).font = font_reg
        ws2.cell(row=r2, column=3).alignment = Alignment(wrap_text=True)

        ws2.cell(row=r2, column=4, value=p["unidad"]).font = font_reg
        ws2.cell(row=r2, column=4).alignment = Alignment(horizontal="center")

        c_q = ws2.cell(row=r2, column=5, value=p["cantidad"])
        c_q.font = font_reg
        c_q.number_format = "#,##0.00"

        c_to = ws2.cell(row=r2, column=6, value=p["tarifa_oficial"])
        c_to.font = font_reg
        c_to.number_format = "#,##0.00 €"

        c_dt = ws2.cell(row=r2, column=7, value=p["descuento"])
        c_dt.font = font_reg
        c_dt.number_format = "0%"
        c_dt.alignment = Alignment(horizontal="center")

        c_cd = ws2.cell(row=r2, column=8, value=p["coste_dixis"])
        c_cd.font = font_red
        c_cd.number_format = "#,##0.00 €"

        c_pu = ws2.cell(row=r2, column=9, value=p["precio_cliente"])
        c_pu.font = font_reg
        c_pu.number_format = "#,##0.00 €"

        c_ve = ws2.cell(row=r2, column=10, value=f"=E{r2}*I{r2}")
        c_ve.font = font_bold
        c_ve.number_format = "#,##0.00 €"

        c_mg = ws2.cell(row=r2, column=11, value=f"=J{r2}-H{r2}")
        c_mg.font = font_green
        c_mg.number_format = "#,##0.00 €"

        c_mp = ws2.cell(row=r2, column=12, value=f"=IF(J{r2}>0,K{r2}/J{r2},0)")
        c_mp.font = font_bold
        c_mp.number_format = "0.0%"

        for c_idx in range(2, 13):
            ws2.cell(row=r2, column=c_idx).border = border_thin
            if r2 % 2 == 0:
                ws2.cell(row=r2, column=c_idx).fill = fill_alt
        ws2.row_dimensions[r2].height = 28
        r2 += 1

    last_r2 = r2 - 1
    ws2.cell(row=r2, column=3, value="TOTALES ESCANDALLO OPERATIVO:").font = font_tot
    ws2.cell(row=r2, column=8, value=f"=SUM(H6:H{last_r2})").font = font_red
    ws2.cell(row=r2, column=8).number_format = "#,##0.00 €"
    ws2.cell(row=r2, column=10, value=f"=SUM(J6:J{last_r2})").font = font_tot
    ws2.cell(row=r2, column=10).number_format = "#,##0.00 €"
    ws2.cell(row=r2, column=11, value=f"=SUM(K6:K{last_r2})").font = font_green
    ws2.cell(row=r2, column=11).number_format = "#,##0.00 €"
    ws2.cell(row=r2, column=12, value=f"=K{r2}/J{r2}").font = font_tot
    ws2.cell(row=r2, column=12).number_format = "0.0%"
    for c_idx in range(2, 13):
        ws2.cell(row=r2, column=c_idx).fill = fill_tot
        ws2.cell(row=r2, column=c_idx).border = border_total

    r2 += 2
    ws2.cell(row=r2, column=3, value="ANÁLISIS DE SENSIBILIDAD Y CONDICIONES PROVEEDOR LUX-TOP (3074/26)").font = font_sec
    sens_lines = [
        f"• Compra material LUX-TOP (3074/26): 3.250,07 € base imponible (3.932,58 € c/IVA) · Pago: Giro 60 días CESCE.",
        "• Coste MO operativa estimada (32 h x 25 €/h + 60 € brocas/consumibles = 860,00 €) -> Coste directo total: 4.600,07 € | Margen: 2.899,93 € (38,67% s/venta).",
        "• Sensibilidad con tarifa máxima `costes-mo.json` (45 €/h x 32 h + 60 € = 1.500,00 €) -> Coste imputado: 5.240,07 € | Margen neto: 2.259,93 € (30,13% s/venta).",
        "• Ratio unitario resultante: 150,00 €/ml (50 ml comerciales) / 151,73 €/ml (49,43 ml exactos de plano LV1).",
        "• ALERTA CRÍTICA DE PEDIDO: Confirmar medidas H+V (20+20 cm) y posición placa H in situ antes de encargar SOKO (20-25 días fabricación).",
    ]
    for sl in sens_lines:
        r2 += 1
        ws2.cell(row=r2, column=3, value=sl).font = font_reg

    widths_2 = {1: 3, 2: 7, 3: 48, 4: 6, 5: 9, 6: 13, 7: 7, 8: 15, 9: 12, 10: 14, 11: 14, 12: 11}
    for col_i, w in widths_2.items():
        ws2.column_dimensions[chr(64 + col_i)].width = w

    # ------------------------------------------------------------------
    # HOJA 3: ESPECIFICACIÓN TÉCNICA
    # ------------------------------------------------------------------
    ws3 = wb.create_sheet(title="Especificación Técnica")
    ws3["B2"] = "FICHA TÉCNICA DE SISTEMA ANTICAÍDAS LUX-TOP® FSE 2003 · EDAR ACCIONA"
    ws3["B2"].font = font_title

    specs = [
        ("Normativa aplicable", DATA["proyecto"]["normativa_referencia"]),
        ("Sistema instalado", DATA["proveedor_homologado"]["sistema"]),
        ("Longitud en plano", f"49,43 ml (Depósito circular Ø ~15 m, muro ~0,20 m, paso entre soportes ~2,47 m)"),
        ("Cable flexible", "53 ml LUX-top® FSE 2003 Acero Inoxidable AISI 316 Ø8 mm (código 000011710)"),
        ("Soportes especiales", "20 uds LUX-top® ASP - SOKO EV2s / 40 (Ø26 mm, 90º, placa 80x150x6 mm 2-Loch, H+V 20+20 cm)"),
        ("Fijación hormigón", "20 sets (40 pernos) MKT BZ3 M-12x115/20 Acero Inoxidable A4 (código 000040131)"),
        ("Kit de cierre directo", "030 - Cierre 3: SKE II + Tensor PV + Terminal horquilla SV + Placa SB fijación directa"),
        ("Control y ensayo final", "Prueba de tiro estático in situ con dinamómetro calibrado + Certificado Oficial LUX-TOP®"),
        ("Plazo fabricación SOKO", "20-25 días laborables desde confirmación de medidas H+V in situ + 2 jornadas de montaje"),
    ]
    for idx, (k, v) in enumerate(specs, start=4):
        c1 = ws3.cell(row=idx, column=2, value=k)
        c1.font = font_bold
        c1.fill = fill_sub
        c1.border = border_thin
        c2 = ws3.cell(row=idx, column=3, value=v)
        c2.font = font_reg
        c2.border = border_thin
    ws3.column_dimensions["A"].width = 3
    ws3.column_dimensions["B"].width = 26
    ws3.column_dimensions["C"].width = 90

    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0057_Linea_de_Vida_EDAR_Acciona.xlsx")
    wb.save(excel_path)
    print(f"Excel generado: {excel_path}")
    return excel_path


def create_html_client():
    rows_html = ""
    for p in DATA["partidas"]:
        rows_html += f"""
          <tr>
            <td class="c bold">{p['id']}</td>
            <td><strong>{p['concepto']}</strong><br><span class="subdesc">{p['descripcion']}</span></td>
            <td class="c">{p['unidad']}</td>
            <td class="r">{p['cantidad']:.2f}</td>
            <td class="r">{p['precio_cliente']:.2f} €</td>
            <td class="r bold">{p['subtotal']:.2f} €</td>
          </tr>"""

    tot = DATA["totales"]
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presupuesto Oficial LUX-top® {DATA['codigo']} • EDAR ACCIONA</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 0;
    }}
    :root {{
      --ink: #0f172a;
      --muted: #475569;
      --line: #cbd5e1;
      --soft: #f8fafc;
      --brand: #0f172a;
      --accent: #b45309;
      --card-bg: #f1f5f9;
      --highlight: #0284c7;
      --blue-bg: #eff6ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 9px;
      line-height: 1.25;
    }}
    .page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 6mm 10.5mm 5mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      page-break-inside: avoid;
      page-break-after: avoid;
    }}
    header {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: center;
      border-top: 4px solid var(--brand);
      padding-top: 5px;
      padding-bottom: 5px;
      border-bottom: 1px solid var(--line);
    }}
    .company {{ display: flex; gap: 10px; align-items: center; }}
    .logo {{ width: 92px; flex: 0 0 92px; }}
    .logo img {{ width: 100%; height: auto; display: block; }}
    .company-info h1 {{
      margin: 0;
      color: var(--brand);
      font-size: 13px;
      font-weight: 800;
      letter-spacing: -0.2px;
    }}
    .company-info p {{ margin: 1px 0; color: var(--muted); font-size: 8.5px; }}
    .badge-luxtop {{
      display: inline-block;
      background: #0284c7;
      color: #fff;
      font-size: 7.5px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
      text-transform: uppercase;
      margin-left: 4px;
      vertical-align: middle;
    }}
    .meta {{ text-align: right; }}
    .meta h2 {{ margin: 0; color: var(--accent); font-size: 13.5px; font-weight: 800; }}
    .meta .ref-badge {{
      display: inline-block;
      background: var(--brand);
      color: #fff;
      font-size: 8px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      margin: 2px 0;
    }}
    .meta p {{ margin: 1px 0; color: var(--muted); font-size: 8px; }}
    .hero {{
      margin-top: 5px;
      background: var(--soft);
      border-left: 3px solid var(--accent);
      padding: 4px 8px;
      border-radius: 0 4px 4px 0;
    }}
    .hero h3 {{ margin: 0 0 2px; color: var(--brand); font-size: 10.5px; font-weight: 700; }}
    .hero p {{ margin: 0; color: var(--muted); font-size: 8.3px; }}
    .grid-meta {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      margin-top: 5px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 4px 6px;
    }}
    .card .label {{
      display: block;
      font-size: 7px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      color: var(--muted);
      font-weight: 700;
      margin-bottom: 1px;
    }}
    .card .value {{ font-size: 8.5px; font-weight: 700; color: var(--brand); }}
    h4 {{
      margin: 6px 0 3px;
      color: var(--brand);
      font-size: 9px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
      text-transform: uppercase;
    }}
    table {{ width: 100%; border-collapse: collapse; font-size: 8.2px; margin-bottom: 5px; }}
    th {{
      background: var(--brand);
      color: #fff;
      padding: 3px 5px;
      font-size: 7.5px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      font-weight: 700;
      border: 1px solid var(--brand);
    }}
    td {{ padding: 3px 5px; border: 1px solid var(--line); vertical-align: top; }}
    tr:nth-child(even) td {{ background: var(--soft); }}
    .subdesc {{ color: var(--muted); font-size: 7.2px; display: block; margin-top: 1px; line-height: 1.2; }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; white-space: nowrap; }}
    .bold {{ font-weight: 700; }}
    .price-box {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 8px;
      background: var(--blue-bg);
      border: 1.5px solid var(--highlight);
      border-radius: 4px;
      padding: 5px 9px;
      margin-bottom: 5px;
      align-items: center;
    }}
    .price-base .label {{ font-size: 7.5px; text-transform: uppercase; color: var(--muted); font-weight: 700; }}
    .price-base .price-amount {{ font-size: 14px; font-weight: 800; color: var(--brand); }}
    .price-final {{
      text-align: right;
      background: var(--brand);
      color: #fff;
      padding: 5px 9px;
      border-radius: 4px;
    }}
    .price-final .label {{ font-size: 7.5px; text-transform: uppercase; font-weight: 700; color: #cbd5e1; }}
    .price-final .price-amount {{ font-size: 15.5px; font-weight: 800; color: #fef08a; }}
    .notice-soko {{
      background: #fffbeb;
      border: 1px solid #f59e0b;
      border-radius: 4px;
      padding: 4px 7px;
      margin-bottom: 5px;
      font-size: 7.8px;
      color: #78350f;
    }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; margin-bottom: 4px; }}
    .col {{ background: #fff; border: 1px solid var(--line); border-radius: 4px; padding: 4px 6px; }}
    .col h5 {{
      margin: 0 0 2px;
      font-size: 8px;
      color: var(--brand);
      font-weight: 700;
      text-transform: uppercase;
      border-bottom: 1px solid var(--line);
      padding-bottom: 1px;
    }}
    ul.compact {{ margin: 0; padding-left: 12px; font-size: 7.5px; color: var(--muted); line-height: 1.22; }}
    ul.compact li {{ margin-bottom: 1.5px; }}
    .sign-section {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 2px;
      padding-top: 3px;
      border-top: 1px solid var(--line);
    }}
    .sign-box {{
      height: 32px;
      border: 1px dashed var(--line);
      border-radius: 4px;
      padding: 3px 5px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      font-size: 7.2px;
      color: var(--muted);
    }}
    footer {{
      border-top: 1px solid var(--line);
      padding-top: 3px;
      display: flex;
      justify-content: space-between;
      font-size: 7.2px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="page">
    <div>
      <header>
        <div class="company">
          <div class="logo"><img src="logo-ham.svg" alt="HAM Estructuras Metálicas"></div>
          <div class="company-info">
            <h1>HAM ESTRUCTURAS METÁLICAS <span class="badge-luxtop">INSTALADOR HOMOLOGADO LUX-TOP®</span></h1>
            <p><strong>Dixis Recursos y Soluciones S.L.</strong> • CIF: B57825432</p>
            <p>Av. Circunval·lació, 11 • Polígono Industrial de Sant Lluís, 07710 Menorca</p>
            <p>+34 971 35 20 18 • +34 669 769 541 • pablo@dixis.es • www.hamenorca.com</p>
          </div>
        </div>
        <div class="meta">
          <h2>PRESUPUESTO {DATA['codigo']}</h2>
          <div class="ref-badge">{DATA['referencia']}</div>
          <p><strong>Cliente:</strong> {DATA['cliente']['nombre']}</p>
          <p><strong>Fecha:</strong> {DATA['fecha']} • <strong>Validez:</strong> {DATA['validez_dias']} días</p>
        </div>
      </header>

      <section class="hero">
        <h3>Suministro, Instalación Homologada y Certificación de Línea de Vida LUX-top® FSE 2003 (50 ml) · EDAR ACCIONA</h3>
        <p>Instalación completa llave en mano de sistema anticaídas permanente homologado <strong>LUX-top® FSE 2003 Paso Manual</strong> sobre coronación de muro circular de hormigón (desarrollo 49,43 ml según plano LV1). Ejecutado por equipo instalador homologado LUX-TOP® con cable inoxidable AISI 316, 20 soportes especiales ASP-SOKO, pernos inox A4, ensayo con dinamómetro in situ y Certificación Oficial.</p>
      </section>

      <section class="grid-meta">
        <div class="card">
          <span class="label">Cliente / Obra</span>
          <span class="value">ACCIONA AGUA · EDAR</span>
        </div>
        <div class="card">
          <span class="label">Sistema Certificado</span>
          <span class="value">LUX-top® FSE 2003 (EN 795-C)</span>
        </div>
        <div class="card">
          <span class="label">Anclaje Hormigón</span>
          <span class="value">20 uds ASP-SOKO 90º + M12 A4</span>
        </div>
        <div class="card">
          <span class="label">Ratio Llave en Mano</span>
          <span class="value">150,00 €/ml (50 ml)</span>
        </div>
      </section>

      <h4>Desglose Oficial de Partidas • Suministro, Montaje Homologado y Certificación</h4>
      <table>
        <thead>
          <tr>
            <th class="c" style="width: 24px;">Nº</th>
            <th>Concepto y Especificación Homologada LUX-TOP®</th>
            <th class="c" style="width: 28px;">Ud</th>
            <th class="r" style="width: 34px;">Cant.</th>
            <th class="r" style="width: 56px;">Precio Ud</th>
            <th class="r" style="width: 64px;">Importe</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>

      <section class="price-box">
        <div class="price-base">
          <span class="label">Base Imponible (Suministro + Instalación Homologada + Certificación)</span>
          <div class="price-amount">{tot['base_imponible']:,.2f} €</div>
          <span style="font-size: 7.6px; color: var(--muted);">I.V.A. 21%: {tot['iva_21']:,.2f} € • Partida 1.05 deducible (-380,00 €) si aporta medios propios</span>
        </div>
        <div class="price-final">
          <span class="label">Importe Total Llave en Mano</span>
          <div class="price-amount">{tot['total_con_iva']:,.2f} €</div>
          <span style="font-size: 7.5px; color: #cbd5e1;">Impuestos incluidos (I.V.A. 21%)</span>
        </div>
      </section>

      <div class="notice-soko">
        <strong>Plazo fabricación especial SOKO y replanteo previo:</strong> Los 20 soportes <em>LUX-top® ASP-SOKO EV2s/40</em> son de fabricación especial bajo pedido (plazo mínimo fabricante: <strong>20-25 días laborables</strong> desde confirmación de medidas reales H+V 20+20 cm y posición de placa H en obra). Montaje y certificación en <strong>2 jornadas</strong>.
      </div>

      <div class="two-col">
        <div class="col">
          <h5>Alcance Incluido por Instalador Homologado</h5>
          <ul class="compact">
            <li><strong>Visita previa de replanteo:</strong> Comprobación in situ de medidas H+V y geometría del muro antes de orden de fabricación SOKO.</li>
            <li><strong>Calidad EDAR / Marina:</strong> Cable Ø8 mm AISI 316 y 40 pernos MKT BZ3 M-12x115/20 en acero inoxidable A4 con par certificado.</li>
            <li><strong>Pruebas y Legalización:</strong> Ensayo de tiro estático con dinamómetro calibrado in situ, placa SB indeleble y Certificado Oficial LUX-TOP®.</li>
            <li><strong>Documentación PRL/CAE:</strong> Manual de Uso y Mantenimiento, Libro de Revisiones Anuales y acreditación instalador homologado.</li>
          </ul>
        </div>
        <div class="col">
          <h5>Exclusiones y Condiciones Comerciales</h5>
          <ul class="compact">
            <li><strong>Exclusiones:</strong> Reparación/saneo estructural si el hormigón existente presentara disgregación incompatible con perno M12; vaciado o parada de servicio del depósito; EPIs individuales de uso posterior; tasas externas.</li>
            <li><strong>Mantenimiento legal:</strong> Inspección técnica periódica anual obligatoria según UNE-EN 795 y UNE-EN 365.</li>
            <li><strong>Garantía:</strong> Garantía oficial LUX-TOP® en materiales y 2 años de garantía de montaje HAM / DIXIS.</li>
            <li><strong>Forma de pago:</strong> {DATA['condiciones_comerciales']['forma_pago']}.</li>
          </ul>
        </div>
      </div>

      <section class="sign-section">
        <div class="sign-box">
          <span><strong>Por HAM Estructuras Metálicas (DIXIS) • Instalador Homologado LUX-TOP®</strong></span>
          <span>Pablo Sebastián Sánchez Arnoletto</span>
        </div>
        <div class="sign-box">
          <span><strong>Aceptación del Cliente (ACCIONA AGUA, S.A.)</strong></span>
          <span>Fecha, sello y firma de conformidad:</span>
        </div>
      </section>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • C.I.F. B57825432 • Sant Lluís, Menorca (Illes Balears)</div>
      <div>{DATA['codigo']} • LUX-top® FSE 2003 (50 ml) EDAR ACCIONA • Hoja 1 de 1</div>
    </footer>
  </div>
</body>
</html>"""

    path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML Cliente generado: {path}")
    return path


def create_html_technical():
    rows_html = ""
    for p in DATA["partidas"]:
        margen = p["subtotal"] - p["coste_dixis"]
        mp = (margen / p["subtotal"] * 100.0) if p["subtotal"] > 0 else 0.0
        dto_txt = f"{int(p['descuento']*100)}%" if p["descuento"] > 0 else "-"
        rows_html += f"""
          <tr>
            <td class="c bold">{p['id']}</td>
            <td><strong>{p['concepto']}</strong><br><span style="color:var(--muted); font-size:7.2px;">Ref: {p['codigo_luxtop']}</span></td>
            <td class="c">{p['unidad']}</td>
            <td class="r">{p['cantidad']:.2f}</td>
            <td class="r">{p['tarifa_oficial']:.2f} €</td>
            <td class="c">{dto_txt}</td>
            <td class="r bold" style="color:var(--tech-red);">{p['coste_dixis']:.2f} €</td>
            <td class="r bold">{p['subtotal']:.2f} €</td>
            <td class="r bold" style="color:var(--tech-green);">{margen:.2f} € ({mp:.1f}%)</td>
          </tr>"""

    tot = DATA["totales"]
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Estudio Técnico Interno {DATA['codigo']} • EDAR ACCIONA</title>
  <style>
    @page {{ size: A4 portrait; margin: 0; }}
    :root {{
      --ink: #0f172a;
      --muted: #475569;
      --line: #cbd5e1;
      --soft: #f8fafc;
      --brand: #0f172a;
      --tech-red: #b91c1c;
      --tech-green: #15803d;
      --accent: #b45309;
      --card-bg: #f1f5f9;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: #e2e8f0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 9px;
      line-height: 1.25;
    }}
    .page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 6mm 10.5mm 5mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      page-break-inside: avoid;
      page-break-after: avoid;
    }}
    header {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: center;
      border-top: 4px solid var(--tech-red);
      padding-top: 5px;
      padding-bottom: 5px;
      border-bottom: 1px solid var(--line);
    }}
    .company {{ display: flex; gap: 10px; align-items: center; }}
    .logo {{ width: 92px; flex: 0 0 92px; }}
    .logo img {{ width: 100%; height: auto; display: block; }}
    .company-info h1 {{ margin: 0; color: var(--brand); font-size: 13px; font-weight: 800; }}
    .company-info p {{ margin: 1px 0; color: var(--tech-red); font-weight: 700; font-size: 8.5px; }}
    .meta {{ text-align: right; }}
    .meta h2 {{ margin: 0; color: var(--tech-red); font-size: 13px; font-weight: 800; }}
    .meta .ref-badge {{
      display: inline-block;
      background: var(--brand);
      color: #fff;
      font-size: 8px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      margin: 2px 0;
    }}
    .meta p {{ margin: 1px 0; color: var(--muted); font-size: 8px; }}
    .hero {{
      margin-top: 5px;
      background: #fef2f2;
      border-left: 3px solid var(--tech-red);
      padding: 4px 8px;
      border-radius: 0 4px 4px 0;
    }}
    .hero h3 {{ margin: 0 0 2px; color: var(--brand); font-size: 10.5px; font-weight: 700; }}
    .hero p {{ margin: 0; color: var(--muted); font-size: 8.2px; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-top: 5px; }}
    .kpi {{
      background: var(--card-bg);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 4px 6px;
    }}
    .kpi .label {{ font-size: 7px; text-transform: uppercase; color: var(--muted); font-weight: 700; display: block; }}
    .kpi .val {{ font-size: 11px; font-weight: 800; color: var(--brand); }}
    .kpi.green .val {{ color: var(--tech-green); }}
    .kpi.red .val {{ color: var(--tech-red); }}
    h4 {{
      margin: 6px 0 3px;
      color: var(--brand);
      font-size: 9px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
      text-transform: uppercase;
    }}
    table {{ width: 100%; border-collapse: collapse; font-size: 7.9px; margin-bottom: 5px; }}
    th {{
      background: var(--brand);
      color: #fff;
      padding: 3px 4px;
      font-size: 7.2px;
      text-transform: uppercase;
      border: 1px solid var(--brand);
    }}
    td {{ padding: 3px 4px; border: 1px solid var(--line); vertical-align: top; }}
    tr:nth-child(even) td {{ background: var(--soft); }}
    .c {{ text-align: center; }}
    .r {{ text-align: right; white-space: nowrap; }}
    .bold {{ font-weight: 700; }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; margin-bottom: 5px; }}
    .col {{ background: #fff; border: 1px solid var(--line); border-radius: 4px; padding: 5px 7px; }}
    .col h5 {{
      margin: 0 0 3px;
      font-size: 8.2px;
      color: var(--brand);
      font-weight: 700;
      text-transform: uppercase;
      border-bottom: 1px solid var(--line);
      padding-bottom: 2px;
    }}
    ul.compact {{ margin: 0; padding-left: 12px; font-size: 7.7px; color: var(--muted); line-height: 1.25; }}
    ul.compact li {{ margin-bottom: 2px; }}
    .alert-box {{
      background: #fffbeb;
      border: 1px solid #f59e0b;
      border-radius: 4px;
      padding: 5px 7px;
      font-size: 7.8px;
      color: #78350f;
    }}
    footer {{
      border-top: 1px solid var(--line);
      padding-top: 3px;
      display: flex;
      justify-content: space-between;
      font-size: 7.2px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="page">
    <div>
      <header>
        <div class="company">
          <div class="logo"><img src="logo-ham.svg" alt="HAM"></div>
          <div class="company-info">
            <h1>ESTUDIO TÉCNICO INTERNO • DIXIS / HAM MENORCA</h1>
            <p>DOCUMENTO CONFIDENCIAL DE ESCANDALLO Y RENTABILIDAD (NO ENVIAR AL CLIENTE)</p>
            <p style="color:var(--muted); font-weight:400;">Obra: EDAR - ACCIONA - ILLES BALEARS • Presupuesto Proveedor LUX-TOP Nº 3074/26 (10/11/2026)</p>
          </div>
        </div>
        <div class="meta">
          <h2>{DATA['codigo']} INTERNO</h2>
          <div class="ref-badge">{DATA['referencia']}</div>
          <p><strong>Fecha:</strong> {DATA['fecha']}</p>
          <p><strong>Ratio Venta:</strong> {tot['precio_ml_comercial_50ml']:.2f} €/ml (50 ml)</p>
        </div>
      </header>

      <section class="hero">
        <h3>Análisis Interno: Línea de Vida LUX-top® FSE 2003 (49,43 m plano / 50 ml) · 20 Soportes Especiales SOKO en Hormigón</h3>
        <p>Presupuesto elaborado a partir del coste neto oficial LUX-TOP nº 3074/26 (3.250,07 € base con 18% dto.) más replanteo in situ, montaje homologado de 20 postes ASP-SOKO (40 pernos M12 A4 en hormigón armado), medios auxiliares PEMP (2 jornadas), portes a Illes Balears y certificación con dinamómetro.</p>
      </section>

      <section class="kpi-grid">
        <div class="kpi red">
          <span class="label">Coste Material LUX-TOP</span>
          <span class="val">{tot['coste_material_luxtop_dixis']:,.2f} €</span>
        </div>
        <div class="kpi red">
          <span class="label">Coste Directo Total Dixis</span>
          <span class="val">{tot['coste_directo_total_dixis']:,.2f} €</span>
        </div>
        <div class="kpi">
          <span class="label">Base Imponible Cliente</span>
          <span class="val">{tot['base_imponible']:,.2f} €</span>
        </div>
        <div class="kpi green">
          <span class="label">Margen Bruto Operativo</span>
          <span class="val">{tot['margen_euros']:,.2f} € ({tot['margen_porcentaje']:.2f}%)</span>
        </div>
      </section>

      <h4>Escandallo Completo por Partidas (Costes Reales vs Precio de Venta Cliente)</h4>
      <table>
        <thead>
          <tr>
            <th class="c" style="width: 22px;">Nº</th>
            <th>Partida y Referencia</th>
            <th class="c" style="width: 24px;">Ud</th>
            <th class="r" style="width: 30px;">Cant.</th>
            <th class="r" style="width: 48px;">Tarifa</th>
            <th class="c" style="width: 26px;">Dto</th>
            <th class="r" style="width: 54px;">Coste Dixis</th>
            <th class="r" style="width: 54px;">Venta Cli.</th>
            <th class="r" style="width: 74px;">Margen (€ / %)</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
          <tr style="background:#fef3c7; font-weight:700;">
            <td colspan="6" class="r" style="padding:4px;">TOTALES ESCANDALLO OPERATIVO:</td>
            <td class="r" style="color:var(--tech-red); padding:4px;">{tot['coste_directo_total_dixis']:,.2f} €</td>
            <td class="r" style="color:var(--brand); padding:4px;">{tot['base_imponible']:,.2f} €</td>
            <td class="r" style="color:var(--tech-green); padding:4px;">{tot['margen_euros']:,.2f} € ({tot['margen_porcentaje']:.1f}%)</td>
          </tr>
        </tbody>
      </table>

      <div class="two-col">
        <div class="col">
          <h5>Desglose de Costes Internos y Sensibilidad MO</h5>
          <ul class="compact">
            <li><strong>Material LUX-TOP (3074/26):</strong> Tarifa oficial 3.963,50 € - 18% dto = <strong>3.250,07 €</strong> neto (+682,51 € IVA = 3.932,58 €). Venta material: 5.250,00 € (margen 1.999,93 € / 38,09%).</li>
            <li><strong>Mano de obra operativa (1.04):</strong> 2 oficiales x 16 h (2 jornadas) + replanteo = 32 h x 25 €/h (800 €) + 60 € brocas SDS Ø12 y consumibles = <strong>860,00 €</strong>.</li>
            <li><strong>Sensibilidad tarifa plena (costes-mo.json, 45 €/h):</strong> Si se imputa coste pleno de 45 €/h (1.440 € MO + 60 € cons. = 1.500 €), el coste total sube a <strong>5.240,07 €</strong> y el margen neto queda en <strong>2.259,93 € (30,13%)</strong>.</li>
            <li><strong>Otros costes directos:</strong> PEMP/medios 2 días (260 €), Porte Península-Baleares (120 €), Dinamómetro/Certificación/CAE (110 €).</li>
          </ul>
        </div>
        <div class="col">
          <h5>Tesorería, Logística y Condiciones Proveedor</h5>
          <ul class="compact">
            <li><strong>Pago a LUX-TOP:</strong> Giro comercial a <strong>60 días</strong> (Operación asegurada CESCE).</li>
            <li><strong>Pago cliente propuesto:</strong> 100% a la aceptación (o condiciones marco vigentes con Acciona Agua, S.A.).</li>
            <li><strong>Portes a Baleares:</strong> Las condiciones LUX-TOP 3074/26 limitan portes pagados a Península; el envío especial SOKO a Illes Balears se cubre en partida 1.06 (coste est. 120 € / PVP 180 €).</li>
            <li><strong>Precio unitario comparativo:</strong> 150,00 €/ml (50 ml) / 151,73 €/ml (49,43 ml plano), muy alineado con P-2026-0055 (145,60 €/ml) pese a llevar 20 soportes especiales SOKO en hormigón.</li>
          </ul>
        </div>
      </div>

      <div class="alert-box">
        <strong>RIESGOS TÉCNICOS Y RECORDATORIO ANTES DE PEDIDO A FÁBRICA LUX-TOP:</strong><br>
        1) <strong>Confirmar medidas SOKO antes de pedir:</strong> El presupuesto 3074/26 pide indicar <em>"long: H+V / 20+20 cm y posición placa H"</em> y no admite devolución de soportes especiales SOKO ni cable cortado. Realizar visita de replanteo al aceptar el cliente.<br>
        2) <strong>Plazo SOKO (20-25 días):</strong> Informado expresamente al cliente para evitar penalizaciones de plazo.<br>
        3) <strong>Estado del hormigón y ferralla:</strong> Muros antiguos de EDAR pueden tener armadura superficial o carbonatación; verificar espesor y calidad del hormigón en replanteo por si algún punto requiriera anclaje químico en lugar de perno mecánico MKT BZ3 M12.
      </div>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • HAM Menorca • Oficina Técnica</div>
      <div>{DATA['codigo']} • Estudio Interno LUX-top® 3074/26 · EDAR ACCIONA • Hoja 1 de 1</div>
    </footer>
  </div>
</body>
</html>"""

    path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML Técnico generado: {path}")
    return path


def convert_to_pdf(html_file, pdf_file):
    if not os.path.exists(CHROME_PATH):
        raise FileNotFoundError(f"Chrome no encontrado en: {CHROME_PATH}")
    uri = "file:///" + html_file.replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        uri,
    ]
    subprocess.run(cmd, check=True)
    print(f"PDF generado: {pdf_file}")


if __name__ == "__main__":
    create_excel()
    c_html = create_html_client()
    convert_to_pdf(c_html, os.path.join(BASE_DIR, "presupuesto-cliente.pdf"))
    t_html = create_html_technical()
    convert_to_pdf(t_html, os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf"))
    print("Generación completada con éxito.")
