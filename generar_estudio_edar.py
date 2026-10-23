# -*- coding: utf-8 -*-
import os
import subprocess
import json
import base64
import tempfile
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

base_dir = r"c:\Users\pablo\Documents\Presupuestador"
folder_budget = os.path.join(base_dir, "presupuestos", "P-2026-0040-estudio-tecnico-barandilla-laguna-edar-es-castell")
os.makedirs(folder_budget, exist_ok=True)

html_path = os.path.join(base_dir, "Presupuesto_Estudio_Tecnico_EDAR_EsCastell.html")
pdf_path = os.path.join(base_dir, "Presupuesto_Estudio_Tecnico_EDAR_EsCastell.pdf")
xlsx_path = os.path.join(base_dir, "Presupuesto_Estudio_Tecnico_EDAR_EsCastell.xlsx")

html_dest = os.path.join(folder_budget, "presupuesto-final.html")
pdf_dest = os.path.join(folder_budget, "presupuesto.pdf")
xlsx_dest = os.path.join(folder_budget, "presupuesto.xlsx")
json_dest = os.path.join(folder_budget, "datos.json")
readme_dest = os.path.join(folder_budget, "README.md")

# Convertir imágenes a base64 para que el HTML y PDF sean 100% autónomos
def img_to_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

b64_op1 = img_to_b64(os.path.join(base_dir, "img", "fotomontaje_op1.jpg"))
b64_op2 = img_to_b64(os.path.join(base_dir, "img", "fotomontaje_op2.jpg"))
b64_op3 = img_to_b64(os.path.join(base_dir, "img", "fotomontaje_op3.jpg"))

# =========================================================================
# DATOS ECONÓMICOS OFICIALES DEFINIDOS (175 ML)
# =========================================================================
# OP 1: 175 €/ML  -> 30.625,00 € Base  -> 37.056,25 € Total con IVA
# OP 2: 245 €/ML  -> 42.875,00 € Base  -> 51.878,75 € Total con IVA
# OP 3: 265 €/ML  -> 46.375,00 € Base  -> 56.113,75 € Total con IVA

