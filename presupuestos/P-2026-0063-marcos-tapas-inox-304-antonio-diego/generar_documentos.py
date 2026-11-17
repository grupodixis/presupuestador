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

    font_title = Font(name="Segoe UI", size=13, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=9.5, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=8.5, color="1E293B")
    font_tot = Font(name="Segoe UI", size=10.5, bold=True, color=NAVY)
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

    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["B2"].font = font_sub
    ws1["B3"] = f"PRESUPUESTO {DATA['codigo']} • 4 MARCOS Y TAPAS ESTANCAS INOX AISI 304 (60x60 CM)"
    ws1["B3"].font = font_title

    meta_rows = [
        ("REFERENCIA:", DATA["referencia"]),
        ("CLIENTE:", f"{DATA['cliente']['nombre']} · CIF: {DATA['cliente']['cif']}"),
        ("DOMICILIO:", f"{DATA['cliente']['domicilio']}"),
        ("OBRA / UBICACIÓN:", f"{DATA['cliente']['obra']} · {DATA['cliente']['ubicacion']}"),
        ("FECHA / VALIDEZ:", f"{DATA['fecha']} • Validez: {DATA['validez_dias']} días naturales"),
        ("CALIDAD / PROCESO:", f"{DATA['calidad_inox']} · {DATA['proceso_soldadura']}"),
    ]
    for idx, (k, v) in enumerate(meta_rows, start=5):
        ws1[f"B{idx}"] = k
        ws1[f"B{idx}"].font = font_bold
        ws1[f"C{idx}"] = v
        ws1[f"C{idx}"].font = font_reg

    ws1["B12"] = "DESGLOSE DE PARTIDAS (FABRICACIÓN EN TALLER Y ENTREGA)"
    ws1["B12"].font = font_sec

    headers_client = ["Nº", "Concepto y Descripción Técnica", "Ud.", "Cantidad", "Precio Unitario", "Subtotal"]
    for c_idx, h in enumerate(headers_client, start=2):
        cell = ws1.cell(row=13, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws1.row_dimensions[13].height = 24

    p = DATA["partida"]
    row_cur = 14
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
    ws1.row_dimensions[row_cur].height = 100

    # Totales
    r_tot = 16
    ws1.cell(row=r_tot, column=6, value="BASE IMPONIBLE:").font = font_bold
    c_bi = ws1.cell(row=r_tot, column=7, value=f"=G{row_cur}")
    c_bi.font = font_tot
    c_bi.number_format = '#,##0.00 "€"'
    c_bi.border = border_thin

    ws1.cell(row=r_tot+1, column=6, value="IVA (21%):").font = font_bold
    c_iva = ws1.cell(row=r_tot+1, column=7, value=f"=G{r_tot}*0.21")
    c_iva.font = font_reg
    c_iva.number_format = '#,##0.00 "€"'
    c_iva.border = border_thin

    ws1.cell(row=r_tot+2, column=6, value="TOTAL PRESUPUESTO:").font = font_tot_gold
    c_total = ws1.cell(row=r_tot+2, column=7, value=f"=G{r_tot}+G{r_tot+1}")
    c_total.font = font_tot_gold
    c_total.fill = fill_tot
    c_total.number_format = '#,##0.00 "€"'
    c_total.border = border_total

    # Condiciones comerciales
    r_cond = r_tot + 4
    ws1.cell(row=r_cond, column=2, value="CONDICIONES COMERCIALES Y ALCANCE").font = font_sec
    cond_items = [
        ("Forma de pago:", "100% a la aceptación del presupuesto (o según condiciones habituales de cliente)."),
        ("Plazo de fabricación:", "Aprox. 4 a 6 días laborables desde confirmación de pedido y medidas definitivas."),
        ("Lugar de entrega:", "Instalaciones / almacén de Antonio y Diego S.A. en Pol. Ind. POIMA, Mahón (Menorca)."),
        ("Garantía y Calidad:", "Acero Inoxidable AISI 304, soldadura TIG y decapado/pasivado de cordones según norma."),
        ("No incluye:", "Obra civil de colocación/recibido en albañilería, medios mecánicos especiales de descarga.")
    ]
    for c_i, (k_c, v_c) in enumerate(cond_items, start=r_cond+1):
        ws1.cell(row=c_i, column=2, value=k_c).font = font_bold
        ws1.cell(row=c_i, column=3, value=v_c).font = font_reg

    ws1.column_dimensions["B"].width = 10
    ws1.column_dimensions["C"].width = 68
    ws1.column_dimensions["D"].width = 8
    ws1.column_dimensions["E"].width = 11
    ws1.column_dimensions["F"].width = 16
    ws1.column_dimensions["G"].width = 16

    # -------------------------------------------------------------
    # HOJA 2: DESGLOSE DE COSTES Y ESTUDIO INTERNO
    # -------------------------------------------------------------
    ws2 = wb.create_sheet("Desglose Costes y Fabricacion")
    ws2.views.sheetView[0].showGridLines = True

    ws2["B2"] = f"ESTUDIO TÉCNICO Y ECONÓMICO INTERNO — {DATA['codigo']} (HAM ESTRUCTURAS METÁLICAS)"
    ws2["B2"].font = font_title

    headers_int = ["Concepto de Coste", "Descripción Técnica / Operativa", "Ud.", "Cant. Ud", "Coste Ud", "Coste Total (4 uds)", "Origen / Justificación"]
    for c_idx, h in enumerate(headers_int, start=2):
        cell = ws2.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_thin
    ws2.row_dimensions[4].height = 24

    cost_items = [
        ("Tapa chapa plegada", DATA["desglose_costes_unitario"]["tapa_chapa_plegada"]["concepto"], "ud", 4, 200.00, DATA["desglose_costes_unitario"]["tapa_chapa_plegada"]["origen"]),
        ("Marco angular L 40x40x4", DATA["desglose_costes_unitario"]["marco_angular_inox"]["concepto"], "conj", 4, 44.20, DATA["desglose_costes_unitario"]["marco_angular_inox"]["origen"]),
        ("Garras anclaje inox", DATA["desglose_costes_unitario"]["garras_anclaje_inox"]["concepto"], "juego", 4, 10.00, DATA["desglose_costes_unitario"]["garras_anclaje_inox"]["origen"]),
        ("Junta estanqueidad EPDM", DATA["desglose_costes_unitario"]["junta_estanqueidad_epdm"]["concepto"], "juego", 4, 15.00, DATA["desglose_costes_unitario"]["junta_estanqueidad_epdm"]["origen"]),
        ("Tornillería apriete + tirador", DATA["desglose_costes_unitario"]["apriete_estanco_tirador"]["concepto"], "juego", 4, 30.00, DATA["desglose_costes_unitario"]["apriete_estanco_tirador"]["origen"]),
        ("Consumibles taller TIG", DATA["desglose_costes_unitario"]["consumibles_taller"]["concepto"], "lote", 4, 18.00, DATA["desglose_costes_unitario"]["consumibles_taller"]["origen"]),
        ("Mano de obra taller TIG", DATA["desglose_costes_unitario"]["mo_taller_tig"]["concepto"], "h", 11.0, 35.00, DATA["desglose_costes_unitario"]["mo_taller_tig"]["origen"]),
        ("Transporte y entrega POIMA", DATA["desglose_costes_unitario"]["transporte_entrega"]["concepto"], "lote", 4, 10.00, DATA["desglose_costes_unitario"]["transporte_entrega"]["origen"]),
    ]

    r_c = 5
    for row_data in cost_items:
        ws2.cell(row=r_c, column=2, value=row_data[0]).font = font_bold
        ws2.cell(row=r_c, column=3, value=row_data[1]).font = font_reg
        ws2.cell(row=r_c, column=4, value=row_data[2]).alignment = Alignment(horizontal="center")
        
        c_q = ws2.cell(row=r_c, column=5, value=row_data[3])
        c_q.alignment = Alignment(horizontal="right")
        c_q.number_format = "#,##0.00"
        
        c_u = ws2.cell(row=r_c, column=6, value=row_data[4])
        c_u.number_format = '#,##0.00 "€"'
        c_u.fill = fill_edit
        c_u.font = font_bold
        
        c_t = ws2.cell(row=r_c, column=7, value=f"=E{r_c}*F{r_c}")
        c_t.number_format = '#,##0.00 "€"'
        c_t.font = font_bold
        
        c_orig = ws2.cell(row=r_c, column=8, value=row_data[5])
        c_orig.font = font_green if "cliente" in row_data[5].lower() else font_reg
        
        for col in range(2, 9):
            ws2.cell(row=r_c, column=col).border = border_thin
        r_c += 1

    # Totales internos
    ws2.cell(row=r_c+1, column=6, value="COSTE DIRECTO TOTAL:").font = font_tot
    c_tot_cost = ws2.cell(row=r_c+1, column=7, value=f"=SUM(G5:G{r_c-1})")
    c_tot_cost.font = font_tot
    c_tot_cost.number_format = '#,##0.00 "€"'
    c_tot_cost.border = border_thin

    ws2.cell(row=r_c+2, column=6, value="VENTA TOTAL CLIENTE:").font = font_tot
    c_tot_sale = ws2.cell(row=r_c+2, column=7, value=DATA["totales"]["base_imponible"])
    c_tot_sale.font = font_tot
    c_tot_sale.number_format = '#,##0.00 "€"'
    c_tot_sale.border = border_thin

    ws2.cell(row=r_c+3, column=6, value="BENEFICIO BRUTO:").font = font_green
    c_profit = ws2.cell(row=r_c+3, column=7, value=f"=G{r_c+2}-G{r_c+1}")
    c_profit.font = font_green
    c_profit.fill = fill_tot
    c_profit.number_format = '#,##0.00 "€"'
    c_profit.border = border_thin

    ws2.cell(row=r_c+4, column=6, value="MARGEN SOBRE VENTA:").font = font_green
    c_margin_v = ws2.cell(row=r_c+4, column=7, value=f"=G{r_c+3}/G{r_c+2}")
    c_margin_v.font = font_green
    c_margin_v.number_format = "0.00%"
    c_margin_v.border = border_total

    ws2.column_dimensions["B"].width = 24
    ws2.column_dimensions["C"].width = 62
    ws2.column_dimensions["D"].width = 8
    ws2.column_dimensions["E"].width = 10
    ws2.column_dimensions["F"].width = 14
    ws2.column_dimensions["G"].width = 18
    ws2.column_dimensions["H"].width = 32

    xlsx_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0063_Marcos_Tapas_Inox_Antonio_Diego.xlsx")
    wb.save(xlsx_path)
    return xlsx_path

def create_html_and_pdf():
    p = DATA["partida"]
    tot = DATA["totales"]

    # 1. HTML CLIENTE
    html_cliente = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presupuesto {DATA['codigo']} — Marcos y Tapas Inox AISI 304 (60x60 cm)</title>
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
    h1 {{ font-size: 11.5pt; color: #0f172a; margin: 0 0 6px 0; font-weight: 800; }}
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

  <h1>PRESUPUESTO {DATA['codigo']} — FABRICACIÓN DE 4 MARCOS ANGULARES Y TAPAS ESTANCAS EN ACERO INOXIDABLE AISI 304 (60x60 CM)</h1>
  <div class="banner-def">
    <strong>ALCANCE DEL SUMINISTRO:</strong> Conjuntos completos de arqueta/registro de 600x600 mm fabricados en taller mediante soldadura TIG, chapa plegada reforzada, junta elástica perimetral EPDM, sistema de apriete estanco perimetral y acabado decapado/pasivado.
  </div>

  <table class="meta">
    <tr>
      <td class="lbl">Cliente</td>
      <td><strong>{DATA['cliente']['nombre']}</strong> (CIF: {DATA['cliente']['cif']})</td>
      <td class="lbl">Referencia</td>
      <td><strong>{DATA['referencia']}</strong></td>
    </tr>
    <tr>
      <td class="lbl">Domicilio</td>
      <td>{DATA['cliente']['domicilio']}</td>
      <td class="lbl">Fecha</td>
      <td>{DATA['fecha']}</td>
    </tr>
    <tr>
      <td class="lbl">Atención / Obra</td>
      <td>{DATA['cliente']['contacto']} · {DATA['cliente']['obra']}</td>
      <td class="lbl">Validez</td>
      <td>{DATA['validez_dias']} días naturales</td>
    </tr>
    <tr>
      <td class="lbl">Calidad / Normativa</td>
      <td colspan="3">{DATA['calidad_inox']} · {DATA['proceso_soldadura']}</td>
    </tr>
  </table>

  <table class="items">
    <thead>
      <tr>
        <th class="center" style="width:6%">Nº</th>
        <th style="width:54%">Concepto y Descripción Técnica</th>
        <th class="center" style="width:6%">Ud.</th>
        <th class="right" style="width:10%">Cant.</th>
        <th class="right" style="width:12%">Precio Ud.</th>
        <th class="right" style="width:12%">Subtotal</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="center bold">{p['id']}</td>
        <td>
          <strong>{p['concepto']}</strong>
          <span class="desc">
            Suministro y fabricación a medida de conjunto de marco y tapa estanca de paso útil interior <strong>600 x 600 mm</strong> realizado íntegramente en acero inoxidable calidad AISI 304 (EN 1.4301).<br>
            • <strong>Tapa superior:</strong> ejecutada en chapa de acero inoxidable AISI 304 plegada con pestañas perimetrales descendentes a 90°, esquinas soldadas a TIG y rigidizadores de refuerzo interior. Dotada de tirador/asa escamoteable de acero inoxidable embutido enrasado para facilitar su izado sin resaltes.<br>
            • <strong>Marco angular perimetral:</strong> fabricado con perfil angular en L de 40x40x4 mm en acero inoxidable AISI 304, cortado a inglete a 45° y soldado a TIG, dotado exteriormente de 4 garras de anclaje en pletina inox para su perfecto empotramiento en obra civil.<br>
            • <strong>Estanqueidad:</strong> garantizada mediante asiento perimetral continuo con junta de estanqueidad de caucho celular EPDM de alta recuperación elástica, impermeable y resistente a intemperie.<br>
            • <strong>Sistema de apriete estanco:</strong> 4 puntos de apriete perimetral mediante tornillos de acero inoxidable A2 con arandela/junta elástica para asegurar una compresión uniforme y estanca.<br>
            • <strong>Acabado superficial:</strong> totalmente desbarbado, aristas pulidas, con cordones de soldadura decapados y pasivados químicamente para máxima resistencia a la corrosión.
          </span>
        </td>
        <td class="center">{p['unidad']}</td>
        <td class="right bold">{p['cantidad']:.2f}</td>
        <td class="right">{eur(p['precio_unitario'])}</td>
        <td class="right bold">{eur(p['subtotal'])}</td>
      </tr>
    </tbody>
  </table>

  <div class="totals-wrap">
    <table class="totals">
      <tr>
        <td class="bold">Base Imponible</td>
        <td class="right bold">{eur(tot['base_imponible'])}</td>
      </tr>
      <tr>
        <td>IVA Régimen General (21%)</td>
        <td class="right">{eur(tot['iva_importe'])}</td>
      </tr>
      <tr class="grand">
        <td>TOTAL PRESUPUESTO</td>
        <td class="right">{eur(tot['total_con_iva'])}</td>
      </tr>
    </table>
  </div>

  <div class="conds">
    <div class="conds-grid">
      <div>
        <h3>Condiciones Comerciales y Logística</h3>
        <ul>
          <li><strong>Forma de pago:</strong> 100% a la aceptación del presupuesto (o según acuerdo habitual).</li>
          <li><strong>Plazo de ejecución:</strong> 4 a 6 días laborables desde la confirmación del pedido.</li>
          <li><strong>Entrega incluida:</strong> Transporte y descarga en almacén/obra de Antonio y Diego SA (Pol. Ind. POIMA, Mahón).</li>
          <li><strong>Validez de la oferta:</strong> 30 días naturales.</li>
        </ul>
      </div>
      <div>
        <h3>Exclusiones y Aclaraciones Técnicas</h3>
        <ul>
          <li>No incluye trabajos de albañilería, demolición, vaciado ni recibido de marcos en obra.</li>
          <li>No incluye medios auxiliares especiales de izado distintos a transporte convencional.</li>
          <li>Instalación y anclaje químico/mecánico en obra a cargo del cliente/instalador.</li>
          <li>IVA aplicable del 21% desglosado en el resumen económico superior.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="footer-note">
    HAM Estructuras Metálicas Menorca · Dixis Recursos y Soluciones S.L. · CIF: B57825432 · Av. Circunval·lació 11, Pol. Sant Lluís · Registro Mercantil de Menorca
  </div>
</body>
</html>
"""

    # 2. HTML INTERNO TÉCNICO
    html_interno = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Estudio Interno Técnico {DATA['codigo']} — Marcos y Tapas Inox AISI 304</title>
  <style>
    @page {{ size: A4 landscape; margin: 10mm; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; margin: 0; font-size: 8.5pt; line-height: 1.35; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0f172a; padding-bottom: 6px; margin-bottom: 8px; }}
    .brand {{ font-size: 11pt; font-weight: 800; color: #0f172a; }}
    .tag {{ background: #0f172a; color: #fff; padding: 2px 6px; font-size: 7.5pt; font-weight: 700; border-radius: 3px; }}
    h1 {{ font-size: 11pt; color: #0f172a; margin: 0 0 4px 0; }}
    h2 {{ font-size: 9pt; color: #0f172a; margin: 10px 0 4px 0; border-bottom: 2px solid #b45309; padding-bottom: 2px; text-transform: uppercase; }}
    .banner {{ background: #ecfdf5; border-left: 4px solid #10b981; padding: 5px 8px; font-size: 8pt; color: #065f46; margin-bottom: 8px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; font-size: 8pt; }}
    th {{ background: #0f172a; color: #fff; padding: 5px; font-size: 7.5pt; text-align: left; }}
    td {{ padding: 4.5px 5px; border-bottom: 1px solid #cbd5e1; vertical-align: top; }}
    .right {{ text-align: right; }}
    .center {{ text-align: center; }}
    .bold {{ font-weight: 700; }}
    .green {{ color: #15803d; font-weight: 700; }}
    .tot {{ background: #fef3c7; font-weight: 800; }}
    .grid-2 {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 12px; }}
    .card {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 6px 10px; font-size: 7.5pt; border-radius: 4px; }}
    .card h3 {{ margin: 0 0 4px 0; font-size: 8pt; color: #0f172a; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand">HAM ESTRUCTURAS METÁLICAS · DOCUMENTO INTERNO DE COSTES Y PRODUCCIÓN</div>
    <div><span class="tag">USO INTERNO EXCLUSIVO</span> <span class="tag">{DATA['codigo']}</span></div>
  </div>

  <h1>ESTUDIO ECONÓMICO Y TÉCNICO: 4 MARCOS Y TAPAS INOX AISI 304 (60x60 CM) ESTANCAS</h1>
  <div class="banner">
    <strong>CLIENTE: ANTONIO Y DIEGO, S.A.</strong> | Coste unitario de tapa chapa plegada fijado en <strong>200,00 €/ud</strong> según prescripción. Se calculan perfiles angulares L 40x40x4 inox, juntas EPDM, apriete estanco, MO taller soldadura TIG y transporte.
  </div>

  <div class="grid-2">
    <div>
      <h2>1. Desglose Detallado de Costes Directos (Por Unidad y Total 4 Uds)</h2>
      <table>
        <thead>
          <tr>
            <th>Concepto de Coste</th>
            <th>Descripción Técnica</th>
            <th class="center">Ud.</th>
            <th class="right">Cant. Total</th>
            <th class="right">Coste Unit.</th>
            <th class="right">Coste Total</th>
            <th>Origen / Proveedor</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="bold">Tapas chapa plegada</td>
            <td>Chapa inox AISI 304 e=3 mm con pestañas a 90° y rigidización</td>
            <td class="center">ud</td>
            <td class="right bold">4.00</td>
            <td class="right">200,00 €</td>
            <td class="right bold">800,00 €</td>
            <td class="green">Coste fijado por cliente</td>
          </tr>
          <tr>
            <td class="bold">Marco angular L 40x40x4</td>
            <td>Angular inox AISI 304 (2,60 m x 4 = 10,40 m @ 2,42 kg/m = 25,2 kg @ 7 €/kg)</td>
            <td class="center">conj</td>
            <td class="right bold">4.00</td>
            <td class="right">44,20 €</td>
            <td class="right bold">176,80 €</td>
            <td>Tarifa perfiles inox</td>
          </tr>
          <tr>
            <td class="bold">Garras de anclaje inox</td>
            <td>4 pletinas inox 304 por marco para empotrar en obra (16 uds)</td>
            <td class="center">juego</td>
            <td class="right bold">4.00</td>
            <td class="right">10,00 €</td>
            <td class="right bold">40,00 €</td>
            <td>Taller inox HAM</td>
          </tr>
          <tr>
            <td class="bold">Junta estanqueidad EPDM</td>
            <td>Junta celular elástica EPDM resistente intemperie (2,40 m x 4 = 9,60 m)</td>
            <td class="center">juego</td>
            <td class="right bold">4.00</td>
            <td class="right">15,00 €</td>
            <td class="right bold">60,00 €</td>
            <td>Suministro técnico EPDM</td>
          </tr>
          <tr>
            <td class="bold">Apriete estanco + tirador</td>
            <td>4 tornillos inox A2 de apriete estanco + tirador escamoteable inox</td>
            <td class="center">juego</td>
            <td class="right bold">4.00</td>
            <td class="right">30,00 €</td>
            <td class="right bold">120,00 €</td>
            <td>Tornillería A2 y herrajes</td>
          </tr>
          <tr>
            <td class="bold">Consumibles TIG / acabado</td>
            <td>Argón puro, varilla TIG 304L, discos corte/repaso y gel decapante</td>
            <td class="center">lote</td>
            <td class="right bold">4.00</td>
            <td class="right">18,00 €</td>
            <td class="right bold">72,00 €</td>
            <td>Consumibles taller HAM</td>
          </tr>
          <tr>
            <td class="bold">MO Taller Soldador TIG</td>
            <td>Corte ingletes, armado, soldadura TIG, roscado M8, ajuste y pasivado (11 h)</td>
            <td class="center">h</td>
            <td class="right bold">11.00</td>
            <td class="right">35,00 €</td>
            <td class="right bold">385,00 €</td>
            <td>Oficial 1ª Taller TIG</td>
          </tr>
          <tr>
            <td class="bold">Transporte y entrega POIMA</td>
            <td>Embalaje con esquineras y porte directo a almacén Antonio y Diego</td>
            <td class="center">porte</td>
            <td class="right bold">1.00</td>
            <td class="right">40,00 €</td>
            <td class="right bold">40,00 €</td>
            <td>Logística interna Menorca</td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="tot">
            <td colspan="5" class="bold">COSTE DIRECTO TOTAL (4 UNIDADES):</td>
            <td class="right bold">{eur(tot['coste_directo_total'])}</td>
            <td>Coste medio: {eur(tot['coste_directo_total']/4)} / ud</td>
          </tr>
        </tfoot>
      </table>
    </div>

    <div>
      <h2>2. Rentabilidad Comercial y Márgenes</h2>
      <table>
        <thead>
          <tr>
            <th>Concepto Económico</th>
            <th class="right">Por Unidad</th>
            <th class="right">Total 4 Uds</th>
            <th class="right">% s/ Venta</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Coste Directo Fabricación</td>
            <td class="right">{eur(tot['coste_directo_total']/4)}</td>
            <td class="right">{eur(tot['coste_directo_total'])}</td>
            <td class="right">{(tot['coste_directo_total']/tot['base_imponible']*100):.2f}%</td>
          </tr>
          <tr class="bold">
            <td>Precio Venta Cliente (Base)</td>
            <td class="right">{eur(p['precio_unitario'])}</td>
            <td class="right">{eur(tot['base_imponible'])}</td>
            <td class="right">100,00%</td>
          </tr>
          <tr class="green">
            <td>BENEFICIO BRUTO COMERCIAL</td>
            <td class="right">+{eur(tot['beneficio_bruto']/4)}</td>
            <td class="right">+{eur(tot['beneficio_bruto'])}</td>
            <td class="right"><strong>{tot['margen_sobre_venta_pct']:.2f}%</strong></td>
          </tr>
          <tr>
            <td>Margen industrial s/ Coste</td>
            <td class="right">+{tot['margen_sobre_coste_pct']:.2f}%</td>
            <td class="right">+{tot['margen_sobre_coste_pct']:.2f}%</td>
            <td class="right">—</td>
          </tr>
          <tr>
            <td>IVA Repercutido (21%)</td>
            <td class="right">{eur(tot['iva_importe']/4)}</td>
            <td class="right">{eur(tot['iva_importe'])}</td>
            <td class="right">—</td>
          </tr>
          <tr class="tot">
            <td>TOTAL PRESUPUESTO CLIENTE</td>
            <td class="right">{eur(tot['total_con_iva']/4)}</td>
            <td class="right">{eur(tot['total_con_iva'])}</td>
            <td class="right">—</td>
          </tr>
        </tbody>
      </table>

      <div class="card">
        <h3>Observaciones para el Taller</h3>
        <p>• <strong>Control de medidas:</strong> Verificar que la luz interior del marco terminado sea exactamente de 602x602 mm para permitir una holgura perimetral de 2 mm por lado respecto a la tapa plegada de 598x598 mm.<br>
        • <strong>Estanqueidad:</strong> La junta de EPDM celular debe colocarse perimetralmente en el ala horizontal del ángulo, asegurando unión en inglete sin huecos en esquinas.<br>
        • <strong>Pasivado:</strong> Aplicar gel decapante especial inox en todas las soldaduras TIG, dejar actuar 20 minutos y neutralizar con agua a presión antes de montar la junta y la tornillería.</p>
      </div>
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
            subprocess.run([
                CHROME_PATH, "--headless", "--disable-gpu",
                "--no-pdf-header-footer", f"--print-to-pdf={p_path}", h_path
            ], check=False)

    return cli_html, int_html, cli_pdf, int_pdf

def create_readme():
    tot = DATA["totales"]
    p = DATA["partida"]
    content = f"""# Presupuesto {DATA['codigo']} — 4 Marcos y Tapas Estancas Inox AISI 304 (60x60 cm)

## Cliente y Datos Generales
- **Código:** {DATA['codigo']}
- **Referencia:** {DATA['referencia']}
- **Cliente:** {DATA['cliente']['nombre']} (CIF: {DATA['cliente']['cif']})
- **Domicilio:** {DATA['cliente']['domicilio']}
- **Contacto:** {DATA['cliente']['contacto']}
- **Fecha:** {DATA['fecha']}
- **Validez:** {DATA['validez_dias']} días naturales
- **Materiales:** {DATA['calidad_inox']}
- **Procedimiento:** {DATA['proceso_soldadura']}

## Resumen del Trabajo
Fabricación en taller de herrería y cerrajería inoxidable mediante soldadura TIG con argón puro de **4 conjuntos de marco angular y tapa estanca de 600 x 600 mm útiles**.
- **Tapas de chapa plegada:** Chapa de acero inoxidable AISI 304 con pestañas plegadas a 90°, refuerzos rigidizadores y tirador embutido escamoteable. Coste directo de las tapas de chapa plegada: **200,00 € / ud** (fijado por el cliente).
- **Marcos angulares perimetrales:** Perfil angular en L de 40x40x4 mm en acero inoxidable AISI 304 cortado a inglete a 45° y soldado a TIG, dotado de 4 garras de anclaje de pletina inox por marco para empotramiento en obra civil.
- **Estanqueidad:** Asiento perimetral con junta técnica de caucho celular EPDM de alta recuperación elástica.
- **Sistema de apriete:** 4 tornillos de acero inoxidable A2 con junta elastomérica para cierre estanco a presión.
- **Acabado:** Decapado y pasivado químico completo de todas las soldaduras.
- **Entrega:** Incluido embalaje protector y transporte a las instalaciones de Antonio y Diego SA en el Polígono Industrial POIMA (Mahón).

## Resumen Económico

| Concepto | Coste Directo | Venta Cliente (PVP) | Beneficio Bruto | Margen s/ Venta |
|---|---:|---:|---:|---:|
| **Por Unidad (ud)** | {eur(tot['coste_directo_total']/4)} | {eur(p['precio_unitario'])} | +{eur(tot['beneficio_bruto']/4)} | {tot['margen_sobre_venta_pct']:.2f}% |
| **Total 4 Unidades** | **{eur(tot['coste_directo_total'])}** | **{eur(tot['base_imponible'])}** | **+{eur(tot['beneficio_bruto'])}** | **{tot['margen_sobre_venta_pct']:.2f}%** |

- **Base Imponible:** {eur(tot['base_imponible'])}
- **IVA (21%):** {eur(tot['iva_importe'])}
- **Total Presupuesto:** {eur(tot['total_con_iva'])}

## Archivos Generados
- `presupuesto-cliente.html` / `presupuesto-cliente.pdf`: Documento comercial para entregar al cliente.
- `presupuesto-interno-tecnico.html` / `presupuesto-interno-tecnico.pdf`: Desglose interno técnico y económico para taller y dirección.
- `Presupuesto_P2026_0063_Marcos_Tapas_Inox_Antonio_Diego.xlsx`: Hoja de cálculo completa con fórmulas activas, hoja de cliente y hoja de desglose de costes.
- `datos.json`: Fuente de datos estructurada del presupuesto.
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    return readme_path

if __name__ == "__main__":
    xlsx = create_excel()
    cli_h, int_h, cli_p, int_p = create_html_and_pdf()
    rd = create_readme()
    print("Archivos generados con éxito:")
    for f in [xlsx, cli_h, cli_p, int_h, int_p, rd]:
        print(f" - {f}")
