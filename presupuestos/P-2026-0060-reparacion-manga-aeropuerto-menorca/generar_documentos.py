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
    SLATE = "334155"
    GOLD = "B45309"
    LIGHT_BG = "F8FAFC"
    SUB_BG = "E2E8F0"
    TOTAL_BG = "FEF3C7"
    GREEN_TXT = "15803D"

    fill_navy = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUB_BG, end_color=SUB_BG, fill_type="solid")
    fill_alt = PatternFill(start_color=LIGHT_BG, end_color=LIGHT_BG, fill_type="solid")
    fill_total = PatternFill(start_color=TOTAL_BG, end_color=TOTAL_BG, fill_type="solid")

    font_title = Font(name="Segoe UI", size=14, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=10, bold=True, color=GOLD)
    font_head = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_regular = Font(name="Segoe UI", size=9, color="1E293B")
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
    # SHEET 1: PRESUPUESTO CLIENTE
    # ==========================================
    ws_cli.views.sheetView[0].showGridLines = True
    ws_cli.merge_cells("A1:G1")
    ws_cli["A1"] = f"{DATA['emisor']['nombre_comercial']} — {DATA['emisor']['razon_social']}"
    ws_cli["A1"].font = font_title

    ws_cli.merge_cells("A2:G2")
    ws_cli["A2"] = f"PRESUPUESTO TÉCNICO-COMERCIAL · Ref: {DATA['codigo']} ({DATA['referencia']})"
    ws_cli["A2"].font = font_sub

    ws_cli.cell(row=4, column=1, value="CLIENTE:").font = font_bold
    ws_cli.cell(row=4, column=2, value=DATA["cliente"]["empresa"]).font = font_regular
    ws_cli.cell(row=4, column=5, value="FECHA:").font = font_bold
    ws_cli.cell(row=4, column=6, value=DATA["fecha"]).font = font_regular

    ws_cli.cell(row=5, column=1, value="OBRA / UBICACIÓN:").font = font_bold
    ws_cli.cell(row=5, column=2, value=DATA["cliente"]["emplazamiento"]).font = font_regular
    ws_cli.cell(row=5, column=5, value="VALIDEZ:").font = font_bold
    ws_cli.cell(row=5, column=6, value=f"{DATA['validez_dias']} días").font = font_regular

    ws_cli.cell(row=6, column=1, value="ALCANCE RESUMIDO:").font = font_bold
    ws_cli.merge_cells("B6:G6")
    ws_cli["B6"] = DATA["proyecto"]["titulo"]
    ws_cli["B6"].font = font_regular

    # Table Header
    headers_cli = ["Cód.", "Concepto / Descripción de la Partida", "Ud.", "Cant.", "Precio Unitario", "Subtotal (€)"]
    start_row = 8
    for col_idx, h in enumerate(headers_cli, start=1):
        cell = ws_cli.cell(row=start_row, column=col_idx, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 3] else ("right" if col_idx >= 4 else "left"), vertical="center")
        cell.border = border_thin

    current_row = start_row + 1
    subtotal_formulas = []

    for cap in DATA["capitulos"]:
        # Chapter header
        ws_cli.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=6)
        c_title = ws_cli.cell(row=current_row, column=1, value=f"CAPÍTULO {cap['numero']} — {cap['titulo'].upper()}")
        c_title.font = font_sec
        c_title.fill = fill_sub
        c_title.border = border_thin
        current_row += 1

        for p in cap["partidas"]:
            ws_cli.cell(row=current_row, column=1, value=p["codigo"]).font = font_bold
            ws_cli.cell(row=current_row, column=1).alignment = Alignment(horizontal="center")
            ws_cli.cell(row=current_row, column=1).border = border_thin

            ws_cli.cell(row=current_row, column=2, value=f"{p['concepto']}\n{p['descripcion']}").font = font_regular
            ws_cli.cell(row=current_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
            ws_cli.cell(row=current_row, column=2).border = border_thin

            ws_cli.cell(row=current_row, column=3, value=p["unidad"]).font = font_regular
            ws_cli.cell(row=current_row, column=3).alignment = Alignment(horizontal="center", vertical="top")
            ws_cli.cell(row=current_row, column=3).border = border_thin

            ws_cli.cell(row=current_row, column=4, value=p["cantidad"]).font = font_regular
            ws_cli.cell(row=current_row, column=4).alignment = Alignment(horizontal="right", vertical="top")
            ws_cli.cell(row=current_row, column=4).border = border_thin

            p_unit = ws_cli.cell(row=current_row, column=5, value=p["precio_venta_unitario"])
            p_unit.font = font_regular
            p_unit.number_format = "#,##0.00 €"
            p_unit.alignment = Alignment(horizontal="right", vertical="top")
            p_unit.border = border_thin

            p_sub = ws_cli.cell(row=current_row, column=6, value=f"=D{current_row}*E{current_row}")
            p_sub.font = font_bold
            p_sub.number_format = "#,##0.00 €"
            p_sub.alignment = Alignment(horizontal="right", vertical="top")
            p_sub.border = border_thin
            subtotal_formulas.append(f"F{current_row}")

            current_row += 1

    current_row += 1
    # Totals
    ws_cli.cell(row=current_row, column=4, value="BASE IMPONIBLE:").font = font_sec
    ws_cli.cell(row=current_row, column=6, value=f"=SUM({','.join(subtotal_formulas)})").font = font_total
    ws_cli.cell(row=current_row, column=6).number_format = "#,##0.00 €"
    ws_cli.cell(row=current_row, column=6).fill = fill_total
    ws_cli.cell(row=current_row, column=6).border = border_thin
    base_row = current_row

    current_row += 1
    ws_cli.cell(row=current_row, column=4, value=f"I.V.A. ({DATA['resumen_economico']['tipo_iva_pct']:.0f}%):").font = font_regular
    ws_cli.cell(row=current_row, column=6, value=f"=F{base_row}*{DATA['resumen_economico']['tipo_iva_pct']/100}").font = font_regular
    ws_cli.cell(row=current_row, column=6).number_format = "#,##0.00 €"
    ws_cli.cell(row=current_row, column=6).border = border_thin
    iva_row = current_row

    current_row += 1
    ws_cli.cell(row=current_row, column=4, value="TOTAL PRESUPUESTO:").font = font_total_gold
    ws_cli.cell(row=current_row, column=6, value=f"=F{base_row}+F{iva_row}").font = font_total_gold
    ws_cli.cell(row=current_row, column=6).number_format = "#,##0.00 €"
    ws_cli.cell(row=current_row, column=6).fill = fill_total
    ws_cli.cell(row=current_row, column=6).border = border_double

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
    ws_cli.column_dimensions["A"].width = 10
    ws_cli.column_dimensions["B"].width = 65
    ws_cli.column_dimensions["C"].width = 8
    ws_cli.column_dimensions["D"].width = 8
    ws_cli.column_dimensions["E"].width = 16
    ws_cli.column_dimensions["F"].width = 18

    # ==========================================
    # SHEET 2: ESTUDIO TÉCNICO INTERNO
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

    r_int = 4
    for cap in DATA["capitulos"]:
        for p in cap["partidas"]:
            c_coste = p["coste_unitario"] * p["cantidad"]
            c_venta = p["precio_venta_unitario"] * p["cantidad"]
            c_ben = c_venta - c_coste
            m_vta = (c_ben / c_venta * 100) if c_venta else 0
            m_cst = (c_ben / c_coste * 100) if c_coste else 0

            ws_int.cell(row=r_int, column=1, value=f"{p['codigo']} - {p['concepto']}").font = font_regular
            ws_int.cell(row=r_int, column=2, value=c_coste).number_format = "#,##0.00 €"
            ws_int.cell(row=r_int, column=3, value=c_venta).number_format = "#,##0.00 €"
            ws_int.cell(row=r_int, column=4, value=c_ben).number_format = "#,##0.00 €"
            ws_int.cell(row=r_int, column=5, value=m_vta / 100).number_format = "0.0%"
            ws_int.cell(row=r_int, column=6, value=m_cst / 100).number_format = "0.0%"

            for c in range(1, 7):
                ws_int.cell(row=r_int, column=c).border = border_thin
            r_int += 1

    # Total Row
    ws_int.cell(row=r_int, column=1, value="TOTALES").font = font_total
    ws_int.cell(row=r_int, column=2, value=DATA["resumen_economico"]["coste_directo_total"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=3, value=DATA["resumen_economico"]["venta_base_imponible"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=4, value=DATA["resumen_economico"]["beneficio_bruto"]).number_format = "#,##0.00 €"
    ws_int.cell(row=r_int, column=5, value=DATA["resumen_economico"]["margen_sobre_venta_pct"] / 100).number_format = "0.0%"
    ws_int.cell(row=r_int, column=6, value=DATA["resumen_economico"]["margen_sobre_coste_pct"] / 100).number_format = "0.0%"

    for c in range(1, 7):
        ws_int.cell(row=r_int, column=c).font = font_total
        ws_int.cell(row=r_int, column=c).fill = fill_total
        ws_int.cell(row=r_int, column=c).border = border_double

    # Breakdown by resource
    r_int += 3
    ws_int.cell(row=r_int, column=1, value="RESUMEN POR NATURALEZA DE COSTE").font = font_sec
    r_int += 1
    re = DATA["resumen_economico"]
    nature = [
        ("Materiales e Insumos", re["coste_materiales"]),
        ("Mano de Obra y Gestión Técnica", re["coste_mano_obra"]),
        ("Medios Auxiliares (PEMP) y Desplazamientos", re["coste_medios_y_transporte"]),
        ("COSTE DIRECTO TOTAL", re["coste_directo_total"]),
        ("PRECIO VENTA RECOMENDADO (BASE)", re["venta_base_imponible"]),
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

    ws_int.column_dimensions["A"].width = 50
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

    # Table 1: Materiales
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

    # Table 2: Mano de Obra
    r_mat += 2
    ws_mat.cell(row=r_mat, column=1, value="2. Mano de Obra y Supervisión Técnica").font = font_sec
    r_mat += 1
    mo_heads = ["Puesto / Tarea", "Horas", "Tarifa (€/h)", "Subtotal (€)", ""]
    for i, h in enumerate(mo_heads[:4], start=1):
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

    # Table 3: Maquinaria y Medios
    r_mat += 2
    ws_mat.cell(row=r_mat, column=1, value="3. Medios de Elevación (PEMP) y Desplazamientos").font = font_sec
    r_mat += 1
    for i, h in enumerate(["Concepto", "Unidades/Días", "Coste Ud. (€)", "Subtotal (€)"], start=1):
        cell = ws_mat.cell(row=r_mat, column=i, value=h)
        cell.font = font_head
        cell.fill = fill_navy
        cell.border = border_thin
    r_mat += 1
    for med in DATA["desglose_costes_internos"]["medios_auxiliares_y_transporte"]:
        ws_mat.cell(row=r_mat, column=1, value=med["concepto"]).font = font_regular
        cnt = med.get("dias", med.get("viajes", 1))
        ws_mat.cell(row=r_mat, column=2, value=cnt).alignment = Alignment(horizontal="right")
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
    # Load HAM Logo SVG
    svg_path = os.path.join(BASE_DIR, "logo-ham.svg")
    svg_content = ""
    if os.path.exists(svg_path):
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

    # Partidas client table rows
    rows_cliente = ""
    for cap in DATA["capitulos"]:
        rows_cliente += f"""
        <tr class="cap-row">
          <td colspan="6"><strong>CAPÍTULO {cap['numero']} — {cap['titulo'].upper()}</strong></td>
        </tr>"""
        for p in cap["partidas"]:
            sub = p["cantidad"] * p["precio_venta_unitario"]
            rows_cliente += f"""
            <tr>
              <td class="center code">{p['codigo']}</td>
              <td>
                <div class="item-title">{p['concepto']}</div>
                <div class="item-desc">{p['descripcion']}</div>
              </td>
              <td class="center">{p['unidad']}</td>
              <td class="right">{p['cantidad']}</td>
              <td class="right bold">{eur(p['precio_venta_unitario'])}</td>
              <td class="right bold total-cell">{eur(sub)}</td>
            </tr>"""

    re = DATA["resumen_economico"]

    cond_html = "".join([f"<li>{c}</li>" for c in DATA["condiciones_generales"]])

    # HTML CLIENTE
    html_cliente = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presupuesto {DATA['codigo']} — Reparación Pasarela Aeropuerto Menorca</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 8mm 9mm 8mm 9mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      color: #1e293b;
      font-size: 8.8pt;
      line-height: 1.35;
      background: #f1f5f9;
    }}
    .document-page {{
      width: 210mm;
      min-height: 297mm;
      margin: 0 auto;
      background: #fff;
      padding: 10mm 12mm;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
      position: relative;
    }}
    @media print {{
      body {{ background: #fff; }}
      .document-page {{
        width: 100%;
        min-height: auto;
        padding: 0;
        box-shadow: none;
      }}
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #0f172a;
      color: #fff;
      padding: 10px 16px;
      border-radius: 6px;
      border-bottom: 4px solid #b45309;
      margin-bottom: 12px;
    }}
    .brand-box {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-logo {{
      width: 44px;
      height: 44px;
      background: rgba(255,255,255,0.1);
      border-radius: 6px;
      padding: 3px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .brand-logo svg {{ width: 100%; height: 100%; }}
    .brand-text h1 {{
      margin: 0;
      font-size: 15pt;
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #ffffff;
    }}
    .brand-text .sub {{
      font-size: 8pt;
      color: #cbd5e1;
      margin-top: 1px;
    }}
    .meta-box {{
      text-align: right;
      font-size: 8.5pt;
      line-height: 1.35;
      color: #e2e8f0;
    }}
    .meta-box strong {{
      font-size: 11pt;
      color: #fbbf24;
      display: block;
    }}
    .client-card {{
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 10px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 4px solid #0f172a;
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 12px;
    }}
    .client-card h3 {{
      margin: 0 0 4px 0;
      font-size: 8pt;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #64748b;
    }}
    .client-card p {{
      margin: 0;
      font-size: 9pt;
      color: #0f172a;
      font-weight: 600;
    }}
    .client-card .sub-info {{
      font-size: 8pt;
      color: #475569;
      font-weight: normal;
      margin-top: 2px;
    }}
    .scope-box {{
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-left: 4px solid #2563eb;
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 12px;
    }}
    .scope-box h4 {{
      margin: 0 0 3px 0;
      font-size: 8.5pt;
      color: #1e40af;
      text-transform: uppercase;
      font-weight: 700;
    }}
    .scope-box p {{
      margin: 0;
      font-size: 8.3pt;
      color: #1e3a8a;
      line-height: 1.35;
    }}
    .photos-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 12px;
    }}
    .photo-card {{
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      overflow: hidden;
      background: #fff;
    }}
    .photo-card img {{
      width: 100%;
      height: 120px;
      object-fit: cover;
      display: block;
    }}
    .photo-caption {{
      padding: 4px 8px;
      font-size: 7.5pt;
      color: #475569;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      font-weight: 500;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 12px;
    }}
    th {{
      background: #0f172a;
      color: #fff;
      padding: 6px 8px;
      font-size: 8pt;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    td {{
      padding: 6px 8px;
      border-bottom: 1px solid #e2e8f0;
      font-size: 8.3pt;
      vertical-align: top;
    }}
    .cap-row td {{
      background: #e2e8f0;
      color: #0f172a;
      font-size: 8.2pt;
      border-top: 1px solid #cbd5e1;
      border-bottom: 1px solid #cbd5e1;
      padding: 5px 8px;
    }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .bold {{ font-weight: 700; }}
    .code {{ font-family: Consolas, monospace; font-size: 8pt; color: #475569; }}
    .item-title {{ font-weight: 700; color: #0f172a; margin-bottom: 2px; }}
    .item-desc {{ font-size: 7.8pt; color: #64748b; line-height: 1.3; }}
    .total-cell {{ color: #0f172a; }}
    .summary-box {{
      width: 250px;
      margin-left: auto;
      margin-bottom: 12px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      overflow: hidden;
    }}
    .summary-row {{
      display: flex;
      justify-content: space-between;
      padding: 5px 10px;
      font-size: 8.5pt;
      border-bottom: 1px solid #e2e8f0;
    }}
    .summary-row.total {{
      background: #fef3c7;
      font-size: 10pt;
      font-weight: 800;
      color: #b45309;
      border-bottom: none;
    }}
    .conditions-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 12px;
    }}
    .conditions-box h4 {{
      margin: 0 0 4px 0;
      font-size: 8pt;
      color: #0f172a;
      text-transform: uppercase;
    }}
    .conditions-box ul {{
      margin: 0;
      padding-left: 16px;
      font-size: 7.8pt;
      color: #475569;
      line-height: 1.35;
    }}
    .signature-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid #e2e8f0;
    }}
    .sig-box {{
      border: 1px dashed #cbd5e1;
      border-radius: 6px;
      padding: 8px 10px;
      min-height: 65px;
      background: #fafafa;
    }}
    .sig-box h5 {{
      margin: 0 0 2px 0;
      font-size: 7.5pt;
      text-transform: uppercase;
      color: #64748b;
    }}
    .sig-box .sub {{
      font-size: 7pt;
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
        <div>Fecha: {DATA['fecha']}</div>
        <div>Validez: {DATA['validez_dias']} días</div>
      </div>
    </header>

    <div class="client-card">
      <div>
        <h3>Cliente / Entidad Promotora:</h3>
        <p>{DATA['cliente']['empresa']}</p>
        <div class="sub-info">{DATA['cliente']['atencion']}</div>
        <div class="sub-info">{DATA['cliente']['obra']}</div>
      </div>
      <div>
        <h3>Emplazamiento Operativo:</h3>
        <p>{DATA['cliente']['emplazamiento']}</p>
        <div class="sub-info">{DATA['cliente']['direccion']} — {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}</div>
        <div class="sub-info">Régimen: Plataforma de Aeronaves (Lado Aire AENA)</div>
      </div>
    </div>

    <div class="scope-box">
      <h4>Alcance de los Trabajos y Especificaciones Principales</h4>
      <p>
        {DATA['proyecto']['descripcion']}
      </p>
    </div>

    <div class="photos-grid">
      <div class="photo-card">
        <img src="img/foto_dano_tubo_soporte.jpg" alt="Detalle de tubo dañado y soporte de guía">
        <div class="photo-caption"><strong>Inspección visual:</strong> Tubo estructural 80x80x4 mm colapsado y soporte de guía industrial con corrosión y deformación bajo el chasis de la manga.</div>
      </div>
      <div class="photo-card">
        <img src="img/foto_perspectiva_manga_pista.jpg" alt="Perspectiva de la manga en plataforma aeroportuaria">
        <div class="photo-caption"><strong>Entorno de trabajo:</strong> Plataforma activa de estacionamiento de aeronaves (apron). Requiere PEMP, protocolo FOD, acreditaciones AENA y hot work permit.</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width: 8%;">Cód.</th>
          <th style="width: 52%;">Descripción de la Partida</th>
          <th style="width: 6%;" class="center">Ud.</th>
          <th style="width: 6%;" class="right">Cant.</th>
          <th style="width: 14%;" class="right">Precio Unit.</th>
          <th style="width: 14%;" class="right">Subtotal</th>
        </tr>
      </thead>
      <tbody>
        {rows_cliente}
      </tbody>
    </table>

    <div class="summary-box">
      <div class="summary-row">
        <span>BASE IMPONIBLE:</span>
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
    rows_int = ""
    for cap in DATA["capitulos"]:
        rows_int += f"""
        <tr class="cap-row">
          <td colspan="7"><strong>CAPÍTULO {cap['numero']} — {cap['titulo'].upper()}</strong></td>
        </tr>"""
        for p in cap["partidas"]:
            c_cost = p["coste_unitario"] * p["cantidad"]
            c_vent = p["precio_venta_unitario"] * p["cantidad"]
            ben = c_vent - c_cost
            mg = (ben / c_vent * 100) if c_vent else 0
            rows_int += f"""
            <tr>
              <td class="center code">{p['codigo']}</td>
              <td><strong>{p['concepto']}</strong></td>
              <td class="center">{p['unidad']}</td>
              <td class="right">{p['cantidad']}</td>
              <td class="right">{eur(c_cost)}</td>
              <td class="right bold">{eur(c_vent)}</td>
              <td class="right bold green">{eur(ben)} ({mg:.1f}%)</td>
            </tr>"""

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
        cnt = med.get("dias", med.get("viajes", 1))
        med_rows += f"""
        <tr>
          <td>{med['concepto']}</td>
          <td class="right">{cnt}</td>
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
      background: #fee2e2;
      border-left: 4px solid #b91c1c;
      padding: 6px 10px;
      font-size: 8pt;
      color: #7f1d1d;
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
    .cap-row td {{ background: #e2e8f0; font-weight: 700; }}
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
        <h1>ESTUDIO TÉCNICO INTERNO Y ANÁLISIS DE COSTES — {DATA['codigo']}</h1>
        <div style="font-size: 8pt; color: #cbd5e1;">HAM Estructuras Metálicas · Obra: Reparación Manga de Pasarela (Pista Aeropuerto de Menorca)</div>
      </div>
      <div style="text-align: right; font-size: 8pt; color: #fbbf24; font-weight: 700;">
        USO INTERNO EXCLUSIVO · NO ENTREGAR AL CLIENTE
      </div>
    </header>

    <div class="alert-banner">
      <strong>CRITERIOS DE ALTA COMPLEJIDAD Y SEGURIDAD:</strong> Trabajo en pista activa de aeronaves (zona aire AENA). Requiere acreditaciones ZRS, permiso de trabajo en caliente (cecop), protocolo FOD estricto de barrido magnético permanente y plataforma elevadora PEMP. Pintura bicomponente formulada para categoría marina C5-M aplicada estrictamente en obra (prohibida pintura al horno según regla HAM).
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
        <div class="kpi-title">Medios (PEMP) + Transp.</div>
        <div class="kpi-val">{eur(re['coste_medios_y_transporte'])}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Coste Directo Total</div>
        <div class="kpi-val gold">{eur(re['coste_directo_total'])}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Beneficio Estimado</div>
        <div class="kpi-val green">{eur(re['beneficio_bruto'])} ({re['margen_sobre_venta_pct']:.1f}%)</div>
      </div>
    </div>

    <h2>1. Resumen Económico por Partida</h2>
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
        {rows_int}
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

        <h2>3. Medios de Elevación y Logística</h2>
        <table>
          <thead>
            <tr><th>Concepto</th><th class="right">Unidades</th><th class="right">Coste Ud.</th><th class="right">Total</th></tr>
          </thead>
          <tbody>{med_rows}</tbody>
        </table>
      </div>

      <div>
        <h2>4. Desglose de Mano de Obra y Supervisión Técnica</h2>
        <table>
          <thead>
            <tr><th>Puesto / Operación</th><th class="right">Horas</th><th class="right">Tarifa</th><th class="right">Total</th></tr>
          </thead>
          <tbody>{mo_rows}</tbody>
        </table>

        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; margin-top: 15px;">
          <h3 style="margin: 0 0 6px 0; font-size: 8.5pt; color: #0f172a; text-transform: uppercase;">Puntos Críticos de Ejecución Técnica</h3>
          <ul style="margin: 0; padding-left: 16px; font-size: 7.8pt; color: #475569; line-height: 1.4;">
            <li><strong>Apeo previo:</strong> La guía telescópica debe estar acuñada y sustentada para evitar que al cortar el tubo de 80x80x4 mm se altere la flecha o se desplace el eje de rodadura.</li>
            <li><strong>Seguridad en caliente:</strong> Mantas ignífugas y presencia activa de vigilante con extintor durante el soldeo y amolado para evitar ignición de sellados de manga o cableados adyacentes.</li>
            <li><strong>Barrido FOD estricto:</strong> Ningún resto metálico puede quedar en la plataforma; se utilizará barredora magnética manual al final de cada jornada.</li>
            <li><strong>Pintura en obra:</strong> Aplicar imprimación epoxi rica en fosfato de zinc y acabado poliuretano bicomponente C5-M a brocha/rodillo respetando tiempos de repintado. Prohibida pintura al horno.</li>
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
