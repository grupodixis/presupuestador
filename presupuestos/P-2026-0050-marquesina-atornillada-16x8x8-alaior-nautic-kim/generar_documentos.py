import os
import sys
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

def create_excel():
    wb = Workbook()
    
    # Colores corporativos Dixis / HAM
    NAVY = "0F172A"       # Fondo cabecera principal
    GOLD = "B45309"       # Acento dorado / óxido
    SLATE_LIGHT = "F8FAFC" # Fila alterna
    SLATE_HEADER = "1E293B"
    SUBHEADER_FILL = "E2E8F0"
    TOTAL_FILL = "FEF3C7"  # Amarillo cálido
    SECTION_FILL = "F1F5F9"
    HIGHLIGHT_GREEN = "047857"
    
    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub = PatternFill(start_color=SUBHEADER_FILL, end_color=SUBHEADER_FILL, fill_type="solid")
    fill_sec = PatternFill(start_color=SECTION_FILL, end_color=SECTION_FILL, fill_type="solid")
    fill_alt = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type="solid")
    fill_tot = PatternFill(start_color=TOTAL_FILL, end_color=TOTAL_FILL, fill_type="solid")
    
    font_title = Font(name="Segoe UI", size=15, bold=True, color=NAVY)
    font_sub = Font(name="Segoe UI", size=10, bold=True, color=GOLD)
    font_header = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
    font_sec = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=9, bold=True, color="000000")
    font_reg = Font(name="Segoe UI", size=9, color="1E293B")
    font_italic = Font(name="Segoe UI", size=8.5, italic=True, color="64748B")
    font_tot = Font(name="Segoe UI", size=11, bold=True, color=NAVY)
    font_tot_gold = Font(name="Segoe UI", size=11, bold=True, color=GOLD)

    border_thin = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    border_total = Border(
        top=Side(style='thin', color=NAVY),
        bottom=Side(style='double', color=NAVY)
    )

    # -------------------------------------------------------------------------
    # HOJA 1: RESUMEN EJECUTIVO COMERCIAL
    # -------------------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Resumen Ejecutivo"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["B2"] = "DIXIS RECURSOS Y SOLUCIONES S.L. | HAM ESTRUCTURAS METÁLICAS"
    ws1["B2"].font = font_title
    ws1["B3"] = "OFERTA TÉCNICO-COMERCIAL: MARQUESINA INDUSTRIAL ATORNILLABLE 16x8x8 m (150 m²)"
    ws1["B3"].font = font_sub
    
    # Ficha técnica
    info_rows = [
        ("Código de Oferta:", DATA["codigo"], "Fecha de Emisión:", DATA["fecha"]),
        ("Cliente:", DATA["cliente"]["empresa"], "Atención / Contacto:", f"{DATA['cliente']['contacto']} ({DATA['cliente']['telefono']})"),
        ("Email Contacto:", DATA["cliente"]["email"], "Ubicación Obra:", DATA["proyecto"]["ubicacion"]),
        ("Dimensiones Base:", "16,00 m x 8,00 m (Luz libre 8 m)", "Altura Libre Alero:", "8,00 m (Cumbrera 8,60 m)"),
        ("Superficie Techada:", "150,30 m² con aleros", "Cubierta:", "Panel Sándwich 30 mm PUR + Remates"),
        ("Sistema Constructivo:", "100% Atornillable (Mecano)", "Acabado Pintura:", "Imprimación Epoxi + Esmalte Poliuretano 2C (Sin horno)"),
        ("Acero Estructural:", "6.471 kg Acero S275JR", "Ratio Estructural:", "43,05 kg acero / m²"),
    ]
    
    r = 5
    for c1, v1, c2, v2 in info_rows:
        ws1.cell(row=r, column=2, value=c1).font = font_bold
        ws1.cell(row=r, column=3, value=v1).font = font_reg
        ws1.cell(row=r, column=5, value=c2).font = font_bold
        ws1.cell(row=r, column=6, value=v2).font = font_reg
        for col in [2,3,5,6]:
            ws1.cell(row=r, column=col).border = border_thin
        r += 1
        
    r += 1
    ws1.cell(row=r, column=2, value="RESUMEN ECONÓMICO DE LA OFERTA").font = font_sec
    r += 1
    
    headers_res = ["Nº", "Descripción de la Partida", "Unidad", "Cantidad", "Precio Unitario", "Importe Neto (€)"]
    for col_idx, h in enumerate(headers_res, start=2):
        c = ws1.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [2,4,5] else ("right" if col_idx == 7 else "left"))
        c.border = border_thin
    
    r_start_partidas = r + 1
    r += 1
    for p in DATA["presupuesto_cliente"]["partidas"]:
        ws1.cell(row=r, column=2, value=p["num"]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r, column=3, value=p["concepto"])
        ws1.cell(row=r, column=4, value=p["unidad"]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r, column=5, value=p["cantidad"]).alignment = Alignment(horizontal="right")
        ws1.cell(row=r, column=6, value=p["precio_unitario"]).alignment = Alignment(horizontal="right")
        ws1.cell(row=r, column=7, value=f"=E{r}*F{r}").alignment = Alignment(horizontal="right")
        
        ws1.cell(row=r, column=5).number_format = '#,##0.00' if isinstance(p["cantidad"], float) else '#,##0'
        ws1.cell(row=r, column=6).number_format = '#,##0.00 €'
        ws1.cell(row=r, column=7).number_format = '#,##0.00 €'
        
        for col_idx in range(2, 8):
            ws1.cell(row=r, column=col_idx).font = font_reg
            ws1.cell(row=r, column=col_idx).border = border_thin
            if r % 2 == 0:
                ws1.cell(row=r, column=col_idx).fill = fill_alt
        r += 1
        
    r_end_partidas = r - 1
    
    # Totales
    ws1.cell(row=r, column=6, value="SUBTOTAL NETO (B.I.):").font = font_bold
    c_subtot = ws1.cell(row=r, column=7, value=f"=SUM(G{r_start_partidas}:G{r_end_partidas})")
    c_subtot.font = font_tot
    c_subtot.number_format = '#,##0.00 €'
    c_subtot.border = border_thin
    r += 1
    
    ws1.cell(row=r, column=6, value="I.V.A. (21%):").font = font_reg
    c_iva = ws1.cell(row=r, column=7, value=f"=G{r-1}*0.21")
    c_iva.font = font_reg
    c_iva.number_format = '#,##0.00 €'
    c_iva.border = border_thin
    r += 1
    
    ws1.cell(row=r, column=6, value="TOTAL PRESUPUESTO (€):").font = font_tot_gold
    c_tot = ws1.cell(row=r, column=7, value=f"=G{r-2}+G{r-1}")
    c_tot.font = font_tot_gold
    c_tot.fill = fill_tot
    c_tot.number_format = '#,##0.00 €'
    c_tot.border = border_total
    
    # -------------------------------------------------------------------------
    # HOJA 2: PRESUPUESTO TÉCNICO INTERNO (DESGLOSE Y ESCANDALLO)
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Presupuesto Tecnico Interno")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["B2"] = "PRESUPUESTO TÉCNICO INTERNO Y DESGLOSE OPERATIVO DE TAREAS"
    ws2["B2"].font = font_title
    ws2["B3"] = "Costes directos, horas de mano de obra técnica/taller/montaje y maquinaria (H=8 m)"
    ws2["B3"].font = font_sub
    
    headers_tec = ["Fase / Tarea Operativa", "Descripción del Trabajo y Medios", "Tipo Recurso", "Horas / Uds", "Coste Unit. (€)", "Coste Subtotal (€)"]
    r = 5
    for col_idx, h in enumerate(headers_tec, start=2):
        c = ws2.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [4,5] else ("right" if col_idx == 7 else "left"))
        c.border = border_thin
    
    tec_tasks = [
        ("1. INGENIERÍA Y OFICINA TÉCNICA", "Modelado 3D BIM, cálculo estructural CTE DB-SE-AE (viento Alaior), planos taller y despiece", "Ingeniero", 24, 26.00),
        ("2. TALLER: CORTE Y PREPARACIÓN", "Corte con cinta, biselado de perfiles (Tubo 180, IPE 240, Tubo 120, 100x50)", "Oficial 1ª", 28, 26.00),
        ("3. TALLER: MECANIZADO Y TALADRADO", "Taladrado de placas base e=20, rigidizadores, agujeros pasantes para tornillos M16/M20 8.8", "Oficial 1ª", 36, 26.00),
        ("4. TALLER: ARMADO Y SOLDADURA", "Soldeo MAG de placas base a pilares, cartelas de nudos, jabalcones y ensambles previos", "Oficial Soldador", 44, 26.00),
        ("5. TALLER: TRATAMIENTO SUPERFICIAL", "Chorreado/limpieza Sa 2.5, imprimación epoxi bicomponente y esmalte poliuretano 2C (Sin horno)", "Pintor Taller", 32, 26.00),
        ("6. OBRA: REPLANTEO Y ANCLAJES", "Replanteo topográfico, taladro e inyección de 40 anclajes químicos M20 Hilti HIT-HY en solera", "Cuadrilla 2 op.", 12, 28.00),
        ("7. OBRA: MONTAJE PÓRTICOS (H=8 m)", "Elevación y aplomado de 10 pilares de 8 m y 5 dinteles IPE 240 con camión grúa", "Cuadrilla 3 op.", 72, 28.00),
        ("8. OBRA: ATADO Y CORREAS (H=8 m)", "Instalación de vigas atado 120x120, 8 líneas de correas y arriostramientos con PEMP 12 m", "Cuadrilla 3 op.", 60, 28.00),
        ("9. OBRA: TECHADO PANEL SÁNDWICH", "Colocación de 150,3 m² panel sándwich PUR 30 mm, fijaciones estancas EPDM y remates", "Cuadrilla 3 op.", 54, 28.00),
        ("10. OBRA: PLUVIALES Y CANALÓN", "Instalación de canalón galvanizado prelacado 400 mm (16,7 ml) y 2 bajantes a pie de pilar", "Cuadrilla 2 op.", 14, 28.00),
        ("11. OBRA: CONTROL CALIDAD Y PINTURA", "Apriete dinamométrico tornillería 8.8, repaso de pintura poliuretano en cabezas y entrega", "Jefe Equipo", 10, 28.00),
    ]
    
    r_start_tec = r + 1
    r += 1
    for t_nom, t_desc, t_rec, t_h, t_cost in tec_tasks:
        ws2.cell(row=r, column=2, value=t_nom).font = font_bold
        ws2.cell(row=r, column=3, value=t_desc).font = font_reg
        ws2.cell(row=r, column=4, value=t_rec).font = font_reg
        ws2.cell(row=r, column=4).alignment = Alignment(horizontal="center")
        ws2.cell(row=r, column=5, value=t_h).font = font_bold
        ws2.cell(row=r, column=5).alignment = Alignment(horizontal="right")
        ws2.cell(row=r, column=5).number_format = '#,##0.00'
        ws2.cell(row=r, column=6, value=t_cost).font = font_reg
        ws2.cell(row=r, column=6).alignment = Alignment(horizontal="right")
        ws2.cell(row=r, column=6).number_format = '#,##0.00 €'
        ws2.cell(row=r, column=7, value=f"=E{r}*F{r}").font = font_reg
        ws2.cell(row=r, column=7).alignment = Alignment(horizontal="right")
        ws2.cell(row=r, column=7).number_format = '#,##0.00 €'
        
        for col_idx in range(2, 8):
            ws2.cell(row=r, column=col_idx).border = border_thin
            if r % 2 == 0:
                ws2.cell(row=r, column=col_idx).fill = fill_alt
        r += 1
        
    r_end_tec = r - 1
    
    ws2.cell(row=r, column=4, value="TOTAL HORAS:").font = font_bold
    ws2.cell(row=r, column=5, value=f"=SUM(E{r_start_tec}:E{r_end_tec})").font = font_bold
    ws2.cell(row=r, column=5).number_format = '#,##0 horas'
    ws2.cell(row=r, column=6, value="COSTE MANO DE OBRA:").font = font_bold
    c_mo = ws2.cell(row=r, column=7, value=f"=SUM(G{r_start_tec}:G{r_end_tec})")
    c_mo.font = font_bold
    c_mo.number_format = '#,##0.00 €'
    c_mo.border = border_thin
    r += 2
    
    # Escandallo de costes directos y margen
    ws2.cell(row=r, column=2, value="ESCANDALLO ECONÓMICO DIRECTO Y MÁRGENES").font = font_sec
    r += 1
    
    escandallo_items = [
        ("Coste Acero Estructural S275JR (6.471 kg suministrado y cortado)", DATA["escandallo_interno"]["coste_materiales_acero"]),
        ("Coste Panel Sándwich PUR 30 mm y Rematería (150,3 m² + remates)", DATA["escandallo_interno"]["coste_materiales_panel_remates"]),
        ("Coste Pintura HAM (Imprimación Epoxi 2C + Poliuretano Alifático 2C exterior)", DATA["escandallo_interno"]["coste_pintura_consumibles"]),
        ("Coste Tornillería Estructural 8.8 cincada y Anclajes Químicos Hilti", DATA["escandallo_interno"]["coste_tornilleria_anclajes"]),
        ("Coste Mano de Obra Taller e Ingeniería (164 h)", DATA["escandallo_interno"]["coste_mano_obra_taller"] + DATA["escandallo_interno"]["coste_oficina_tecnica"]),
        ("Coste Mano de Obra Montaje en Obra Alaior (222 h)", DATA["escandallo_interno"]["coste_mano_obra_montaje"]),
        ("Coste Medios Auxiliares (Camión Grúa 16h + Plataforma Elevadora PEMP 12m)", DATA["escandallo_interno"]["coste_medios_auxiliares_grua_pemp"]),
        ("Coste Transporte material despiezado en camión (1 viaje a Alaior)", DATA["escandallo_interno"]["coste_transporte"]),
    ]
    
    r_start_esc = r
    for item_nom, item_val in escandallo_items:
        ws2.cell(row=r, column=2, value=item_nom).font = font_reg
        ws2.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        ws2.cell(row=r, column=6, value=item_val).font = font_reg
        ws2.cell(row=r, column=6).number_format = '#,##0.00 €'
        for c in range(2, 7):
            ws2.cell(row=r, column=c).border = border_thin
        r += 1
    r_end_esc = r - 1
    
    ws2.cell(row=r, column=2, value="TOTAL COSTE DIRECTO (CD):").font = font_bold
    ws2.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    ws2.cell(row=r, column=6, value=f"=SUM(F{r_start_esc}:F{r_end_esc})").font = font_bold
    ws2.cell(row=r, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=r, column=6).fill = fill_sec
    r += 1
    
    ws2.cell(row=r, column=2, value="Gastos Generales (10,0%):").font = font_reg
    ws2.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    ws2.cell(row=r, column=6, value=f"=F{r-1}*0.10").font = font_reg
    ws2.cell(row=r, column=6).number_format = '#,##0.00 €'
    r += 1
    
    ws2.cell(row=r, column=2, value="Beneficio Industrial (19,1%):").font = font_reg
    ws2.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    ws2.cell(row=r, column=6, value=f"=F{r-2}*0.19075").font = font_reg
    ws2.cell(row=r, column=6).number_format = '#,##0.00 €'
    r += 1
    
    ws2.cell(row=r, column=2, value="PRECIO DE VENTA NETO FINAL (PVP Base Imponible):").font = font_tot_gold
    ws2.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    c_pvp = ws2.cell(row=r, column=6, value=f"=F{r-3}+F{r-2}+F{r-1}")
    c_pvp.font = font_tot_gold
    c_pvp.fill = fill_tot
    c_pvp.number_format = '#,##0.00 €'
    c_pvp.border = border_total

    # -------------------------------------------------------------------------
    # HOJA 3: ESCANDALLO DE ACERO Y CÁLCULO ESTRUCTURAL (KG)
    # -------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="Desglose Acero y Calculo")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3["B2"] = "DIMENSIONAMIENTO Y DESGLOSE ANALÍTICO DE ACERO ESTRUCTURAL"
    ws3["B2"].font = font_title
    ws3["B3"] = "Justificación de kilogramos de hierro S275JR según CTE DB-SE-A y DB-SE-AE (Alaior Zona C)"
    ws3["B3"].font = font_sub
    
    headers_acero = ["Elemento Estructural", "Perfil Adoptado", "Uds", "Long. Unit. (m)", "Metros Totales", "Kg / ml", "Peso Total (kg)", "Criterio / Norma"]
    r = 5
    for col_idx, h in enumerate(headers_acero, start=2):
        c = ws3.cell(row=r, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if col_idx in [4,5,6,7,8] else "left")
        c.border = border_thin
        
    acero_items = [
        ("Pilares Principales", "Tubo hueco 180x180x6 mm", 10, 8.00, "=D6*E6", 31.70, "=F6*G6", "Pandeo H=8m, lambda=90, chi=0.55"),
        ("Dinteles de Pórticos", "Viga IPE 240", 5, 8.00, "=D7*E7", 30.70, "=F7*G7", "Luz 8m (ef. 6m), Wz=324cm3, f<L/400"),
        ("Jabalcones Refuerzo Nudos (45°)", "Tubo hueco 100x100x4 mm", 10, 1.40, "=D8*E8", 11.70, "=F8*G8", "Triangulación nudo pilar-dintel"),
        ("Vigas de Atado Coronación", "Tubo hueco 120x120x5 mm", 2, 16.00, "=D9*E9", 17.50, "=F9*G9", "Atado longitudinal cabezas pilares"),
        ("Correas de Cubierta", "Tubo rectangular 100x50x3 mm", 8, 16.70, "=D10*E10", 6.62, "=F10*G10", "Apoyo sándwich 30mm, intereje 1.25m"),
        ("Cruces de San Andrés (Fachadas)", "Redondo macizo Ø20 mm", 8, 9.00, "=D11*E11", 2.47, "=F11*G11", "Arriostramiento vertical viento Alaior"),
        ("Cruces de San Andrés (Cubierta)", "Redondo macizo Ø20 mm", 4, 9.00, "=D12*E12", 2.47, "=F12*G12", "Viga cortante en plano cubierta"),
        ("Placas Base Anclaje (350x350x20)", "Chapa S275JR e=20 mm", 10, 0.35, "10 uds", 19.23, 192.30, "Placa base pilar con 4 taladros Ø26"),
        ("Cartelas Base Rigidizadoras", "Chapa S275JR e=10 mm", 40, 0.15, "40 uds", 2.00, 80.00, "Rigidizadores triangulares en placas base"),
        ("Placas Cabeza y Uniones Mecano", "Chapa S275JR e=15 mm", 20, 0.30, "20 uds", 10.50, 210.00, "Placas frontales unión atornillada"),
        ("Casquillos y Ángulos fijación correas", "Angular 80x80x8 mm", 40, 0.12, "40 uds", 3.00, 120.00, "Casquillos soldados a dintel para atornillar"),
        ("Tornillería Estructural Cincada", "M16 y M20 Calidad 8.8", 1, 1.00, "Global", 110.00, 110.00, "Tornillos pretensados, arandelas y tuercas")
    ]
    
    r_start_acero = r + 1
    r += 1
    for el, per, uds, l_u, l_t, w_m, w_t, obs in acero_items:
        ws3.cell(row=r, column=2, value=el).font = font_bold
        ws3.cell(row=r, column=3, value=per).font = font_reg
        ws3.cell(row=r, column=4, value=uds).alignment = Alignment(horizontal="center")
        ws3.cell(row=r, column=5, value=l_u).alignment = Alignment(horizontal="right")
        ws3.cell(row=r, column=6, value=l_t).alignment = Alignment(horizontal="right")
        ws3.cell(row=r, column=7, value=w_m).alignment = Alignment(horizontal="right")
        ws3.cell(row=r, column=8, value=w_t).alignment = Alignment(horizontal="right")
        ws3.cell(row=r, column=9, value=obs).font = font_italic
        
        ws3.cell(row=r, column=4).number_format = '#,##0'
        if isinstance(l_u, (int, float)):
            ws3.cell(row=r, column=5).number_format = '#,##0.00 m'
        if isinstance(w_m, (int, float)):
            ws3.cell(row=r, column=7).number_format = '#,##0.00 kg/m'
        if isinstance(w_t, (int, float)):
            ws3.cell(row=r, column=8).number_format = '#,##0.00 kg'
        else:
            ws3.cell(row=r, column=8).number_format = '#,##0.00 kg'
            
        for c in range(2, 10):
            ws3.cell(row=r, column=c).border = border_thin
            if r % 2 == 0:
                ws3.cell(row=r, column=c).fill = fill_alt
        r += 1
        
    r_end_acero = r - 1
    
    ws3.cell(row=r, column=2, value="TOTAL KILOGRAMOS DE ACERO S275JR:").font = font_tot
    ws3.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    c_tot_kg = ws3.cell(row=r, column=8, value=f"=SUM(H{r_start_acero}:H{r_end_acero})")
    c_tot_kg.font = font_tot_gold
    c_tot_kg.fill = fill_tot
    c_tot_kg.number_format = '#,##0.00 kg'
    c_tot_kg.border = border_total
    
    # Autoajuste de columnas
    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or '')
                if len(val) > max_len and not cell.coordinate in ws.merged_cells:
                    max_len = len(val)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 11)
            
    ws1.column_dimensions["A"].width = 3
    ws1.column_dimensions["B"].width = 18
    ws1.column_dimensions["C"].width = 46
    ws1.column_dimensions["D"].width = 12
    ws1.column_dimensions["E"].width = 15
    ws1.column_dimensions["F"].width = 18
    ws1.column_dimensions["G"].width = 20
    
    excel_path = os.path.join(BASE_DIR, "Presupuesto_P2026_0050_Marquesina_Nautic_KIM.xlsx")
    wb.save(excel_path)
    print(f"Excel generado con éxito en: {excel_path}")
    return excel_path

