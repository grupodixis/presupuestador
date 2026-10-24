"""Fotomontajes orientativos: 3 variantes x 3 colores sobre la foto del cliente."""
import cv2, numpy as np, json, os, sys

S = 0.4  # px por mm en el alzado
calc = json.load(open('calc.json', encoding='utf8'))['params']
LC, ALTO, LP, HP = calc['LC'], calc['ALTO'], calc['LP'], calc['HP']
F = 101
COLORS = {'blanco': (226, 231, 232), 'antracita': (58, 54, 49), 'verde': (36, 50, 28)}  # BGR aprox RAL 9016 / 7016 / verde carruaje

photo = cv2.imread('foto.png')
H0, W0 = photo.shape[:2]

# 1) Limpieza de cotas rojas
b, g, r = [photo[..., i].astype(int) for i in range(3)]
red = ((r > 110) & (r - g > 50) & (r - b > 45)).astype(np.uint8) * 255
red = cv2.dilate(red, np.ones((5, 5), np.uint8), 2)
clean = cv2.inpaint(photo, red, 6, cv2.INPAINT_TELEA)

# Cuadriláteros (TL, TR, BR, BL) en la foto
Q_C = np.float32([(434, 216), (719, 199), (703, 525), (444, 396)])
Q_P = np.float32([(740, 219), (812, 221), (801, 469), (727, 482)])
POST_EDGE = [(751, 120), (728, 530)]  # canto derecho del pilar izquierdo (delante de la peatonal)
MOTOR = np.int32([(584, 478), (600, 470), (624, 468), (668, 468), (675, 486), (676, 540), (654, 549), (628, 543), (606, 528), (586, 521)])

def plate(w, h):
    """Fondo visto a través de huecos: seto/jardín difuso arriba, grava abajo."""
    y = np.linspace(0, 1, h)[:, None]
    top, mid, bot = np.array([80, 104, 92]), np.array([38, 58, 46]), np.array([110, 135, 152])
    col = np.where(y[..., None] < 0.55, top + (mid - top) * (y[..., None] / 0.55), mid + (bot - mid) * ((y[..., None] - 0.55) / 0.45))
    img = np.repeat(col, w, axis=1).astype(np.float32)
    rng = np.random.default_rng(3)
    noise = cv2.GaussianBlur(rng.normal(0, 40, (h, w)).astype(np.float32), (0, 0), 9) + cv2.GaussianBlur(rng.normal(0, 25, (h, w)).astype(np.float32), (0, 0), 2)
    return np.clip(img + noise[..., None], 0, 255)

def bevel_rect(img, alpha, x0, y0, x1, y1, base, hi=1.12, lo=0.80, e=3):
    """Perfil lacado con canto iluminado arriba/izquierda y sombra abajo/derecha."""
    X0, Y0, X1, Y1 = [int(round(v * S)) for v in (x0, y0, x1, y1)]
    E = max(1, int(round(e * S)))
    img[Y0:Y1, X0:X1] = base; alpha[Y0:Y1, X0:X1] = 1
    img[Y0:Y0 + E, X0:X1] = np.clip(base * hi, 0, 255); img[Y0:Y1, X0:X0 + E] = np.clip(base * hi, 0, 255)
    img[Y1 - E:Y1, X0:X1] = base * lo; img[Y0:Y1, X1 - E:X1] = base * lo

