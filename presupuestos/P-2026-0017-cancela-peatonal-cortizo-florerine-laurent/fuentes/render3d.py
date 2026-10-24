"""Fotomontajes 3D: modelo geométrico con secciones Cortizo, cámara calibrada desde la foto, z-buffer y luz de escena."""
import cv2, numpy as np, json, os, sys

calc = json.load(open('calc.json', encoding='utf8'))['params']
LC, ALTO = calc['LC'], calc['ALTO']
HUECO_P = 985
SS = 3
photo = cv2.imread('foto.png')
clean = cv2.imread('render/foto_limpia.jpg')
H0, W0 = photo.shape[:2]

# ---------- color
def lin(c): c = np.asarray(c, np.float64) / 255; return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def srgb(l): l = np.clip(l, 0, 1); return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055) * 255
COLORS = {'blanco': (241, 240, 234), 'antracita': (56, 62, 66), 'verde': (39, 53, 42)}  # RAL 9016 / 7016 / 6009 (verde carruaje ref.)
ILLUM = lin((170, 160, 143)) / lin((236, 229, 210)) * 0.97   # pilar izq. sobre enlucido blanco-crema
DARK = np.array([0.02, 0.02, 0.02])

# ---------- cámara
Q_C = np.float32([(434, 216), (719, 199), (703, 525), (444, 396)])
Q_P = np.float32([(742, 219), (812, 221), (801, 469), (729, 485)])
def pose(Q, L, H, f=None):
    Hm = cv2.getPerspectiveTransform(np.float32([(0, 0), (L, 0), (L, H), (0, H)]), Q)
    c = (W0 / 2, H0 / 2)
    if f is None:
        T = np.array([[1, 0, c[0]], [0, 1, c[1]], [0, 0, 1]]); Hn = np.linalg.inv(T) @ Hm; h1, h2 = Hn[:, 0], Hn[:, 1]
        f = np.sqrt(-(h1[0] * h2[0] + h1[1] * h2[1]) / (h1[2] * h2[2]))
    K = np.array([[f, 0, c[0]], [0, f, c[1]], [0, 0, 1]])
    M = np.linalg.inv(K) @ Hm; lam = 1 / np.linalg.norm(M[:, 0])
    if (lam * M[:, 2])[2] < 0: lam = -lam
    r1, r2, t = lam * M[:, 0], lam * M[:, 1], lam * M[:, 2]
    U, _, Vt = np.linalg.svd(np.column_stack([r1, r2, np.cross(r1, r2)])); R = U @ Vt
    C = -R.T @ t
    front = np.sign(C[2])  # +Z o -Z hacia la cámara
    return dict(K=K, R=R, t=t, C=C, front=front, f=f)
camC = pose(Q_C, LC, ALTO)
def lookat(pos, target, f, c):
    z = np.asarray(target, float) - pos; z /= np.linalg.norm(z)
    y = np.array([0, 1.0, 0]) - z[1] * z; y /= np.linalg.norm(y); x = np.cross(y, z)
    R = np.stack([x, y, z]); t = -R @ pos
    return dict(K=np.array([[f, 0, c[0]], [0, f, c[1]], [0, 0, 1]]), R=R, t=t, C=np.asarray(pos, float), front=-1.0, f=f)
_ang = np.radians(57); _ctr = np.array([HUECO_P / 2, 900, 0])
camP = lookat(_ctr + 5500 * np.array([-np.sin(_ang), 0, -np.cos(_ang)]) + [0, -650, 0], _ctr, camC['f'], (620, 370))
print('f', round(camC['f'], 1), 'cam C', camC['C'].round(0))

# ---------- luz: n en coordenadas puerta (x derecha, y abajo, z hacia cámara = front)
SUN = np.array([-0.35, -0.67, 0.55]); SUN = SUN / np.linalg.norm(SUN)   # izquierda-arriba-frente
def light(n):
    return 0.45 + 0.935 * max(0.0, float(n @ SUN))

