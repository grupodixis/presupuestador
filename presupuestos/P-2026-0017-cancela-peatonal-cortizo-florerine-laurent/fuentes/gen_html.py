import json, os, shutil, sys
OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
d = json.load(open('calc.json', encoding='utf8'))
P = d['params']; V = d['variants']
for f in os.listdir('render3d'):
    shutil.copy(os.path.join('render3d', f), os.path.join(OUT, 'img', f))
    import cv2
    im = cv2.imread(os.path.join('render3d', f))
    cv2.imwrite(os.path.join(OUT, 'img', f.replace('.jpg', '_crop.jpg')), im[150:590, 385:880], [cv2.IMWRITE_JPEG_QUALITY, 92])
shutil.copy('foto.png', os.path.join(OUT, 'img', 'foto_actual.png'))

REF, FECHA = 'P-2026-0017', '19/10/2026'
def eur(x): return f"{x:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')
def num(x, n=1): return f"{x:,.{n}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
CNAMES = {'blanco': 'Blanco', 'antracita': 'Gris antracita', 'verde': 'Verde carruaje'}
CREF = {'blanco': 'RAL 9016', 'antracita': 'RAL 7016', 'verde': 'tono a confirmar en carta'}
SW = {'blanco': '#ece9e2', 'antracita': '#383e42', 'verde': '#1f3324'}
VAR = {
 'portales': ('A', 'CORTIZO Portales · lama ciega vertical',
   'Bastidor de hoja Portales COR-2245 (101 × 50 mm) con travesaño intermedio COR-2243 y relleno ciego de lamas apilables machihembradas COR-2290 (200 × 20 mm) en vertical. Máxima privacidad, aspecto continuo y robusto.'),
 'mallorquina': ('B', 'Portales + paño Mallorquina de lamas fijas',
   'Bastidor Portales COR-2245 dividido en 3 paños (cancela) y 1 paño (peatonal) con relleno CORTIZO Mallorquina de lamas fijas inclinadas (COR-2440 rigidizadora en la cancela, COR-440 en la peatonal) a paso de 40 mm. Ventila y deja pasar luz sin vistas directas, estética tradicional menorquina.'),
 'rejas': ('C', 'Portales + rejas verticales 100 × 20 mm',
   'Bastidor Portales COR-2245 con soporte para barrotes COR-2265 y tubos rectangulares de 100 × 20 mm en vertical, cara de 100 mm vista, con hueco libre de ≈100 mm entre tubos (16 tubos en la cancela y 3 en la peatonal). Aspecto ligero y contemporáneo, con visibilidad parcial.'),
}