def create_html_client():
    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presupuesto P-2026-0050: Marquesina Industrial Atornillable 16x8x8m - Nautic KIM</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 12mm 14mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #f8fafc;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 9.5px;
      line-height: 1.45;
    }}
    .sheet {{
      width: 210mm;
      margin: 0 auto;
      background: #ffffff;
      padding: 12mm 15mm;
    }}
    header {{
      background: #0f172a;
      color: #fff;
      padding: 16px 20px;
      border-radius: 8px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 16px;
      align-items: center;
      border-bottom: 4px solid #b45309;
      margin-bottom: 14px;
    }}
    .brand {{ display: flex; align-items: center; gap: 14px; }}
    .brand-title {{ font-size: 15px; font-weight: 800; letter-spacing: 0.5px; color: #ffffff; text-transform: uppercase; }}
    .brand-sub {{ font-size: 8.5px; color: #94a3b8; margin-top: 2px; }}
    .header-doc {{ text-align: right; }}
    .doc-num {{ font-size: 13px; font-weight: 800; color: #fbbf24; }}
    .doc-date {{ font-size: 8.5px; color: #cbd5e1; }}
    
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px; }}
    .card-title {{ font-size: 9px; font-weight: 800; text-transform: uppercase; color: #b45309; margin-bottom: 6px; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }}
    .card-line {{ display: flex; justify-content: space-between; margin-bottom: 3px; }}
    .card-label {{ color: #64748b; font-weight: 600; }}
    .card-val {{ color: #0f172a; font-weight: 700; text-align: right; }}

    .highlight-banner {{
      background: #eff6ff;
      border-left: 4px solid #2563eb;
      padding: 8px 12px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-around;
      font-size: 9px;
    }}
    .hb-item {{ text-align: center; }}
    .hb-val {{ font-size: 11px; font-weight: 800; color: #1e3a8a; }}
    .hb-lbl {{ font-size: 8px; color: #475569; text-transform: uppercase; font-weight: 600; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 14px;
    }}
    th {{
      background: #0f172a;
      color: #ffffff;
      font-weight: 700;
      font-size: 8.5px;
      text-transform: uppercase;
      padding: 7px 8px;
      text-align: left;
      border: 1px solid #0f172a;
    }}
    th.r, td.r {{ text-align: right; }}
    th.c, td.c {{ text-align: center; }}
    td {{
      padding: 7px 8px;
      border: 1px solid #e2e8f0;
      font-size: 8.5px;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: #f8fafc; }}
    .desc-text {{ font-size: 8px; color: #475569; margin-top: 3px; line-height: 1.35; }}

    .totals-area {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 14px;
    }}
    .totals-box {{
      width: 250px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      overflow: hidden;
    }}
    .t-row {{
      display: flex;
      justify-content: space-between;
      padding: 6px 10px;
      font-size: 9px;
      border-bottom: 1px solid #e2e8f0;
    }}
    .t-row:last-child {{
      border-bottom: none;
      background: #fef3c7;
      font-size: 11px;
      font-weight: 800;
      color: #92400e;
      border-top: 2px solid #b45309;
    }}

    .conditions {{
      background: #f1f5f9;
      border-radius: 6px;
      padding: 10px 14px;
      font-size: 8px;
      color: #334155;
      line-height: 1.4;
    }}
    .cond-title {{ font-weight: 800; text-transform: uppercase; color: #0f172a; margin-bottom: 4px; }}
    .cond-list {{ margin: 0; padding-left: 14px; }}
    .cond-list li {{ margin-bottom: 2px; }}

    footer {{
      margin-top: 14px;
      padding-top: 8px;
      border-top: 1px solid #cbd5e1;
      display: flex;
      justify-content: space-between;
      color: #64748b;
      font-size: 7.5px;
    }}
  </style>
</head>
<body>
  <div class="sheet">
    <header>
      <div class="brand">
        <div>
          <div class="brand-title">DIXIS RECURSOS Y SOLUCIONES S.L.</div>
          <div class="brand-sub">HAM ESTRUCTURAS METÁLICAS MENORCA • CALDERERÍA INDUSTRIAL Y CERRAJERÍA</div>
        </div>
      </div>
      <div class="header-doc">
        <div class="doc-num">PRESUPUESTO P-2026-0050</div>
        <div class="doc-date">Fecha: 02/11/2026 • Validez: 30 días</div>
      </div>
    </header>

    <div class="grid-2">
      <div class="card">
        <div class="card-title">Datos del Cliente</div>
        <div class="card-line"><span class="card-label">Empresa / Razón:</span><span class="card-val">Nautic KIM</span></div>
        <div class="card-line"><span class="card-label">Persona de Contacto:</span><span class="card-val">Mariano</span></div>
        <div class="card-line"><span class="card-label">Teléfono:</span><span class="card-val">675 573 682</span></div>
        <div class="card-line"><span class="card-label">Email:</span><span class="card-val">mfa@nautickim.com</span></div>
        <div class="card-line"><span class="card-label">Ubicación Obra:</span><span class="card-val">Polígono Industrial de Alaior, Menorca</span></div>
      </div>
      <div class="card">
        <div class="card-title">Especificaciones Principales del Proyecto</div>
        <div class="card-line"><span class="card-label">Tipología:</span><span class="card-val">Marquesina rectangular 100% atornillable</span></div>
        <div class="card-line"><span class="card-label">Dimensiones en Planta:</span><span class="card-val">16,00 m largo x 8,00 m ancho libre</span></div>
        <div class="card-line"><span class="card-label">Altura Libre al Alero:</span><span class="card-val">8,00 m (Cumbrera a 8,60 m)</span></div>
        <div class="card-line"><span class="card-label">Superficie Techada:</span><span class="card-val">150,30 m² (faldón con aleros)</span></div>
        <div class="card-line"><span class="card-label">Cubierta y Acabado:</span><span class="card-val">Sándwich PUR 30 mm / Pintura Epoxi+2C poliuretano</span></div>
      </div>
    </div>

    <div class="highlight-banner">
      <div class="hb-item"><div class="hb-val">6.471 Kg</div><div class="hb-lbl">Acero Estructural S275JR</div></div>
      <div class="hb-item"><div class="hb-val">43,05 Kg/m²</div><div class="hb-lbl">Ratio Estructural CTE</div></div>
      <div class="hb-item"><div class="hb-val">150,30 m²</div><div class="hb-lbl">Panel PUR 30 mm</div></div>
      <div class="hb-item"><div class="hb-val">100% Mecano</div><div class="hb-lbl">Estructura Atornillada</div></div>
      <div class="hb-item"><div class="hb-val">C3 / C4 Marino</div><div class="hb-lbl">Protección Anticorrosión HAM</div></div>
    </div>

    <table>
      <thead>
        <tr>
          <th class="c" style="width: 32px;">Nº</th>
          <th>Concepto y Descripción de la Partida</th>
          <th class="c" style="width: 35px;">Ud</th>
          <th class="r" style="width: 48px;">Cant.</th>
          <th class="r" style="width: 65px;">Precio (€)</th>
          <th class="r" style="width: 75px;">Importe (€)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="c"><b>01</b></td>
          <td>
            <b>CÁLCULO ESTRUCTURAL, INGENIERÍA Y PLANOS DE TALLER</b>
            <div class="desc-text">Cálculo estructural según CTE DB-SE-AE (viento Zona C en Alaior) y DB-SE-A. Modelado BIM 3D, planos de taller, despiece analítico y replanteo de anclajes.</div>
          </td>
          <td class="c">PA</td>
          <td class="r">1,00</td>
          <td class="r">980,00 €</td>
          <td class="r"><b>980,00 €</b></td>
        </tr>
        <tr>
          <td class="c"><b>02</b></td>
          <td>
            <b>FABRICACIÓN EN TALLER DE ESTRUCTURA METÁLICA ATORNILLABLE (6.471 KG ACERO S275JR)</b>
            <div class="desc-text">Fabricación integral de estructura tipo mecano (16x8x8 m). 10 pilares tubo 180x180x6 mm con placas base 350x350x20 mm y rigidizadores; 5 dinteles IPE 240; 10 jabalcones a 45° tubo 100x100x4 mm; vigas de coronación 120x120x5 mm; 8 líneas correas 100x50x3 mm; cruces de San Andrés Ø20 mm con tensores M20 8.8; tornillería de alta resistencia M16/M20 cincada.</div>
          </td>
          <td class="c">Kg</td>
          <td class="r">6.471,00</td>
          <td class="r">2,85 €</td>
          <td class="r"><b>18.442,35 €</b></td>
        </tr>
        <tr>
          <td class="c"><b>03</b></td>
          <td>
            <b>TRATAMIENTO ANTICORROSIVO E IMPRIMACIÓN + PINTURA POLIURETANO 2C (SISTEMA HAM EXTERIOR)</b>
            <div class="desc-text">Limpieza mecánica y desengrasado Sa 2.5 / St 3. Aplicación de imprimación epoxídica bicomponente anticorrosiva (60-80 µm) y esmalte de acabado poliuretano alifático 2C para exteriores (50-60 µm) resistente a UV y salinidad. NUNCA secado al horno conforme al estándar HAM Menorca. Color RAL a elegir.</div>
          </td>
          <td class="c">m²</td>
          <td class="r">385,00</td>
          <td class="r">10,50 €</td>
          <td class="r"><b>4.042,50 €</b></td>
        </tr>
        <tr>
          <td class="c"><b>04</b></td>
          <td>
            <b>SUMINISTRO Y MONTAJE DE CUBIERTA EN PANEL SÁNDWICH PUR 30 MM Y REMATERÍA</b>
            <div class="desc-text">Suministro e instalación sobre correas de 150,30 m² de panel sándwich de cubierta de 30 mm de espesor (PUR 40 kg/m³, chapa grecada exterior 0,5 mm prelacada e interior 0,4 mm blanco pirineo). Fijaciones bimetálicas autotaladrantes con arandelas de estanqueidad de EPDM. Remate troquelado de cumbrera y testeros laterales plegados.</div>
          </td>
          <td class="c">m²</td>
          <td class="r">150,30</td>
          <td class="r">48,00 €</td>
          <td class="r"><b>7.214,40 €</b></td>
        </tr>
        <tr>
          <td class="c"><b>05</b></td>
          <td>
            <b>RECOGIDA DE PLUVIALES (CANALÓN GALVANIZADO PRELACADO Y BAJANTES)</b>
            <div class="desc-text">Canalón perimetral de chapa galvanizada prelacada desarrollo 400 mm fijado con ganchos reforzados en alero (16,70 ml), y 2 bajantes pluviales circulares hasta pie de pilar (16,00 ml totales) con codos y abrazaderas.</div>
          </td>
          <td class="c">ml</td>
          <td class="r">16,70</td>
          <td class="r">65,00 €</td>
          <td class="r"><b>1.085,50 €</b></td>
        </tr>
        <tr>
          <td class="c"><b>06</b></td>
          <td>
            <b>TRANSPORTE, MEDIOS AUXILIARES DE ELEVACIÓN Y ANCLAJES ESTRUCTURALES</b>
            <div class="desc-text">Transporte ida de camión tráiler con material despiezado a parcela de Alaior. Camión grúa para descarga y elevación de pilares y pórticos a 8 m. Plataforma elevadora móvil (PEMP) articulada diésel de 12 m. 40 anclajes químicos Hilti HIT-HY con varillas roscadas M20 calidad 8.8 cincadas.</div>
          </td>
          <td class="c">PA</td>
          <td class="r">1,00</td>
          <td class="r">5.250,00 €</td>
          <td class="r"><b>5.250,00 €</b></td>
        </tr>
        <tr>
          <td class="c"><b>07</b></td>
          <td>
            <b>MONTAJE INTEGRAL MECANO EN OBRA Y AJUSTES DINAMOMÉTRICOS</b>
            <div class="desc-text">Mano de obra cualificada de cuadrilla de montadores oficiales en obra. Ensamblado atornillado mecano de la estructura completa a 8 m de altura, aplomado, nivelación, apriete controlado con llave dinamométrica según norma, retocado de pintura en cabezas de tornillos y verificación final de seguridad.</div>
          </td>
          <td class="c">PA</td>
          <td class="r">1,00</td>
          <td class="r">4.180,00 €</td>
          <td class="r"><b>4.180,00 €</b></td>
        </tr>
      </tbody>
    </table>

    <div class="totals-area">
      <div class="totals-box">
        <div class="t-row"><span>SUBTOTAL NETO:</span><span>41.194,75 €</span></div>
        <div class="t-row"><span>I.V.A. (21%):</span><span>8.650,90 €</span></div>
        <div class="t-row"><span>TOTAL PRESUPUESTO:</span><span>49.845,65 €</span></div>
      </div>
    </div>

    <div class="conditions">
      <div class="cond-title">Condiciones de Contratación y Ejecución:</div>
      <ul class="cond-list">
        <li><b>Forma de pago:</b> 40% a la confirmación del pedido y acopio de acero/panel; 30% a la finalización de fabricación en taller previo a carga; 30% a la finalización del montaje y recepción.</li>
        <li><b>Plazo de ejecución:</b> 3 a 4 semanas para fabricación y pintura en taller tras aprobación de planos; 6 a 8 días laborables para montaje in situ en Alaior.</li>
        <li><b>Exclusiones:</b> Obra civil de solera o zapatas de cimentación (se presupuesta anclaje sobre hormigón existente según especificación técnica), acometidas eléctricas e iluminación, tasas o licencias municipales de obras.</li>
        <li><b>Garantía:</b> 10 años en estabilidad estructural según LOE y 3 años en estanqueidad de cubierta y fijaciones.</li>
      </ul>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • CIF: B57825432 • Circunval·lació 11, Sant Lluís (Menorca) • Tel: 669 769 541</div>
      <div>Página 1 de 1 • Oferta P-2026-0050</div>
    </footer>
  </div>
</body>
</html>"""
    
    html_path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Cliente generado en: {html_path}")
    return html_path

def create_html_technical():
    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>P-2026-0050 Presupuesto Técnico Interno: Marquesina Atornillable 16x8x8m Alaior</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 10mm 12mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #f8fafc;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 8.5px;
      line-height: 1.4;
    }}
    .sheet {{
      width: 210mm;
      margin: 0 auto;
      background: #ffffff;
      padding: 10mm 12mm;
      page-break-after: always;
    }}
    .sheet:last-child {{ page-break-after: auto; }}
    
    header {{
      background: #1e293b;
      color: #fff;
      padding: 12px 16px;
      border-radius: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 3px solid #b45309;
      margin-bottom: 10px;
    }}
    .header-title {{ font-size: 13px; font-weight: 800; color: #fff; text-transform: uppercase; }}
    .header-sub {{ font-size: 8px; color: #94a3b8; }}
    .header-tag {{ background: #b45309; color: #fff; font-size: 8px; font-weight: 700; padding: 4px 8px; border-radius: 4px; }}
    
    h2 {{
      font-size: 10px;
      font-weight: 800;
      color: #0f172a;
      text-transform: uppercase;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 3px;
      margin: 8px 0 6px 0;
    }}
    
    .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 10px; }}
    .box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px 8px; }}
    .box-title {{ font-size: 8px; font-weight: 700; color: #b45309; text-transform: uppercase; margin-bottom: 4px; }}
    .box-val {{ font-size: 11px; font-weight: 800; color: #0f172a; }}
    .box-sub {{ font-size: 7.5px; color: #64748b; }}

    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
    th {{
      background: #0f172a;
      color: #ffffff;
      font-weight: 700;
      font-size: 7.8px;
      text-transform: uppercase;
      padding: 5px 6px;
      text-align: left;
      border: 1px solid #0f172a;
    }}
    th.r, td.r {{ text-align: right; }}
    th.c, td.c {{ text-align: center; }}
    td {{
      padding: 4.5px 6px;
      border: 1px solid #e2e8f0;
      font-size: 8px;
      vertical-align: middle;
    }}
    tr:nth-child(even) td {{ background: #f8fafc; }}

    .badge {{
      display: inline-block;
      padding: 2px 5px;
      border-radius: 3px;
      font-size: 7px;
      font-weight: 700;
      background: #e2e8f0;
      color: #334155;
    }}
    .badge-ok {{ background: #dcfce7; color: #166534; }}
    .badge-alert {{ background: #fef3c7; color: #92400e; }}

    .escandallo-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 8px;
    }}
    
    footer {{
      margin-top: 8px;
      padding-top: 6px;
      border-top: 1px solid #cbd5e1;
      display: flex;
      justify-content: space-between;
      color: #64748b;
      font-size: 7px;
    }}
  </style>
</head>
<body>
  <!-- PÁGINA 1: CÁLCULO ESTRUCTURAL Y DESGLOSE DE ACERO -->
  <div class="sheet">
    <header>
      <div>
        <div class="header-title">PRESUPUESTO TÉCNICO INTERNO • P-2026-0050</div>
        <div class="header-sub">Proyecto: Marquesina Industrial Atornillable 16x8x8 m • Nautic KIM (Alaior)</div>
      </div>
      <div class="header-tag">DOCUMENTO DE USO TÉCNICO INTERNO</div>
    </header>

    <div class="grid-3">
      <div class="box">
        <div class="box-title">Cálculo Estructural (CTE)</div>
        <div class="box-val">6.471 Kg de Acero</div>
        <div class="box-sub">43,05 kg/m² • Acero S275JR en perfiles tubulares e IPE</div>
      </div>
      <div class="box">
        <div class="box-title">Esfuerzo Crítico</div>
        <div class="box-val">Viento Zona C (Alaior)</div>
        <div class="box-sub">qp=1,00 kN/m² • Pandeo pilar 8m controlado con jabalcones</div>
      </div>
      <div class="box">
        <div class="box-title">Mano de Obra Estimada</div>
        <div class="box-val">386 Horas Totales</div>
        <div class="box-sub">24h Técnica + 140h Taller + 222h Montaje a 8m</div>
      </div>
    </div>

    <h2>1. Desglose Analítico de Acero Estructural S275JR (Hierro)</h2>
    <table>
      <thead>
        <tr>
          <th>Elemento</th>
          <th>Perfil Estructural</th>
          <th class="c">Uds</th>
          <th class="r">Long. (m)</th>
          <th class="r">Total (m)</th>
          <th class="r">Kg/ml</th>
          <th class="r">Peso (kg)</th>
          <th>Criterio Técnico / Comprobación</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>Pilares Pórticos</b></td>
          <td>Tubo estructural 180x180x6 mm</td>
          <td class="c">10</td>
          <td class="r">8,00</td>
          <td class="r">80,00</td>
          <td class="r">31,70</td>
          <td class="r"><b>2.536,00</b></td>
          <td><span class="badge badge-ok">CUMPLE</span> Pandeo H=8m (λ=90, χ=0,55, Nb,Rd=581 kN)</td>
        </tr>
        <tr>
          <td><b>Dinteles de Pórtico</b></td>
          <td>Viga laminada IPE 240</td>
          <td class="c">5</td>
          <td class="r">8,00</td>
          <td class="r">40,00</td>
          <td class="r">30,70</td>
          <td class="r"><b>1.228,00</b></td>
          <td><span class="badge badge-ok">CUMPLE</span> Luz ef. 6,00 m, f=11,2 mm < L/400 (20 mm)</td>
        </tr>
        <tr>
          <td><b>Jabalcones Nudos (45°)</b></td>
          <td>Tubo estructural 100x100x4 mm</td>
          <td class="c">10</td>
          <td class="r">1,40</td>
          <td class="r">14,00</td>
          <td class="r">11,70</td>
          <td class="r"><b>163,80</b></td>
          <td>Triangulación rígida pilar-dintel; reduce flexión un 55%</td>
        </tr>
        <tr>
          <td><b>Vigas Atado Coronación</b></td>
          <td>Tubo estructural 120x120x5 mm</td>
          <td class="c">2</td>
          <td class="r">16,00</td>
          <td class="r">32,00</td>
          <td class="r">17,50</td>
          <td class="r"><b>560,00</b></td>
          <td>Atado en cabeza; soporte canalón y empuje longitudinal</td>
        </tr>
        <tr>
          <td><b>Correas de Cubierta</b></td>
          <td>Tubo rectangular 100x50x3 mm</td>
          <td class="c">8</td>
          <td class="r">16,70</td>
          <td class="r">133,60</td>
          <td class="r">6,62</td>
          <td class="r"><b>884,43</b></td>
          <td>Separación 1,25 m, soporte de panel sándwich PUR 30 mm</td>
        </tr>
        <tr>
          <td><b>Cruces San Andrés Laterales</b></td>
          <td>Redondo Ø20 mm + tensores M20</td>
          <td class="c">8</td>
          <td class="r">9,00</td>
          <td class="r">72,00</td>
          <td class="r">2,47</td>
          <td class="r"><b>177,84</b></td>
          <td>2 vanos extremos en lateral izquierdo y derecho (H=8 m)</td>
        </tr>
        <tr>
          <td><b>Cruces San Andrés Cubierta</b></td>
          <td>Redondo Ø20 mm + tensores M20</td>
          <td class="c">4</td>
          <td class="r">9,00</td>
          <td class="r">36,00</td>
          <td class="r">2,47</td>
          <td class="r"><b>88,92</b></td>
          <td>Viga paraviento en faldón (2 vanos arriostrados)</td>
        </tr>
        <tr>
          <td><b>Placas Base Cimentación</b></td>
          <td>Chapa S275JR e=20 mm (350x350)</td>
          <td class="c">10</td>
          <td class="r">-</td>
          <td class="r">-</td>
          <td class="r">19,23</td>
          <td class="r"><b>192,30</b></td>
          <td>4 taladros Ø26 para anclaje químico estructural M20</td>
        </tr>
        <tr>
          <td><b>Cartelas y Rigidizadores</b></td>
          <td>Chapas e=10 y e=15 mm</td>
          <td class="c">Global</td>
          <td class="r">-</td>
          <td class="r">-</td>
          <td class="r">-</td>
          <td class="r"><b>410,00</b></td>
          <td>Rigidizadores base, placas testa unión pilar-dintel y casquillos</td>
        </tr>
        <tr>
          <td><b>Tornillería Estructural Cincada</b></td>
          <td>Pernos M16 y M20 Calidad 8.8</td>
          <td class="c">Global</td>
          <td class="r">-</td>
          <td class="r">-</td>
          <td class="r">-</td>
          <td class="r"><b>110,00</b></td>
          <td>Uniones resistentes atornilladas pretensadas con tuerca doble</td>
        </tr>
        <tr style="background: #fef3c7; font-weight: 800;">
          <td colspan="6"><b>TOTAL ACERO ESTRUCTURAL S275JR CALCULADO (Kg)</b></td>
          <td class="r" style="color: #92400e; font-size: 9.5px;"><b>6.471,00 kg</b></td>
          <td><b>Ratio: 43,05 kg / m² cubierta</b></td>
        </tr>
      </tbody>
    </table>

    <h2>2. Especificación Estricta de Pintura y Acabado HAM</h2>
    <div class="box" style="margin-bottom: 8px;">
      <div class="box-title">SISTEMA ANTICORROSIVO HAM EXTERIOR (C3/C4) — REGLA ESTRICTA: NUNCA AL HORNO</div>
      <div style="font-size: 7.8px; line-height: 1.4; color: #334155;">
        1. <b>Preparación Superficial:</b> Desengrasado previo, eliminación de cascarilla de laminación y limpieza mecánica abrasiva Sa 2.5 / St 3 según ISO 8501-1.<br>
        2. <b>Imprimación Epoxídica:</b> Aplicación a pistola airless de imprimación anticorrosiva epoxi de 2 componentes con pigmentos inhibidores (espesor seco 60-80 µm).<br>
        3. <b>Pintura de Acabado:</b> Esmalte de acabado mediante poliuretano alifático bicomponente 2C especial exteriores, alta retención de brillo y resistencia a radiación UV y atmósfera marina de Menorca (espesor seco 50-60 µm). Secado al aire en cabina de aplicación.<br>
        4. <b>Repaso de Obra:</b> Sellado y repaso in situ de cabezas de tornillos y roscas cincadas con imprimación y esmalte de retoque.
      </div>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • HAM Menorca • P-2026-0050</div>
      <div>Página 1 de 2 • Desglose Estructural</div>
    </footer>
  </div>

  <!-- PÁGINA 2: HORAS DE MANO DE OBRA, TAREAS Y ESCANDALLO DE COSTES -->
  <div class="sheet">
    <header>
      <div>
        <div class="header-title">PRESUPUESTO TÉCNICO INTERNO • P-2026-0050 (CONTINUACIÓN)</div>
        <div class="header-sub">Desglose Operativo de Mano de Obra, Medios Auxiliares y Escandallo de Costes</div>
      </div>
      <div class="header-tag">DOCUMENTO DE USO TÉCNICO INTERNO</div>
    </header>

    <h2>3. Desglose de Tareas y Horas de Personal (386 Horas Totales)</h2>
    <table>
      <thead>
        <tr>
          <th>Tarea Operativa</th>
          <th>Descripción y Medios Asignados</th>
          <th class="c">Categoría</th>
          <th class="r">Horas</th>
          <th class="r">Coste H (€)</th>
          <th class="r">Coste Subtotal</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>1. Oficina Técnica</b></td>
          <td>Modelado 3D BIM, cálculo estructural CTE, planos de taller y despiece analítico</td>
          <td class="c">Ingeniero</td>
          <td class="r">24 h</td>
          <td class="r">26,00 €</td>
          <td class="r">624,00 €</td>
        </tr>
        <tr>
          <td><b>2. Corte y Biselado Taller</b></td>
          <td>Corte con sierra de cinta de pilares tubo 180, dinteles IPE 240, correas y rigidizadores</td>
          <td class="c">Oficial 1ª</td>
          <td class="r">28 h</td>
          <td class="r">26,00 €</td>
          <td class="r">728,00 €</td>
        </tr>
        <tr>
          <td><b>3. Mecanizado y Taladros</b></td>
          <td>Taladro coordinado con plantilla de placas base e=20 mm y placas frontales mecano</td>
          <td class="c">Oficial 1ª</td>
          <td class="r">36 h</td>
          <td class="r">26,00 €</td>
          <td class="r">936,00 €</td>
        </tr>
        <tr>
          <td><b>4. Armado y Soldadura Taller</b></td>
          <td>Soldeo MAG de placas base a tubos 180, rigidizadores, casquillos de correas y pre-ensamble</td>
          <td class="c">Oficial Soldador</td>
          <td class="r">44 h</td>
          <td class="r">26,00 €</td>
          <td class="r">1.144,00 €</td>
        </tr>
        <tr>
          <td><b>5. Tratamiento y Pintura Taller</b></td>
          <td>Limpieza mecánica Sa 2.5, imprimación epoxi 2C y esmalte poliuretano alifático 2C</td>
          <td class="c">Pintor Especialista</td>
          <td class="r">32 h</td>
          <td class="r">26,00 €</td>
          <td class="r">832,00 €</td>
        </tr>
        <tr>
          <td><b>6. Replanteo y Anclajes Químicos</b></td>
          <td>Replanteo ejes, taladro de 40 perforaciones Ø24 e inyección química Hilti HIT-HY M20</td>
          <td class="c">Cuadrilla Obra</td>
          <td class="r">12 h</td>
          <td class="r">28,00 €</td>
          <td class="r">336,00 €</td>
        </tr>
        <tr>
          <td><b>7. Izado Pórticos a 8 m con Grúa</b></td>
          <td>Elevación de 10 pilares de 8 m y 5 dinteles IPE 240, nivelación, aplomado y apriete base</td>
          <td class="c">3 Montadores</td>
          <td class="r">72 h</td>
          <td class="r">28,00 €</td>
          <td class="r">2.016,00 €</td>
        </tr>
        <tr>
          <td><b>8. Montaje Correas y Atado (H=8 m)</b></td>
          <td>Instalación de vigas atado tubo 120, 8 correas tubo 100x50 y arriostramientos con PEMP</td>
          <td class="c">3 Montadores</td>
          <td class="r">60 h</td>
          <td class="r">28,00 €</td>
          <td class="r">1.680,00 €</td>
        </tr>
        <tr>
          <td><b>9. Montaje Panel Sándwich 30 mm</b></td>
          <td>Izado y fijación de 150,3 m² de panel PUR 30 mm con tornillos EPDM, remates cumbrera y testeros</td>
          <td class="c">3 Montadores</td>
          <td class="r">54 h</td>
          <td class="r">28,00 €</td>
          <td class="r">1.512,00 €</td>
        </tr>
        <tr>
          <td><b>10. Pluviales y Canalón</b></td>
          <td>Montaje de 16,7 ml de canalón prelacado 400 mm y 2 bajantes pluviales hasta suelo</td>
          <td class="c">2 Montadores</td>
          <td class="r">14 h</td>
          <td class="r">28,00 €</td>
          <td class="r">392,00 €</td>
        </tr>
        <tr>
          <td><b>11. Control Calidad y Repasos</b></td>
          <td>Comprobación dinamométrica pernos 8.8, repaso de pintura poliuretano cabezas y remates</td>
          <td class="c">Jefe Montaje</td>
          <td class="r">10 h</td>
          <td class="r">28,00 €</td>
          <td class="r">280,00 €</td>
        </tr>
        <tr style="background: #f1f5f9; font-weight: 800;">
          <td colspan="3"><b>TOTAL MANO DE OBRA (164 h Taller/Técnica + 222 h Montaje)</b></td>
          <td class="r"><b>386 h</b></td>
          <td class="r">-</td>
          <td class="r" style="color: #0f172a;"><b>10.480,00 €</b></td>
        </tr>
      </tbody>
    </table>

    <div class="escandallo-grid">
      <div>
        <h2>4. Elementos Auxiliares y Maquinaria Especial</h2>
        <table>
          <thead>
            <tr><th>Medio Auxiliar</th><th class="c">Uds</th><th class="r">Tarifa</th><th class="r">Coste</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Camión Grúa Pluma</b> (Izado pilares 8 m y pórticos)</td>
              <td class="c">16 h</td>
              <td class="r">100,00 €/h</td>
              <td class="r">1.600,00 €</td>
            </tr>
            <tr>
              <td><b>Plataforma Elevadora PEMP 12 m</b> (Tijera/Brazo diésel)</td>
              <td class="c">1 sem</td>
              <td class="r">1.150,00 €</td>
              <td class="r">1.150,00 €</td>
            </tr>
            <tr>
              <td><b>Transporte Despiezado</b> (1 viaje camión tráiler taller-Alaior)</td>
              <td class="c">1 viaje</td>
              <td class="r">280,00 €</td>
              <td class="r">280,00 €</td>
            </tr>
            <tr>
              <td><b>Líneas de vida provisionales y EPIs altura</b></td>
              <td class="c">Lote</td>
              <td class="r">280,00 €</td>
              <td class="r">280,00 €</td>
            </tr>
            <tr style="font-weight: 700; background: #f8fafc;">
              <td colspan="3"><b>SUBTOTAL MEDIOS Y TRANSPORTE</b></td>
              <td class="r"><b>3.310,00 €</b></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div>
        <h2>5. Resumen de Escandallo y Margen Económico</h2>
        <table>
          <thead>
            <tr><th>Concepto Económico</th><th class="r">Importe (€)</th><th class="r">% s/ Venta</th></tr>
          </thead>
          <tbody>
            <tr><td>Coste Acero S275JR (6.471 kg)</td><td class="r">11.647,80 €</td><td class="r">28,3%</td></tr>
            <tr><td>Coste Panel Sándwich PUR 30 mm y Remates</td><td class="r">4.208,40 €</td><td class="r">10,2%</td></tr>
            <tr><td>Coste Pintura Epoxi + Poliuretano 2C HAM</td><td class="r">1.450,00 €</td><td class="r">3,5%</td></tr>
            <tr><td>Coste Tornillería 8.8 y Anclajes Hilti M20</td><td class="r">820,00 €</td><td class="r">2,0%</td></tr>
            <tr><td>Coste Mano de Obra Taller e Ingeniería (164 h)</td><td class="r">4.264,00 €</td><td class="r">10,4%</td></tr>
            <tr><td>Coste Mano de Obra Montaje Alaior (222 h)</td><td class="r">6.216,00 €</td><td class="r">15,1%</td></tr>
            <tr><td>Coste Medios Auxiliares y Transporte</td><td class="r">3.310,00 €</td><td class="r">8,0%</td></tr>
            <tr style="background: #e2e8f0; font-weight: 800;">
              <td><b>COSTE DIRECTO TOTAL (CD)</b></td>
              <td class="r"><b>31.916,20 €</b></td>
              <td class="r"><b>77,5%</b></td>
            </tr>
            <tr><td>Gastos Generales (GG 10,0%)</td><td class="r">3.191,62 €</td><td class="r">7,7%</td></tr>
            <tr><td>Beneficio Industrial (BI 14,8%)</td><td class="r">6.086,93 €</td><td class="r">14,8%</td></tr>
            <tr style="background: #fef3c7; font-weight: 800; color: #92400e;">
              <td><b>PRECIO DE VENTA NETO (B.I.)</b></td>
              <td class="r"><b>41.194,75 €</b></td>
              <td class="r"><b>100,0%</b></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <footer>
      <div>DIXIS RECURSOS Y SOLUCIONES S.L. • HAM Menorca • P-2026-0050</div>
      <div>Página 2 de 2 • Desglose Técnico y Económico</div>
    </footer>
  </div>
</body>
</html>"""
    
    html_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML Técnico generado en: {html_path}")
    return html_path

def convert_to_pdf(html_file, pdf_file):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{html_file.replace(os.sep, '/')}")
        page.pdf(
            path=pdf_file,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        browser.close()
    print(f"PDF generado con éxito en: {pdf_file}")

if __name__ == "__main__":
    excel_path = create_excel()
    client_html = create_html_client()
    client_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    convert_to_pdf(client_html, client_pdf)
    
    tech_html = create_html_technical()
    tech_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")
    convert_to_pdf(tech_html, tech_pdf)
    
    print("\nTodos los documentos han sido creados correctamente.")