# ---------- geometría: caras como (puntos 3D [x,y,d], normal [x,y,d] , albedo, ao)
# d = profundidad hacia atrás desde la cara frontal (mm). Se convierte a z mundo = -front*d
def box(x0, x1, y0, y1, d0, d1, alb, ao=1.0, faces='all'):
    P = lambda x, y, d: (x, y, d)
    F = []
    F.append(([P(x0, y0, d0), P(x1, y0, d0), P(x1, y1, d0), P(x0, y1, d0)], (0, 0, 1), alb, ao))       # frente
    F.append(([P(x0, y0, d1), P(x0, y0, d0), P(x0, y1, d0), P(x0, y1, d1)], (-1, 0, 0), alb, ao))      # izq
    F.append(([P(x1, y0, d0), P(x1, y0, d1), P(x1, y1, d1), P(x1, y1, d0)], (1, 0, 0), alb, ao))       # dcha
    F.append(([P(x0, y0, d1), P(x1, y0, d1), P(x1, y0, d0), P(x0, y0, d0)], (0, -1, 0), alb, ao))      # arriba
    F.append(([P(x0, y1, d0), P(x1, y1, d0), P(x1, y1, d1), P(x0, y1, d1)], (0, 1, 0), alb, ao))       # abajo
    return F

def bevel_box(x0, x1, y0, y1, d0, d1, alb, b=1.5, ao=1.0):
    """Perfil con aristas redondeadas aproximadas (chaflán pequeño en cara frontal)."""
    F = box(x0 + b, x1 - b, y0 + b, y1 - b, d0, d1, alb, ao)[:1]
    s = 0.7071
    F += [([(x0, y0 + b, d0 + b), (x0 + b, y0 + b, d0), (x0 + b, y1 - b, d0), (x0, y1 - b, d0 + b)], (-s, 0, s), alb, ao),
          ([(x1 - b, y0 + b, d0), (x1, y0 + b, d0 + b), (x1, y1 - b, d0 + b), (x1 - b, y1 - b, d0)], (s, 0, s), alb, ao),
          ([(x0 + b, y0, d0 + b), (x1 - b, y0, d0 + b), (x1 - b, y0 + b, d0), (x0 + b, y0 + b, d0)], (0, -s, s), alb, ao),
          ([(x0 + b, y1 - b, d0), (x1 - b, y1 - b, d0), (x1 - b, y1, d0 + b), (x0 + b, y1, d0 + b)], (0, s, s), alb, ao)]
    F += box(x0, x1, y0, y1, d0 + b, d1, alb, ao)[1:]
    return F

F_ = 101; REC = 13  # cara hoja; retranqueo del relleno (13 mm, pestaña de la COR-2245)

def frame(L, H, alb):
    F = []
    F += bevel_box(0, L, 0, F_, 0, 50, alb); F += bevel_box(0, L, H - F_, H, 0, 50, alb)
    F += bevel_box(0, F_, F_, H - F_, 0, 50, alb); F += bevel_box(L - F_, L, F_, H - F_, 0, 50, alb)
    return F

def portales(L, H, alb):
    F = frame(L, H, alb)
    iw0, iw1, ih0, ih1 = F_, L - F_, F_, H - F_
    ty = ih0 + (ih1 - ih0 - F_) / 2
    F += bevel_box(iw0, iw1, ty, ty + F_, 0, 50, alb)          # travesaño COR-2243 enrasado
    F += box(iw0, iw1, ih0, ih1, REC + 6, REC + 20, alb, 0.55)[:1]  # fondo de machihembrado
    s = 0.7071
    for x in np.arange(iw0, iw1 - 1, 200):                   # lama COR-2290 200x20 con chaflanes de 5 mm
        x1 = min(x + 200, iw1)
        for y0, y1 in [(ih0, ty), (ty + F_, ih1)]:
            F += [([(x + 5, y0, REC), (x1 - 5, y0, REC), (x1 - 5, y1, REC), (x + 5, y1, REC)], (0, 0, 1), alb, 0.97),
                  ([(x, y0, REC + 5), (x + 5, y0, REC), (x + 5, y1, REC), (x, y1, REC + 5)], (-s, 0, s), alb, 0.9),
                  ([(x1 - 5, y0, REC), (x1, y0, REC + 5), (x1, y1, REC + 5), (x1 - 5, y1, REC)], (s, 0, s), alb, 0.9)]
    return F