def leaf(L, H, variant, color, peatonal=False):
    base = np.array(COLORS[color], np.float32)
    w, h = int(L * S), int(H * S)
    img = plate(w, h); alpha = np.zeros((h, w), np.float32)
    iw, ih = L - 2 * F, H - 2 * F
    if variant == 'portales':
        tr_y = F + (ih - F) / 2
        for x in np.arange(F, L - F, 200):
            x1 = min(x + 200, L - F)
            bevel_rect(img, alpha, x, F, x1, H - F, base * 0.96, hi=1.05, lo=0.70, e=4)
        bevel_rect(img, alpha, 0, tr_y, L, tr_y + F, base)
    elif variant == 'mallorquina':
        npan = 1 if peatonal else 3
        pw = (iw - (npan - 1) * F) / npan
        for k in range(npan):
            px = F + k * (pw + F)
            bevel_rect(img, alpha, px, F, px + pw, H - F, base * 0.92, e=6)  # marco 729
            for y in np.arange(F + 30, H - F - 30, 40):
                X0, X1 = int((px + 18) * S), int((px + pw - 18) * S)
                Y0, Y1 = int(y * S), int((y + 40) * S)
                grad = np.linspace(1.10, 0.72, max(1, Y1 - Y0))[:, None, None]
                img[Y0:Y1, X0:X1] = base * grad; alpha[Y0:Y1, X0:X1] = 1
                gy = int((y + 33) * S)  # rendija entre lamas: se intuye el fondo
                img[gy:Y1, X0:X1] = img[gy:Y1, X0:X1] * 0.25 + base * 0.35 * 0.75
            if k < npan - 1:
                bevel_rect(img, alpha, px + pw, 0, px + pw + F, H, base)
    elif variant == 'rejas':
        n = round((iw - 100) / 200); gap = (iw - n * 100) / (n + 1)
        bevel_rect(img, alpha, F, F, L - F, F + 22, base * 0.9)
        bevel_rect(img, alpha, F, H - F - 22, L - F, H - F, base * 0.9)
        for k in range(n):
            x = F + gap + k * (100 + gap)
            bevel_rect(img, alpha, x, F + 22, x + 100, H - F - 22, base, hi=1.15, lo=0.72, e=8)
    for (x0, y0, x1, y1) in [(0, 0, L, F), (0, H - F, L, H), (0, 0, F, H), (L - F, 0, L, H)]:
        bevel_rect(img, alpha, x0, y0, x1, y1, base)
    if peatonal:  # manilla y cerradura lado derecho
        bevel_rect(img, alpha, L - F + 20, H * 0.52, L - F + 75, H * 0.56, np.array([40, 40, 40], np.float32), e=2)
        bevel_rect(img, alpha, L - F + 40, H * 0.58, L - F + 58, H * 0.62, np.array([90, 90, 90], np.float32), e=2)
    return img, np.ones_like(alpha)

def warp(src, quad):
    tw = int(max(np.linalg.norm(quad[1] - quad[0]), np.linalg.norm(quad[2] - quad[3])) * 1.5)
    src = cv2.resize(src.astype(np.float32), (tw, int(src.shape[0] * tw / src.shape[1])), interpolation=cv2.INTER_AREA)
    h, w = src.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), quad)
    out = cv2.warpPerspective(src.astype(np.float32), M, (W0, H0), flags=cv2.INTER_AREA)
    m = cv2.warpPerspective(np.ones((h, w), np.float32), M, (W0, H0), flags=cv2.INTER_LINEAR)
    return out, m

def shading(quad):
    """Luz ambiente de la foto original sobre la puerta (sol/sombra)."""
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY).astype(np.float32)
    m = np.zeros((H0, W0), np.uint8); cv2.fillConvexPoly(m, quad.astype(np.int32), 1)
    blur = cv2.GaussianBlur(gray * m, (0, 0), 45) / np.maximum(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 45), 1e-3)
    med = np.median(gray[m > 0])
    return np.clip(blur / med, 0.85, 1.08)[..., None]

SH_C, SH_P = shading(Q_C), shading(Q_P)
hsv = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
palm = ((hsv[..., 0] > 30) & (hsv[..., 0] < 95) & (hsv[..., 1] > 70) & (hsv[..., 2] > 60)).astype(np.uint8)
palm[:, 520:] = 0; palm[:250, :] = 0
palm = cv2.morphologyEx(palm, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)).astype(np.float32)
palm = cv2.GaussianBlur(palm, (3, 3), 0)[..., None]
motor = np.zeros((H0, W0), np.float32); cv2.fillPoly(motor, [MOTOR], 1); motor = cv2.GaussianBlur(motor, (3, 3), 0)[..., None]
yy, xx = np.mgrid[0:H0, 0:W0]
(px0, py0), (px1, py1) = POST_EDGE
post_mask = (xx > px0 + (yy - py0) * (px1 - px0) / (py1 - py0)).astype(np.float32)[..., None]

os.makedirs('render', exist_ok=True)
cv2.imwrite('render/foto_limpia.jpg', clean, [cv2.IMWRITE_JPEG_QUALITY, 90])
for v in ['portales', 'mallorquina', 'rejas']:
    for c in COLORS:
        out = clean.astype(np.float32)
        img, _ = leaf(LP, HP, v, c, peatonal=True)
        wp, mp = warp(img, Q_P); mp = mp[..., None] * post_mask
        out = out * (1 - mp) + wp * SH_P * mp
        img, _ = leaf(LC, ALTO, v, c)
        wc, mc = warp(img, Q_C); mc = mc[..., None]
        out = out * (1 - mc) + wc * SH_C * mc
        out = out * (1 - motor) + photo * motor
        out = out * (1 - palm) + photo * palm
        cv2.imwrite(f'render/{v}_{c}.jpg', np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 90])
        if c == 'antracita':  # alzado limpio para ficha técnica
            el, _ = leaf(LC, ALTO, v, c)
            cv2.imwrite(f'render/alzado_{v}.png', np.clip(el, 0, 255).astype(np.uint8))
print('ok')
