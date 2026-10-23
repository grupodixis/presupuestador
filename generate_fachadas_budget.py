import subprocess
import sys
import os

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import('openpyxl')

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Presupuesto Fachadas"

# Headers
headers = ["Ubicación", "Descripción", "Medidas / Unidades", "Precio Unitario", "Total"]
ws.append(headers)
for col_num, value in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_num)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    cell.alignment = Alignment(horizontal="center")

# Data
data = [
    ["Fachada lateral oeste", "Fabricado y montaje de 4 líneas de tubo 100x50x3 galvanizado base reforzado a fijar en estructura existente, incluye accesorios de montaje.", "41 ML x 4 Uds", "", ""],
    ["Fachada lateral oeste", "Suministro y montaje de sistema thermoclick de paneles celulares de policarbonato entrelazados.", "41 ML x 5 ML (ancho x alto)", "", ""],
    ["Fachada frontal sur", "Fabricado y montaje de 4 líneas de tubo 100x50x3 galvanizado base reforzado a fijar en estructura existente.", "21 ML x 4 Uds", "", ""],
    ["Fachada frontal sur", "Fabricado y montaje de pilar intermedio de tubo 100x100x4.", "1 Ud", "", ""],
    ["Fachada frontal sur", "Suministro y montaje de sistema thermoclick de paneles celulares de policarbonato entrelazados.", "21 ML x 5 ML (ancho x alto)", "", ""],
    ["Mantenimiento general", "Raspado, pasivado, imprimado con rica en zinc y acabado poliuretanico de postes existentes de 150x150 mm.", "9 ML x 12 Uds", "", ""]
]

for row in data:
    ws.append(row)

for col in ws.columns:
    max_length = 0
    column = col[0].column_letter # Get the column name
    for cell in col:
        try: # Necessary to avoid error on empty cells
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = min(max_length + 2, 80) # Max width 80
    ws.column_dimensions[column].width = adjusted_width

# Set text wrap for Descripción
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=2, max_col=2):
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical="center")

# Align everything else vertically
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for cell in row:
        if cell.column != 2:
            cell.alignment = Alignment(vertical="center")

excel_path = r"C:\Users\pablo\Documents\Presupuestador\Presupuesto_Fachadas.xlsx"
wb.save(excel_path)
print(f"Archivo Excel creado exitosamente en {excel_path}")
