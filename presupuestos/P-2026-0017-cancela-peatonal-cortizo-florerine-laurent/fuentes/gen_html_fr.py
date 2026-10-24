"""Version française du devis client (mêmes chiffres, mêmes images que gen_html.py)."""
import os, sys
OUT = sys.argv[1]
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_html.py'), encoding='utf8').read()
exec(_src.split('def header():')[0])  # données, CSS, copie des images

def eur(x): return f"{x:,.2f} €".replace(',', ' ').replace('.', ',')
def num(x, n=1): return f"{x:,.{n}f}".replace(',', ' ').replace('.', ',')
CNAMES = {'blanco': 'Blanc', 'antracita': 'Gris anthracite', 'verde': 'Vert foncé'}
CREF = {'blanco': 'RAL 9016', 'antracita': 'RAL 7016', 'verde': '« verde carruaje », teinte à confirmer'}
VAR = {
 'portales': ('A', 'CORTIZO Portales · lames pleines verticales',
   'Cadre de vantail Portales COR-2245 (101 × 50 mm) avec traverse intermédiaire COR-2243 et remplissage plein en lames emboîtables à rainure et languette COR-2290 (200 × 20 mm) posées verticalement. Intimité totale, aspect continu et robuste.'),
 'mallorquina': ('B', 'Portales + panneaux à lames fixes Mallorquina',
   'Cadre Portales COR-2245 divisé en 3 panneaux (portail) et 1 panneau (portillon), remplissage CORTIZO Mallorquina à lames fixes inclinées (COR-2440 renforcée sur le portail, COR-440 sur le portillon) au pas de 40 mm. Ventile et laisse passer la lumière sans vue directe : l’esthétique traditionnelle des volets minorquins.'),
 'rejas': ('C', 'Portales + barreaudage vertical 100 × 20 mm',
   'Cadre Portales COR-2245 avec support de barreaux COR-2265 et tubes rectangulaires de 100 × 20 mm posés verticalement, face de 100 mm visible, espacement libre d’environ 100 mm (16 tubes sur le portail, 3 sur le portillon). Aspect léger et contemporain, visibilité partielle.'),
}
CLIENT = 'Florerine Laurent'

def header():
    return f"""<header><section class="company"><div class="logo"><img src="https://www.alufac.es/assets/alufac-logo.svg" alt="ALUFAC"></div>
<div><h1>ALUFAC</h1><p>Menuiserie aluminium, PVC et fermetures sur mesure à Minorque</p><p>Circunval·lació, 11 · 07710 Sant Lluís, Minorque (Espagne)</p>
<p>info@alufac.es · Tél./WhatsApp : +34 669 769 541 · www.alufac.es</p></div></section>
<section class="meta"><h2>Devis</h2><div class="ref-badge">N° {REF}</div><p>Date : {FECHA}</p><p>Validité : 30 jours</p></section></header>"""

def footer(n):
    return f'<footer><span>Devis {REF} · {CLIENT} · Portail + portillon CORTIZO</span><span>Page {n} · ALUFAC Minorque · info@alufac.es</span></footer>'

rows = ''
for v, (tag, title, _) in VAR.items():
    tds = ''.join(f"<td><span class='big'>{eur(V[v]['colors'][c]['base'])}</span><span class='sub'>TTC (TVA 21 %) {eur(V[v]['colors'][c]['total'])}</span></td>" for c in CNAMES)
    rows += f"<tr><td><strong>{tag} · {title}</strong></td>{tds}</tr>"
