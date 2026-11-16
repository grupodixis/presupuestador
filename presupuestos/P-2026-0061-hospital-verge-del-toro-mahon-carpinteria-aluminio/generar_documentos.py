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
    # HOJA 1: RESUMEN EJECUTIVO Y OFERTA CLIENTE
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Resumen Ejecutivo"
    ws1.views.sheetView[0].showGridLines = True

    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. · ALUFAC CARPINTERÍA DE ALUMINIO / HAM MENORCA"
    ws1["B2"].font = font_brand
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} · {DATA['referencia']}"
    ws1["B3"].font = font_title

    ws1["B5"] = "DATOS DEL CLIENTE"
    ws1["B5"].font = font_sec
    ws1["B6"] = "Empresa:"
    ws1["C6"] = DATA["cliente"]["empresa"]
    ws1["B7"] = "Atención:"
    ws1["C7"] = f"{DATA['cliente']['contacto']} ({DATA['cliente']['cargo']})"
    ws1["B8"] = "Teléfonos:"
    ws1["C8"] = DATA["cliente"]["telefono"]
    ws1["B9"] = "Dirección:"
    ws1["C9"] = f"{DATA['cliente']['direccion']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']} ({DATA['cliente']['provincia']})"

    for r in range(6, 10):
        ws1[f"B{r}"].font = font_bold
        ws1[f"C{r}"].font = font_reg

    ws1["F5"] = "DATOS DE LA LICITACIÓN / PROYECTO"
    ws1["F5"].font = font_sec
    ws1["F6"] = "Proyecto:"
    ws1["G6"] = DATA["proyecto"]["obra"]
    ws1["F7"] = "Promotor:"
    ws1["G7"] = DATA["proyecto"]["promotor"]
    ws1["F8"] = "Emplazamiento:"
    ws1["G8"] = DATA["proyecto"]["emplazamiento"]
    ws1["F9"] = "Capítulo:"
    ws1["G9"] = f"{DATA['proyecto']['capitulo_codigo']} {DATA['proyecto']['capitulo_nombre']}"

    for r in range(6, 10):
        ws1[f"F{r}"].font = font_bold
        ws1[f"G{r}"].font = font_reg

    # Tabla resumen de partidas
    headers1 = ["Ítem", "Código", "Resumen / Denominación de la Partida", "Sistema / Serie", "Ud", "Medición (m²)", "Precio Venta Unit.", "Importe (€)"]
    row = 12
    for col_idx, h in enumerate(headers1, start=2):
        cell = ws1.cell(row=row, column=col_idx, value=h)
        cell.font = font_hdr
        cell.fill = f_navy
        cell.alignment = Alignment(horizontal="center" if col_idx in [2, 6, 7] else "left" if col_idx in [3, 4, 5] else "right", vertical="center")
        cell.border = b_thin
    ws1.row_dimensions[row].height = 24

    start_row = row + 1
    for p in DATA["partidas"]:
        row += 1
        ws1.row_dimensions[row].height = 20
        c2 = ws1.cell(row=row, column=2, value=p["orden"])
        c3 = ws1.cell(row=row, column=3, value=p["codigo"])
        c4 = ws1.cell(row=row, column=4, value=p["resumen"])
        c5 = ws1.cell(row=row, column=5, value=p["sistema"])
        c6 = ws1.cell(row=row, column=6, value=p["unidad"])
        c7 = ws1.cell(row=row, column=7, value=p["cantidad"])
        c8 = ws1.cell(row=row, column=8, value=p["precio_venta_unitario"])
        c9 = ws1.cell(row=row, column=9, value=f"=G{row}*H{row}")

        c2.alignment = Alignment(horizontal="center")
        c3.alignment = Alignment(horizontal="center")
        c4.alignment = Alignment(horizontal="left")
        c5.alignment = Alignment(horizontal="left")
        c6.alignment = Alignment(horizontal="center")
        c7.alignment = Alignment(horizontal="right")
        c8.alignment = Alignment(horizontal="right")
        c9.alignment = Alignment(horizontal="right")

        c7.number_format = NUM_QTY
        c8.number_format = NUM_EUR
        c9.number_format = NUM_EUR

        fill_r = f_alt if p["orden"] % 2 == 0 else PatternFill(fill_type=None)
        for col_idx in range(2, 10):
            c = ws1.cell(row=row, column=col_idx)
            c.font = font_reg
            c.border = b_thin
            if fill_r.fill_type:
                c.fill = fill_r

    # Totales
    row += 1
    ws1.row_dimensions[row].height = 22
    ws1.cell(row=row, column=4, value="TOTAL CARPINTERÍA Y CELOSÍAS H25").font = font_tot
    c_qty_tot = ws1.cell(row=row, column=7, value=f"=SUM(G{start_row}:G{row-1})")
    c_qty_tot.font = font_tot
    c_qty_tot.alignment = Alignment(horizontal="right")
    c_qty_tot.number_format = NUM_QTY

    c_base = ws1.cell(row=row, column=9, value=f"=SUM(I{start_row}:I{row-1})")
    c_base.font = font_tot
    c_base.alignment = Alignment(horizontal="right")
    c_base.number_format = NUM_EUR
    for c in range(2, 10):
        ws1.cell(row=row, column=c).border = b_tot
        ws1.cell(row=row, column=c).fill = f_sub

    row += 1
    ws1.cell(row=row, column=8, value="BASE IMPONIBLE:").font = font_bold
    c_bimp = ws1.cell(row=row, column=9, value=f"=I{row-1}")
    c_bimp.font = font_bold
    c_bimp.number_format = NUM_EUR

    row += 1
    ws1.cell(row=row, column=8, value="I.V.A. (21,0%):").font = font_bold
    c_iva = ws1.cell(row=row, column=9, value=f"=I{row-1}*0.21")
    c_iva.font = font_bold
    c_iva.number_format = NUM_EUR

    row += 1
    ws1.row_dimensions[row].height = 24
    ws1.cell(row=row, column=8, value="TOTAL PRESUPUESTO CON IVA:").font = font_tot_gold
    c_tot = ws1.cell(row=row, column=9, value=f"=I{row-2}+I{row-1}")
    c_tot.font = font_tot_gold
    c_tot.number_format = NUM_EUR
    ws1.cell(row=row, column=8).fill = f_tot
    ws1.cell(row=row, column=9).fill = f_tot
    ws1.cell(row=row, column=8).border = b_tot
    ws1.cell(row=row, column=9).border = b_tot

    for col in ["B", "C", "D", "E", "F", "G", "H", "I"]:
        max_len = max(len(str(ws1[f"{col}{r}"].value or "")) for r in range(1, row + 2))
        ws1.column_dimensions[col].width = max(max_len + 3, 11)
    ws1.column_dimensions["D"].width = 46
    ws1.column_dimensions["E"].width = 34
    ws1.column_dimensions["I"].width = 17

    # -------------------------------------------------------------
    # HOJA 2: MEDICIONES LÍNEA A LÍNEA (DETALLE CSV COMPLETO)
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Mediciones Detalladas")
    ws2.views.sheetView[0].showGridLines = True

    ws2["B2"] = "CUADRO DE MEDICIONES DETALLADAS Y JUSTIFICACIÓN POR PARTIDAS"
    ws2["B2"].font = font_title
    ws2["B3"] = f"{DATA['proyecto']['titulo']} · Licitación IB-SALUT"
    ws2["B3"].font = font_brand

    headers2 = ["Código", "Nat / Tipo", "Ud", "Resumen / Línea de Medición", "Nº", "Longitud (m)", "Anchura (m)", "Altura (m)", "Parcial (m²)", "CanPres", "Precio Venta", "Importe (€)"]
    row2 = 5
    for col_idx, h in enumerate(headers2, start=2):
        cell = ws2.cell(row=row2, column=col_idx, value=h)
        cell.font = font_hdr
        cell.fill = f_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = b_thin
    ws2.row_dimensions[row2].height = 24

    for p in DATA["partidas"]:
        row2 += 1
        ws2.row_dimensions[row2].height = 21
        ws2.cell(row2, 2, p["codigo"]).font = font_bold
        ws2.cell(row2, 3, "Partida").font = font_bold
        ws2.cell(row2, 4, p["unidad"]).font = font_bold
        ws2.cell(row2, 5, p["resumen"]).font = font_bold
        ws2.cell(row2, 11, p["cantidad"]).font = font_bold
        ws2.cell(row2, 11).number_format = NUM_QTY
        ws2.cell(row2, 12, p["precio_venta_unitario"]).font = font_bold
        ws2.cell(row2, 12).number_format = NUM_EUR
        ws2.cell(row2, 13, f"=K{row2}*L{row2}").font = font_bold
        ws2.cell(row2, 13).number_format = NUM_EUR

        for col in range(2, 14):
            ws2.cell(row2, col).fill = f_sub
            ws2.cell(row2, col).border = b_thin

        # Línea de texto descriptivo
        row2 += 1
        ws2.cell(row2, 5, p["descripcion"]).font = font_italic
        for col in range(2, 14):
            ws2.cell(row2, col).border = b_thin

        # Líneas de desglose
        for d in p["desglose_medicion"]:
            row2 += 1
            ws2.cell(row2, 5, d["etiqueta"]).font = font_reg
            ws2.cell(row2, 6, d["n"]).font = font_reg
            ws2.cell(row2, 7, d["longitud"]).font = font_reg
            ws2.cell(row2, 8, d["anchura"]).font = font_reg
            ws2.cell(row2, 9, d["altura"]).font = font_reg
            
            # Cálculo de cantidad parcial
            # si anchura == 0, n * long * alt, si no n * long * anch
            if d["anchura"] == 0:
                ws2.cell(row2, 10, f"=F{row2}*G{row2}*I{row2}").font = font_reg
            elif d["altura"] == 0:
                ws2.cell(row2, 10, f"=F{row2}*G{row2}*H{row2}").font = font_reg
            else:
                ws2.cell(row2, 10, f"=F{row2}*G{row2}*H{row2}*I{row2}").font = font_reg

            for col in [6, 7, 8, 9, 10]:
                ws2.cell(row2, col).alignment = Alignment(horizontal="right")
                ws2.cell(row2, col).number_format = NUM_QTY

            for col in range(2, 14):
                ws2.cell(row2, col).border = b_thin

        # Línea Total de partida
        row2 += 1
        ws2.cell(row2, 5, f"Total {p['codigo']}").font = font_bold
        ws2.cell(row2, 11, p["cantidad"]).font = font_bold
        ws2.cell(row2, 11).number_format = NUM_QTY
        ws2.cell(row2, 12, p["precio_venta_unitario"]).font = font_bold
        ws2.cell(row2, 12).number_format = NUM_EUR
        ws2.cell(row2, 13, f"=K{row2}*L{row2}").font = font_bold
        ws2.cell(row2, 13).number_format = NUM_EUR
        for col in range(2, 14):
            ws2.cell(row2, col).fill = f_gold
            ws2.cell(row2, col).border = b_thin

    # Total general en Hoja 2
    row2 += 2
    ws2.cell(row2, 5, "TOTAL GENERAL CAPÍTULO H25 CARPINTERIA ALUMINIO").font = font_tot
    ws2.cell(row2, 13, f"='Resumen Ejecutivo'!I{row-2}").font = font_tot
    ws2.cell(row2, 13).number_format = NUM_EUR
    for col in range(2, 14):
        ws2.cell(row2, col).fill = f_tot
        ws2.cell(row2, col).border = b_tot

    for col in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
        ws2.column_dimensions[col].width = 12
    ws2.column_dimensions["E"].width = 50
    ws2.column_dimensions["M"].width = 16

    # -------------------------------------------------------------
    # HOJA 3: ESTUDIO INTERNO DE COSTES Y MÁRGENES
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Estudio Costes y Márgenes")
    ws3.views.sheetView[0].showGridLines = True

    ws3["B2"] = "ANÁLISIS INTERNO DE COSTES DIRECTOS, MÁRGENES Y RENTABILIDAD TÉCNICA"
    ws3["B2"].font = font_title
    ws3["B3"] = f"{DATA['codigo']} · {DATA['proyecto']['obra']}"
    ws3["B3"].font = font_brand

    headers3 = ["Ítem", "Código", "Resumen Partida", "Medición (m²)", "Coste Directo Unit.", "Coste Total (€)", "Precio Venta Unit.", "Venta Total (€)", "Margen Bruto (€)", "Margen / Venta (%)"]
    row3 = 5
    for col_idx, h in enumerate(headers3, start=2):
        cell = ws3.cell(row=row3, column=col_idx, value=h)
        cell.font = font_hdr
        cell.fill = f_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = b_thin
    ws3.row_dimensions[row3].height = 24

    start_row3 = row3 + 1
    for p in DATA["partidas"]:
        row3 += 1
        ws3.cell(row3, 2, p["orden"]).alignment = Alignment(horizontal="center")
        ws3.cell(row3, 3, p["codigo"]).alignment = Alignment(horizontal="center")
        ws3.cell(row3, 4, p["resumen"])
        ws3.cell(row3, 5, p["cantidad"]).number_format = NUM_QTY
        ws3.cell(row3, 6, p["coste_unitario"]).number_format = NUM_EUR
        ws3.cell(row3, 7, f"=E{row3}*F{row3}").number_format = NUM_EUR
        ws3.cell(row3, 8, p["precio_venta_unitario"]).number_format = NUM_EUR
        ws3.cell(row3, 9, f"=E{row3}*H{row3}").number_format = NUM_EUR
        ws3.cell(row3, 10, f"=I{row3}-G{row3}").number_format = NUM_EUR
        ws3.cell(row3, 11, f"=J{row3}/I{row3}").number_format = NUM_PCT

        fill_r = f_alt if p["orden"] % 2 == 0 else PatternFill(fill_type=None)
        for col in range(2, 12):
            cell = ws3.cell(row3, col)
            cell.font = font_reg
            cell.border = b_thin
            if fill_r.fill_type:
                cell.fill = fill_r
        ws3.cell(row3, 10).font = font_green
        ws3.cell(row3, 11).font = font_green

    # Totales internos
    row3 += 1
    ws3.row_dimensions[row3].height = 22
    ws3.cell(row3, 4, "TOTALES GENERALES").font = font_tot
    ws3.cell(row3, 5, f"=SUM(E{start_row3}:E{row3-1})").number_format = NUM_QTY
    ws3.cell(row3, 7, f"=SUM(G{start_row3}:G{row3-1})").number_format = NUM_EUR
    ws3.cell(row3, 9, f"=SUM(I{start_row3}:I{row3-1})").number_format = NUM_EUR
    ws3.cell(row3, 10, f"=SUM(J{start_row3}:J{row3-1})").number_format = NUM_EUR
    ws3.cell(row3, 11, f"=J{row3}/I{row3}").number_format = NUM_PCT

    for col in range(2, 12):
        cell = ws3.cell(row3, col)
        cell.font = font_tot
        cell.fill = f_sub
        cell.border = b_tot

    for col in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]:
        ws3.column_dimensions[col].width = 13
    ws3.column_dimensions["D"].width = 44
    ws3.column_dimensions["G"].width = 16
    ws3.column_dimensions["I"].width = 16
    ws3.column_dimensions["J"].width = 16

    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0061_Hospital_Verge_del_Toro_Cobra.xlsx")
    wb.save(excel_path)
    print(f"Excel generado con éxito en: {excel_path}")
    return excel_path

