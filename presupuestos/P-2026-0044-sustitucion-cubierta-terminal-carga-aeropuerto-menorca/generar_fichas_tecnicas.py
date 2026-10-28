"""
Generador de Fichas Técnicas Oficiales en PDF para el Proyecto P-2026-0044
Aeropuerto de Menorca - Terminal de Carga (AENA 100.174)
"""
import os
from playwright.sync_api import sync_playwright

output_dir = os.path.join(os.path.dirname(__file__), "fichas-tecnicas")
os.makedirs(output_dir, exist_ok=True)

# 1. FICHA TÉCNICA: ACERO PREPINTADO ARCELORMITTAL GRANITE® HDX55
html_granite_hdx = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Ficha Técnica: ArcelorMittal Granite® HDX55</title>
  <style>
    @page { size: A4 portrait; margin: 10mm 12mm 10mm 12mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 10px; line-height: 1.35; color: #1e293b; margin: 0; background: #fff; }
    .header { border-bottom: 3px solid #b91c1c; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-end; }
    .title { font-size: 18px; font-weight: 800; color: #0f172a; margin: 0; }
    .subtitle { font-size: 11px; color: #64748b; font-weight: 600; margin-top: 3px; }
    .badge { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 10px; border: 1px solid #fecaca; }
    
    .section-title { font-size: 11px; font-weight: 700; color: #0f172a; border-left: 3.5px solid #b91c1c; padding-left: 6px; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    p { margin: 0 0 6px; text-align: justify; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 9.5px; }
    th { background: #0f172a; color: #fff; text-align: left; padding: 5px 8px; font-weight: 600; }
    td { padding: 4.5px 8px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f8fafc; }
    .param { font-weight: 600; color: #334155; width: 45%; }
    .val { color: #0f172a; font-weight: 500; }
    
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px; margin-bottom: 8px; }
    .box-title { font-weight: 700; color: #0f172a; margin-bottom: 4px; font-size: 10px; }
    
    .footer { border-top: 1px solid #cbd5e1; padding-top: 6px; margin-top: 14px; font-size: 8.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">FICHA TÉCNICA: GRANITE® HDX (55 µm)</div>
      <div class="subtitle">ArcelorMittal Europe Flat Products · Acero Prepintado para Ambientes Severos C5-M</div>
    </div>
    <div class="badge">RC5 · RUV4 · C5-M</div>
  </div>

  <p><strong>Granite® HDX</strong> es un sistema de acero prepintado orgánico multicapa de máxima durabilidad desarrollado específicamente para cerramientos exteriores y cubiertas industriales sometidas a exigencias ambientales severas: frentes marítimos de alta salinidad, fuerte radiación UV e industrias con emisiones corrosivas.</p>

  <div class="section-title">1. Estructura del Recubrimiento y Propiedades Físicas</div>
  <table>
    <tr><th>Parámetro Técnico</th><th>Especificación / Valor Homologado</th><th>Normativa / Ensayo</th></tr>
    <tr><td class="param">Espesor nominal pintura (cara exterior)</td><td class="val"><strong>55 µm</strong> (25 µm imprimación + 30 µm acabado estructurado)</td><td>EN 13523-1</td></tr>
    <tr><td class="param">Espesor nominal pintura (cara interior HDX)</td><td class="val"><strong>55 µm</strong> (Opción 2 caras para ambientes marinos agresivos)</td><td>EN 13523-1</td></tr>
    <tr><td class="param">Sustrato metálico base</td><td class="val">Chapa de acero estructural galvanizado Z275 o aleación Zinc-Magnesio Optigal®</td><td>EN 10346</td></tr>
    <tr><td class="param">Aspecto superficial y acabado</td><td class="val">Satinado con textura de poliamida estructurada antiarañazos</td><td>Visual</td></tr>
    <tr><td class="param">Nivel de brillo (Brillo a 60°)</td><td class="val">30 GU (Grained / Satinado homogéneo)</td><td>EN 13523-2</td></tr>
    <tr><td class="param">Espesores de chapa base</td><td class="val">0,50 mm / 0,60 mm / 0,70 mm (según aplicación)</td><td>EN 10143</td></tr>
  </table>

  <div class="section-title">2. Resistencia a la Corrosión y Durabilidad Ambiental</div>
  <div class="grid-2">
    <div class="box">
      <div class="box-title">Comportamiento frente a la Corrosión (RC5)</div>
      <table>
        <tr><td>Niebla salina neutra (NSS):</td><td><strong>≥ 700 horas</strong> (EN 13523-8)</td></tr>
        <tr><td>Categoría de corrosión:</td><td><strong>RC5 / RC5+</strong> (EN 10169)</td></tr>
        <tr><td>Resistencia a la condensación (QCT):</td><td><strong>≥ 1.500 horas</strong> (EN 13523-26)</td></tr>
        <tr><td>Distancia al mar recomendada:</td><td>Apto desde <strong>≥ 0 m (primera línea de costa)</strong></td></tr>
      </table>
    </div>
    <div class="box">
      <div class="box-title">Resistencia a la Radiación Solar UV (RUV4)</div>
      <table>
        <tr><td>Ensayo envejecimiento artificial UV:</td><td><strong>≥ 2.000 horas</strong> (EN 13523-10)</td></tr>
        <tr><td>Clasificación radiación solar:</td><td><strong>RUV4</strong> (Máxima categoría europea)</td></tr>
        <tr><td>Estabilidad cromática (ΔE):</td><td>≤ 2,0 tras ciclo de exposición</td></tr>
        <tr><td>Retención de brillo original:</td><td>≥ 80% post-envejecimiento</td></tr>
      </table>
    </div>
  </div>

  <div class="section-title">3. Prestaciones Mecánicas y Comportamiento al Fuego</div>
  <table>
    <tr><th>Propiedad Mecánica</th><th>Valor</th><th>Norma</th></tr>
    <tr><td class="param">Reacción al fuego</td><td class="val"><strong>Clase A1</strong> (Incombustible)</td><td>EN 13501-1</td></tr>
    <tr><td class="param">Adherencia tras plegado (T-bend)</td><td class="val">≤ 1 T (sin desprendimiento de revestimiento)</td><td>EN 13523-7</td></tr>
    <tr><td class="param">Resistencia al agrietamiento</td><td class="val">≤ 1,5 T</td><td>EN 13523-7</td></tr>
    <tr><td class="param">Resistencia al impacto</td><td class="val">18 Joules</td><td>EN 13523-5</td></tr>
    <tr><td class="param">Resistencia al rayado (Clemen)</td><td class="val">≥ 3,0 kg</td><td>EN 13523-12</td></tr>
    <tr><td class="param">Temperatura de servicio continuo</td><td class="val">-40 °C hasta +100 °C</td><td>Servicio</td></tr>
    <tr><td class="param">Cumplimiento medioambiental</td><td class="val">Libre de cromo hexavalente y metales pesados. Conforme a Reglamento REACH</td><td>REACH UE</td></tr>
  </table>

  <div class="footer">
    <span>Expediente: P-2026-0044 · Aeropuerto de Menorca Terminal de Carga</span>
    <span>ArcelorMittal Construction Materials / Granite® HDX Technical Dossier</span>
  </div>
</body>
</html>
"""

# 2. FICHA TÉCNICA: PANEL SÁNDWICH PIR 40 MM CUBIERTA
html_panel_pir = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Ficha Técnica: Panel Sándwich Cubierta PIR 40 mm</title>
  <style>
    @page { size: A4 portrait; margin: 10mm 12mm 10mm 12mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 10px; line-height: 1.35; color: #1e293b; margin: 0; background: #fff; }
    .header { border-bottom: 3px solid #0f172a; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-end; }
    .title { font-size: 18px; font-weight: 800; color: #0f172a; margin: 0; }
    .subtitle { font-size: 11px; color: #64748b; font-weight: 600; margin-top: 3px; }
    .badge { background: #e0f2fe; color: #0369a1; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 10px; border: 1px solid #bae6fd; }
    
    .section-title { font-size: 11px; font-weight: 700; color: #0f172a; border-left: 3.5px solid #0f172a; padding-left: 6px; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    p { margin: 0 0 6px; text-align: justify; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 9.5px; }
    th { background: #0f172a; color: #fff; text-align: left; padding: 5px 8px; font-weight: 600; }
    td { padding: 4.5px 8px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f8fafc; }
    .param { font-weight: 600; color: #334155; width: 45%; }
    .val { color: #0f172a; font-weight: 500; }
    
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px; margin-bottom: 8px; }
    .box-title { font-weight: 700; color: #0f172a; margin-bottom: 4px; font-size: 10px; }
    
    .footer { border-top: 1px solid #cbd5e1; padding-top: 6px; margin-top: 14px; font-size: 8.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">FICHA TÉCNICA: PANEL SÁNDWICH CUBIERTA PIR 40 MM</div>
      <div class="subtitle">Panel Autoportante 3 Grecas con Tapajuntas Oculto · UNE-EN 14509:2014</div>
    </div>
    <div class="badge">B-s1, d0 · Broof(t1) · PIR 40 mm</div>
  </div>

  <p>Panel sándwich de cubierta formado por dos chapas de acero grecado y un núcleo aislante central de espuma rígida de poliisocianurato (PIR) de alta densidad inyectada en continuo. Incorpora un perfilado exterior de 3 grecas de 40 mm de canto con sistema de tapajuntas metálico que oculta y protege la fijación pasante de las inclemencias meteorológicas.</p>

  <div class="section-title">1. Dimensiones, Pesos y Geometría</div>
  <table>
    <tr><th>Parámetro</th><th>Valor Nominal</th><th>Normativa / Tolerancias</th></tr>
    <tr><td class="param">Espesor nominal aislante</td><td class="val"><strong>40 mm</strong> en valle del perfil</td><td>UNE-EN 14509</td></tr>
    <tr><td class="param">Ancho útil modular</td><td class="val"><strong>1.000 mm</strong></td><td>EN 10143</td></tr>
    <tr><td class="param">Geometría exterior</td><td class="val">3 grecas trapeciales (altura greca 40 mm, paso 500 mm)</td><td>Estándar industrial</td></tr>
    <tr><td class="param">Sistema de unión longitudinal</td><td class="val">Solape con tapajuntas clipado de fijación oculta y junta estanca</td><td>Estanco</td></tr>
    <tr><td class="param">Espesor chapas de acero</td><td class="val">Exterior: 0,50 mm / Interior: 0,50 mm</td><td>EN 10143</td></tr>
    <tr><td class="param">Acabado protector anticorrosión</td><td class="val"><strong>Granite® HDX (55 µm) por ambas caras</strong> (RC5 / RUV4)</td><td>EN 10169</td></tr>
    <tr><td class="param">Peso superficial aproximado</td><td class="val"><strong>10,35 kg/m²</strong></td><td>Estimado s/ chapas 0,5/0,5</td></tr>
  </table>

  <div class="section-title">2. Aislamiento Térmico y Propiedades del Núcleo PIR</div>
  <div class="grid-2">
    <div class="box">
      <div class="box-title">Prestaciones Térmicas</div>
      <table>
        <tr><td>Conductividad térmica (λ):</td><td><strong>0,022 W/m·K</strong></td></tr>
        <tr><td>Transmitancia térmica (U):</td><td><strong>0,51 W/m²·K</strong></td></tr>
        <tr><td>Resistencia térmica (R):</td><td><strong>1,82 m²·K/W</strong></td></tr>
        <tr><td>Densidad media núcleo:</td><td><strong>40 ± 2 kg/m³</strong></td></tr>
      </table>
    </div>
    <div class="box">
      <div class="box-title">Reacción al Fuego y Seguridad</div>
      <table>
        <tr><td>Euroclase de reacción al fuego:</td><td><strong>B-s1, d0</strong> (UNE-EN 13501-1)</td></tr>
        <tr><td>Comportamiento fuego exterior:</td><td><strong>Broof (t1)</strong> (UNE-EN 13501-5)</td></tr>
        <tr><td>Aislamiento acústico (Rw):</td><td>26 dB (estimado)</td></tr>
        <tr><td>Agente espumante:</td><td>Libre de CFC y HCFC (GWP &lt; 5)</td></tr>
      </table>
    </div>
  </div>

  <div class="section-title">3. Tabla de Sobrecargas Admisibles (Luces entre correas en metros)</div>
  <table>
    <tr><th>Configuración de Apoyo</th><th>1,50 m</th><th>1,75 m</th><th>2,00 m</th><th>2,25 m</th><th>2,50 m</th></tr>
    <tr><td class="param">Presión admisible (viento/nieve) - 2 apoyos (kg/m²)</td><td class="val">260</td><td class="val">210</td><td class="val">165</td><td class="val">125</td><td class="val">95</td></tr>
    <tr><td class="param">Presión admisible (viento/nieve) - Múltiples apoyos (kg/m²)</td><td class="val">295</td><td class="val">245</td><td class="val">190</td><td class="val">145</td><td class="val">110</td></tr>
    <tr><td class="param">Succión de viento admisible (kg/m²)</td><td class="val">240</td><td class="val">195</td><td class="val">150</td><td class="val">115</td><td class="val">85</td></tr>
  </table>

  <div class="footer">
    <span>Expediente: P-2026-0044 · Aeropuerto de Menorca Terminal de Carga</span>
    <span>Panel de Cubierta Sándwich PIR 40 mm / Marcado CE UNE-EN 14509</span>
  </div>
</body>
</html>
"""

# 3. FICHA TÉCNICA: LÍNEA DE VIDA LUX-TOP® FSE 2003
html_luxtop = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Ficha Técnica: Línea de Vida LUX-top® FSE 2003</title>
  <style>
    @page { size: A4 portrait; margin: 10mm 12mm 10mm 12mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 10px; line-height: 1.35; color: #1e293b; margin: 0; background: #fff; }
    .header { border-bottom: 3px solid #2563eb; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-end; }
    .title { font-size: 18px; font-weight: 800; color: #0f172a; margin: 0; }
    .subtitle { font-size: 11px; color: #64748b; font-weight: 600; margin-top: 3px; }
    .badge { background: #dbeafe; color: #1e40af; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 10px; border: 1px solid #bfdbfe; }
    
    .section-title { font-size: 11px; font-weight: 700; color: #0f172a; border-left: 3.5px solid #2563eb; padding-left: 6px; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    p { margin: 0 0 6px; text-align: justify; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 9.5px; }
    th { background: #0f172a; color: #fff; text-align: left; padding: 5px 8px; font-weight: 600; }
    td { padding: 4.5px 8px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f8fafc; }
    .param { font-weight: 600; color: #334155; width: 45%; }
    .val { color: #0f172a; font-weight: 500; }
    
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px; margin-bottom: 8px; }
    .box-title { font-weight: 700; color: #0f172a; margin-bottom: 4px; font-size: 10px; }
    
    .footer { border-top: 1px solid #cbd5e1; padding-top: 6px; margin-top: 14px; font-size: 8.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">FICHA TÉCNICA: LÍNEA DE VIDA LUX-TOP® FSE 2003</div>
      <div class="subtitle">Sistema Horizontal Continuo de Cable de Acero Inoxidable · UNE-EN 795:2012 Tipo C</div>
    </div>
    <div class="badge">EN 795:2012 Tipo C · CEN/TS 16415</div>
  </div>

  <p><strong>LUX-top® FSE 2003</strong> es un sistema de anclaje lineal horizontal flexible homologado de alta gama diseñado para garantizar la seguridad en trabajos de mantenimiento y tránsito sobre cubiertas. Incorpora cable de acero inoxidable AISI 316, postes absorbedores de energía de deformación programada y piezas intermedias que permiten el paso del carro deslizador sin necesidad de desconectarse en ningún momento.</p>

  <div class="section-title">1. Componentes Principales y Materiales</div>
  <table>
    <tr><th>Elemento del Sistema</th><th>Especificación Técnica</th><th>Material</th></tr>
    <tr><td class="param">Cable de seguridad continuo</td><td class="val">Diámetro <strong>Ø 8 mm</strong> (construcción 7x7 triple torsión de alta resistencia)</td><td>Acero Inoxidable AISI 316 (1.4401)</td></tr>
    <tr><td class="param">Postes absorbedores de impacto</td><td class="val">LUX-top® ASP deformables por torsión / tracción para disipación de carga</td><td>Acero Inoxidable AISI 304 / 316</td></tr>
    <tr><td class="param">Fijación a cubierta sándwich</td><td class="val">Placas de fijación estanca a grecas mediante remaches estancos bulb-tite y juntas EPDM</td><td>Aluminio / Inox + EPDM</td></tr>
    <tr><td class="param">Elemento tensor y amortiguador</td><td class="val">Tensor horquilla con testigo visual de pretensado integrado (tensado 80-100 kg)</td><td>Acero Inoxidable AISI 316</td></tr>
    <tr><td class="param">Carro pasante móvil</td><td class="val">Carro corredero multidireccional LUX-top® de paso continuo por piezas intermedias</td><td>Acero Inoxidable AISI 316</td></tr>
    <tr><td class="param">Soportes intermedios y esquinas</td><td class="val">Guías pasantes y piezas de curva hasta 90° sin interrumpir la línea de anclaje</td><td>Acero Inoxidable AISI 316</td></tr>
  </table>

  <div class="section-title">2. Parámetros Operativos y Homologación</div>
  <div class="grid-2">
    <div class="box">
      <div class="box-title">Certificaciones y Capacidad</div>
      <table>
        <tr><td>Norma de anclajes:</td><td><strong>UNE-EN 795:2012 Tipo C</strong></td></tr>
        <tr><td>Uso simultáneo multiusuario:</td><td><strong>CEN/TS 16415:2013</strong> (Hasta 4 usuarios)</td></tr>
        <tr><td>Resistencia a la rotura cable:</td><td><strong>≥ 36 kN (~3.670 kg)</strong></td></tr>
        <tr><td>Carga máxima transmitida a estructura:</td><td>≤ 10 kN (gracias a absorbedores)</td></tr>
      </table>
    </div>
    <div class="box">
      <div class="box-title">Condiciones de Instalación</div>
      <table>
        <tr><td>Distancia máx. entre postes:</td><td>Recomendada <strong>7,5 a 10,0 m</strong> (máx. 15 m)</td></tr>
        <tr><td>Inclinación de cubierta admisible:</td><td>Hasta 15° respecto a horizontal</td></tr>
        <tr><td>Garantía y vida útil:</td><td>Acero anticorrosión marina garantizado</td></tr>
        <tr><td>Inspección periódica:</td><td>Anual obligatoria s/ UNE-EN 365</td></tr>
      </table>
    </div>
  </div>

  <div class="section-title">3. Procedimiento de Ensayo y Entrega Oficial</div>
  <table>
    <tr><th>Documento / Ensayo</th><th>Descripción</th><th>Entidad / Validez</th></tr>
    <tr><td class="param">Marcado CE y Declaración de Conformidad</td><td class="val">Certificado de conformidad con normativa comunitaria y DEKRA EXAM GmbH</td><td>Organismo Notificado CE</td></tr>
    <tr><td class="param">Prueba de tracción in situ</td><td class="val">Ensayo de tracción estática a 5 kN en extremos para verificación de estanqueidad y anclaje</td><td>Técnico Homologado HAM</td></tr>
    <tr><td class="param">Placa de señalización indeleble</td><td class="val">Placa grabada en acero inox con fecha montaje, n° instalador, n° usuarios y revisión</td><td>Fijada en punto de acceso</td></tr>
  </table>

  <div class="footer">
    <span>Expediente: P-2026-0044 · Aeropuerto de Menorca Terminal de Carga</span>
    <span>Sistema de Línea de Vida LUX-top® FSE 2003 / Homologación EN 795:2012</span>
  </div>
</body>
</html>
"""

# 4. FICHA TÉCNICA: ESCALERA FIJA DE GATO CON CRINOLINA EN ACERO INOXIDABLE
html_escalera = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Ficha Técnica: Escalera Fija con Crinolina en Acero Inoxidable</title>
  <style>
    @page { size: A4 portrait; margin: 10mm 12mm 10mm 12mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 10px; line-height: 1.35; color: #1e293b; margin: 0; background: #fff; }
    .header { border-bottom: 3px solid #059669; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-end; }
    .title { font-size: 18px; font-weight: 800; color: #0f172a; margin: 0; }
    .subtitle { font-size: 11px; color: #64748b; font-weight: 600; margin-top: 3px; }
    .badge { background: #d1fae5; color: #065f46; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 10px; border: 1px solid #a7f3d0; }
    
    .section-title { font-size: 11px; font-weight: 700; color: #0f172a; border-left: 3.5px solid #059669; padding-left: 6px; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    p { margin: 0 0 6px; text-align: justify; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 9.5px; }
    th { background: #0f172a; color: #fff; text-align: left; padding: 5px 8px; font-weight: 600; }
    td { padding: 4.5px 8px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f8fafc; }
    .param { font-weight: 600; color: #334155; width: 45%; }
    .val { color: #0f172a; font-weight: 500; }
    
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px; margin-bottom: 8px; }
    .box-title { font-weight: 700; color: #0f172a; margin-bottom: 4px; font-size: 10px; }
    
    .footer { border-top: 1px solid #cbd5e1; padding-top: 6px; margin-top: 14px; font-size: 8.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">FICHA TÉCNICA: ESCALERA FIJA DE GATO INOX</div>
      <div class="subtitle">Escalera con Protección Dorsal (Crinolina) · UNE-EN ISO 14122-4 / INSST NTP 1160</div>
    </div>
    <div class="badge">AISI 304 / 316 · ISO 14122-4</div>
  </div>

  <p>Escalera vertical fija de gato fabricada íntegramente en <strong>acero inoxidable (AISI 304 / AISI 316)</strong> destinada al acceso seguro y permanente a cubiertas industriales e instalaciones aeroportuarias en ambiente marino. Incorpora jaula de protección dorsal (crinolina), cancela superior de cierre automático por gravedad/muelle y puerta inferior anti-intrusión con candado conforme a protocolos AENA.</p>

  <div class="section-title">1. Geometría y Criterios Normativos (UNE-EN ISO 14122-4)</div>
  <table>
    <tr><th>Parámetro de Diseño</th><th>Valor Cumplido</th><th>Criterio Normativo</th></tr>
    <tr><td class="param">Material de fabricación</td><td class="val"><strong>Acero Inoxidable AISI 304 / 316</strong> (alta resistencia marina)</td><td>UNE-EN 10088</td></tr>
    <tr><td class="param">Ancho útil entre montantes</td><td class="val"><strong>450 mm</strong></td><td>Norma exige: 400 a 600 mm</td></tr>
    <tr><td class="param">Paso entre peldaños</td><td class="val"><strong>250 mm uniforme</strong></td><td>Norma exige: 225 a 300 mm</td></tr>
    <tr><td class="param">Peldaños antideslizantes</td><td class="val">Perfil perforado embutido antideslizante con huella ≥ 25 mm</td><td>Superficie segura</td></tr>
    <tr><td class="param">Inicio de la jaula dorsal (crinolina)</td><td class="val">A <strong>2.300 mm</strong> del suelo (voladizo) / <strong>2.500 mm</strong> (cubierta)</td><td>Norma exige: 2.200 a 3.000 mm</td></tr>
    <tr><td class="param">Diámetro interior de la jaula</td><td class="val"><strong>700 mm</strong> libre desde eje de peldaño</td><td>Norma exige: 650 a 800 mm</td></tr>
    <tr><td class="param">Separación entre aros horizontales</td><td class="val"><strong>1.200 mm</strong> máximo</td><td>Norma exige: ≤ 1.500 mm</td></tr>
    <tr><td class="param">Pletinas verticales interiores</td><td class="val">5 pletinas continuas soldadas por cara interior (separación &lt; 280 mm)</td><td>Norma exige: ≤ 300 mm</td></tr>
  </table>

  <div class="section-title">2. Desembarco Superior y Seguridad Aeroportuaria AENA</div>
  <div class="grid-2">
    <div class="box">
      <div class="box-title">Plataforma de Desembarco Superior</div>
      <table>
        <tr><td>Prolongación de largueros:</td><td><strong>1.100 mm</strong> sobre cota de llegada</td></tr>
        <tr><td>Ensanchamiento de paso:</td><td>Desembarco ensanchado a 1.000 mm</td></tr>
        <tr><td>Puerta de seguridad:</td><td>Cancela batiente inox con cierre automático</td></tr>
        <tr><td>Rodapié perimetral:</td><td>Altura 150 mm en zona de desembarco</td></tr>
      </table>
    </div>
    <div class="box">
      <div class="box-title">Control de Acceso Inferior (AENA)</div>
      <table>
        <tr><td>Placa anti-intrusión:</td><td>Chapa inox abatible cubre-peldaños h=1,80 m</td></tr>
        <tr><td>Cierre de seguridad:</td><td>Portacandados de acero inox para control AENA</td></tr>
        <tr><td>Fijación mural/estructura:</td><td>Consolas inox cada 1,50 m con anclaje A4</td></tr>
        <tr><td>Carga de ensayo:</td><td>Conforme a cargas de servicio ISO 14122-4</td></tr>
      </table>
    </div>
  </div>

  <div class="section-title">3. Modelos Aplicados en Proyecto Terminal Carga Menorca</div>
  <table>
    <tr><th>Referencia</th><th>Ubicación</th><th>Desnivel a Salvar</th><th>Longitud Total</th><th>Importe Opcional</th></tr>
    <tr><td class="param"><strong>OPC-01 (ESC-VOL-INOX)</strong></td><td class="val">Acceso desde suelo a Voladizo Este</td><td class="val">H ≈ 4,20 m</td><td class="val">5,30 m (con desembarco)</td><td class="val"><strong>5.005,00 € + IVA</strong></td></tr>
    <tr><td class="param"><strong>OPC-02 (ESC-CUB-INOX)</strong></td><td class="val">Acceso desde suelo a Cubierta Principal</td><td class="val">H ≈ 6,80 m</td><td class="val">7,90 m (con desembarco)</td><td class="val"><strong>7.735,00 € + IVA</strong></td></tr>
  </table>

  <div class="footer">
    <span>Expediente: P-2026-0044 · Aeropuerto de Menorca Terminal de Carga</span>
    <span>Escaleras Fijas con Crinolina en Acero Inoxidable / UNE-EN ISO 14122-4</span>
  </div>
</body>
</html>
"""

# 5. FICHA TÉCNICA: TORNILLERÍA ROSCACHAPA GALVANIZADA CON JUNTA EPDM
html_tornilleria = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Ficha Técnica: Tornillería Roscachapa con Arandela EPDM</title>
  <style>
    @page { size: A4 portrait; margin: 10mm 12mm 10mm 12mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 10px; line-height: 1.35; color: #1e293b; margin: 0; background: #fff; }
    .header { border-bottom: 3px solid #d97706; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-end; }
    .title { font-size: 18px; font-weight: 800; color: #0f172a; margin: 0; }
    .subtitle { font-size: 11px; color: #64748b; font-weight: 600; margin-top: 3px; }
    .badge { background: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 10px; border: 1px solid #fde68a; }
    
    .section-title { font-size: 11px; font-weight: 700; color: #0f172a; border-left: 3.5px solid #d97706; padding-left: 6px; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    p { margin: 0 0 6px; text-align: justify; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 9.5px; }
    th { background: #0f172a; color: #fff; text-align: left; padding: 5px 8px; font-weight: 600; }
    td { padding: 4.5px 8px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f8fafc; }
    .param { font-weight: 600; color: #334155; width: 45%; }
    .val { color: #0f172a; font-weight: 500; }
    
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px; margin-bottom: 8px; }
    .box-title { font-weight: 700; color: #0f172a; margin-bottom: 4px; font-size: 10px; }
    
    .footer { border-top: 1px solid #cbd5e1; padding-top: 6px; margin-top: 14px; font-size: 8.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">FICHA TÉCNICA: TORNILLERÍA ROSCACHAPA GALVANIZADA CON EPDM</div>
      <div class="subtitle">Fijación Estanca para Cubiertas y Cerramientos Metálicos · DIN 7504-K</div>
    </div>
    <div class="badge">DIN 7504-K · EPDM Vulcanizado</div>
  </div>

  <p>Tornillo autorroscante / autotaladrante de cabeza hexagonal con arandela metálica incorporada con junta vulcanizada de elastómero de etileno-propileno-dieno (EPDM). Diseñado para la fijación mecánica directa sobre correas y perfiles metálicos garantizando un apriete controlado y estanqueidad total frente al paso del agua y condensación.</p>

  <div class="section-title">1. Características Técnicas y Geométricas</div>
  <table>
    <tr><th>Parámetro Técnico</th><th>Valor Nominal</th><th>Normativa / Referencia</th></tr>
    <tr><td class="param">Material del tornillo</td><td class="val">Acero al carbono cementado y templado de alta resistencia</td><td>DIN 7504-K / ISO 15480</td></tr>
    <tr><td class="param">Recubrimiento superficial</td><td class="val">Galvanizado / Cincado electrolítico de alta protección (≥ 12 µm)</td><td>ISO 4042</td></tr>
    <tr><td class="param">Tipo de cabeza</td><td class="val">Hexagonal con valona integrada (entrecaras 8 mm)</td><td>DIN 7504-K</td></tr>
    <tr><td class="param">Arandela de estanqueidad</td><td class="val">Arandela metálica estampada de Ø 16 mm / Ø 19 mm</td><td>DIN 7504</td></tr>
    <tr><td class="param">Junta de hermeticidad</td><td class="val"><strong>EPDM vulcanizado</strong> de alta elasticidad resistente a rayos UV y ozono</td><td>Elastómero EPDM</td></tr>
    <tr><td class="param">Punta perforante</td><td class="val">Punta broca autotaladrante (#3) para espesores de correa de 1,5 a 6,0 mm</td><td>Perforación rápida</td></tr>
    <tr><td class="param">Diámetro y longitudes</td><td class="val">Ø 5,5 / Ø 6,3 mm (longitud adaptada al espesor del panel: 80 - 100 mm)</td><td>Montaje en onda alta</td></tr>
  </table>

  <div class="section-title">2. Resistencia Mecánica y Estanqueidad</div>
  <div class="grid-2">
    <div class="box">
      <div class="box-title">Valores Resistentes Característicos</div>
      <table>
        <tr><td>Resistencia a la tracción (axial):</td><td><strong>≥ 12,8 kN</strong></td></tr>
        <tr><td>Resistencia a cortante (cizalladura):</td><td><strong>≥ 9,5 kN</strong></td></tr>
        <tr><td>Par de rotura por torsión:</td><td><strong>≥ 14,0 N·m</strong></td></tr>
        <tr><td>Dureza superficial del núcleo:</td><td>≥ 320 HV / Superficial ≥ 550 HV</td></tr>
      </table>
    </div>
    <div class="box">
      <div class="box-title">Propiedades de la Junta EPDM</div>
      <table>
        <tr><td>Rango de temperatura:</td><td>-40 °C hasta +120 °C</td></tr>
        <tr><td>Resistencia a intemperie:</td><td>Excelente frente a ozono, UV y salitre</td></tr>
        <tr><td>Deformación remanente:</td><td>&lt; 25% tras compresión mantenida</td></tr>
        <tr><td>Estanqueidad hidráulica:</td><td>Probada a presión estática de agua</td></tr>
      </table>
    </div>
  </div>

  <div class="section-title">3. Instrucciones de Colocación en Obra</div>
  <table>
    <tr><th>Fase de Montaje</th><th>Prescripción Técnica</th></tr>
    <tr><td class="param">Herramienta de atornillado</td><td class="val">Atornillador eléctrico con embrague de profundidad y velocidad entre 1.500 y 2.000 rpm.</td></tr>
    <tr><td class="param">Control del par de apriete</td><td class="val">El apriete debe realizarse hasta que la junta de EPDM rebose ligeramente el perímetro de la arandela sin llegar a deformarse en exceso ni cortarse.</td></tr>
    <tr><td class="param">Ubicación en cubierta</td><td class="val">Siempre en la cúspide de la greca superior (onda alta) apoyada en caballete o grapa de fijación de tapajuntas para evitar zonas de escorrentía directa.</td></tr>
  </table>

  <div class="footer">
    <span>Expediente: P-2026-0044 · Aeropuerto de Menorca Terminal de Carga</span>
    <span>Tornillería Autotaladrante de Acero Galvanizado con Arandela EPDM / DIN 7504-K</span>
  </div>
</body>
</html>
"""

fichas = [
    ("FT-01-acero-granite-hdx55-arcelormittal.pdf", html_granite_hdx),
    ("FT-02-panel-sandwich-pir-40mm-cubierta.pdf", html_panel_pir),
    ("FT-03-linea-de-vida-luxtop-fse2003.pdf", html_luxtop),
    ("FT-04-escalera-gato-crinolina-acero-inoxidable.pdf", html_escalera),
    ("FT-05-tornilleria-roscachapa-galvanizada-epdm.pdf", html_tornilleria)
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for filename, html_content in fichas:
        page = browser.new_page()
        page.set_content(html_content)
        pdf_path = os.path.join(output_dir, filename)
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        page.close()
        print(f"Ficha técnica generada: {pdf_path}")
    browser.close()

print("Todas las fichas técnicas han sido generadas exitosamente en PDF.")