CSS = """
:root{--ink:#1e2530;--muted:#5f6c80;--line:#d8e0e9;--soft:#f4f7fa;--brand:#0f172a;--accent:#0284c7;--highlight:#f0f9ff}
*{box-sizing:border-box}body{margin:0;background:#e2e8f0;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;font-size:13px;line-height:1.45}
.page{width:210mm;min-height:297mm;margin:20px auto;background:#fff;box-shadow:0 14px 38px rgba(15,23,42,.12);padding:14mm 16mm;position:relative}
header{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:start;border-top:5px solid var(--brand);padding-top:14px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.company{display:flex;gap:18px}.logo{width:150px;flex:0 0 150px}.logo img{width:100%;display:block}
.company h1{margin:0;color:var(--brand);font-size:18px;letter-spacing:.5px}.company p,.meta p{margin:2px 0;color:var(--muted);font-size:11.5px}
.meta{text-align:right;min-width:200px}.meta h2{margin:0 0 6px;color:var(--brand);font-size:23px;text-transform:uppercase;letter-spacing:1px}
.ref-badge{display:inline-block;padding:4px 10px;background:var(--soft);border:1px solid var(--line);font-weight:700;color:var(--brand);border-radius:4px}
.hero{margin:14px 0;padding:12px 16px;border-left:4px solid var(--accent);background:linear-gradient(135deg,var(--highlight) 0%,#fff 80%);border-radius:0 6px 6px 0}
.hero h2{margin:0 0 5px;color:var(--brand);font-size:17px}.hero p{margin:0;color:var(--muted);font-size:12.5px}
.client-card{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:var(--soft);border:1px solid var(--line);padding:10px 14px;border-radius:6px;margin-bottom:12px;font-size:12.5px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0}
.card{border:1px solid var(--line);background:#fafbfc;padding:8px 10px;border-radius:6px}
.card .label{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}.card .value{font-weight:700;font-size:13px;color:var(--brand)}
h3{margin:16px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line);color:var(--brand);font-size:14.5px;text-transform:uppercase;letter-spacing:.5px}
table{width:100%;border-collapse:collapse;margin:6px 0 12px}th{background:var(--brand);color:#fff;text-align:left;padding:7px 9px;font-size:11px;text-transform:uppercase;letter-spacing:.4px}
td{padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top;font-size:12px}.right{text-align:right;white-space:nowrap}.center{text-align:center}
.total-row td{background:#f8fafc;border-top:2px solid var(--accent);font-weight:700}
.matrix td,.matrix th{text-align:right}.matrix td:first-child,.matrix th:first-child{text-align:left}
.matrix .big{font-size:14px;font-weight:800;color:var(--brand)}.matrix .sub{display:block;font-size:10.5px;color:var(--muted);font-weight:400}
.photo-main{width:100%;height:92mm;object-fit:cover;object-position:50% 50%;border-radius:6px;border:1px solid var(--line);display:block}
.photos{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:8px 0 6px}
.photos figure{margin:0}.photos img{width:100%;aspect-ratio:495/440;object-fit:cover;border-radius:6px;border:1px solid var(--line);display:block}
.photos figcaption{display:flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;color:var(--brand);margin-top:4px}
.sw{width:12px;height:12px;border-radius:3px;border:1px solid #9aa5b4;display:inline-block}
.photos .price{margin-left:auto;font-weight:800}
.vhead{display:flex;align-items:baseline;gap:10px;margin-top:6px}.vtag{background:var(--brand);color:#fff;border-radius:4px;padding:2px 9px;font-weight:800;font-size:13px}
.vhead h2{margin:0;font-size:17px;color:var(--brand)}.vdesc{color:var(--muted);font-size:12px;margin:4px 0 2px}
ul{margin:6px 0 0;padding-left:18px;font-size:12px}ul li{margin-bottom:3px}
.notice{border-left:4px solid var(--accent);background:var(--highlight);padding:9px 13px;margin:12px 0;font-size:11.5px;color:#0c4a6e;border-radius:0 4px 4px 0}
.warn{border-left-color:#d97706;background:#fffbeb;color:#78350f}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.sign{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:14px}.sig-box{min-height:70px;border:1px dashed var(--line);border-radius:6px;padding:10px;color:var(--muted);font-size:11.5px;background:#fafbfc}
footer{display:flex;justify-content:space-between;border-top:1px solid var(--line);margin-top:14px;padding-top:7px;color:var(--muted);font-size:10px}
@media print{@page{size:A4;margin:0}body{background:#fff;font-size:11px;line-height:1.32}.page{margin:0;box-shadow:none;width:210mm;height:297mm;min-height:0;overflow:hidden;padding:9mm 11mm;page-break-after:always}td{padding:4px 7px;font-size:10.5px}th{padding:5px 7px;font-size:9.5px}h3{margin:10px 0 5px;font-size:12.5px}.hero{margin:9px 0;padding:8px 12px}.grid{margin:8px 0}.photo-main{height:80mm}.notice{margin:7px 0;padding:7px 11px}header{padding-top:9px;padding-bottom:8px}.logo{width:120px;flex-basis:120px}.client-card{padding:8px 12px;margin-bottom:8px}ul li{margin-bottom:1px;font-size:10.5px}footer{position:absolute;left:11mm;right:11mm;bottom:7mm}.long{height:auto!important;overflow:visible!important}.long footer{position:static}.page:last-child{page-break-after:auto}table,.photos,.notice{break-inside:avoid}}
"""

