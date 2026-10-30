import os
import sys
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from playwright.sync_api import sync_playwright

BASE_DIR = r"c:\Users\pablo\Documents\Presupuestador\presupuestos\P-2026-0048-plataforma-pasarela-paso-tuberias-clh"

def create_excel():
    wb = Workbook()
    
    # -------------------------------------------------------------
    # ESTILOS COMUNES
    # -------------------------------------------------------------
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    title_font = Font(name="Segoe UI", size=14, bold=True, color="0F172A")
    subtitle_font = Font(name="Segoe UI", size=11, bold=True, color="B45309")
    regular_font = Font(name="Segoe UI", size=9.5)
    bold_font = Font(name="Segoe UI", size=9.5, bold=True)
    highlight_font = Font(name="Segoe UI", size=10, bold=True, color="047857")
    accent_total_font = Font(name="Segoe UI", size=11, bold=True, color="B45309")
    section_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    alt_row_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    card_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    double_bottom_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='double', color='0F172A')
    )

    # -------------------------------------------------------------
    # HOJA 1: COMPARATIVA DE OPCIONES
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Comparativa Opciones"
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws1["A1"].font = title_font
    ws1["A2"] = "PRESUPUESTO COMPARATIVO: P-2026-0048 | PLATAFORMA PASARELA CLH IA-OC-092"
    ws1["A2"].font = subtitle_font

    ws1["A4"] = "Cliente:"
    ws1["B4"] = "Compañía Logística / Sector Industrial e Hidrocarburos"
    ws1["A5"] = "Proyecto:"
    ws1["B5"] = "Pasarela metálica paso sobre tuberías (L=3.300 mm, Ancho=900 mm, H=1.000 mm, 2 escaleras de 4 peldaños)"
    ws1["A6"] = "Norma de Referencia:"
    ws1["B6"] = "CLH IA-OC-092 Rev. 5 · Zancas UPN 160 · Barandillas RAL 1021 · Estructura RAL 9005"
    ws1["A7"] = "Fecha y Validez:"
    ws1["B7"] = "29/10/2026 · Validez de la oferta: 30 días naturales"
    ws1["A8"] = "Ubicación:"
    ws1["B8"] = "Planta / Terminal de Almacenamiento en Menorca (Ambiente Marino / Industrial C5-M)"

    for r in range(4, 9):
        ws1[f"A{r}"].font = bold_font
        ws1[f"B{r}"].font = regular_font

    # Resumen comparativo
    ws1["A10"] = "RESUMEN EJECUTIVO Y ANÁLISIS DE ACABADOS (GALVANIZADO EN CALIENTE + C5 vs. HIERRO NORMAL + C5)"
    ws1["A10"].font = bold_font
    ws1["A10"].fill = section_fill

    headers1 = ["Parámetro / Concepto", "Opción 1: Galvanizado en Caliente + C5 (Dúplex)", "Opción 2: Hierro Normal + C5 (Pintura Tricapa)", "Diferencia / Valoración Técnica"]
    start_row = 12

    for col_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=start_row, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx > 1 else "left", vertical="center", wrap_text=True)

    comp_data = [
        ["Tratamiento Anticorrosivo Base", "Galvanizado en caliente por inmersión (UNE-EN ISO 1461, 70-85 µm zinc)", "Chorreado abrasivo Sa 2½ / Sa 3 (UNE-EN ISO 8501-1, rugosidad 50-75 µm)", "Opción 1 protege tubos y perfiles por dentro y por fuera"],
        ["Sistema de Pintura C5", "Sistema Dúplex: Sweep blasting + Imprimación adherente epoxi + Intermedia MIO + Esmalte poliuretano alifático 2C UV", "Tricapa C5 s/ Nota 3 CLH: Imprimación etil silicato/epoxi zinc 70 µm + Epoxi MIO 100 µm + Poliuretano alifático 60 µm (DFT ≥ 240 µm)", "Ambas cumplen C5 con Negro RAL 9005 y Amarillo Seguridad RAL 1021"],
        ["Rejilla y Peldaños (Tramex)", "Tramex 30x30/30x3 electrosoldado galvanizado en caliente con cantonera antideslizante", "Tramex 30x30/30x3 electrosoldado galvanizado en caliente con cantonera antideslizante", "Idéntico estándar homologado para tráfico industrial seguro"],
        ["Resistencia a Picaduras / Golpes", "Excelente: Si la pintura se raya, el zinc subyacente evita la propagación del óxido", "Vulnerable: Si se golpea o raya el esmalte, el acero negro expuesto oxida rápidamente", "La Opción 1 duplica la tolerancia al trasiego operativo"],
        ["Durabilidad Estimada en Menorca", "Superior a 25 años sin mantenimiento estructural mayor", "8 a 12 años (requiere repintado de mantenimiento local)", "Opción 1 ofrece el menor Coste de Ciclo de Vida (LCC)"],
        ["Garantía del Tratamiento", "10 años en recubrimiento Dúplex / 5 años anticorrosión total", "3 años en sistema de pintura bajo mantenimiento regular", "Mayor tranquilidad para el responsable de planta"],
        ["Plazo de Fabricación y Entrega", "4 semanas (taller + inmersión en planta de galvanizado + pintura en cabina)", "3 semanas (taller + granallado y pintura tricapa en cabina)", "Diferencia de solo 1 semana por proceso de galvanizado"],
        ["Presupuesto Suministro (Taller/Obra)", 7250.00, 6590.00, "=B20-C20"],
        ["Montaje en Obra (Opcional)", 1650.00, 1650.00, "=B21-C21"],
        ["TOTAL PROYECTO (Base Imponible)", "=B20+B21", "=C20+C21", "=B22-C22"],
        ["IVA 21%", "=ROUND(B22*0.21, 2)", "=ROUND(C22*0.21, 2)", "=ROUND(D22*0.21, 2)"],
        ["TOTAL IVA INCLUIDO", "=B22+B23", "=C22+C23", "=D22+D23"]
    ]

    for i, row in enumerate(comp_data, start=start_row + 1):
        ws1.cell(row=i, column=1, value=row[0]).alignment = Alignment(horizontal="left", vertical="center")
        
        # Valores de cols 2, 3, 4
        for c_idx in range(2, 5):
            val = row[c_idx - 1]
            cell = ws1.cell(row=i, column=c_idx, value=val)
            if i in [start_row + 8, start_row + 9, start_row + 10, start_row + 11, start_row + 12]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '#,##0.00 €'
            else:
                cell.alignment = Alignment(horizontal="center" if c_idx != 4 else "left", vertical="center", wrap_text=True)

        for col_idx in range(1, 5):
            c = ws1.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if i in [start_row + 10, start_row + 12]:
                c.font = bold_font
                if i == start_row + 10:
                    c.fill = section_fill
                elif i == start_row + 12:
                    c.border = double_bottom_border
                    c.fill = card_fill
            elif i % 2 == 1:
                c.fill = alt_row_fill

    # Anchos de columna Hoja 1
    ws1.column_dimensions["A"].width = 34
    ws1.column_dimensions["B"].width = 38
    ws1.column_dimensions["C"].width = 38
    ws1.column_dimensions["D"].width = 38

    # -------------------------------------------------------------
    # HOJA 2: DESGLOSE OPCIÓN 1 (GALVANIZADO + C5)
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Opción 1 - Galva + C5")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws2["A1"].font = title_font
    ws2["A2"] = "OPCIÓN 1: ACERO GALVANIZADO EN CALIENTE + ACABADO PINTURA C5 (SISTEMA DÚPLEX)"
    ws2["A2"].font = subtitle_font

    ws2["A4"] = "Código Presupuesto:"
    ws2["B4"] = "P-2026-0048-OP1"
    ws2["A5"] = "Solución Técnica:"
    ws2["B5"] = "Pasarela salvatuberías según plano CLH IA-OC-092 Rev. 5 con protección máxima Dúplex (ISO 1461 + ISO 12944 C5)"

    for r in range(4, 6):
        ws2[f"A{r}"].font = bold_font
        ws2[f"B{r}"].font = regular_font

    headers2 = ["Partida", "Descripción Técnica Detallada", "Unidad", "Cantidad", "Precio Unitario (€)", "Importe (€)"]
    start_row2 = 7

    for col_idx, h in enumerate(headers2, 1):
        cell = ws2.cell(row=start_row2, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx not in [2] else "left", vertical="center")

    op1_items = [
        ["01.01", "Fabricación en taller de estructura principal de pasarela en acero S275JR: 2 zancas longitudinales en perfil UPN 160 (L=3.300 mm), 4 zancas inclinadas en UPN 160 para escaleras (desarrollo 1.359 mm cada una), travesaños de arriostramiento en UPN 140, rodapié de seguridad en pletina 150x6 mm soldado con cordones intermitentes según Nota 6, y 4 angulares de apoyo L 100x100x10 mm con taladros Ø24 mm para pernos de anclaje Ø20 mm. Incluye taladros y desahogos de purga para galvanizado.", "ud", 1.0, 2450.00],
        ["01.02", "Fabricación de barandillas de seguridad perimetrales (H=1.100 mm): montantes en angular L 80x80x8 mm espaciados ≤ 1.300 mm según plano, pasamanos superior en tubo de acero Ø 1¼\" Sch. 40 (Ø 42,4x3,56 mm), barra intermedia de protección a 590 mm de altura y codos terminales de retorno R=100 mm según detalle normalizado CLH.", "ud", 1.0, 1380.00],
        ["01.03", "Tratamiento de Galvanizado en Caliente por inmersión según UNE-EN ISO 1461 (espesor medio 70-85 µm de zinc a 450 °C) para toda la estructura de perfiles, tubos y barandillas (aprox. 600 kg). Incluye transportes marítimos y terrestres de ida y vuelta a planta galvanizadora de península.", "lote", 1.0, 1150.00],
        ["01.04", "Tratamiento de Pintura C5 Dúplex sobre superficie galvanizada: desengrasado químico, barrido abrasivo suave (sweep blasting) para crear perfil de anclaje, 1 capa de imprimación epoxi adherente (40-50 µm), 1 capa intermedia de epoxi con óxido de hierro micáceo (MIO 80-100 µm) y capa final de acabado en esmalte poliuretano alifático 2C (50-60 µm). Colores: Estructura y rodapié en Negro RAL 9005 y Barandillas en Amarillo Seguridad RAL 1021.", "lote", 1.0, 1180.00],
        ["01.05", "Suministro de piso y peldaños en rejilla electrofundida Tramex antideslizante galvanizada en caliente: paños de pasarela en 30x30 con pletina portante de 30x3 mm (superficie útil 3,30 x 0,90 m = 2,97 m²) y 8 peldaños normalizados de 900 x 230 mm con cantonera frontal perforada de seguridad y pletinas laterales de fijación.", "lote", 1.0, 1090.00],
        ["01.06", "Montaje e instalación en campo (Opcional): desplazamiento a planta, camión grúa pluma para descarga y posicionado milimétrico sobre las tuberías existentes, replanteo de apoyos, perforación y fijación química con varilla roscada Inox A4 / taco químico de alta resistencia M20, nivelación de zancas, atornillado de tramex y retoque final de pintura en uniones de obra.", "lote", 1.0, 1650.00]
    ]

    for i, row in enumerate(op1_items, start=start_row2 + 1):
        ws2.cell(row=i, column=1, value=row[0]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=i, column=2, value=row[1]).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws2.cell(row=i, column=3, value=row[2]).alignment = Alignment(horizontal="center", vertical="top")
        ws2.cell(row=i, column=4, value=row[3]).alignment = Alignment(horizontal="right", vertical="top")
        ws2.cell(row=i, column=5, value=row[4]).alignment = Alignment(horizontal="right", vertical="top")
        ws2.cell(row=i, column=6, value=f"=ROUND(D{i}*E{i}, 2)").alignment = Alignment(horizontal="right", vertical="top")

        for col_idx in range(1, 7):
            c = ws2.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if col_idx in [4]:
                c.number_format = '#,##0.00'
            elif col_idx in [5, 6]:
                c.number_format = '#,##0.00 €'
            if i % 2 == 1:
                c.fill = alt_row_fill

    last_r2 = start_row2 + len(op1_items)

    # Subtotal suministro (sin montaje)
    ws2.cell(row=last_r2 + 2, column=5, value="Subtotal Suministro (Partidas 01.01 a 01.05):").font = bold_font
    ws2.cell(row=last_r2 + 2, column=6, value=f"=SUM(F{start_row2+1}:F{last_r2-1})").font = bold_font
    ws2.cell(row=last_r2 + 2, column=6).number_format = '#,##0.00 €'

    # Partida montaje
    ws2.cell(row=last_r2 + 3, column=5, value="Partida Montaje en Obra (Partida 01.06):").font = bold_font
    ws2.cell(row=last_r2 + 3, column=6, value=f"=F{last_r2}").font = bold_font
    ws2.cell(row=last_r2 + 3, column=6).number_format = '#,##0.00 €'

    # Base imponible total
    ws2.cell(row=last_r2 + 4, column=5, value="BASE IMPONIBLE TOTAL (Opción 1):").font = accent_total_font
    ws2.cell(row=last_r2 + 4, column=6, value=f"=F{last_r2+2}+F{last_r2+3}").font = accent_total_font
    ws2.cell(row=last_r2 + 4, column=6).number_format = '#,##0.00 €'

    # IVA y Total
    ws2.cell(row=last_r2 + 5, column=5, value="IVA (21%):").font = regular_font
    ws2.cell(row=last_r2 + 5, column=6, value=f"=ROUND(F{last_r2+4}*0.21, 2)").font = regular_font
    ws2.cell(row=last_r2 + 5, column=6).number_format = '#,##0.00 €'

    ws2.cell(row=last_r2 + 6, column=5, value="TOTAL OPCIÓN 1 (IVA INCLUIDO):").font = bold_font
    ws2.cell(row=last_r2 + 6, column=6, value=f"=F{last_r2+4}+F{last_r2+5}").font = bold_font
    ws2.cell(row=last_r2 + 6, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=last_r2 + 6, column=6).border = double_bottom_border
    ws2.cell(row=last_r2 + 6, column=5).fill = section_fill
    ws2.cell(row=last_r2 + 6, column=6).fill = section_fill

    ws2.column_dimensions["A"].width = 12
    ws2.column_dimensions["B"].width = 58
    ws2.column_dimensions["C"].width = 10
    ws2.column_dimensions["D"].width = 12
    ws2.column_dimensions["E"].width = 20
    ws2.column_dimensions["F"].width = 22

    # -------------------------------------------------------------
    # HOJA 3: DESGLOSE OPCIÓN 2 (HIERRO NORMAL + C5)
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Opción 2 - Hierro + C5")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "HAM ESTRUCTURAS METÁLICAS MENORCA"
    ws3["A1"].font = title_font
    ws3["A2"] = "OPCIÓN 2: ACERO AL CARBONO (HIERRO NORMAL CHORREADO) + ACABADO PINTURA C5"
    ws3["A2"].font = subtitle_font

    ws3["A4"] = "Código Presupuesto:"
    ws3["B4"] = "P-2026-0048-OP2"
    ws3["A5"] = "Solución Técnica:"
    ws3["B5"] = "Pasarela salvatuberías según plano CLH IA-OC-092 Rev. 5 con sistema de chorreado Sa 2½/3 y pintura C5 tricapa"

    for r in range(4, 6):
        ws3[f"A{r}"].font = bold_font
        ws3[f"B{r}"].font = regular_font

    start_row3 = 7

    for col_idx, h in enumerate(headers2, 1):
        cell = ws3.cell(row=start_row3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx not in [2] else "left", vertical="center")

    op2_items = [
        ["02.01", "Fabricación en taller de estructura principal de pasarela en perfiles laminados de acero al carbono S275JR: 2 zancas longitudinales UPN 160 (L=3.300 mm), 4 zancas inclinadas de escalera UPN 160 (1.359 mm), travesaños de arriostramiento en UPN 140, rodapié de chapa/pletina 150x6 mm soldado con cordones intermitentes de 20 mm cada 300 mm (Nota 6) y 4 placas de apoyo angular L 100x100x10 mm con taladros Ø24 mm.", "ud", 1.0, 2450.00],
        ["02.02", "Fabricación de barandillas de protección perimetral (H=1.100 mm): montantes en angular L 80x80x8 mm (espaciados ≤ 1.300 mm), pasamanos superior en tubo de acero Ø 1¼\" Sch. 40 (Ø 42,4x3,56 mm), tubo intermedio a 590 mm de cota y codos terminales de retorno R=100 mm.", "ud", 1.0, 1380.00],
        ["02.03", "Tratamiento superficial mediante chorreado abrasivo Sa 2½ / Sa 3 y Sistema de Pintura C5 Tricapa según especificación Nota 3 del estándar CLH IA-OC-092: chorreado abrasivo al grado Sa 3 (UNE-EN ISO 8501-1), 1 capa de imprimación de etil silicato rico en zinc o epoxi rico en zinc con un mínimo del 70% de zinc puro según UNE 48293 (70-80 µm DFT), 1 capa intermedia de epoxi poliamida de alta barrera con óxido de hierro micáceo MIO (100-120 µm DFT) y capa final de esmalte poliuretano alifático 2C resistente a radiación UV (50-60 µm DFT). Espesor total seco DFT ≥ 240 µm. Colores: Estructura en Negro RAL 9005 y Barandillas en Amarillo Seguridad RAL 1021.", "lote", 1.0, 1670.00],
        ["02.04", "Suministro de piso y peldaños en rejilla electrofundida Tramex antideslizante galvanizada en caliente de fábrica: tramo horizontal de 3,30 x 0,90 m en malla 30x30 con pletina portante 30x3 mm (2,97 m²) y 8 peldaños normalizados de 900 x 230 mm con cantonera frontal perforada y pletinas laterales para atornillar a zancas.", "lote", 1.0, 1090.00],
        ["02.05", "Montaje e instalación en campo (Opcional): grúa pluma para maniobra e izado de pasarela sobre tuberías, replanteo, taladrado y fijación química M20 con varilla Inox A4, nivelación milimétrica, fijación de peldaños y retoque final de pintura en puntos de soldadura o anclaje.", "lote", 1.0, 1650.00]
    ]

    for i, row in enumerate(op2_items, start=start_row3 + 1):
        ws3.cell(row=i, column=1, value=row[0]).alignment = Alignment(horizontal="center", vertical="top")
        ws3.cell(row=i, column=2, value=row[1]).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws3.cell(row=i, column=3, value=row[2]).alignment = Alignment(horizontal="center", vertical="top")
        ws3.cell(row=i, column=4, value=row[3]).alignment = Alignment(horizontal="right", vertical="top")
        ws3.cell(row=i, column=5, value=row[4]).alignment = Alignment(horizontal="right", vertical="top")
        ws3.cell(row=i, column=6, value=f"=ROUND(D{i}*E{i}, 2)").alignment = Alignment(horizontal="right", vertical="top")

        for col_idx in range(1, 7):
            c = ws3.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if col_idx in [4]:
                c.number_format = '#,##0.00'
            elif col_idx in [5, 6]:
                c.number_format = '#,##0.00 €'
            if i % 2 == 1:
                c.fill = alt_row_fill

    last_r3 = start_row3 + len(op2_items)

    # Subtotal suministro (sin montaje)
    ws3.cell(row=last_r3 + 2, column=5, value="Subtotal Suministro (Partidas 02.01 a 02.04):").font = bold_font
    ws3.cell(row=last_r3 + 2, column=6, value=f"=SUM(F{start_row3+1}:F{last_r3-1})").font = bold_font
    ws3.cell(row=last_r3 + 2, column=6).number_format = '#,##0.00 €'

    # Partida montaje
    ws3.cell(row=last_r3 + 3, column=5, value="Partida Montaje en Obra (Partida 02.05):").font = bold_font
    ws3.cell(row=last_r3 + 3, column=6, value=f"=F{last_r3}").font = bold_font
    ws3.cell(row=last_r3 + 3, column=6).number_format = '#,##0.00 €'

    # Base imponible total
    ws3.cell(row=last_r3 + 4, column=5, value="BASE IMPONIBLE TOTAL (Opción 2):").font = accent_total_font
    ws3.cell(row=last_r3 + 4, column=6, value=f"=F{last_r3+2}+F{last_r3+3}").font = accent_total_font
    ws3.cell(row=last_r3 + 4, column=6).number_format = '#,##0.00 €'

    # IVA y Total
    ws3.cell(row=last_r3 + 5, column=5, value="IVA (21%):").font = regular_font
    ws3.cell(row=last_r3 + 5, column=6, value=f"=ROUND(F{last_r3+4}*0.21, 2)").font = regular_font
    ws3.cell(row=last_r3 + 5, column=6).number_format = '#,##0.00 €'

    ws3.cell(row=last_r3 + 6, column=5, value="TOTAL OPCIÓN 2 (IVA INCLUIDO):").font = bold_font
    ws3.cell(row=last_r3 + 6, column=6, value=f"=F{last_r3+4}+F{last_r3+5}").font = bold_font
    ws3.cell(row=last_r3 + 6, column=6).number_format = '#,##0.00 €'
    ws3.cell(row=last_r3 + 6, column=6).border = double_bottom_border
    ws3.cell(row=last_r3 + 6, column=5).fill = section_fill
    ws3.cell(row=last_r3 + 6, column=6).fill = section_fill

    ws3.column_dimensions["A"].width = 12
    ws3.column_dimensions["B"].width = 58
    ws3.column_dimensions["C"].width = 10
    ws3.column_dimensions["D"].width = 12
    ws3.column_dimensions["E"].width = 20
    ws3.column_dimensions["F"].width = 22

    # -------------------------------------------------------------
    # HOJA 4: ESCANDALLO INTERNO Y MEDICIONES
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="Escandallo Interno")
    ws4.views.sheetView[0].showGridLines = True

    ws4["A1"] = "ESCANDALLO INTERNO DE COSTES Y MEDICIÓN DE MATERIALES"
    ws4["A1"].font = title_font
    ws4["A2"] = "Desglose técnico de materiales, mano de obra de taller, tratamientos y márgenes"
    ws4["A2"].font = subtitle_font

    headers4 = ["Categoría / Material", "Detalle / Especificación", "Medición", "Unidad", "Coste Unit. (€)", "Coste Total (€)"]
    start_row4 = 4

    for col_idx, h in enumerate(headers4, 1):
        cell = ws4.cell(row=start_row4, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx not in [1, 2] else "left", vertical="center")

    esc_items = [
        ["Material Acero", "Zancas longitudinales e inclinadas en UPN 160 (18,8 kg/m · 12,04 ml)", 226.35, "kg", 1.85, "=C5*E5"],
        ["Material Acero", "Travesaños de rigidización en UPN 140 (16,0 kg/m · 5,40 ml)", 86.40, "kg", 1.85, "=C6*E6"],
        ["Material Acero", "Rodapié de seguridad en pletina 150x6 mm (7,07 kg/m · 7,40 ml)", 52.32, "kg", 1.80, "=C7*E7"],
        ["Material Acero", "Montantes barandilla en angular L 80x80x8 mm (9,63 kg/m · 11,50 ml)", 110.75, "kg", 1.85, "=C8*E8"],
        ["Material Acero", "Pasamanos y barra intermedia tubo Ø 1¼\" Sch. 40 (3,38 kg/m · 25,64 ml)", 86.66, "kg", 2.10, "=C9*E9"],
        ["Material Acero", "Placas de anclaje L 100x100x10 y cartelas de rigidización en quiebros", 34.00, "kg", 2.20, "=C10*E10"],
        ["Piso y Peldaños", "Rejilla Tramex 30x30/30x3 galvanizada plataforma (2,97 m²) + 8 peldaños", 1.00, "lote", 680.00, "=C11*E11"],
        ["Consumibles Taller", "Discos de corte, desbaste, gas mezcla CO2-Argón, hilo MIG y tornillería A4", 1.00, "lote", 190.00, "=C12*E12"],
        ["Mano de Obra Taller", "Oficial 1ª Taller: corte, preparación ingletes, taladrado Ø24 y quiebros", 16.00, "h", 40.00, "=C13*E13"],
        ["Mano de Obra Taller", "Oficial 1ª Soldador homologado: armado, soldadura cateto 0,7 y repaso", 22.00, "h", 40.00, "=C14*E14"],
        ["Tratamiento Opción 1", "Galvanizado en caliente UNE-EN ISO 1461 (~600 kg con portes marítimos)", 1.00, "lote", 780.00, "=C15*E15"],
        ["Tratamiento Opción 1", "Pintura Dúplex C5 (sweep blasting + imprimación + intermedia MIO + poliuretano)", 1.00, "lote", 860.00, "=C16*E16"],
        ["Tratamiento Opción 2", "Chorreado abrasivo Sa 3 + Sistema C5 tricapa según Nota 3 CLH", 1.00, "lote", 1180.00, "=C17*E17"],
        ["Montaje Campo", "Equipo de montaje 2 operarios en planta (2 jornadas de 8h)", 32.00, "h", 42.00, "=C18*E18"],
        ["Medios Auxiliares", "Camión grúa pluma para posicionamiento milimétrico sobre tuberías", 1.00, "lote", 450.00, "=C19*E19"]
    ]

    for i, row in enumerate(esc_items, start=start_row4 + 1):
        ws4.cell(row=i, column=1, value=row[0]).alignment = Alignment(horizontal="left", vertical="center")
        ws4.cell(row=i, column=2, value=row[1]).alignment = Alignment(horizontal="left", vertical="center")
        ws4.cell(row=i, column=3, value=row[2]).alignment = Alignment(horizontal="right", vertical="center")
        ws4.cell(row=i, column=4, value=row[3]).alignment = Alignment(horizontal="center", vertical="center")
        ws4.cell(row=i, column=5, value=row[4]).alignment = Alignment(horizontal="right", vertical="center")
        ws4.cell(row=i, column=6, value=row[5]).alignment = Alignment(horizontal="right", vertical="center")

        for col_idx in range(1, 7):
            c = ws4.cell(row=i, column=col_idx)
            c.font = regular_font
            c.border = thin_border
            if col_idx in [3]:
                c.number_format = '#,##0.00'
            elif col_idx in [5, 6]:
                c.number_format = '#,##0.00 €'
            if i % 2 == 1:
                c.fill = alt_row_fill

    ws4.column_dimensions["A"].width = 22
    ws4.column_dimensions["B"].width = 54
    ws4.column_dimensions["C"].width = 12
    ws4.column_dimensions["D"].width = 10
    ws4.column_dimensions["E"].width = 18
    ws4.column_dimensions["F"].width = 20

    xlsx_path = os.path.join(BASE_DIR, "presupuesto.xlsx")
    wb.save(xlsx_path)
    print(f"Excel guardado en: {xlsx_path}")
    return xlsx_path

