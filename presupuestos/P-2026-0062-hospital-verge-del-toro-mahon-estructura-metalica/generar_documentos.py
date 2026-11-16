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

def fmt_eur(val):
    if val is None:
        return "0,00 €"
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_num(val, dec=2):
    if val is None:
        return "0,00"
    return f"{val:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def convert_html_to_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    print(f"Generando PDF desde: {html_path} -> {pdf_path}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error generando PDF: {res.stderr}")
    else:
        print(f"PDF generado correctamente: {pdf_path}")

def create_excel():
    wb = Workbook()

    NAVY = "0F172A"
    BLUE = "0284C7"
    DARK_BLUE = "0369A1"
    GOLD = "B45309"
    LIGHT_BG = "F8FAFC"
    SUB_BG = "E2E8F0"
    TOTAL_BG = "FEF3C7"
    GREEN_TXT = "15803D"
    WHITE = "FFFFFF"

    f_navy = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    f_sub = PatternFill(start_color=SUB_BG, end_color=SUB_BG, fill_type="solid")
    f_alt = PatternFill(start_color=LIGHT_BG, end_color=LIGHT_BG, fill_type="solid")
    f_tot = PatternFill(start_color=TOTAL_BG, end_color=TOTAL_BG, fill_type="solid")
    f_gold = PatternFill(start_color="FFFBEB", end_color="FFFBEB", fill_type="solid")

    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_brand = Font(name="Segoe UI", size=9.5, bold=True, color=DARK_BLUE)
    font_hdr = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color=NAVY)
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_italic = Font(name="Segoe UI", size=8, italic=True, color="64748B")
    font_tot = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=10.5, bold=True, color=GOLD)
    font_green = Font(name="Segoe UI", size=9, bold=True, color=GREEN_TXT)

    b_thin = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )
    b_tot = Border(
        top=Side(style="thin", color=NAVY),
        bottom=Side(style="double", color=NAVY)
    )

    NUM_EUR = '#,##0.00 "€"'
    NUM_QTY = "#,##0.00"
    NUM_PCT = "0.00%"

    # -------------------------------------------------------------
    # HOJA 1: RESUMEN EJECUTIVO
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Resumen Ejecutivo"
    ws1.views.sheetView[0].showGridLines = True

    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. · HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_brand
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} · {DATA['referencia']}"
    ws1["B3"].font = font_title
    ws1["B4"] = f"{DATA['proyecto']['obra']} · {DATA['proyecto']['capitulo_codigo']} {DATA['proyecto']['capitulo_nombre']}"
    ws1["B4"].font = font_sec

    ws1["B6"] = "DATOS DEL CLIENTE / LICITACIÓN"
    ws1["B6"].font = font_bold
    ws1["B7"] = "Cliente:"
    ws1["C7"] = DATA["cliente"]["empresa"]
    ws1["B8"] = "Atención:"
    ws1["C8"] = f"{DATA['cliente']['contacto']} ({DATA['cliente']['cargo']})"
    ws1["B9"] = "Emplazamiento:"
    ws1["C9"] = DATA["proyecto"]["emplazamiento"]
    ws1["B10"] = "Promotor Oficial:"
    ws1["C10"] = DATA["proyecto"]["promotor"]
    for r in range(7, 11):
        ws1[f"B{r}"].font = font_italic
        ws1[f"C{r}"].font = font_bold

    ws1["E6"] = "DATOS DE LA OFERTA"
    ws1["E6"].font = font_bold
    ws1["E7"] = "Fecha de Emisión:"
    ws1["F7"] = DATA["fecha"]
    ws1["E8"] = "Validez Oferta:"
    ws1["F8"] = f"{DATA['validez_dias']} días naturales"
    ws1["E9"] = "Normativa y Clase:"
    ws1["F9"] = "Código Estructural · UNE-EN 1090-2 (EXC3 / EXC2)"
    ws1["E10"] = "Forma de Pago:"
    ws1["F10"] = "Certificaciones mensuales por avance aprobado"
    for r in range(7, 11):
        ws1[f"E{r}"].font = font_italic
        ws1[f"F{r}"].font = font_bold

    row = 13
    headers1 = ["Cód.", "Subcapítulo / Partida Resumida", "Unidad", "Cantidad", "Precio (€)", "Importe Venta (€)"]
    cols1 = ["B", "C", "D", "E", "F", "G"]
    for c, h in zip(cols1, headers1):
        cell = ws1[f"{c}{row}"]
        cell.value = h
        cell.font = font_hdr
        cell.fill = f_navy
        cell.alignment = Alignment(horizontal="center" if c in ["B", "D"] else "left" if c == "C" else "right", vertical="center")
    row += 1

    for sub in DATA["subcapitulos"]:
        ws1[f"B{row}"] = sub["codigo"]
        ws1[f"C{row}"] = f"SUBCAPÍTULO {sub['codigo']} - {sub['nombre']}"
        ws1[f"G{row}"] = sub["subtotal_venta"]
        ws1[f"G{row}"].number_format = NUM_EUR
        for c in cols1:
            ws1[f"{c}{row}"].font = font_bold
            ws1[f"{c}{row}"].fill = f_sub
            ws1[f"{c}{row}"].border = b_thin
        row += 1

        for p in sub["partidas"]:
            ws1[f"B{row}"] = p["codigo"]
            ws1[f"C{row}"] = p["resumen"]
            ws1[f"D{row}"] = p["unidad"]
            ws1[f"E{row}"] = p["cantidad"]
            ws1[f"F{row}"] = p["precio_venta_unitario"]
            ws1[f"G{row}"] = p["importe_venta"]

            ws1[f"B{row}"].alignment = Alignment(horizontal="center")
            ws1[f"D{row}"].alignment = Alignment(horizontal="center")
            ws1[f"E{row}"].number_format = NUM_QTY
            ws1[f"F{row}"].number_format = NUM_EUR
            ws1[f"G{row}"].number_format = NUM_EUR

            for c in cols1:
                ws1[f"{c}{row}"].font = font_reg
                ws1[f"{c}{row}"].border = b_thin
            row += 1

    row += 1
    ws1[f"B{row}"] = ""
    ws1[f"C{row}"] = "TOTAL BASE IMPONIBLE (VENTA)"
    ws1[f"C{row}"].font = font_tot
    ws1[f"G{row}"] = DATA["totales"]["base_imponible"]
    ws1[f"G{row}"].font = font_tot
    ws1[f"G{row}"].number_format = NUM_EUR
    for c in cols1:
        ws1[f"{c}{row}"].fill = f_tot
        ws1[f"{c}{row}"].border = b_tot

    row += 1
    ws1[f"C{row}"] = f"I.V.A. General ({DATA['totales']['iva_porcentaje']}%)"
    ws1[f"C{row}"].font = font_bold
    ws1[f"G{row}"] = DATA["totales"]["iva_importe"]
    ws1[f"G{row}"].font = font_bold
    ws1[f"G{row}"].number_format = NUM_EUR

    row += 1
    ws1[f"C{row}"] = "TOTAL PRESUPUESTO CON I.V.A."
    ws1[f"C{row}"].font = font_tot_gold
    ws1[f"G{row}"] = DATA["totales"]["total_con_iva"]
    ws1[f"G{row}"].font = font_tot_gold
    ws1[f"G{row}"].number_format = NUM_EUR
    for c in cols1:
        ws1[f"{c}{row}"].fill = f_gold
        ws1[f"{c}{row}"].border = b_tot

    ws1.column_dimensions["A"].width = 3
    ws1.column_dimensions["B"].width = 18
    ws1.column_dimensions["C"].width = 65
    ws1.column_dimensions["D"].width = 10
    ws1.column_dimensions["E"].width = 15
    ws1.column_dimensions["F"].width = 16
    ws1.column_dimensions["G"].width = 20

    # -------------------------------------------------------------
    # HOJA 2: MEDICIÓN Y PRESUPUESTO DETALLADO (LÍNEA A LÍNEA)
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Medición y Presupuesto")
    ws2.views.sheetView[0].showGridLines = True

    ws2["B2"] = "CAPÍTULO H06: ESTRUCTURA METÁLICA · MEDICIONES LÍNEA A LÍNEA"
    ws2["B2"].font = font_title
    ws2["B3"] = f"{DATA['proyecto']['titulo']}"
    ws2["B3"].font = font_italic

    row = 5
    cols2 = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    headers2 = ["Código", "Nat", "Ud", "Resumen / Comentario", "Nº", "Longitud", "Anchura", "Altura", "Cantidad", "CanPres", "Precio (€)", "Importe (€)"]
    for c, h in zip(cols2, headers2):
        cell = ws2[f"{c}{row}"]
        cell.value = h
        cell.font = font_hdr
        cell.fill = f_navy
        cell.alignment = Alignment(horizontal="center" if c in ["B", "C", "D"] else "left" if c == "E" else "right", vertical="center")
    row += 1

    for sub in DATA["subcapitulos"]:
        ws2[f"B{row}"] = sub["codigo"]
        ws2[f"C{row}"] = "Capítulo"
        ws2[f"E{row}"] = sub["nombre"]
        ws2[f"K{row}"] = 1
        ws2[f"L{row}"] = sub["subtotal_venta"]
        ws2[f"L{row}"].number_format = NUM_EUR
        for c in cols2:
            ws2[f"{c}{row}"].font = font_bold
            ws2[f"{c}{row}"].fill = f_sub
            ws2[f"{c}{row}"].border = b_thin
        row += 1

        for p in sub["partidas"]:
            ws2[f"B{row}"] = p["codigo"]
            ws2[f"C{row}"] = "Partida"
            ws2[f"D{row}"] = p["unidad"]
            ws2[f"E{row}"] = p["resumen"]
            ws2[f"J{row}"] = p["cantidad"]
            ws2[f"K{row}"] = p["precio_venta_unitario"]
            ws2[f"L{row}"] = p["importe_venta"]

            ws2[f"B{row}"].alignment = Alignment(horizontal="center")
            ws2[f"C{row}"].alignment = Alignment(horizontal="center")
            ws2[f"D{row}"].alignment = Alignment(horizontal="center")
            ws2[f"J{row}"].number_format = NUM_QTY
            ws2[f"K{row}"].number_format = NUM_EUR
            ws2[f"L{row}"].number_format = NUM_EUR

            for c in cols2:
                ws2[f"{c}{row}"].font = font_bold
                ws2[f"{c}{row}"].fill = f_alt
                ws2[f"{c}{row}"].border = b_thin
            row += 1

            # Descripción de la partida
            ws2[f"E{row}"] = p["descripcion"]
            ws2[f"E{row}"].font = font_italic
            ws2.row_dimensions[row].height = 40
            row += 1

            # Desglose de mediciones
            for m in p["mediciones"]:
                ws2[f"C{row}"] = "Spc0010"
                ws2[f"E{row}"] = m["comentario"]
                ws2[f"F{row}"] = m["n"]
                ws2[f"G{row}"] = m["longitud"]
                ws2[f"H{row}"] = m["anchura"]
                ws2[f"I{row}"] = m["altura"]
                ws2[f"J{row}"] = m["cantidad"]

                ws2[f"C{row}"].alignment = Alignment(horizontal="center")
                ws2[f"F{row}"].number_format = NUM_QTY
                ws2[f"G{row}"].number_format = NUM_QTY
                ws2[f"H{row}"].number_format = NUM_QTY
                ws2[f"I{row}"].number_format = NUM_QTY
                ws2[f"J{row}"].number_format = NUM_QTY

                for c in cols2:
                    ws2[f"{c}{row}"].font = font_reg
                    ws2[f"{c}{row}"].border = b_thin
                row += 1

            # Total Partida
            ws2[f"E{row}"] = f"Total {p['codigo']}"
            ws2[f"J{row}"] = p["cantidad"]
            ws2[f"K{row}"] = p["precio_venta_unitario"]
            ws2[f"L{row}"] = p["importe_venta"]

            ws2[f"E{row}"].alignment = Alignment(horizontal="right")
            ws2[f"J{row}"].number_format = NUM_QTY
            ws2[f"K{row}"].number_format = NUM_EUR
            ws2[f"L{row}"].number_format = NUM_EUR

            for c in cols2:
                ws2[f"{c}{row}"].font = font_bold
                ws2[f"{c}{row}"].border = b_thin
            row += 2

    ws2.column_dimensions["A"].width = 3
    ws2.column_dimensions["B"].width = 18
    ws2.column_dimensions["C"].width = 10
    ws2.column_dimensions["D"].width = 8
    ws2.column_dimensions["E"].width = 50
    ws2.column_dimensions["F"].width = 8
    ws2.column_dimensions["G"].width = 10
    ws2.column_dimensions["H"].width = 10
    ws2.column_dimensions["I"].width = 10
    ws2.column_dimensions["J"].width = 14
    ws2.column_dimensions["K"].width = 14
    ws2.column_dimensions["L"].width = 18

    # -------------------------------------------------------------
    # HOJA 3: ESTUDIO TÉCNICO DE COSTES HAM (CONFIDENCIAL)
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Estudio de Costes HAM")
    ws3.views.sheetView[0].showGridLines = True

    ws3["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. · ANÁLISIS CONFIDENCIAL DE COSTES Y RENTABILIDAD"
    ws3["B2"].font = font_brand
    ws3["B3"] = f"ESTUDIO TÉCNICO ECONÓMICO HAM · EXPEDIENTE {DATA['codigo']}"
    ws3["B3"].font = font_title

    row = 5
    headers3 = ["Cód.", "Partida Presupuestaria", "Ud.", "Cantidad", "Coste Ud. (€)", "Coste Directo (€)", "Venta Ud. (€)", "Importe Venta (€)", "Margen (€)", "% Margen"]
    cols3 = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    for c, h in zip(cols3, headers3):
        cell = ws3[f"{c}{row}"]
        cell.value = h
        cell.font = font_hdr
        cell.fill = f_navy
        cell.alignment = Alignment(horizontal="center" if c in ["B", "D"] else "left" if c == "C" else "right", vertical="center")
    row += 1

    for sub in DATA["subcapitulos"]:
        ws3[f"B{row}"] = sub["codigo"]
        ws3[f"C{row}"] = f"SUBCAPÍTULO {sub['codigo']} - {sub['nombre']}"
        ws3[f"G{row}"] = sub["subtotal_coste"]
        ws3[f"I{row}"] = sub["subtotal_venta"]
        ws3[f"J{row}"] = sub["subtotal_margen"]
        ws3[f"K{row}"] = sub["subtotal_margen_porcentaje"] / 100.0

        ws3[f"G{row}"].number_format = NUM_EUR
        ws3[f"I{row}"].number_format = NUM_EUR
        ws3[f"J{row}"].number_format = NUM_EUR
        ws3[f"K{row}"].number_format = NUM_PCT

        for c in cols3:
            ws3[f"{c}{row}"].font = font_bold
            ws3[f"{c}{row}"].fill = f_sub
            ws3[f"{c}{row}"].border = b_thin
        row += 1

        for p in sub["partidas"]:
            ws3[f"B{row}"] = p["codigo"]
            ws3[f"C{row}"] = p["resumen"]
            ws3[f"D{row}"] = p["unidad"]
            ws3[f"E{row}"] = p["cantidad"]
            ws3[f"F{row}"] = p["coste_unitario"]
            ws3[f"G{row}"] = p["importe_coste"]
            ws3[f"H{row}"] = p["precio_venta_unitario"]
            ws3[f"I{row}"] = p["importe_venta"]
            ws3[f"J{row}"] = p["margen_bruto"]
            ws3[f"K{row}"] = p["margen_porcentaje"] / 100.0

            ws3[f"B{row}"].alignment = Alignment(horizontal="center")
            ws3[f"D{row}"].alignment = Alignment(horizontal="center")
            ws3[f"E{row}"].number_format = NUM_QTY
            ws3[f"F{row}"].number_format = NUM_EUR
            ws3[f"G{row}"].number_format = NUM_EUR
            ws3[f"H{row}"].number_format = NUM_EUR
            ws3[f"I{row}"].number_format = NUM_EUR
            ws3[f"J{row}"].number_format = NUM_EUR
            ws3[f"K{row}"].number_format = NUM_PCT

            for c in cols3:
                ws3[f"{c}{row}"].font = font_reg
                ws3[f"{c}{row}"].border = b_thin
            row += 1

    row += 1
    ws3[f"C{row}"] = "TOTALES DE PRODUCCIÓN HAM"
    ws3[f"C{row}"].font = font_tot
    ws3[f"G{row}"] = DATA["totales"]["coste_directo_total"]
    ws3[f"I{row}"] = DATA["totales"]["base_imponible"]
    ws3[f"J{row}"] = DATA["totales"]["margen_bruto_total"]
    ws3[f"K{row}"] = DATA["totales"]["margen_porcentaje_sobre_venta"] / 100.0

    ws3[f"G{row}"].font = font_tot
    ws3[f"I{row}"].font = font_tot
    ws3[f"J{row}"].font = font_green
    ws3[f"K{row}"].font = font_green

    ws3[f"G{row}"].number_format = NUM_EUR
    ws3[f"I{row}"].number_format = NUM_EUR
    ws3[f"J{row}"].number_format = NUM_EUR
    ws3[f"K{row}"].number_format = NUM_PCT

    for c in cols3:
        ws3[f"{c}{row}"].fill = f_tot
        ws3[f"{c}{row}"].border = b_tot

    ws3.column_dimensions["A"].width = 3
    ws3.column_dimensions["B"].width = 18
    ws3.column_dimensions["C"].width = 55
    ws3.column_dimensions["D"].width = 8
    ws3.column_dimensions["E"].width = 14
    ws3.column_dimensions["F"].width = 14
    ws3.column_dimensions["G"].width = 18
    ws3.column_dimensions["H"].width = 14
    ws3.column_dimensions["I"].width = 18
    ws3.column_dimensions["J"].width = 16
    ws3.column_dimensions["K"].width = 12

    excel_file = os.path.join(BASE_DIR, "Presupuesto_P2026_0062_Hospital_Verge_del_Toro_Estructura.xlsx")
    wb.save(excel_file)
    print(f"Excel guardado en: {excel_file}")
    return excel_file

def create_html_client():
    subcaps_html = ""
    for sub in DATA["subcapitulos"]:
        partidas_rows = ""
        for p in sub["partidas"]:
            partidas_rows += f"""
            <tr class="item-row">
              <td class="code">{p['codigo']}</td>
              <td class="desc">
                <strong>{p['resumen']}</strong>
                <p class="partida-desc">{p['descripcion']}</p>
              </td>
              <td class="center unit">{p['unidad']}</td>
              <td class="right qty">{fmt_num(p['cantidad'])}</td>
              <td class="right price">{fmt_eur(p['precio_venta_unitario'])}</td>
              <td class="right amount">{fmt_eur(p['importe_venta'])}</td>
            </tr>
            """
        subcaps_html += f"""
        <div class="subchapter-block">
          <div class="subchapter-header">
            <h3>SUBCAPÍTULO {sub['codigo']} - {sub['nombre']}</h3>
            <span class="subchapter-total">{fmt_eur(sub['subtotal_venta'])}</span>
          </div>
          <table class="items-table">
            <thead>
              <tr>
                <th style="width: 14%;">Código</th>
                <th style="width: 46%;">Descripción y Alcance</th>
                <th style="width: 8%; text-align: center;">Ud.</th>
                <th style="width: 10%; text-align: right;">Cantidad</th>
                <th style="width: 11%; text-align: right;">Precio Ud.</th>
                <th style="width: 11%; text-align: right;">Importe</th>
              </tr>
            </thead>
            <tbody>
              {partidas_rows}
            </tbody>
          </table>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Presupuesto {DATA['codigo']} · {DATA['proyecto']['obra']}</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 15mm 12mm 15mm 12mm;
    }}
    * {{
      box-sizing: border-box;
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    }}
    body {{
      color: #1e293b;
      margin: 0;
      padding: 0;
      font-size: 9pt;
      line-height: 1.4;
      background: #ffffff;
    }}
    .header-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 12px;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 8px;
    }}
    .brand-title {{
      font-size: 14pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.5px;
      margin: 0;
    }}
    .brand-sub {{
      font-size: 8.5pt;
      font-weight: 600;
      color: #0284c7;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin: 2px 0 0 0;
    }}
    .brand-contact {{
      font-size: 7.5pt;
      color: #64748b;
      margin-top: 4px;
    }}
    .doc-badge {{
      text-align: right;
    }}
    .badge-code {{
      display: inline-block;
      background: #0f172a;
      color: #ffffff;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 10pt;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .badge-ref {{
      font-size: 8pt;
      font-weight: 600;
      color: #64748b;
      margin-top: 4px;
    }}
    .meta-grid {{
      display: table;
      width: 100%;
      margin-bottom: 14px;
    }}
    .meta-col {{
      display: table-cell;
      width: 50%;
      vertical-align: top;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 10px 12px;
    }}
    .meta-col:first-child {{
      margin-right: 8px;
    }}
    .meta-col h4 {{
      margin: 0 0 6px 0;
      font-size: 8.5pt;
      font-weight: 700;
      color: #0f172a;
      text-transform: uppercase;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 3px;
    }}
    .meta-line {{
      font-size: 8pt;
      margin-bottom: 3px;
    }}
    .meta-line strong {{
      color: #334155;
    }}
    .scope-box {{
      background: #f0fdf4;
      border-left: 4px solid #16a34a;
      padding: 8px 12px;
      margin-bottom: 14px;
      font-size: 8pt;
      border-radius: 0 4px 4px 0;
    }}
    .scope-box strong {{
      color: #166534;
    }}
    .subchapter-block {{
      margin-bottom: 16px;
      page-break-inside: auto;
    }}
    .subchapter-header {{
      background: #0f172a;
      color: #ffffff;
      padding: 6px 10px;
      border-radius: 4px 4px 0 0;
      display: table;
      width: 100%;
    }}
    .subchapter-header h3 {{
      display: table-cell;
      font-size: 9pt;
      font-weight: 700;
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}
    .subchapter-total {{
      display: table-cell;
      text-align: right;
      font-size: 9pt;
      font-weight: 700;
      color: #fef08a;
    }}
    .items-table {{
      width: 100%;
      border-collapse: collapse;
      border: 1px solid #cbd5e1;
      border-top: none;
      margin-bottom: 4px;
    }}
    .items-table th {{
      background: #f1f5f9;
      color: #334155;
      font-size: 7.5pt;
      font-weight: 700;
      padding: 5px 8px;
      border-bottom: 1px solid #cbd5e1;
      text-transform: uppercase;
    }}
    .items-table td {{
      padding: 6px 8px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: top;
      font-size: 8pt;
    }}
    .items-table tr:nth-child(even) {{
      background: #fafafa;
    }}
    .items-table td.code {{
      font-family: Consolas, monospace;
      font-size: 7.5pt;
      color: #475569;
      font-weight: 600;
    }}
    .items-table td.desc strong {{
      color: #0f172a;
      font-size: 8pt;
    }}
    .partida-desc {{
      margin: 3px 0 0 0;
      font-size: 7.5pt;
      color: #475569;
      line-height: 1.3;
    }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .qty, .price {{ font-variant-numeric: tabular-nums; }}
    .amount {{ font-weight: 700; color: #0f172a; font-variant-numeric: tabular-nums; }}

    .summary-card {{
      margin-top: 14px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 12px;
      page-break-inside: avoid;
    }}
    .summary-table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .summary-table td {{
      padding: 4px 6px;
      font-size: 8.5pt;
    }}
    .summary-table td.total-label {{
      font-size: 11pt;
      font-weight: 800;
      color: #0f172a;
      border-top: 2px solid #0f172a;
      padding-top: 8px;
    }}
    .summary-table td.total-val {{
      font-size: 12pt;
      font-weight: 800;
      color: #b45309;
      text-align: right;
      border-top: 2px solid #0f172a;
      padding-top: 8px;
    }}
    .conditions-grid {{
      margin-top: 14px;
      border-top: 1px solid #cbd5e1;
      padding-top: 10px;
      page-break-inside: avoid;
    }}
    .cond-title {{
      font-size: 8pt;
      font-weight: 700;
      color: #0f172a;
      text-transform: uppercase;
      margin-bottom: 4px;
    }}
    .cond-list {{
      margin: 0;
      padding-left: 14px;
      font-size: 7.5pt;
      color: #475569;
    }}
    .cond-list li {{
      margin-bottom: 2px;
    }}
    .signatures-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 18px;
      page-break-inside: avoid;
    }}
    .sig-col {{
      width: 50%;
      border: 1px dashed #cbd5e1;
      padding: 10px;
      text-align: center;
      background: #f8fafc;
      border-radius: 4px;
    }}
    .sig-box {{
      height: 45px;
    }}
  </style>
</head>
<body>

  <table class="header-table">
    <tr>
      <td style="width: 60%; vertical-align: top;">
        <h1 class="brand-title">HAM MENORCA · ESTRUCTURAS METÁLICAS</h1>
        <p class="brand-sub">Dixis Recursos y Soluciones S.L. · CIF B57825432</p>
        <p class="brand-contact">Av. Circunval·lació 11, Pol. Ind. Sant Lluís, Menorca · Tel: +34 971 35 20 18 / 669 769 541 · info@dixis.es · www.hamenorca.com</p>
      </td>
      <td style="width: 40%; vertical-align: top;" class="doc-badge">
        <div class="badge-code">OFERTA {DATA['codigo']}</div>
        <div class="badge-ref">REF: {DATA['referencia']}</div>
        <div class="badge-ref">Fecha: {DATA['fecha']} · Validez: {DATA['validez_dias']} días</div>
      </td>
    </tr>
  </table>

  <div class="meta-grid">
    <div class="meta-col">
      <h4>Destinatario / Cliente Licitador</h4>
      <div class="meta-line"><strong>Empresa:</strong> {DATA['cliente']['empresa']}</div>
      <div class="meta-line"><strong>Atención:</strong> {DATA['cliente']['contacto']} ({DATA['cliente']['cargo']})</div>
      <div class="meta-line"><strong>Teléfonos:</strong> {DATA['cliente']['telefono']}</div>
      <div class="meta-line"><strong>Sede Central:</strong> {DATA['cliente']['direccion']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}</div>
    </div>
    <div class="meta-col" style="margin-left: 10px;">
      <h4>Datos del Proyecto y Emplazamiento</h4>
      <div class="meta-line"><strong>Proyecto:</strong> {DATA['proyecto']['titulo']}</div>
      <div class="meta-line"><strong>Promotor:</strong> {DATA['proyecto']['promotor']}</div>
      <div class="meta-line"><strong>Ubicación:</strong> {DATA['proyecto']['emplazamiento']}</div>
      <div class="meta-line"><strong>Capítulo:</strong> {DATA['proyecto']['capitulo_codigo']} {DATA['proyecto']['capitulo_nombre']} (EXC3 / EXC2)</div>
    </div>
  </div>

  <div class="scope-box">
    <strong>ALCANCE DE LA OFERTA ESTRUCTURAL HAM:</strong> Fabricación en taller y montaje en obra de <strong>347.475,00 kg (~347,48 Tn)</strong> de acero laminado S275JR y <strong>403,17 m²</strong> de forjado colaborante e=16 cm. Incluye sustitución funcional de jácenas de hormigón mediante perfiles UPN conectados, refuerzo perimetral de pilares con empresillados angulares y presillas cada 40 cm, capiteles de acero retacados de 2, 3 y 4 jácenas, vigas soporte de parteluces, forjados colaborantes bajo y sobre rasante, y zancas de Escaleras 1 y 2.
    <br><strong>Tratamiento Anticorrosión:</strong> Imprimación anticorrosiva en taller y acabado en obra según ambiente C1/C4 (conforme a las directrices de HAM, en ningún caso se presupuesta pintura al horno).
  </div>

  {subcaps_html}

  <div class="summary-card">
    <table class="summary-table">
      <tr>
        <td style="width: 70%;"><strong>Subtotal 06.01 - REHABILITACIÓN</strong> (Acero vertical/horizontal, anclajes y forjados colaborantes)</td>
        <td style="width: 30%; text-align: right; font-weight: 700;">{fmt_eur(DATA['subcapitulos'][0]['subtotal_venta'])}</td>
      </tr>
      <tr>
        <td><strong>Subtotal 06.02 - OBRA NUEVA</strong> (Perfiles S275JR en cubierta P6 y pasarela ascensor)</td>
        <td style="text-align: right; font-weight: 700;">{fmt_eur(DATA['subcapitulos'][1]['subtotal_venta'])}</td>
      </tr>
      <tr>
        <td><strong>Subtotal 06.03 - REFUERZOS ESTRUCTURALES</strong> (Jácenas UPN, empresillados, capiteles y parteluces)</td>
        <td style="text-align: right; font-weight: 700;">{fmt_eur(DATA['subcapitulos'][2]['subtotal_venta'])}</td>
      </tr>
      <tr>
        <td class="total-label">BASE IMPONIBLE TOTAL (VENTA)</td>
        <td class="total-val" style="color: #0f172a;">{fmt_eur(DATA['totales']['base_imponible'])}</td>
      </tr>
      <tr>
        <td style="font-weight: 700; color: #475569;">I.V.A. Repercutible ({DATA['totales']['iva_porcentaje']}%)</td>
        <td style="text-align: right; font-weight: 700; color: #475569;">{fmt_eur(DATA['totales']['iva_importe'])}</td>
      </tr>
      <tr>
        <td class="total-label" style="color: #b45309;">TOTAL OFERTA ECONÓMICA (CON I.V.A.)</td>
        <td class="total-val">{fmt_eur(DATA['totales']['total_con_iva'])}</td>
      </tr>
    </table>
  </div>

  <div class="conditions-grid">
    <div class="cond-title">Condiciones Técnicas y Contractuales</div>
    <ul class="cond-list">
      <li><strong>Normativa de Ejecución:</strong> Código Estructural (RD 470/2021) y UNE-EN 1090-2 clase EXC3 para refuerzos principales de fustes, jácenas y capiteles; clase EXC2 para vigas y zancas interiores. Marcado CE obligatorio de todos los componentes metálicos.</li>
      <li><strong>Tratamiento de Acabado:</strong> Preparación de superficies, imprimación de adherencia antioxidante de alta durabilidad en taller y pintura de acabado en obra. No incluye termolacado ni pintura al horno.</li>
      <li><strong>Conexiones y Rellenos:</strong> Incluye p.p. de varillas roscadas corrugadas B500S M16 y M20 con inyección continua de resina epoxi de dos componentes de baja viscosidad, y retacado perimetral con mortero sin retracción tipo Grout de alta fluidez y resistencia característica.</li>
      <li><strong>Medios de Montaje:</strong> Incluye camión pluma para descarga a pie de tajo, polipastos mecánicos y medios de izado interior para manipulación en plantas existentes. La contrata principal garantizará accesos despejados y apuntalamiento previo según planos ER.02.</li>
      <li><strong>Forma de Pago:</strong> Certificaciones mensuales de obra ejecutada y validada por la Dirección Facultativa, con abono mediante transferencia bancaria a 30 días fecha factura.</li>
    </ul>
  </div>

  <table class="signatures-table">
    <tr>
      <td class="sig-col" style="margin-right: 10px;">
        <div style="font-size: 8pt; font-weight: 700; color: #0f172a; margin-bottom: 4px;">Por HAM MENORCA (Dixis Recursos y Soluciones S.L.)</div>
        <div class="sig-box"></div>
        <div style="font-size: 7.5pt; color: #64748b;">Pablo Sebastián Sánchez Arnoletto<br>Administrador Solidario · Dpto. Técnico</div>
      </td>
      <td class="sig-col">
        <div style="font-size: 8pt; font-weight: 700; color: #0f172a; margin-bottom: 4px;">Conforme Cliente (Cobra Edificación Singular)</div>
        <div class="sig-box"></div>
        <div style="font-size: 7.5pt; color: #64748b;">Firma y Sello de Aceptación<br>Fecha: _____ / _____ / 2026</div>
      </td>
    </tr>
  </table>

</body>
</html>
"""
    html_file = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML cliente guardado en: {html_file}")
    return html_file

def create_html_internal():
    subcaps_internal = ""
    for sub in DATA["subcapitulos"]:
        rows = ""
        for p in sub["partidas"]:
            rows += f"""
            <tr>
              <td class="code">{p['codigo']}</td>
              <td class="desc">{p['resumen']}</td>
              <td class="center">{p['unidad']}</td>
              <td class="right">{fmt_num(p['cantidad'])}</td>
              <td class="right">{fmt_eur(p['coste_unitario'])}</td>
              <td class="right">{fmt_eur(p['importe_coste'])}</td>
              <td class="right">{fmt_eur(p['precio_venta_unitario'])}</td>
              <td class="right font-bold">{fmt_eur(p['importe_venta'])}</td>
              <td class="right green font-bold">+{fmt_eur(p['margen_bruto'])}</td>
              <td class="right green font-bold">{p['margen_porcentaje']}%</td>
            </tr>
            """
        subcaps_internal += f"""
        <tr class="sub-header">
          <td colspan="5"><strong>SUBCAPÍTULO {sub['codigo']} - {sub['nombre']}</strong></td>
          <td class="right"><strong>{fmt_eur(sub['subtotal_coste'])}</strong></td>
          <td></td>
          <td class="right font-bold"><strong>{fmt_eur(sub['subtotal_venta'])}</strong></td>
          <td class="right green font-bold"><strong>+{fmt_eur(sub['subtotal_margen'])}</strong></td>
          <td class="right green font-bold"><strong>{sub['subtotal_margen_porcentaje']}%</strong></td>
        </tr>
        {rows}
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Estudio Técnico Interno de Costes · {DATA['codigo']}</title>
  <style>
    @page {{
      size: A4 landscape;
      margin: 12mm;
    }}
    * {{
      box-sizing: border-box;
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }}
    body {{
      color: #1e293b;
      margin: 0;
      padding: 0;
      font-size: 8pt;
      line-height: 1.35;
      background: #ffffff;
    }}
    .header {{
      border-bottom: 2px solid #0f172a;
      padding-bottom: 8px;
      margin-bottom: 10px;
      display: table;
      width: 100%;
    }}
    .header-left {{
      display: table-cell;
      width: 60%;
    }}
    .header-right {{
      display: table-cell;
      width: 40%;
      text-align: right;
    }}
    .title {{
      font-size: 13pt;
      font-weight: 800;
      color: #0f172a;
      margin: 0;
    }}
    .confidential-tag {{
      display: inline-block;
      background: #dc2626;
      color: #ffffff;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 8pt;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .meta-box {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 8px 12px;
      border-radius: 6px;
      margin-bottom: 12px;
      display: table;
      width: 100%;
    }}
    .meta-cell {{
      display: table-cell;
      width: 25%;
      font-size: 7.5pt;
    }}
    .cost-table {{
      width: 100%;
      border-collapse: collapse;
      border: 1px solid #cbd5e1;
      margin-bottom: 12px;
    }}
    .cost-table th {{
      background: #0f172a;
      color: #ffffff;
      font-size: 7pt;
      font-weight: 700;
      padding: 5px 6px;
      text-transform: uppercase;
    }}
    .cost-table td {{
      padding: 4px 6px;
      border-bottom: 1px solid #e2e8f0;
      font-size: 7.5pt;
    }}
    .sub-header {{
      background: #e2e8f0;
      color: #0f172a;
    }}
    .center {{ text-align: center; }}
    .right {{ text-align: right; }}
    .code {{ font-family: Consolas, monospace; font-size: 7pt; font-weight: 600; color: #475569; }}
    .desc {{ font-size: 7.5pt; color: #1e293b; }}
    .font-bold {{ font-weight: 700; }}
    .green {{ color: #15803d; }}
    .tot-row {{
      background: #fef3c7;
      border-top: 2px solid #0f172a;
      border-bottom: 2px solid #0f172a;
      font-size: 8.5pt;
      font-weight: 800;
    }}
    .kpi-grid {{
      display: table;
      width: 100%;
      margin-top: 10px;
    }}
    .kpi-card {{
      display: table-cell;
      width: 25%;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px 10px;
      text-align: center;
    }}
    .kpi-card:not(:last-child) {{
      margin-right: 8px;
    }}
    .kpi-val {{
      font-size: 13pt;
      font-weight: 800;
      color: #0f172a;
      margin: 2px 0;
    }}
    .kpi-lbl {{
      font-size: 7pt;
      color: #64748b;
      text-transform: uppercase;
      font-weight: 600;
    }}
    .notes-box {{
      background: #eff6ff;
      border-left: 4px solid #3b82f6;
      padding: 8px 10px;
      margin-top: 10px;
      font-size: 7.5pt;
      border-radius: 0 4px 4px 0;
    }}
  </style>
</head>
<body>

  <div class="header">
    <div class="header-left">
      <h1 class="title">HAM MENORCA · ESTUDIO TÉCNICO INTERNO Y RENTABILIDAD</h1>
      <div style="font-size: 8pt; color: #0284c7; font-weight: 600; margin-top: 2px;">
        EXPEDIENTE {DATA['codigo']} · {DATA['proyecto']['obra']} (IB-SALUT)
      </div>
    </div>
    <div class="header-right">
      <div class="confidential-tag">DOCUMENTO INTERNO CONFIDENCIAL</div>
      <div style="font-size: 7.5pt; color: #64748b; margin-top: 3px;">Fecha: {DATA['fecha']} · Destinatario: Cobra Edificación Singular</div>
    </div>
  </div>

  <div class="meta-box">
    <div class="meta-cell">
      <strong>Acero Laminado Total:</strong> {fmt_num(DATA['totales']['total_kg_acero'])} kg ({fmt_num(DATA['totales']['total_kg_acero']/1000.0, 2)} Tn)<br>
      <strong>Forjados Colaborantes:</strong> {fmt_num(DATA['totales']['total_m2_forjado'])} m²
    </div>
    <div class="meta-cell">
      <strong>Coste Directo Total:</strong> {fmt_eur(DATA['totales']['coste_directo_total'])}<br>
      <strong>Coste Medio Acero:</strong> {fmt_eur(DATA['totales']['coste_directo_total']/DATA['totales']['total_kg_acero'])}/kg
    </div>
    <div class="meta-cell">
      <strong>Venta Base Imponible:</strong> {fmt_eur(DATA['totales']['base_imponible'])}<br>
      <strong>Precio Medio Venta Acero:</strong> {fmt_eur(DATA['totales']['base_imponible']/DATA['totales']['total_kg_acero'])}/kg
    </div>
    <div class="meta-cell">
      <strong>Margen Bruto Total:</strong> +{fmt_eur(DATA['totales']['margen_bruto_total'])}<br>
      <strong>Rentabilidad s/ Venta:</strong> {DATA['totales']['margen_porcentaje_sobre_venta']}%
    </div>
  </div>

  <table class="cost-table">
    <thead>
      <tr>
        <th style="width: 10%;">Código</th>
        <th style="width: 32%;">Partida Presupuestaria</th>
        <th style="width: 4%; text-align: center;">Ud.</th>
        <th style="width: 8%; text-align: right;">Cantidad</th>
        <th style="width: 7%; text-align: right;">Coste Ud.</th>
        <th style="width: 10%; text-align: right;">Coste Total</th>
        <th style="width: 7%; text-align: right;">Venta Ud.</th>
        <th style="width: 10%; text-align: right;">Venta Total</th>
        <th style="width: 7%; text-align: right;">Margen (€)</th>
        <th style="width: 5%; text-align: right;">% Marg.</th>
      </tr>
    </thead>
    <tbody>
      {subcaps_internal}
      <tr class="tot-row">
        <td colspan="5" style="text-align: right;">TOTALES CONSOLIDADOS DEL EXPEDIENTE:</td>
        <td class="right">{fmt_eur(DATA['totales']['coste_directo_total'])}</td>
        <td></td>
        <td class="right">{fmt_eur(DATA['totales']['base_imponible'])}</td>
        <td class="right green">+{fmt_eur(DATA['totales']['margen_bruto_total'])}</td>
        <td class="right green">{DATA['totales']['margen_porcentaje_sobre_venta']}%</td>
      </tr>
    </tbody>
  </table>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-lbl">Venta Base Imponible</div>
      <div class="kpi-val">{fmt_eur(DATA['totales']['base_imponible'])}</div>
    </div>
    <div class="kpi-card" style="margin-left: 8px;">
      <div class="kpi-lbl">Coste Directo Estimado</div>
      <div class="kpi-val" style="color: #475569;">{fmt_eur(DATA['totales']['coste_directo_total'])}</div>
    </div>
    <div class="kpi-card" style="margin-left: 8px;">
      <div class="kpi-lbl">Margen Bruto de Operación</div>
      <div class="kpi-val" style="color: #15803d;">+{fmt_eur(DATA['totales']['margen_bruto_total'])}</div>
    </div>
    <div class="kpi-card" style="margin-left: 8px;">
      <div class="kpi-lbl">Rentabilidad sobre Venta</div>
      <div class="kpi-val" style="color: #15803d;">{DATA['totales']['margen_porcentaje_sobre_venta']}%</div>
    </div>
  </div>

  <div class="notes-box">
    <strong>Estrategia de Fabricación y Aprovisionamiento HAM:</strong>
    <ul style="margin: 2px 0 0 0; padding-left: 14px;">
      <li><strong>Acero Base S275JR:</strong> Compra directa agrupada a fábrica/almacén siderúrgico para optimizar precio de partida (~1,10 - 1,18 €/kg en perfiles pesados IPE, UPN y HEB; chapa en bobina/plancha a ~1,25 €/kg). Transporte marítimo en plataformas completas.</li>
      <li><strong>Taller y Transformación:</strong> Oxicorte por plasma de cartelas y placas, sierra de cinta y taladro automatizado en taller HAM Sant Lluís. Soldaduras semiautomáticas MAG bajo control de producción en fábrica según UNE-EN 1090-2 (EXC3).</li>
      <li><strong>Protección Superficial:</strong> Chorreado Sa 2½, imprimación epoxi fosfato de zinc 80 µm en taller. Esmalte de poliuretano 60 µm aplicado en obra tras montaje. (Nunca pintura al horno).</li>
      <li><strong>Logística y Medios Auxiliares:</strong> Transporte insular por camión plataforma según secuencias de obra. En obra, maniobras mediante grúa telescópica para entradas en planta y carros mecánicos de transferencia interna.</li>
    </ul>
  </div>

</body>
</html>
"""
    html_file = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML interno técnico guardado en: {html_file}")
    return html_file

def create_readme():
    readme_content = f"""# Presupuesto P-2026-0062 · Nou Hospital Verge del Toro (Mahón)

- **Código:** `P-2026-0062`
- **Referencia:** `PRE-2026-1116-HOSPITAL-MAHON-ESTRUCTURA`
- **Fecha de Emisión:** {DATA['fecha']}
- **Cliente:** {DATA['cliente']['empresa']}
- **Atención:** {DATA['cliente']['contacto']} ({DATA['cliente']['cargo']})
- **Teléfonos:** {DATA['cliente']['telefono']}
- **Sede:** {DATA['cliente']['direccion']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}
- **Proyecto:** {DATA['proyecto']['titulo']}
- **Promotor:** {DATA['proyecto']['promotor']}
- **Emplazamiento:** {DATA['proyecto']['emplazamiento']}
- **Capítulo de Licitación:** {DATA['proyecto']['capitulo_codigo']} {DATA['proyecto']['capitulo_nombre']}
- **Planos de Referencia:** ES.01.01 a ES.04.09 y ER.01.01 a ER.05.07 (Estructura, cuadros de pilares, plantas de derribo y obra nueva, escaleras y detalles)

---

## Resumen Económico Consolidado

| Concepto | Cantidad | Coste Directo (€) | Venta Base Imponible (€) | Margen Bruto (€) | % Margen |
|---|---:|---:|---:|---:|---:|
| **06.01 Rehabilitación** (Pilares, vigas, zancas escaleras y forjados colaborantes) | 34.880,65 kg + 403,17 m² | 148.974,27 € | 208.809,27 € | +59.835,00 € | 28,66% |
| **06.02 Obra Nueva** (Cubierta P6 y pasarela ascensor) | 1.068,96 kg | 4.062,05 € | 5.718,94 € | +1.656,89 € | 28,97% |
| **06.03 Refuerzos Estructurales** (Jácenas UPN, parteluces, empresillados fustes y capiteles) | 311.525,39 kg | 1.061.294,99 € | 1.472.944,61 € | +411.649,62 € | 27,95% |
| **TOTALES CAPÍTULO H06** | **347.475,00 kg + 403,17 m²** | **{fmt_eur(DATA['totales']['coste_directo_total'])}** | **{fmt_eur(DATA['totales']['base_imponible'])}** | **+{fmt_eur(DATA['totales']['margen_bruto_total'])}** | **{DATA['totales']['margen_porcentaje_sobre_venta']}%** |

- **I.V.A. Repercutible ({DATA['totales']['iva_porcentaje']}%):** {fmt_eur(DATA['totales']['iva_importe'])}
- **Total Presupuesto (con IVA):** **{fmt_eur(DATA['totales']['total_con_iva'])}**

---

## Desglose Técnico de Suministros
1. **Acero Estructural S275JR:** 347.475,00 kg (~347,48 toneladas métricas) trabajadas en taller HAM y montadas en obra con medios auxiliares.
2. **Forjados Colaborantes (e=16 cm):** 403,17 m² (66,01 m² bajo rasante HA-25/XC3 y 337,16 m² sobre rasante HA-25/XC1).
3. **Clase de Ejecución:** EXC3 (refuerzos y capiteles principales) y EXC2 (vigas de forjado y zancas) según Código Estructural.
4. **Pintura y Acabado HAM:** Imprimación de adherencia antioxidante en taller y pintura de acabado en obra (C1/C4). *Nunca pintura al horno*.

---

## Archivos del Expediente

- [Presupuesto_P2026_0062_Hospital_Verge_del_Toro_Estructura.xlsx](file:///{os.path.join(BASE_DIR, "Presupuesto_P2026_0062_Hospital_Verge_del_Toro_Estructura.xlsx").replace(os.sep, "/")}): Libro de trabajo completo con 3 pestañas (Resumen Ejecutivo, Mediciones Detalladas línea a línea según CSV del proyecto, y Estudio Interno de Costes y Márgenes).
- [presupuesto-cliente.pdf](file:///{os.path.join(BASE_DIR, "presupuesto-cliente.pdf").replace(os.sep, "/")}): Oferta comercial oficial formal para Cobra Edificación Singular.
- [presupuesto-cliente.html](file:///{os.path.join(BASE_DIR, "presupuesto-cliente.html").replace(os.sep, "/")}): Versión HTML interactiva de alta definición para revisión directa.
- [presupuesto-interno-tecnico.pdf](file:///{os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf").replace(os.sep, "/")}): Informe técnico de costes, horas de taller y montaje, logística y ratios de rentabilidad.
- [presupuesto-interno-tecnico.html](file:///{os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html").replace(os.sep, "/")}): HTML del informe técnico confidencial.
- [datos.json](file:///{os.path.join(BASE_DIR, "datos.json").replace(os.sep, "/")}): Fuente de datos estructurada con todas las mediciones, fórmulas y parámetros.
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"README generado en: {readme_path}")
    return readme_path

def main():
    excel_path = create_excel()
    html_cli = create_html_client()
    pdf_cli = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    convert_html_to_pdf(html_cli, pdf_cli)

    html_int = create_html_internal()
    pdf_int = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")
    convert_html_to_pdf(html_int, pdf_int)

    create_readme()
    print("¡Todos los documentos han sido generados exitosamente!")

if __name__ == "__main__":
    main()
