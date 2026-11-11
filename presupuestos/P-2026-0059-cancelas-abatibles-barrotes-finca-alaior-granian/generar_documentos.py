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


def fmt_num(val, dec=2):
    s = f"{val:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_eur(val):
    return f"{fmt_num(val, 2)} €"


def create_excel():
    wb = Workbook()

    NAVY = "0F172A"
    GOLD = "B45309"
    BLUE = "0369A1"
    SLATE_LIGHT = "F8FAFC"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"
    HIGHLIGHT_FILL = "EFF6FF"
    GREEN_DARK = "15803D"

    f_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    f_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    f_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    f_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    f_hl = PatternFill(start_color=HIGHLIGHT_FILL, end_color=HIGHLIGHT_FILL, fill_type="solid")

    fn_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    fn_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    fn_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    fn_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    fn_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    fn_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    fn_tot = Font(name="Segoe UI", size=10.5, bold=True, color=NAVY)
    fn_tot_gold = Font(name="Segoe UI", size=10.5, bold=True, color=GOLD)
    fn_green = Font(name="Segoe UI", size=9, bold=True, color=GREEN_DARK)
    fn_blue = Font(name="Segoe UI", size=9.5, bold=True, color=BLUE)

    b_thin = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )
    b_tot = Border(
        top=Side(style="thin", color=NAVY),
        bottom=Side(style="double", color=NAVY),
    )

    NUM_EUR = "#,##0.00 €"
    NUM_DEC = "#,##0.00"
    NUM_PCT = "0.00%"

    # ------------------------------------------------------------------
    # HOJA 1: PRESUPUESTO CLIENTE (LIMPIO)
    # ------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Presupuesto Cliente"
    ws1.views.sheetView[0].showGridLines = True

    ws1["B2"] = f"{DATA['emisor']['razon_social'].upper()} | {DATA['emisor']['nombre_comercial'].upper()}"
    ws1["B2"].font = fn_sub
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} • CANCELAS METÁLICAS ABATIBLES CON BARROTES · FINCA ALAIOR"
    ws1["B3"].font = fn_title

    meta_rows = [
        ("REFERENCIA:", DATA["referencia"]),
        ("CLIENTE:", f"{DATA['cliente']['nombre']} (Att. {DATA['cliente']['contacto']})"),
        ("UBICACIÓN:", DATA["cliente"]["ubicacion"]),
        ("FECHA / VALIDEZ:", f"{DATA['fecha']} • Validez: {DATA['validez_dias']} días naturales"),
        ("REFERENCIA VISUAL:", DATA["cliente"]["referencia_solicitud"]),
    ]
    for idx, (k, v) in enumerate(meta_rows, start=5):
        ws1[f"B{idx}"] = k
        ws1[f"B{idx}"].font = fn_bold
        ws1[f"C{idx}"] = v
        ws1[f"C{idx}"].font = fn_reg

    ws1["B11"] = "DESGLOSE COMERCIAL — FABRICACIÓN, TRATAMIENTO ANTICORROSIVO C4 E INSTALACIÓN"
    ws1["B11"].font = fn_sec

    headers_client = ["Cód.", "Concepto y Especificación Técnica", "Medidas / Hojas", "Ud.", "Cantidad", "Precio Ud.", "Subtotal"]
    for c_idx, h in enumerate(headers_client, start=2):
        cell = ws1.cell(row=12, column=c_idx, value=h)
        cell.font = fn_header
        cell.fill = f_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = b_thin
    ws1.row_dimensions[12].height = 24

    r = 13
    for idx, p in enumerate(DATA["partidas"]):
        ws1.cell(row=r, column=2, value=p["codigo"]).alignment = Alignment(horizontal="center", vertical="top")
        ws1.cell(row=r, column=3, value=f"{p['concepto']}\n{p['descripcion']}").alignment = Alignment(wrap_text=True, vertical="top")
        ws1.cell(row=r, column=4, value=f"{p['dimensiones']}\n{p['hojas']}").alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
        ws1.cell(row=r, column=5, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
        c_cant = ws1.cell(row=r, column=6, value=p["cantidad"])
        c_cant.alignment = Alignment(horizontal="right", vertical="top")
        c_cant.number_format = NUM_DEC
        c_pu = ws1.cell(row=r, column=7, value=p["precio_unitario"])
        c_pu.alignment = Alignment(horizontal="right", vertical="top")
        c_pu.number_format = NUM_EUR
        c_sub = ws1.cell(row=r, column=8, value=f"=F{r}*G{r}")
        c_sub.alignment = Alignment(horizontal="right", vertical="top")
        c_sub.number_format = NUM_EUR

        for col in range(2, 9):
            cell = ws1.cell(row=r, column=col)
            cell.font = fn_bold if col in (2, 8) else fn_reg
            cell.border = b_thin
            if idx % 2 == 1:
                cell.fill = f_alt
        ws1.row_dimensions[r].height = 56
        r += 1

    # Totales
    ws1.cell(row=r, column=7, value="SOLO SUMINISTRO (01 + 02):").font = fn_blue
    ws1.cell(row=r, column=7).alignment = Alignment(horizontal="right")
    c_sum = ws1.cell(row=r, column=8, value="=SUM(H13:H14)")
    c_sum.font = fn_blue
    c_sum.number_format = NUM_EUR
    c_sum.fill = f_hl
    c_sum.border = b_thin
    r += 1

    base_row = r
    ws1.cell(row=r, column=7, value="BASE IMPONIBLE TOTAL (LLAVE EN MANO):").font = fn_bold
    ws1.cell(row=r, column=7).alignment = Alignment(horizontal="right")
    c_base = ws1.cell(row=r, column=8, value="=SUM(H13:H15)")
    c_base.font = fn_tot
    c_base.number_format = NUM_EUR
    c_base.border = b_thin
    r += 1

    ws1.cell(row=r, column=7, value="I.V.A. (21,00%):").font = fn_reg
    ws1.cell(row=r, column=7).alignment = Alignment(horizontal="right")
    c_iva = ws1.cell(row=r, column=8, value=f"=H{base_row}*0.21")
    c_iva.font = fn_bold
    c_iva.number_format = NUM_EUR
    c_iva.border = b_thin
    r += 1

    ws1.cell(row=r, column=7, value="TOTAL PRESUPUESTO (I.V.A. INCLUIDO):").font = fn_tot_gold
    ws1.cell(row=r, column=7).alignment = Alignment(horizontal="right")
    c_tot = ws1.cell(row=r, column=8, value=f"=H{base_row}*1.21")
    c_tot.font = fn_tot_gold
    c_tot.number_format = NUM_EUR
    c_tot.fill = f_tot
    c_tot.border = b_tot
    r += 2

    # Opcional Galvanizado
    opt = DATA["opcionales"][0]
    ws1.cell(row=r, column=2, value="ALTERNATIVA OPCIONAL DE MÁXIMA DURABILIDAD (MENORCA)").font = fn_sec
    r += 1
    ws1.cell(row=r, column=2, value=opt["codigo"]).font = fn_bold
    ws1.cell(row=r, column=3, value=f"{opt['concepto']}\n{opt['descripcion']}").font = fn_reg
    ws1.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="top")
    ws1.cell(row=r, column=5, value=opt["unidad"]).alignment = Alignment(horizontal="center", vertical="top")
    ws1.cell(row=r, column=6, value=opt["cantidad"]).number_format = NUM_DEC
    ws1.cell(row=r, column=7, value=opt["precio_unitario"]).number_format = NUM_EUR
    ws1.cell(row=r, column=8, value=f"=F{r}*G{r}").number_format = NUM_EUR
    for col in range(2, 9):
        c = ws1.cell(row=r, column=col)
        c.border = b_thin
        c.fill = f_tot
        if col in (2, 8):
            c.font = fn_bold
    ws1.row_dimensions[r].height = 46
    r += 2

    ws1.cell(row=r, column=2, value="PLAZO DE ENTREGA, CONDICIONES Y EXCLUSIONES").font = fn_sec
    r += 1
    cond_lines = [
        f"• Plazo estimado (Opción Base C4): {DATA['condiciones']['plazo_entrega_base']}",
        f"• Plazo estimado (Alternativa B Galvanizado): {DATA['condiciones']['plazo_entrega_galvanizado']}",
        f"• Tratamiento superficial: {DATA['condiciones']['acabado_ham']}",
        f"• Forma de pago: {DATA['condiciones']['forma_pago']} · Validez: {DATA['condiciones']['validez']}.",
    ] + [f"• Exclusión: {e}" for e in DATA["exclusiones"]]
    for line in cond_lines:
        ws1.cell(row=r, column=2, value=line).font = fn_reg
        r += 1

    for col, w in [(1, 3), (2, 12), (3, 62), (4, 22), (5, 8), (6, 11), (7, 15), (8, 16)]:
        ws1.column_dimensions[get_column_letter(col)].width = w

    # ------------------------------------------------------------------
    # HOJA 2: ESCANDALLO INTERNO Y MÁRGENES
    # ------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Escandallo Interno")
    ws2["B2"] = f"ESTUDIO TÉCNICO INTERNO Y ESCANDALLO · {DATA['codigo']}"
    ws2["B2"].font = fn_title
    ws2["B3"] = "CONFIDENCIAL HAM / DIXIS — NO ENTREGAR AL CLIENTE"
    ws2["B3"].font = fn_sub

    headers_esc = ["Bloque", "Concepto de Coste Directo", "Medición / Base", "Coste Directo", "Venta Neta", "Margen (€)", "Margen (%)"]
    for c_idx, h in enumerate(headers_esc, start=2):
        cell = ws2.cell(row=5, column=c_idx, value=h)
        cell.font = fn_header
        cell.fill = f_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = b_thin
    ws2.row_dimensions[5].height = 24

    esc = DATA["escandallo_interno"]
    fab = esc["fabricacion_y_tratamiento"]
    mon = esc["replanteo_transporte_montaje"]

    rows_esc = [
        ("Materiales", "Perfilería tubular acero S235JR (40x40x2 + 20x20x2 incl. 5% merma)", "276 kg × 1,85 €/kg", fab["coste_acero_material"], None),
        ("Materiales", "Herrajes (16 bisagras regulables + 4 pasadores portacandado + 4 fallebas/topes)", "Lote 4 juegos", fab["coste_herrajes_bisagras_pasadores"], None),
        ("Materiales", "Anclajes químicos + 64 varillas inox A4 + consumibles MIG/corte", "Lote obra + taller", fab["coste_anclajes_a4_quimico_consumibles"], None),
        ("Técnica", "Oficina técnica, despiece, plantillas remate dos aguas", "4,0 h × 35,00 €/h", fab["coste_oficina_tecnica"], None),
        ("Taller", "Mano de obra fabricación taller HAM (4 juegos / 8 hojas)", "32,0 h × 35,00 €/h", fab["coste_mo_taller"], None),
        ("Tratamiento C4", "Sistema C4 HAM: materiales epoxi zinc + PU 2C (240 €) + MO cabina (16 h × 30 €)", "24 m² / 16 h", fab["coste_tratamiento_c4_total"], None),
        ("SUBTOTAL FAB.", "TOTAL FABRICACIÓN + TRATAMIENTO C4 (PARTIDAS 01 + 02)", "4 cancelas", "=SUM(E6:E11)", fab["venta_total"]),
        ("Replanteo", "Visita técnica medición huecos entre pilares en Alaior", "2,0 h × 35,00 €/h", mon["coste_replanteo"], None),
        ("Logística", "Transporte finca Alaior + furgón taller + grupo electrógeno", "2 viajes / lote", mon["coste_transporte_furgon_generador"], None),
        ("Montaje", "Instalación en obra (2 operarios × 2 jornadas = 32 h)", "32,0 h × 35,00 €/h", mon["coste_mo_montaje"], None),
        ("SUBTOTAL MONT.", "TOTAL REPLANTEO, TRANSPORTE Y MONTAJE (PARTIDA 03)", "4 conjuntos", "=SUM(E13:E15)", mon["venta_total"]),
    ]

    r = 6
    for idx, (blk, desc, base_txt, cd, pv) in enumerate(rows_esc):
        ws2.cell(row=r, column=2, value=blk)
        ws2.cell(row=r, column=3, value=desc)
        ws2.cell(row=r, column=4, value=base_txt).alignment = Alignment(horizontal="right")
        c_cd = ws2.cell(row=r, column=5, value=cd)
        c_cd.number_format = NUM_EUR
        if pv is not None:
            c_pv = ws2.cell(row=r, column=6, value=pv)
            c_pv.number_format = NUM_EUR
            c_mg = ws2.cell(row=r, column=7, value=f"=F{r}-E{r}")
            c_mg.number_format = NUM_EUR
            c_pct = ws2.cell(row=r, column=8, value=f"=G{r}/F{r}")
            c_pct.number_format = NUM_PCT
        for col in range(2, 9):
            c = ws2.cell(row=r, column=col)
            c.border = b_thin
            if pv is not None:
                c.fill = f_hl
                c.font = fn_bold
            else:
                c.font = fn_reg
                if idx % 2 == 1:
                    c.fill = f_alt
        ws2.row_dimensions[r].height = 22
        r += 1

    # Total consolidado
    ws2.cell(row=r, column=2, value="TOTAL GLOBAL")
    ws2.cell(row=r, column=3, value="CONSOLIDADO P-2026-0059 (OPCIÓN BASE LLAVE EN MANO)")
    ws2.cell(row=r, column=4, value="4 cancelas / 262,5 kg")
    ws2.cell(row=r, column=5, value="=E12+E16").number_format = NUM_EUR
    ws2.cell(row=r, column=6, value="=F12+F16").number_format = NUM_EUR
    ws2.cell(row=r, column=7, value=f"=F{r}-E{r}").number_format = NUM_EUR
    ws2.cell(row=r, column=8, value=f"=G{r}/F{r}").number_format = NUM_PCT
    for col in range(2, 9):
        c = ws2.cell(row=r, column=col)
        c.font = fn_tot
        c.fill = f_tot
        c.border = b_tot
    ws2.row_dimensions[r].height = 26

    for col, w in [(1, 3), (2, 16), (3, 56), (4, 22), (5, 16), (6, 16), (7, 15), (8, 13)]:
        ws2.column_dimensions[get_column_letter(col)].width = w

    xlsx_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0059_Cancelas_Alaior_Granian.xlsx")
    wb.save(xlsx_path)
    print("Excel generado:", xlsx_path)


