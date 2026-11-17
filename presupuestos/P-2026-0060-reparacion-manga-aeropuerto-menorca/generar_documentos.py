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
    if val is None:
        return "0,00 €"
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def create_excel():
    wb = Workbook()
    ws_cli = wb.active
    ws_cli.title = "Presupuesto Cliente"
    ws_int = wb.create_sheet(title="Estudio Interno y Márgenes")
    ws_mat = wb.create_sheet(title="Desglose Costes Directos")

    NAVY = "0F172A"
    GOLD = "B45309"
    LIGHT_BG = "F8FAFC"
    SUB_BG = "E2E8F0"
    TOTAL_BG = "FEF3C7"
    GREEN_TXT = "15803D"

    fill_navy = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUB_BG, end_color=SUB_BG, fill_type="solid")
    fill_alt = PatternFill(start_color=LIGHT_BG, end_color=LIGHT_BG, fill_type="solid")
    fill_total = PatternFill(start_color=TOTAL_BG, end_color=TOTAL_BG, fill_type="solid")

    font_title = Font(name="Segoe UI", size=13.5, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_head = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_regular = Font(name="Segoe UI", size=8.8, color="1E293B")
    font_total = Font(name="Segoe UI", size=10.5, bold=True, color=NAVY)
    font_total_gold = Font(name="Segoe UI", size=11, bold=True, color=GOLD)
    font_green = Font(name="Segoe UI", size=9.5, bold=True, color=GREEN_TXT)

    border_thin = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1")
    )
    border_double = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="double", color=NAVY)
    )

    # ==========================================
    # SHEET 1: PRESUPUESTO CLIENTE (1 CONCEPTO)
    # ==========================================
    ws_cli.views.sheetView[0].showGridLines = True
    ws_cli.merge_cells("A1:F1")
    ws_cli["A1"] = f"{DATA['emisor']['nombre_comercial']} — {DATA['emisor']['razon_social']}"
    ws_cli["A1"].font = font_title

    ws_cli.merge_cells("A2:F2")
    ws_cli["A2"] = f"PRESUPUESTO TÉCNICO-COMERCIAL · Ref: {DATA['codigo']} ({DATA['referencia']})"
    ws_cli["A2"].font = font_sub

    ws_cli.cell(row=4, column=1, value="CLIENTE:").font = font_bold
    ws_cli.cell(row=4, column=2, value=f"{DATA['cliente']['empresa']} (NIF: {DATA['cliente']['cif']})").font = font_regular
    ws_cli.cell(row=4, column=5, value="FECHA:").font = font_bold
    ws_cli.cell(row=4, column=6, value=DATA["fecha"]).font = font_regular

    ws_cli.cell(row=5, column=1, value="DOMICILIO CLIENTE:").font = font_bold
    ws_cli.cell(row=5, column=2, value=f"{DATA['cliente']['domicilio']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']} · {DATA['cliente']['email']}").font = font_regular
    ws_cli.cell(row=5, column=5, value="VALIDEZ:").font = font_bold
    ws_cli.cell(row=5, column=6, value=f"{DATA['validez_dias']} días").font = font_regular

    ws_cli.cell(row=6, column=1, value="CONDICIONES OPERATIVAS:").font = font_bold
    ws_cli.merge_cells("B6:F6")
    ws_cli["B6"] = "Plataforma elevadora (PEMP) prestada por el cliente · Permisos y acreditaciones de seguridad ZRS por cuenta del cliente"
    ws_cli["B6"].font = font_regular

    # Table Header
    headers_cli = ["Cód.", "Concepto / Descripción del Trabajo Realizado", "Ud.", "Cant.", "Precio Unitario", "Subtotal (€)"]
    start_row = 8
    for col_idx, h in enumerate(headers_cli, start=1):
        cell = ws_cli.cell(row=start_row, column=col_idx, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 3] else ("right" if col_idx >= 4 else "left"), vertical="center")
        cell.border = border_thin

    # Single Partida Row
    p = DATA["partidas_cliente"][0]
    row_p = start_row + 1
    ws_cli.cell(row=row_p, column=1, value=p["codigo"]).font = font_bold
    ws_cli.cell(row=row_p, column=1).alignment = Alignment(horizontal="center", vertical="top")
    ws_cli.cell(row=row_p, column=1).border = border_thin

    ws_cli.cell(row=row_p, column=2, value=f"{p['concepto']}\n\n{p['descripcion']}").font = font_regular
    ws_cli.cell(row=row_p, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws_cli.cell(row=row_p, column=2).border = border_thin

    ws_cli.cell(row=row_p, column=3, value=p["unidad"]).font = font_regular
    ws_cli.cell(row=row_p, column=3).alignment = Alignment(horizontal="center", vertical="top")
    ws_cli.cell(row=row_p, column=3).border = border_thin

    ws_cli.cell(row=row_p, column=4, value=p["cantidad"]).font = font_regular
    ws_cli.cell(row=row_p, column=4).alignment = Alignment(horizontal="right", vertical="top")
    ws_cli.cell(row=row_p, column=4).border = border_thin

    c_unit = ws_cli.cell(row=row_p, column=5, value=p["precio_venta_unitario"])
    c_unit.font = font_regular
    c_unit.number_format = "#,##0.00 €"
    c_unit.alignment = Alignment(horizontal="right", vertical="top")
    c_unit.border = border_thin

    c_sub = ws_cli.cell(row=row_p, column=6, value=f"=D{row_p}*E{row_p}")
    c_sub.font = font_bold
    c_sub.number_format = "#,##0.00 €"
    c_sub.alignment = Alignment(horizontal="right", vertical="top")
    c_sub.border = border_thin

    current_row = row_p + 2
    # Totals
    ws_cli.cell(row=current_row, column=4, value="BASE IMPONIBLE:").font = font_sec
    c_base = ws_cli.cell(row=current_row, column=6, value=f"=F{row_p}")
    c_base.font = font_total
    c_base.number_format = "#,##0.00 €"
    c_base.fill = fill_total
    c_base.border = border_thin
    base_row = current_row

    current_row += 1
    ws_cli.cell(row=current_row, column=4, value=f"I.V.A. ({DATA['resumen_economico']['tipo_iva_pct']:.0f}%):").font = font_regular
    c_iva = ws_cli.cell(row=current_row, column=6, value=f"=ROUND(F{base_row}*{DATA['resumen_economico']['tipo_iva_pct']/100}, 2)")
    c_iva.font = font_regular
    c_iva.number_format = "#,##0.00 €"
    c_iva.border = border_thin
    iva_row = current_row

    current_row += 1
    ws_cli.cell(row=current_row, column=4, value="TOTAL PRESUPUESTO:").font = font_total_gold
    c_tot = ws_cli.cell(row=current_row, column=6, value=f"=F{base_row}+F{iva_row}")
    c_tot.font = font_total_gold
    c_tot.number_format = "#,##0.00 €"
    c_tot.fill = fill_total
    c_tot.border = border_double

    # Conditions
    current_row += 2
    ws_cli.cell(row=current_row, column=1, value="CONDICIONES Y OBSERVACIONES:").font = font_sec
    current_row += 1
    for cond in DATA["condiciones_generales"]:
        ws_cli.cell(row=current_row, column=1, value="•").alignment = Alignment(horizontal="center")
        ws_cli.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=6)
        ws_cli.cell(row=current_row, column=2, value=cond).font = font_regular
        current_row += 1

    # Column widths
    ws_cli.column_dimensions["A"].width = 9
    ws_cli.column_dimensions["B"].width = 72
    ws_cli.column_dimensions["C"].width = 8
    ws_cli.column_dimensions["D"].width = 8
    ws_cli.column_dimensions["E"].width = 16
    ws_cli.column_dimensions["F"].width = 18

    # ==========================================
    # SHEET 2: ESTUDIO INTERNO Y MÁRGENES
    # ==========================================
    ws_int.views.sheetView[0].showGridLines = True
    ws_int.merge_cells("A1:G1")
    ws_int["A1"] = f"ESTUDIO TÉCNICO DE COSTES Y MÁRGENES — {DATA['codigo']}"
    ws_int["A1"].font = font_title

    ws_int.cell(row=3, column=1, value="Concepto").font = font_head
    ws_int.cell(row=3, column=1).fill = fill_navy
    ws_int.cell(row=3, column=2, value="Coste Directo (€)").font = font_head
    ws_int.cell(row=3, column=2).fill = fill_navy
    ws_int.cell(row=3, column=3, value="Precio Venta (€)").font = font_head
    ws_int.cell(row=3, column=3).fill = fill_navy
    ws_int.cell(row=3, column=4, value="Beneficio (€)").font = font_head
    ws_int.cell(row=3, column=4).fill = fill_navy
    ws_int.cell(row=3, column=5, value="Margen / Venta (%)").font = font_head
    ws_int.cell(row=3, column=5).fill = fill_navy
    ws_int.cell(row=3, column=6, value="Margen / Coste (%)").font = font_head
    ws_int.cell(row=3, column=6).fill = fill_navy

    re = DATA["resumen_economico"]
    r_int = 4
    ws_int.cell(row=r_int, column=1, value=f"{p['codigo']} - {p['concepto'][:60]}...").font = font_regular
    ws_int.cell(row=r_int, column=2, value=re["coste_directo_total"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=3, value=re["venta_base_imponible"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=4, value=re["beneficio_bruto"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=5, value=re["margen_sobre_venta_pct"] / 100).number_format = "0.0%"
    ws_int.cell(row=r_int, column=6, value=re["margen_sobre_coste_pct"] / 100).number_format = "0.0%"
    for c in range(1, 7):
        ws_int.cell(row=r_int, column=c).border = border_thin

    r_int += 1
    ws_int.cell(row=r_int, column=1, value="TOTALES").font = font_total
    ws_int.cell(row=r_int, column=2, value=re["coste_directo_total"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=3, value=re["venta_base_imponible"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=4, value=re["beneficio_bruto"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=5, value=re["margen_sobre_venta_pct"] / 100).number_format = "0.0%"
    ws_int.cell(row=r_int, column=6, value=re["margen_sobre_coste_pct"] / 100).number_format = "0.0%"
    for c in range(1, 7):
        ws_int.cell(row=r_int, column=c).font = font_total
        ws_int.cell(row=r_int, column=c).fill = fill_total
        ws_int.cell(row=r_int, column=c).border = border_double

    # Breakdown by nature
    r_int += 3
    ws_int.cell(row=r_int, column=1, value="RESUMEN POR NATURALEZA DE RECURSOS").font = font_sec
    r_int += 1
    nature = [
        ("Materiales e Insumos (acero, consumibles, pintura C5)", re["coste_materiales"]),
        ("Mano de Obra Especializada (Taller + Obra en Pista 2 oficiales)", re["coste_mano_obra"]),
        ("Plataforma Elevadora PEMP (prestada por cliente)", 0.0),
        ("Tramitaciones de Permisos AENA (por cuenta del cliente)", 0.0),
        ("Desplazamientos furgón taller (2 días)", re["coste_medios_y_transporte"]),
        ("COSTE DIRECTO TOTAL", re["coste_directo_total"]),
        ("PRECIO VENTA OFERTADO (BASE IMPONIBLE 1 x 3.952,12 €)", re["venta_base_imponible"]),
        ("BENEFICIO BRUTO ESTIMADO", re["beneficio_bruto"])
    ]
    for lbl, val in nature:
        ws_int.cell(row=r_int, column=1, value=lbl).font = font_bold if "TOTAL" in lbl or "PRECIO" in lbl else font_regular
        c_val = ws_int.cell(row=r_int, column=2, value=val)
        c_val.font = font_bold if "TOTAL" in lbl or "PRECIO" in lbl else font_regular
        c_val.number_format = "#,##0.00 €"
        if "BENEFICIO" in lbl:
            c_val.font = font_green
        r_int += 1

    ws_int.column_dimensions["A"].width = 55
    ws_int.column_dimensions["B"].width = 18
    ws_int.column_dimensions["C"].width = 18
    ws_int.column_dimensions["D"].width = 18
    ws_int.column_dimensions["E"].width = 18
    ws_int.column_dimensions["F"].width = 18

    # ==========================================
    # SHEET 3: DESGLOSE COSTES DIRECTOS
    # ==========================================
    ws_mat.views.sheetView[0].showGridLines = True
    ws_mat.merge_cells("A1:E1")
    ws_mat["A1"] = f"DESGLOSE DE RECURSOS DIRECTOS — {DATA['codigo']}"
    ws_mat["A1"].font = font_title

    r_mat = 3
    ws_mat.cell(row=r_mat, column=1, value="1. Materiales, Acero y Consumibles").font = font_sec
    r_mat += 1
    m_heads = ["Concepto", "Unidad", "Cantidad", "Coste Ud. (€)", "Subtotal (€)"]
    for i, h in enumerate(m_heads, start=1):
        cell = ws_mat.cell(row=r_mat, column=i, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.border = border_thin
    r_mat += 1
    for m in DATA["desglose_costes_internos"]["materiales"]:
        ws_mat.cell(row=r_mat, column=1, value=m["concepto"]).font = font_regular
        ws_mat.cell(row=r_mat, column=2, value=m["unidad"]).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=r_mat, column=3, value=m["cantidad"]).alignment = Alignment(horizontal="right")
        ws_mat.cell(row=r_mat, column=4, value=m["coste_unit"]).number_format = "#,##0.00 €"
        ws_mat.cell(row=r_mat, column=5, value=m["total"]).number_format = "#,##0.00 €"
        for i in range(1, 6):
            ws_mat.cell(row=r_mat, column=i).border = border_thin
        r_mat += 1

    r_mat += 2
    ws_mat.cell(row=r_mat, column=1, value="2. Mano de Obra y Supervisión Técnica").font = font_sec
    r_mat += 1
    mo_heads = ["Puesto / Tarea", "Horas", "Tarifa (€/h)", "Subtotal (€)"]
    for i, h in enumerate(mo_heads, start=1):
        cell = ws_mat.cell(row=r_mat, column=i, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.border = border_thin
    r_mat += 1
    for mo in DATA["desglose_costes_internos"]["mano_de_obra"]:
        ws_mat.cell(row=r_mat, column=1, value=mo["concepto"]).font = font_regular
        ws_mat.cell(row=r_mat, column=2, value=mo["horas"]).alignment = Alignment(horizontal="right")
        ws_mat.cell(row=r_mat, column=3, value=mo["tarifa"]).number_format = "#,##0.00 €"
        ws_mat.cell(row=r_mat, column=4, value=mo["total"]).number_format = "#,##0.00 €"
        for i in range(1, 5):
            ws_mat.cell(row=r_mat, column=i).border = border_thin
        r_mat += 1

    r_mat += 2
    ws_mat.cell(row=r_mat, column=1, value="3. Medios y Logística").font = font_sec
    r_mat += 1
    for i, h in enumerate(["Concepto", "Días", "Coste Ud. (€)", "Subtotal (€)"], start=1):
        cell = ws_mat.cell(row=r_mat, column=i, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.border = border_thin
    r_mat += 1
    for med in DATA["desglose_costes_internos"]["medios_auxiliares_y_transporte"]:
        ws_mat.cell(row=r_mat, column=1, value=med["concepto"]).font = font_regular
        ws_mat.cell(row=r_mat, column=2, value=med.get("dias", 1)).alignment = Alignment(horizontal="right")
        ws_mat.cell(row=r_mat, column=3, value=med["coste_unit"]).number_format = "#,##0.00 €"
        ws_mat.cell(row=r_mat, column=4, value=med["total"]).number_format = "#,##0.00 €"
        for i in range(1, 5):
            ws_mat.cell(row=r_mat, column=i).border = border_thin
        r_mat += 1

    ws_mat.column_dimensions["A"].width = 65
    ws_mat.column_dimensions["B"].width = 15
    ws_mat.column_dimensions["C"].width = 15
    ws_mat.column_dimensions["D"].width = 15
    ws_mat.column_dimensions["E"].width = 18

    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0060_Reparacion_Manga_Aeropuerto_Menorca.xlsx")
    wb.save(excel_path)
    return excel_path


def create_html_and_pdf():
    svg_path = os.path.join(BASE_DIR, "logo-ham.svg")
    svg_content = ""
    if os.path.exists(svg_path):
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

    p = DATA["partidas_cliente"][0]
    re = DATA["resumen_economico"]

    desc_lines = p["descripcion"].replace("\n", "<br>")
    cond_html = "".join([f"<li>{c}</li>" for c in DATA["condiciones_generales"]])

    # HTML CLIENTE (1 CONCEPTO - 1 SOLA PÁGINA A4)
    html_cliente = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presupuesto {DATA['codigo']} — Reparación Pasarela Aeropuerto Menorca</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 5mm 6mm 4mm 6mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      color: #1e293b;
      font-size: 8.2pt;
      line-height: 1.25;
      background: #f1f5f9;
    }}
    .document-page {{
      width: 100%;
      max-width: 210mm;
      margin: 0 auto;
      background: #fff;
      padding: 4mm 6mm;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
      position: relative;
    }}
    @media print {{
      body {{ background: #fff; margin: 0; }}
      .document-page {{
        width: 100%;
        max-width: none;
        padding: 0;
        margin: 0;
        box-shadow: none;
      }}
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #0f172a;
      color: #fff;
      padding: 6px 12px;
      border-radius: 5px;
      border-bottom: 3px solid #b45309;
      margin-bottom: 6px;
    }}
    .brand-box {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .brand-logo {{
      width: 36px;
      height: 36px;
      background: rgba(255,255,255,0.1);
      border-radius: 5px;
      padding: 2px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .brand-logo svg {{ width: 100%; height: 100%; }}
    .brand-text h1 {{
      margin: 0;
      font-size: 13pt;
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #ffffff;
      line-height: 1.1;
    }}
    .brand-text .sub {{
      font-size: 7.2pt;
      color: #cbd5e1;
      margin-top: 1px;
    }}
    .meta-box {{
      text-align: right;
      font-size: 7.5pt;
      line-height: 1.25;
      color: #e2e8f0;
    }}
    .meta-box strong {{
      font-size: 10pt;
      color: #fbbf24;
      display: block;
    }}
    .client-card {{
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 8px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 3.5px solid #0f172a;
      border-radius: 5px;
      padding: 5px 9px;
      margin-bottom: 5px;
    }}
    .client-card h3 {{
      margin: 0 0 2px 0;
      font-size: 7pt;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #64748b;
    }}
    .client-card p {{
      margin: 0;
      font-size: 8.2pt;
      color: #0f172a;
      font-weight: 600;
    }}
    .client-card .sub-info {{
      font-size: 7.4pt;
      color: #475569;
      font-weight: normal;
      margin-top: 1px;
    }}
    .badge-bar {{
      display: flex;
      gap: 6px;
      margin-bottom: 6px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 4px;
      padding: 2.5px 6px;
      font-size: 7pt;
      color: #1e40af;
      font-weight: 600;
    }}
    .badge.amber {{
      background: #fef3c7;
      border-color: #fde68a;
      color: #92400e;
    }}
    .photos-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 6px;
    }}
    .photo-card {{
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      overflow: hidden;
      background: #fff;
    }}
    .photo-card img {{
      width: 100%;
      height: 72px;
      object-fit: cover;
      display: block;
    }}
    .photo-caption {{
      padding: 2.5px 6px;
      font-size: 6.8pt;
      color: #475569;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      font-weight: 500;
      line-height: 1.15;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 6px;
    }}
    th {{
      background: #0f172a;
      color: #fff;
      padding: 4px 6px;
      font-size: 7.2pt;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    td {{
      padding: 5px 6px;
      border-bottom: 1px solid #e2e8f0;
      font-size: 7.6pt;
      vertical-align: top;
    }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .code {{ font-family: Consolas, monospace; font-size: 7.5pt; color: #475569; }}
    .item-title {{ font-weight: 700; color: #0f172a; font-size: 8pt; margin-bottom: 2px; }}
    .item-desc {{ font-size: 7.2pt; color: #475569; line-height: 1.25; }}
    .summary-box {{
      width: 240px;
      margin-left: auto;
      margin-bottom: 5px;
      border: 1px solid #cbd5e1;
      border-radius: 5px;
      overflow: hidden;
    }}
    .summary-row {{
      display: flex;
      justify-content: space-between;
      padding: 3.5px 8px;
      font-size: 7.8pt;
      border-bottom: 1px solid #e2e8f0;
    }}
    .summary-row.total {{
      background: #fef3c7;
      font-size: 9.5pt;
      font-weight: 800;
      color: #b45309;
      border-bottom: none;
    }}
    .conditions-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 5px 8px;
      margin-bottom: 5px;
    }}
    .conditions-box h4 {{
      margin: 0 0 2px 0;
      font-size: 7.2pt;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .conditions-box ul {{
      margin: 0;
      padding-left: 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 14px;
      row-gap: 2px;
      font-size: 6.9pt;
      color: #475569;
      line-height: 1.2;
    }}
    .signature-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 4px;
      padding-top: 4px;
      border-top: 1px solid #e2e8f0;
    }}
    .sig-box {{
      border: 1px dashed #cbd5e1;
      border-radius: 4px;
      padding: 4px 7px;
      min-height: 42px;
      background: #fafafa;
    }}
    .sig-box h5 {{
      margin: 0 0 1px 0;
      font-size: 6.8pt;
      text-transform: uppercase;
      color: #64748b;
    }}
    .sig-box .sub {{
      font-size: 6.4pt;
      color: #94a3b8;
    }}
  </style>
</head>
<body>
  <div class="document-page">
    <header>
      <div class="brand-box">
        <div class="brand-logo">
          {svg_content}
        </div>
        <div class="brand-text">
          <h1>{DATA['emisor']['nombre_comercial']}</h1>
          <div class="sub">{DATA['emisor']['razon_social']} · CIF: {DATA['emisor']['cif']} · Sant Lluís (Menorca)</div>
        </div>
      </div>
      <div class="meta-box">
        <strong>{DATA['codigo']}</strong>
        <div>Ref: {DATA['referencia']}</div>
        <div>Fecha: {DATA['fecha']} · Validez: {DATA['validez_dias']}d</div>
      </div>
    </header>

    <div class="client-card">
      <div>
        <h3>Cliente / Razón Social:</h3>
        <p style="font-size:7.6pt; line-height:1.2; margin-bottom:1px;"><strong>{DATA['cliente']['empresa']}</strong></p>
        <div class="sub-info">{DATA['cliente']['nombre_comercial']} · NIF: <strong>{DATA['cliente']['cif']}</strong></div>
        <div class="sub-info">{DATA['cliente']['domicilio']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']} · {DATA['cliente']['email']}</div>
      </div>
      <div>
        <h3>Emplazamiento Operativo:</h3>
        <p>{DATA['cliente']['emplazamiento']}</p>
        <div class="sub-info">{DATA['cliente']['direccion_obra']}</div>
        <div class="sub-info">{DATA['cliente']['atencion']}</div>
      </div>
    </div>

    <div class="badge-bar">
      <div class="badge">✔ Plataforma PEMP: Prestada por el cliente</div>
      <div class="badge amber">✔ Permisos y ZRS: Gestión por el cliente</div>
      <div class="badge">✔ Pintura: Bicomponente en obra (Norma HAM)</div>
    </div>

    <div class="photos-grid">
      <div class="photo-card">
        <img src="img/foto_dano_tubo_soporte.jpg" alt="Detalle de tubo dañado y soporte de guía">
        <div class="photo-caption"><strong>Inspección:</strong> Tubo 80x80x4 mm colapsado y soporte de guía deformado bajo chasis manga.</div>
      </div>
      <div class="photo-card">
        <img src="img/foto_perspectiva_manga_pista.jpg" alt="Perspectiva de la manga en plataforma aeroportuaria">
        <div class="photo-caption"><strong>Entorno en pista:</strong> Plataforma de aeronaves activa. Protocolo FOD y pantallas ignífugas.</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width: 8%;">Cód.</th>
          <th style="width: 54%;">Concepto y Alcance de la Actuación</th>
          <th style="width: 6%;" class="center">Ud.</th>
          <th style="width: 6%;" class="right">Cant.</th>
          <th style="width: 13%;" class="right">Precio Unit.</th>
          <th style="width: 13%;" class="right">Subtotal</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="center code">{p['codigo']}</td>
          <td>
            <div class="item-title">{p['concepto']}</div>
            <div class="item-desc">{desc_lines}</div>
          </td>
          <td class="center">{p['unidad']}</td>
          <td class="right bold">{p['cantidad']}</td>
          <td class="right bold">{eur(p['precio_venta_unitario'])}</td>
          <td class="right bold" style="color:#0f172a; font-size:8.5pt;">{eur(p['subtotal'])}</td>
        </tr>
      </tbody>
    </table>

    <div class="summary-box">
      <div class="summary-row">
        <span>BASE IMPONIBLE (1 x {eur(p['precio_venta_unitario'])}):</span>
        <span class="bold">{eur(re['venta_base_imponible'])}</span>
      </div>
      <div class="summary-row">
        <span>I.V.A. ({re['tipo_iva_pct']:.0f}%):</span>
        <span>{eur(re['importe_iva'])}</span>
      </div>
      <div class="summary-row total">
        <span>TOTAL OFERTA:</span>
        <span>{eur(re['total_presupuesto_con_iva'])}</span>
      </div>
    </div>

    <div class="conditions-box">
      <h4>Condiciones Generales y Compromisos Operacionales</h4>
      <ul>
        {cond_html}
      </ul>
    </div>

    <div class="signature-grid">
      <div class="sig-box">
        <h5>Por HAM Estructuras Metálicas Menorca</h5>
        <div class="sub">{DATA['emisor']['razon_social']} · Pablo Sánchez</div>
      </div>
      <div class="sig-box">
        <h5>Conforme Cliente / Aceptación de la Propuesta</h5>
        <div class="sub">Firma, sello y fecha de aceptación:</div>
      </div>
    </div>
  </div>
</body>
</html>"""

    # HTML INTERNO TÉCNICO
    mat_rows = ""
    for m in DATA["desglose_costes_internos"]["materiales"]:
        mat_rows += f"""
        <tr>
          <td>{m['concepto']}</td>
          <td class="center">{m['unidad']}</td>
          <td class="right">{m['cantidad']}</td>
          <td class="right">{eur(m['coste_unit'])}</td>
          <td class="right bold">{eur(m['total'])}</td>
        </tr>"""

    mo_rows = ""
    for mo in DATA["desglose_costes_internos"]["mano_de_obra"]:
        mo_rows += f"""
        <tr>
          <td>{mo['concepto']}</td>
          <td class="right">{mo['horas']} h</td>
          <td class="right">{eur(mo['tarifa'])}/h</td>
          <td class="right bold">{eur(mo['total'])}</td>
        </tr>"""

    med_rows = ""
    for med in DATA["desglose_costes_internos"]["medios_auxiliares_y_transporte"]:
        med_rows += f"""
        <tr>
          <td>{med['concepto']}</td>
          <td class="right">{med.get('dias', 1)}</td>
          <td class="right">{eur(med['coste_unit'])}</td>
          <td class="right bold">{eur(med['total'])}</td>
        </tr>"""

    html_interno = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Estudio Técnico Interno {DATA['codigo']} — Manga Aeropuerto Menorca</title>
  <style>
    @page {{ size: A4 landscape; margin: 8mm; }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      color: #1e293b;
      font-size: 8.5pt;
      line-height: 1.35;
      background: #f8fafc;
    }}
    .document-page {{
      width: 280mm;
      margin: 0 auto;
      background: #fff;
      padding: 8mm 10mm;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }}
    @media print {{
      body {{ background: #fff; }}
      .document-page {{ width: 100%; padding: 0; box-shadow: none; }}
    }}
    header {{
      background: #0f172a;
      color: #fff;
      padding: 8px 14px;
      border-radius: 6px;
      border-bottom: 3px solid #b45309;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    h1 {{ margin: 0; font-size: 13pt; color: #fff; }}
    .alert-banner {{
      background: #ecfdf5;
      border-left: 4px solid #059669;
      padding: 6px 10px;
      font-size: 8pt;
      color: #065f46;
      margin-bottom: 10px;
      border-radius: 4px;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin-bottom: 12px;
    }}
    .kpi-card {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-left: 3px solid #0f172a;
      border-radius: 5px;
      padding: 6px 8px;
    }}
    .kpi-title {{ font-size: 7.5pt; text-transform: uppercase; color: #64748b; font-weight: 700; }}
    .kpi-val {{ font-size: 12pt; font-weight: 800; color: #0f172a; }}
    .kpi-val.green {{ color: #15803d; }}
    .kpi-val.gold {{ color: #b45309; }}
    h2 {{
      font-size: 9.5pt;
      color: #0f172a;
      margin: 10px 0 5px 0;
      border-bottom: 2px solid #b45309;
      padding-bottom: 2px;
      text-transform: uppercase;
    }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 8pt; }}
    th {{ background: #0f172a; color: #fff; padding: 5px; text-align: left; }}
    td {{ padding: 4.5px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .green {{ color: #15803d; }}
    .tot {{ background: #fef3c7; font-weight: 800; }}
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  </style>
</head>
<body>
  <div class="document-page">
    <header>
      <div>
        <h1>ESTUDIO TÉCNICO INTERNO Y ANÁLISIS DE COSTES — {DATA['codigo']} (REV 2)</h1>
        <div style="font-size: 8pt; color: #cbd5e1;">HAM Estructuras Metálicas · Obra: Reparación Manga Pasarela (Aeropuerto de Menorca) · Concepto Único Cerrado</div>
      </div>
      <div style="text-align: right; font-size: 8pt; color: #fbbf24; font-weight: 700;">
        USO INTERNO EXCLUSIVO · NO ENTREGAR AL CLIENTE
      </div>
    </header>

    <div class="alert-banner">
      <strong>CONDICIONES CONFIRMADAS POR CLIENTE:</strong>
      1. Presupuesto comercial agrupado en <strong>partida única cerrada: 1 x 3.952,12 €</strong> (Base).
      2. <strong>Plataforma elevadora (PEMP):</strong> provista y prestada por el cliente (coste imputado = 0,00 €).
      3. <strong>Permisos y acreditaciones aeroportuarias:</strong> gestionados por el cliente (coste imputado = 0,00 €).
      4. <strong>Pintura:</strong> sistema bicomponente marino C5-M aplicado estrictamente en obra (prohibida pintura al horno según regla HAM).
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Coste Materiales</div>
        <div class="kpi-val">{eur(re['coste_materiales'])}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Coste Mano de Obra</div>
        <div class="kpi-val">{eur(re['coste_mano_obra'])}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Desplazamientos Taller</div>
        <div class="kpi-val">{eur(re['coste_medios_y_transporte'])}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Coste Directo Total</div>
        <div class="kpi-val gold">{eur(re['coste_directo_total'])}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Beneficio Neto Estimado</div>
        <div class="kpi-val green">{eur(re['beneficio_bruto'])} ({re['margen_sobre_venta_pct']:.1f}%)</div>
      </div>
    </div>

    <h2>1. Resumen Económico General (Concepto Único)</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 8%;" class="center">Cód.</th>
          <th style="width: 44%;">Concepto</th>
          <th style="width: 6%;" class="center">Ud.</th>
          <th style="width: 6%;" class="right">Cant.</th>
          <th style="width: 12%;" class="right">Coste Directo</th>
          <th style="width: 12%;" class="right">Venta Cliente</th>
          <th style="width: 12%;" class="right">Beneficio (Margen Vta.)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="center bold">{p['codigo']}</td>
          <td><strong>{p['concepto']}</strong></td>
          <td class="center">{p['unidad']}</td>
          <td class="right">{p['cantidad']}</td>
          <td class="right">{eur(re['coste_directo_total'])}</td>
          <td class="right bold">{eur(re['venta_base_imponible'])}</td>
          <td class="right bold green">{eur(re['beneficio_bruto'])} ({re['margen_sobre_venta_pct']:.1f}%)</td>
        </tr>
        <tr class="tot">
          <td colspan="4" class="right">TOTALES GENERALES:</td>
          <td class="right">{eur(re['coste_directo_total'])}</td>
          <td class="right">{eur(re['venta_base_imponible'])}</td>
          <td class="right green">{eur(re['beneficio_bruto'])} ({re['margen_sobre_venta_pct']:.1f}%)</td>
        </tr>
      </tbody>
    </table>

    <div class="grid-2">
      <div>
        <h2>2. Desglose de Materiales e Insumos</h2>
        <table>
          <thead>
            <tr><th>Material / Consumible</th><th class="center">Ud.</th><th class="right">Cant.</th><th class="right">Coste Ud.</th><th class="right">Total</th></tr>
          </thead>
          <tbody>{mat_rows}</tbody>
        </table>

        <h2>3. Medios Auxiliares y Logística</h2>
        <table>
          <thead>
            <tr><th>Concepto</th><th class="right">Días</th><th class="right">Coste Ud.</th><th class="right">Total</th></tr>
          </thead>
          <tbody>{med_rows}</tbody>
        </table>
      </div>

      <div>
        <h2>4. Desglose de Mano de Obra (Taller + Obra en Pista)</h2>
        <table>
          <thead>
            <tr><th>Puesto / Operación</th><th class="right">Horas</th><th class="right">Tarifa</th><th class="right">Total</th></tr>
          </thead>
          <tbody>{mo_rows}</tbody>
        </table>

        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; margin-top: 15px;">
          <h3 style="margin: 0 0 6px 0; font-size: 8.5pt; color: #0f172a; text-transform: uppercase;">Puntos Clave de Ejecución y Rentabilidad</h3>
          <ul style="margin: 0; padding-left: 16px; font-size: 7.8pt; color: #475569; line-height: 1.4;">
            <li><strong>Margen excelente:</strong> Con precio base de 3.952,12 € y sin repercutir coste de PEMP ni gestión de permisos, el beneficio bruto directo estimado asciende a <strong>2.212,12 €</strong> (55,97% sobre venta).</li>
            <li><strong>Apeo previo imprescindible:</strong> Sustentar la guía telescópica con puntales regulables antes de cortar el tubo 80x80x4 mm para no alterar el rodamiento.</li>
            <li><strong>Vigilancia de chispas y FOD:</strong> Mantas ignífugas perimetrales y barredora magnética al concluir cada jornada de corte y soldadura.</li>
            <li><strong>Pintura:</strong> Imprimación epoxi de alto espesor y esmalte poliuretano bicomponente aplicado en obra, nunca al horno.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
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
    print("Archivos generados exitosamente:")
    print(" - Excel:", xlsx)
    print(" - Cliente HTML:", cli_h)
    print(" - Cliente PDF:", cli_p)
    print(" - Técnico HTML:", int_h)
    print(" - Técnico PDF:", int_p)
