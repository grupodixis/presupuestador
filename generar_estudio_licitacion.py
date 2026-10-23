import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estudio de Licitación - S'Enclusa</title>
    <style>
        @page { margin: 25mm 20mm; }
        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; margin: 0; color: #333; font-size: 11pt; }
        h1, h2, h3 { color: #0056b3; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
        h1 { font-size: 20pt; text-align: center; border-bottom: 2px solid #0056b3; margin-bottom: 30px; }
        h2 { font-size: 14pt; margin-top: 30px; }
        .highlight-box { background-color: #f0f7ff; border-left: 4px solid #0056b3; padding: 15px; margin: 20px 0; }
        .warning-box { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f8f9fa; color: #0056b3; font-weight: bold; }
        .badge { display: inline-block; padding: 4px 8px; background: #28a745; color: white; border-radius: 4px; font-size: 9pt; font-weight: bold; }
        .badge-info { background: #17a2b8; }
        ul { margin-top: 5px; }
        li { margin-bottom: 8px; }
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <h1>INFORME DE ANÁLISIS DE LICITACIÓN PÚBLICA</h1>
    <p style="text-align: center; font-size: 12pt; color: #666; margin-top: -20px;">
        <strong>Proyecto Integrado de Obras, Dirección Facultativa y CSS - Antigua Base de S'Enclusa</strong>
    </p>

    <div class="highlight-box">
        <strong>Resumen Ejecutivo:</strong> Se trata de un contrato de servicios de arquitectura e ingeniería muy completo para el Consell Insular de Menorca. El presupuesto es atractivo (455.000 € sin IVA) y el enfoque principal es la rehabilitación de 2.142 m² de edificios militares para convertirlos en albergue y centro de interpretación. Al contar ya con equipo técnico propio, es una oportunidad inmejorable, siempre que se alcance la máxima puntuación en la Memoria Tècnica.
    </div>

    <h2>1. Datos Básicos del Contrato</h2>
    <table>
        <tr><th>Órgano de Contratación</th><td>Consell Insular de Menorca</td></tr>
        <tr><th>Presupuesto Base (Sin IVA)</th><td><strong>455.000,00 €</strong></td></tr>
        <tr><th>Presupuesto Total (Con IVA)</th><td>550.550,00 €</td></tr>
        <tr><th>Duración Estimada</th><td><strong>21 meses</strong> en total</td></tr>
        <tr><th>Desglose de Fases</th>
            <td>
                - <strong>Fase 1 (Redacción):</strong> 5 meses (Proy. Básico, Ejecutivo y Ambiental)<br>
                - <strong>Fase 2 (Dirección Obra):</strong> 16 meses
            </td>
        </tr>
    </table>

    <h2>2. Alcance Técnico (Objeto de Proyecto)</h2>
    <p>Rehabilitación de 8 edificaciones en la montaña de S'Enclusa, manteniendo la estética militar pero adaptando usos:</p>
    <ul>
        <li><strong>Edificios A, B, C y D:</strong> Albergue juvenil (50 plazas), servicios comunes, zona deportiva y comedor.</li>
        <li><strong>Edificios E y F:</strong> Cantina, tienda y punto de información.</li>
        <li><strong>Edificios G y H:</strong> Centro de interpretación de la Reserva de la Biosfera.</li>
    </ul>
    <p><strong>Total Superficie Construida a proyectar:</strong> 2.142,80 m².</p>

    <h2>3. Requisitos de Solvencia y Equipo Técnico</h2>
    <div class="warning-box">
        <strong>Atención:</strong> Para adjudicarse la obra, la empresa (o UTE) debe justificar solvencia económica y técnica. Como disponéis de profesionales, la configuración del equipo es el punto más fuerte.
    </div>
    <ul>
        <li><strong>Solvencia Económica:</strong> Seguro de Responsabilidad Civil Profesional por importe no inferior a 455.000 €.</li>
        <li><strong>Solvencia Técnica:</strong> Haber realizado trabajos similares en los últimos 3 años. El año de mayor facturación debe sumar al menos el 70% de la anualidad media del contrato (182.000 € justificados en un solo año).</li>
        <li><strong>Equipo Técnico Mínimo (Al menos 3 profesionales distintos):</strong>
            <ul>
                <li>1 Arquitecto/a (o equivalente) para Redacción y Dirección de Obra.</li>
                <li>1 Enginyer/a Tècnic/a (o equivalente) para Instalaciones y Actividades.</li>
                <li>1 Arquitecto/a Tècnic/a (o equivalente) para CSS y Dirección de Ejecución.</li>
                <li>1 Tècnic/a Ambiental para el Estudio de Impacto Ambiental.</li>
            </ul>
        </li>
    </ul>

    <div class="page-break"></div>

    <h2>4. Criterios de Adjudicación (Total 100 puntos)</h2>
    
    <h3>4.1. Criterios por Juicio de Valor (Sobre B1 - 45 Puntos) <span class="badge badge-info">Umbral mínimo: 23 puntos</span></h3>
    <p>Es vital presentar una propuesta de máxima calidad técnica (Máximo 30 páginas, Arial 11). Si no se superan los 23 puntos, se excluye al licitador sin abrir su oferta económica.</p>
    <table>
        <tr><th>Criterio Técnico (Memoria y Plànols)</th><th>Puntos</th></tr>
        <tr><td>Funcionalidad y usos previstos</td><td>5 pts</td></tr>
        <tr><td>Calidad del diseño y soluciones técnicas</td><td>5 pts</td></tr>
        <tr><td>Eficiencia energética y sostenibilidad</td><td>5 pts</td></tr>
        <tr><td>Facilidad de mantenimiento y reparación</td><td>5 pts</td></tr>
        <tr><td>Viabilidad constructiva</td><td>5 pts</td></tr>
        <tr><td>Integración en el entorno y cumplimiento normativo</td><td>5 pts</td></tr>
        <tr><td>Programación y calendario coherente (Gantt)</td><td>5 pts</td></tr>
        <tr><td>Nivel de detalle de la programación</td><td>5 pts</td></tr>
        <tr><td>Gestión de riesgos y contingencias</td><td>5 pts</td></tr>
    </table>

    <h3>4.2. Criterios Automáticos mediante Fórmulas (Sobre B2 - 55 Puntos)</h3>
    <table>
        <tr><th>Criterio Matemático</th><th>Puntos</th><th>Estrategia Recomendada</th></tr>
        <tr>
            <td><strong>Oferta Económica</strong></td>
            <td>49 pts</td>
            <td>La oferta más baja se lleva los 49 puntos. Evaluar margen de baja sobre los 455k €.</td>
        </tr>
        <tr>
            <td><strong>Visitas de obra adicionales (Fase 2)</strong></td>
            <td>3 pts</td>
            <td><span class="badge">Ofrecer 5 visitas/mes</span> (El mínimo exigido son 2. Ofrecer 5 otorga los 3 puntos directos).</td>
        </tr>
        <tr>
            <td><strong>Personal Técnico Adicional (Fase 1)</strong></td>
            <td>3 pts</td>
            <td><span class="badge">Ofrecer 3 técnicos extra</span> (Ofrecer 1 arquitecto, 1 ingeniero y 1 técnico ambiental a mayores del mínimo otorga los 3 puntos directos).</td>
        </tr>
    </table>

    <h2>5. Conclusiones y Plan de Acción Estratégico</h2>
    <ol>
        <li><strong>Formar el Equipo:</strong> Recopilar las titulaciones de los profesionales internos para cubrir el equipo mínimo y, crucialmente, el equipo adicional para asegurar los 3 puntos extra.</li>
        <li><strong>Redacción de la Memoria Tècnica (Sobre B1):</strong> Centrarse en la eficiencia energética y la sostenibilidad (es clave en Menorca Reserva de Biosfera). Diseñar un cronograma de Gantt de 5 meses muy detallado, previendo riesgos.</li>
        <li><strong>Tramitación:</strong> Preparar el DEUC (Documento Europeo Único de Contratación) y la firma electrónica.</li>
    </ol>

</body>
</html>
"""

work_dir = r"C:\Users\pablo\Documents\Presupuestador"
html_path = os.path.join(work_dir, "Estudio_Licitacion_SEnclusa.html")
pdf_path = os.path.join(work_dir, "Estudio_Licitacion_SEnclusa.pdf")

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
        print(f"PDF guardado en {pdf_path}")
    else:
        print(f"Error PDF: {result.stderr}")
else:
    print("Browser not found.")
