"""Despiece, pesos y costes P-2026-0017 (cancela corredera + peatonal, 3 variantes x 3 colores).
Pesos: catálogo oficial Cortizo Portales (05/2022) y Mallorquina (02/2024).
Costes: referencia real P-2026-0016 (misma serie Portales); recargo color y ratios de la skill costes-aluminio-cortizo.md.
"""
import json, math

KG = {  # kg/m catálogo Cortizo
    'COR-2245': 2.4327, 'COR-2243': 2.5272, 'COR-2222': 1.728, 'COR-2240': 1.1421, 'COR-2205': 2.9781,
    'COR-2290': 2.0439, 'COR-2265': 0.378,
    '729': 0.7209, '11494': 0.270, '11495': 0.4455, 'COR-440': 0.3537, 'COR-2440': 0.3996,
    'TUBO-100x20x2': round((100*20 - 96*16) * 2.7e-3, 4),  # teórico, NO Cortizo, pendiente proveedor
}
DESC = {
    'COR-2245': 'Hoja para portales 101x50', 'COR-2243': 'Travesaño/montante portales 101x50',
    'COR-2222': 'Marco para portales 56,4x70', 'COR-2240': 'Guía hoja portal corredera',
    'COR-2205': 'Perfil emboque portales', 'COR-2290': 'Lama apilable 200x20', 'COR-2265': 'Soporte para barrotes',
    '729': 'Marco lama fija (Mallorquina)', '11494': 'Complemento (Mallorquina)', '11495': 'Media lama (Mallorquina)',
    'COR-440': 'Lama fija 50,3x10,5', 'COR-2440': 'Lama fija rigidizadora 50,3x10,5',
    'TUBO-100x20x2': 'Tubo rectangular 100x20x2 (no Cortizo)',
}
MERMA = 0.10
# Tarifas de presupuestos.alufac.es (19/10/2026)
EUR_KG = 9.0                 # Aluminio €/kg
RAL_EXTRA = 19.5 - 17.5      # recargo color RAL (skill costes-aluminio-cortizo); la app no distingue color
HOUR = 40.0                  # Mano de obra de taller €/h
HOUR_M = 45.0                # Mano de obra de montaje €/h
TRANSPORT = 100.0            # Transporte por obra (se suma sin margen, como la app)
GG, MG = 15.0, 20.0          # Gastos generales %, margen sobre venta %
MARGIN = (1 + GG / 100) / (1 - MG / 100)   # fórmula de domain.mjs calculateLine
MOTOR_MAT = 360 + 70 + 95 + 45             # P-2026-0016: motor, cremallera, seguridad, mandos
MOTOR_H = 5

# Geometría (mm)
HUECO_C, HUECO_P, ALTO = 3435, 985, 1800
LC = HUECO_C + 150           # hoja corredera: solape tras emboque y tope
LP, HP = 905, 1780           # hoja peatonal dentro de marco COR-2222
F = 101; INS = 20            # cara hoja/travesaño; inserción relleno en ranura

def gate(L, H, variant, peatonal):
    bom = {}
    add = lambda r, m: bom.__setitem__(r, bom.get(r, 0) + m)
    add('COR-2245', 2 * (L + H) / 1000)
    if peatonal:
        add('COR-2222', (2 * ALTO + HUECO_P) / 1000)
    else:
        add('COR-2240', L / 1000); add('COR-2205', H / 1000)
    iw, ih = L - 2 * F, H - 2 * F
    info = {}
    if variant == 'portales':
        add('COR-2243', (iw + 2 * INS) / 1000)
        n = math.ceil(iw / 200); field = (ih - F) / 2 + 2 * INS
        add('COR-2290', n * 2 * field / 1000); info = {'lamas': n, 'campos': 2}
    elif variant == 'mallorquina':
        npan = 1 if peatonal else 3
        pw = (iw - (npan - 1) * F) / npan
        if npan > 1: add('COR-2243', (npan - 1) * (ih + 2 * INS) / 1000)
        lama = 'COR-440' if pw <= 985 else 'COR-2440'
        n = math.ceil((ih - 166) / 40)
        for _ in range(npan):
            add('729', (2 * (pw + 28) + 2 * (ih + 28)) / 1000)
            add('11494', (2 * (pw - 80) + 2 * (ih - 84)) / 1000)
            add(lama, n * (pw - 86) / 1000)
            add('11495', 2 * (pw - 60) / 1000)
        info = {'paneles': npan, 'ancho_panel': round(pw), 'lamas_por_panel': n, 'lama': lama,
                'portalamas_300355': npan * (n + 2), 'escuadras_920347': npan * 4}
    elif variant == 'rejas':
        n = round((iw - 100) / 200); gap = (iw - n * 100) / (n + 1)
        add('COR-2265', 2 * iw / 1000)
        add('TUBO-100x20x2', n * (ih + 2 * INS) / 1000)
        info = {'tubos': n, 'hueco_libre_mm': round(gap, 1)}
    rows = [{'ref': r, 'desc': DESC[r], 'm': round(m, 2), 'kg_m': KG[r], 'kg': round(m * KG[r], 1)} for r, m in bom.items()]
    kg = sum(r['kg'] for r in rows)
    return {'rows': rows, 'kg_neto': round(kg, 1), 'kg_merma': round(kg * (1 + MERMA), 1), 'info': info}