def header():
    return f"""<header><section class="company"><div class="logo"><img src="https://www.alufac.es/assets/alufac-logo.svg" alt="ALUFAC"></div>
<div><h1>ALUFAC</h1><p>Carpintería de aluminio, PVC y cerramientos a medida en Menorca</p><p>Circunval·lació, 11 · 07710 Sant Lluís, Menorca</p>
<p>info@alufac.es · Tel/WhatsApp: +34 669 769 541 · www.alufac.es</p></div></section>
<section class="meta"><h2>Presupuesto</h2><div class="ref-badge">Nº {REF}</div><p>Fecha: {FECHA}</p><p>Validez: 30 días</p></section></header>"""

def footer(n):
    return f'<footer><span>Presupuesto {REF} · Florerine Laurent · Cancela + peatonal CORTIZO</span><span>Pág. {n} · ALUFAC Menorca · info@alufac.es</span></footer>'

# ---------- Página 1: portada + matriz
rows = ''
for v, (tag, title, _) in VAR.items():
    tds = ''.join(f"<td><span class='big'>{eur(V[v]['colors'][c]['base'])}</span><span class='sub'>Total IVA incl. {eur(V[v]['colors'][c]['total'])}</span></td>" for c in CNAMES)
    rows += f"<tr><td><strong>{tag} · {title}</strong></td>{tds}</tr>"
p1 = f"""<main class="page">{header()}
<section class="hero"><h2>Cancela corredera de garaje + puerta peatonal · CORTIZO Portales</h2>
<p>Sustitución de la cancela corredera y la puerta peatonal de madera actuales por carpintería de aluminio CORTIZO lacada con calidad QUALICOAT SEASIDE para ambiente marino. Se presentan tres diseños de relleno (A, B y C) en tres colores, con motorización nueva incluida.</p></section>
<section class="client-card"><div><strong>Cliente:</strong> Florerine Laurent<br><strong>Teléfono:</strong> +44 7763 526090</div>
<div><strong>Ubicación de obra:</strong> Calle Baixada a la mar, 6<br><strong>Población:</strong> 07713 Son Ganxo, Sant Lluís (Menorca)<br><strong>Ambiente:</strong> Marino costero</div></section>
<section class="grid">
<article class="card"><span class="label">Hueco cancela</span><span class="value">3.435 × 1.800 mm</span></article>
<article class="card"><span class="label">Hueco peatonal</span><span class="value">985 × 1.800 mm</span></article>
<article class="card"><span class="label">Sistema</span><span class="value">CORTIZO Portales</span></article>
<article class="card"><span class="label">Motorización</span><span class="value">Motor nuevo incluido</span></article></section>
<h3>Situación actual</h3>
<img class="photo-main" src="img/foto_actual.png" alt="Cancela y puerta peatonal de madera actuales con medidas">
<h3>Resumen de precios · cancela + peatonal + motor</h3>
<table class="matrix"><thead><tr><th>Diseño</th>{''.join(f'<th><span class="sw" style="background:{SW[c]}"></span> {n}</th>' for c, n in CNAMES.items())}</tr></thead>
<tbody>{rows}</tbody></table>
<p style="font-size:11px;color:var(--muted);margin:0">Importes en base imponible (IVA 21 % no incluido) salvo indicación. Cada precio incluye cancela corredera, puerta peatonal, motorización nueva, desmontaje de lo existente, transporte y montaje.</p>
{footer(1)}</main>"""