def mallorquina(L, H, alb, npan):
    F = frame(L, H, alb)
    iw = L - 2 * F_; ih0, ih1 = F_, H - F_
    pw = (iw - (npan - 1) * F_) / npan
    ang = np.radians(40)
    for k in range(npan):
        px = F_ + k * (pw + F_)
        if k < npan - 1: F += bevel_box(px + pw, px + pw + F_, ih0, ih1, 0, 50, alb)
        m = 22  # marco 729 visto
        F += bevel_box(px, px + pw, ih0, ih0 + m, 8, 45, alb, ao=0.95); F += bevel_box(px, px + pw, ih1 - m, ih1, 8, 45, alb, ao=0.95)
        F += bevel_box(px, px + m, ih0 + m, ih1 - m, 8, 45, alb, ao=0.95); F += bevel_box(px + pw - m, px + pw, ih0 + m, ih1 - m, 8, 45, alb, ao=0.95)
        F += box(px + m, px + pw - m, ih0 + m, ih0 + m + 45, 12, 25, alb, 0.93)[:1]   # media lama 11495
        F += box(px + m, px + pw - m, ih1 - m - 45, ih1 - m, 12, 25, alb, 0.93)[:1]
        xa, xb = px + m, px + pw - m
        y = ih0 + m + 45 + 22
        while y < ih1 - m - 45 - 18:
            # sección 50,3 x 10,5 girada: canto cercano (cámara) más alto, lejano más bajo
            c = np.array([y, 28.0]); u = np.array([np.sin(ang), np.cos(ang)]); v = np.array([np.cos(ang), -np.sin(ang)])
            P = [c - u * 25.15 - v * 5.25, c + u * 25.15 - v * 5.25, c + u * 25.15 + v * 5.25, c - u * 25.15 + v * 5.25]
            for i in range(4):
                a, b = P[i], P[(i + 1) % 4]
                e = b - a; nrm = np.array([e[1], -e[0]]); nrm /= np.linalg.norm(nrm)
                mid = (a + b) / 2
                if nrm @ (mid - c) < 0: nrm = -nrm
                F.append(([(xa, a[0], a[1]), (xb, a[0], a[1]), (xb, b[0], b[1]), (xa, b[0], b[1])], (0, nrm[0], -nrm[1]), alb, 0.92))
            y += 40
    return F

def rejas(L, H, alb, peatonal):
    F = frame(L, H, alb)
    iw = L - 2 * F_; ih0, ih1 = F_, H - F_
    n = round((iw - 100) / 200); gap = (iw - n * 100) / (n + 1)
    F += box(F_, L - F_, ih0, ih0 + 20, REC, REC + 25, alb, 0.85); F += box(F_, L - F_, ih1 - 20, ih1, REC, REC + 25, alb, 0.85)
    for k in range(n):
        x = F_ + gap + k * (100 + gap)
        F += bevel_box(x, x + 100, ih0 + 20, ih1 - 20, REC + 2, REC + 22, alb, b=2)
    return F

def handle(L, H, alb_metal=(60, 60, 60)):
    x = L - F_ + 25
    F = box(x, x + 30, H * 0.52, H * 0.52 + 70, -40, 0, alb_metal)          # roseta + soporte
    F += box(x - 110, x + 30, H * 0.52 + 20, H * 0.52 + 40, -55, -40, alb_metal)  # palanca
    F += box(x + 3, x + 27, H * 0.60, H * 0.60 + 45, -6, 0, (120, 120, 120))  # bombillo
    return F

