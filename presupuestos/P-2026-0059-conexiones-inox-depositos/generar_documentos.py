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


def calc_partida(p, tarifas):
    mat_total = sum(m["cantidad"] * m["coste_unitario_est"] for m in p["materiales_inox"])
    cons_total = p["cantidad"] * p["consumibles_tig_por_ud"]
    mo_taller = p["cantidad"] * (
        p["mo_taller_horas_tig_por_ud"] * tarifas["oficial_1_taller_tig"]
        + p["mo_taller_horas_prep_por_ud"] * tarifas["oficial_2_taller"]
    )
    tarifa_equipo_obra = tarifas["oficial_montaje_obra"] + tarifas["ayudante_montaje_obra"]
    mo_obra = p["cantidad"] * p["mo_obra_horas_equipo_por_ud"] * tarifa_equipo_obra
    transporte = p["cantidad"] * p["transporte_por_ud"]
    coste_total = mat_total + cons_total + mo_taller + mo_obra + transporte
    venta_total = p["cantidad"] * p["precio_cliente_unitario"]
    beneficio = venta_total - coste_total
    margen_venta = (beneficio / venta_total * 100) if venta_total else 0.0
    margen_coste = (beneficio / coste_total * 100) if coste_total else 0.0
    return {
        "mat_total": mat_total,
        "cons_total": cons_total,
        "mo_taller": mo_taller,
        "mo_obra": mo_obra,
        "transporte": transporte,
        "coste_total": coste_total,
        "coste_unitario": coste_total / p["cantidad"],
        "venta_total": venta_total,
        "beneficio": beneficio,
        "margen_venta": margen_venta,
        "margen_coste": margen_coste,
    }