def create_html_client():
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Presupuesto {DATA['codigo']} - Nou Hospital Verge del Toro (Mahón) - Cobra Edificación Singular</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 12mm 14mm 12mm 14mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-size: 8.5pt;
    line-height: 1.35;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 3px solid #0f172a;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }}
  .logo-block h1 {{
    margin: 0;
    font-size: 15pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
  }}
  .logo-block .sub {{
    font-size: 8pt;
    font-weight: 600;
    color: #0284c7;
    margin-top: 2px;
  }}
  .doc-ref {{
    text-align: right;
  }}
  .doc-badge {{
    display: inline-block;
    background: #0f172a;
    color: #ffffff;
    padding: 3px 8px;
    font-size: 8pt;
    font-weight: 700;
    border-radius: 3px;
    margin-bottom: 4px;
  }}
  .doc-ref p {{
    margin: 1px 0;
    font-size: 7.5pt;
    color: #64748b;
  }}
  .cards-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 12px;
  }}
  .card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 8px 10px;
  }}
  .card-title {{
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    color: #0f172a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
  }}
  .card p {{
    margin: 2px 0;
    font-size: 8pt;
  }}
  .card strong {{
    color: #0f172a;
  }}
  .project-banner {{
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #0284c7;
    padding: 7px 10px;
    margin-bottom: 12px;
    border-radius: 3px;
  }}
  .project-banner h2 {{
    margin: 0 0 3px 0;
    font-size: 9.5pt;
    font-weight: 700;
    color: #0369a1;
  }}
  .project-banner p {{
    margin: 2px 0;
    font-size: 7.5pt;
    color: #334155;
  }}
  table.items {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10px;
    font-size: 8pt;
  }}
  table.items th {{
    background: #0f172a;
    color: #ffffff;
    padding: 5px 6px;
    font-size: 7.5pt;
    font-weight: 700;
    text-align: left;
    border: 1px solid #0f172a;
  }}
  table.items th.num {{ text-align: right; }}
  table.items th.center {{ text-align: center; }}
  table.items td {{
    padding: 4px 6px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }}
  table.items tr.even {{
    background: #f8fafc;
  }}
  table.items tr.head-partida {{
    background: #e2e8f0;
    font-weight: 700;
  }}
  table.items tr.meas {{
    font-size: 7pt;
    color: #475569;
    background: #ffffff;
  }}
  table.items tr.meas td {{
    padding: 1px 6px;
    border-top: none;
    border-bottom: 1px dashed #cbd5e1;
  }}
  .code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-weight: 700;
    color: #0369a1;
  }}
  .totals-block {{
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
  }}
  .totals-table {{
    width: 320px;
    border-collapse: collapse;
    font-size: 8.5pt;
  }}
  .totals-table td {{
    padding: 4px 8px;
    border-bottom: 1px solid #e2e8f0;
  }}
  .totals-table td.label {{
    text-align: right;
    font-weight: 600;
    color: #475569;
  }}
  .totals-table td.val {{
    text-align: right;
    font-weight: 700;
    color: #0f172a;
  }}
  .totals-table tr.grand-total {{
    background: #fef3c7;
    border-top: 2px solid #b45309;
    border-bottom: 2px solid #b45309;
  }}
  .totals-table tr.grand-total td {{
    font-size: 10.5pt;
    color: #92400e;
    font-weight: 800;
    padding: 6px 8px;
  }}
  .condiciones {{
    margin-top: 14px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 8px 10px;
    border-radius: 4px;
    font-size: 7.5pt;
  }}
  .condiciones h3 {{
    margin: 0 0 4px 0;
    font-size: 8pt;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
  }}
  .condiciones ul {{
    margin: 0;
    padding-left: 14px;
  }}
  .condiciones li {{
    margin-bottom: 2px;
    color: #334155;
  }}
  .footer-sig {{
    margin-top: 18px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    font-size: 7.5pt;
  }}
  .sig-box {{
    border: 1px dashed #cbd5e1;
    border-radius: 4px;
    height: 70px;
    padding: 6px;
    position: relative;
  }}
  .sig-box .label {{
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    font-size: 7pt;
  }}
  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

  <!-- PÁGINA 1: PORTADA Y RESUMEN GENERAL -->
  <div class="header">
    <div class="logo-block">
      <h1>DIXIS RECURSOS Y SOLUCIONES S.L.</h1>
      <div class="sub">ALUFAC CARPINTERÍA DE ALUMINIO · HAM ESTRUCTURAS METÁLICAS MENORCA</div>
    </div>
    <div class="doc-ref">
      <div class="doc-badge">OFERTA TÉCNICO-COMERCIAL</div>
      <p><strong>Cód:</strong> {DATA['codigo']}</p>
      <p><strong>Ref:</strong> {DATA['referencia']}</p>
      <p><strong>Fecha:</strong> {DATA['fecha']}</p>
      <p><strong>Validez:</strong> {DATA['validez_dias']} días</p>
    </div>
  </div>

  <div class="cards-grid">
    <div class="card">
      <div class="card-title"><span>Cliente / Contratista Principal</span> <span>EXP. COBRA</span></div>
      <p><strong>Empresa:</strong> {DATA['cliente']['empresa']}</p>
      <p><strong>Atención:</strong> {DATA['cliente']['contacto']} ({DATA['cliente']['cargo']})</p>
      <p><strong>Teléfonos:</strong> {DATA['cliente']['telefono']}</p>
      <p><strong>Sede:</strong> {DATA['cliente']['direccion']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}</p>
      <p><strong>Web:</strong> {DATA['cliente']['web']}</p>
    </div>
    <div class="card">
      <div class="card-title"><span>Emisor / Fabricante e Instalador</span> <span>MENORCA</span></div>
      <p><strong>Razón Social:</strong> {DATA['emisor']['razon_social']} (CIF: {DATA['emisor']['cif']})</p>
      <p><strong>Instalaciones:</strong> {DATA['emisor']['domicilio']}</p>
      <p><strong>Contacto Técnico:</strong> {DATA['emisor']['representante']}</p>
      <p><strong>Teléfono / Móvil:</strong> {DATA['emisor']['telefono']} / {DATA['emisor']['movil']}</p>
      <p><strong>Email / Web:</strong> {DATA['emisor']['email']} · {DATA['emisor']['web']}</p>
    </div>
  </div>

  <div class="project-banner">
    <h2>{DATA['proyecto']['titulo']}</h2>
    <p><strong>Promotor:</strong> {DATA['proyecto']['promotor']} &nbsp;|&nbsp; <strong>Emplazamiento:</strong> {DATA['proyecto']['emplazamiento']}</p>
    <p><strong>Alcance Licitado:</strong> {DATA['proyecto']['capitulo_codigo']} {DATA['proyecto']['capitulo_nombre']} &nbsp;|&nbsp; <strong>Planos:</strong> {DATA['proyecto']['planos_referencia']}</p>
    <p><strong>Acabado y Calidades:</strong> {DATA['proyecto']['acabado_superficial']}. Doble acristalamiento acústico y seguridad 4+4/12/4+4 bajo emisivo con control solar.</p>
  </div>

  <!-- TABLA RESUMEN GENERAL -->
  <table class="items">
    <thead>
      <tr>
        <th class="center" style="width: 25px;">#</th>
        <th style="width: 80px;">Código</th>
        <th>Descripción y Sistema de Carpintería</th>
        <th class="center" style="width: 35px;">Ud</th>
        <th class="num" style="width: 55px;">Medición</th>
        <th class="num" style="width: 65px;">Precio Ud.</th>
        <th class="num" style="width: 75px;">Importe (€)</th>
      </tr>
    </thead>
    <tbody>