HOURS = {  # taller (bastidor + relleno), montaje, desmontaje
    'portales':    {'taller': 8 + 4 + 3 + 1.5},
    'mallorquina': {'taller': 8 + 3 + 2.5 * 4},
    'rejas':       {'taller': 8 + 3.5 + 3 + 1},
}
COLORS = [('blanco', 'Blanco RAL 9016', 0.0), ('antracita', 'Gris antracita RAL 7016', RAL_EXTRA),
          ('verde', 'Verde carruaje', RAL_EXTRA)]

def r2(x): return round(x, 2)

out = {'params': {'eur_kg': round(EUR_KG, 2), 'ral_extra': RAL_EXTRA, 'hour': HOUR, 'hour_m': HOUR_M, 'transport': TRANSPORT,
                  'gg': GG, 'mg': MG, 'motor_mat': MOTOR_MAT, 'motor_h': MOTOR_H, 'margin': round(MARGIN, 4),
                  'LC': LC, 'LP': LP, 'HP': HP, 'ALTO': ALTO, 'tubo_kg_m': KG['TUBO-100x20x2']}, 'variants': {}}
for v in ['portales', 'mallorquina', 'rejas']:
    c = gate(LC, ALTO, v, False); p = gate(LP, HP, v, True)
    kg = c['kg_merma'] + p['kg_merma']
    mall_extra = 0.0
    if v == 'mallorquina':  # accesorios Mallorquina (portalamas, escuadras): 60 % s/ perfil Mallorquina (skill, mínimo)
        mk = sum(r['kg'] for g in (c, p) for r in g['rows'] if r['ref'] in ('729', '11494', '11495', 'COR-440', 'COR-2440'))
        mall_extra = round(mk * (1 + MERMA) * EUR_KG * 0.60, 0)
    var = {'cancela': c, 'peatonal': p, 'kg_total': round(kg, 1), 'colors': {}}
    for key, name, extra in COLORS:
        lines = [
            ('Perfilería aluminio lacado Seaside (' + f'{kg:.1f} kg con merma 10 % × {EUR_KG + extra:.2f} €/kg)', kg * (EUR_KG + extra)),
            ('Herrajes rodadura inox AISI 316 (carril, 2 ruedas, puente guía, tope)', 420),
            ('Cerrajería corredera (cerradura gancho, bombillo, pasador)', 110),
            ('Herraje peatonal: cerradura + bombillo + manilla (P-0016) y bisagras 3 palas (ref. skill)', 110 + 105),
            ('Tornillería inox A2/A4, escuadras, juntas y sellado MS', 70 + 30),
        ]
        if mall_extra: lines.append(('Accesorios Mallorquina (portalamas 300355, escuadras 920347)', mall_extra))
        lines += [
            (f"Mano de obra taller ({HOURS[v]['taller']:g} h × {HOUR:.0f} €/h)", HOURS[v]['taller'] * HOUR),
            (f'Desmontaje cancela, peatonal y motor existentes (5 h × {HOUR_M:.0f} €/h)', 5 * HOUR_M),
            (f'Montaje en obra cancela + peatonal (14 h × {HOUR_M:.0f} €/h)', 14 * HOUR_M),
        ]
        cost = sum(x for _, x in lines)
        sale = r2(cost * MARGIN + TRANSPORT)
        motor_cost = MOTOR_MAT + MOTOR_H * HOUR_M
        motor = r2(motor_cost * MARGIN)
        total = r2(sale + motor)
        var['colors'][key] = {'name': name, 'lines': [[a, round(b, 2)] for a, b in lines], 'cost': round(cost, 2),
                              'motor_cost': motor_cost, 'sale_puertas': sale, 'motor': motor, 'base': total,
                              'iva': round(total * 0.21, 2), 'total': round(total * 1.21, 2)}
    out['variants'][v] = var

json.dump(out, open('calc.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for v, d in out['variants'].items():
    print(v, 'kg', d['kg_total'], d['cancela']['info'], d['peatonal']['info'])
    for k, c in d['colors'].items(): print('  ', k, 'coste', c['cost'], 'venta puertas', c['sale_puertas'], 'base', c['base'], 'total', c['total'])
