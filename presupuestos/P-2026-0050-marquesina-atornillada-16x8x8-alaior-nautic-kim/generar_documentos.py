import os
import sys
import json
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "datos.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

def create_html_client():
    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presupuesto P-2026-0050: Marquesina Industrial Atornillable 16x8x8m - Nautic KIM</title>
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
      font-size: 8.8px;
      line-height: 1.38;
    }}
    .sheet {{
      width: 210mm;
      margin: 0 auto;
      background: #ffffff;
      padding: 10mm 13mm;
    }}
    header {{
      background: #0f172a;
      color: #fff;
      padding: 14px 18px;
      border-radius: 8px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 16px;
      align-items: center;
      border-bottom: 4px solid #b45309;
      margin-bottom: 10px;
    }}
    .brand {{ display: flex; align-items: center; gap: 14px; }}
    .brand-title {{ font-size: 14px; font-weight: 800; letter-spacing: 0.5px; color: #ffffff; text-transform: uppercase; }}
    .brand-sub {{ font-size: 8px; color: #94a3b8; margin-top: 2px; }}
    .header-doc {{ text-align: right; }}
    .doc-num {{ font-size: 13px; font-weight: 800; color: #fbbf24; }}
    .doc-date {{ font-size: 8px; color: #cbd5e1; }}
    
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 10px; }}
    .card-title {{ font-size: 8.5px; font-weight: 800; text-transform: uppercase; color: #b45309; margin-bottom: 4px; border-bottom: 1px solid #e2e8f0; padding-bottom: 3px; }}
    .card-line {{ display: flex; justify-content: space-between; margin-bottom: 2px; }}
    .card-label {{ color: #64748b; font-weight: 600; font-size: 8px; }}
    .card-val {{ color: #0f172a; font-weight: 700; text-align: right; font-size: 8px; }}

    .alert-banner {{
      background: #fef2f2;
      border: 1.5px solid #dc2626;
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .alert-icon {{ font-size: 18px; color: #dc2626; font-weight: 900; line-height: 1; }}
    .alert-text {{ font-size: 8.5px; color: #991b1b; line-height: 1.35; }}
    .alert-text b {{ color: #7f1d1d; text-transform: uppercase; }}

    .highlight-banner {{
      background: #eff6ff;
      border-left: 4px solid #2563eb;
      padding: 6px 10px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-around;
      font-size: 8.5px;
    }}
    .hb-item {{ text-align: center; }}
    .hb-val {{ font-size: 10.5px; font-weight: 800; color: #1e3a8a; }}
    .hb-lbl {{ font-size: 7.5px; color: #475569; text-transform: uppercase; font-weight: 600; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
    }}
    th {{
      background: #0f172a;
      color: #ffffff;
      font-weight: 700;
      font-size: 8px;
      text-transform: uppercase;
      padding: 6px 7px;
      text-align: left;
      border: 1px solid #0f172a;
    }}
    th.r, td.r {{ text-align: right; }}
    th.c, td.c {{ text-align: center; }}
    td {{
      padding: 5.2px 7px;
      border: 1px solid #e2e8f0;
      font-size: 8px;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: #f8fafc; }}
    .desc-text {{ font-size: 7.5px; color: #475569; margin-top: 2px; line-height: 1.3; }}

    .totals-area {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 10px;
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
      padding: 5px 10px;
      font-size: 8.5px;
      border-bottom: 1px solid #e2e8f0;
    }}
    .t-row:last-child {{
      border-bottom: none;
      background: #fef3c7;
      font-size: 10.5px;
      font-weight: 800;
      color: #92400e;
      border-top: 2px solid #b45309;
    }}

    .conditions {{
      background: #f1f5f9;
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 7.5px;
      color: #334155;
      line-height: 1.35;
    }}
    .cond-title {{ font-weight: 800; text-transform: uppercase; color: #0f172a; margin-bottom: 3px; font-size: 8px; }}
    .cond-list {{ margin: 0; padding-left: 12px; }}
    .cond-list li {{ margin-bottom: 2px; }}

    footer {{
      margin-top: 10px;
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
        <div class="card-title">Especificaciones Principales de la Oferta</div>
        <div class="card-line"><span class="card-label">Tipología:</span><span class="card-val">Marquesina rectangular 100% atornillable</span></div>
        <div class="card-line"><span class="card-label">Dimensiones en Planta:</span><span class="card-val">16,00 m largo x 8,00 m ancho libre</span></div>
        <div class="card-line"><span class="card-label">Altura Libre al Alero:</span><span class="card-val">8,00 m (Cumbrera a 8,60 m)</span></div>
        <div class="card-line"><span class="card-label">Superficie Techada:</span><span class="card-val">150,30 m² (faldón con aleros)</span></div>
        <div class="card-line"><span class="card-label">Cubierta y Acabado:</span><span class="card-val">Sándwich PUR 30 mm / Pintura Epoxi+2C poliuretano</span></div>
      </div>
    </div>

    <!-- BANNER DE EXCLUSIÓN EXPRESA -->
    <div class="alert-banner">
      <div class="alert-icon">⚠️</div>
      <div class="alert-text">
        <b>Exclusión Expresa de Cimentación:</b> Este presupuesto <b>NO INCLUYE la ejecución de zapatas (necesarias) ni solera</b>. Al tratarse de una estructura con pilares a 8 metros de altura, las zapatas de hormigón armado para la absorción de los momentos de viento y axil corren por cuenta del cliente, debiendo ser ejecutadas previamente según las dimensiones, armados y cargas que facilitará DIXIS a partir del pre-cálculo de la Partida 01.
      </div>
    </div>

    <div class="highlight-banner">
      <div class="hb-item"><div class="hb-val">6.471 Kg</div><div class="hb-lbl">Acero S275JR a 5,00 €/kg</div></div>
      <div class="hb-item"><div class="hb-val">150,30 m²</div><div class="hb-lbl">Panel PUR 30 a 115,00 €/m²</div></div>
      <div class="hb-item"><div class="hb-val">Pre-cálculo</div><div class="hb-lbl">Dimensionamiento Estimativo</div></div>
      <div class="hb-item"><div class="hb-val">C3 / C4 Marino</div><div class="hb-lbl">Pintura HAM (Sin horno)</div></div>
      <div class="hb-item"><div class="hb-val">H = 8,00 m</div><div class="hb-lbl">Montaje con Grúa y PEMP</div></div>
    </div>

    <table>
      <thead>
        <tr>
          <th class="c" style="width: 28px;">Nº</th>
          <th>Concepto y Descripción de la Partida</th>
          <th class="c" style="width: 32px;">Ud</th>
          <th class="r" style="width: 45px;">Cant.</th>
          <th class="r" style="width: 65px;">Precio (€)</th>
          <th class="r" style="width: 75px;">Importe (€)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="c"><b>01</b></td>
          <td>
            <b>PRE-CÁLCULO ESTRUCTURAL, INGENIERÍA PRELIMINAR Y ESTIMACIÓN DE DIMENSIONES</b>
            <div class="desc-text">Pre-cálculo estructural analítico y modelado preliminar para dimensionamiento de perfiles, estimación de kg de acero y elaboración de presupuesto técnico aproximado según acciones de viento del CTE (Zona C en Alaior) para estructura atornillable mecano de 16x8x8 m. Incluye estimación inicial de cargas a transmitir a las zapatas de cimentación requeridas.</div>
          </td>
          <td class="c">PA</td>
          <td class="r">1,00</td>
          <td class="r">3.000,00 €</td>
          <td class="r"><b>3.000,00 €</b></td>
        </tr>
        <tr>
          <td class="c"><b>02</b></td>
          <td>
            <b>FABRICACIÓN EN TALLER DE ESTRUCTURA METÁLICA ATORNILLABLE (6.471 KG A 5,00 €/KG)</b>
            <div class="desc-text">Fabricación integral de estructura tipo mecano (16x8x8 m). 10 pilares tubo 180x180x6 mm con placas base 350x350x20 mm y rigidizadores; 5 dinteles IPE 240; 10 jabalcones a 45° tubo 100x100x4 mm; vigas coronación 120x120x5 mm; 8 líneas correas 100x50x3 mm; cruces San Andrés Ø20 mm con tensores M20 8.8; tornillería de alta resistencia M16/M20 cincada. Cotizado a 5,00 €/kg.</div>
          </td>
          <td class="c">Kg</td>
          <td class="r">6.471,00</td>
          <td class="r">5,00 €</td>
          <td class="r"><b>32.355,00 €</b></td>
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
            <b>SUMINISTRO Y MONTAJE DE CUBIERTA EN PANEL SÁNDWICH PUR 30 MM Y REMATERÍA (115,00 €/M²)</b>
            <div class="desc-text">Suministro e instalación sobre correas de 150,30 m² de panel sándwich de cubierta de 30 mm (PUR 40 kg/m³, chapa grecada exterior 0,5 mm prelacada e interior 0,4 mm blanco pirineo). Fijaciones bimetálicas autotaladrantes con arandelas de estanqueidad de EPDM. Remate troquelado de cumbrera y testeros laterales plegados. Cotizado a 115,00 €/m².</div>
          </td>
          <td class="c">m²</td>
          <td class="r">150,30</td>
          <td class="r">115,00 €</td>
          <td class="r"><b>17.284,50 €</b></td>
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
          <td class="r">12.180,00 €</td>
          <td class="r"><b>12.180,00 €</b></td>
        </tr>
      </tbody>
    </table>

    <div class="totals-area">
      <div class="totals-box">
        <div class="t-row"><span>SUBTOTAL NETO (B.I.):</span><span>75.197,50 €</span></div>
        <div class="t-row"><span>I.V.A. (21%):</span><span>15.791,48 €</span></div>
        <div class="t-row"><span>TOTAL PRESUPUESTO:</span><span>90.988,98 €</span></div>
      </div>
    </div>

    <div class="conditions">
      <div class="cond-title">Condiciones de Contratación y Exclusiones:</div>
      <ul class="cond-list">
        <li><b>EXCLUSIÓN EXPRESA DE CIMENTACIÓN:</b> No se incluye la ejecución de zapatas de cimentación (necesarias) ni solera. Dichos trabajos serán contratados directamente por el cliente conforme a las directrices de replanteo que entregará DIXIS.</li>
        <li><b>Naturaleza de la oferta:</b> Presupuesto aproximado formulado sobre pre-cálculo estructural preliminar.</li>
        <li><b>Forma de pago:</b> 100% a la aceptación del presupuesto.</li>
        <li><b>Plazo de ejecución:</b> 3 meses a partir de la aceptación del presupuesto y confirmación técnica.</li>
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

    .alert-box {{
      background: #fef2f2;
      border: 1.5px solid #dc2626;
      border-radius: 4px;
      padding: 6px 10px;
      margin-bottom: 8px;
      font-size: 8px;
      color: #991b1b;
      line-height: 1.35;
    }}

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
  <!-- PÁGINA 1: PRE-CÁLCULO ESTRUCTURAL Y DESGLOSE DE ACERO -->
  <div class="sheet">
    <header>
      <div>
        <div class="header-title">PRESUPUESTO TÉCNICO INTERNO • P-2026-0050</div>
        <div class="header-sub">Proyecto: Marquesina Industrial Atornillable 16x8x8 m • Nautic KIM (Alaior)</div>
      </div>
      <div class="header-tag">DOCUMENTO TÉCNICO INTERNO</div>
    </header>

    <div class="alert-box">
      <b>NOTA TÉCNICA DE CIMENTACIÓN:</b> <b>No se incluye zapatas ni solera</b>. Al tratarse de pilares de 8 metros de altura con viento en Alaior (Zona C), el momento de vuelco en base requiere zapatas aisladas de hormigón armado con anclajes. La definición geométrica de cargas será entregada al contratista del cliente a partir de la Partida 01.
    </div>

    <div class="grid-3">
      <div class="box">
        <div class="box-title">Pre-cálculo Estimativo</div>
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
          <td><b>Cotizado a 5,00 €/kg = 32.355,00 €</b></td>
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
      <div class="header-tag">DOCUMENTO TÉCNICO INTERNO</div>
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
          <td>Pre-cálculo estructural CTE, modelado preliminar, planos de taller y despiece analítico</td>
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
            <tr><td>Coste Acero S275JR (6.471 kg)</td><td class="r">11.647,80 €</td><td class="r">15,5%</td></tr>
            <tr><td>Coste Panel Sándwich PUR 30 mm y Remates</td><td class="r">4.208,40 €</td><td class="r">5,6%</td></tr>
            <tr><td>Coste Pintura Epoxi + Poliuretano 2C HAM</td><td class="r">1.450,00 €</td><td class="r">1,9%</td></tr>
            <tr><td>Coste Tornillería 8.8 y Anclajes Hilti M20</td><td class="r">820,00 €</td><td class="r">1,1%</td></tr>
            <tr><td>Coste Mano de Obra Taller e Ingeniería (164 h)</td><td class="r">4.264,00 €</td><td class="r">5,7%</td></tr>
            <tr><td>Coste Mano de Obra Montaje Alaior (222 h)</td><td class="r">6.216,00 €</td><td class="r">8,3%</td></tr>
            <tr><td>Coste Medios Auxiliares y Transporte</td><td class="r">3.310,00 €</td><td class="r">4,4%</td></tr>
            <tr style="background: #e2e8f0; font-weight: 800;">
              <td><b>COSTE DIRECTO TOTAL (CD)</b></td>
              <td class="r"><b>31.916,20 €</b></td>
              <td class="r"><b>42,4%</b></td>
            </tr>
            <tr style="background: #dcfce7; font-weight: 800; color: #166534;">
              <td><b>MARGEN BRUTO COMERCIAL E INDUSTRIAL</b></td>
              <td class="r"><b>43.281,30 €</b></td>
              <td class="r"><b>57,6%</b></td>
            </tr>
            <tr style="background: #fef3c7; font-weight: 800; color: #92400e;">
              <td><b>PRECIO DE VENTA NETO (B.I.)</b></td>
              <td class="r"><b>75.197,50 €</b></td>
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
    client_html = create_html_client()
    client_pdf = os.path.join(BASE_DIR, "presupuesto-cliente.pdf")
    convert_to_pdf(client_html, client_pdf)
    
    tech_html = create_html_technical()
    tech_pdf = os.path.join(BASE_DIR, "presupuesto-interno-tecnico.pdf")
    convert_to_pdf(tech_html, tech_pdf)
    
    print("\nPDFs de presupuesto generados correctamente (sin inclusión de Excel para el cliente).")