"""

    for p in DATA["partidas"]:
        row_cls = "even" if p["orden"] % 2 == 0 else ""
        html += f"""
      <tr class="{row_cls}">
        <td class="center">{p['orden']}</td>
        <td><span class="code">{p['codigo']}</span></td>
        <td><strong>{p['resumen']}</strong><br><span style="font-size: 7pt; color: #64748b;">{p['sistema']} · {p['tipo']}</span></td>
        <td class="center">{p['unidad']}</td>
        <td class="num">{fmt_num(p['cantidad'])}</td>
        <td class="num">{fmt_eur(p['precio_venta_unitario'])}</td>
        <td class="num"><strong>{fmt_eur(p['subtotal'])}</strong></td>
      </tr>"""

    html += f"""
    </tbody>
  </table>

  <div class="totals-block">
    <table class="totals-table">
      <tr>
        <td class="label">Superficie Total Carpintería y Celosías:</td>
        <td class="val">{fmt_num(DATA['totales']['superficie_total_m2'])} m²</td>
      </tr>
      <tr>
        <td class="label">BASE IMPONIBLE (Capítulo H25):</td>
        <td class="val">{fmt_eur(DATA['totales']['base_imponible'])}</td>
      </tr>
      <tr>
        <td class="label">I.V.A. Repercutido ({DATA['totales']['iva_porcentaje']}%):</td>
        <td class="val">{fmt_eur(DATA['totales']['iva_importe'])}</td>
      </tr>
      <tr class="grand-total">
        <td class="label" style="color: #92400e;">TOTAL PRESUPUESTO:</td>
        <td class="val">{fmt_eur(DATA['totales']['total_con_iva'])}</td>
      </tr>
    </table>
  </div>

  <div class="condiciones">
    <h3>Condiciones de Suministro y Montaje Hospital Verge del Toro</h3>
    <ul>