# ---------- Páginas por variante
pages = []
for i, (v, (tag, title, desc)) in enumerate(VAR.items()):
    var = V[v]; ci = var['cancela']['info']
    figs = ''.join(f"""<figure><img src="img/{v}_{c}_crop.jpg" alt="Fotomontaje {title} en {n}"><figcaption><span class="sw" style="background:{SW[c]}"></span>{n}<span class="price">{eur(var['colors'][c]['base'])}</span></figcaption></figure>""" for c, n in CNAMES.items())
    if v == 'portales':
        relleno = f"Relleno ciego de {ci['lamas']} lamas apilables COR-2290 por campo, en dos campos separados por travesaño COR-2243."
    elif v == 'mallorquina':
        relleno = f"Cancela en 3 paños de ≈{ci['ancho_panel']} mm separados por montantes COR-2243; {ci['lamas_por_panel']} lamas fijas por paño (paso 40 mm) con marco 729, complemento 11494 y media lama 11495."
    else:
        relleno = f"{ci['tubos']} tubos de 100 × 20 mm en la cancela y 3 en la peatonal, hueco libre ≈{num(ci['hueco_libre_mm'],0)} mm, fijados con soporte COR-2265 arriba y abajo."
    prices = ''.join(f"<tr><td><span class='sw' style='background:{SW[c]}'></span> {n} <span style='color:var(--muted)'>({CREF[c]})</span></td><td class='right'>{eur(var['colors'][c]['sale_puertas'])}</td><td class='right'>{eur(var['colors'][c]['motor'])}</td><td class='right'><strong>{eur(var['colors'][c]['base'])}</strong></td><td class='right'>{eur(var['colors'][c]['total'])}</td></tr>" for c, n in CNAMES.items())
    pages.append(f"""<main class="page">{header()}
<div class="vhead"><span class="vtag">{tag}</span><h2>{title}</h2></div>
<p class="vdesc">{desc}</p>
<div class="photos">{figs}</div>
<p style="font-size:10.5px;color:var(--muted);margin:0 0 4px">Fotomontajes 3D sobre la fotografía actual, con las secciones reales de los perfiles; los colores en pantalla o impresión pueden variar respecto a la carta de lacado.</p>
<h3>Partidas</h3>
<table><thead><tr><th class="center" style="width:40px">Pos.</th><th>Descripción del suministro y trabajos</th><th class="center" style="width:55px">Cant.</th></tr></thead><tbody>
<tr><td class="center"><strong>01</strong></td><td><strong>Cancela corredera de 1 hoja ≈ {num(P['LC']/1000,3)} × {num(P['ALTO']/1000,2)} m</strong> sobre carril.<br>
• Bastidor perimetral con hoja para portales COR-2245, guía superior COR-2240 y perfil emboque COR-2205 en el pilar receptor.<br>• {relleno}<br>
• Rodadura en acero inoxidable AISI 316: carril, 2 ruedas con rodamientos estancos, puente guía con rodillos de nylon y tope final de carrera.<br>
• Cerradura de gancho para corredera con bombillo de seguridad y pasador.</td><td class="center">1 ud</td></tr>
<tr><td class="center"><strong>02</strong></td><td><strong>Puerta peatonal abatible de 1 hoja</strong> para hueco de 985 × 1.800 mm, mismo diseño que la cancela.<br>
• Marco para portales COR-2222 a tres lados y hoja COR-2245.<br>• Bisagras Mechanica de 3 palas, cerradura con bombillo de seguridad y manilla.</td><td class="center">1 ud</td></tr>
<tr><td class="center"><strong>03</strong></td><td><strong>Motorización nueva para la cancela corredera</strong>: motorreductor 24 V con cuadro y antiaplastamiento, 4 m de cremallera de nylon con alma de acero, 2 fotocélulas, lámpara LED y 2 mandos rolling code. Conexión a la acometida existente, programación y ensayos.</td><td class="center">1 kit</td></tr>
<tr><td class="center"><strong>04</strong></td><td><strong>Desmontaje y montaje</strong>: desmontaje y retirada de cancela, puerta peatonal y motor actuales; transporte, colocación, nivelación del carril, aplomado y ajuste en obra. Tornillería inoxidable A2/A4 y sellado con polímero MS.</td><td class="center">1 ud</td></tr>
</tbody></table>
<h3>Precio por color</h3>
<table><thead><tr><th>Color (Qualicoat Seaside)</th><th class="right">Puertas (01+02+04)</th><th class="right">Motor (03)</th><th class="right">Base imponible</th><th class="right">Total IVA incl.</th></tr></thead><tbody>{prices}</tbody></table>
{footer(i + 2)}</main>""")