html_template = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>P-2026-0040 Estudio T&eacute;cnico y Presupuesto con Fotomontajes: Barandilla Laguna EDAR Es Castell / Mah&oacute;n (175 ML)</title>
  <style>
    @page {{ 
      size: A4; 
      margin: 10mm 12mm 12mm 12mm; 
    }}
    * {{ box-sizing: border-box; }}
    body {{ 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
      color: #0f172a; 
      margin: 0; 
      background: #f1f5f9; 
      line-height: 1.4; 
      -webkit-print-color-adjust: exact; 
      print-color-adjust: exact; 
      font-size: 10.5pt;
    }}
    .page-container {{
      max-width: 940px;
      margin: 20px auto;
      background: #ffffff;
      padding: 30px 36px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      border-radius: 4px;
    }}
    @media print {{
      body {{ background: #fff; }}
      .page-container {{ 
        max-width: 100%; 
        margin: 0; 
        padding: 0; 
        box-shadow: none; 
        border-radius: 0; 
      }}
      .no-print {{ display: none !important; }}
      .page-break {{ page-break-before: always; }}
    }}

    /* HEADER */
    header {{ 
      border-top: 5px solid #16202a; 
      padding-top: 14px; 
      display: grid; 
      grid-template-columns: minmax(0, 1fr) 230px; 
      gap: 16px; 
      align-items: start; 
      border-bottom: 2px solid #e2e8f0; 
      padding-bottom: 14px; 
    }}
    .company {{ display: flex; gap: 14px; align-items: flex-start; }}
    .company-logo {{ width: 135px; flex: 0 0 135px; }}
    .company-logo img {{ width: 100%; height: auto; display: block; }}
    .company-details h1 {{ 
      margin: 0 0 3px 0; 
      font-size: 18px; 
      font-weight: 800; 
      color: #16202a; 
      letter-spacing: -0.2px; 
    }}
    .company-details p {{ 
      margin: 2px 0; 
      color: #475569; 
      font-size: 10px; 
      line-height: 1.35; 
    }}
    .meta-box {{ 
      text-align: right; 
      display: flex; 
      flex-direction: column; 
      align-items: flex-end; 
    }}
    .meta-box .doc-type {{ 
      font-size: 12px; 
      font-weight: 700; 
      text-transform: uppercase; 
      letter-spacing: 0.5px; 
      color: #64748b; 
      margin-bottom: 3px; 
    }}
    .meta-box .ref-code {{ 
      display: inline-block; 
      padding: 5px 12px; 
      background: #16202a; 
      color: #ffffff; 
      font-weight: 800; 
      font-size: 13px; 
      border-radius: 4px; 
    }}
    .meta-box .meta-line {{ 
      margin: 3px 0 0; 
      color: #475569; 
      font-size: 10.5px; 
    }}

    /* HERO */
    .hero-banner {{ 
      margin: 16px 0 14px; 
      padding: 14px 18px; 
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
      border-left: 5px solid #16202a; 
      border-radius: 0 5px 5px 0; 
    }}
    .hero-banner h2 {{ 
      margin: 0 0 6px 0; 
      font-size: 18px; 
      color: #16202a; 
      font-weight: 700; 
      line-height: 1.25; 
    }}
    .hero-banner p {{ 
      margin: 0; 
      color: #334155; 
      font-size: 11px; 
      line-height: 1.45; 
    }}

    /* INFO CLIENTE */
    .client-card {{ 
      display: grid; 
      grid-template-columns: 1fr 1fr; 
      gap: 14px; 
      background: #f8fafc; 
      border: 1px solid #e2e8f0; 
      border-radius: 5px; 
      padding: 12px 16px; 
      margin-bottom: 18px; 
      font-size: 10.5px; 
    }}
    .client-card .col p {{ margin: 2px 0; }}
    .client-card strong {{ color: #1e293b; font-weight: 600; }}
    .badge-env {{
      display: inline-block;
      padding: 2px 6px;
      background: #fee2e2;
      color: #991b1b;
      font-weight: 700;
      border-radius: 3px;
      font-size: 9.5px;
    }}
    .badge-iso {{
      display: inline-block;
      padding: 2px 6px;
      background: #e0f2fe;
      color: #0369a1;
      font-weight: 700;
      border-radius: 3px;
      font-size: 9.5px;
    }}

    /* SECCIONES Y FOTOMONTAJES */
    .section-title {{ 
      font-size: 14px; 
      font-weight: 700; 
      color: #16202a; 
      margin: 22px 0 12px 0; 
      text-transform: uppercase; 
      letter-spacing: 0.3px; 
      border-bottom: 1.5px solid #e2e8f0; 
      padding-bottom: 5px; 
    }}

    /* GALERÍA DE FOTOMONTAJES COMPARATIVOS */
    .gallery-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 20px;
    }}
    .gallery-item {{
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      overflow: hidden;
      background: #ffffff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      display: flex;
      flex-direction: column;
    }}
    .gallery-item.recommended {{
      border: 2px solid #059669;
      box-shadow: 0 3px 12px rgba(5,150,105,0.15);
    }}
    .gallery-img {{
      width: 100%;
      height: 145px;
      object-fit: cover;
      display: block;
      border-bottom: 1px solid #e2e8f0;
    }}
    .gallery-body {{
      padding: 10px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .gallery-title {{
      font-size: 12px;
      font-weight: 700;
      color: #16202a;
      margin-bottom: 3px;
    }}
    .gallery-price {{
      font-size: 15px;
      font-weight: 800;
      color: #0f172a;
      margin: 4px 0;
    }}
    .gallery-price small {{
      font-size: 10px;
      color: #64748b;
      font-weight: 500;
    }}
    .gallery-badge {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 9px;
      font-weight: 700;
      text-transform: uppercase;
      margin-top: 4px;
    }}
    .badge-op1 {{ background: #fef2f2; color: #b91c1c; }}
    .badge-op2 {{ background: #f1f5f9; color: #334155; }}
    .badge-op3 {{ background: #dcfce7; color: #047857; }}

    /* IMAGEN EN CABECERA DE CADA CAPÍTULO */
    .chapter-img-box {{
      margin: 10px 0 12px 0;
      border-radius: 5px;
      overflow: hidden;
      border: 1px solid #cbd5e1;
      page-break-inside: avoid;
    }}
    .chapter-img {{
      width: 100%;
      height: 170px;
      object-fit: cover;
      display: block;
    }}
    .chapter-img-caption {{
      background: #f8fafc;
      padding: 6px 12px;
      font-size: 9.5px;
      color: #475569;
      border-top: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* TABLAS DE DESGLOSE */
    table.data-table {{ 
      width: 100%; 
      border-collapse: collapse; 
      margin-top: 6px; 
      margin-bottom: 16px; 
      table-layout: fixed; 
      font-size: 10px; 
    }}
    table.data-table th {{ 
      background: #16202a; 
      color: #ffffff; 
      text-align: left; 
      padding: 7px 6px; 
      font-weight: 600; 
      font-size: 9.5px; 
      text-transform: uppercase; 
    }}
    table.data-table td {{ 
      border-bottom: 1px solid #e2e8f0; 
      padding: 6px 6px; 
      vertical-align: top; 
      color: #1e293b; 
      line-height: 1.3; 
    }}
    table.data-table tbody tr:nth-child(even) {{ 
      background: #f8fafc; 
    }}
    .num {{ text-align: right; white-space: nowrap; }}
    .col-cap {{ width: 12%; font-weight: 600; color: #475569; }}
    .col-des {{ width: 49%; }}
    .col-can {{ width: 8%; }}
    .col-uni {{ width: 6%; }}
    .col-pre {{ width: 11%; }}
    .col-imp {{ width: 14%; font-weight: 600; }}
    
    .subtotal-row td {{ 
      background: #f1f5f9 !important; 
      font-weight: 700; 
      border-top: 1.5px solid #cbd5e1; 
      color: #0f172a; 
    }}
    .iva-row td {{ 
      background: #ffffff !important; 
      color: #475569; 
    }}
    .total-row td {{ 
      background: #16202a !important; 
      color: #ffffff !important; 
      font-size: 11.5px; 
      font-weight: 800; 
      padding: 8px 6px; 
    }}

    /* ESTUDIO TÉCNICO */
    .tech-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 14px 16px;
      margin: 12px 0 16px;
      font-size: 10.5px;
    }}
    .tech-box h4 {{
      margin: 0 0 6px;
      font-size: 12px;
      color: #16202a;
    }}
    .tech-box p {{
      margin: 0 0 8px;
      color: #334155;
      text-align: justify;
    }}
    .verdict-callout {{
      background: #ecfdf5;
      border-left: 4px solid #059669;
      padding: 10px 14px;
      border-radius: 0 5px 5px 0;
      margin: 10px 0;
      font-size: 10.5px;
    }}
    .verdict-callout strong {{
      color: #065f46;
      font-size: 11px;
    }}
    .warning-callout {{
      background: #fffbeb;
      border-left: 4px solid #f59e0b;
      padding: 10px 14px;
      border-radius: 0 5px 5px 0;
      margin: 10px 0;
      font-size: 10.5px;
    }}
    .warning-callout strong {{
      color: #92400e;
      font-size: 11px;
    }}

    /* CONDICIONES GENERALES */
    .conditions-list {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      font-size: 10px;
      color: #475569;
      margin-top: 8px;
    }}
    .cond-item {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 7px 10px;
      border-radius: 4px;
    }}
    .cond-item strong {{
      color: #1e293b;
      display: block;
      margin-bottom: 2px;
    }}

    /* FOOTER */
    footer {{ 
      margin-top: 24px; 
      padding-top: 12px; 
      border-top: 1px solid #cbd5e1; 
      text-align: center; 
      font-size: 9.5px; 
      color: #64748b; 
    }}

    /* BOTONES */
    .btn-bar {{
      margin-top: 20px;
      display: flex;
      gap: 10px;
      justify-content: flex-end;
    }}
    .btn {{
      padding: 8px 16px;
      font-size: 11px;
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
      border: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      text-decoration: none;
    }}
    .btn-secondary {{ background: #e2e8f0; color: #1e293b; }}
    .btn-secondary:hover {{ background: #cbd5e1; }}
  </style>
</head>
<body>

<div class="page-container">

  <!-- CABECERA HAM -->
  <header>
    <div class="company">
      <div class="company-logo">
        <img src="https://www.hamenorca.com/images/logo-hamenorca-dark.svg" alt="HAM Estructuras Met&aacute;licas" onerror="this.onerror=null; this.src='https://placehold.co/180x50/16202a/ffffff?text=HAM+MENORCA'">
      </div>
      <div class="company-details">
        <h1>HAM ESTRUCTURAS MET&Aacute;LICAS</h1>
        <p><strong>Ingenier&iacute;a, Fabricaci&oacute;n y Montaje Industrial en Menorca</strong></p>
        <p>Av. Circunvalaci&oacute;, 11 &middot; Pol&iacute;gono Industrial de Sant Llu&iacute;s &middot; 07710 Sant Llu&iacute;s (Menorca)</p>
        <p>Telf: +34 971 35 20 18 &middot; M&oacute;vil / WhatsApp: +34 669 769 541 &middot; info@hamenorca.com</p>
        <p>www.hamenorca.com</p>
      </div>
    </div>
    <div class="meta-box">
      <div class="doc-type">Estudio T&eacute;cnico &amp; Oferta</div>
      <div class="ref-code">P-2026-0040</div>
      <div class="meta-line"><strong>Fecha:</strong> 09 de Octubre de 2026</div>
      <div class="meta-line"><strong>Validez:</strong> 30 d&iacute;as naturales</div>
      <div class="meta-line"><strong>Revisi&oacute;n:</strong> 3.0 (Con Fotomontajes)</div>
    </div>
  </header>

  <!-- BANNER TÍTULO -->
  <div class="hero-banner">
    <h2>ESTUDIO T&Eacute;CNICO Y VALORACI&Oacute;N ECON&Oacute;MICA: CERRAMIENTO BARANDILLA LAGUNA EDAR (175 ML)</h2>
    <p>An&aacute;lisis comparativo y recreaci&oacute;n fotogr&aacute;fica fotorrealista para el cerramiento de protecci&oacute;n de la balsa de la <strong>Estaci&oacute;n Depuradora de Aguas Residuales (EDAR) de Es Castell / Mah&oacute;n (Menorca)</strong>. Conforme a norma <strong>UNE-EN ISO 14122-3</strong>, Ley 31/1995 de Prevenci&oacute;n de Riesgos Laborales y criterios de durabilidad C5-M.</p>
  </div>

  <!-- TARJETA CLIENTE -->
  <div class="client-card">
    <div class="col">
      <p><strong>Instalaci&oacute;n:</strong> EDAR Es Castell / Mah&oacute;n (Balsa de Lagunaje)</p>
      <p><strong>Ubicaci&oacute;n:</strong> T&eacute;rmino Municipal de Es Castell / Mah&oacute;n, Menorca</p>
      <p><strong>Medici&oacute;n Perimetral Total:</strong> <strong>175,00 Metros Lineales (ML)</strong></p>
      <p><strong>Uso / Destino:</strong> Protecci&oacute;n perimetral colectiva contra ca&iacute;das a l&aacute;mina de agua residual</p>
    </div>
    <div class="col">
      <p><strong>Clasificaci&oacute;n Ambiental:</strong> <span class="badge-env">C5-M Marino Severo + Gases Qu&iacute;micos EDAR (H2S, NH3)</span></p>
      <p><strong>Normativa de Seguridad:</strong> <span class="badge-iso">UNE-EN ISO 14122-3 / CTE DB-SUA</span></p>
      <p><strong>Soporte de Fijaci&oacute;n:</strong> Corona perimetral continua de hormig&oacute;n armado</p>
      <p><strong>Ingenier&iacute;a Responsable:</strong> HAM Oficina T&eacute;cnica &amp; Montajes</p>
    </div>
  </div>

  <!-- SECCIÓN 1: FOTOMONTAJES COMPARATIVOS -->
  <div class="section-title">
    <span>1. ESTUDIO VISUAL Y FOTOMONTAJES EN EDAR ES CASTELL</span>
  </div>

  <div style="background:#eff6ff; border-left:4px solid #3b82f6; padding:8px 12px; margin-bottom:12px; border-radius:0 4px 4px 0; font-size:10px; color:#1e40af;">
    <strong>Aviso técnico sobre infografía:</strong> Las tres imágenes y fotomontajes técnicos presentados en este estudio han sido <strong>creadas mediante Inteligencia Artificial (IA)</strong> como simulación fotorrealista de alta precisión para valorar visualmente el acabado estético y constructivo de cada alternativa sobre la coronación perimetral real de la laguna de la EDAR Es Castell / Mahón.
  </div>

  <div class="gallery-grid">
    <!-- FOTO 1 -->
    <div class="gallery-item">
      <img src="{b64_op1}" alt="Opción 1: Inox 316L + Cuerdas" class="gallery-img">
      <div class="gallery-body">
        <div>
          <div class="gallery-title">Opci&oacute;n #1: Inox 316L + Cuerdas</div>
          <div style="font-size:9.5px; color:#64748b;">Postes redondos AISI 316L con 2 l&iacute;neas de cabo n&aacute;utico y tensores. <em>(Simulaci&oacute;n por IA)</em></div>
        </div>
        <div>
          <div class="gallery-price">175,00 &euro; <small>/ ML</small></div>
          <div style="font-size:9.5px; color:#475569;">Total: 30.625,00 &euro; + IVA</div>
          <span class="gallery-badge badge-op1">&#10060; No Cumple UNE 14122</span>
        </div>
      </div>
    </div>

    <!-- FOTO 2 -->
    <div class="gallery-item">
      <img src="{b64_op2}" alt="Opción 2: Inox 316L Modular" class="gallery-img">
      <div class="gallery-body">
        <div>
          <div class="gallery-title">Opci&oacute;n #2: Inox 316L Modular (40x40x1.5)</div>
          <div style="font-size:9.5px; color:#64748b;">Tubo 40x40x1.5mm en montantes y travesa&ntilde;os, orejas con tornillo M12. <em>(Simulaci&oacute;n por IA)</em></div>
        </div>
        <div>
          <div class="gallery-price">245,00 &euro; <small>/ ML</small></div>
          <div style="font-size:9.5px; color:#475569;">Total: 42.875,00 &euro; + IVA</div>
          <span class="gallery-badge badge-op2">&#9989; Conforme Estructural</span>
        </div>
      </div>
    </div>

    <!-- FOTO 3 -->
    <div class="gallery-item recommended">
      <img src="{b64_op3}" alt="Opción 3: Barandilla PRFV Articulada" class="gallery-img">
      <div class="gallery-body">
        <div>
          <div class="gallery-title" style="color:#065f46;">Opci&oacute;n #3: PRFV Articulada &#11088;</div>
          <div style="font-size:9.5px; color:#64748b;">Tubo 50x50, pasamano Omega, z&oacute;calo 200 mm y r&oacute;tulas POM orientables. <em>(Simulaci&oacute;n por IA)</em></div>
        </div>
        <div>
          <div class="gallery-price" style="color:#059669;">265,00 &euro; <small>/ ML</small></div>
          <div style="font-size:9.5px; color:#047857;">Total: 46.375,00 &euro; + IVA</div>
          <span class="gallery-badge badge-op3">&#9989; Conforme 100% (Rodapi&eacute;)</span>
        </div>
      </div>
    </div>
  </div>

  <!-- TABLA COMPARATIVA DIRECTA -->
  <table class="data-table">
    <thead>
      <tr>
        <th style="width:25%;">Criterio T&eacute;cnico / Operativo</th>
        <th style="width:25%;">Opci&oacute;n #1: Inox 316L + Cuerdas</th>
        <th style="width:25%;">Opci&oacute;n #2: Inox 316L Tubo 40x40x1.5</th>
        <th style="width:25%;">Opci&oacute;n #3: Barandilla PRFV Articulada</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Material Principal</strong></td>
        <td>AISI 316L + Cuerda t&eacute;xtil n&aacute;utica</td>
        <td>Acero Inox AISI 316L (Tubo 40x40x1.5 mm integral)</td>
        <td>PRFV Pultruido + Accesorios POM</td>
      </tr>
      <tr>
        <td><strong>Separaci&oacute;n entre Montantes</strong></td>
        <td>2,00 - 2,50 m</td>
        <td>1,50 m (seg&uacute;n dise&ntilde;o)</td>
        <td>1,10 m (seg&uacute;n ficha t&eacute;cnica)</td>
      </tr>
      <tr>
        <td><strong>Cumplimiento UNE-EN ISO 14122-3</strong></td>
        <td><span style="color:#dc2626; font-weight:700;">No Cumple</span> (deformable, sin rodapi&eacute;)</td>
        <td><span style="color:#d97706; font-weight:700;">Cumple Estructural</span> (sin rodapi&eacute;)</td>
        <td><span style="color:#16a34a; font-weight:700;">Cumplimiento Total</span> (con rodapi&eacute; 200mm)</td>
      </tr>
      <tr>
        <td><strong>Resistencia a Corrosi&oacute;n EDAR (H2S, NH3)</strong></td>
        <td>Media (cuerda sufre degradaci&oacute;n UV/biol.)</td>
        <td>Excelente (AISI 316L resiste cloruros)</td>
        <td><strong>Inmune Absoluta</strong> (no met&aacute;lica)</td>
      </tr>
      <tr>
        <td><strong>Rodapi&eacute; / Z&oacute;calo de Protecci&oacute;n</strong></td>
        <td>No existente</td>
        <td>No previsto en dise&ntilde;o base</td>
        <td><strong>Pletina nerviada PRFV 200x3.5 mm</strong></td>
      </tr>
      <tr>
        <td><strong>Precio Unitario / Metro Lineal</strong></td>
        <td><strong>175,00 &euro; / ML</strong></td>
        <td><strong>245,00 &euro; / ML</strong></td>
        <td><strong>265,00 &euro; / ML</strong></td>
      </tr>
      <tr style="background:#f1f5f9; font-weight:700;">
        <td><strong>BASE IMPONIBLE (175 ML)</strong></td>
        <td style="color:#1e293b;">30.625,00 &euro;</td>
        <td style="color:#1e293b;">42.875,00 &euro;</td>
        <td style="color:#059669; font-size:11px;">46.375,00 &euro;</td>
      </tr>
      <tr style="background:#ffffff;">
        <td><strong>IVA (21%)</strong></td>
        <td>6.431,25 &euro;</td>
        <td>9.003,75 &euro;</td>
        <td>9.738,75 &euro;</td>
      </tr>
      <tr style="background:#16202a; color:#fff; font-weight:800;">
        <td style="color:#fff;"><strong>TOTAL PRESUPUESTO CON IVA</strong></td>
        <td style="color:#fff;">37.056,25 &euro;</td>
        <td style="color:#fff;">51.878,75 &euro;</td>
        <td style="color:#a7f3d0;">56.113,75 &euro;</td>
      </tr>
    </tbody>
  </table>

  <!-- SALTO DE PÁGINA PARA DESGLOSES ECONÓMICOS -->
  <div class="page-break"></div>

  <!-- SECCIÓN 2: DESGLOSE ECONÓMICO DETALLADO -->
  <div class="section-title">
    <span>2. VALORACI&Oacute;N ECON&Oacute;MICA DETALLADA POR PARTIDAS (MEDICI&Oacute;N: 175 ML)</span>
  </div>

  <!-- DESGLOSE OPCIÓN 1 -->
  <h4 style="margin:14px 0 5px; color:#16202a; font-size:12px;">OPCI&Oacute;N #1: VERTICALES DE INOX 316L Y CUERDA DE PASAMANOS Y DIVISI&Oacute;N HORIZONTAL (175,00 &euro; / ML)</h4>
  <div class="chapter-img-box">
    <img src="{b64_op1}" alt="Fotomontaje Opción 1" class="chapter-img">
    <div class="chapter-img-caption">
      <span><strong>Fotomontaje Opci&oacute;n #1:</strong> Montantes cil&iacute;ndricos de Inox AISI 316L y doble l&iacute;nea de cabo n&aacute;utico marino tensado. <em>(Recreaci&oacute;n fotogr&aacute;fica generada por Inteligencia Artificial)</em></span>
      <span style="font-weight:700; color:#16202a;">175,00 &euro; / ML</span>
    </div>
  </div>
  <table class="data-table">
    <thead>
      <tr>
        <th class="col-cap">Cap&iacute;tulo</th>
        <th class="col-des">Concepto y Especificaciones T&eacute;cnicas</th>
        <th class="col-can num">Cant.</th>
        <th class="col-uni">Ud.</th>
        <th class="col-pre num">Precio (&euro;)</th>
        <th class="col-imp num">Importe (&euro;)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="col-cap">Materiales</td>
        <td><strong>Montantes verticales en Acero Inoxidable AISI 316L</strong><br>Montantes de tubo 40x40x2 mm en inox AISI 316L h=1.100 mm con placa base 120x120x6 mm soldada con TIG y cartelas, equipados con 2 c&aacute;ncamos pasantes soldados en AISI 316L. Separaci&oacute;n aprox. 2,00 m (88 uds para 175 ML).</td>
        <td class="num">88</td>
        <td>ud</td>
        <td class="num">145,00</td>
        <td class="num">12.760,00</td>
      </tr>
      <tr>
        <td class="col-cap">Materiales</td>
        <td><strong>Cuerda pasamanos y divisi&oacute;n horizontal + herrajes AISI 316</strong><br>Suministro de cuerda n&aacute;utica (2 pasadas x 175 ML = 350 ML), incluyendo 16 tensores n&aacute;uticos tipo botella M10 en acero inoxidable AISI 316, terminales prensados, guardacabos y grilletes de fijaci&oacute;n en extremos y quiebros.</td>
        <td class="num">1</td>
        <td>lote</td>
        <td class="num">1.250,00</td>
        <td class="num">1.250,00</td>
      </tr>
      <tr>
        <td class="col-cap">Fijaciones</td>
        <td><strong>Anclajes estructurales en Acero Inox A4 a corona de hormig&oacute;n</strong><br>352 anclajes qu&iacute;micos formados por varilla roscada M10 en acero inoxidable A4 (AISI 316) con resina de inyecci&oacute;n vinil&eacute;ster de alta resistencia para exterior agresivo y tuercas autoblocantes.</td>
        <td class="num">88</td>
        <td>ud</td>
        <td class="num">12,00</td>
        <td class="num">1.056,00</td>
      </tr>
      <tr>
        <td class="col-cap">Taller HAM</td>
        <td><strong>Mano de obra de calderer&iacute;a y fabricaci&oacute;n en taller</strong><br>Corte de perfiles, soldadura TIG bajo gas Arg&oacute;n puro con aportaci&oacute;n 316L, repasado y decapado/pasivado qu&iacute;mico de cordones de soldadura.</td>
        <td class="num">60</td>
        <td>h</td>
        <td class="num">40,00</td>
        <td class="num">2.400,00</td>
      </tr>
      <tr>
        <td class="col-cap">Montaje Obra</td>
        <td><strong>Mano de obra de replanteo, fijaci&oacute;n y tesado en EDAR Es Castell</strong><br>Instalaci&oacute;n en obra por equipo especialista HAM: replanteo perimetral, perforaci&oacute;n de 352 taladros, inyecci&oacute;n qu&iacute;mica, colocaci&oacute;n de montantes a nivel y aplomado, enhebrado de cuerdas y tesado con dinam&oacute;metro.</td>
        <td class="num">175</td>
        <td>ML</td>
        <td class="num">68,00</td>
        <td class="num">11.900,00</td>
      </tr>
      <tr>
        <td class="col-cap">Log&iacute;stica/Seg.</td>
        <td><strong>Transporte en Menorca, medios auxiliares y EPIs de seguridad</strong><br>Portes de material desde taller Sant Llu&iacute;s a EDAR Es Castell, generador el&eacute;ctrico, equipos de perforaci&oacute;n SDS y EPIs antica&iacute;da al borde de balsa de agua residual.</td>
        <td class="num">1</td>
        <td>lote</td>
        <td class="num">1.259,00</td>
        <td class="num">1.259,00</td>
      </tr>
      <tr class="subtotal-row">
        <td colspan="5" style="text-align:right;">BASE IMPONIBLE (OPCI&Oacute;N #1 - 175,00 &euro;/ML):</td>
        <td class="num">30.625,00 &euro;</td>
      </tr>
      <tr class="iva-row">
        <td colspan="5" style="text-align:right;">IVA (21%):</td>
        <td class="num">6.431,25 &euro;</td>
      </tr>
      <tr class="total-row">
        <td colspan="5" style="text-align:right;">TOTAL PRESUPUESTO OPCI&Oacute;N #1:</td>
        <td class="num">37.056,25 &euro;</td>
      </tr>
    </tbody>
  </table>

  <!-- SALTO DE PÁGINA PARA OPCIÓN 2 -->
  <div class="page-break"></div>

  <!-- DESGLOSE OPCIÓN 2 -->
  <h4 style="margin:14px 0 5px; color:#16202a; font-size:12px;">OPCI&Oacute;N #2: BARANDILLA MODULAR DE ACERO INOXIDABLE AISI 316L (TUBO 40x40x1.5) - (245,00 &euro; / ML)</h4>
  <div class="chapter-img-box">
    <img src="{b64_op2}" alt="Fotomontaje Opción 2" class="chapter-img">
    <div class="chapter-img-caption">
      <span><strong>Fotomontaje Opci&oacute;n #2:</strong> Estructura modular Inox AISI 316L (tubo cuadrado 40x40x1.5 mm integral en montantes y travesa&ntilde;os) con pletinas de oreja y tornillos pasantes M12 (tramos entre postes, sin pasamanos continuo corrido). <em>(Recreaci&oacute;n fotogr&aacute;fica generada por Inteligencia Artificial)</em></span>
      <span style="font-weight:700; color:#16202a;">245,00 &euro; / ML</span>
    </div>
  </div>
  <table class="data-table">
    <thead>
      <tr>
        <th class="col-cap">Cap&iacute;tulo</th>
        <th class="col-des">Concepto y Especificaciones T&eacute;cnicas</th>
        <th class="col-can num">Cant.</th>
        <th class="col-uni">Ud.</th>
        <th class="col-pre num">Precio (&euro;)</th>
        <th class="col-imp num">Importe (&euro;)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="col-cap">Materiales</td>
        <td><strong>Montantes verticales en Tubo Cuadrado Inox AISI 316L 40x40x1.5 mm con orejas</strong><br>118 montantes de tubo cuadrado 40x40x1.5 mm en inox AISI 316L h=1.100 mm con placa base 120x120x6 mm, tap&oacute;n plano de coronaci&oacute;n soldado y pletinas de oreja soldadas tanto en coronaci&oacute;n como a media altura con taladro pasante para tornillo M12. Separaci&oacute;n cada 1,50 m.</td>
        <td class="num">118</td>
        <td>ud</td>
        <td class="num">125,00</td>
        <td class="num">14.750,00</td>
      </tr>
      <tr>
        <td class="col-cap">Materiales</td>
        <td><strong>Pasamanos modular en tramos de 1,5m Tubo Cuadrado Inox AISI 316L 40x40x1.5 mm</strong><br>Perfiles de pasamanos en tubo cuadrado 40x40x1.5 mm de acero inoxidable AISI 316L cortados en tramos de 1,5 m entre montantes (sin pasamanos corrido continuo), con perforaciones en extremos para fijaci&oacute;n a las pletinas de oreja mediante torniller&iacute;a pasante M12.</td>
        <td class="num">175</td>
        <td>ML</td>
        <td class="num">42,00</td>
        <td class="num">7.350,00</td>
      </tr>
      <tr>
        <td class="col-cap">Materiales</td>
        <td><strong>Barra intermedia modular en Tubo Cuadrado Inox AISI 316L 40x40x1.5 mm</strong><br>Tubo cuadrado de acero inoxidable AISI 316L 40x40x1.5 mm a media altura (h=550 mm) cortado en tramos de 1,5 m con perforaciones en extremos, fijado id&eacute;nticamente a la pletina de oreja intermedia mediante tornillo pasante M12.</td>
        <td class="num">175</td>
        <td>ML</td>
        <td class="num">28,00</td>
        <td class="num">4.900,00</td>
      </tr>
      <tr>
        <td class="col-cap">Torniller&iacute;a/Ancl.</td>
        <td><strong>Torniller&iacute;a pasante M12 inox A4 y fijaciones qu&iacute;micas de alto rendimiento</strong><br>Torniller&iacute;a pasante M12 con arandelas anchas y tuercas autoblocantes en calidad A4-70 (AISI 316) para sujeci&oacute;n de tramos superior e intermedio a pletinas, y 472 anclajes qu&iacute;micos M10x130 mm en acero inoxidable A4 con resina pura vinil&eacute;ster.</td>
        <td class="num">1</td>
        <td>lote</td>
        <td class="num">1.950,00</td>
        <td class="num">1.950,00</td>
      </tr>
      <tr>
        <td class="col-cap">Taller HAM</td>
        <td><strong>Mano de obra de calderer&iacute;a, corte, mecanizado y pasivado TIG</strong><br>Corte de perfiles, mecanizado de perforaciones en extremos, armado de montantes con orejas, soldadura TIG y decapado/pasivado qu&iacute;mico de cordones.</td>
        <td class="num">100</td>
        <td>h</td>
        <td class="num">40,00</td>
        <td class="num">4.000,00</td>
      </tr>
      <tr>
        <td class="col-cap">Montaje Obra</td>
        <td><strong>Instalaci&oacute;n, anclaje y ensamblaje atornillado en EDAR Es Castell</strong><br>Equipo de montaje especializado HAM en obra: replanteo perimetral (175 m), perforaci&oacute;n de 472 orificios en corona de hormig&oacute;n, colocaci&oacute;n qu&iacute;mica de montantes a nivel y aplomado, y montaje atornillado de pasamanos e intermedios.</td>
        <td class="num">175</td>
        <td>ML</td>
        <td class="num">50,00</td>
        <td class="num">8.750,00</td>
      </tr>
      <tr>
        <td class="col-cap">Log&iacute;stica/Seg.</td>
        <td><strong>Transporte protegido, medios de elevaci&oacute;n y seguridad perimetral</strong><br>Transporte de perfiles protegidos a obra, furg&oacute;n taller m&oacute;vil, grupos electr&oacute;genos y medios de prevenci&oacute;n espec&iacute;ficos para trabajo sobre borde de agua.</td>
        <td class="num">1</td>
        <td>lote</td>
        <td class="num">1.175,00</td>
        <td class="num">1.175,00</td>
      </tr>
      <tr class="subtotal-row">
        <td colspan="5" style="text-align:right;">BASE IMPONIBLE (OPCI&Oacute;N #2 - 245,00 &euro;/ML):</td>
        <td class="num">42.875,00 &euro;</td>
      </tr>
      <tr class="iva-row">
        <td colspan="5" style="text-align:right;">IVA (21%):</td>
        <td class="num">9.003,75 &euro;</td>
      </tr>
      <tr class="total-row">
        <td colspan="5" style="text-align:right;">TOTAL PRESUPUESTO OPCI&Oacute;N #2:</td>
        <td class="num">51.878,75 &euro;</td>
      </tr>
    </tbody>
  </table>

  <!-- SALTO DE PÁGINA PARA OPCIÓN 3 Y ESTUDIO TÉCNICO -->
  <div class="page-break"></div>

  <!-- DESGLOSE OPCIÓN 3 -->
  <h4 style="margin:14px 0 5px; color:#059669; font-size:12.5px;">OPCI&Oacute;N #3: BARANDILLA ARTICULADA DE PRFV SEG&Uacute;N FICHA T&Eacute;CNICA OFICIAL (265,00 &euro; / ML) &#11088;</h4>
  <div class="chapter-img-box" style="border-color:#059669;">
    <img src="{b64_op3}" alt="Fotomontaje Opción 3" class="chapter-img">
    <div class="chapter-img-caption" style="background:#f0fdf4;">
      <span><strong>Fotomontaje Opci&oacute;n #3:</strong> Sistema modular articulado de PRFV con pasamanos Omega, r&oacute;tulas POM y rodapi&eacute; continuo de 200 mm. <em>(Recreaci&oacute;n fotogr&aacute;fica generada por Inteligencia Artificial)</em></span>
      <span style="font-weight:700; color:#059669;">265,00 &euro; / ML</span>
    </div>
  </div>
  <table class="data-table">
    <thead>
      <tr>
        <th class="col-cap">Cap&iacute;tulo</th>
        <th class="col-des">Concepto y Especificaciones T&eacute;cnicas (Seg&uacute;n Ficha T&eacute;cnica PRFV)</th>
        <th class="col-can num">Cant.</th>
        <th class="col-uni">Ud.</th>
        <th class="col-pre num">Precio (&euro;)</th>
        <th class="col-imp num">Importe (&euro;)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="col-cap" style="color:#059669;">Material PRFV</td>
        <td><strong>Suministro de Barandilla Modular Articulada en PRFV (175 ML)</strong><br>Sistema fabricado en Poli&eacute;ster Reforzado con Fibra de Vidrio (proceso pultruido), color Gris RAL 7047, h=1.100 mm, montantes cada 1.100 mm, compuesto por:<br>
        &bull; <strong>Montantes verticales:</strong> Tubo cuadrado de PRFV 50x50x5 mm.<br>
        &bull; <strong>Pasamanos:</strong> Perfil ergon&oacute;mico de PRFV dise&ntilde;o Omega E-2100.<br>
        &bull; <strong>Perfil intermedio:</strong> Tubo cil&iacute;ndrico de PRFV &Oslash;25x3.5 mm.<br>
        &bull; <strong>Z&oacute;calo / Rodapi&eacute; de seguridad:</strong> Pletina nerviada de PRFV 200x3.5 mm.<br>
        &bull; <strong>Accesorios articulados en P.O.M.:</strong> R&oacute;tulas horizontales Omega y codos orientables &Oslash;25 mm.<br>
        &bull; <strong>Bases de suelo:</strong> Pies de fijaci&oacute;n para montante cuadrado.<br>
        &bull; <strong>Torniller&iacute;a del conjunto:</strong> Acero Inoxidable A-4 (AISI 316).<br>
        <em>(Partida completa de suministro de perfiles, accesorios, embalaje y flete mar&iacute;timo a Menorca).</em></td>
        <td class="num">175</td>
        <td>ML</td>
        <td class="num">145,00</td>
        <td class="num">25.375,00</td>
      </tr>
      <tr>
        <td class="col-cap">Fijaciones A4</td>
        <td><strong>Anclajes estructurales de suelo en Acero Inoxidable A-4</strong><br>Juego de anclajes expansivos / qu&iacute;micos de alta resistencia en Acero Inoxidable calidad A4 (AISI 316) para fijaci&oacute;n de las 160 bases de suelo a la corona de hormig&oacute;n de la laguna (aprox. 480 fijaciones A4 certificadas).</td>
        <td class="num">160</td>
        <td>ud</td>
        <td class="num">12,50</td>
        <td class="num">2.000,00</td>
      </tr>
      <tr>
        <td class="col-cap">Mano de Obra</td>
        <td><strong>Mano de obra oficial montador especialista en obra (80 horas)</strong><br>Replanteo perimetral y trazado de curvas en la corona de hormig&oacute;n, perforaci&oacute;n de orificios con martillo percutor SDS y aspiraci&oacute;n de polvo, nivelaci&oacute;n microm&eacute;trica de bases, embutido de montantes 50x50x5 mm, alineaci&oacute;n y montaje de pasamanos Omega, perfil intermedio &Oslash;25 mm y rodapi&eacute; de 200 mm.</td>
        <td class="num">80</td>
        <td>h</td>
        <td class="num">55,00</td>
        <td class="num">4.400,00</td>
      </tr>
      <tr>
        <td class="col-cap">Mano de Obra</td>
        <td><strong>Mano de obra ayudante especialista de montaje (80 horas)</strong><br>Asistencia continua en manipulaci&oacute;n de perfiles, acopio selectivo de accesorios POM, apoyo en taladrado, colocaci&oacute;n de remaches/tornillos A4 de z&oacute;calo rodapi&eacute; y apriete de seguridad.</td>
        <td class="num">80</td>
        <td>h</td>
        <td class="num">45,00</td>
        <td class="num">3.600,00</td>
      </tr>
      <tr>
        <td class="col-cap">Montaje Especial.</td>
        <td><strong>Alineaci&oacute;n perimetral, ensamblaje de rodapi&eacute; y remates continuos</strong><br>Ajuste de dilataci&oacute;n, montaje milim&eacute;trico de las r&oacute;tulas orientables en quiebros de la corona de la balsa y sellados t&eacute;cnicos de estanqueidad.</td>
        <td class="num">175</td>
        <td>ML</td>
        <td class="num">48,00</td>
        <td class="num">8.400,00</td>
      </tr>
      <tr>
        <td class="col-cap">Medios/Seg.</td>
        <td><strong>Medios auxiliares, herramientas a bater&iacute;a y EPIs de seguridad</strong><br>Desplazamientos continuos de furg&oacute;n taller durante 10 jornadas de trabajo, consumibles de perforaci&oacute;n, aspiraci&oacute;n industrial, l&iacute;nea de vida provisional y EPIs espec&iacute;ficos para planta EDAR (riesgo biol&oacute;gico y ca&iacute;da a distinto nivel).</td>
        <td class="num">1</td>
        <td>lote</td>
        <td class="num">2.600,00</td>
        <td class="num">2.600,00</td>
      </tr>
      <tr class="subtotal-row" style="background:#e2e8f0 !important;">
        <td colspan="5" style="text-align:right;">BASE IMPONIBLE TOTAL (OPCI&Oacute;N #3 - 265,00 &euro;/ML):</td>
        <td class="num">46.375,00 &euro;</td>
      </tr>
      <tr class="iva-row">
        <td colspan="5" style="text-align:right;">IVA (21%):</td>
        <td class="num">9.738,75 &euro;</td>
      </tr>
      <tr class="total-row" style="background:#065f46 !important;">
        <td colspan="5" style="text-align:right;">TOTAL PRESUPUESTO OPCI&Oacute;N #3 (LLAVE EN MANO):</td>
        <td class="num">56.113,75 &euro;</td>
      </tr>
    </tbody>
  </table>

  <!-- SECCIÓN 3: ESTUDIO TÉCNICO Y DICTAMEN DE INGENIERÍA -->
  <div class="section-title">
    <span>3. DICTAMEN T&Eacute;CNICO Y EVALUACI&Oacute;N DE INGENIER&Iacute;A HAM</span>
  </div>

  <div class="tech-box">
    <h4>1. An&aacute;lisis del Entorno Agresivo en EDAR de Menorca (Es Castell / Mah&oacute;n)</h4>
    <p>El per&iacute;metro de una laguna o balsa de aguas residuales en una EDAR costera como la de Es Castell/Mah&oacute;n combina dos de los vectores de corrosi&oacute;n m&aacute;s agresivos que existen en la ingenier&iacute;a civil:
    <br>1) <strong>Agresi&oacute;n Qu&iacute;mica:</strong> Desprendimiento continuo de &Aacute;cido Sulfh&iacute;drico (H2S), que en contacto con la humedad ambiental se convierte en &aacute;cido sulf&uacute;rico (H2SO4), atacando metales est&aacute;ndar y provocando fragilizaci&oacute;n.
    <br>2) <strong>Ambiente Marino C5-M:</strong> Vientos salinos dominantes y atm&oacute;sfera saturada de cloruros propia de la costa menorquina, propensa a generar corrosi&oacute;n por picadura (pitting) en aceros inoxidables.</p>

    <div class="warning-callout">
      <strong>&#9888; Desaconsejamiento T&eacute;cnico de la Opci&oacute;n #1 (Inox + Cuerdas - 175,00 &euro;/ML):</strong>
      <br>Aunque es la configuraci&oacute;n actual existente, la utilizaci&oacute;n de cuerdas textiles como elemento de contenci&oacute;n en lagunas de depuradoras <strong>incumple la norma UNE-EN ISO 14122-3</strong>. La cuerda presenta una deformabilidad excesiva ante el tropiezo o ca&iacute;da accidental de un operario, carece de rodapi&eacute; (facilitando que resbalen herramientas o personas al agua) y sufre una r&aacute;pida p&eacute;rdida de tensi&oacute;n y degradaci&oacute;n qu&iacute;mica debida a la intensa radiaci&oacute;n UV de Menorca.
    </div>

    <div class="verdict-callout">
      <strong>&#11088; Dictamen y Recomendaci&oacute;n de HAM: Opci&oacute;n #3 (Barandilla de PRFV Articulada - 265,00 &euro;/ML)</strong>
      <br>La barandilla de PRFV seg&uacute;n la ficha t&eacute;cnica aportada constituye la <strong>soluci&oacute;n t&eacute;cnica definitiva para una EDAR</strong>:
      <br>&bull; <strong>Cero Corrosi&oacute;n y Cero Mantenimiento:</strong> Al ser un material no met&aacute;lico a base de resinas termoestables y fibra de vidrio, es 100% inmune al H2S, al agua salina, a la humedad y a los rayos UV. No requiere pintura, pasivado ni repasos en toda su vida &uacute;til (&gt;30 a&ntilde;os).
      <br>&bull; <strong>Cumplimiento Normativo Integral:</strong> Altura normalizada de 1.100 mm, distancia entre montantes reducida a 1.100 mm y <strong>z&oacute;calo rodapi&eacute; de 200x3.5 mm incluido</strong> de origen, impidiendo la ca&iacute;da de objetos al agua residual.
      <br>&bull; <strong>Adaptabilidad &Oacute;ptima por R&oacute;tulas POM:</strong> Sus piezas articuladas de polioximetileno permiten copiar con perfecta continuidad las formas curvas o poligonales de la corona de la laguna sin necesidad de cortes complejos ni soldaduras.
      <br>&bull; <strong>Seguridad El&eacute;ctrica:</strong> Es un material completamente aislante frente a la electricidad est&aacute;tica y derivaciones de maquinaria de bombeo.
    </div>
  </div>

  <!-- CONDICIONES GENERALES Y OPERATIVAS -->
  <div class="section-title">
    <span>4. CONDICIONES COMERCIALES Y EJECUCI&Oacute;N</span>
  </div>

  <div class="conditions-list">
    <div class="cond-item">
      <strong>Plazo de Fabricaci&oacute;n y Suministro:</strong>
      Aprox. 15-20 d&iacute;as laborables para suministro de materiales desde confirmaci&oacute;n formal del pedido.
    </div>
    <div class="cond-item">
      <strong>Plazo de Montaje en Obra:</strong>
      8-10 jornadas laborables completas con cuadrilla de 2 montadores especialistas HAM.
    </div>
    <div class="cond-item">
      <strong>Garant&iacute;a Estructural y Anticorrosi&oacute;n:</strong>
      Opci&oacute;n Inox 316L: 5 a&ntilde;os. Opci&oacute;n PRFV: 10 a&ntilde;os frente a corrosi&oacute;n qu&iacute;mica y atmosf&eacute;rica.
    </div>
    <div class="cond-item">
      <strong>Forma de Pago Est&aacute;ndar:</strong>
      40% al encargo y acopio de materiales &middot; 60% a la finalizaci&oacute;n de los trabajos y recepci&oacute;n en obra.
    </div>
  </div>

  <!-- BOTONES ACCIÓN (NO PRINT) -->
  <div class="btn-bar no-print">
    <button class="btn btn-secondary" onclick="window.print()">&#128424; Imprimir / Guardar en PDF</button>
  </div>

  <!-- PIE DE PÁGINA -->
  <footer>
    HAM ESTRUCTURAS MET&Aacute;LICAS &middot; Soluciones Integrales de Calderer&iacute;a, Estructuras y Cerramientos Industriales &middot; Menorca<br>
    Documento t&eacute;cnico generado para EDAR Es Castell / Mah&oacute;n. Ref: P-2026-0040.
  </footer>

</div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

with open(html_dest, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"HTML con fotomontajes guardado con éxito:\n - {html_path}\n - {html_dest}")

# GENERACIÓN DEL PDF
browser_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
]

browser_exe = None
for bp in browser_paths:
    if os.path.exists(bp):
        browser_exe = bp
        break

if browser_exe:
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
        except Exception:
            pass

    temp_profile = tempfile.mkdtemp()
    res = subprocess.run([
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={temp_profile}",
        f"--print-to-pdf={pdf_path}",
        html_path
    ], capture_output=True, text=True)

    if res.returncode == 0 and os.path.exists(pdf_path):
        print(f"PDF con fotomontajes generado correctamente en: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
        with open(pdf_path, "rb") as fr, open(pdf_dest, "wb") as fw:
            fw.write(fr.read())
    else:
        print(f"Error generando PDF: {res.stderr}")
else:
    print("Navegador no localizado para generar PDF.")

# ACTUALIZACIÓN DE EXCEL CON NOTA DE FOTOMONTAJES
wb = openpyxl.Workbook()

font_title = Font(name="Segoe UI", size=14, bold=True, color="16202A")
font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="475569")
font_th = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
font_td = Font(name="Segoe UI", size=9, color="0F172A")
font_td_bold = Font(name="Segoe UI", size=9, bold=True, color="0F172A")
font_total = Font(name="Segoe UI", size=10, bold=True, color="16202A")

fill_navy = PatternFill(start_color="16202A", end_color="16202A", fill_type="solid")
fill_green_hdr = PatternFill(start_color="065F46", end_color="065F46", fill_type="solid")
fill_accent_green = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")

thin_border_side = Side(border_style="thin", color="CBD5E1")
thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

ws_sum = wb.active
ws_sum.title = "Resumen Comparativo"
ws_sum.views.sheetView[0].showGridLines = True

ws_sum.merge_cells("A1:G1")
ws_sum["A1"] = "HAM ESTRUCTURAS METÁLICAS — ESTUDIO TÉCNICO Y PRESUPUESTO"
ws_sum["A1"].font = font_title
ws_sum["A1"].alignment = Alignment(vertical="center")

ws_sum.merge_cells("A2:G2")
ws_sum["A2"] = "Cerramiento perimetral de Laguna en EDAR Es Castell / Mahón (Menorca) · Longitud: 175 ML · Ref: P-2026-0040 (Incluye Fotomontajes)"
ws_sum["A2"].font = font_subtitle

headers_summary = ["Opción", "Descripción Constructiva", "Material Principal", "Norma UNE 14122", "PVP / ML (€)", "Base Imponible (€)", "Total con IVA (21%)"]
for col_num, h in enumerate(headers_summary, 1):
    cell = ws_sum.cell(row=4, column=col_num)
    cell.value = h
    cell.font = font_th
    cell.fill = fill_navy
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data_summary = [
    ("Opción #1", "Verticales de Inox 316L + 2 líneas de Cuerda náutica pasamanos/intermedia", "AISI 316L + Textil UV", "❌ No cumple", 175.00, 30625.00, 37056.25),
    ("Opción #2", "Barandilla modular Inox AISI 316L (tubo 40x40x1.5mm en montantes y travesaños, orejas y tornillo pasante M12)", "AISI 316L 40x40x1.5", "✅ Conforme", 245.00, 42875.00, 51878.75),
    ("Opción #3 (⭐)", "Barandilla articulada PRFV pultruido: tubo 50x50, pasamano Omega, zócalo 200mm, POM", "PRFV + Resinas POM", "✅ Cumple 100%", 265.00, 46375.00, 56113.75)
]

for r_idx, row in enumerate(data_summary, 5):
    is_rec = "Opción #3" in row[0]
    for c_idx, val in enumerate(row, 1):
        cell = ws_sum.cell(row=r_idx, column=c_idx, value=val)
        cell.font = font_td_bold if is_rec else font_td
        cell.border = thin_border
        if is_rec:
            cell.fill = fill_accent_green
        if c_idx in [5, 6, 7]:
            cell.number_format = '#,##0.00 €'
            cell.alignment = Alignment(horizontal="right")
        elif c_idx in [1, 4]:
            cell.alignment = Alignment(horizontal="center")

ws_sum.cell(row=10, column=1, value="DICTAMEN TÉCNICO OFICIAL DE HAM ESTRUCTURAS METÁLICAS:").font = font_title
ws_sum.cell(row=11, column=1, value="1. La Opción #1 (175,00 €/ML) queda desaconsejada técnicamente por incumplimiento de la norma UNE-EN ISO 14122-3 y riesgo de caída en balsa de aguas residuales.").font = font_td
ws_sum.cell(row=12, column=1, value="2. La Opción #2 (245,00 €/ML) es mecánicamente óptima y muy resistente en Tubo Cuadrado Inox AISI 316L 40x40x1.5 mm integral.").font = font_td
ws_sum.cell(row=13, column=1, value="3. La Opción #3 (265,00 €/ML) es la SOLUCIÓN RECOMENDADA: barandilla de PRFV homologada, 100% inmune a corrosión por H2S y niebla salina, con rodapié de 200 mm incluido.").font = Font(name="Segoe UI", size=9, bold=True, color="065F46")
ws_sum.cell(row=15, column=1, value="* Nota: Las recreaciones y fotomontajes fotorrealistas adjuntos en los documentos PDF y HTML han sido generados mediante Inteligencia Artificial (IA) para visualización y simulación técnica del proyecto.").font = font_subtitle

col_widths_sum = [15, 45, 22, 18, 16, 20, 20]
for idx, w in enumerate(col_widths_sum, 1):
    ws_sum.column_dimensions[get_column_letter(idx)].width = w

def crear_hoja_desglose(ws, titulo_opcion, sub_opcion, lineas, fill_header):
    ws.views.sheetView[0].showGridLines = True
    ws.merge_cells("A1:F1")
    ws["A1"] = f"HAM — {titulo_opcion.upper()}"
    ws["A1"].font = font_title
    
    ws.merge_cells("A2:F2")
    ws["A2"] = f"{sub_opcion} · Medición total: 175 ML"
    ws["A2"].font = font_subtitle
    
    headers = ["Capítulo", "Concepto y Especificación Técnica", "Cantidad", "Unidad", "Precio Unitario (€)", "Importe (€)"]
    for c_i, h in enumerate(headers, 1):
        c = ws.cell(row=4, column=c_i, value=h)
        c.font = font_th
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center" if c_i not in [2] else "left", vertical="center")
    
    curr_r = 5
    for item in lineas:
        ws.cell(row=curr_r, column=1, value=item[0]).alignment = Alignment(horizontal="left")
        ws.cell(row=curr_r, column=2, value=item[1]).alignment = Alignment(horizontal="left", wrap_text=True)
        ws.cell(row=curr_r, column=3, value=item[2]).alignment = Alignment(horizontal="right")
        ws.cell(row=curr_r, column=4, value=item[3]).alignment = Alignment(horizontal="center")
        
        c_p = ws.cell(row=curr_r, column=5, value=item[4])
        c_p.alignment = Alignment(horizontal="right")
        c_p.number_format = '#,##0.00 €'
        
        c_i = ws.cell(row=curr_r, column=6, value=f"=C{curr_r}*E{curr_r}")
        c_i.alignment = Alignment(horizontal="right")
        c_i.number_format = '#,##0.00 €'
        
        for ci in range(1, 7):
            ws.cell(row=curr_r, column=ci).border = thin_border
            ws.cell(row=curr_r, column=ci).font = font_td
        curr_r += 1
    
    ws.merge_cells(f"A{curr_r}:E{curr_r}")
    ws.cell(row=curr_r, column=1, value="BASE IMPONIBLE:").alignment = Alignment(horizontal="right")
    ws.cell(row=curr_r, column=1).font = font_total
    c_base = ws.cell(row=curr_r, column=6, value=f"=SUM(F5:F{curr_r-1})")
    c_base.number_format = '#,##0.00 €'
    c_base.font = font_total
    curr_r += 1

    ws.merge_cells(f"A{curr_r}:E{curr_r}")
    ws.cell(row=curr_r, column=1, value="IVA (21%):").alignment = Alignment(horizontal="right")
    ws.cell(row=curr_r, column=1).font = font_td
    c_iva = ws.cell(row=curr_r, column=6, value=f"=F{curr_r-1}*0.21")
    c_iva.number_format = '#,##0.00 €'
    c_iva.font = font_td
    curr_r += 1

    ws.merge_cells(f"A{curr_r}:E{curr_r}")
    ws.cell(row=curr_r, column=1, value="TOTAL PRESUPUESTO:").alignment = Alignment(horizontal="right")
    ws.cell(row=curr_r, column=1).font = font_title
    c_tot = ws.cell(row=curr_r, column=6, value=f"=F{curr_r-2}+F{curr_r-1}")
    c_tot.number_format = '#,##0.00 €'
    c_tot.font = font_title
    
    col_w = [14, 55, 10, 8, 18, 18]
    for idx, w in enumerate(col_w, 1):
        ws.column_dimensions[get_column_letter(idx)].width = w

# HOJA 2: OPCIÓN 1
ws_op1 = wb.create_sheet("Opción 1 - Inox + Cuerdas")
lineas_op1 = [
    ("Materiales", "Montantes verticales Inox AISI 316L h=1.100mm con placa base y 2 cáncamos pasantes (cada 2m)", 88, "ud", 145.00),
    ("Materiales", "Cuerda pasamanos/intermedia (2 pasadas x 175 ML) + 16 tensores náuticos AISI 316 y herrajes", 1, "lote", 1250.00),
    ("Fijaciones", "Anclajes químicos M10 inox A4 (AISI 316) con resina de inyección en corona de hormigón", 88, "ud", 12.00),
    ("Taller HAM", "Mano de obra de fabricación en taller: corte, soldadura TIG con aportación 316L y pasivado", 60, "h", 40.00),
    ("Montaje Obra", "Mano de obra especialista de replanteo, fijación a hormigón, aplomado, enhebrado y tesado", 175, "ML", 68.00),
    ("Logística/Seg.", "Transporte local a EDAR Es Castell, medios auxiliares y EPIs de seguridad", 1, "lote", 1259.00)
]
crear_hoja_desglose(ws_op1, "Opción #1: Inox 316L + Cuerdas (175,00 €/ML)", "Montantes Inox AISI 316L con 2 líneas de cuerda náutica pasamanos/intermedia", lineas_op1, fill_navy)

# HOJA 3: OPCIÓN 2
ws_op2 = wb.create_sheet("Opción 2 - Inox 316L Modular")
lineas_op2 = [
    ("Materiales", "Montantes verticales tubo Inox AISI 316L 40x40x1.5mm h=1.100mm con base 120x120 y orejas soldadas para tornillo M12", 118, "ud", 125.00),
    ("Materiales", "Pasamanos modular en tramos 1,5m tubo cuadrado Inox AISI 316L 40x40x1.5mm perforado en puntas para atornillar a montantes", 175, "ML", 42.00),
    ("Materiales", "Barra intermedia modular en tramos 1,5m tubo cuadrado Inox AISI 316L 40x40x1.5mm atornillada a orejas intermedias (h=550mm)", 175, "ML", 28.00),
    ("Tornillería/Ancl.", "Tornillería pasante M12 A4-70 autoblocante con arandelas y 472 anclajes químicos M10x130 A4 en corona de hormigón", 1, "lote", 1950.00),
    ("Taller HAM", "Mano de obra taller: corte perfiles 40x40x1.5, perforaciones en puntas, armado, TIG y decapado/pasivado", 100, "h", 40.00),
    ("Montaje Obra", "Mano de obra montaje e instalación completa de 175 ML en EDAR Es Castell (equipo especialista HAM)", 175, "ML", 50.00),
    ("Logística/Seg.", "Transporte de perfiles protegidos a obra, furgón taller, generadores y prevención de riesgos", 1, "lote", 1175.00)
]
crear_hoja_desglose(ws_op2, "Opción #2: Inox 316L Modular 40x40x1.5 (245,00 €/ML)", "Barandilla modular con tubo 40x40x1.5mm en montantes y travesaños, orejas soldadas y tornillos pasantes M12", lineas_op2, fill_navy)

# HOJA 4: OPCIÓN 3
ws_op3 = wb.create_sheet("Opción 3 - PRFV Articulada")
lineas_op3 = [
    ("Material PRFV", "Suministro Barandilla PRFV según Ficha Técnica (tubo 50x50x5, pasamano Omega E-2100, intermedio Ø25, rodapié 200x3.5mm, rótulas POM y bases)", 175, "ML", 145.00),
    ("Fijaciones A4", "Juegos de anclajes estructurales de suelo en Acero Inoxidable A-4 para las 160 bases de suelo", 160, "ud", 12.50),
    ("Mano de Obra", "Mano de obra oficial montador especialista en obra (80 horas): replanteo, taladros y montaje", 80, "h", 55.00),
    ("Mano de Obra", "Mano de obra ayudante especialista de montaje (80 horas): acopio, asistencia y fijación", 80, "h", 45.00),
    ("Montaje Especial.", "Alineación perimetral, ensamblaje de rodapié y remates continuos", 175, "ML", 48.00),
    ("Medios/Seg.", "Medios auxiliares, herramientas batería, aspiración, furgón taller durante 10 días y EPIs", 1, "lote", 2600.00)
]
crear_hoja_desglose(ws_op3, "Opción #3: Barandilla PRFV (265,00 €/ML)", "Barandilla modular pultruida de PRFV según Ficha Técnica Oficial (UNE-EN ISO 14122)", lineas_op3, fill_green_hdr)

wb.save(xlsx_path)
wb.save(xlsx_dest)
print(f"Excel guardado con éxito:\n - {xlsx_path}\n - {xlsx_dest}")

# JSON & README
datos_json = {
    "numeroPresupuesto": "P-2026-0040",
    "fecha": "2026-10-09",
    "cliente": "EDAR Es Castell / Mahón",
    "ubicacion": "Es Castell / Mahón, Menorca",
    "longitudML": 175.0,
    "fotomontajes": {
        "opcion1": "img/fotomontaje_op1.jpg",
        "opcion2": "img/fotomontaje_op2.jpg",
        "opcion3": "img/fotomontaje_op3.jpg"
    },
    "opciones": [
        {
            "id": 1,
            "nombre": "Verticales Inox 316L + Cuerdas",
            "pvpUnitarioML": 175.00,
            "baseImponible": 30625.00,
            "iva": 6431.25,
            "totalConIva": 37056.25,
            "cumpleNorma": False
        },
        {
            "id": 2,
            "nombre": "Barandilla Inox 316L Rígida Integral",
            "pvpUnitarioML": 245.00,
            "baseImponible": 42875.00,
            "iva": 9003.75,
            "totalConIva": 51878.75,
            "cumpleNorma": True
        },
        {
            "id": 3,
            "nombre": "Barandilla Articulada PRFV (Ficha Técnica)",
            "pvpUnitarioML": 265.00,
            "baseImponible": 46375.00,
            "iva": 9738.75,
            "totalConIva": 56113.75,
            "cumpleNorma": True,
            "recomendada": True
        }
    ]
}

with open(json_dest, "w", encoding="utf-8") as f:
    json.dump(datos_json, f, indent=2, ensure_ascii=False)

print("Proceso completado.")