"""
    for c in DATA["condiciones_comerciales"]:
        html += f"      <li>{c}</li>\n"

    html += f"""
    </ul>
  </div>

  <div class="footer-sig">
    <div class="sig-box">
      <div class="label">Por DIXIS Recursos y Soluciones S.L. / ALUFAC</div>
      <div style="font-size: 7pt; margin-top: 35px; color: #475569;">Fdo.: Pablo Sebastián Sánchez Arnoletto · Dpto. Técnico Menorca</div>
    </div>
    <div class="sig-box">
      <div class="label">Conforme el Cliente / Cobra Edificación Singular</div>
      <div style="font-size: 7pt; margin-top: 35px; color: #475569;">Fdo.: Fernando Sánchez Sánchez · Arquitecto Técnico</div>
    </div>
  </div>

  <!-- PÁGINA 2: DESGLOSE DETALLADO LÍNEA A LÍNEA DE MEDICIONES -->
  <div class="page-break"></div>

  <div class="header">
    <div class="logo-block">
      <h1>JUSTIFICACIÓN DETALLADA DE MEDICIONES Y PARTIDAS</h1>
      <div class="sub">HOSPITAL VERGE DEL TORO (MAHÓN) · CAPÍTULO H25 CARPINTERIA ALUMINIO</div>
    </div>
    <div class="doc-ref">
      <div class="doc-badge">ANEXO DE MEDICIONES</div>
      <p><strong>Plano Ref:</strong> AL.03.01 / AL.03.02</p>
    </div>
  </div>

  <table class="items" style="font-size: 7.5pt;">
    <thead>
      <tr>
        <th style="width: 75px;">Código</th>
        <th>Resumen / Concepto / Desglose de Huecos</th>
        <th class="center" style="width: 25px;">Nº</th>
        <th class="num" style="width: 40px;">Long.</th>
        <th class="num" style="width: 40px;">Anch.</th>
        <th class="num" style="width: 40px;">Alt.</th>
        <th class="num" style="width: 50px;">Parcial</th>
        <th class="num" style="width: 55px;">Total Partida</th>
        <th class="num" style="width: 55px;">Precio Ud.</th>
        <th class="num" style="width: 65px;">Importe (€)</th>
      </tr>
    </thead>
    <tbody>
