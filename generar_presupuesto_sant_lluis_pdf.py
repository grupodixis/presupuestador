import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Presupuesto Carpintería Sant Lluís</title>
    <style>
        @page { margin: 25mm 20mm; }
        body { 
            font-family: 'Cambria', 'Georgia', serif; 
            line-height: 1.6; 
            margin: 0; 
            color: #2b2b2b; 
            font-size: 11pt;
            box-sizing: border-box;
        }
        h1, h2, h3, h4 { font-family: 'Segoe UI', sans-serif; color: #1a365d; page-break-after: avoid; }
        
        .header { border-bottom: 2px solid #1a365d; padding-bottom: 15px; margin-bottom: 40px; display: table; width: 100%; }
        .header-logo { display: table-cell; font-family: 'Segoe UI', sans-serif; font-size: 20pt; font-weight: 700; color: #1a365d; vertical-align: bottom; }
        .header-logo span { color: #d9534f; }
        .header-info { display: table-cell; text-align: right; font-size: 9pt; color: #555; vertical-align: bottom; font-family: 'Segoe UI', sans-serif; line-height: 1.4; }

        .title-block { text-align: center; margin-bottom: 40px; }
        .title-block h1 { font-size: 20pt; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
        .title-block .subtitle { font-size: 13pt; color: #4a5568; font-family: 'Segoe UI', sans-serif; }

        .section { margin-bottom: 25px; }
        .section h2 { font-size: 13pt; border-bottom: 1px solid #cbd5e0; padding-bottom: 5px; margin-top: 25px; }
        p, li { text-align: justify; }

        .client-info { background-color: #f7fafc; padding: 15px; margin-bottom: 20px; border-left: 4px solid #1a365d; font-size: 10pt; font-family: 'Segoe UI', sans-serif; }
        .client-info table { width: 100%; border: none; margin: 0; font-size: 10pt; }
        .client-info td { padding: 3px; border: none; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-family: 'Segoe UI', sans-serif; font-size: 9.5pt; }
        th, td { border: 1px solid #a0aec0; padding: 8px 10px; text-align: left; }
        th { background-color: #edf2f7; color: #1a365d; font-weight: 600; text-transform: uppercase; }
        .total-row { font-weight: bold; background-color: #e2e8f0; font-size: 11pt; }
        .currency { text-align: right; white-space: nowrap; }
        
        .footer { margin-top: 40px; text-align: center; font-size: 8pt; color: #718096; border-top: 1px solid #e2e8f0; padding-top: 15px; font-family: 'Segoe UI', sans-serif; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-logo">DIXIS<span>.</span> INGENIERÍA Y OBRAS</div>
        <div class="header-info">
            <strong>Ref. Doc:</strong> PRE-2026-142<br>
            <strong>Fecha:</strong> 21 de Agosto de 2026<br>
            <strong>Proyecto:</strong> Cambio de Uso (Garaje a Vivienda)
        </div>
    </div>

    <div class="title-block">
        <h1>PRESUPUESTO TÉCNICO</h1>
        <div class="subtitle">CONJUNTO DE CARPINTERÍA (PE2 + PE3 UNIFICADAS)</div>
    </div>
    
    <div class="client-info">
        <table>
            <tr><td width="15%"><strong>Cliente:</strong></td><td>Sonia Arjona</td></tr>
            <tr><td><strong>Ubicación:</strong></td><td>Sant Lluís, Menorca</td></tr>
            <tr><td><strong>Referencia:</strong></td><td>Actuación en fachada principal según memoria técnica del arquitecto</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>1. Descripción de los Trabajos</h2>
        <p>Fabricación, suministro e instalación de conjunto de carpintería de aluminio con Rotura de Puente Térmico (RPT) en color blanco, diseñado para cubrir un hueco de obra de 3,50 metros de ancho por 3,02 metros de alto. La estructura integra un montante vertical central continuo preparado para la fijación de tabiquería seca de separación interna.</p>
        <p>El conjunto cumple estrictamente con los requisitos de transmitancia térmica y ventilación indicados en proyecto para las zonas PE2 y PE3.</p>
    </div>

    <div class="section">
        <h2>2. Valoración Económica</h2>
        <table>
            <thead>
                <tr>
                    <th>Ud.</th>
                    <th>Concepto y Descripción</th>
                    <th class="currency">Precio Unit.</th>
                    <th class="currency">Importe</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td><strong>Estructura Principal (Aluminio RPT Blanco)</strong><br>
                    Perfilería RPT en color blanco. Incluye montante vertical central continuo (suelo a techo) para tabiquería interior. Dimensiones totales: 3,50m x 3,02m.</td>
                    <td class="currency">1.150,00 €</td>
                    <td class="currency">1.150,00 €</td>
                </tr>
                <tr>
                    <td>1</td>
                    <td><strong>Puerta Peatonal (Zona PE3)</strong><br>
                    Hoja batiente de 85x211 cm, panel ciego aluminio RPT blanco. Herrajes de seguridad. Transmitancia U ≤ 3.2 W/m²K.</td>
                    <td class="currency">780,00 €</td>
                    <td class="currency">780,00 €</td>
                </tr>
                <tr>
                    <td>1</td>
                    <td><strong>Puerta Seccional Motorizada (Zona PE2)</strong><br>
                    Medidas 254x211 cm. Paneles color blanco a juego. Incluye motor de techo y 2 mandos. Ventilación integrada mediante lamas troqueladas (≥ 480 cm²). Transmitancia U ≤ 2.2 W/m²K.</td>
                    <td class="currency">1.450,00 €</td>
                    <td class="currency">1.450,00 €</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td><strong>Paños Fijos Superiores Acristalados</strong><br>
                    Altura aprox. 91 cm. Vidrio doble transparente bajo emisivo (Low-E).</td>
                    <td class="currency">245,00 €</td>
                    <td class="currency">490,00 €</td>
                </tr>
                <tr>
                    <td>1</td>
                    <td><strong>Transporte, Instalación y Remates</strong><br>
                    Medición definitiva en obra, desplazamientos en Menorca, mano de obra especialista para montaje y sellados perimetrales.</td>
                    <td class="currency">550,00 €</td>
                    <td class="currency">550,00 €</td>
                </tr>
                <tr class="total-row">
                    <td colspan="3" style="text-align: right; border-right: none;">BASE IMPONIBLE:</td>
                    <td class="currency">4.420,00 €</td>
                </tr>
                <tr class="total-row" style="background-color: #f7fafc;">
                    <td colspan="3" style="text-align: right; border-right: none; font-weight: normal;">IVA (21%):</td>
                    <td class="currency" style="font-weight: normal;">928,20 €</td>
                </tr>
                <tr class="total-row">
                    <td colspan="3" style="text-align: right; border-right: none; font-size: 13pt; color: #1a365d;">TOTAL PRESUPUESTO:</td>
                    <td class="currency" style="font-size: 13pt; color: #1a365d;">5.348,20 €</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="footer">
        Presupuesto válido por 30 días. Las medidas definitivas se tomarán en obra previo inicio de fabricación.<br>
        DIXIS INGENIERÍA Y OBRAS - Departamento de Presupuestos
    </div>
</body>
</html>"""

work_dir = r"C:\Users\pablo\Documents\Presupuestador"
html_path = os.path.join(work_dir, "Presupuesto_Carpinteria_Sant_Lluis.html")
pdf_path = os.path.join(work_dir, "Presupuesto_Carpinteria_Sant_Lluis.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
]

browser_exe = None
for p in edge_paths:
    if os.path.exists(p):
        browser_exe = p
        break

if browser_exe:
    result = subprocess.run([
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"PDF generado correctamente en {pdf_path}")
    else:
        print(f"Error generando PDF: {result.stderr}")
else:
    print("Navegador no encontrado.")
