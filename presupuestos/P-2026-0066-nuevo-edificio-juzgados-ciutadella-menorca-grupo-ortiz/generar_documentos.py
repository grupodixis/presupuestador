import os
import json
import subprocess
import shutil
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
NETWORK_DIR = r"o:\030. Comercial\210. Presupuestos\Grupo Ortiz\10. ESTRUCTURA METÁLICA Y CERRAJERÍA"

def eur(val):
    if val is None:
        return "0,00 €"
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def num(val):
    if val is None:
        return "0,00"
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# -------------------------------------------------------------------------
# GENERACIÓN DE EXCEL PROFESIONAL CON FÓRMULAS ACTIVAS
# -------------------------------------------------------------------------
def create_excel():
    wb = Workbook()

    # Colores corporativos
    NAVY = "0F172A"       # Encabezados principales
    BLUE_SUB = "1E3A8A"   # Capítulos
    GOLD = "B45309"       # Acentos
    SLATE_LIGHT = "F8FAFC"# Filas alternas
    TOTAL_FILL = "FEF3C7" # Totales
    HEADER_TEXT = "FFFFFF"

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_cap = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")

    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9.5, bold=True, color=HEADER_TEXT)
    font_cap = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=9, color="1E293B")
    font_desc = Font(name="Segoe UI", size=8.5, color="475569")
    font_tot = Font(name="Segoe UI", size=10, bold=True, color=NAVY)

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

    # ----------------------------------------------------
    # PESTAÑA 1: OFERTA COMERCIAL (CLIENTE)
    # ----------------------------------------------------
    ws1 = wb.active
    ws1.title = "Oferta Comercial"
    ws1.views.sheetView[0].showGridLines = True

    # Cabecera Documento
    ws1.merge_cells("A1:G1")
    ws1["A1"] = f"{DATA['emisor']['empresa']} · {DATA['emisor']['marca_comercial']}"
    ws1["A1"].font = font_title
    ws1["A1"].alignment = Alignment(vertical="center")

    ws1.merge_cells("A2:G2")
    ws1["A2"] = f"CIF: {DATA['emisor']['cif']} · {DATA['emisor']['domicilio']}, {DATA['emisor']['codigo_postal']} {DATA['emisor']['poblacion']} (Menorca) · Tel: {DATA['emisor']['telefono']} · {DATA['emisor']['web']}"
    ws1["A2"].font = Font(name="Segoe UI", size=8.5, color="64748B")

    ws1.merge_cells("A4:G4")
    ws1["A4"] = f"OFERTA ECONÓMICA: {DATA['codigo']} · {DATA['proyecto']['titulo']}"
    ws1["A4"].font = Font(name="Segoe UI", size=11, bold=True, color=NAVY)

    ws1["A5"] = "CLIENTE:"
    ws1["A5"].font = font_bold
    ws1["B5"] = DATA['cliente']['empresa']
    ws1["B5"].font = font_bold
    ws1["E5"] = "EXPEDIENTE:"
    ws1["E5"].font = font_bold
    ws1["F5"] = DATA['proyecto']['expediente']

    ws1["A6"] = "ATENCIÓN:"
    ws1["A6"].font = font_reg
    ws1["B6"] = f"{DATA['cliente']['contacto']} ({DATA['cliente']['cargo']}) · {DATA['cliente']['telefono']}"
    ws1["E6"] = "FECHA EMISIÓN:"
    ws1["E6"].font = font_reg
    ws1["F6"] = DATA['fecha']

    ws1["A7"] = "LOCALIZACIÓN:"
    ws1["A7"].font = font_reg
    ws1["B7"] = DATA['proyecto']['emplazamiento']
    ws1["E7"] = "FECHA LÍMITE:"
    ws1["E7"].font = font_reg
    ws1["F7"] = DATA['fecha_entrega_limite']

    # Encabezados de tabla
    headers1 = ["CÓDIGO", "CONCEPTO / RESUMEN DE PARTIDA", "UD", "CANTIDAD", "PRECIO UNIT. (€)", "IMPORTE (€)", "NOTAS"]
    row_idx = 9
    for col_idx, h in enumerate(headers1, start=1):
        cell = ws1.cell(row=row_idx, column=col_idx, value=h)
        cell.fill = fill_header
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 3, 4, 5, 6] else "left", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[row_idx].height = 24

    item_rows = []
    row_idx += 1

    for cap in DATA["capitulos"]:
        # Fila de Capítulo
        ws1.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=7)
        c_cell = ws1.cell(row=row_idx, column=1, value=f"{cap['codigo']} · {cap['titulo']}")
        c_cell.fill = fill_cap
        c_cell.font = font_cap
        c_cell.alignment = Alignment(vertical="center")
        for col_i in range(1, 8):
            ws1.cell(row=row_idx, column=col_i).border = border_thin
        ws1.row_dimensions[row_idx].height = 20
        row_idx += 1

        for p in cap["partidas"]:
            c_cod = ws1.cell(row=row_idx, column=1, value=p["codigo"])
            c_desc = ws1.cell(row=row_idx, column=2, value=p["descripcion_corta"])
            c_ud = ws1.cell(row=row_idx, column=3, value=p["unidad"])
            c_cant = ws1.cell(row=row_idx, column=4, value=p["cantidad"])
            c_punit = ws1.cell(row=row_idx, column=5, value=p["precio_unitario_venta"])
            c_tot = ws1.cell(row=row_idx, column=6, value=f"=D{row_idx}*E{row_idx}")
            c_not = ws1.cell(row=row_idx, column=7, value="Conforme a proyecto")

            c_cod.alignment = Alignment(horizontal="center", vertical="center")
            c_desc.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            c_ud.alignment = Alignment(horizontal="center", vertical="center")
            c_cant.alignment = Alignment(horizontal="right", vertical="center")
            c_punit.alignment = Alignment(horizontal="right", vertical="center")
            c_tot.alignment = Alignment(horizontal="right", vertical="center")
            c_not.alignment = Alignment(horizontal="left", vertical="center")

            c_cant.number_format = "#,##0.00"
            c_punit.number_format = "#,##0.00 €"
            c_tot.number_format = "#,##0.00 €"

            for col_i in range(1, 8):
                cell_i = ws1.cell(row=row_idx, column=col_i)
                cell_i.border = border_thin
                cell_i.font = font_reg

            item_rows.append(row_idx)
            ws1.row_dimensions[row_idx].height = 22
            row_idx += 1

    # Fila de Totales
    row_idx += 1
    sum_formula = "+".join([f"F{r}" for r in item_rows])
    
    ws1.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=5)
    t_lbl = ws1.cell(row=row_idx, column=1, value="TOTAL BASE IMPONIBLE (VENTA)")
    t_lbl.font = font_tot
    t_lbl.alignment = Alignment(horizontal="right", vertical="center")
    t_lbl.fill = fill_tot
    for col_i in range(1, 6):
        ws1.cell(row=row_idx, column=col_i).border = border_total
        ws1.cell(row=row_idx, column=col_i).fill = fill_tot

    t_val = ws1.cell(row=row_idx, column=6, value=f"={sum_formula}")
    t_val.font = font_tot
    t_val.alignment = Alignment(horizontal="right", vertical="center")
    t_val.number_format = "#,##0.00 €"
    t_val.border = border_total
    t_val.fill = fill_tot
    base_row = row_idx
    ws1.row_dimensions[row_idx].height = 24
    row_idx += 1

    # IVA
    ws1.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=5)
    iva_lbl = ws1.cell(row=row_idx, column=1, value="I.V.A. REPERCUTIBLE (21%)")
    iva_lbl.font = font_reg
    iva_lbl.alignment = Alignment(horizontal="right", vertical="center")
    for col_i in range(1, 6):
        ws1.cell(row=row_idx, column=col_i).border = border_thin

    iva_val = ws1.cell(row=row_idx, column=6, value=f"=F{base_row}*0.21")
    iva_val.font = font_reg
    iva_val.alignment = Alignment(horizontal="right", vertical="center")
    iva_val.number_format = "#,##0.00 €"
    iva_val.border = border_thin
    iva_row = row_idx
    ws1.row_dimensions[row_idx].height = 20
    row_idx += 1

    # TOTAL PRESUPUESTO
    ws1.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=5)
    tot_lbl = ws1.cell(row=row_idx, column=1, value="TOTAL PRESUPUESTO (CON IVA)")
    tot_lbl.font = font_title
    tot_lbl.alignment = Alignment(horizontal="right", vertical="center")
    tot_lbl.fill = fill_tot
    for col_i in range(1, 6):
        ws1.cell(row=row_idx, column=col_i).border = border_total
        ws1.cell(row=row_idx, column=col_i).fill = fill_tot

    tot_val = ws1.cell(row=row_idx, column=6, value=f"=F{base_row}+F{iva_row}")
    tot_val.font = font_title
    tot_val.alignment = Alignment(horizontal="right", vertical="center")
    tot_val.number_format = "#,##0.00 €"
    tot_val.border = border_total
    tot_val.fill = fill_tot
    ws1.row_dimensions[row_idx].height = 26

    # ----------------------------------------------------
    # PESTAÑA 2: ESCANDALLO INTERNO Y COSTES (CONFIDENCIAL)
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="Escandallo Interno")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:I1")
    ws2["A1"] = f"ESTUDIO CONFIDENCIAL DE COSTES, MÁRGENES Y RENTABILIDAD · {DATA['codigo']}"
    ws2["A1"].font = font_title
    ws2["A1"].alignment = Alignment(vertical="center")

    headers2 = ["CÓDIGO", "CAPÍTULO / PARTIDA", "UD", "CANTIDAD", "COSTE UNIT. (€)", "COSTE TOTAL (€)", "VENTA UNIT. (€)", "VENTA TOTAL (€)", "MARGEN (€)"]
    row_idx2 = 3
    for col_idx, h in enumerate(headers2, start=1):
        cell = ws2.cell(row=row_idx2, column=col_idx, value=h)
        cell.fill = fill_header
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 3, 4, 5, 6, 7, 8, 9] else "left", vertical="center")
        cell.border = border_thin
    ws2.row_dimensions[row_idx2].height = 24

    item_rows2 = []
    row_idx2 += 1

    for cap in DATA["capitulos"]:
        ws2.merge_cells(start_row=row_idx2, start_column=1, end_row=row_idx2, end_column=9)
        c_cell = ws2.cell(row=row_idx2, column=1, value=f"{cap['codigo']} · {cap['titulo']}")
        c_cell.fill = fill_cap
        c_cell.font = font_cap
        for col_i in range(1, 10):
            ws2.cell(row=row_idx2, column=col_i).border = border_thin
        ws2.row_dimensions[row_idx2].height = 20
        row_idx2 += 1

        for p in cap["partidas"]:
            ws2.cell(row=row_idx2, column=1, value=p["codigo"]).alignment = Alignment(horizontal="center", vertical="center")
            ws2.cell(row=row_idx2, column=2, value=p["descripcion_corta"]).alignment = Alignment(horizontal="left", vertical="center")
            ws2.cell(row=row_idx2, column=3, value=p["unidad"]).alignment = Alignment(horizontal="center", vertical="center")
            
            c_cant = ws2.cell(row=row_idx2, column=4, value=p["cantidad"])
            c_cant.number_format = "#,##0.00"
            c_cant.alignment = Alignment(horizontal="right", vertical="center")

            c_cunit = ws2.cell(row=row_idx2, column=5, value=p["coste_unitario"])
            c_cunit.number_format = "#,##0.00 €"
            c_cunit.alignment = Alignment(horizontal="right", vertical="center")

            c_ctot = ws2.cell(row=row_idx2, column=6, value=f"=D{row_idx2}*E{row_idx2}")
            c_ctot.number_format = "#,##0.00 €"
            c_ctot.alignment = Alignment(horizontal="right", vertical="center")

            c_vunit = ws2.cell(row=row_idx2, column=7, value=p["precio_unitario_venta"])
            c_vunit.number_format = "#,##0.00 €"
            c_vunit.alignment = Alignment(horizontal="right", vertical="center")

            c_vtot = ws2.cell(row=row_idx2, column=8, value=f"=D{row_idx2}*G{row_idx2}")
            c_vtot.number_format = "#,##0.00 €"
            c_vtot.alignment = Alignment(horizontal="right", vertical="center")

            c_mrg = ws2.cell(row=row_idx2, column=9, value=f"=H{row_idx2}-F{row_idx2}")
            c_mrg.number_format = "#,##0.00 €"
            c_mrg.alignment = Alignment(horizontal="right", vertical="center")

            for col_i in range(1, 10):
                cell_i = ws2.cell(row=row_idx2, column=col_i)
                cell_i.border = border_thin
                cell_i.font = font_reg

            item_rows2.append(row_idx2)
            ws2.row_dimensions[row_idx2].height = 20
            row_idx2 += 1

    # Totales Escandallo
    row_idx2 += 1
    sum_coste = "+".join([f"F{r}" for r in item_rows2])
    sum_venta = "+".join([f"H{r}" for r in item_rows2])
    sum_mrg = "+".join([f"I{r}" for r in item_rows2])

    ws2.merge_cells(start_row=row_idx2, start_column=1, end_row=row_idx2, end_column=5)
    t2_lbl = ws2.cell(row=row_idx2, column=1, value="TOTALES GENERALES")
    t2_lbl.font = font_tot
    t2_lbl.alignment = Alignment(horizontal="right", vertical="center")
    t2_lbl.fill = fill_tot
    for col_i in range(1, 6):
        ws2.cell(row=row_idx2, column=col_i).border = border_total
        ws2.cell(row=row_idx2, column=col_i).fill = fill_tot

    c_tot_coste = ws2.cell(row=row_idx2, column=6, value=f"={sum_coste}")
    c_tot_coste.font = font_tot
    c_tot_coste.alignment = Alignment(horizontal="right", vertical="center")
    c_tot_coste.number_format = "#,##0.00 €"
    c_tot_coste.border = border_total
    c_tot_coste.fill = fill_tot

    ws2.cell(row=row_idx2, column=7, value="").border = border_total
    ws2.cell(row=row_idx2, column=7).fill = fill_tot

    c_tot_venta = ws2.cell(row=row_idx2, column=8, value=f"={sum_venta}")
    c_tot_venta.font = font_tot
    c_tot_venta.alignment = Alignment(horizontal="right", vertical="center")
    c_tot_venta.number_format = "#,##0.00 €"
    c_tot_venta.border = border_total
    c_tot_venta.fill = fill_tot

    c_tot_mrg = ws2.cell(row=row_idx2, column=9, value=f"={sum_mrg}")
    c_tot_mrg.font = font_title
    c_tot_mrg.alignment = Alignment(horizontal="right", vertical="center")
    c_tot_mrg.number_format = "#,##0.00 €"
    c_tot_mrg.border = border_total
    c_tot_mrg.fill = fill_tot
    ws2.row_dimensions[row_idx2].height = 24

    # Ajustar anchos de columnas
    col_widths1 = [12, 50, 8, 14, 18, 18, 25]
    for i, w in enumerate(col_widths1, start=1):
        ws1.column_dimensions[get_column_letter(i)].width = w

    col_widths2 = [12, 45, 8, 12, 16, 16, 16, 16, 16]
    for i, w in enumerate(col_widths2, start=1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    excel_path = os.path.join(BASE_DIR, f"Presupuesto_{DATA['codigo'].replace('-', '_')}_Nuevo_Edificio_Juzgados_Ciutadella_Grupo_Ortiz.xlsx")
    wb.save(excel_path)
    print(f"Excel guardado en: {excel_path}")
    return excel_path

# -------------------------------------------------------------------------
# GENERACIÓN DE HTML CLIENTE
# -------------------------------------------------------------------------
def create_html_cliente():
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Oferta Económica · {DATA['codigo']} · {DATA['proyecto']['titulo']}</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 14mm 12mm 14mm 12mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #f1f5f9;
    margin: 0;
    padding: 20px;
    font-size: 11px;
    line-height: 1.4;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    background: #ffffff;
    padding: 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-radius: 6px;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 16px;
    margin-bottom: 20px;
  }}
  .logo-box {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .logo-box img {{
    height: 48px;
  }}
  .company-title {{
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
  }}
  .company-sub {{
    font-size: 10px;
    color: #64748b;
  }}
  .doc-info {{
    text-align: right;
  }}
  .doc-badge {{
    display: inline-block;
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 4px;
  }}
  .doc-date {{
    font-size: 10px;
    color: #64748b;
  }}
  .grid-info {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 20px;
  }}
  .card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 12px 14px;
  }}
  .card-title {{
    font-size: 10.5px;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
  }}
  .field-row {{
    display: flex;
    margin-bottom: 4px;
  }}
  .field-lbl {{
    width: 100px;
    color: #64748b;
    font-weight: 600;
    font-size: 10px;
  }}
  .field-val {{
    flex: 1;
    color: #0f172a;
    font-size: 10px;
  }}
  .field-val strong {{
    color: #0f172a;
  }}
  table.items-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 14px;
    margin-bottom: 20px;
  }}
  table.items-table th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    font-size: 9.5px;
    padding: 8px 6px;
    text-align: left;
    border: 1px solid #0f172a;
  }}
  table.items-table td {{
    border: 1px solid #e2e8f0;
    padding: 7px 6px;
    font-size: 10px;
    vertical-align: middle;
  }}
  tr.cap-row td {{
    background: #e2e8f0;
    font-weight: 800;
    color: #0f172a;
    font-size: 10.5px;
    padding: 7px 8px;
    border-top: 1.5px solid #cbd5e1;
  }}
  tr.item-row:nth-child(even) {{
    background: #f8fafc;
  }}
  .text-center {{ text-align: center; }}
  .text-right {{ text-align: right; }}
  .font-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; }}
  .totals-box {{
    margin-left: auto;
    width: 340px;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 20px;
  }}
  .total-row {{
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    font-size: 11px;
  }}
  .total-row.grand {{
    border-top: 2px solid #0f172a;
    margin-top: 6px;
    padding-top: 8px;
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
  }}
  .conditions {{
    background: #ffffff;
    border-left: 4px solid #b45309;
    padding: 10px 14px;
    background: #fef3c7;
    border-radius: 0 4px 4px 0;
    margin-bottom: 20px;
    font-size: 9.5px;
    color: #78350f;
  }}
  .conditions h4 {{
    margin: 0 0 4px 0;
    font-size: 10.5px;
    color: #92400e;
  }}
  .conditions ul {{
    margin: 0;
    padding-left: 16px;
  }}
  .signatures {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-top: 25px;
    padding-top: 15px;
    border-top: 1px dashed #cbd5e1;
  }}
  .sig-block {{
    text-align: center;
  }}
  .sig-space {{
    height: 55px;
  }}
  .sig-name {{
    font-weight: 700;
    font-size: 10px;
    color: #0f172a;
  }}
  .sig-role {{
    font-size: 9px;
    color: #64748b;
  }}
  @media print {{
    body {{ background: #ffffff; padding: 0; font-size: 10px; }}
    .container {{ box-shadow: none; padding: 0; max-width: 100%; }}
    .page-break {{ page-break-before: always; }}
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="logo-box">
      <img src="logo-ham.svg" alt="HAM Logo">
      <div>
        <div class="company-title">{DATA['emisor']['empresa']}</div>
        <div class="company-sub">{DATA['emisor']['marca_comercial']} · CIF: {DATA['emisor']['cif']} · Menorca (Illes Balears)</div>
      </div>
    </div>
    <div class="doc-info">
      <div class="doc-badge">PRESUPUESTO OFICIAL {DATA['codigo']}</div>
      <div class="doc-date">Fecha: <strong>{DATA['fecha']}</strong> · Ref: {DATA['referencia']}</div>
    </div>
  </div>

  <div class="grid-info">
    <div class="card">
      <div class="card-title">Datos del Cliente / Contratista</div>
      <div class="field-row"><div class="field-lbl">Empresa:</div><div class="field-val"><strong>{DATA['cliente']['empresa']}</strong></div></div>
      <div class="field-row"><div class="field-lbl">Atención:</div><div class="field-val"><strong>{DATA['cliente']['contacto']}</strong> ({DATA['cliente']['cargo']})</div></div>
      <div class="field-row"><div class="field-lbl">Contacto:</div><div class="field-val">{DATA['cliente']['telefono']} · {DATA['cliente']['email']}</div></div>
      <div class="field-row"><div class="field-lbl">Sede:</div><div class="field-val">{DATA['cliente']['direccion']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}</div></div>
    </div>
    <div class="card">
      <div class="card-title">Datos del Proyecto y Licitación</div>
      <div class="field-row"><div class="field-lbl">Proyecto:</div><div class="field-val"><strong>{DATA['proyecto']['titulo']}</strong></div></div>
      <div class="field-row"><div class="field-lbl">Expediente:</div><div class="field-val"><strong>{DATA['proyecto']['expediente']}</strong></div></div>
      <div class="field-row"><div class="field-lbl">Ubicación:</div><div class="field-val">{DATA['proyecto']['emplazamiento']}</div></div>
      <div class="field-row"><div class="field-lbl">Promotor:</div><div class="field-val">{DATA['proyecto']['promotor']}</div></div>
    </div>
  </div>

  <table class="items-table">
    <thead>
      <tr>
        <th style="width: 8%;" class="text-center">CÓDIGO</th>
        <th style="width: 52%;">RESUMEN DE PARTIDA / DESCRIPCIÓN</th>
        <th style="width: 6%;" class="text-center">UD</th>
        <th style="width: 10%;" class="text-right">CANTIDAD</th>
        <th style="width: 11%;" class="text-right">PRECIO UNIT.</th>
        <th style="width: 13%;" class="text-right">IMPORTE</th>
      </tr>
    </thead>
    <tbody>
"""
    for cap in DATA["capitulos"]:
        html_content += f"""      <tr class="cap-row">
        <td colspan="6">{cap['codigo']} · {cap['titulo']}</td>
      </tr>
"""
        for p in cap["partidas"]:
            html_content += f"""      <tr class="item-row">
        <td class="text-center font-mono">{p['codigo']}</td>
        <td>
          <strong>{p['descripcion_corta']}</strong><br>
          <span style="font-size: 8.5px; color: #475569;">{p['descripcion_completa']}</span>
        </td>
        <td class="text-center">{p['unidad']}</td>
        <td class="text-right font-mono">{num(p['cantidad'])}</td>
        <td class="text-right font-mono">{eur(p['precio_unitario_venta'])}</td>
        <td class="text-right font-mono"><strong>{eur(p['importe_total_venta'])}</strong></td>
      </tr>
"""
    html_content += f"""    </tbody>
  </table>

  <div class="totals-box">
    <div class="total-row">
      <span>BASE IMPONIBLE (VENTA):</span>
      <span class="font-mono"><strong>{eur(DATA['totales']['base_imponible_venta'])}</strong></span>
    </div>
    <div class="total-row">
      <span>I.V.A. Repercutible ({DATA['totales']['iva_tipo']}%):</span>
      <span class="font-mono">{eur(DATA['totales']['iva_importe'])}</span>
    </div>
    <div class="total-row grand">
      <span>TOTAL PRESUPUESTO:</span>
      <span class="font-mono">{eur(DATA['totales']['total_con_iva'])}</span>
    </div>
  </div>

  <div class="conditions">
    <h4>Condiciones Técnicas y de Ejecución (Estándar HAM Menorca)</h4>
    <ul>
      <li><strong>Tratamiento de Pintura:</strong> Según directriz estricta de HAM, la pintura <em>NUNCA es al horno</em>. Todos los tratamientos se realizan mediante desengrasado, preparación mecánica superficial, imprimación de adherencia antioxidante y esmalte poliuretano bicomponente para exteriores en obra.</li>
      <li><strong>Fabricación y Montaje:</strong> Fabricación íntegra en taller en Menorca con medios propios, garantizando marcado CE y trazabilidad UNE-EN 1090-2 (EXC2/EXC3) y Código Estructural.</li>
      <li><strong>Transporte y Logística:</strong> Material despiezado y estructurado para transporte directo a obra en Ciutadella de Menorca.</li>
      <li><strong>Validez de la Oferta:</strong> {DATA['validez_dias']} días naturales desde su emisión.</li>
    </ul>
  </div>

  <div class="signatures">
    <div class="sig-block">
      <div class="sig-name">Por DIXIS RECURSOS Y SOLUCIONES S.L. (HAM)</div>
      <div class="sig-space"></div>
      <div class="sig-role">D. Pablo Sebastián Sánchez Arnoletto<br>Administrador Solidario</div>
    </div>
    <div class="sig-block">
      <div class="sig-name">Conforme y Aceptado por GRUPO ORTIZ</div>
      <div class="sig-space"></div>
      <div class="sig-role">Firma y Sello de Aceptación<br>Fecha: _____ / _____ / 2026</div>
    </div>
  </div>
</div>
</body>
</html>
"""
    html_path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Cliente generado en: {html_path}")
    return html_path

# -------------------------------------------------------------------------
# GENERACIÓN DE HTML INTERNO TÉCNICO (CONFIDENCIAL)
# -------------------------------------------------------------------------
def create_html_interno():
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Estudio Técnico Interno · {DATA['codigo']} · {DATA['proyecto']['titulo']}</title>
<style>
  @page {{
    size: A4 landscape;
    margin: 12mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #f1f5f9;
    margin: 0;
    padding: 20px;
    font-size: 11px;
  }}
  .container {{
    max-width: 1150px;
    margin: 0 auto;
    background: #ffffff;
    padding: 26px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-radius: 6px;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }}
  .title {{
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
  }}
  .confidential-badge {{
    background: #dc2626;
    color: #ffffff;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11px;
    letter-spacing: 0.5px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 20px;
  }}
  th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    font-size: 9.5px;
    padding: 8px 6px;
    text-align: left;
    border: 1px solid #0f172a;
  }}
  td {{
    border: 1px solid #e2e8f0;
    padding: 6px;
    font-size: 9.5px;
    vertical-align: middle;
  }}
  tr.cap-row td {{
    background: #e2e8f0;
    font-weight: 800;
    color: #0f172a;
    font-size: 10px;
  }}
  tr.item-row:nth-child(even) {{
    background: #f8fafc;
  }}
  .text-center {{ text-align: center; }}
  .text-right {{ text-align: right; }}
  .font-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 18px;
  }}
  .kpi-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px;
    text-align: center;
  }}
  .kpi-val {{
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 4px;
  }}
  .kpi-lbl {{
    font-size: 9.5px;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
  }}
  .kpi-mrg {{ color: #16a34a; }}
  @media print {{
    body {{ background: #ffffff; padding: 0; }}
    .container {{ box-shadow: none; padding: 0; max-width: 100%; }}
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <div class="title">INFORME TÉCNICO INTERNO DE COSTES Y RENTABILIDAD</div>
      <div style="font-size: 10.5px; color: #64748b;">EXPEDIENTE {DATA['codigo']} · {DATA['proyecto']['titulo']} · Grupo Ortiz</div>
    </div>
    <div class="confidential-badge">USO ESTRICTAMENTE INTERNO</div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-lbl">Coste Directo Total</div>
      <div class="kpi-val font-mono">{eur(DATA['totales']['total_coste_directo'])}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-lbl">Venta Base Imponible</div>
      <div class="kpi-val font-mono">{eur(DATA['totales']['base_imponible_venta'])}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-lbl">Margen Bruto (€)</div>
      <div class="kpi-val font-mono kpi-mrg">+{eur(DATA['totales']['margen_bruto_euros'])}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-lbl">Margen s/ Venta (%)</div>
      <div class="kpi-val font-mono kpi-mrg">{DATA['totales']['margen_bruto_porcentaje']}%</div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width: 8%;" class="text-center">CÓDIGO</th>
        <th style="width: 32%;">CONCEPTO</th>
        <th style="width: 5%;" class="text-center">UD</th>
        <th style="width: 9%;" class="text-right">CANTIDAD</th>
        <th style="width: 11%;" class="text-right">COSTE UNIT.</th>
        <th style="width: 11%;" class="text-right">COSTE TOTAL</th>
        <th style="width: 11%;" class="text-right">VENTA UNIT.</th>
        <th style="width: 11%;" class="text-right">VENTA TOTAL</th>
        <th style="width: 12%;" class="text-right">MARGEN (€)</th>
      </tr>
    </thead>
    <tbody>
"""
    for cap in DATA["capitulos"]:
        html_content += f"""      <tr class="cap-row">
        <td colspan="9">{cap['codigo']} · {cap['titulo']}</td>
      </tr>
"""
        for p in cap["partidas"]:
            mrg_p = p['importe_total_venta'] - p['coste_total']
            html_content += f"""      <tr class="item-row">
        <td class="text-center font-mono">{p['codigo']}</td>
        <td><strong>{p['descripcion_corta']}</strong></td>
        <td class="text-center">{p['unidad']}</td>
        <td class="text-right font-mono">{num(p['cantidad'])}</td>
        <td class="text-right font-mono">{eur(p['coste_unitario'])}</td>
        <td class="text-right font-mono">{eur(p['coste_total'])}</td>
        <td class="text-right font-mono">{eur(p['precio_unitario_venta'])}</td>
        <td class="text-right font-mono"><strong>{eur(p['importe_total_venta'])}</strong></td>
        <td class="text-right font-mono" style="color: #16a34a;"><strong>+{eur(mrg_p)}</strong></td>
      </tr>
"""
    html_content += f"""    </tbody>
    <tfoot>
      <tr style="background: #fef3c7; font-weight: 800; border-top: 2px solid #0f172a;">
        <td colspan="5" class="text-right">TOTALES GENERALES:</td>
        <td class="text-right font-mono">{eur(DATA['totales']['total_coste_directo'])}</td>
        <td></td>
        <td class="text-right font-mono">{eur(DATA['totales']['base_imponible_venta'])}</td>
        <td class="text-right font-mono" style="color: #16a34a; font-size: 11px;">+{eur(DATA['totales']['margen_bruto_euros'])}</td>
      </tr>
    </tfoot>
  </table>
</div>
</body>
</html>
"""
    html_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Interno generado en: {html_path}")
    return html_path

# -------------------------------------------------------------------------
# GENERACIÓN DE CARTA DE COMPROMISO OFICIAL PARA GRUPO ORTIZ
# -------------------------------------------------------------------------
def create_carta_compromiso():
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Carta de Compromiso de Colaboración · Grupo Ortiz · Juzgados Ciutadella</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 20mm 18mm 20mm 18mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #f8fafc;
    margin: 0;
    padding: 24px;
    font-size: 11.5px;
    line-height: 1.6;
  }}
  .container {{
    max-width: 820px;
    margin: 0 auto;
    background: #ffffff;
    padding: 36px 42px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border-radius: 4px;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 14px;
    margin-bottom: 24px;
  }}
  .logo-box {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .logo-box img {{ height: 50px; }}
  .company-title {{ font-size: 16px; font-weight: 800; color: #0f172a; }}
  .company-sub {{ font-size: 9.5px; color: #64748b; }}
  .title-block {{
    text-align: center;
    margin-bottom: 24px;
  }}
  .doc-title {{
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }}
  .doc-sub {{
    font-size: 11px;
    color: #475569;
    font-weight: 600;
  }}
  .recipient-box {{
    background: #f1f5f9;
    border-left: 4px solid #0f172a;
    padding: 10px 14px;
    margin-bottom: 22px;
    font-size: 10.5px;
  }}
  .p-text {{
    text-align: justify;
    margin-bottom: 12px;
  }}
  .p-text strong {{ color: #0f172a; }}
  .cap-list {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 12px 18px;
    margin: 14px 0 20px 0;
  }}
  .cap-list ul {{
    margin: 0;
    padding-left: 20px;
  }}
  .cap-list li {{
    margin-bottom: 4px;
  }}
  .signatures {{
    margin-top: 40px;
    padding-top: 20px;
    display: grid;
    grid-template-columns: 1fr;
    text-align: center;
  }}
  .sig-space {{
    height: 70px;
  }}
  .sig-name {{
    font-weight: 800;
    font-size: 11px;
    color: #0f172a;
  }}
  .sig-details {{
    font-size: 10px;
    color: #475569;
  }}
  @media print {{
    body {{ background: #ffffff; padding: 0; font-size: 11px; }}
    .container {{ box-shadow: none; padding: 0; max-width: 100%; }}
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="logo-box">
      <img src="logo-ham.svg" alt="HAM Menorca">
      <div>
        <div class="company-title">{DATA['emisor']['empresa']}</div>
        <div class="company-sub">{DATA['emisor']['marca_comercial']} · CIF: {DATA['emisor']['cif']} · Sant Lluís (Menorca)</div>
      </div>
    </div>
    <div style="text-align: right; font-size: 10px; color: #64748b;">
      En Sant Lluís (Menorca), a {DATA['fecha']}
    </div>
  </div>

  <div class="title-block">
    <div class="doc-title">CARTA DE COMPROMISO DE COLABORACIÓN Y SUBCONTRATACIÓN</div>
    <div class="doc-sub">LICITACIÓN PÚBLICA: EXPTE AOB/2026/135</div>
  </div>

  <div class="recipient-box">
    <strong>A LA ATENCIÓN DE:</strong><br>
    <strong>GRUPO ORTIZ (Delegación Baleares - Rehabilitación)</strong><br>
    D. Damià Melià Vives · Avda. Ensanche de Vallecas, 44, 28051 Madrid<br>
    <strong>ÓRGANO DE CONTRATACIÓN:</strong> Ministerio de la Presidencia, Justicia y Relaciones con las Cortes.
  </div>

  <div class="p-text">
    D. <strong>{DATA['emisor']['representante_legal']}</strong>, mayor de edad, con DNI número <strong>{DATA['emisor']['dni']}</strong>, en calidad de <strong>{DATA['emisor']['cargo']}</strong> de la mercantil <strong>{DATA['emisor']['empresa']}</strong> (con nombre comercial <strong>{DATA['emisor']['marca_comercial']}</strong>), provista de CIF número <strong>{DATA['emisor']['cif']}</strong>, con domicilio fiscal en {DATA['emisor']['domicilio']}, C.P. {DATA['emisor']['codigo_postal']} de {DATA['emisor']['poblacion']} (Islas Baleares), inscrita debidamente en el Registro de Empresas Acreditadas (REA) en el sector de la construcción bajo la actividad principal CNAE 2511 (Fabricación de estructuras metálicas y sus componentes),
  </div>

  <div class="p-text">
    <strong>MANIFIESTA Y HACE CONSTAR:</strong>
  </div>

  <div class="p-text">
    <strong>PRIMERO.-</strong> Que tiene pleno conocimiento del proyecto de licitación para la <strong>«{DATA['proyecto']['titulo']}»</strong> (Expediente número <strong>{DATA['proyecto']['expediente']}</strong>), promovido por el Ministerio de Justicia con emplazamiento en {DATA['proyecto']['emplazamiento']}.
  </div>

  <div class="p-text">
    <strong>SEGUNDO.-</strong> Que la empresa <strong>{DATA['emisor']['empresa']}</strong> dispone de instalaciones industriales, capacidad técnica, medios humanos, maquinaria de taller y equipo cualificado de montaje homologado en la isla de Menorca para ejecutar con la máxima solvencia técnica los trabajos correspondientes a:
  </div>

  <div class="cap-list">
    <ul>
      <li><strong>Capítulo 05 · Estructura Metálica:</strong> Fabricación y montaje de estructura metálica tubular y perfiles laminados en caliente para lucernarios y cuelgues (5.791,54 kg totales de acero S275JR con marcado CE).</li>
      <li><strong>Capítulo 10 · Cerrajería:</strong> Barandillas tubulares interiores (81,80 m), pasamanos de acero (78,00 m), barandillas de vidrio laminar de seguridad con perfil continuo (73,27 m), caperuzas, cargaderos y rejillas.</li>
      <li><strong>Capítulo 26 · Urbanización:</strong> Cierre perimetral de parcela en chapa plegada de 6 mm con acabado efecto corten (112,36 m) y cancelas automáticas correderas (3,50 m y 2,02 m) y abatible (6,75 m) motorizadas.</li>
      <li><strong>Capítulo 07 y 08 · Revestimientos y Cubiertas:</strong> Entramados tipo Tramex galvanizados (20,95 m²) y albardillas de chapa lacada (90,09 m).</li>
      <li><strong>Capítulo 09 · Carpintería Metálica de Seguridad:</strong> Puertas de celda judicial blindadas abatibles y correderas con mirilla antibalas y trampilla.</li>
    </ul>
  </div>

  <div class="p-text">
    <strong>TERCERO.-</strong> Que mediante el presente documento formaliza su <strong>FIRME COMPROMISO DE COLABORACIÓN Y PARTICIPACIÓN</strong> con <strong>GRUPO ORTIZ</strong> para la ejecución de las unidades de obra citadas conforme a la oferta económica remitida (Presupuesto <strong>{DATA['codigo']}</strong> por importe de <strong>{eur(DATA['totales']['base_imponible_venta'])}</strong> + IVA), comprometiéndose formalmente a suscribir el correspondiente contrato de subcontratación en caso de que <strong>GRUPO ORTIZ</strong> resulte adjudicataria del citado expediente público.
  </div>

  <div class="p-text">
    Y para que conste y surta los efectos oportunos ante la Mesa de Contratación y la constructora solicitante, se firma la presente en Sant Lluís (Menorca).
  </div>

  <div class="signatures">
    <div class="sig-space"></div>
    <div class="sig-name">Por DIXIS RECURSOS Y SOLUCIONES S.L. (HAM)</div>
    <div class="sig-details">
      D. {DATA['emisor']['representante_legal']}<br>
      Administrador Solidario · CIF: {DATA['emisor']['cif']}
    </div>
  </div>
</div>
</body>
</html>
"""
    html_path = os.path.join(BASE_DIR, "Carta_Compromiso_Grupo_Ortiz_Juzgados_Ciutadella.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Carta de Compromiso generada en: {html_path}")
    return html_path

# -------------------------------------------------------------------------
# CONVERSIÓN A PDF CON CHROME HEADLESS
# -------------------------------------------------------------------------
def render_pdf(html_path, pdf_path, landscape=False):
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}"
    ]
    cmd.append(html_path)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"PDF generado con éxito: {pdf_path}")
    else:
        print(f"Error generando PDF {pdf_path}: {res.stderr}")

# -------------------------------------------------------------------------
# GENERACIÓN DE RESPUESTA EMAIL AL CLIENTE
# -------------------------------------------------------------------------
def create_email_draft():
    content = f"""# Borrador de Respuesta para Grupo Ortiz

**Para:** Damià Melià Vives (`damia.melia@grupoortiz.com`)  
**De:** Pablo Sánchez Arnoletto (`pablo@dixis.es` / `administracion@dixis.es`) · DIXIS / HAM Menorca  
**Asunto:** Oferta Económica y Carta de Compromiso · Nuevo Edificio Juzgados Ciutadella (EXPTE AOB/2026/135) - DIXIS / HAM

---

Estimado Damià,

En respuesta a su solicitud de colaboración para la licitación de las obras de **"Construcción de Nuevo Edificio de Juzgados en Ciutadella de Menorca (EXPTE AOB/2026/135)"**, desde **DIXIS Recursos y Soluciones S.L. (HAM Menorca)** nos complace remitirles nuestra oferta económica detallada y la Carta de Compromiso formal para su incorporación a la documentación de la propuesta.

Como taller especializado en herrería, calderería y estructuras metálicas con base y personal propio en Menorca, hemos estudiado exhaustivamente los capítulos de proyecto correspondientes a nuestra especialidad:

### Resumen de la Oferta ({DATA['codigo']})
- **Capítulo 05 · Estructura Metálica:** Lucernarios en perfiles tubulares SHS/RHS y laminados IPE, tensores y uniones ({num(DATA['capitulos'][0]['partidas'][0]['cantidad'] + DATA['capitulos'][0]['partidas'][1]['cantidad'])} kg S275JR) -> **{eur(DATA['capitulos'][0]['partidas'][0]['importe_total_venta'] + DATA['capitulos'][0]['partidas'][1]['importe_total_venta'])}**
- **Capítulo 10 · Cerrajería:** Cargaderos L-60.6 mm, caperuzas de chimenea, rejillas de ventilación de cámara, barandillas tubulares de barrotes h=110 cm ({num(DATA['capitulos'][1]['partidas'][3]['cantidad'])} m), pasamanos murales Ø40 mm ({num(DATA['capitulos'][1]['partidas'][4]['cantidad'])} m) y barandillas técnicas de vidrio laminar de seguridad 10+10+2,5 mm ({num(DATA['capitulos'][1]['partidas'][5]['cantidad'])} m) -> **{eur(sum(p['importe_total_venta'] for p in DATA['capitulos'][1]['partidas']))}**
- **Capítulo 26 · Urbanización (Cerramientos y Cancelas):** Vallado perimetral en chapa de 6 mm plegada con acabado efecto corten ({num(DATA['capitulos'][4]['partidas'][0]['cantidad'])} m) y tres cancelas automáticas motorizadas (correderas de 3,50 m y 2,02 m y abatible de gran vano de 6,75 m) -> **{eur(sum(p['importe_total_venta'] for p in DATA['capitulos'][4]['partidas']))}**
- **Capítulo 07 y 08 · Revestimientos y Cubiertas:** Entramado metálico tipo Tramex galvanizado ({num(DATA['capitulos'][2]['partidas'][0]['cantidad'])} m²) y albardillas de chapa lacada desarrollo 50 cm ({num(DATA['capitulos'][3]['partidas'][0]['cantidad'])} m) -> **{eur(DATA['capitulos'][2]['partidas'][0]['importe_total_venta'] + DATA['capitulos'][3]['partidas'][0]['importe_total_venta'])}**
- **Capítulo 09 · Carpintería Metálica de Seguridad (Celdas):** Puertas blindadas de seguridad para celdas de 2 chapas de acero de 2 mm con mirilla antibalas y trampillas (abatibles y correderas con casoneto) -> **{eur(sum(p['importe_total_venta'] for p in DATA['capitulos'][5]['partidas']))}**

---
- **TOTAL BASE IMPONIBLE:** **{eur(DATA['totales']['base_imponible_venta'])}**
- **I.V.A. (21%):** {eur(DATA['totales']['iva_importe'])}
- **TOTAL OFERTA:** **{eur(DATA['totales']['total_con_iva'])}**

### Documentación Adjunta:
1. `Presupuesto_{DATA['codigo'].replace('-', '_')}_Nuevo_Edificio_Juzgados_Ciutadella_Grupo_Ortiz.xlsx`: Libro Excel completo con desglose de precios unitarios y mediciones.
2. `presupuesto-cliente.pdf`: Oferta comercial formalizada en formato PDF.
3. `Carta_Compromiso_Grupo_Ortiz_Juzgados_Ciutadella.pdf`: Carta oficial de compromiso de colaboración y subcontratación debidamente emitida y firmada por nuestro administrador solidario.

Quedamos a su entera disposición para cualquier aclaración técnica o ajuste que precisen.

Atentamente,

**Pablo Sebastián Sánchez Arnoletto**  
*Administrador Solidario*  
**Dixis Recursos y Soluciones S.L. (HAM Menorca)**  
Tel: +34 669 769 541 · `pablo@dixis.es`  
`www.hamenorca.com`
"""
    email_path = os.path.join(BASE_DIR, "respuesta-email-cliente.md")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Borrador de email generado en: {email_path}")
    return email_path

# -------------------------------------------------------------------------
# GENERACIÓN DE README.MD
# -------------------------------------------------------------------------
def create_readme():
    content = f"""# Presupuesto {DATA['codigo']} · Nuevo Edificio de Juzgados de Ciutadella de Menorca

- **Código:** `{DATA['codigo']}`
- **Referencia:** `{DATA['referencia']}`
- **Fecha de Emisión:** {DATA['fecha']}
- **Fecha Límite:** {DATA['fecha_entrega_limite']}
- **Cliente:** {DATA['cliente']['empresa']}
- **Atención:** {DATA['cliente']['contacto']} ({DATA['cliente']['cargo']})
- **Teléfonos:** {DATA['cliente']['telefono']} · {DATA['cliente']['email']}
- **Sede:** {DATA['cliente']['direccion']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}
- **Proyecto:** {DATA['proyecto']['titulo']}
- **Expediente:** {DATA['proyecto']['expediente']}
- **Emplazamiento:** {DATA['proyecto']['emplazamiento']}
- **Promotor:** {DATA['proyecto']['promotor']}

---

## Resumen Económico Consolidado

| Capítulo | Concepto | Coste Directo (€) | Venta Base Imponible (€) | Margen Bruto (€) | % Margen |
|---|---|---:|---:|---:|---:|
| **CAP_05** | Estructura Metálica (Lucernarios y cuelgues IPE/tubulares) | 19.775,98 € | 28.395,00 € | +8.619,02 € | 30,35% |
| **CAP_10** | Cerrajería (Barandillas barrotes, pasamanos, vidrio y cargaderos) | 33.183,45 € | 48.958,45 € | +15.775,00 € | 32,22% |
| **CAP_07** | Revestimientos (Entramado tipo Tramex galvanizado) | 1.676,00 € | 2.681,60 € | +1.005,60 € | 37,50% |
| **CAP_08** | Cubiertas (Albardilla chapa lacada desarrollo 50 cm) | 2.522,52 € | 4.054,05 € | +1.531,53 € | 37,78% |
| **CAP_26** | Urbanización (Vallado chapa 6 mm efecto corten y cancelas automáticas) | 58.717,60 € | 85.754,20 € | +27.036,60 € | 31,53% |
| **CAP_09** | Carpintería Seguridad (Puertas blindadas celdas abatibles y correderas) | 9.400,00 € | 14.160,00 € | +4.760,00 € | 33,62% |
| **TOTALES** | **Conjunto de Partidas Especializadas HAM** | **{eur(DATA['totales']['total_coste_directo'])}** | **{eur(DATA['totales']['base_imponible_venta'])}** | **+{eur(DATA['totales']['margen_bruto_euros'])}** | **{DATA['totales']['margen_bruto_porcentaje']}%** |

- **I.V.A. Repercutible (21.0%):** {eur(DATA['totales']['iva_importe'])}
- **Total Presupuesto (con IVA):** **{eur(DATA['totales']['total_con_iva'])}**

---

## Archivos del Expediente

- [Presupuesto_{DATA['codigo'].replace('-', '_')}_Nuevo_Edificio_Juzgados_Ciutadella_Grupo_Ortiz.xlsx](file:///{BASE_DIR.replace('\\', '/')}/Presupuesto_{DATA['codigo'].replace('-', '_')}_Nuevo_Edificio_Juzgados_Ciutadella_Grupo_Ortiz.xlsx): Libro Excel completo con 2 pestañas (Oferta Comercial y Escandallo Interno).
- [presupuesto-cliente.pdf](file:///{BASE_DIR.replace('\\', '/')}/presupuesto-cliente.pdf): Oferta oficial en PDF para Grupo Ortiz.
- [presupuesto-cliente.html](file:///{BASE_DIR.replace('\\', '/')}/presupuesto-cliente.html): Versión interactiva para navegador.
- [presupuesto-interno-tecnico.pdf](file:///{BASE_DIR.replace('\\', '/')}/presupuesto-interno-tecnico.pdf): Estudio confidencial interno de costes y márgenes.
- [Carta_Compromiso_Grupo_Ortiz_Juzgados_Ciutadella.pdf](file:///{BASE_DIR.replace('\\', '/')}/Carta_Compromiso_Grupo_Ortiz_Juzgados_Ciutadella.pdf): Carta de compromiso oficial de colaboración/subcontratación para licitación pública.
- [respuesta-email-cliente.md](file:///{BASE_DIR.replace('\\', '/')}/respuesta-email-cliente.md): Borrador de email para responder a Damià Melià Vives.
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"README.md generado en: {readme_path}")
    return readme_path

# -------------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("Iniciando generación de documentos para P-2026-0066...")
    excel_file = create_excel()
    html_cli = create_html_cliente()
    html_int = create_html_interno()
    html_cart = create_carta_compromiso()

    pdf_cli = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    pdf_int = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")
    pdf_cart = os.path.join(BASE_DIR, "Carta_Compromiso_Grupo_Ortiz_Juzgados_Ciutadella.pdf")

    render_pdf(html_cli, pdf_cli)
    render_pdf(html_int, pdf_int)
    render_pdf(html_cart, pdf_cart)

    create_email_draft()
    create_readme()

    # Copiar archivos a la carpeta de Grupo Ortiz en O:
    if os.path.exists(NETWORK_DIR):
        print(f"Copiando archivos generados a {NETWORK_DIR}...")
        for src in [excel_file, pdf_cli, pdf_cart]:
            dest = os.path.join(NETWORK_DIR, os.path.basename(src))
            shutil.copy2(src, dest)
            print(f"  Copiado: {os.path.basename(src)}")

    print("Proceso completado exitosamente.")