"""

    for p in DATA["partidas"]:
        html += f"""
      <tr class="head-partida">
        <td><span class="code">{p['codigo']}</span></td>
        <td><strong>{p['resumen']}</strong></td>
        <td colspan="5"></td>
        <td class="num"><strong>{fmt_num(p['cantidad'])} {p['unidad']}</strong></td>
        <td class="num"><strong>{fmt_eur(p['precio_venta_unitario'])}</strong></td>
        <td class="num"><strong>{fmt_eur(p['subtotal'])}</strong></td>
      </tr>
      <tr>
        <td colspan="10" style="font-size: 6.8pt; color: #475569; background: #fafafa; padding: 3px 6px;">
          <em>{p['descripcion']}</em>
        </td>
      </tr>"""

        for d in p["desglose_medicion"]:
            dim_anch = f"{d['anchura']:.2f}" if d['anchura'] > 0 else "-"
            dim_alt = f"{d['altura']:.2f}" if d['altura'] > 0 else "-"
            html += f"""
      <tr class="meas">
        <td style="color: #94a3b8; font-size: 6.5pt;">Spc0010</td>
        <td>&bull; {d['etiqueta']}</td>
        <td class="center">{d['n']}</td>
        <td class="num">{d['longitud']:.2f}</td>
        <td class="num">{dim_anch}</td>
        <td class="num">{dim_alt}</td>
        <td class="num">{d['cantidad']:.2f}</td>
        <td colspan="3"></td>
      </tr>"""

    html += f"""
      <tr style="background: #fef3c7; font-weight: 800; border-top: 2px solid #0f172a;">
        <td colspan="7" style="text-align: right; padding: 6px;">TOTAL BASE IMPONIBLE CAPÍTULO H25:</td>
        <td class="num" style="padding: 6px;">{fmt_num(DATA['totales']['superficie_total_m2'])} m²</td>
        <td class="num" style="padding: 6px;"></td>
        <td class="num" style="padding: 6px; font-size: 9pt; color: #92400e;">{fmt_eur(DATA['totales']['base_imponible'])}</td>
      </tr>
    </tbody>
  </table>