def marco_peatonal(alb):
    m = 40
    F = bevel_box(0, m, 0, ALTO, -10, 60, alb) + bevel_box(HUECO_P - m, HUECO_P, 0, ALTO, -10, 60, alb) + bevel_box(m, HUECO_P - m, 0, m, -10, 60, alb)
    return F, m

# ---------- rasterizado con z-buffer
X0, Y0, X1, Y1 = 405, 180, 840, 560
RW, RH = (X1 - X0) * SS, (Y1 - Y0) * SS
yy, xx = np.mgrid[0:RH, 0:RW]
U = (xx + 0.5) / SS + X0; V = (yy + 0.5) / SS + Y0

def render(faces, cam, offset=(0, 0)):
    K, R, t, front = cam['K'], cam['R'], cam['t'], cam['front']
    Ki = np.linalg.inv(K)
    rays = np.stack([Ki[0, 0] * U + Ki[0, 2], Ki[1, 1] * V + Ki[1, 2], np.ones_like(U)], -1)
    zbuf = np.full((RH, RW), np.inf); col = np.zeros((RH, RW, 3))
    C = cam['C']
    for pts, n, alb, ao in faces:
        Pw = np.array([(p[0] + offset[0], p[1] + offset[1], -front * p[2]) for p in pts], float)
        nw = np.array([n[0], n[1], front * n[2]], float)
        if nw @ (C - Pw.mean(0)) <= 0: continue
        Pc = (R @ Pw.T).T + t
        if (Pc[:, 2] <= 1).any(): continue
        uv = (K @ Pc.T).T; uv = uv[:, :2] / uv[:, 2:3]
        poly = np.round(((uv - (X0, Y0)) * SS) * 16).astype(np.int32)
        bx0, by0 = np.clip(poly.min(0) // 16 - 1, 0, None); bx1, by1 = poly.max(0) // 16 + 2
        bx1, by1 = min(bx1, RW), min(by1, RH)
        if bx1 <= bx0 or by1 <= by0: continue
        m = np.zeros((by1 - by0, bx1 - bx0), np.uint8)
        cv2.fillPoly(m, [poly - np.array([bx0, by0]) * 16], 1, lineType=cv2.LINE_8, shift=4)
        if not m.any(): continue
        nc = R @ nw; d0 = nc @ Pc[0]
        r = rays[by0:by1, bx0:bx1]
        z = d0 / np.where(np.abs(r @ nc) < 1e-9, 1e-9, r @ nc)
        sel = (m > 0) & (z < zbuf[by0:by1, bx0:bx1])
        if not sel.any(): continue
        zbuf[by0:by1, bx0:bx1][sel] = z[sel]
        nl = np.array([n[0], n[1], n[2]], float); nl /= np.linalg.norm(nl)
        nl_light = np.array([nl[0], nl[1], nl[2]])
        shade = light(nl_light) * ao
        base = lin(alb) * ILLUM * shade
        if nl[2] > 0.5:  # lacado satinado: reflejo de cielo más claro en la parte alta
            Pcs = r[sel] * z[sel][:, None]
            yw = (R.T @ (Pcs - t).T)[1]
            spec = (1.07 - 0.12 * np.clip(yw / ALTO, 0, 1))[:, None]
            col[by0:by1, bx0:bx1][sel] = base * spec
        else:
            col[by0:by1, bx0:bx1][sel] = base
    return col, np.isfinite(zbuf)

def silhouette(cam, L, H):
    K, R, t, front = cam['K'], cam['R'], cam['t'], cam['front']
    Pw = np.array([(0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)], float)
    uv = (K @ ((R @ Pw.T).T + t).T).T; uv = uv[:, :2] / uv[:, 2:3]
    m = np.zeros((RH, RW), np.uint8)
    cv2.fillPoly(m, [np.round((uv - (X0, Y0)) * SS * 16).astype(np.int32)], 1, shift=4)
    return m > 0

# ---------- fondo visto a través (seto + terreno detrás), desde la propia foto
def background():
    hedge = clean[240:300, 380:432].astype(np.float32)
    ground = clean[560:700, 460:600].astype(np.float32)
    ground = cv2.resize(ground, None, fx=0.45, fy=0.45, interpolation=cv2.INTER_AREA) * 0.72
    sky = np.array(clean[160:175, 470:520].reshape(-1, 3).mean(0), np.float32)
    bg = np.zeros((H0, W0, 3), np.float32)
    def tile(src, w, h):
        reps = (h // src.shape[0] + 2, w // src.shape[1] + 2)
        a = np.concatenate([src, src[:, ::-1]], 1); a = np.concatenate([a, a[::-1]], 0)
        return np.tile(a, (reps[0], reps[1], 1))[:h, :w]
    hed = tile(hedge, W0, H0) * 0.82; gr = tile(ground, W0, H0)
    # horizonte de la cámara de la cancela
    R, K = camC['R'], camC['K']
    up_c = R @ np.array([0, -1, 0.0]); l = np.linalg.inv(K).T @ up_c
    ys = np.arange(H0)[:, None]; xs = np.arange(W0)[None, :]
    hor = -(l[0] * xs + l[2]) / l[1]
    top = hor - 28; bot = hor + 32
    bg[:] = sky
    m_h = (ys >= top) & (ys < bot); m_g = ys >= bot
    bg[m_h] = hed[m_h]; bg[m_g] = gr[m_g]
    bg = cv2.GaussianBlur(bg, (0, 0), 1.0)
    return bg, hor

def shade_map(Q, lo=0.4):
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY).astype(np.float32)
    m = np.zeros((H0, W0), np.uint8); cv2.fillConvexPoly(m, Q.astype(np.int32), 1)
    blur = cv2.GaussianBlur(gray * m, (0, 0), 22) / np.maximum(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 22), 1e-3)
    ref = np.percentile(gray[m > 0], 80)
    return np.clip(blur / max(ref, 1) * 1.15, lo, 1.08)