p1 = f"""<main class="page">{header()}
<section class="hero"><h2>Portail coulissant + portillon · CORTIZO Portales</h2>
<p>Remplacement du portail coulissant et du portillon en bois actuels par une menuiserie aluminium CORTIZO thermolaquée QUALICOAT SEASIDE, adaptée au climat marin. Trois modèles de remplissage (A, B et C) sont proposés en trois couleurs, motorisation neuve incluse.</p></section>
<section class="client-card"><div><strong>Client :</strong> {CLIENT}<br><strong>Téléphone :</strong> +44 7763 526090</div>
<div><strong>Adresse du chantier :</strong> Calle Baixada a la mar, 6<br><strong>Localité :</strong> 07713 Son Ganxo, Sant Lluís (Minorque)<br><strong>Environnement :</strong> marin, bord de mer</div></section>
<section class="grid">
<article class="card"><span class="label">Ouverture portail</span><span class="value">3 435 × 1 800 mm</span></article>
<article class="card"><span class="label">Ouverture portillon</span><span class="value">985 × 1 800 mm</span></article>
<article class="card"><span class="label">Système</span><span class="value">CORTIZO Portales</span></article>
<article class="card"><span class="label">Motorisation</span><span class="value">Moteur neuf inclus</span></article></section>
<h3>Situation actuelle</h3>
<img class="photo-main" src="img/foto_actual.png" alt="Portail et portillon en bois actuels avec leurs dimensions">
<h3>Récapitulatif des prix · portail + portillon + moteur</h3>
<table class="matrix"><thead><tr><th>Modèle</th>{''.join(f'<th><span class="sw" style="background:{SW[c]}"></span> {n}</th>' for c, n in CNAMES.items())}</tr></thead>
<tbody>{rows}</tbody></table>
<p style="font-size:11px;color:var(--muted);margin:0">Montants hors taxes (TVA espagnole de 21 % non incluse), sauf mention TTC. Chaque prix comprend le portail coulissant, le portillon, la motorisation neuve, la dépose de l’existant, le transport et la pose.</p>
{footer(1)}</main>"""

pages = []
for i, (v, (tag, title, desc)) in enumerate(VAR.items()):
    var = V[v]; ci = var['cancela']['info']
    figs = ''.join(f"""<figure><img src="img/{v}_{c}_crop.jpg" alt="Photomontage {title} en {n}"><figcaption><span class="sw" style="background:{SW[c]}"></span>{n}<span class="price">{eur(var['colors'][c]['base'])}</span></figcaption></figure>""" for c, n in CNAMES.items())
    if v == 'portales':
        relleno = f"Remplissage plein de {ci['lamas']} lames emboîtables COR-2290 par champ, en deux champs séparés par la traverse COR-2243."
    elif v == 'mallorquina':
        relleno = f"Portail en 3 panneaux d’environ {ci['ancho_panel']} mm séparés par des montants COR-2243 ; {ci['lamas_por_panel']} lames fixes par panneau (pas de 40 mm) avec cadre 729, complément 11494 et demi-lame 11495."
    else:
        relleno = f"{ci['tubos']} tubes de 100 × 20 mm sur le portail et 3 sur le portillon, espacement libre d’environ {num(ci['hueco_libre_mm'],0)} mm, fixés en haut et en bas par le support COR-2265."
    prices = ''.join(f"<tr><td><span class='sw' style='background:{SW[c]}'></span> {n} <span style='color:var(--muted)'>({CREF[c]})</span></td><td class='right'>{eur(var['colors'][c]['sale_puertas'])}</td><td class='right'>{eur(var['colors'][c]['motor'])}</td><td class='right'><strong>{eur(var['colors'][c]['base'])}</strong></td><td class='right'>{eur(var['colors'][c]['total'])}</td></tr>" for c, n in CNAMES.items())
    pages.append(f"""<main class="page">{header()}
<div class="vhead"><span class="vtag">{tag}</span><h2>{title}</h2></div>
<p class="vdesc">{desc}</p>
<div class="photos">{figs}</div>
<p style="font-size:10.5px;color:var(--muted);margin:0 0 4px">Photomontages 3D réalisés sur la photo actuelle avec les sections réelles des profilés ; les couleurs à l’écran ou à l’impression peuvent différer du nuancier de laquage.</p>
<h3>Prestations</h3>
<table><thead><tr><th class="center" style="width:40px">Pos.</th><th>Description de la fourniture et des travaux</th><th class="center" style="width:55px">Qté</th></tr></thead><tbody>
<tr><td class="center"><strong>01</strong></td><td><strong>Portail coulissant 1 vantail ≈ {num(P['LC']/1000,3)} × {num(P['ALTO']/1000,2)} m</strong> sur rail.<br>
• Cadre périphérique en profilé de vantail COR-2245, guide supérieur COR-2240 et profilé de réception COR-2205 sur le pilier.<br>• {relleno}<br>
• Roulement en acier inoxydable AISI 316 : rail, 2 roues à roulements étanches, guide supérieur à galets nylon et butée de fin de course.<br>
• Serrure à crochet pour portail coulissant avec cylindre de sécurité et verrou.</td><td class="center">1 u</td></tr>
<tr><td class="center"><strong>02</strong></td><td><strong>Portillon battant 1 vantail</strong> pour ouverture de 985 × 1 800 mm, même modèle que le portail.<br>
• Dormant COR-2222 sur trois côtés et vantail COR-2245.<br>• Paumelles Mechanica 3 lames, serrure à cylindre de sécurité et poignée.</td><td class="center">1 u</td></tr>
<tr><td class="center"><strong>03</strong></td><td><strong>Motorisation neuve du portail coulissant</strong> : motoréducteur 24 V avec centrale et anti-écrasement, 4 m de crémaillère nylon à âme acier, 2 photocellules, feu clignotant LED et 2 télécommandes à code tournant. Raccordement à l’alimentation existante, programmation et essais.</td><td class="center">1 kit</td></tr>
<tr><td class="center"><strong>04</strong></td><td><strong>Dépose et pose</strong> : dépose et évacuation du portail, du portillon et du moteur actuels ; transport, mise en place, mise à niveau du rail, aplomb et réglages sur chantier. Visserie inox A2/A4 et joints en polymère MS.</td><td class="center">1 u</td></tr>
</tbody></table>
<h3>Prix par couleur</h3>
<table><thead><tr><th>Couleur (Qualicoat Seaside)</th><th class="right">Portes (01+02+04)</th><th class="right">Moteur (03)</th><th class="right">Total HT</th><th class="right">Total TTC</th></tr></thead><tbody>{prices}</tbody></table>
{footer(i + 2)}</main>""")