</body>
</html>
"""
    html_path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML Cliente generado en: {html_path}")
    return html_path

def create_html_internal():
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Estudio Interno Técnico - Presupuesto {DATA['codigo']} - Nou Hospital Verge del Toro</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 12mm 14mm 12mm 14mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-size: 8pt;
    line-height: 1.35;
  }}
  .header {{
    border-bottom: 3px solid #b45309;
    padding-bottom: 6px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }}
  .header h1 {{
    margin: 0;
    font-size: 13pt;
    color: #0f172a;
  }}
  .badge {{
    background: #b45309;
    color: #ffffff;
    padding: 2px 8px;
    font-weight: 700;
    font-size: 7.5pt;
    border-radius: 3px;
  }}
  table.matrix {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.5pt;
    margin-bottom: 12px;
  }}
  table.matrix th {{
    background: #0f172a;
    color: #ffffff;
    padding: 4px 6px;
    font-weight: 700;
    border: 1px solid #0f172a;
  }}
  table.matrix th.num {{ text-align: right; }}
  table.matrix th.center {{ text-align: center; }}
  table.matrix td {{
    padding: 4px 6px;
    border: 1px solid #cbd5e1;
  }}
  table.matrix tr.even {{ background: #f8fafc; }}
  table.matrix td.num {{ text-align: right; }}
  table.matrix td.center {{ text-align: center; }}
  table.matrix tr.total {{
    background: #e2e8f0;
    font-weight: 700;
  }}
  .highlight {{
    color: #15803d;
    font-weight: 700;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 12px;
  }}
  .kpi-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 8px;
    text-align: center;
  }}
  .kpi-title {{
    font-size: 7pt;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 700;
  }}
  .kpi-val {{
    font-size: 11pt;
    color: #0f172a;
    font-weight: 800;
    margin-top: 3px;
  }}
  .kpi-val.green {{ color: #15803d; }}
  .kpi-val.blue {{ color: #0284c7; }}
  .notes-box {{
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #b45309;
    padding: 8px 10px;
    border-radius: 4px;
    font-size: 7.5pt;
  }}
  .notes-box h3 {{
    margin: 0 0 4px 0;
    color: #92400e;
    font-size: 8pt;
  }}
  .notes-box ul {{
    margin: 0;
    padding-left: 14px;
  }}
  .notes-box li {{
    margin-bottom: 2px;
    color: #78350f;
  }}
</style>
</head>
<body>

  <div class="header">
    <div>
      <h1>ESTUDIO TÉCNICO INTERNO Y ANÁLISIS DE RENTABILIDAD</h1>
      <div style="font-size: 8pt; color: #64748b; margin-top: 2px;">
        Expediente: <strong>{DATA['codigo']}</strong> · Ref: <strong>{DATA['referencia']}</strong> · Nou Hospital Verge del Toro (Mahón)
      </div>
    </div>
    <div style="text-align: right;">
      <span class="badge">ESTRICTAMENTE CONFIDENCIAL</span>
      <div style="font-size: 7.5pt; color: #64748b; margin-top: 3px;">Fecha: {DATA['fecha']}</div>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-title">Superficie Total</div>
      <div class="kpi-val blue">{fmt_num(DATA['totales']['superficie_total_m2'])} m²</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Coste Directo Total</div>
      <div class="kpi-val">{fmt_eur(DATA['totales']['coste_directo_total'])}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Venta Presupuestada (Base)</div>
      <div class="kpi-val">{fmt_eur(DATA['totales']['base_imponible'])}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Margen Bruto Total</div>
      <div class="kpi-val green">{fmt_eur(DATA['totales']['margen_bruto_total'])} ({DATA['totales']['margen_porcentaje_sobre_venta']}%)</div>
    </div>
  </div>

  <table class="matrix">
    <thead>
      <tr>
        <th class="center" style="width: 25px;">#</th>
        <th style="width: 75px;">Código</th>
        <th>Resumen de la Partida</th>
        <th class="num" style="width: 45px;">Med. (m²)</th>
        <th class="num" style="width: 60px;">Coste Ud.</th>
        <th class="num" style="width: 65px;">Coste Total</th>
        <th class="num" style="width: 60px;">Venta Ud.</th>
        <th class="num" style="width: 65px;">Venta Total</th>
        <th class="num" style="width: 60px;">Margen (€)</th>
        <th class="num" style="width: 50px;">% S/Vta</th>
      </tr>
    </thead>
    <tbody>
"""

    for p in DATA["partidas"]:
        row_cls = "even" if p["orden"] % 2 == 0 else ""
        m_eur = p["subtotal"] - p["coste_subtotal"]
        m_pct = (m_eur / p["subtotal"]) * 100 if p["subtotal"] > 0 else 0
        html += f"""
      <tr class="{row_cls}">
        <td class="center">{p['orden']}</td>
        <td><strong style="color: #0284c7;">{p['codigo']}</strong></td>
        <td><strong>{p['resumen']}</strong></td>
        <td class="num">{fmt_num(p['cantidad'])}</td>
        <td class="num">{fmt_eur(p['coste_unitario'])}</td>
        <td class="num">{fmt_eur(p['coste_subtotal'])}</td>
        <td class="num">{fmt_eur(p['precio_venta_unitario'])}</td>
        <td class="num"><strong>{fmt_eur(p['subtotal'])}</strong></td>
        <td class="num highlight">+{fmt_eur(m_eur)}</td>
        <td class="num highlight">{m_pct:.1f}%</td>
      </tr>"""

    html += f"""
      <tr class="total">
        <td colspan="3" style="text-align: right; padding: 6px;">TOTALES CONSOLIDADOS:</td>
        <td class="num">{fmt_num(DATA['totales']['superficie_total_m2'])}</td>
        <td class="num">-</td>
        <td class="num">{fmt_eur(DATA['totales']['coste_directo_total'])}</td>
        <td class="num">-</td>
        <td class="num">{fmt_eur(DATA['totales']['base_imponible'])}</td>
        <td class="num highlight">+{fmt_eur(DATA['totales']['margen_bruto_total'])}</td>
        <td class="num highlight">{DATA['totales']['margen_porcentaje_sobre_venta']}%</td>
      </tr>
    </tbody>
  </table>

  <div class="notes-box">
    <h3>Puntos Críticos Técnicos y Operativos para la Ejecución en Menorca:</h3>
    <ul>
      <li><strong>Lamas Tubulares COR-2847 (389,50 m²):</strong> Constituye el 41,4% del presupuesto total (126.587,50 €). Los módulos mr1 y mr2 alcanzan 13,50 metros de altura en fachadas hospitalarias. Es indispensable coordinar con Cobra la fase de andamiaje o el uso de PEMP telescópica/articulada y asegurar los anclajes estructurales a los forjados de hormigón.</li>
      <li><strong>Carpintería Millenium Plus 70 (33,00 m² de puertas dobles + 14,63 m² de puertas simples):</strong> Puertas de alto tránsito con ensayos a 500.000 ciclos. Equipadas con bisagras mecánicas de 3 palas para 220 kg y mecanismos antipánico certificados.</li>
      <li><strong>Serie Hoja Oculta Cortizo COR 60 (160 m² entre fijos, ventanas y balconeras):</strong> Estanqueidad Clase 9A y resistencia al viento C5. Acristalamiento laminado acústico 4+4/12/4+4 bajo emisivo en cumplimiento estricto del CTE y pliegos IB-SALUT.</li>
      <li><strong>Tratamiento Qualicoat Seaside:</strong> Decapado profundo de 2 g/m² para prevenir corrosión filiforme en el ambiente salino de Mahón.</li>
      <li><strong>Regla de Fabricación HAM:</strong> En piezas auxiliares o soportes de acero complementarios, nunca pintura al horno: siempre preparación mecánica St 3, imprimación anticorrosiva de adherencia y acabado con esmalte de poliuretano de dos componentes aplicado in situ o en taller.</li>
    </ul>
  </div>

</body>
</html>
"""
    html_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML Interno generado en: {html_path}")
    return html_path