def build_cliente_html():
    t = DATA["totales"]
    esp = DATA["especificaciones_tecnicas"]
    opt = DATA["opcionales"][0]

    rows_partidas = ""
    for p in DATA["partidas"]:
        rows_partidas += f"""
        <tr>
          <td><strong>{p['codigo']}</strong></td>
          <td><strong>{p['concepto']}</strong><br><span class="desc">{p['descripcion']}</span></td>
          <td class="cen"><strong>{p['dimensiones']}</strong><br><span class="desc">{p['hojas']}</span></td>
          <td class="num">{fmt_num(p['cantidad'], 0)} {p['unidad']}</td>
          <td class="num">{fmt_eur(p['precio_unitario'])}</td>
          <td class="num"><strong>{fmt_eur(p['subtotal'])}</strong></td>
        </tr>"""

    excl_li = "".join(f"<li>{e}</li>" for e in DATA["exclusiones"])

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{DATA['codigo']} · Presupuesto Cancelas Abatibles · Inversiones Granian SL</title>
  <style>
    @page {{ size: A4 portrait; margin: 6mm; }}
    * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    body {{ margin: 0; background: #e2e8f0; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 8.6px; line-height: 1.32; }}
    .sheet {{ width: 210mm; margin: 10px auto; background: #fff; padding: 7mm 9mm; box-shadow: 0 10px 30px rgba(15,23,42,.12); }}
    header {{ background: #0f172a; color: #fff; padding: 9px 14px; border-radius: 7px; border-bottom: 3px solid #0284c7; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
    .brand {{ display: flex; align-items: center; gap: 10px; }}
    .logo {{ width: 38px; height: 38px; background: rgba(255,255,255,.1); border-radius: 5px; padding: 4px; filter: brightness(0) invert(1); }}
    h1 {{ margin: 0; font-size: 13.5px; font-weight: 700; color: #fff; }}
    .subtitle {{ font-size: 9px; color: #94a3b8; margin-top: 2px; }}
    .meta {{ text-align: right; font-size: 8.5px; color: #cbd5e1; }}
    .meta strong {{ display: block; color: #38bdf8; font-size: 10.5px; margin-bottom: 2px; }}
    .summary-card {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 9px 12px; margin-bottom: 8px; display: grid; grid-template-columns: 1.45fr 1fr; gap: 12px; align-items: center; }}
    .summary-card p {{ margin: 3px 0 0; color: #334155; font-size: 8.4px; }}
    .price-box {{ border-left: 2px solid #cbd5e1; padding-left: 12px; text-align: right; }}
    .price-tag {{ font-size: 7.8px; text-transform: uppercase; letter-spacing: .5px; color: #64748b; font-weight: 700; }}
    .main-price {{ font-size: 19px; font-weight: 800; color: #0284c7; margin: 2px 0; }}
    .sub-price {{ font-size: 8.5px; color: #0f172a; }}
    h2 {{ font-size: 10px; text-transform: uppercase; letter-spacing: .4px; color: #0f172a; border-bottom: 2px solid #cbd5e1; padding-bottom: 3px; margin: 8px 0 5px; display: flex; justify-content: space-between; align-items: center; }}
    .badge {{ background: #e0f2fe; color: #0369a1; font-size: 8px; padding: 2px 7px; border-radius: 10px; font-weight: 700; text-transform: none; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 7px; }}
    th {{ background: #f1f5f9; color: #334155; font-size: 7.8px; text-transform: uppercase; padding: 4px 6px; border-bottom: 1.5px solid #cbd5e1; text-align: left; }}
    td {{ padding: 4.5px 6px; border-bottom: 1px solid #e2e8f0; vertical-align: top; font-size: 8.2px; }}
    tr:nth-child(even) td {{ background: #fafafa; }}
    .desc {{ font-size: 7.4px; color: #475569; line-height: 1.24; }}
    .num {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
    .cen {{ text-align: center; font-size: 7.9px; }}
    .sub-row td {{ background: #e0f2fe !important; font-weight: 700; color: #0369a1; }}
    .grand-total td {{ background: #0f172a !important; color: #ffffff !important; padding: 6px 10px; }}
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; margin-top: 6px; }}
    .box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 9px; }}
    .box h3 {{ margin: 0 0 3px; font-size: 8.7px; color: #0369a1; text-transform: uppercase; }}
    .box ul {{ margin: 0; padding-left: 13px; font-size: 7.8px; color: #334155; }}
    .box li {{ margin-bottom: 2px; }}
    .opt-box {{ background: #fffbeb; border: 1px solid #fcd34d; border-radius: 5px; padding: 6px 9px; margin-top: 6px; font-size: 8px; }}
    .plazo-box {{ background: #ecfdf5; border: 1px solid #6ee7b7; border-radius: 5px; padding: 6px 9px; margin-top: 6px; font-size: 8.1px; color: #065f46; }}
    footer {{ margin-top: 8px; padding-top: 5px; border-top: 1px solid #e2e8f0; font-size: 7.5px; color: #64748b; display: flex; justify-content: space-between; }}
    @media print {{ body {{ background: #fff; }} .sheet {{ box-shadow: none; margin: 0; width: 100%; padding: 4mm 6mm; }} }}
  </style>
</head>
<body>
  <div class="sheet">
    <header>
      <div class="brand">
        <img class="logo" src="logo-ham.svg" alt="HAM">
        <div>
          <h1>HAM ESTRUCTURAS METÁLICAS MENORCA</h1>
          <div class="subtitle">Dixis Recursos y Soluciones S.L. (CIF {DATA['emisor']['cif']}) · Herrería, Cancelas y Estructuras a Medida</div>
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
        <strong style="color:#0369a1; font-size:10px;">{DATA['cliente']['proyecto']}</strong>
        <p><strong>Cliente:</strong> {DATA['cliente']['nombre']} (Att. {DATA['cliente']['contacto']})<br>
        <strong>Ubicación:</strong> {DATA['cliente']['ubicacion']}<br>
        <strong>Referencia:</strong> {DATA['cliente']['referencia_solicitud']}</p>
      </div>
      <div class="price-box">
        <div class="price-tag">Total Llave en Mano (Opción Base C4)</div>
        <div class="main-price">{fmt_eur(t['base_imponible'])}</div>
        <div class="sub-price">IVA 21%: {fmt_eur(t['iva_importe'])} · <strong>Total: {fmt_eur(t['total_presupuesto'])}</strong></div>
        <div style="font-size:7.6px; color:#475569; margin-top:2px;">Solo suministro en taller (sin montaje): <strong>{fmt_eur(t['subtotal_solo_suministro'])}</strong> + IVA</div>
      </div>
    </div>

    <h2>Desglose de Partidas · Fabricación, Acabado Anticorrosivo C4 e Instalación <span class="badge">4 Conjuntos · 8 Hojas · 13,50 ml totales</span></h2>
    <table>
      <thead>
        <tr>
          <th style="width:6%;">Cód.</th>
          <th style="width:50%;">Descripción Técnica del Suministro y Montaje</th>
          <th style="width:16%; text-align:center;">Medidas / Hojas</th>
          <th style="width:7%; text-align:right;">Cant.</th>
          <th style="width:10%; text-align:right;">Precio Ud.</th>
          <th style="width:11%; text-align:right;">Subtotal</th>
        </tr>
      </thead>
      <tbody>
        {rows_partidas}
        <tr class="sub-row">
          <td colspan="4"><strong>SUBTOTAL SOLO SUMINISTRO DE LAS 4 CANCELAS FABRICADAS Y PINTADAS EN C4 (PARTIDAS 01 + 02)</strong></td>
          <td class="num">-</td>
          <td class="num"><strong>{fmt_eur(t['subtotal_solo_suministro'])}</strong></td>
        </tr>
        <tr class="grand-total">
          <td colspan="4" style="font-size:9.5px;"><strong>BASE IMPONIBLE TOTAL — FABRICACIÓN, TRANSPORTE E INSTALACIÓN EN ALAIOR (01 + 02 + 03)</strong></td>
          <td class="num">-</td>
          <td class="num" style="font-size:11px;"><strong>{fmt_eur(t['base_imponible'])}</strong></td>
        </tr>
        <tr>
          <td colspan="4" style="padding:4px 6px;">I.V.A. General (21,00%)</td>
          <td class="num">-</td>
          <td class="num" style="padding:4px 6px;">{fmt_eur(t['iva_importe'])}</td>
        </tr>
        <tr style="background:#e0f2fe; color:#0369a1;">
          <td colspan="4" style="padding:5px 6px; font-size:9.8px;"><strong>TOTAL PRESUPUESTO LLAVE EN MANO (I.V.A. INCLUIDO)</strong></td>
          <td class="num">-</td>
          <td class="num" style="padding:5px 6px; font-size:11.5px;"><strong>{fmt_eur(t['total_presupuesto'])}</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="plazo-box">
      <strong>Plazo de Entrega Estimado:</strong> <strong>3 a 4 semanas</strong> desde la aceptación del presupuesto y la toma de medidas reales (replanteo) entre pilares en la finca de Alaior (+ <strong>2 jornadas</strong> de montaje en obra).<br>
      <em>En caso de optar por la Alternativa B (Galvanizado en Caliente), el plazo total es de <strong>5 a 6 semanas</strong> debido al transporte marítimo y turno en planta galvanizadora.</em>
    </div>

    <div class="opt-box">
      <strong>Alternativa Opcional de Máxima Durabilidad ({opt['codigo']}):</strong> {opt['concepto']}. {opt['descripcion']}
      <strong>Suplemento: +{fmt_eur(opt['subtotal'])} + IVA</strong> (Total Base Imponible con Galvanizado: <strong>{fmt_eur(t['base_imponible_con_galvanizado'])}</strong> + IVA = <strong>{fmt_eur(t['total_con_galvanizado'])}</strong>).
    </div>

    <div class="grid-2">
      <div class="box">
        <h3>Especificaciones Constructivas y Tratamiento C4 Menorca</h3>
        <ul>
          <li><strong>Diseño fiel a referencia:</strong> {esp['diseno']}</li>
          <li><strong>Perfilería:</strong> Bastidor en {esp['bastidor'].replace('Tubo', 'tubo')} Relleno: {esp['barrotes']}</li>
          <li><strong>Herrajes y anclajes:</strong> {esp['herrajes']} {esp['fijacion']}</li>
          <li><strong>Acabado C4 (no horno):</strong> {DATA['condiciones']['acabado_ham']}</li>
        </ul>
      </div>
      <div class="box">
        <h3>Condiciones Comerciales y Exclusiones</h3>
        <ul>
          <li><strong>Validez y pago:</strong> {DATA['condiciones']['validez']}. Forma de pago: {DATA['condiciones']['forma_pago']}.</li>
          {excl_li}
        </ul>
      </div>
    </div>

    <footer>
      <div>{DATA['emisor']['nombre_comercial']} · {DATA['emisor']['direccion']} · {DATA['emisor']['telefono']} · WhatsApp {DATA['emisor']['movil']} · {DATA['emisor']['email']}</div>
      <div style="white-space:nowrap;">Página 1 de 1</div>
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
    esp = DATA["especificaciones_tecnicas"]
    esc = DATA["escandallo_interno"]
    fab = esc["fabricacion_y_tratamiento"]
    mon = esc["replanteo_transporte_montaje"]
    eg = esc["resumen_global"]

    riesgos_li = "".join(f"<li>{r}</li>" for r in DATA["riesgos_internos"])

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{DATA['codigo']} · Estudio Técnico Interno y Escandallo · Granian Alaior</title>
  <style>
    @page {{ size: A4 portrait; margin: 7mm; }}
    * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    body {{ margin: 0; background: #e2e8f0; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 8.7px; line-height: 1.34; }}
    .sheet {{ width: 210mm; margin: 10px auto; background: #fff; padding: 8mm 10mm; box-shadow: 0 10px 30px rgba(15,23,42,.12); }}
    header {{ background: #1e293b; color: #fff; padding: 9px 14px; border-radius: 7px; border-bottom: 3px solid #d97706; display: flex; justify-content: space-between; align-items: center; margin-bottom: 9px; }}
    h1 {{ margin: 0; font-size: 13px; color: #fff; }}
    .sub {{ font-size: 8.8px; color: #cbd5e1; margin-top: 2px; }}
    .tag {{ background: #b45309; color: #fff; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 8.3px; }}
    h2 {{ font-size: 9.8px; text-transform: uppercase; color: #0f172a; border-bottom: 2px solid #cbd5e1; padding-bottom: 3px; margin: 9px 0 5px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 7px; }}
    th {{ background: #f1f5f9; color: #334155; font-size: 7.8px; text-transform: uppercase; padding: 4.5px 6px; border-bottom: 1.5px solid #cbd5e1; text-align: left; }}
    td {{ padding: 4px 6px; border-bottom: 1px solid #e2e8f0; font-size: 8.2px; vertical-align: top; }}
    .num {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
    .subrow td {{ background: #eff6ff; font-weight: 700; color: #1e40af; }}
    .tot td {{ background: #fef3c7; font-weight: 700; border-top: 1.5px solid #d97706; border-bottom: 1.5px solid #d97706; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 9px; }}
    .kpi {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px 9px; }}
    .kpi span {{ display: block; font-size: 7.4px; text-transform: uppercase; color: #64748b; font-weight: 700; }}
    .kpi strong {{ font-size: 12.5px; color: #0f172a; }}
    .alert {{ background: #fff7ed; border-left: 4px solid #ea580c; padding: 6px 9px; margin-bottom: 7px; font-size: 8.1px; }}
    .box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 9px; margin-bottom: 7px; font-size: 8.1px; }}
    ul {{ margin: 3px 0 0; padding-left: 14px; font-size: 8px; }}
    li {{ margin-bottom: 2px; }}
    footer {{ margin-top: 8px; padding-top: 5px; border-top: 1px solid #e2e8f0; font-size: 7.6px; color: #64748b; display: flex; justify-content: space-between; }}
    @media print {{ body {{ background: #fff; }} .sheet {{ box-shadow: none; margin: 0; width: 100%; padding: 5mm 7mm; }} }}
  </style>
</head>
<body>
  <div class="sheet">
    <header>
      <div>
        <h1>ESTUDIO TÉCNICO INTERNO Y ESCANDALLO · {DATA['codigo']}</h1>
        <div class="sub">Inversiones Granian S.L. (Belén González) · Finca en Alaior · Uso confidencial HAM / DIXIS</div>
      </div>
      <div class="tag">USO INTERNO</div>
    </header>

    <div class="kpi-grid">
      <div class="kpi"><span>Coste Directo Total</span><strong>{fmt_eur(eg['coste_directo_total'])}</strong></div>
      <div class="kpi"><span>Venta Neta (Llave en Mano)</span><strong>{fmt_eur(eg['venta_total'])}</strong></div>
      <div class="kpi"><span>Margen Bruto (€)</span><strong style="color:#15803d;">{fmt_eur(eg['margen_bruto_total'])}</strong></div>
      <div class="kpi"><span>Margen Bruto (% s/Venta)</span><strong style="color:#15803d;">{fmt_num(eg['margen_bruto_porcentaje'])}%</strong></div>
    </div>

    <h2>1. Cubicaje de Materiales y Pesos Estimados (4 Cancelas / 8 Hojas Abatibles)</h2>
    <table>
      <thead>
        <tr>
          <th>Modelo</th>
          <th>Medidas (Alto × Ancho)</th>
          <th style="text-align:right;">Uds.</th>
          <th style="text-align:right;">Tubo 40×40×2</th>
          <th style="text-align:right;">Tubo 20×20×2</th>
          <th style="text-align:right;">Herrajes</th>
          <th style="text-align:right;">Peso Neto</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>C1</strong></td>
          <td>130 × 360 cm (2 hojas 180 cm)</td>
          <td class="num">1</td>
          <td class="num">15,50 ml (36,4 kg)</td>
          <td class="num">25,30 ml (28,8 kg)</td>
          <td class="num">6,8 kg</td>
          <td class="num"><strong>72,0 kg</strong></td>
        </tr>
        <tr>
          <td><strong>C2</strong></td>
          <td>120 × 330 cm (2 hojas 165 cm)</td>
          <td class="num">3</td>
          <td class="num">42,48 ml (99,8 kg)</td>
          <td class="num">63,00 ml (71,8 kg)</td>
          <td class="num">18,9 kg</td>
          <td class="num"><strong>190,5 kg</strong></td>
        </tr>
        <tr class="subrow">
          <td colspan="2">TOTAL NETO (Con 5% merma de compra: {fmt_num(esp['peso_compra_con_merma_kg'], 1)} kg)</td>
          <td class="num">4</td>
          <td class="num">57,98 ml (136,2 kg)</td>
          <td class="num">88,30 ml (100,6 kg)</td>
          <td class="num">25,7 kg</td>
          <td class="num"><strong>{fmt_num(esp['peso_neto_total_kg'], 1)} kg</strong></td>
        </tr>
      </tbody>
    </table>

    <h2>2. Escandallo Detallado de Costes Directos y Márgenes</h2>
    <table>
      <thead>
        <tr>
          <th style="width:16%;">Bloque</th>
          <th style="width:44%;">Concepto de Coste e Hipótesis</th>
          <th style="width:14%; text-align:right;">Base / Horas</th>
          <th style="width:13%; text-align:right;">Coste Directo</th>
          <th style="width:13%; text-align:right;">Venta / Margen</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Materiales</td><td>Acero tubular S235JR puesto Menorca (incl. 5% merma)</td><td class="num">276 kg × 1,85 €</td><td class="num">{fmt_eur(fab['coste_acero_material'])}</td><td class="num">-</td></tr>
        <tr><td>Herrajes</td><td>16 bisagras regulables (288 €) + 4 pasadores portacandado (88 €) + 4 fallebas/topes (100 €)</td><td class="num">Lote 4 uds</td><td class="num">{fmt_eur(fab['coste_herrajes_bisagras_pasadores'])}</td><td class="num">-</td></tr>
        <tr><td>Fijación/Cons.</td><td>Taco químico + 64 varillas inox A4 (140 €) + consumibles MIG/corte (95 €)</td><td class="num">Lote</td><td class="num">{fmt_eur(fab['coste_anclajes_a4_quimico_consumibles'])}</td><td class="num">-</td></tr>
        <tr><td>Oficina Técn.</td><td>Despiece y plantillas de remate inclinado a dos aguas</td><td class="num">4,0 h × 35,00 €</td><td class="num">{fmt_eur(fab['coste_oficina_tecnica'])}</td><td class="num">-</td></tr>
        <tr><td>MO Taller</td><td>Corte, soldadura continua sellada, herrajes (9,5 h C1 + 22,5 h 3×C2)</td><td class="num">32,0 h × 35,00 €</td><td class="num">{fmt_eur(fab['coste_mo_taller'])}</td><td class="num">-</td></tr>
        <tr><td>Tratam. C4</td><td>Material epoxi fosfato zinc + poliuretano 2C (240 €) + cabina/pintura (16 h × 30 €)</td><td class="num">~24 m² / 16 h</td><td class="num">{fmt_eur(fab['coste_tratamiento_c4_total'])}</td><td class="num">-</td></tr>
        <tr class="subrow">
          <td colspan="3">SUBTOTAL FABRICACIÓN + TRATAMIENTO C4 (PARTIDAS 01 + 02)</td>
          <td class="num">{fmt_eur(fab['coste_directo_total'])}</td>
          <td class="num">{fmt_eur(fab['venta_total'])} ({fmt_num(fab['margen_porcentaje'])}%)</td>
        </tr>
        <tr><td>Replanteo</td><td>Visita previa a finca en Alaior para medir pilares, aplomados y rasantes</td><td class="num">2,0 h × 35,00 €</td><td class="num">{fmt_eur(mon['coste_replanteo'])}</td><td class="num">-</td></tr>
        <tr><td>Logística</td><td>Furgón/camión Sant Lluís–Alaior + grupo electrógeno autónomo</td><td class="num">Lote obra</td><td class="num">{fmt_eur(mon['coste_transporte_furgon_generador'])}</td><td class="num">-</td></tr>
        <tr><td>MO Montaje</td><td>2 operarios × 2 jornadas completas (taladrado pilares, químico A4, nivelado, retoques)</td><td class="num">32,0 h × 35,00 €</td><td class="num">{fmt_eur(mon['coste_mo_montaje'])}</td><td class="num">-</td></tr>
        <tr class="subrow">
          <td colspan="3">SUBTOTAL REPLANTEO, TRANSPORTE Y MONTAJE (PARTIDA 03)</td>
          <td class="num">{fmt_eur(mon['coste_directo_total'])}</td>
          <td class="num">{fmt_eur(mon['venta_total'])} ({fmt_num(mon['margen_porcentaje'])}%)</td>
        </tr>
        <tr class="tot">
          <td colspan="3"><strong>TOTAL CONSOLIDADO OPCIÓN BASE C4 (LLAVE EN MANO)</strong></td>
          <td class="num">{fmt_eur(eg['coste_directo_total'])}</td>
          <td class="num">{fmt_eur(eg['venta_total'])} ({fmt_num(eg['margen_bruto_porcentaje'])}%)</td>
        </tr>
      </tbody>
    </table>

    <div class="alert">
      <strong>Nota sobre Alternativa B (Galvanizado en Caliente OPC-GALV = +1.340,00 € venta):</strong>
      Coste estimado porte marítimo i/v Menorca–Barcelona (~360 €) + galvanizado inmersión ~270 kg (~380 €) + preparación/wash-primer sobre zinc y PU 2C (~190 € suplemento) = <strong>~930 € coste directo</strong> → Margen ~410 € (~30,6%).
    </div>

    <div class="box">
      <strong>Riesgos Técnicos y Puntos a Validar en Replanteo de Obra (Alaior):</strong>
      <ul>
        {riesgos_li}
        <li><strong>Referencia comercial (FACTUSOL / Política HAM):</strong> Precio resultante ~400 €/m² instalado (490 €/ml) para cancelas tubulares a medida con barrotes y sistema C4 Menorca, alineado con el margen comercial objetivo de puertas metálicas (30–40%).</li>
      </ul>
    </div>

    <footer>
      <div>Documento interno confidencial · {DATA['emisor']['nombre_comercial']}</div>
      <div style="white-space:nowrap;">Página 1 de 1</div>
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