cond = f"""<main class="page">{header()}
<section class="two-col"><div><h3>Compris dans l’offre</h3><ul>
<li>Fabrication sur mesure en profilés CORTIZO, alliage 6063.</li><li>Thermolaquage QUALICOAT SEASIDE pour climat marin.</li>
<li>Roulement et rail en acier inoxydable AISI 316.</li><li>Motorisation neuve complète avec 2 télécommandes.</li>
<li>Dépose et évacuation du portail, du portillon et du moteur actuels.</li><li>Transport jusqu’à Son Ganxo, pose et mise en service.</li></ul></div>
<div><h3>Conditions</h3><ul>
<li><strong>Paiement :</strong> 50 % à la commande et au relevé de cotes, 50 % à la fin des travaux.</li>
<li><strong>Délai :</strong> 4 à 5 semaines après confirmation des dimensions et de la couleur.</li>
<li><strong>Garantie :</strong> 2 ans sur les profilés, la quincaillerie et le moteur.</li>
<li><strong>Non compris :</strong> maçonnerie, réparation des piliers et nouvelle alimentation électrique.</li></ul></div></section>
<div class="notice"><strong>Dimensions :</strong> le devis est établi à partir des cotes relevées sur la photo (portail 343,5 × 180 cm, portillon 98,5 × 180 cm). Les cotes définitives seront prises sur place avant fabrication ; le vantail coulissant est fabriqué avec un recouvrement de 150 mm sur l’ouverture.</div>
<div class="notice"><strong>Couleurs :</strong> blanc RAL 9016 et gris anthracite RAL 7016. Le vert foncé (« verde carruaje ») sera confirmé avec la référence exacte du nuancier Cortizo avant la commande.</div>
<div class="notice"><strong>Modèle B (Mallorquina) :</strong> associe le cadre Portales aux panneaux à lames fixes de la série Mallorquina. L’assemblage des deux systèmes sera validé avec le bureau technique de Cortizo avant fabrication.</div>
<div class="notice"><strong>Modèle C (barreaudage) :</strong> le tube de 100 × 20 mm ne fait pas partie de la série Portales ; il sera fourni en aluminium laqué de même couleur et de même qualité.</div>
<div class="notice"><strong>Langue :</strong> traduction du devis original en espagnol n° {REF}. En cas de divergence, la version espagnole fait foi.</div>
<h3>Acceptation</h3>
<section class="sign"><div class="sig-box"><strong>Pour ALUFAC :</strong><br>Service technique et commercial</div>
<div class="sig-box"><strong>Acceptation du client :</strong> {CLIENT}<br>Modèle : [&nbsp;&nbsp;] A &nbsp;&nbsp;[&nbsp;&nbsp;] B &nbsp;&nbsp;[&nbsp;&nbsp;] C<br>Couleur : [&nbsp;&nbsp;] Blanc &nbsp;[&nbsp;&nbsp;] Gris anthracite &nbsp;[&nbsp;&nbsp;] Vert foncé<br>Signature et date :</div></section>
{footer(len(VAR) + 2)}</main>"""

html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Devis {REF} - Portail et portillon CORTIZO</title><style>{CSS}</style></head><body>{p1}{''.join(pages)}{cond}</body></html>"""
open(os.path.join(OUT, 'devis-client-fr.html'), 'w', encoding='utf8').write(html)
print('ok')