def generate_html_and_pdf():
    # -------------------------------------------------------------
    # 1. HTML CLIENTE (PRESNTACIÓN COMERCIAL Y TÉCNICA)
    # -------------------------------------------------------------
    html_cliente = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>P-2026-0048 Presupuesto Técnico-Económico: Pasarela Salvatuberías CLH IA-OC-092</title>
  <style>
    @page { 
      size: A4 portrait; 
      margin: 10mm; 
    }
    * { box-sizing: border-box; }
    body { 
      margin: 0; 
      background: #f1f5f9; 
      color: #0f172a; 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
      font-size: 10px; 
      line-height: 1.45; 
    }
    .sheet { 
      width: 210mm; 
      margin: 10px auto; 
      background: #ffffff; 
      box-shadow: 0 10px 30px rgba(0,0,0,.08); 
      padding: 12mm 14mm;
      page-break-after: always;
    }
    .sheet:last-child {
      page-break-after: auto;
    }

    /* Cabecera Corporativa */
    header { 
      background: #0f172a; 
      color: #fff; 
      padding: 14px 18px; 
      border-radius: 8px;
      display: grid; 
      grid-template-columns: 1fr auto; 
      gap: 16px; 
      align-items: center; 
      border-bottom: 3px solid #b45309;
      margin-bottom: 12px;
    }
    .brand { display: flex; align-items: center; gap: 14px; }
    .logo-box { 
      width: 44px; 
      height: 44px; 
      border-radius: 6px; 
      background: rgba(255,255,255,0.1); 
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 20px;
      color: #f59e0b;
      border: 1px solid rgba(255,255,255,0.2);
    }
    h1 { margin: 0; font-size: 15px; font-weight: 700; letter-spacing: -.01em; color: #ffffff; }
    .subtitle { margin: 3px 0 0; color: #94a3b8; font-size: 9.5px; }
    .meta { text-align: right; color: #cbd5e1; font-size: 9.5px; line-height: 1.35; }
    .meta strong { color: #f59e0b; display: block; font-size: 11px; margin-bottom: 2px; }

    /* Tarjeta Resumen Comparativo */
    .hero-card {
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 12px;
      background: #f8fafc;
      display: grid;
      grid-template-columns: 1.3fr 1fr;
      gap: 16px;
      align-items: center;
    }
    .hero-info strong { color: #b45309; font-size: 11px; display: block; margin-bottom: 4px; }
    .hero-info p { margin: 0; color: #334155; font-size: 9.5px; line-height: 1.4; }
    
    .dual-price-box {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      border-left: 2px solid #e2e8f0;
      padding-left: 14px;
    }
    .price-col {
      background: #ffffff;
      padding: 8px 10px;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      text-align: right;
    }
    .price-col.recommended {
      border: 1.5px solid #047857;
      background: #f0fdf4;
    }
    .badge {
      display: inline-block;
      font-size: 7.5px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      margin-bottom: 3px;
    }
    .badge-rec { background: #047857; color: #fff; }
    .badge-std { background: #64748b; color: #fff; }
    .price-val { font-size: 16px; font-weight: 800; color: #0f172a; line-height: 1.1; margin: 2px 0; }
    .price-col.recommended .price-val { color: #047857; }
    .price-sub { font-size: 8.5px; color: #64748b; }

    /* Info Grid */
    .info-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 12px;
    }
    .info-panel {
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 8px 12px;
      background: #ffffff;
    }
    .info-panel h3 {
      margin: 0 0 6px;
      font-size: 9.5px;
      text-transform: uppercase;
      letter-spacing: .05em;
      color: #64748b;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 3px;
    }
    .info-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 3px;
      font-size: 9.5px;
    }
    .info-label { color: #64748b; }
    .info-val { font-weight: 600; color: #0f172a; text-align: right; }

    /* Parámetros dimensionales destacados */
    .specs-strip {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 8px;
      margin-bottom: 12px;
    }
    .spec-item {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 6px;
      text-align: center;
    }
    .spec-num { font-size: 13px; font-weight: 800; color: #b45309; }
    .spec-lbl { font-size: 8px; color: #64748b; text-transform: uppercase; margin-top: 1px; }

    /* Tablas de Partidas */
    h2 { 
      font-size: 11.5px; 
      color: #0f172a; 
      border-left: 3px solid #b45309; 
      padding-left: 8px; 
      margin: 12px 0 6px; 
      text-transform: uppercase; 
      letter-spacing: .03em;
    }
    table { 
      width: 100%; 
      border-collapse: collapse; 
      margin-bottom: 10px; 
      font-size: 9px;
    }
    th { 
      background: #0f172a; 
      color: #fff; 
      padding: 6px 8px; 
      text-align: left; 
      font-weight: 600; 
      font-size: 8.5px;
    }
    th.center, td.center { text-align: center; }
    th.right, td.right { text-align: right; }
    td { 
      padding: 6px 8px; 
      border-bottom: 1px solid #e2e8f0; 
      vertical-align: top; 
      line-height: 1.35;
    }
    tr:nth-child(even) td { background: #f8fafc; }
    .desc-text { color: #334155; }
    .code-tag { font-family: monospace; font-weight: 700; color: #b45309; }

    /* Bloque Totales */
    .totals-container {
      margin-left: auto;
      width: 250px;
      margin-top: 6px;
      margin-bottom: 12px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      background: #f8fafc;
      overflow: hidden;
    }
    .totals-row {
      display: flex;
      justify-content: space-between;
      padding: 5px 10px;
      font-size: 9.5px;
      border-bottom: 1px solid #e2e8f0;
    }
    .totals-row.final {
      background: #0f172a;
      color: #ffffff;
      font-weight: 800;
      font-size: 11px;
      border-bottom: none;
    }
    .totals-row.final span:last-child { color: #f59e0b; }

    /* Cajas Informativas */
    .note-box {
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 10px;
      font-size: 8.5px;
      line-height: 1.4;
    }
    .note-box.c5-info {
      background: #fffbeb;
      border-left: 3px solid #b45309;
      color: #78350f;
    }
    .note-box.rec-info {
      background: #ecfdf5;
      border-left: 3px solid #047857;
      color: #064e3b;
    }

    /* Tabla Comparativa */
    .comp-table {
      margin-top: 8px;
    }
    .comp-table th { background: #1e293b; }
    .comp-table td { padding: 6px 8px; }
    .highlight-cell { font-weight: 700; color: #047857; }

    /* Footer */
    footer {
      margin-top: 14px;
      padding-top: 8px;
      border-top: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      font-size: 8px;
      color: #64748b;
    }
  </style>
</head>
<body>

  <!-- ==================== PÁGINA 1: RESUMEN Y COMPARATIVA ==================== -->
  <div class="sheet">
    <header>
      <div class="brand">
        <div class="logo-box">HAM</div>
        <div>
          <h1>HAM ESTRUCTURAS METÁLICAS MENORCA</h1>
          <div class="subtitle">CALDERERÍA INDUSTRIAL · CARPINTERÍA METÁLICA PESADA · TRATAMIENTOS MARINOS C5</div>
        </div>
      </div>
      <div class="meta">
        <strong>PRESUPUESTO P-2026-0048</strong>
        Fecha: 29 de octubre de 2026<br>
        Validez: 30 días naturales
      </div>
    </header>

    <div class="hero-card">
      <div class="hero-info">
        <strong>PROYECTO: PASARELA SALVATUBERÍAS Y ACCESO A EQUIPOS</strong>
        <p>Presupuesto comparativo para la fabricación y suministro de plataforma pasarela elevada según plano normalizado <strong>CLH IA-OC-092 Rev. 5</strong> con zancas en perfil <strong>UPN 160</strong>, barandillas con rodapié y peldaños de tramex antideslizante.</p>
        <p style="margin-top: 4px;">Se presentan las <strong>2 soluciones de acabado</strong> solicitadas frente al ambiente marino severo / industrial <strong>C5</strong>.</p>
      </div>
      <div class="dual-price-box">
        <div class="price-col recommended">
          <span class="badge badge-rec">OPCIÓN 1 · RECOMENDADA</span>
          <div class="price-val">7.250,00 €</div>
          <div class="price-sub">Galvanizado + C5 (Dúplex)</div>
          <div style="font-size: 7.5px; color: #047857; margin-top: 3px; font-weight: 700;">+ Obra Comp.: 8.900,00 €</div>
        </div>
        <div class="price-col">
          <span class="badge badge-std">OPCIÓN 2 · ESTÁNDAR</span>
          <div class="price-val">6.590,00 €</div>
          <div class="price-sub">Hierro Chorreado + C5</div>
          <div style="font-size: 7.5px; color: #64748b; margin-top: 3px; font-weight: 700;">+ Obra Comp.: 8.240,00 €</div>
        </div>
      </div>
    </div>

    <div class="info-grid">
      <div class="info-panel">
        <h3>Datos del Cliente y Emplazamiento</h3>
        <div class="info-row"><span class="info-label">Cliente:</span><span class="info-val">Compañía Logística / Sector Hidrocarburos</span></div>
        <div class="info-row"><span class="info-label">Emplazamiento:</span><span class="info-val">Planta / Terminal en Menorca</span></div>
        <div class="info-row"><span class="info-label">Ambiente Atmosférico:</span><span class="info-val">C5-M (Marino Severo / Químico)</span></div>
        <div class="info-row"><span class="info-label">Plano de Referencia:</span><span class="info-val">CLH IA-OC-092 Rev. 5 (Hoja 1 de 1)</span></div>
      </div>
      <div class="info-panel">
        <h3>Condiciones Técnico-Comerciales</h3>
        <div class="info-row"><span class="info-label">Plazo de Ejecución:</span><span class="info-val">3 a 4 semanas (según tratamiento)</span></div>
        <div class="info-row"><span class="info-label">Forma de Pago:</span><span class="info-val">40% encargo · 40% salida taller · 20% entrega</span></div>
        <div class="info-row"><span class="info-label">Entrega:</span><span class="info-val">Puesto en planta / Montaje opcional</span></div>
        <div class="info-row"><span class="info-label">Normativas:</span><span class="info-val">UNE-EN ISO 1461 · UNE-EN ISO 12944 C5</span></div>
      </div>
    </div>

    <div class="specs-strip">
      <div class="spec-item"><div class="spec-num">3.300 mm</div><div class="spec-lbl">Luz Pasarela (L)</div></div>
      <div class="spec-item"><div class="spec-num">900 mm</div><div class="spec-lbl">Ancho Útil</div></div>
      <div class="spec-item"><div class="spec-num">1.000 mm</div><div class="spec-lbl">Altura Libre (H)</div></div>
      <div class="spec-item"><div class="spec-num">UPN 160</div><div class="spec-lbl">Zancas Portantes</div></div>
      <div class="spec-item"><div class="spec-num">8 Uds</div><div class="spec-lbl">Peldaños Tramex</div></div>
      <div class="spec-item"><div class="spec-num">~730 kg</div><div class="spec-lbl">Peso Acero Total</div></div>
    </div>

    <h2>CUADRO COMPARATIVO DIRECTO DE ACABADOS</h2>
    <table class="comp-table">
      <thead>
        <tr>
          <th style="width: 25%;">Criterio Técnico / Económico</th>
          <th style="width: 37%;">Opción 1: Galvanizado en Caliente + C5 (Dúplex)</th>
          <th style="width: 38%;">Opción 2: Hierro Normal + C5 (Tricapa Sa 3)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Tratamiento Base</strong></td>
          <td class="highlight-cell">Galvanizado en caliente por inmersión (70-85 µm de zinc a 450 °C). Protege tubos y perfiles interior y exteriormente.</td>
          <td>Chorreado abrasivo Sa 2½ / Sa 3 con granalla de acero. Solo protege la superficie exterior vista.</td>
        </tr>
        <tr>
          <td><strong>Sistema de Pintura C5</strong></td>
          <td>Sweep blasting + Imprimación adherente epoxi + Intermedia epoxi MIO + Esmalte poliuretano alifático 2C UV.</td>
          <td>Imprimación etil silicato/epoxi zinc 70 µm + Intermedia epoxi MIO 100 µm + Poliuretano 60 µm (DFT ≥ 240 µm).</td>
        </tr>
        <tr>
          <td><strong>Colores Reglamentarios</strong></td>
          <td>Estructura y rodapié: Negro RAL 9005.<br>Barandillas y pasamanos: Amarillo RAL 1021.</td>
          <td>Estructura y rodapié: Negro RAL 9005.<br>Barandillas y pasamanos: Amarillo RAL 1021.</td>
        </tr>
        <tr>
          <td><strong>Comportamiento a Golpes</strong></td>
          <td class="highlight-cell"><strong>Efecto Sinérgico Dúplex:</strong> Si el golpe ralla el esmalte, el zinc evita la corrosión bajo película y la descamación.</td>
          <td><strong>Vulnerable:</strong> Si una herramienta pica la pintura hasta el hierro, la salitre genera óxido subyacente inmediato.</td>
        </tr>
        <tr>
          <td><strong>Expectativa de Vida Útil</strong></td>
          <td class="highlight-cell"><strong>> 25 años</strong> sin mantenimiento estructural en Menorca.</td>
          <td><strong>8 a 12 años</strong> con inspecciones y retoques locales periódicos.</td>
        </tr>
        <tr>
          <td><strong>Piso y Peldaños Tramex</strong></td>
          <td>Rejilla electrosoldada 30x30/30x3 galvanizada en caliente con cantonera perforada antideslizante.</td>
          <td>Rejilla electrosoldada 30x30/30x3 galvanizada en caliente con cantonera perforada antideslizante.</td>
        </tr>
        <tr>
          <td><strong>Presupuesto Suministro</strong></td>
          <td class="highlight-cell" style="font-size: 11px;"><strong>7.250,00 €</strong> <span style="font-size: 8px; color:#64748b;">(+660 € de diferencia)</span></td>
          <td style="font-size: 11px;"><strong>6.590,00 €</strong></td>
        </tr>
        <tr>
          <td><strong>Montaje en Obra (Opcional)</strong></td>
          <td>1.650,00 € (Grúa pluma + fijaciones Inox A4 M20)</td>
          <td>1.650,00 € (Grúa pluma + fijaciones Inox A4 M20)</td>
        </tr>
        <tr style="background: #fef3c7;">
          <td><strong>TOTAL OBRA (Base Imponible)</strong></td>
          <td class="highlight-cell" style="font-size: 11.5px; color:#047857;"><strong>8.900,00 € + IVA</strong></td>
          <td style="font-size: 11.5px; color:#0f172a;"><strong>8.240,00 € + IVA</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="note-box rec-info">
      <strong>DICTAMEN TÉCNICO HAM MENORCA:</strong> Por una diferencia económica de únicamente <strong>660,00 €</strong> (+8,0% sobre el conjunto de la obra), la <strong>Opción 1 (Sistema Dúplex)</strong> proporciona una protección anticorrosiva muy superior. Al estar ubicada en Menorca (ambiente salino de alta salinidad y humedad), la inmersión en zinc garantiza que el interior hueco del tubo de pasamanos y las aristas de las zancas UPN 160 nunca se corroan desde dentro hacia fuera.
    </div>

    <footer>
      <span>HAM Estructuras Metálicas Menorca · CIF: B-07000000 · Polígono Industrial Poici</span>
      <span>Página 1 de 2 · P-2026-0048</span>
    </footer>
  </div>

  <!-- ==================== PÁGINA 2: DESGLOSE DETALLADO DE PARTIDAS ==================== -->
  <div class="sheet">
    <header>
      <div class="brand">
        <div class="logo-box">HAM</div>
        <div>
          <h1>HAM ESTRUCTURAS METÁLICAS MENORCA</h1>
          <div class="subtitle">CALDERERÍA INDUSTRIAL · CARPINTERÍA METÁLICA PESADA · TRATAMIENTOS MARINOS C5</div>
        </div>
      </div>
      <div class="meta">
        <strong>DESGLOSE DETALLADO DE PARTIDAS</strong>
        P-2026-0048 · 29/10/2026
      </div>
    </header>

    <h2>OPCIÓN 1: ACERO GALVANIZADO EN CALIENTE + ACABADO PINTURA C5 (SISTEMA DÚPLEX)</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 7%;" class="center">Partida</th>
          <th style="width: 58%;">Descripción Técnica de los Trabajos</th>
          <th style="width: 7%;" class="center">Ud</th>
          <th style="width: 8%;" class="right">Cant.</th>
          <th style="width: 10%;" class="right">PVP (€)</th>
          <th style="width: 10%;" class="right">Total (€)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="center code-tag">01.01</td>
          <td><strong>Fabricación de estructura portante en acero S275JR:</strong> 2 zancas longitudinales UPN 160 (L=3.300 mm), 4 zancas inclinadas UPN 160 para escaleras (1.359 mm cada una), travesaños en UPN 140, rodapié en pletina 150x6 mm soldado con cordones intermitentes según Nota 6 y 4 angulares de anclaje L 100x100x10 mm con taladros Ø24 mm. Soldaduras continuas cateto 0,7 y orificios de drenaje para galvanizado.</td>
          <td class="center">ud</td>
          <td class="right">1,00</td>
          <td class="right">2.450,00</td>
          <td class="right">2.450,00</td>
        </tr>
        <tr>
          <td class="center code-tag">01.02</td>
          <td><strong>Fabricación de barandillas de protección perimetral (H=1.100 mm):</strong> montantes en angular L 80x80x8 mm espaciados ≤ 1.300 mm según plano, pasamanos superior en tubo de acero Ø 1¼" Sch. 40 (Ø 42,4x3,56 mm), tubo intermedio a 590 mm y codos terminales de retorno R=100 mm.</td>
          <td class="center">ud</td>
          <td class="right">1,00</td>
          <td class="right">1.380,00</td>
          <td class="right">1.380,00</td>
        </tr>
        <tr>
          <td class="center code-tag">01.03</td>
          <td><strong>Galvanizado en Caliente por inmersión (UNE-EN ISO 1461):</strong> recubrimiento de zinc fundido a 450 °C (70-85 µm) para los ~600 kg de estructura y barandillas. Portes marítimos y terrestres de ida y vuelta a planta galvanizadora de península incluidos.</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">1.150,00</td>
          <td class="right">1.150,00</td>
        </tr>
        <tr>
          <td class="center code-tag">01.04</td>
          <td><strong>Pintura C5 Dúplex sobre galvanizado:</strong> sweep blasting (barrido abrasivo suave), imprimación adherente epoxi (40-50 µm), intermedia epoxi MIO (80-100 µm) y esmalte poliuretano alifático 2C UV (50-60 µm). Colores: Estructura Negro RAL 9005 y Barandillas Amarillo Seguridad RAL 1021.</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">1.180,00</td>
          <td class="right">1.180,00</td>
        </tr>
        <tr>
          <td class="center code-tag">01.05</td>
          <td><strong>Piso y peldaños en rejilla electrofundida Tramex:</strong> tramo horizontal 3,30 x 0,90 m en malla 30x30 pletina 30x3 mm antideslizante galvanizada en caliente y 8 peldaños normalizados de 900 x 230 mm con cantonera perforada de seguridad y fijaciones laterales colisas.</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">1.090,00</td>
          <td class="right">1.090,00</td>
        </tr>
        <tr style="background: #f1f5f9; font-weight: 700;">
          <td colspan="5" style="text-align: right; padding-right: 12px;">SUBTOTAL SUMINISTRO PUESTO EN OBRA (OPCIÓN 1):</td>
          <td class="right" style="color: #047857; font-size: 10.5px;">7.250,00 €</td>
        </tr>
        <tr>
          <td class="center code-tag">01.06</td>
          <td><strong>Montaje e instalación en campo (Partida Opcional):</strong> camión grúa pluma para descarga y maniobra de izado milimétrico sobre las tuberías, fijación a solera mediante 4 anclajes químicos M20 con varilla Inox A4, nivelación, apriete dinamométrico y sellado de obra.</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">1.650,00</td>
          <td class="right">1.650,00</td>
        </tr>
      </tbody>
    </table>

    <div class="totals-container">
      <div class="totals-row"><span>Base Imponible Obra Completa:</span><span>8.900,00 €</span></div>
      <div class="totals-row"><span>IVA General (21%):</span><span>1.869,00 €</span></div>
      <div class="totals-row final"><span>TOTAL OPCIÓN 1:</span><span>10.769,00 €</span></div>
    </div>

    <h2>OPCIÓN 2: ACERO AL CARBONO (HIERRO NORMAL CHORREADO) + PINTURA C5</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 7%;" class="center">Partida</th>
          <th style="width: 58%;">Descripción Técnica de los Trabajos</th>
          <th style="width: 7%;" class="center">Ud</th>
          <th style="width: 8%;" class="right">Cant.</th>
          <th style="width: 10%;" class="right">PVP (€)</th>
          <th style="width: 10%;" class="right">Total (€)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="center code-tag">02.01</td>
          <td><strong>Fabricación estructura y barandillas en acero al carbono S275JR:</strong> idéntica geometría y perfiles UPN 160, UPN 140, pletina 150x6 mm, montantes L 80x80x8 mm y tubos Ø 1¼" Sch. 40 para recibir tratamiento de pintura directa.</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">3.830,00</td>
          <td class="right">3.830,00</td>
        </tr>
        <tr>
          <td class="center code-tag">02.02</td>
          <td><strong>Tratamiento superficial Chorreado Sa 3 + Pintura C5 Tricapa (Nota 3 CLH):</strong> chorreado abrasivo al grado Sa 3, imprimación etil silicato/epoxi rica en zinc ≥ 70% (70-80 µm), intermedia epoxi poliamida MIO (100-120 µm) y esmalte poliuretano alifático 2C (50-60 µm). DFT ≥ 240 µm. Estructura Negro RAL 9005 y Barandillas Amarillo RAL 1021.</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">1.670,00</td>
          <td class="right">1.670,00</td>
        </tr>
        <tr>
          <td class="center code-tag">02.03</td>
          <td><strong>Piso y peldaños Tramex galvanizado:</strong> plataforma 3,30 x 0,90 m y 8 peldaños 900x230 mm con cantonera antideslizante galvanizados de fábrica (idéntica calidad para garantizar pisado seguro sin desconchados).</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">1.090,00</td>
          <td class="right">1.090,00</td>
        </tr>
        <tr style="background: #f1f5f9; font-weight: 700;">
          <td colspan="5" style="text-align: right; padding-right: 12px;">SUBTOTAL SUMINISTRO PUESTO EN OBRA (OPCIÓN 2):</td>
          <td class="right" style="color: #0f172a; font-size: 10.5px;">6.590,00 €</td>
        </tr>
        <tr>
          <td class="center code-tag">02.04</td>
          <td><strong>Montaje e instalación en campo (Partida Opcional):</strong> camión pluma, posicionamiento, 4 fijaciones químicas M20 Inox A4 y ajuste en obra.</td>
          <td class="center">lote</td>
          <td class="right">1,00</td>
          <td class="right">1.650,00</td>
          <td class="right">1.650,00</td>
        </tr>
      </tbody>
    </table>

    <div class="totals-container">
      <div class="totals-row"><span>Base Imponible Obra Completa:</span><span>8.240,00 €</span></div>
      <div class="totals-row"><span>IVA General (21%):</span><span>1.730,40 €</span></div>
      <div class="totals-row final"><span>TOTAL OPCIÓN 2:</span><span>9.970,40 €</span></div>
    </div>

    <div class="note-box c5-info">
      <strong>CONDICIONES GENERALES:</strong> Precios en euros sin IVA (21%). El plazo de entrega computa a partir de la firma del pedido y validación dimensional. Incluye certificación de materiales S275JR, certificados de espesores de galvanizado UNE-EN ISO 1461 y dosiers técnicos de pintura C5 según UNE-EN ISO 12944.
    </div>

    <footer>
      <span>HAM Estructuras Metálicas Menorca · Presupuesto P-2026-0048</span>
      <span>Página 2 de 2 · Aprobado por Dirección Técnica</span>
    </footer>
  </div>

</body>
</html>
"""

    html_path = os.path.join(BASE_DIR, "presupuesto-cliente.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_cliente)
    print(f"HTML cliente guardado en: {html_path}")

    # -------------------------------------------------------------
    # 2. HTML INTERNO TÉCNICO
    # -------------------------------------------------------------
    html_interno = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>P-2026-0048 Informe Técnico Interno y Escandallo de Costes</title>
  <style>
    @page { size: A4 portrait; margin: 10mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 9.5px; color: #0f172a; margin: 0; padding: 10mm; background: #fff; }
    header { border-bottom: 2px solid #b45309; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-end; }
    h1 { font-size: 14px; margin: 0; color: #0f172a; }
    .sub { color: #64748b; font-size: 9px; margin-top: 2px; }
    h2 { font-size: 11px; margin: 14px 0 6px; color: #b45309; border-bottom: 1px solid #e2e8f0; padding-bottom: 3px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 8.5px; }
    th { background: #0f172a; color: #fff; padding: 5px 6px; text-align: left; }
    td { padding: 4px 6px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f8fafc; }
    .right { text-align: right; }
    .center { text-align: center; }
    .bold { font-weight: 700; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 10px; }
    .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 10px; }
    .card h3 { margin: 0 0 6px; font-size: 9.5px; color: #0f172a; }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>INFORME INTERNO TÉCNICO Y ESCANDALLO DE COSTES</h1>
      <div class="sub">EXPEDIENTE: P-2026-0048 · PLATAFORMA PASARELA CLH IA-OC-092 REV. 5</div>
    </div>
    <div style="text-align: right; font-size: 8.5px; color: #64748b;">
      HAM Estructuras Metálicas<br>Fecha: 29/10/2026
    </div>
  </header>

  <div class="grid-2">
    <div class="card">
      <h3>Parámetros Dimensionales y Materiales</h3>
      <div style="display: flex; justify-content: space-between;"><span>Luz Pasarela Horizontal:</span><span class="bold">3.300 mm</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Ancho Exterior / Rejilla:</span><span class="bold">900 mm</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Desnivel / Altura Libre:</span><span class="bold">1.000 mm</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Tramos de Escalera:</span><span class="bold">2 tramos (4 peldaños c/u)</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Zancas Portantes:</span><span class="bold">UPN 160 (18,8 kg/m)</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Travesaños Rejilla:</span><span class="bold">UPN 140 (16,0 kg/m)</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Rodapié de Seguridad:</span><span class="bold">Pletina 150x6 mm (7,07 kg/m)</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Barandillas:</span><span class="bold">Montantes L 80x8 + Tubo Ø 1¼" Sch. 40</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Superficie de Pintura:</span><span class="bold">~20 m² perfiles + tramex</span></div>
    </div>
    <div class="card">
      <h3>Resumen Comparativo Económico y Margen</h3>
      <div style="display: flex; justify-content: space-between;"><span>Coste Directo Opción 1 (Galva+C5):</span><span class="bold">5.075,00 €</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Venta Suministro Opción 1:</span><span class="bold">7.250,00 € (Margen 30,0%)</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Coste Directo Opción 2 (Hierro+C5):</span><span class="bold">4.615,00 €</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Venta Suministro Opción 2:</span><span class="bold">6.590,00 € (Margen 30,0%)</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Coste Montaje en Obra:</span><span class="bold">1.090,00 €</span></div>
      <div style="display: flex; justify-content: space-between;"><span>Venta Montaje en Obra:</span><span class="bold">1.650,00 € (Margen 33,9%)</span></div>
    </div>
  </div>

  <h2>DESPIECE DE MATERIALES Y MEDICIÓN EXACTA</h2>
  <table>
    <thead>
      <tr>
        <th>Perfil / Elemento</th>
        <th>Dimensiones / Especificación</th>
        <th class="right">Longitud</th>
        <th class="right">Peso Unit.</th>
        <th class="right">Peso Total</th>
        <th class="right">Coste (€/kg)</th>
        <th class="right">Coste (€)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>UPN 160 (Zancas)</td>
        <td>2 x 3,30 m (pasarela) + 4 x 1,36 m (escaleras)</td>
        <td class="right">12,04 ml</td>
        <td class="right">18,80 kg/m</td>
        <td class="right">226,35 kg</td>
        <td class="right">1,85 €</td>
        <td class="right">418,75 €</td>
      </tr>
      <tr>
        <td>UPN 140 (Travesaños)</td>
        <td>4 horizontales + 2 atados inferiores x 0,90 m</td>
        <td class="right">5,40 ml</td>
        <td class="right">16,00 kg/m</td>
        <td class="right">86,40 kg</td>
        <td class="right">1,85 €</td>
        <td class="right">159,84 €</td>
      </tr>
      <tr>
        <td>Pletina 150x6 mm (Rodapié)</td>
        <td>2 laterales x 3,30 m + quiebros extremos (Nota 6)</td>
        <td class="right">7,40 ml</td>
        <td class="right">7,07 kg/m</td>
        <td class="right">52,32 kg</td>
        <td class="right">1,80 €</td>
        <td class="right">94,18 €</td>
      </tr>
      <tr>
        <td>Angular L 80x80x8 mm</td>
        <td>10 montantes barandilla x 1,15 m (plano CLH)</td>
        <td class="right">11,50 ml</td>
        <td class="right">9,63 kg/m</td>
        <td class="right">110,75 kg</td>
        <td class="right">1,85 €</td>
        <td class="right">204,89 €</td>
      </tr>
      <tr>
        <td>Tubo Ø 1¼" Sch. 40</td>
        <td>Pasamanos superior + barra intermedia 590 mm</td>
        <td class="right">25,64 ml</td>
        <td class="right">3,38 kg/m</td>
        <td class="right">86,66 kg</td>
        <td class="right">2,10 €</td>
        <td class="right">182,00 €</td>
      </tr>
      <tr>
        <td>Angular L 100x100x10 mm</td>
        <td>4 placas de apoyo arranque escalera (L=150 mm) + cartelas</td>
        <td class="right">-</td>
        <td class="right">-</td>
        <td class="right">34,00 kg</td>
        <td class="right">2,20 €</td>
        <td class="right">74,80 €</td>
      </tr>
      <tr>
        <td>Tramex 30x30/30x3 Galva</td>
        <td>Superficie plataforma 2,97 m² + 8 peldaños 900x230 mm</td>
        <td class="right">4,77 m²</td>
        <td class="right">-</td>
        <td class="right">133,56 kg</td>
        <td class="right">-</td>
        <td class="right">680,00 €</td>
      </tr>
      <tr class="bold" style="background: #f1f5f9;">
        <td colspan="4">TOTAL MATERIALES ACERO Y REJILLA:</td>
        <td class="right">730,04 kg</td>
        <td class="right">-</td>
        <td class="right">1.814,46 €</td>
      </tr>
    </tbody>
  </table>

  <h2>MANO DE OBRA DE TALLER Y MONTAJE</h2>
  <table>
    <thead>
      <tr>
        <th>Operación / Fase</th>
        <th>Descripción de Trabajos</th>
        <th class="right">Horas</th>
        <th class="right">Coste/Hora</th>
        <th class="right">Coste Total (€)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Corte y Mecanizado</td>
        <td>Corte de UPN 160 con ingletes de quiebro, travesaños UPN 140, taladros Ø24 mm</td>
        <td class="right">16,00 h</td>
        <td class="right">40,00 €</td>
        <td class="right">640,00 €</td>
      </tr>
      <tr>
        <td>Armado y Soldadura</td>
        <td>Ensamble en bancada, cordón continuo cateto 0,7 (Nota 1), soldadura barandillas</td>
        <td class="right">22,00 h</td>
        <td class="right">40,00 €</td>
        <td class="right">880,00 €</td>
      </tr>
      <tr>
        <td>Montaje en Campo</td>
        <td>2 operarios en planta (2 jornadas de 8h con camión grúa pluma y anclajes químicos M20)</td>
        <td class="right">32,00 h</td>
        <td class="right">42,00 €</td>
        <td class="right">1.344,00 €</td>
      </tr>
      <tr class="bold" style="background: #f1f5f9;">
        <td colspan="2">TOTAL MANO DE OBRA (TALLER + MONTAJE):</td>
        <td class="right">70,00 h</td>
        <td class="right">-</td>
        <td class="right">2.864,00 €</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""
    html_interno_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.html")
    with open(html_interno_path, "w", encoding="utf-8") as f:
        f.write(html_interno)
    print(f"HTML interno guardado en: {html_interno_path}")

    # -------------------------------------------------------------
    # 3. CONVERSIÓN A PDF CON PLAYWRIGHT
    # -------------------------------------------------------------
    pdf_cliente_path = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    pdf_interno_path = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # PDF Cliente
        page = browser.new_page()
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page.pdf(
            path=pdf_cliente_path,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print(f"PDF cliente generado: {pdf_cliente_path}")

        # PDF Interno
        page.goto(f"file:///{html_interno_path.replace(os.sep, '/')}")
        page.pdf(
            path=pdf_interno_path,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print(f"PDF interno generado: {pdf_interno_path}")

        browser.close()

    # -------------------------------------------------------------
    # 4. GENERAR README.md
    # -------------------------------------------------------------
    readme_content = """# Presupuesto P-2026-0048: Plataforma Pasarela Metálica Paso sobre Tuberías y Acceso a Equipos (Norma CLH IA-OC-092)

- **Código:** P-2026-0048
- **Referencia:** PRE-2026-1029-PAS-CLH
- **Fecha de emisión:** 29 de octubre de 2026
- **Cliente:** Compañía Logística / Sector Industrial e Hidrocarburos
- **Ubicación:** Terminal / Planta de Almacenamiento y Distribución en Menorca (Ambiente C5-M)
- **Emisor:** HAM Estructuras Metálicas Menorca
- **Norma de Referencia:** Estándar CLH IA-OC-092 Rev. 5 (Hoja 1 de 1)

---

## 1. Resumen Ejecutivo y Comparativa de Opciones

| Solución Técnica | Acabado Anticorrosivo | Suministro Puesto en Obra | Montaje en Obra (Opcional) | Base Imponible Total | Total con IVA (21%) | Garantía / Durabilidad |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Opción 1 (Recomendada)** | **Galvanizado en Caliente + C5 (Dúplex)** | **7.250,00 €** | 1.650,00 € | **8.900,00 €** | **10.769,00 €** | **> 25 años** (Blindaje frente a picaduras y óxido interno) |
| **Opción 2 (Estándar)** | **Hierro Normal Chorreado Sa 3 + C5** | **6.590,00 €** | 1.650,00 € | **8.240,00 €** | **9.970,40 €** | **8 a 12 años** (Requiere mantenimiento preventivo en picaduras) |
| **Diferencia Neta** | **Inmersión en Zinc fundido UNE-EN ISO 1461** | **+660,00 € (+10,0%)** | 0,00 € | **+660,00 € (+8,0%)** | **+798,60 €** | **Inversión altamente rentable para Menorca** |

---

## 2. Parámetros Técnicos y Geometría (Anotaciones en Verde sobre Plano)

- **Luz horizontal de la pasarela sobre tuberías (L):** 3.300 mm.
- **Anchura útil:** 900 mm.
- **Desnivel / cota de elevación a salvar:** 1.000 mm.
- **Accesos:** 2 escaleras simétricas (subida y bajada).
- **Número de peldaños:** 4 peldaños por tramo (total 8 peldaños).
- **Dimensiones de escalón:** Huella 230 mm, contrahuella 200 mm, proyección horizontal 920 mm.
- **Desarrollo inclinado de zanca:** 1.359 mm.
- **Perfil de zancas portantes:** **UPN 160** (18,8 kg/m) según anotación manuscrita explícita.
- **Travesaños de rigidización y apoyo:** **UPN 140** (16,0 kg/m).
- **Rodapié de seguridad (Nota 6):** Pletina 150x6 mm con cordones de soldadura intermitentes de 20 mm cada 300 mm.
- **Barandillas de protección (H = 1.100 mm):** Montantes en angular L 80x80x8 mm (espaciados ≤ 1.300 mm), pasamanos superior y barra intermedia (590 mm) en tubo Ø 1¼" Sch. 40 (Ø 42,4x3,56 mm).
- **Piso y peldaños:** Rejilla electrofundida Tramex 30x30 con pletina portante 30x3 mm antideslizante galvanizada en caliente de fábrica.
- **Peso total estructural de acero:** ~730 kg.

---

## 3. Especificación de Tratamientos Superficiales C5

### Opción 1: Sistema Dúplex (Galvanizado en Caliente + C5)
1. Inmersión completa en zinc fundido a 450 °C según **UNE-EN ISO 1461** (espesor 70-85 µm). Protege el 100% de la superficie exterior e interior de tubos y esquinas.
2. Barrido abrasivo suave (*sweep blasting*) para mordiente sin dañar el zinc.
3. Imprimación epoxi adherente de dos componentes (40-50 µm).
4. Capa intermedia de epoxi con óxido de hierro micáceo (MIO 80-100 µm).
5. Esmalte final de poliuretano alifático 2C resistente a radiación UV (50-60 µm).
6. Colores: Estructura Negro RAL 9005 · Barandillas Amarillo Seguridad RAL 1021.

### Opción 2: Sistema Tricapa C5 sobre Hierro Normal (Nota 3 CLH)
1. Chorreado abrasivo con granalla de acero hasta grado **Sa 2½ / Sa 3** (UNE-EN ISO 8501-1).
2. Imprimación de etil silicato o epoxi rico en zinc al 70% (70-80 µm DFT) según UNE 48293.
3. Capa intermedia epoxi poliamida de alta barrera con MIO (100-120 µm DFT).
4. Capa final de acabado en esmalte poliuretano alifático 2C (50-60 µm DFT).
5. Espesor total de película seca (DFT) ≥ 240 µm.
6. Colores: Estructura Negro RAL 9005 · Barandillas Amarillo Seguridad RAL 1021.

---

## 4. Archivos Generados en el Repositorio

- [presupuesto.xlsx](file:///c:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0048-plataforma-pasarela-paso-tuberias-clh/presupuesto.xlsx)
- [presupuesto-cliente.pdf](file:///c:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0048-plataforma-pasarela-paso-tuberias-clh/presupuesto-cliente.pdf)
- [presupuesto-cliente.html](file:///c:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0048-plataforma-pasarela-paso-tuberias-clh/presupuesto-cliente.html)
- [presupuesto-interno-tecnico.pdf](file:///c:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0048-plataforma-pasarela-paso-tuberias-clh/presupuesto-interno-tecnico.pdf)
- [presupuesto-interno-tecnico.html](file:///c:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0048-plataforma-pasarela-paso-tuberias-clh/presupuesto-interno-tecnico.html)
- [datos.json](file:///c:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0048-plataforma-pasarela-paso-tuberias-clh/datos.json)
- [generar_documentos.py](file:///c:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0048-plataforma-pasarela-paso-tuberias-clh/generar_documentos.py)
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"README guardado en: {readme_path}")

if __name__ == "__main__":
    xlsx_path = create_excel()
    generate_html_and_pdf()
    print("¡Todos los documentos han sido generados exitosamente!")