hsv = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
palm = ((hsv[..., 0] > 30) & (hsv[..., 0] < 95) & (hsv[..., 1] > 70) & (hsv[..., 2] > 60)).astype(np.float32)
palm[:, 520:] = 0; palm[:250, :] = 0
palm = cv2.GaussianBlur(palm, (3, 3), 0)[..., None]
MOTOR = np.int32([(584, 478), (600, 470), (624, 468), (668, 468), (675, 486), (676, 540), (654, 549), (628, 543), (606, 528), (586, 521)])
motor = np.zeros((H0, W0), np.float32); cv2.fillPoly(motor, [MOTOR], 1); motor = cv2.GaussianBlur(motor, (3, 3), 0)[..., None]
gy, gx = np.mgrid[0:H0, 0:W0]
post_mask = (gx > 751 + (gy - 120) * (728 - 751) / (530 - 120)).astype(np.float32)[..., None]

BG, HOR = background()
SH_C = np.clip(cv2.GaussianBlur(shade_map(Q_C, 0.55), (0, 0), 40), 0.95, 1.03)
SH_P = shade_map(Q_P, 0.35)
rng = np.random.default_rng(7)

def to_photo(col, cov, sil, shade):
    """Supermuestreo -> resolución foto; fondo en huecos; luz de escena; grano."""
    small = cv2.resize(col, (X1 - X0, Y1 - Y0), interpolation=cv2.INTER_AREA)
    cv_ = cv2.resize(cov.astype(np.float32), (X1 - X0, Y1 - Y0), interpolation=cv2.INTER_AREA)[..., None]
    sl = cv2.resize(sil.astype(np.float32), (X1 - X0, Y1 - Y0), interpolation=cv2.INTER_AREA)[..., None]
    full = np.zeros((H0, W0, 3), np.float32); a = np.zeros((H0, W0, 1), np.float32); c = np.zeros((H0, W0, 1), np.float32)
    full[Y0:Y1, X0:X1] = srgb(small / np.maximum(cv_, 1e-3) * shade[Y0:Y1, X0:X1, None])[..., ::-1]
    a[Y0:Y1, X0:X1] = sl; c[Y0:Y1, X0:X1] = cv_
    lf = cv2.GaussianBlur(rng.normal(0, 1, (H0, W0)).astype(np.float32), (0, 0), 6)[..., None]
    full = full * (1 + 0.012 * lf / max(lf.std(), 1e-6)) + rng.normal(0, 2.2, full.shape).astype(np.float32)
    # en la silueta: producto donde hay cobertura, fondo donde no
    inside = np.maximum(a, c)
    pix = full * c + BG * np.clip(inside - c, 0, 1)
    pix = pix / np.maximum(inside, 1e-3)
    return pix, inside