def create_excel():
    wb = Workbook()

    NAVY = "0F172A"
    GOLD = "B45309"
    SLATE_LIGHT = "F8FAFC"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"
    EDIT_FILL = "FEF9C3"
    RED_DARK = "B91C1C"
    GREEN_DARK = "15803D"

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    fill_edit = PatternFill(start_color=EDIT_FILL, end_color=EDIT_FILL, fill_type="solid")

    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_tot = Font(name="Segoe UI", size=10.5, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=10.5, bold=True, color=GOLD)
    font_warn = Font(name="Segoe UI", size=8.5, bold=True, color=RED_DARK)
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
    # HOJA 1: PRESUPUESTO CLIENTE
    # ------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Cliente"
    ws1.views.sheetView[0].showGridLines = True

    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} • CONEXIONES INOX AISI 316L A DEPÓSITOS (SOLDADURA TIG)"
    ws1["B3"].font = font_title

    meta_rows = [
        ("REFERENCIA:", DATA["referencia"]),
        ("ESTADO:", DATA["estado_presupuesto"]),
        ("CLIENTE / OBRA:", f"{DATA['cliente']['nombre']} — {DATA['cliente']['obra']}"),
        ("FECHA / VALIDEZ:", f"{DATA['fecha']} • Validez: {DATA['validez_dias']} días naturales"),
        ("PROCESO / CALIDAD:", f"{DATA['calidad_inox']} · {DATA['proceso_soldadura']}"),
    ]
    for idx, (k, v) in enumerate(meta_rows, start=5):
        ws1[f"B{idx}"] = k
        ws1[f"B{idx}"].font = font_bold
        ws1[f"C{idx}"] = v
        ws1[f"C{idx}"].font = font_warn if k == "ESTADO:" else font_reg

    ws1["B11"] = "DESGLOSE DE PARTIDAS (SUMINISTRO, FABRICACIÓN TIG EN TALLER E INSTALACIÓN EN OBRA)"
    ws1["B11"].font = font_sec

    headers_client = ["Nº", "Concepto y Descripción Técnica", "Ud.", "Cantidad", "Precio Unitario", "Subtotal"]
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

        c_qty = ws1.cell(row=row_cur, column=5, value=p["cantidad"])
        c_qty.font = font_bold
        c_qty.number_format = "#,##0.00"
        c_qty.alignment = Alignment(horizontal="right", vertical="top")

        c_pu = ws1.cell(row=row_cur, column=6, value=p["precio_cliente_unitario"])
        c_pu.font = font_reg
        c_pu.number_format = '#,##0.00 "€"'
        c_pu.alignment = Alignment(horizontal="right", vertical="top")

        c_sub = ws1.cell(row=row_cur, column=7, value=f"=E{row_cur}*F{row_cur}")
        c_sub.font = font_bold
        c_sub.number_format = '#,##0.00 "€"'
        c_sub.alignment = Alignment(horizontal="right", vertical="top")

        for col in range(2, 8):
            cell = ws1.cell(row=row_cur, column=col)
            cell.border = border_thin
            if row_cur % 2 == 0:
                cell.fill = fill_alt
        ws1.row_dimensions[row_cur].height = 66
        row_cur += 1

    last_item_row = row_cur - 1
    row_base = row_cur + 1
    ws1.cell(row=row_base, column=6, value="BASE IMPONIBLE:").font = font_tot
    c_base = ws1.cell(row=row_base, column=7, value=f"=SUM(G13:G{last_item_row})")
    c_base.font = font_tot
    c_base.number_format = '#,##0.00 "€"'
    c_base.fill = fill_tot
    c_base.border = border_thin

    row_iva = row_base + 1
    ws1.cell(row=row_iva, column=6, value="IVA (21%):").font = font_bold
    c_iva = ws1.cell(row=row_iva, column=7, value=f"=G{row_base}*0.21")
    c_iva.font = font_bold
    c_iva.number_format = '#,##0.00 "€"'
    c_iva.border = border_thin

    row_tot = row_iva + 1
    ws1.cell(row=row_tot, column=6, value="TOTAL PRESUPUESTO:").font = font_tot_gold
    c_tot = ws1.cell(row=row_tot, column=7, value=f"=G{row_base}+G{row_iva}")
    c_tot.font = font_tot_gold
    c_tot.number_format = '#,##0.00 "€"'
    c_tot.fill = fill_tot
    c_tot.border = border_total

    ws1.column_dimensions["A"].width = 3
    ws1.column_dimensions["B"].width = 10
    ws1.column_dimensions["C"].width = 68
    ws1.column_dimensions["D"].width = 8
    ws1.column_dimensions["E"].width = 11
    ws1.column_dimensions["F"].width = 16
    ws1.column_dimensions["G"].width = 16

    # ------------------------------------------------------------------
    # HOJA 2: MATERIALES INOX (EDITABLE AL RECIBIR OFERTA PROVEEDOR)
    # ------------------------------------------------------------------
    ws2 = wb.create_sheet("Materiales Inox (Proveedor)")
    ws2["B2"] = f"LISTA DE MATERIALES INOX AISI 316L — {DATA['codigo']} (Celdas amarillas editables al recibir oferta)"
    ws2["B2"].font = font_title

    headers_mat = ["Partida", "Material Inoxidable (AISI 316L)", "Ud.", "Cantidad", "Coste Unit. Prov. (Est.)", "Coste Total", "Estado"]
    for c_idx, h in enumerate(headers_mat, start=2):
        cell = ws2.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws2.row_dimensions[4].height = 24

    r2 = 5
    partida_mat_ranges = {}
    for p in DATA["partidas"]:
        start_r = r2
        for m in p["materiales_inox"]:
            ws2.cell(row=r2, column=2, value=f"{p['id']} ({p['diametro_pvco']})").font = font_bold
            ws2.cell(row=r2, column=3, value=m["concepto"]).font = font_reg
            ws2.cell(row=r2, column=4, value=m["unidad"]).alignment = Alignment(horizontal="center")
            ws2.cell(row=r2, column=5, value=m["cantidad"]).number_format = "#,##0.00"
            c_pu = ws2.cell(row=r2, column=6, value=m["coste_unitario_est"])
            c_pu.number_format = '#,##0.00 "€"'
            c_pu.fill = fill_edit
            c_pu.font = font_bold
            c_tot_m = ws2.cell(row=r2, column=7, value=f"=E{r2}*F{r2}")
            c_tot_m.number_format = '#,##0.00 "€"'
            c_tot_m.font = font_bold
            c_est = ws2.cell(row=r2, column=8, value=m["estado"])
            c_est.font = font_warn
            for col in range(2, 9):
                ws2.cell(row=r2, column=col).border = border_thin
            r2 += 1
        end_r = r2 - 1
        partida_mat_ranges[p["id"]] = (start_r, end_r)

    ws2.cell(row=r2 + 1, column=6, value="TOTAL MATERIAL INOX:").font = font_tot
    c_mat_all = ws2.cell(row=r2 + 1, column=7, value=f"=SUM(G5:G{r2-1})")
    c_mat_all.font = font_tot
    c_mat_all.number_format = '#,##0.00 "€"'
    c_mat_all.fill = fill_tot
    c_mat_all.border = border_total

    ws2.column_dimensions["A"].width = 3
    ws2.column_dimensions["B"].width = 18
    ws2.column_dimensions["C"].width = 52
    ws2.column_dimensions["D"].width = 12
    ws2.column_dimensions["E"].width = 10
    ws2.column_dimensions["F"].width = 20
    ws2.column_dimensions["G"].width = 15
    ws2.column_dimensions["H"].width = 22

    # ------------------------------------------------------------------
    # HOJA 3: DESGLOSE INTERNO TÉCNICO
    # ------------------------------------------------------------------
    ws3 = wb.create_sheet("Desglose Interno Técnico")
    ws3["B2"] = f"ESTUDIO INTERNO DE COSTES Y MÁRGENES — {DATA['codigo']}"
    ws3["B2"].font = font_title
    ws3["B3"] = "Tarifas MO: Oficial 1ª TIG 40 €/h · Oficial 2ª Prep. 35 €/h · Montaje Obra (2 op.) 80 €/h equipo"
    ws3["B3"].font = font_sub

    headers_int = [
        "Partida", "Ud.", "Material Inox", "Consumibles TIG",
        "MO Taller (TIG+Prep)", "MO Montaje Obra", "Transporte",
        "Coste Directo Total", "Coste/Ud", "Venta Total", "Beneficio €", "Margen s/Venta"
    ]
    for c_idx, h in enumerate(headers_int, start=2):
        cell = ws3.cell(row=5, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_thin
    ws3.row_dimensions[5].height = 28

    r3 = 6
    tarifas = DATA["tarifas_mo"]
    for idx_p, p in enumerate(DATA["partidas"]):
        calc = calc_partida(p, tarifas)
        s_r, e_r = partida_mat_ranges[p["id"]]
        client_row = 13 + idx_p

        ws3.cell(row=r3, column=2, value=f"{p['id']} {p['diametro_pvco']}").font = font_bold
        ws3.cell(row=r3, column=3, value=p["cantidad"]).alignment = Alignment(horizontal="center")

        c_mat = ws3.cell(row=r3, column=4, value=f"=SUM('Materiales Inox (Proveedor)'!G{s_r}:G{e_r})")
        c_cons = ws3.cell(row=r3, column=5, value=calc["cons_total"])
        c_mot = ws3.cell(row=r3, column=6, value=calc["mo_taller"])
        c_moo = ws3.cell(row=r3, column=7, value=calc["mo_obra"])
        c_tra = ws3.cell(row=r3, column=8, value=calc["transporte"])
        c_cd = ws3.cell(row=r3, column=9, value=f"=SUM(D{r3}:H{r3})")
        c_cu = ws3.cell(row=r3, column=10, value=f"=I{r3}/C{r3}")
        c_vt = ws3.cell(row=r3, column=11, value=f"='Presupuesto Cliente'!G{client_row}")
        c_ben = ws3.cell(row=r3, column=12, value=f"=K{r3}-I{r3}")
        c_mg = ws3.cell(row=r3, column=13, value=f"=L{r3}/K{r3}")

        for col_c in [c_mat, c_cons, c_mot, c_moo, c_tra, c_cd, c_cu, c_vt, c_ben]:
            col_c.number_format = '#,##0.00 "€"'
            col_c.font = font_reg
        c_cd.font = font_bold
        c_vt.font = font_bold
        c_ben.font = font_green
        c_mg.number_format = "0.0%"
        c_mg.font = font_green

        for col in range(2, 14):
            ws3.cell(row=r3, column=col).border = border_thin
        r3 += 1

    ws3.cell(row=r3, column=2, value="TOTALES").font = font_tot
    for col in range(4, 13):
        if col == 10:
            continue
        col_let = chr(64 + col)
        c_sum = ws3.cell(row=r3, column=col, value=f"=SUM({col_let}6:{col_let}{r3-1})")
        c_sum.number_format = '#,##0.00 "€"'
        c_sum.font = font_tot
        c_sum.fill = fill_tot
        c_sum.border = border_total
    c_mg_tot = ws3.cell(row=r3, column=13, value=f"=L{r3}/K{r3}")
    c_mg_tot.number_format = "0.0%"
    c_mg_tot.font = font_tot_gold
    c_mg_tot.fill = fill_tot
    c_mg_tot.border = border_total

    for col_idx, w in enumerate([3, 18, 7, 14, 14, 17, 16, 12, 16, 13, 15, 14, 14], start=1):
        col_let = chr(64 + col_idx)
        ws3.column_dimensions[col_let].width = w

    xlsx_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0059_Conexiones_Inox_Depositos.xlsx")
    wb.save(xlsx_path)
    return xlsx_path


def create_html_and_pdf():
    tarifas = DATA["tarifas_mo"]
    calcs = [calc_partida(p, tarifas) for p in DATA["partidas"]]
    base_imponible = sum(c["venta_total"] for c in calcs)
    iva = base_imponible * 0.21
    total_con_iva = base_imponible + iva

    coste_total_global = sum(c["coste_total"] for c in calcs)
    beneficio_global = base_imponible - coste_total_global
    margen_global = (beneficio_global / base_imponible * 100) if base_imponible else 0.0

    # --- CLIENTE HTML ---
    rows_cli = ""
    for p, c in zip(DATA["partidas"], calcs):
        rows_cli += f"""
        <tr>
          <td class="center bold">{p['id']}</td>
          <td><strong>{p['concepto']}</strong><br><span class="desc">{p['descripcion']}</span></td>
          <td class="center">{p['unidad']}</td>
          <td class="right bold">{p['cantidad']:,.2f}</td>
          <td class="right">{eur(p['precio_cliente_unitario'])}</td>
          <td class="right bold">{eur(c['venta_total'])}</td>
        </tr>"""

    no_inc_li = "".join(f"<li>{item}</li>" for item in DATA["condiciones_comerciales"]["no_incluido"])

    html_cliente = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presupuesto {DATA['codigo']} — Conexiones Inox Depósitos</title>
  <style>
    @page {{ size: A4; margin: 12mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; margin: 0; font-size: 9.5pt; line-height: 1.4; }}
    .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #0f172a; padding-bottom: 10px; margin-bottom: 14px; }}
    .brand {{ font-size: 13pt; font-weight: 800; color: #0f172a; }}
    .subbrand {{ font-size: 8.5pt; color: #b45309; font-weight: 700; text-transform: uppercase; }}
    .company-info {{ text-align: right; font-size: 8pt; color: #475569; }}
    h1 {{ font-size: 12.5pt; color: #0f172a; margin: 0 0 8px 0; }}
    .banner-prov {{ background: #fef3c7; border-left: 4px solid #b45309; padding: 7px 10px; font-size: 8.5pt; margin-bottom: 12px; color: #78350f; }}
    .meta {{ width: 100%; border-collapse: collapse; margin-bottom: 14px; font-size: 8.5pt; }}
    .meta td {{ padding: 4px 6px; border: 1px solid #cbd5e1; }}
    .meta td.lbl {{ background: #f1f5f9; font-weight: 700; width: 18%; }}
    table.items {{ width: 100%; border-collapse: collapse; margin-bottom: 14px; }}
    table.items th {{ background: #0f172a; color: #fff; padding: 7px 6px; font-size: 8.5pt; text-align: left; }}
    table.items td {{ padding: 7px 6px; border-bottom: 1px solid #cbd5e1; vertical-align: top; }}
    .desc {{ font-size: 8pt; color: #475569; }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .totals {{ width: 42%; margin-left: auto; border-collapse: collapse; margin-bottom: 14px; }}
    .totals td {{ padding: 5px 8px; border: 1px solid #cbd5e1; }}
    .totals .grand {{ background: #fef3c7; font-weight: 800; font-size: 10.5pt; color: #0f172a; }}
    .conds {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 10px 12px; font-size: 8.5pt; }}
    .conds h3 {{ margin: 0 0 6px 0; font-size: 9.5pt; color: #0f172a; }}
    .conds ul {{ margin: 4px 0 0 18px; padding: 0; }}
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="subbrand">DIXIS RECURSOS Y SOLUCIONES S.L. · CIF B57825432</div>
      <div class="brand">HAM ESTRUCTURAS METÁLICAS MENORCA</div>
    </div>
    <div class="company-info">
      Av. Circunval·lació, 11 · Pol. Sant Lluís (Menorca)<br>
      Tel: +34 971 35 20 18 · Móvil: +34 669 769 541<br>
      info@hamenorca.com · www.hamenorca.com
    </div>
  </div>

  <h1>PRESUPUESTO {DATA['codigo']} — {DATA['proyecto']['titulo']}</h1>
  <div class="banner-prov"><strong>BORRADOR PROVISIONAL:</strong> Importes sujetos a actualización con costes definitivos de material inoxidable de proveedor.</div>

  <table class="meta">
    <tr><td class="lbl">Referencia</td><td>{DATA['referencia']}</td><td class="lbl">Fecha</td><td>{DATA['fecha']}</td></tr>
    <tr><td class="lbl">Cliente / Obra</td><td>{DATA['cliente']['nombre']} — {DATA['cliente']['obra']}</td><td class="lbl">Validez</td><td>{DATA['validez_dias']} días naturales</td></tr>
    <tr><td class="lbl">Calidad / Proceso</td><td colspan="3">{DATA['calidad_inox']} · {DATA['proceso_soldadura']}</td></tr>
  </table>

  <table class="items">
    <thead>
      <tr>
        <th class="center" style="width:6%">Nº</th>
        <th style="width:52%">Concepto y Descripción Técnica</th>
        <th class="center" style="width:6%">Ud.</th>
        <th class="right" style="width:10%">Cant.</th>
        <th class="right" style="width:13%">Precio Ud.</th>
        <th class="right" style="width:13%">Subtotal</th>
      </tr>
    </thead>
    <tbody>{rows_cli}</tbody>
  </table>

  <table class="totals">
    <tr><td class="bold">Base Imponible</td><td class="right bold">{eur(base_imponible)}</td></tr>
    <tr><td>IVA (21%)</td><td class="right">{eur(iva)}</td></tr>
    <tr class="grand"><td>TOTAL PRESUPUESTO</td><td class="right">{eur(total_con_iva)}</td></tr>
  </table>

  <div class="conds">
    <h3>Condiciones Comerciales y Alcance</h3>
    <p><strong>Forma de pago:</strong> {DATA['condiciones_comerciales']['forma_pago']}<br>
    <strong>Plazo estimado:</strong> {DATA['condiciones_comerciales']['plazo_entrega']}</p>
    <strong>No incluido:</strong>
    <ul>{no_inc_li}</ul>
  </div>
</body>
</html>"""

    # --- INTERNO TECNICO HTML ---
    rows_int = ""
    for p, c in zip(DATA["partidas"], calcs):
        rows_int += f"""
        <tr>
          <td class="bold">{p['id']} {p['diametro_pvco']}<br><span class="desc">{p['equivalencia_dn']}</span></td>
          <td class="center">{p['cantidad']}</td>
          <td class="right">{eur(c['mat_total'])}</td>
          <td class="right">{eur(c['cons_total'])}</td>
          <td class="right">{eur(c['mo_taller'])}</td>
          <td class="right">{eur(c['mo_obra'])}</td>
          <td class="right">{eur(c['transporte'])}</td>
          <td class="right bold">{eur(c['coste_total'])}</td>
          <td class="right bold">{eur(c['venta_total'])}</td>
          <td class="right green">{eur(c['beneficio'])} ({c['margen_venta']:.1f}%)</td>
        </tr>"""

    rows_mat = ""
    for p in DATA["partidas"]:
        for m in p["materiales_inox"]:
            sub_m = m["cantidad"] * m["coste_unitario_est"]
            rows_mat += f"""
            <tr>
              <td>{p['id']} ({p['diametro_pvco']})</td>
              <td>{m['concepto']}</td>
              <td class="center">{m['unidad']}</td>
              <td class="right">{m['cantidad']}</td>
              <td class="right warn">{eur(m['coste_unitario_est'])}</td>
              <td class="right bold">{eur(sub_m)}</td>
            </tr>"""

    html_interno = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Estudio Interno {DATA['codigo']} — Conexiones Inox TIG</title>
  <style>
    @page {{ size: A4 landscape; margin: 10mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; margin: 0; font-size: 8.5pt; line-height: 1.35; }}
    h1 {{ font-size: 12pt; color: #0f172a; margin: 0 0 4px 0; }}
    h2 {{ font-size: 10pt; color: #0f172a; margin: 12px 0 6px 0; border-bottom: 2px solid #b45309; padding-bottom: 2px; }}
    .banner {{ background: #fee2e2; border-left: 4px solid #b91c1c; padding: 6px 10px; font-size: 8pt; color: #7f1d1d; margin-bottom: 10px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
    th {{ background: #0f172a; color: #fff; padding: 5px; font-size: 8pt; text-align: left; }}
    td {{ padding: 5px; border-bottom: 1px solid #cbd5e1; vertical-align: top; }}
    .right {{ text-align: right; }}
    .center {{ text-align: center; }}
    .bold {{ font-weight: 700; }}
    .green {{ color: #15803d; font-weight: 700; }}
    .warn {{ color: #b45309; font-weight: 700; }}
    .tot {{ background: #fef3c7; font-weight: 800; }}
    .desc {{ font-size: 7.5pt; color: #64748b; }}
  </style>
</head>
<body>
  <h1>DOCUMENTO INTERNO TÉCNICO — {DATA['codigo']} · Conexiones Inox AISI 316L (Soldadura TIG en Taller)</h1>
  <div class="banner"><strong>USO INTERNO EXCLUSIVO:</strong> Precios de material inoxidable marcados como <em>ESTIMADOS</em> pendientes de oferta real de proveedor. Sin empalmes en tubos (1 barra de 6 m por cada subida de hasta 5 m).</div>

  <h2>1. Resumen Económico por Partida</h2>
  <table>
    <thead>
      <tr>
        <th>Partida</th><th class="center">Ud.</th><th class="right">Mat. Inox (Est.)</th><th class="right">Consum. TIG</th>
        <th class="right">MO Taller TIG</th><th class="right">MO Obra</th><th class="right">Transp.</th>
        <th class="right">Coste Directo</th><th class="right">Venta Cliente</th><th class="right">Beneficio (Margen)</th>
      </tr>
    </thead>
    <tbody>
      {rows_int}
      <tr class="tot">
        <td>TOTALES</td><td class="center">12</td>
        <td class="right">{eur(sum(c['mat_total'] for c in calcs))}</td>
        <td class="right">{eur(sum(c['cons_total'] for c in calcs))}</td>
        <td class="right">{eur(sum(c['mo_taller'] for c in calcs))}</td>
        <td class="right">{eur(sum(c['mo_obra'] for c in calcs))}</td>
        <td class="right">{eur(sum(c['transporte'] for c in calcs))}</td>
        <td class="right">{eur(coste_total_global)}</td>
        <td class="right">{eur(base_imponible)}</td>
        <td class="right green">{eur(beneficio_global)} ({margen_global:.1f}%)</td>
      </tr>
    </tbody>
  </table>

  <h2>2. Desglose de Materiales Inox a Confirmar con Proveedor</h2>
  <table>
    <thead>
      <tr><th>Partida</th><th>Concepto Material (AISI 316L)</th><th class="center">Ud.</th><th class="right">Cant.</th><th class="right">Coste Ud. (Est.)</th><th class="right">Subtotal</th></tr>
    </thead>
    <tbody>{rows_mat}</tbody>
  </table>
</body>
</html>"""

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
            subprocess.run([
                CHROME_PATH, "--headless", "--disable-gpu",
                "--no-pdf-header-footer", f"--print-to-pdf={p_path}", h_path
            ], check=False)

    return cli_html, int_html, cli_pdf, int_pdf


if __name__ == "__main__":
    xlsx = create_excel()
    cli_h, int_h, cli_p, int_p = create_html_and_pdf()
    print("Generados correctamente:")
    for f in [xlsx, cli_h, cli_p, int_h, int_p]:
        print(" -", f)