def convert_html_to_pdf(html_path, pdf_path):
    if not os.path.exists(CHROME_PATH):
        print(f"Aviso: Chrome no encontrado en {CHROME_PATH}")
        return False
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"PDF generado con éxito: {pdf_path}")
        return True
    except Exception as e:
        print(f"Error generando PDF: {e}")
        return False

def create_readme():
    readme_content = f"""# Presupuesto {DATA['codigo']} · Nou Hospital Verge del Toro (Mahón)

- **Código:** `{DATA['codigo']}`
- **Referencia:** `{DATA['referencia']}`
- **Fecha de Emisión:** {DATA['fecha']}
- **Cliente:** {DATA['cliente']['empresa']}
- **Atención:** {DATA['cliente']['contacto']} ({DATA['cliente']['cargo']})
- **Teléfonos:** {DATA['cliente']['telefono']}
- **Sede:** {DATA['cliente']['direccion']}, {DATA['cliente']['codigo_postal']} {DATA['cliente']['poblacion']}
- **Web:** [{DATA['cliente']['web']}]({DATA['cliente']['web']})
- **Proyecto:** {DATA['proyecto']['titulo']}
- **Promotor:** {DATA['proyecto']['promotor']}
- **Emplazamiento:** {DATA['proyecto']['emplazamiento']}
- **Capítulo de Licitación:** {DATA['proyecto']['capitulo_codigo']} {DATA['proyecto']['capitulo_nombre']}
- **Planos de Referencia:** AL.03.01 (Portes i finestres) y AL.03.02 (Sèrie reixes)

---

## Resumen Económico Consolidado

| Concepto | Superficie (m²) | Coste Directo (€) | Venta Base Imponible (€) | Margen Bruto (€) | % Margen |
|---|---:|---:|---:|---:|---:|
| **Carpintería Aluminio RPT + Celosías + Mamparas** | **{fmt_num(DATA['totales']['superficie_total_m2'])} m²** | **{fmt_eur(DATA['totales']['coste_directo_total'])}** | **{fmt_eur(DATA['totales']['base_imponible'])}** | **+{fmt_eur(DATA['totales']['margen_bruto_total'])}** | **{DATA['totales']['margen_porcentaje_sobre_venta']}%** |

- **I.V.A. (21,0%):** {fmt_eur(DATA['totales']['iva_importe'])}
- **Total Presupuesto (con IVA):** **{fmt_eur(DATA['totales']['total_con_iva'])}**

---

## Archivos del Expediente

- [Presupuesto_P2026_0061_Hospital_Verge_del_Toro_Cobra.xlsx](file:///{os.path.join(BASE_DIR, "Presupuesto_P2026_0061_Hospital_Verge_del_Toro_Cobra.xlsx").replace(os.sep, "/")}): Libro de trabajo completo con 3 pestañas (Resumen Ejecutivo, Mediciones Detalladas línea a línea según CSV del proyecto, y Estudio Interno de Costes y Márgenes).
- [presupuesto-cliente.pdf](file:///{os.path.join(BASE_DIR, "presupuesto-cliente.pdf").replace(os.sep, "/")}): Documento oficial formal de oferta comercial presentado a Cobra Edificación Singular.
- [presupuesto-cliente.html](file:///{os.path.join(BASE_DIR, "presupuesto-cliente.html").replace(os.sep, "/")}): Versión HTML interactiva de alta definición para revisión directa.
- [presupuesto-interno-tecnico.pdf](file:///{os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf").replace(os.sep, "/")}): Informe técnico de costes, horas de taller y montaje, medios de elevación y ratios de rentabilidad.
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
