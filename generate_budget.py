import subprocess
import sys

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
ws.title = "Pressupost S Enclusa"

# Headers
headers = ["Categoria", "Concepte", "Import (€)"]
ws.append(headers)
for col_num, value in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_num)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    cell.alignment = Alignment(horizontal="center")

# Data
data = [
    ["GENERAL", "Seguretat i salut", 2000.00],
    ["GENERAL", "Gestió de residus", 2000.00],
    ["ANTENES", "Preparació superfícies a restaurar", 3500.00],
    ["ANTENES", "Reparacions (soldadures, empernats i altres reparacions menors)", 2500.00],
    ["ANTENES", "Sistema anticorrosiu i pintura exterior", 5000.00],
    ["DIPÒSIT", "Inspecció estructural (soldadures, empernats i altres patologies)", 3000.00],
    ["DIPÒSIT", "Reparacions (soldadures, empernats i altres reparacions estructurals)", 5000.00],
    ["DIPÒSIT", "Sistema anticorrosiu i pintura exterior", 4500.00],
    ["DIPÒSIT", "Tractament interior de conservació (cuba)", 500.00],
    ["DIPÒSIT", "Reposició d’escala d’accés en altura i passarel·la exterior circumdant", 4203.00],
    ["", "", ""],
    ["", "Costos directes", 32203.00],
    ["", "Costos indirectes", 7406.69],
    ["", "Despeses generals (17%)", 5474.51],
    ["", "Benefici industrial (6%)", 1932.18],
    ["", "", ""],
    ["", "TOTAL EXECUCIÓ MATERIAL DELS TREBALLS (PEM)", 39609.69],
    ["", "IVA (21%)", 8318.04],
    ["", "TOTAL EXECUCIÓ DEL CONTRACTE", 47927.73]
]

for row in data:
    ws.append(row)

# Styling
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):
    for cell in row:
        if isinstance(cell.value, (int, float)):
            cell.number_format = '#,##0.00 €'

for col in ws.columns:
    max_length = 0
    column = col[0].column_letter # Get the column name
    for cell in col:
        try: # Necessary to avoid error on empty cells
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column].width = adjusted_width

# Totals styling
for row_num in range(13, 20):
    ws.cell(row=row_num, column=2).font = Font(bold=True)
    if isinstance(ws.cell(row=row_num, column=3).value, (int, float)):
        ws.cell(row=row_num, column=3).font = Font(bold=True)

wb.save(r"C:\Users\pablo\Documents\Presupuestador\Pressupost_Enclusa.xlsx")
print("Archivo Excel creado exitosamente.")