# ---------- Condiciones
cond = f"""<main class="page">{header()}
<section class="two-col"><div><h3>Incluido en la oferta</h3><ul>
<li>Fabricación a medida en perfilería CORTIZO, aleación 6063.</li><li>Lacado QUALICOAT SEASIDE para ambiente marino.</li>
<li>Rodadura y carril en acero inoxidable AISI 316.</li><li>Motorización nueva completa con 2 mandos.</li>
<li>Desmontaje y retirada de cancela, peatonal y motor actuales.</li><li>Transporte a Son Ganxo, montaje y puesta en marcha.</li></ul></div>
<div><h3>Condiciones</h3><ul>
<li><strong>Forma de pago:</strong> 50 % al pedido y replanteo, 50 % a la finalización.</li>
<li><strong>Plazo:</strong> 4 a 5 semanas desde la confirmación de medidas y color.</li>
<li><strong>Garantía:</strong> 2 años en perfilería, herrajes y motor.</li>
<li><strong>No incluye:</strong> albañilería, reparación de pilares ni acometida eléctrica nueva.</li></ul></div></section>
<div class="notice"><strong>Medidas:</strong> el presupuesto se basa en las medidas de la fotografía (cancela 343,5 × 180 cm, peatonal 98,5 × 180 cm). Antes de fabricar se tomarán medidas definitivas en obra; la hoja corredera se fabrica con 150 mm de solape sobre el hueco.</div>
<div class="notice"><strong>Colores:</strong> blanco RAL 9016 y gris antracita RAL 7016. El verde carruaje se confirmará con el código exacto de la carta de colores Cortizo antes del pedido.</div>
<div class="notice"><strong>Diseño B (Mallorquina):</strong> combina el bastidor Portales con el paño de lamas fijas de la serie Mallorquina. La unión entre ambos sistemas se validará con la oficina técnica de Cortizo antes de fabricar.</div>
<div class="notice"><strong>Diseño C (rejas):</strong> el tubo de 100 × 20 mm no pertenece a la serie Portales; se suministrará en aluminio lacado del mismo color y calidad.</div>
<h3>Aceptación</h3>
<section class="sign"><div class="sig-box"><strong>Por ALUFAC:</strong><br>Departamento técnico y comercial</div>
<div class="sig-box"><strong>Aceptación del cliente:</strong> Florerine Laurent<br>Diseño: [&nbsp;&nbsp;] A &nbsp;&nbsp;[&nbsp;&nbsp;] B &nbsp;&nbsp;[&nbsp;&nbsp;] C<br>Color: [&nbsp;&nbsp;] Blanco &nbsp;[&nbsp;&nbsp;] Gris antracita &nbsp;[&nbsp;&nbsp;] Verde carruaje<br>Firma y fecha:</div></section>
{footer(len(VAR) + 2)}</main>"""

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Presupuesto {REF} - Cancela y peatonal CORTIZO</title><style>{CSS}</style></head><body>{p1}{''.join(pages)}{cond}</body></html>"""
open(os.path.join(OUT, 'presupuesto-cliente.html'), 'w', encoding='utf8').write(html)

# ---------- Anexo técnico interno
blocks = ''
for v, (tag, title, _) in VAR.items():
    var = V[v]
    for part in ('cancela', 'peatonal'):
        g = var[part]
        trs = ''.join(f"<tr><td>{r['ref']}</td><td>{r['desc']}</td><td class='right'>{num(r['m'],2)}</td><td class='right'>{num(r['kg_m'],3)}</td><td class='right'>{num(r['kg'],1)}</td></tr>" for r in g['rows'])
        info = ' · '.join(f"{k}: {val}" for k, val in g['info'].items())
        blocks += f"<h3>{tag} · {title} — {part}</h3><p class='vdesc'>{info}</p><table><thead><tr><th>Ref.</th><th>Perfil</th><th class='right'>m</th><th class='right'>kg/m</th><th class='right'>kg</th></tr></thead><tbody>{trs}<tr class='total-row'><td colspan='4'>Neto / con merma 10 %</td><td class='right'>{num(g['kg_neto'])} / {num(g['kg_merma'])}</td></tr></tbody></table>"
    for c, n in CNAMES.items():
        col = var['colors'][c]
        trs = ''.join(f"<tr><td>{a}</td><td class='right'>{eur(b)}</td></tr>" for a, b in col['lines'])
        blocks += f"<table><thead><tr><th>Coste técnico {tag} · {n}</th><th class='right'>Importe</th></tr></thead><tbody>{trs}<tr class='total-row'><td>Coste técnico</td><td class='right'>{eur(col['cost'])}</td></tr><tr><td>Venta puertas: coste × (1 + {num(P['gg'],0)} %) / (1 − {num(P['mg'],0)} %) = × {num(P['margin'],4)} + transporte {eur(P['transport'])}</td><td class='right'>{eur(col['sale_puertas'])}</td></tr><tr><td>Motorización: coste {eur(col['motor_cost'])} ({eur(P['motor_mat'])} material P-2026-0016 + {P['motor_h']} h × {num(P['hour_m'],0)} €/h) × {num(P['margin'],4)}</td><td class='right'>{eur(col['motor'])}</td></tr><tr class='total-row'><td>Base imponible</td><td class='right'>{eur(col['base'])}</td></tr></tbody></table>"
tec = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{REF} técnico interno</title><style>{CSS}</style></head><body><main class="page long">{header()}
<section class="hero"><h2>Anexo técnico interno · despiece, pesos y costes</h2><p>Uso interno. No entregar al cliente.</p></section>
<div class="notice warn"><strong>Origen de datos y pendientes</strong><ul>
<li>Pesos (g/m) y referencias: catálogos oficiales Cortizo <em>Portales</em> (05/2022) y <em>Mallorquina</em> (02/2024), descargados de downloads.cortizo.com.</li>
<li><strong>Tarifas de presupuestos.alufac.es (19/10/2026):</strong> aluminio {num(P['eur_kg'],2)} €/kg, taller {num(P['hour'],0)} €/h, montaje {num(P['hour_m'],0)} €/h, transporte {eur(P['transport'])}/obra, gastos generales {num(P['gg'],0)} %, margen sobre venta {num(P['mg'],0)} %, IVA 21 %. Fórmula de la app: venta = coste × (1+GG)/(1−margen); transporte sumado sin margen.</li>
<li>Recargo color RAL 7016 y verde carruaje: +{num(P['ral_extra'],2)} €/kg (diferencia de puntos medios blanco/RAL de la skill costes-aluminio-cortizo). La app no distingue color; <strong>recargo confirmado por ALUFAC (19/10/2026).</strong></li>
<li>Rodadura (420 €), cerrajería (110 €), tornillería (70 €) y material del motor ({eur(P['motor_mat'])}): costes del P-2026-0016 (la app no tiene tarifa de herrajes).</li>
<li>Bisagras peatonal 105 €: punto medio del coste fijo por hoja de Mallorquina (skill). Accesorios Mallorquina: 60 % sobre su perfilería (mínimo del ratio de la skill). <strong>Pendientes de tarifa.</strong></li>
<li>Tubo 100 × 20 × 2: peso teórico {num(P['tubo_kg_m'],3)} kg/m (sección 464 mm², densidad 2,70); no es perfil Cortizo. <strong>Espesor y proveedor pendientes.</strong></li>
<li>Horas de taller: cancela Portales 12 h (P-2026-0016); el resto son estimaciones por diseño (ajustables). Montaje 14 h, desmontaje 5 h, instalación motor 5 h (a tarifa de montaje).</li>
<li>Geometría: hoja corredera {P['LC']} × {P['ALTO']} mm (hueco 3.435 + 150 de solape); peatonal {P['LP']} × {P['HP']} mm en marco COR-2222. Medidas de la foto, pendientes de verificar en obra.</li>
<li>Diseño B combina Portales y Mallorquina: Cortizo no publica esa unión → validar con TSAC Baleares.</li></ul></div>
{blocks}{footer('T')}</main></body></html>"""
open(os.path.join(OUT, 'presupuesto-interno-tecnico.html'), 'w', encoding='utf8').write(tec)
print('ok')