def compose(variant, color):
    alb = COLORS[color]
    out = clean.astype(np.float32)
    # peatonal
    mf, m = marco_peatonal(alb)
    LPw, HPh = HUECO_P - 2 * m - 6, ALTO - m - 10
    if variant == 'portales': leafF = portales(LPw, HPh, alb)
    elif variant == 'mallorquina': leafF = mallorquina(LPw, HPh, alb, 1)
    else: leafF = rejas(LPw, HPh, alb, True)
    leafF = [([(p[0], p[1], p[2] + 8) for p in pts], n, a, ao) for pts, n, a, ao in leafF + handle(LPw, HPh)]
    colP, covP = render(mf + [([(p[0] + m + 3, p[1] + m + 4, p[2]) for p in pts], n, a, ao) for pts, n, a, ao in leafF], camP)
    silP = silhouette(camP, HUECO_P, ALTO)
    # corrección: llevar el render de la cámara virtual al cuadrilátero observado de la peatonal
    K, R, t = camP['K'], camP['R'], camP['t']
    corners = np.array([(0, 0, 0), (HUECO_P, 0, 0), (HUECO_P, ALTO, 0), (0, ALTO, 0)], float)
    pc = (K @ ((R @ corners.T).T + t).T).T; pc = pc[:, :2] / pc[:, 2:3]
    Hfix = cv2.getPerspectiveTransform(np.float32((pc - (X0, Y0)) * SS), np.float32((Q_P - (X0, Y0)) * SS))
    colP = cv2.warpPerspective(colP.astype(np.float32), Hfix, (RW, RH), flags=cv2.INTER_LINEAR)
    covP = cv2.warpPerspective(covP.astype(np.float32), Hfix, (RW, RH), flags=cv2.INTER_LINEAR)
    silP = cv2.warpPerspective(silP.astype(np.float32), Hfix, (RW, RH), flags=cv2.INTER_LINEAR)
    pixP, aP = to_photo(colP, covP, silP, SH_P)
    aP = aP * post_mask
    out = out * (1 - aP) + pixP * aP
    # cancela
    if variant == 'portales': F = portales(LC, ALTO, alb)
    elif variant == 'mallorquina': F = mallorquina(LC, ALTO, alb, 3)
    else: F = rejas(LC, ALTO, alb, False)
    colC, covC = render(F, camC)
    silC = silhouette(camC, LC, ALTO)
    pixC, aC = to_photo(colC, covC, silC, SH_C)
    out = out * (1 - aC) + pixC * aC
    out = out * (1 - motor) + photo * motor
    out = out * (1 - palm) + photo * palm
    return np.clip(out, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    os.makedirs('render3d', exist_ok=True)
    todo = [(v, c) for v in ['portales', 'mallorquina', 'rejas'] for c in COLORS]
    if len(sys.argv) > 1: todo = [tuple(a.split(':')) for a in sys.argv[1:]]
    for v, c in todo:
        cv2.imwrite(f'render3d/{v}_{c}.jpg', compose(v, c), [cv2.IMWRITE_JPEG_QUALITY, 92]); print(v, c)
