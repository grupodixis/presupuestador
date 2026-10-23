import os

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Plantilla Memoria Técnica - S'Enclusa</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            margin: 3cm;
            color: #000;
        }
        h1 { font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 2cm; text-transform: uppercase; }
        h2 { font-size: 14pt; font-weight: bold; margin-top: 1.5cm; color: #1f497d; border-bottom: 1px solid #1f497d; }
        h3 { font-size: 12pt; font-weight: bold; margin-top: 1cm; color: #333; }
        .instrucciones {
            background-color: #f8f9fa;
            border-left: 4px solid #dc3545;
            padding: 10px;
            font-size: 10pt;
            color: #666;
            font-style: italic;
            margin-bottom: 15px;
        }
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <h1>SOBRE B1: PROPOSTA TÈCNICA<br><br>REDACCIÓ DEL PROJECTE I DIRECCIÓ D'OBRES<br>ANTIGA BASE DE S'ENCLUSA</h1>
    <p style="text-align: center;"><strong>Licitador:</strong> [NOMBRE DE VUESTRA EMPRESA/UTE]</p>

    <div class="page-break"></div>

    <h2>ÍNDEX</h2>
    <p><em>(L'índex i els annexos no computen per al límit màxim de 30 pàgines)</em></p>
    <p>1. Proposta d'actuacions pel projecte constructiu</p>
    <p>&nbsp;&nbsp;&nbsp;1.1. Funcionalitat i usos previstos</p>
    <p>&nbsp;&nbsp;&nbsp;1.2. Qualitat del disseny i solucions tècniques</p>
    <p>&nbsp;&nbsp;&nbsp;1.3. Eficiència energètica i sostenibilitat</p>
    <p>&nbsp;&nbsp;&nbsp;1.4. Facilitat en el manteniment i la reparació</p>
    <p>&nbsp;&nbsp;&nbsp;1.5. Viabilitat constructiva</p>
    <p>&nbsp;&nbsp;&nbsp;1.6. Integració en l'entorn i compliment normatiu</p>
    <p>2. Programació de les actuacions proposades</p>
    <p>&nbsp;&nbsp;&nbsp;2.1. Coherència i realisme del calendari</p>
    <p>&nbsp;&nbsp;&nbsp;2.2. Nivell de detall de la programació</p>
    <p>&nbsp;&nbsp;&nbsp;2.3. Gestió de terminis i contingències</p>

    <div class="page-break"></div>

    <h2>1. PROPOSTA D'ACTUACIONS PEL PROJECTE CONSTRUCTIU (Fins a 30 punts)</h2>

    <h3>1.1. Funcionalitat i usos previstos (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: No os limitéis a describir lo que piden los pliegos. Para el 5 hay que dar una "Solució òptima i clarament superior". Proponed mejoras en la distribución del Albergue (Edificio A) para maximizar la luz natural, y circuitos separados para los usuarios del albergue y los visitantes de los Centros de Interpretación (Edificios G y H) para evitar cruces.</div>
    <p>[Redactar aquí la propuesta de zonificación, circulaciones y organigramas espaciales de los 8 edificios...]</p>

    <h3>1.2. Qualitat del disseny i les solucions tècniques (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: El jurado pide diseño "excel·lent, innovador i molt ben integrat". Describid soluciones arquitectónicas que respeten la herencia "militar" e industrial del entorno, usando materiales vistos, acero corten, madera local, etc.</div>
    <p>[Redactar aquí materiales propuestos, lenguaje arquitectónico y justificación estructural...]</p>

    <h3>1.3. Eficiència energètica i sostenibilitat (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: Estamos en una Reserva de la Biosfera (ANEI). Para el 5/5 exigirán "un alt nivell d’eficiència demostrable". Incluid propuestas de autoconsumo fotovoltaico en cubiertas ocultas, aerotermia, recuperación de aguas pluviales para inodoros, y uso de materiales "Km 0" de Menorca para reducir la huella de carbono.</div>
    <p>[Redactar aquí el esquema de instalaciones térmicas, ciclo del agua y pasaporte de materiales...]</p>

    <h3>1.4. Facilitat en el manteniment i la reparació (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: "Solucions demostrables de costos mínims i alta durabilitat". Un entorno de montaña salino oxida todo. Proponed acabados sin mantenimiento (hormigón visto, maderas termotratadas) y galerías de instalaciones registrables (patinillos) para que el personal del Consell no tenga que romper paredes al reparar tuberías.</div>
    <p>[Redactar aquí el plan de mantenibilidad, accesibilidad a patinillos de instalaciones y durabilidad de materiales en ambiente salino/montaña...]</p>

    <h3>1.5. Viabilitat constructiva (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: S'Enclusa es de "difícil acceso". Para ganar los 5 puntos, debéis explicar cómo van a llegar los camiones hormigonera y las grúas arriba. Proponed acopios intermedios, uso de maquinaria ligera y prefabricación en taller para subir las piezas listas para ensamblar.</div>
    <p>[Redactar aquí la logística de obra, fases de acopio, gestión del tráfico en el camino de subida y medios auxiliares...]</p>

    <h3>1.6. Integració en l'entorn i compliment normatiu (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: Justificar exhaustivamente el PGOU de Ferreries (Sòl rústic protegit ANEI). Explicar cómo la volumetría no se altera, cómo se camuflan las máquinas de clima (aerotermia) para que no rompan el paisaje, y el estricto cumplimiento del CTE y normativas de accesibilidad.</div>
    <p>[Redactar aquí justificación urbanística y de integración paisajística...]</p>

    <div class="page-break"></div>

    <h2>2. PROGRAMACIÓ DE LES ACTUACIONS PROPOSADES (Fins a 15 punts)</h2>

    <h3>2.1. Coherència i realisme del calendari (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: Incluid un diagrama de Gantt incrustado en el texto. Justificad por qué dedicáis 2 meses al básico, 2 al ejecutivo y 1 a la tramitación. Vinculadlo con las reuniones obligatorias exigidas en los pliegos con el promotor.</div>
    <p>[Insertar diagrama de Gantt global e hitos clave de entrega...]</p>

    <h3>2.2. Nivell de detall i claredat (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: Desglosar el Gantt no solo por fases, sino por disciplinas (Estructuras, Instalaciones, Arquitectura, Estudio de Seguridad, Impacto Ambiental) y asignando recursos (qué técnico de la UTE hace qué).</div>
    <p>[Insertar desglose de tareas, dependencias (camino crítico) y responsables...]</p>

    <h3>2.3. Capacitat de gestió de terminis i contingències (Max. 5 punts)</h3>
    <div class="instrucciones">ESTRATEGIA PARA EL 5/5: Matriz de Riesgos. Identificar 3-4 riesgos graves (Ej: retrasos en informes de Patrimoni/Costes, bajas por enfermedad del equipo redactor, cambios normativos). Explicar el plan de contingencia (técnicos suplentes, reuniones previas con los técnicos municipales para adelantar criterios, etc).</div>
    <p>[Insertar tabla de evaluación de riesgos (Probabilidad x Impacto) y medidas correctoras...]</p>

</body>
</html>
"""

work_dir = r"C:\Users\pablo\Documents\Presupuestador"
html_path = os.path.join(work_dir, "Esqueleto_Memoria_Tecnica.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Plantilla guardada en {html_path}")
