#!/usr/bin/env python3
"""V2 - Apotek Berkah Sehat: 'Udah enakan kok.' (antibiotik)
Three layers: WORLD (90x160 low-res, lit, camera crop) -> PROPS drawn in world ->
HUD (full-res 1080x1920 text, cards, scanlines, vignette). Timing synced to VO cues."""
import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H, S, FPS = 90, 160, 12, 30
FW, FH = W * S, H * S
import json as _json
_TM = _json.load(open('timemap.json'))
_OLD = np.array([p[0] for p in _TM]); _NEW = np.array([p[1] for p in _TM])
O = 0.3  # VO offset in final mix
def MAP(x): return float(np.interp(x, _OLD, _NEW))
def T(x): return MAP(x) + O            # old word timestamp -> new video time
def M(v): return MAP(v - O) + O        # old video time -> new video time
TOTAL = round(MAP(55.5) + O + 4.3, 2)

F_TITLE = "ps2p.ttf"; F_BODY = "pixelify700.ttf"; F_BODY2 = "pixelify500.ttf"
_fc = {}
def font(p, s):
    s = max(1, int(s)); k = (p, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(p, s)
    return _fc[k]
def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
GREEN, BLUE, YELLOW, RED = hx('227C4C'), hx('3066B5'), hx('F7CD00'), hx('e0483e')
INK = hx('15131f'); CREAM = hx('f2e9d0'); NAVY = hx('1b1830')

PAL = {k: hx(v) for k, v in {
    'H': '2a2238', 'h': '4a3d63', 'S': 'e8ad80', 's': 'c07f55', 'E': '1b1b2a', 'm': '8a3b3b', 'o': '5a1f1f',
    'R': 'd9453b', 'r': 'a8322c', 'q': 'f07a68', 'W': 'f4f4f4', 'w': 'c9d1d8', 'B': '37477a', 'b': '283559',
    'F': 'f4f4f4', 'f': '9a9a9a', 'n': 'e86a6a', 'G': '227C4C', 'g': '1a5e3a', 'j': '35a067', 'P': '3066B5',
    'D': '4a4f63', 'k': '3a3030', 'L': '7bd389', 'l': '4fa86a', 'V': '9b6bd6', 'v': 'd2b4f7', 'A': 'aab3bd',
    'a': '6b737c', 'X': 'e0483e', 'x': 'a02e28', 'Y': 'F7CD00', 'T': '7fc4ff', 'K': '15131f'}.items()}

RAKA = [
"....HHHHHHH.....", "...HHhHHHHHHH...", "..HHHHHHhHHHHH..", "..HhHHHHHHHHHH..",
"..HHSSSSSSSSHH..", "..HSSSSSSSSSSH..", "..HSSESSSSESSH..", "..HSSESSSSESSH..",
"...SSSSSSSSSS...", "...sSSSmmSSSs...", "....sSSSSSSs....", "......SSSS......",
"...RRRRRRRRRR...", "..RqRRRWRWRRRR..", ".RqRRRRWRWRRRRR.", ".RRrRRRRRRRRrRR.",
".RRrRRRRRRRRrRR.", ".SSrRRRRRRRRrSS.", ".SS.rrrrrrrr.SS.", "....BBBBBBBB....",
"....BBBBBBBB....", "....BBBbbBBB....", "....BBB..BBB....", "....BBB..BBB....",
"...FFFF..FFFF...", "...ffff..ffff..."]
WALK_B = [".....BBBBBB.....", ".....BBBBBB.....", "....FFFFFFFF....", "....ffffffff...."]
APT = [
".....GGGGGG.....", "...GGjGGGGGGG...", "..GGGgGGGGGGGG..", "..GGSSSSSSSSGG..",
"..GSSSSSSSSSSG..", "..GSSESSSSESSG..", "..GSSESSSSESSG..", "..GSSSSSSSSSSG..",
"..GGSSSmmSSSGG..", "..GGGSSSSSSGGG..", ".GGGGGGGGGGGGGG.", ".GGgGGGGGGGGgGG.",
".WWWWGGGGGGWWWW.", ".WWWWWGGGGWWWWW.", ".WWWWWWGGWWWWWW.", ".WWwWWWWWWPWwWW.",
".WWwWWWWWWPWwWW.", ".SSwWWWWWWWWwSS.", ".SS.WWWWWWWW.SS.", "....WWWWWWWW....",
"....DDDDDDDD....", "....DDDDDDDD....", "....DDDDDDDD....", "....DDD..DDD....",
"...kkkk..kkkk...", "...kkkk..kkkk..."]
BACT = ["..LLLLL..", ".LLLLLLL.", "LLELLLELL", "LLLLLLLLL", "LLLmmmLLL", ".LLLLLLL.", "..lllll.."]
BACT_ARM = ["..AAAAA..", ".AAaaaAA.", "XXEXXXEXX", "XXXXXXXXX", "XXXoooXXX", ".XXXXXXX.", "..xxxxx.."]
VIRUS = ["....v....", ".v.VVV.v.", "..VVVVV..", ".VVEVEVV.", "vVVVVVVVv", ".VVVmVVV.", "..VVVVV..", ".v.VVV.v.", "....v...."]

_sc = {}
def sprite(rows, key, swap=None):
    k = (key, tuple(sorted((swap or {}).items())))
    if k in _sc: return _sc[k]
    w = max(len(r) for r in rows); h = len(rows)
    im = Image.new('RGBA', (w + 2, h + 2), (0, 0, 0, 0)); px = im.load()
    g = [[None] * (w + 2) for _ in range(h + 2)]
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.': g[y + 1][x + 1] = PAL[(swap or {}).get(c, c)]
    for y in range(h + 2):
        for x in range(w + 2):
            if g[y][x]: px[x, y] = g[y][x] + (255,)
            elif any(0 <= x + dx < w + 2 and 0 <= y + dy < h + 2 and g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = INK + (255,)
    _sc[k] = im; return im

def person(img, base, x, feet, t, talk=False, sick=False, happy=False, walk=False, bob=True, flip=False, seed=0, cough=False):
    rows = list(base); sw = {}
    if base is RAKA:
        if sick:
            rows[8] = "...SSSSnnSSSS..."; rows[9] = "...sSSSSSSSSs..."; rows[10] = "....sSmmmmSs...."
        if happy:
            rows[6] = "..HSSSSSSSSSSH.."; rows[9] = "...sSSmmmmSSs..."
        if walk and int(t * 6) % 2: rows[22:26] = WALK_B
    if not happy and (t + seed * .37) % 3.1 < .12: sw['E'] = 'S'
    if (talk and int(t * 7) % 2 == 0) or cough: sw['m'] = 'o'
    spr = sprite(rows, (id(base), sick, happy, walk and int(t * 6) % 2), sw)
    if flip: spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    dy = 1 if (bob and not walk and int(t * 2.2 + seed) % 2 == 0) else 0
    if cough: dy = 1 if int(t * 10) % 2 else 0
    img.alpha_composite(spr, (int(round(x)), int(round(feet - spr.height + 1 + dy))))

def R(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)
def ease(u): u = max(0., min(1., u)); return 1 - (1 - u) ** 3
def eio(u): u = max(0., min(1., u)); return u * u * (3 - 2 * u)
def pop(lt, at, dur=0.25):
    u = (lt - at) / dur
    return 0 if u < 0 else 1 if u > 1 else 1 + 0.25 * math.sin(u * math.pi)
def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)

# ---------------- lighting ----------------
def light(im, ambient, lights):
    """multiply world by ambient + sum of radial lights (x,y,r,strength,tint)"""
    a = np.asarray(im.convert('RGB'), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    m = np.ones((H, W, 3), np.float32) * np.array(ambient, np.float32)
    for (lx, ly, r, s, tint) in lights:
        d = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2) / r
        f = np.clip(1 - d, 0, 1) ** 1.6 * s
        f = (np.floor(f * 6) / 6)  # banded = pixel-art lighting
        m += f[..., None] * np.array(tint, np.float32)
    out = np.clip(a * m, 0, 255).astype(np.uint8)
    return Image.fromarray(out).convert('RGBA')

# ---------------- world builders ----------------
def bedroom(t, lamp=True, calendar_on_wall=False):
    im = Image.new('RGBA', (W, H), hx('3a3358')); d = ImageDraw.Draw(im)
    for y in range(0, 92, 6):
        for x in range((y // 6) % 2 * 3, W, 6): im.putpixel((x, y + 2), hx('443c66') + (255,))
    R(d, 0, 74, W, 20, hx('2e2848')); R(d, 0, 74, W, 1, hx('534a78'))
    for x in range(0, W, 10): R(d, x, 75, 1, 19, hx('262140'))
    R(d, 0, 93, W, 3, hx('1d1932'))
    R(d, 0, 96, W, H - 96, hx('6b4a35'))
    for y in range(96, H, 6):
        R(d, 0, y, W, 1, hx('573b2a')); R(d, 0, y + 1, W, 1, hx('7a5640'))
        off = 0 if (y // 6) % 2 else 9
        for x in range(off, W, 18): R(d, x, y, 1, 6, hx('573b2a'))
    # rug
    d.ellipse([18, 108, 86, 130], fill=hx('8c3446')); d.ellipse([22, 110, 82, 128], fill=hx('a8455a'))
    for x in range(26, 80, 6): R(d, x, 118, 3, 2, hx('e0b04a'))
    # window w/ curtains + skyline
    R(d, 6, 10, 28, 30, hx('8b5a3c')); R(d, 8, 12, 24, 26, hx('1a2448'))
    for y in range(12, 38): R(d, 8, y, 24, 1, shade(hx('1a2448'), 1 + (y - 12) * .02))
    rnd = random.Random(3)
    for i in range(10):
        sx, sy = 9 + rnd.randrange(22), 13 + rnd.randrange(14)
        if (int(t * 3) + i) % 5: im.putpixel((sx, sy), hx('f4e7b0') + (255,))
    d.ellipse([22, 15, 28, 21], fill=hx('f4e7b0')); d.ellipse([24, 14, 30, 20], fill=hx('1a2448'))
    for bx, bh in ((8, 6), (12, 9), (17, 5), (21, 8), (26, 6), (29, 10)):
        R(d, bx, 38 - bh, 4, bh, hx('10162e'))
        for wy in range(38 - bh + 1, 37, 3):
            if (bx + wy) % 3: im.putpixel((bx + 1, wy), hx('e6c35a') + (255,))
    R(d, 19, 12, 2, 26, hx('8b5a3c')); R(d, 8, 24, 24, 1, hx('8b5a3c')); R(d, 4, 39, 32, 2, hx('6e4630'))
    R(d, 3, 8, 34, 2, hx('5a3d2c'))
    for cx in (4, 30):
        R(d, cx, 10, 6, 34, hx('b5394a'))
        for y in range(10, 44, 3): R(d, cx + 2, y, 1, 2, hx('8c2a38'))
    # wall clock
    d.ellipse([40, 8, 50, 18], fill=hx('f4f1e6'), outline=INK)
    a = t * 2
    d.line([(45, 13), (45 + round(math.cos(a) * 3), 13 + round(math.sin(a) * 3))], fill=INK)
    R(d, 45, 10, 1, 3, INK)
    if calendar_on_wall:
        R(d, 56, 8, 26, 24, hx('f6f1e3')); R(d, 56, 8, 26, 6, hx('d9453b')); d.rectangle([55, 7, 82, 32], outline=INK)
        for i in range(4):
            for j in range(2): R(d, 58 + i * 6, 17 + j * 7, 5, 5, hx('e6dfcc'))
    else:
        # poster
        R(d, 58, 6, 22, 26, hx('233a6b')); d.rectangle([57, 5, 80, 32], outline=INK)
        d.ellipse([63, 10, 75, 22], fill=hx('F7CD00')); R(d, 60, 24, 18, 2, hx('d9453b')); R(d, 62, 28, 14, 1, hx('f4f4f4'))
    # shelf
    R(d, 46, 40, 40, 2, hx('8b5a3c')); R(d, 46, 42, 40, 1, hx('5a3d2c'))
    bx = 48
    for c, hh in [('3066B5', 10), ('F7CD00', 8), ('d9453b', 11), ('227C4C', 9), ('f2f2f2', 7), ('9b6bd6', 10)]:
        R(d, bx, 40 - hh, 4, hh, hx(c)); R(d, bx, 40 - hh, 1, hh, shade(hx(c), 1.25)); R(d, bx, 40 - hh + 2, 4, 1, INK); bx += 5
    R(d, 79, 34, 6, 6, hx('b5653a')); R(d, 78, 28, 3, 6, hx('4fa86a')); R(d, 81, 26, 3, 8, hx('7bd389'))
    # bed
    R(d, 2, 62, 5, 36, hx('8b5a3c')); R(d, 3, 62, 1, 36, hx('a26c48'))
    R(d, 2, 76, 42, 8, hx('e8e2d0')); R(d, 7, 70, 13, 8, hx('f7f7f7')); R(d, 7, 76, 13, 2, hx('d8d4c4'))
    R(d, 12, 80, 32, 16, hx('3066B5'))
    for x in range(14, 44, 6): R(d, x, 82, 3, 12, hx('2a57a0'))
    R(d, 12, 80, 32, 2, hx('4a80d0')); R(d, 3, 96, 2, 3, hx('6e4630')); R(d, 40, 96, 2, 3, hx('6e4630'))
    return im, d

def nightstand(im, d, drawer=0.0):
    R(d, 46, 78, 14, 19, hx('8b5a3c')); R(d, 46, 78, 14, 1, hx('b07a52')); R(d, 46, 78, 1, 19, hx('a26c48'))
    R(d, 48, 83, 10, 5, hx('7a4e33')); R(d, 52, 85, 2, 1, YELLOW)
    if drawer > 0:
        dx = int(drawer); R(d, 48 + dx, 83, 10, 6, hx('a26c48')); R(d, 48 + dx, 83, 10, 1, hx('c08a60')); R(d, 52 + dx, 85, 2, 1, YELLOW)
    R(d, 51, 72, 4, 6, hx('6e4630')); d.polygon([(48, 72), (58, 72), (56, 64), (50, 64)], fill=YELLOW)
    R(d, 50, 64, 6, 1, hx('fff0a0'))

def strip(d, x, y, used=0, glow=False):
    if glow: d.rectangle([x - 2, y - 2, x + 15, y + 8], fill=hx('fff3b0'))
    R(d, x, y, 14, 7, hx('d6dde3')); d.rectangle([x - 1, y - 1, x + 14, y + 7], outline=INK)
    R(d, x, y, 14, 1, hx('ffffff'))
    for i in range(5):
        for j in range(2):
            cx, cy = x + 1 + i * 3, y + 1 + j * 3
            if i * 2 + j < used: R(d, cx, cy, 2, 2, hx('8a9299'))
            else: R(d, cx, cy, 1, 2, hx('d9453b')); R(d, cx + 1, cy, 1, 2, YELLOW)

def night_light(im, t, lamp=True, extra=()):
    L = [(20, 22, 30, .45, (0.55, 0.6, 0.9))]
    if lamp: L.append((53, 70, 40, 1.0 + 0.03 * math.sin(t * 9), (1.0, 0.85, 0.5)))
    return light(im, (0.42, 0.42, 0.58), L + list(extra))

def apotek_ext(t, day=False, rain=False, sign_on=1.0):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    top, bot = (hx('7ec8f0'), hx('d8f1fb')) if day else (hx('1c2547'), hx('46507e'))
    for y in range(100):
        u = y / 100; c = tuple(int(top[i] * (1 - u) + bot[i] * u) for i in range(3))
        R(d, 0, y, W, 1, c)
    if day:
        for cx, cy in ((10, 8), (60, 4)):
            d.ellipse([cx, cy, cx + 16, cy + 7], fill=hx('ffffff')); d.ellipse([cx + 5, cy - 4, cx + 16, cy + 5], fill=hx('ffffff'))
    else:
        for bx, bh in ((0, 30), (84, 26)): R(d, bx, 100 - bh, 8, bh, hx('151b38'))
    R(d, 0, 100, W, H - 100, hx('7d7889') if not day else hx('a29db0'))
    for y in range(100, H, 8):
        R(d, 0, y, W, 1, hx('6b667a') if not day else hx('8e899c'))
        for x in range((y // 8) % 2 * 8, W, 16): R(d, x, y, 1, 8, hx('6b667a') if not day else hx('8e899c'))
    R(d, 0, 100, W, 2, hx('4d4859'))
    # building
    R(d, 8, 22, 74, 78, hx('f2efe6')); d.rectangle([7, 21, 82, 100], outline=INK)
    for y in range(24, 100, 4): R(d, 9, y, 72, 1, hx('e6e2d6'))
    sg = shade(GREEN, 0.55 + 0.45 * sign_on)
    R(d, 8, 26, 74, 12, sg); R(d, 8, 38, 74, 2, YELLOW); R(d, 8, 26, 74, 1, shade(sg, 1.3))
    # awning
    for x in range(8, 82, 6):
        R(d, x, 42, 3, 4, GREEN); R(d, x + 3, 42, 3, 4, hx('ffffff'))
    for x in range(8, 82, 3): R(d, x, 46, 2, 1, GREEN if (x // 3) % 2 else hx('ffffff'))
    for wx in (11, 55):
        R(d, wx, 50, 24, 36, hx('9fd3e0') if day else hx('ffe9a8')); d.rectangle([wx - 1, 49, wx + 24, 86], outline=INK)
        for sy in (60, 71, 82):
            R(d, wx, sy, 24, 1, hx('6aa9b8') if day else hx('c9a858'))
            for bx in range(wx + 2, wx + 22, 4): R(d, bx, sy - 4, 3, 4, hx(['d9453b', '3066B5', 'F7CD00', '227C4C', 'f2f2f2'][(bx + sy) % 5]))
        R(d, wx + 2, 51, 6, 1, hx('ffffff'))
    R(d, 38, 52, 14, 48, hx('2f5a4a')); R(d, 39, 54, 12, 46, hx('a8dbe6') if day else hx('ffe9a8')); R(d, 49, 76, 1, 4, INK)
    for px in (36, 52):  # plants
        R(d, px, 94, 4, 5, hx('b5653a')); R(d, px - 1, 89, 6, 5, hx('4fa86a')); R(d, px + 1, 87, 2, 3, hx('7bd389'))
    # cross sign
    R(d, 73, 4, 13, 13, hx('ffffff')); d.rectangle([72, 3, 86, 17], outline=INK)
    cc = GREEN if sign_on > .5 else shade(GREEN, .6)
    R(d, 78, 6, 3, 9, cc); R(d, 75, 9, 9, 3, cc); R(d, 79, 17, 2, 5, hx('4d4859'))
    # lamp post
    R(d, 2, 60, 2, 40, hx('2a2a38')); R(d, 1, 58, 5, 3, hx('2a2a38')); R(d, 2, 61, 3, 1, hx('fff0a0'))
    if rain:
        rnd = random.Random(int(t * 20))
        for i in range(60):
            x, y = rnd.randrange(W), rnd.randrange(H)
            R(d, x, y, 1, 3, (160, 190, 245))
        for i in range(10):
            x, y = rnd.randrange(W), rnd.randrange(104, H)
            R(d, x - 1, y, 3, 1, (190, 210, 250))
    if not day:
        Ls = [(3, 62, 30, .9, (1, .85, .5)), (23, 70, 26, .6 * sign_on, (1, .9, .6)), (67, 70, 26, .6 * sign_on, (1, .9, .6)),
              (45, 32, 40, .5 * sign_on, (.3, 1, .5)), (79, 10, 14, .6 * sign_on, (.4, 1, .6))]
        im = light(im, (.5, .52, .7), Ls)
    return im, ImageDraw.Draw(im)

def apotek_int(t):
    im = Image.new('RGBA', (W, H), hx('e3efe6')); d = ImageDraw.Draw(im)
    for x in range(0, W, 8): R(d, x, 0, 4, 100, hx('d8e8dd'))
    R(d, 0, 0, W, 4, hx('cfdcd3'))
    for lx in (20, 66): R(d, lx - 6, 4, 12, 2, hx('fffbe0'))
    rnd = random.Random(7)
    for sy in (22, 40, 58):
        R(d, 4, sy, 82, 2, hx('8b5a3c')); R(d, 4, sy + 2, 82, 1, hx('5a3d2c'))
        x = 6
        while x < 84:
            w = rnd.choice([3, 4, 5]); h = rnd.choice([6, 7, 8, 9])
            c = hx(rnd.choice(['d9453b', '3066B5', 'F7CD00', '227C4C', 'f2f2f2', 'f29bb2', '9b6bd6']))
            R(d, x, sy - h, w, h, c); R(d, x, sy - h, 1, h, shade(c, 1.2)); R(d, x, sy - h + 2, w, 1, hx('ffffff') if c != hx('f2f2f2') else BLUE)
            x += w + 1
    R(d, 4, 6, 82, 2, hx('8b5a3c'))
    R(d, 0, 100, W, H - 100, hx('d9d4c7'))
    for y in range(100, H, 10):
        for x in range((y // 10) % 2 * 10, W, 20): R(d, x, y, 10, 10, hx('cbc5b6'))
    return im, d

def counter(d):
    R(d, 30, 80, 60, 4, GREEN); R(d, 30, 80, 60, 1, hx('3aa86a')); R(d, 30, 84, 60, 18, hx('f7f7f2'))
    d.rectangle([29, 79, 90, 102], outline=INK); R(d, 30, 92, 60, 3, GREEN)
    R(d, 57, 86, 6, 2, GREEN); R(d, 59, 84, 2, 6, GREEN)
    R(d, 76, 70, 10, 8, hx('2a2a38')); R(d, 77, 71, 8, 6, hx('7fc4ff')); R(d, 80, 78, 2, 2, hx('2a2a38'))

def logo_k(d, cx, cy, r=8):
    d.ellipse([cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hx('e0221b'))
    d.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=hx('e0221b'), outline=INK)
    for j, row in enumerate(["X..X", "X.X.", "XX..", "X.X.", "X..X"]):
        for i, c in enumerate(row):
            if c == 'X': R(d, cx - 2 + i, cy - 2 + j, 1, 1, INK)

def bubble(d, x, y, w, h, tail_x):
    R(d, x, y, w, h, hx('ffffff')); d.rectangle([x - 1, y - 1, x + w, y + h], outline=INK)
    d.polygon([(tail_x, y + h), (tail_x + 4, y + h), (tail_x + 1, y + h + 4)], fill=hx('ffffff'))
    d.line([(tail_x, y + h), (tail_x + 1, y + h + 4), (tail_x + 4, y + h)], fill=INK)

def microscope(t):
    im = Image.new('RGBA', (W, H), hx('0c1220')); d = ImageDraw.Draw(im)
    cx, cy, r = 45, 64, 42
    d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=hx('3b4656'))
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=hx('6b7a8c'))
    for rr in range(r, 0, -3):
        c = shade(hx('1e5262'), 0.75 + 0.35 * (1 - rr / r))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=c)
    rnd = random.Random(5)
    for i in range(12):
        a = rnd.random() * 6.28; rr = rnd.random() * (r - 8)
        x0, y0 = cx + math.cos(a) * rr, cy + math.sin(a) * rr; s = rnd.randrange(3, 7)
        d.ellipse([x0, y0 + math.sin(t + i) * 1, x0 + s, y0 + s + math.sin(t + i)], fill=hx('2a6878'))
    return im, d, (cx, cy, r)

# ---------------- camera ----------------
def camera(world, zoom=1.0, fx=W / 2, fy=H / 2, shake=0.0, t=0):
    zoom = max(1.0, zoom)
    w, h = W / zoom, H / zoom
    x0 = min(max(fx - w / 2, 0), W - w); y0 = min(max(fy - h / 2, 0), H - h)
    if shake:
        rnd = random.Random(int(t * 30)); x0 += rnd.uniform(-shake, shake) / zoom; y0 += rnd.uniform(-shake, shake) / zoom
        x0 = min(max(x0, 0), W - w); y0 = min(max(y0, 0), H - h)
    return world.convert('RGB').resize((FW, FH), Image.NEAREST, box=(x0, y0, x0 + w, y0 + h)), (x0, y0, zoom)

def w2s(cam, x, y):
    x0, y0, z = cam; return ((x - x0) * S * z, (y - y0) * S * z)

# ---------------- HUD layer ----------------
def _mk_scan():
    ov = Image.new('RGBA', (FW, FH), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(0, FH, 6): d.rectangle([0, y, FW, y + 1], fill=(0, 0, 0, 34))
    a = np.zeros((FH, FW), np.float32)
    yy, xx = np.mgrid[0:FH, 0:FW]
    dd = np.sqrt(((xx - FW / 2) / (FW * .62)) ** 2 + ((yy - FH / 2) / (FH * .62)) ** 2)
    vig = (np.clip(dd - .55, 0, 1) * 200).astype(np.uint8)
    v = Image.fromarray(np.dstack([np.zeros_like(vig)] * 3 + [vig]), 'RGBA')
    return Image.alpha_composite(ov, v)
SCAN = None

def tstroke(dr, xy, s, f, fill, st=6, anchor='la'):
    dr.text(xy, s, font=f, fill=fill, stroke_width=st, stroke_fill=INK, anchor=anchor)

def card(img, lt, title, sub, y=1330, accent=YELLOW):
    dr = ImageDraw.Draw(img)
    u = ease(lt / 0.28); x0 = int(-1000 + 1060 * u); x1 = x0 + 960
    dr.rectangle([x0 - 6, y - 6, x1 + 6, y + 222], fill=INK)
    dr.rectangle([x0, y, x1, y + 216], fill=CREAM)
    dr.rectangle([x0 + 8, y + 8, x1 - 8, y + 208], fill=NAVY)
    dr.rectangle([x0 + 8, y + 8, x0 + 24, y + 208], fill=accent)
    tstroke(dr, (x0 + 56, y + 44), title, font(F_TITLE, 46), accent, 4)
    n = int(len(sub) * min(1, max(0, (lt - 0.3) / 0.5)))
    dr.text((x0 + 56, y + 122), sub[:n], font=font(F_BODY2, 54), fill=(240, 240, 240))

def brand_tag(img):
    dr = ImageDraw.Draw(img); f = font(F_BODY, 34); s = "APOTEK BERKAH SEHAT"; w = dr.textlength(s, font=f)
    dr.rectangle([42, 214, 42 + w + 48, 274], fill=INK); dr.rectangle([46, 218, 38 + w + 48, 270], fill=GREEN)
    dr.rectangle([46, 218, 54, 270], fill=YELLOW); dr.text((70, 222), s, font=f, fill=(255, 255, 255))

def label(img, xy, s, size=34, fill=(255, 255, 255), f=F_BODY):
    tstroke(ImageDraw.Draw(img), xy, s, font(f, size), fill, 5, 'mm')

def big_text(img, lt, at, lines, y=470, size=66, col=(255, 255, 255)):
    dr = ImageDraw.Draw(img)
    for i, (s, c) in enumerate(lines):
        sc = pop(lt, at + i * .12, .3)
        if sc <= 0: continue
        tstroke(dr, (540, y + i * size * 1.45), s, font(F_TITLE, size * sc), c or col, 9, 'mm')

# ---------------- scenes (lt = local time) ----------------
def sc_hook(lt):  # 0 - 2.6  "Udah enakan kok"
    im, d = bedroom(lt); nightstand(im, d)
    person(im, RAKA, 62, 104, lt, happy=True)
    strip(d, 76, 88, used=4)
    im = night_light(im, lt)
    big, cam = camera(im, 1.9 - 0.15 * eio(lt / 2.6), 70, 88)
    big = big.convert('RGBA')
    big_text(big, lt, 0.15, [("\"UDAH", None), ("ENAKAN", YELLOW), ("KOK.\"", None)], y=330, size=78)
    return big

def sc_stop(lt):  # 2.6 - 4.45  "stop minum"
    im, d = bedroom(lt + 3)
    op = 6 - 6 * ease((lt - .9) / .25) if lt > .9 else 6
    nightstand(im, d, drawer=op)
    person(im, RAKA, 62, 104, lt, happy=lt < 1.2)
    if lt < .9:
        u = ease(lt / .9); sx = 76 - 22 * u; sy = 88 - 14 * math.sin(u * math.pi) - 2 * u
        strip(d, int(sx), int(sy), used=4)
    im = night_light(im, lt)
    big, cam = camera(im, 1.4, 56, 86)
    big = big.convert('RGBA')
    if lt > .25: big_text(big, lt, .25, [("STOP", RED), ("MINUM.", None)], y=360, size=84)
    return big

def sc_week(lt):  # 4.45 - 8.1  "Seminggu kemudian batuknya balik. Lebih parah."
    TEAR = max(1.0, T(5.14) - M(4.45))
    if lt < TEAR:  # calendar tear
        im = Image.new('RGBA', (W, H), hx('3a3358')); d = ImageDraw.Draw(im)
        day = min(7, int(lt / TEAR * 7) + 1)
        R(d, 12, 30, 66, 80, hx('f6f1e3')); d.rectangle([11, 29, 78, 110], outline=INK); R(d, 12, 30, 66, 16, hx('d9453b'))
        for hxp in (24, 64): R(d, hxp, 26, 3, 7, hx('6b737c'))
        frac = (lt / TEAR * 7) % 1
        if frac < .5 and day < 8:
            R(d, 12 + int(frac * 30), 46 - int(frac * 20), 66, 64, hx('ece5d2'))
        im = light(im, (.85, .85, .9), [])
        big, cam = camera(im, 1.0)
        big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
        tstroke(dr, (540, 1000), f"+{day}", font(F_TITLE, 210), INK, 0, 'mm')
        tstroke(dr, (540, 1170), "HARI", font(F_TITLE, 60), hx('d9453b'), 0, 'mm')
        label(big, (540, 330), "SEMINGGU KEMUDIAN", 64, YELLOW, F_TITLE)
        return big
    l2 = lt - TEAR; HARD = T(6.62) - M(4.45) - TEAR
    im, d = bedroom(lt + 8); nightstand(im, d)
    for x, y in ((24, 108), (34, 113), (80, 110), (70, 118)): R(d, x, y, 4, 3, hx('ffffff')); d.rectangle([x - 1, y - 1, x + 4, y + 3], outline=INK)
    hard = l2 > HARD
    person(im, RAKA, 62, 104, l2, sick=True, cough=True)
    im = night_light(im, lt, lamp=True)
    big, cam = camera(im, 1.25 + (.35 * ease((l2 - HARD) / .4) if hard else 0), 66, 90, shake=(5 if hard else 2), t=lt)
    big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    if hard:
        a = Image.new('RGBA', big.size, (180, 20, 30, int(60 * (0.5 + 0.5 * math.sin(lt * 18)))))
        big = Image.alpha_composite(big, a)
        big_text(big, l2, HARD, [("LEBIH", None), ("PARAH.", RED)], y=380, size=86)
    else:
        label(big, (700, 560), "UHUK! UHUK!", 54, (255, 255, 255), F_TITLE)
    return big

def sc_rewind(lt, prev_frame):  # 8.1 - 9.3 "Kok bisa?"
    im, d = bedroom(9.0 - lt * 6); nightstand(im, d)
    person(im, RAKA, 62 - int(lt * 10) % 3, 104, 3 - lt, sick=True)
    im = night_light(im, lt)
    big, _ = camera(im, 1.25, 60, 90)
    a = np.asarray(big).copy()
    rnd = random.Random(int(lt * 30))
    for _ in range(9):  # tracking bands
        y = rnd.randrange(0, FH - 60); h = rnd.randrange(8, 60); s = rnd.randrange(-80, 80)
        a[y:y + h] = np.roll(a[y:y + h], s, axis=1)
    a[..., 0] = np.roll(a[..., 0], 8, axis=1); a[..., 2] = np.roll(a[..., 2], -8, axis=1)
    y = int((lt * 2400) % FH); a[y:y + 40] = np.clip(a[y:y + 40].astype(int) + 70, 0, 255)
    big = Image.fromarray(a).convert('RGBA'); dr = ImageDraw.Draw(big)
    tstroke(dr, (90, 300), "<< REW", font(F_TITLE, 58), (255, 255, 255), 6)
    tstroke(dr, (540, 860), "KOK BISA?", font(F_TITLE, 80), YELLOW, 9, 'mm')
    tstroke(dr, (540, 990), "MUNDUR 9 HARI", font(F_TITLE, 46), (255, 255, 255), 7, 'mm')
    tstroke(dr, (90, 1640), f"00:{int(59 - lt * 40):02d}:{int((lt * 997) % 60):02d}", font(F_TITLE, 36), (255, 255, 255), 5)
    return big

def sc_drawer(lt):  # 9.3 - 12.95 "Awalnya cuma pilek, Raka nemu antibiotik sisa punya kakaknya"
    im, d = bedroom(lt + 9)
    op = ease((lt - 1.0) / .6) * 6; nightstand(im, d, drawer=op)
    person(im, RAKA, 62, 104, lt, sick=True, seed=1)
    yy = None
    if lt > 1.6:
        yy = int(76 - 10 * ease((lt - 1.6) / .6)); strip(d, 49, yy, glow=int(lt * 5) % 2 == 0)
    im = night_light(im, lt, extra=[(56, 70, 16, .8, (1, 1, .6))] if lt > 1.6 else [])
    z = 1.15 + .25 * eio((lt - 1.4) / 1.6)
    big, cam = camera(im, z, 58, 84)
    big = big.convert('RGBA')
    if yy is not None:
        x, y = w2s(cam, 56, yy - 6); label(big, (x, y), "antibiotik sisa", 44, YELLOW)
        x2, y2 = w2s(cam, 56, yy + 12); label(big, (x2, y2), "punya kakak", 36, (255, 255, 255))
    card(big, lt - .2, "AWALNYA", "cuma pilek biasa")
    return big

def sc_cal(lt):  # 12.95 - 16.4 "Diminum dua hari, badan enakan, langsung berhenti"
    im, d = bedroom(lt + 13, calendar_on_wall=True); nightstand(im, d)
    used = 0 + (2 if lt > .3 else 0) + (2 if lt > .6 else 0)
    strip(d, 48, 72, used=used)
    person(im, RAKA, 62, 104, lt, sick=lt < 1.0, happy=1.0 <= lt < 1.9, seed=2)
    im = night_light(im, lt)
    big, cam = camera(im, 1.2, 62, 76)
    big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    marks = [(.3, "V", (60, 170, 90)), (.6, "V", (60, 170, 90)), (1.9, "X", RED), (2.0, "X", RED), (2.1, "X", RED), (2.2, "X", RED), (2.3, "X", RED)]
    for i, (at, m, c) in enumerate(marks):
        col, row = i % 4, i // 4
        x, y = w2s(cam, 58 + col * 6 + 2.5, 17 + row * 7 + 2.5)
        if lt > at: tstroke(dr, (x, y), m, font(F_TITLE, 44 * max(pop(lt, at), .01)), c, 5, 'mm')
    if 1.0 < lt < 1.9: label(big, (540, 1180), "badan enakan :)", 50)
    if lt > 1.9: big_text(big, lt, 1.9, [("BERHENTI", RED)], y=1180, size=70)
    card(big, lt - .1, "DIMINUM 2 HARI", "lalu berhenti sendiri")
    return big

BPOS = [(22, 44), (52, 34), (60, 72), (30, 80), (44, 56), (66, 52)]
VPOS = [(18, 62), (50, 88), (70, 34)]
KILL = [0, 2, 3, 5]
def sc_micro(lt):  # 16.4 - 27.75
    im, d, (cx, cy, r) = microscope(lt)
    ta = int(lt * 10) / 10
    S0 = M(16.4); t_pill = T(19.72) - S0; t_hit = T(22.14) - S0; t_die = T(24.12) - S0; t_strong = T(25.2) - S0; t_kebal = T(26.96) - S0
    for i, (vx, vy) in enumerate(VPOS):
        ox = round(math.sin(ta * 2 + i) * 2); oy = round(math.cos(ta * 1.7 + i) * 2)
        im.alpha_composite(sprite(VIRUS, 'vir'), (vx + ox, vy + oy))
    for i, (bx, by) in enumerate(BPOS):
        ox = round(math.sin(ta * 1.5 + i * 2) * 2); oy = round(math.cos(ta * 1.3 + i))
        if i in KILL:
            k = KILL.index(i); die = t_die + k * .18
            if lt > die:
                if lt < die + .35:
                    rr = (lt - die) * 30
                    for a in range(8): R(d, int(bx + 4 + math.cos(a * .785) * rr), int(by + 3 + math.sin(a * .785) * rr), 1, 1, hx('f4e7b0'))
                continue
        arm = lt > t_kebal
        spr = sprite(BACT_ARM, 'arm') if arm else sprite(BACT, 'bac')
        im.alpha_composite(spr, (bx + ox, by + oy))
        if t_strong < lt < t_kebal and i not in KILL and int(lt * 8) % 2:
            d.rectangle([bx + ox - 2, by + oy - 2, bx + ox + 11, by + oy + 9], outline=YELLOW)
    # pills: first through viruses (no effect), then into bacteria
    for k, (vx, vy) in enumerate(VPOS):
        t0 = t_pill + k * .25
        if t0 < lt < t0 + .9:
            u = (lt - t0) / .9; px, py = vx + 4, int(-6 + (vy + 24) * u)
            R(d, px, py, 2, 2, hx('d9453b')); R(d, px, py + 2, 2, 2, YELLOW)
    for k, i in enumerate(KILL):
        t0 = t_hit + k * .3; bx, by = BPOS[i]
        if t0 < lt < t_die + k * .18:
            u = min(1, (lt - t0) / .7); px, py = bx + 4, int(-6 + (by + 9) * u)
            R(d, px, py, 2, 2, hx('d9453b')); R(d, px, py + 2, 2, 2, YELLOW)
    glow = [(cx, cy, r, .35, (.2, .5, .5))]
    if lt > t_kebal: glow.append((45, 60, 30, .5 * (.5 + .5 * math.sin(lt * 12)), (1, .2, .2)))
    im = light(im, (1, 1, 1), glow)
    z = 1.06 + .06 * math.sin(lt * .6)
    big, cam = camera(im, z, 45 + 3 * math.sin(lt * .4), 64)
    big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    if lt < t_hit:
        x, y = w2s(cam, VPOS[0][0] + 5, VPOS[0][1] - 4); label(big, (x, y), "VIRUS", 40, hx('d2b4f7'), F_TITLE)
        x, y = w2s(cam, BPOS[4][0] + 5, BPOS[4][1] - 4); label(big, (x, y), "BAKTERI", 34, hx('9be8a8'), F_TITLE)
    if t_pill < lt < t_hit: label(big, (540, 300), "ANTIBIOTIK MASUK", 48, YELLOW, F_TITLE)
    if T(20.48) - S0 < lt < t_hit:
        big_text(big, lt, T(20.48) - S0, [("TIDAK", (255, 255, 255)), ("MEMPAN", RED)], y=1060, size=70)
    if t_die < lt < t_kebal: label(big, (540, 300), "yang lemah mati", 56, (255, 255, 255))
    if t_strong < lt < t_kebal: label(big, (540, 380), "yang kuat bertahan", 56, YELLOW)
    if lt > t_kebal:
        big_text(big, lt, t_kebal, [("LEVEL UP!", YELLOW)], y=330, size=86)
        card(big, lt - t_kebal, "BAKTERI KEBAL", "antibiotik makin sulit bekerja", accent=RED)
    elif lt < t_hit:
        card(big, lt - .1, "MASALAHNYA", "pilek umumnya karena virus")
    else:
        card(big, lt - t_hit, "YANG KENA", "justru bakteri")
    return big

def sc_street(lt):  # 27.75 - 31.25
    sign = 1.0 if lt > T(29.74) - M(27.75) else (0.25 if int(lt * 12) % 3 else 0.7)
    im, d = apotek_ext(lt, rain=True, sign_on=sign)
    x = -14 + 46 * ease(lt / 3.0)
    person(im, RAKA, x, 110, lt, sick=True, walk=lt < 3.0, seed=3)
    big, cam = camera(im, 1.15, 20 + 25 * eio(lt / 3), 80)
    big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    x, y = w2s(cam, 45, 32); dr.text((x, y), "APOTEK BERKAH SEHAT", font=font(F_TITLE, 39), fill=YELLOW if sign > .5 else shade(YELLOW, .5), anchor='mm', stroke_width=3, stroke_fill=INK)
    if lt > .3: label(big, (540, 1560), "akhirnya ke apotek...", 54, (255, 255, 255))
    return big

def sc_consult(lt):  # 31.25 - 36.3
    im, d = apotek_int(lt)
    person(im, APT, 58, 88, lt, talk=lt > .1, seed=4); counter(d)
    person(im, RAKA, 8, 112, lt, sick=True, seed=5)
    tk = T(33.38) - M(31.25)
    if lt > tk - .3:
        s = pop(lt, tk - .3, .3)
        bubble(d, 24, 42, 30, 24, 46); logo_k(d, 39, 54, max(1, int(9 * min(s, 1.15))))
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    z = 1.05 + .2 * eio(lt / 5)
    big, cam = camera(im, z, 46, 70)
    big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    if lt > tk:
        x, y = w2s(cam, 39, 37); tstroke(dr, (x, y), "OBAT KERAS", font(F_TITLE, 40), hx('e0221b'), 6, 'mm')
    if lt > T(34.34) - M(31.25):
        big_text(big, lt, T(34.34) - M(31.25), [("WAJIB RESEP", (255, 255, 255)), ("DOKTER", YELLOW)], y=1090, size=58)
    card(big, lt - .1, "KATA APOTEKER", "antibiotik = obat keras")
    return big

ICONS = {
 'virus': VIRUS,
 'rx': ["WWWWWWW.", "WKKWWWW.", "WKWKWWW.", "WKKWWWW.", "WKWKWWW.", "WWWWWWW.", "WRRRRRW.", "WWWWWWW."],
 'clock': ["..YYYY..", ".YWWWWY.", "YWWKWWWY", "YWWKWWWY", "YWWKKKWY", "YWWWWWWY", ".YWWWWY.", "..YYYY.."],
 'strip': ["XX....XX", ".XX..XX.", "..XXXX..", "...XX...", "..XXXX..", ".XX..XX.", "XX....XX", "........"],
}
ITEMS = [("Flu & pilek umumnya", "karena virus", 'virus'), ("Antibiotik harus", "pakai resep dokter", 'rx'),
         ("Minum sesuai aturan", "jangan berhenti sendiri", 'clock'), ("Jangan pakai sisa", "atau punya orang lain", 'strip')]
def sc_list(lt):  # 36.3 - 51.1
    base = M(36.3); times = [T(38.14) - base, T(40.84) - base, T(43.68) - base, T(47.34) - base]
    im, d = apotek_int(lt); person(im, APT, 58, 88, lt, talk=True, seed=4); counter(d)
    im = light(im, (.35, .33, .45), [])
    big, cam = camera(im, 1.1, 45, 70); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    u = ease(lt / .4); y0 = int(300 + (1 - u) * 1600)
    dr.rectangle([54, y0 - 6, 1026, y0 + 1286], fill=INK); dr.rectangle([60, y0, 1020, y0 + 1280], fill=hx('fff7dc'))
    dr.rectangle([60, y0, 1020, y0 + 190], fill=GREEN); dr.rectangle([60, y0 + 190, 1020, y0 + 202], fill=YELLOW)
    dr.text((540, y0 + 64), "4 HAL PENTING", font=font(F_TITLE, 52), fill=YELLOW, anchor='mm', stroke_width=4, stroke_fill=INK)
    dr.text((540, y0 + 140), "sebelum minum antibiotik", font=font(F_BODY, 50), fill=(255, 255, 255), anchor='mm')
    for i, ((a, b, ic), at) in enumerate(zip(ITEMS, times)):
        yy = y0 + 250 + i * 255
        active = lt > at and (i == 3 or lt < times[i + 1])
        if lt < at:
            dr.rectangle([110, yy, 240, yy + 130], outline=hx('e2d6b4'), width=4)
            dr.text((175, yy + 68), str(i + 1), font=font(F_TITLE, 52), fill=hx('e2d6b4'), anchor='mm'); continue
        sc = pop(lt, at, .3); ox = int((1 - ease((lt - at) / .3)) * 200)
        if active: dr.rectangle([70, yy - 18, 1010, yy + 186], fill=hx('fdecb0'))
        bs = 130; bx = 110 + ox
        dr.rectangle([bx - 4, yy - 4, bx + bs + 4, yy + bs + 4], fill=INK)
        dr.rectangle([bx, yy, bx + bs, yy + bs], fill=RED if i in (0, 3) else BLUE)
        ics = sprite(ICONS[ic], 'ic' + ic).resize((int(10 * 10 * max(sc, .01) / 1.0),) * 2, Image.NEAREST)
        big.alpha_composite(ics, (bx + bs // 2 - ics.width // 2, yy + bs // 2 - ics.height // 2))
        tstroke(dr, (bx + bs - 4, yy + 4), str(i + 1), font(F_TITLE, 34), (255, 255, 255), 5, 'ra')
        dr.text((290 + ox, yy + 6), a, font=font(F_BODY, 56), fill=NAVY)
        dr.text((290 + ox, yy + 76), b, font=font(F_BODY2, 46), fill=hx('5a5064'))
    return big

def sc_cta(lt):  # 51.1 - end
    im, d = apotek_ext(lt, day=True)
    person(im, RAKA, 16, 106, lt, happy=True, seed=6); person(im, APT, 58, 106, lt, seed=7)
    rnd = random.Random(1)
    for i in range(26):
        x = rnd.randrange(W); sp = rnd.uniform(8, 16); y = int((rnd.randrange(H) + lt * sp) % 110)
        R(d, x, y, 2, 1, hx(rnd.choice(['F7CD00', '227C4C', '3066B5', 'e0483e', 'ffffff'])))
    big, cam = camera(im, 1.0 + .08 * eio(lt / 6), 45, 70); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    x, y = w2s(cam, 45, 32); dr.text((x, y), "APOTEK BERKAH SEHAT", font=font(F_TITLE, 36), fill=YELLOW, anchor='mm', stroke_width=3, stroke_fill=INK)
    x, y = w2s(cam, 24, 74); label(big, (x, y), "sudah sehat!", 40, YELLOW)
    u = ease((lt - .3) / .4); y = int(1300 + (1 - u) * 700)
    dr.rectangle([54, y - 6, 1026, y + 356], fill=INK); dr.rectangle([60, y, 1020, y + 350], fill=GREEN); dr.rectangle([60, y, 1020, y + 12], fill=YELLOW)
    dr.text((540, y + 74), "RAGU SOAL OBAT?", font=font(F_TITLE, 52), fill=YELLOW, anchor='mm', stroke_width=4, stroke_fill=INK)
    dr.text((540, y + 156), "Tanya apoteker kami", font=font(F_BODY, 56), fill=(255, 255, 255), anchor='mm')
    dr.text((540, y + 236), "Jl. Sunan Muria No. 24, Kudus", font=font(F_BODY2, 44), fill=hx('ebf5ee'), anchor='mm')
    dr.text((540, y + 300), "WA 0821-3626-9724", font=font(F_BODY, 48), fill=YELLOW, anchor='mm')
    return big

_B = [0, M(2.6), M(4.45), M(8.1), M(9.3), M(12.95), M(16.4), M(27.75), M(31.25), M(36.3), M(51.1), TOTAL]
_F = [sc_hook, sc_stop, sc_week, None, sc_drawer, sc_cal, sc_micro, sc_street, sc_consult, sc_list, sc_cta]
SCENES = [(_B[i], _B[i + 1], _F[i]) for i in range(len(_F))]
NO_WIPE = {_B[3], _B[4]}

def wipe(img, u, inward):
    """pixel block diagonal wipe; u 0..1 coverage"""
    if u <= 0: return img
    dr = ImageDraw.Draw(img); bs = 72
    for by in range(0, FH, bs):
        for bx in range(0, FW, bs):
            k = (bx / FW + by / FH) / 2
            if (k < u) if not inward else (k > 1 - u): dr.rectangle([bx, by, bx + bs - 1, by + bs - 1], fill=INK)
    return img

def frame(t):
    global SCAN
    if SCAN is None: SCAN = _mk_scan()
    for a, b, fn in SCENES:
        if a <= t < b:
            lt = t - a
            img = sc_rewind(lt, None) if fn is None else fn(lt)
            img = img.convert('RGBA')
            if a not in NO_WIPE and lt < .2 and a > 0: img = wipe(img, 1 - lt / .2, True)
            if b not in NO_WIPE and b - t < .2 and b < TOTAL: img = wipe(img, 1 - (b - t) / .2, False)
            if t > TOTAL - .6: img = ImageEnhance.Brightness(img).enhance(max(0, (TOTAL - t) / .6))
            img = Image.alpha_composite(img, SCAN)
            brand_tag(img)
            return img.convert('RGB')
    return Image.new('RGB', (FW, FH))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]): frame(tt).save(f"v2_{tt:05.2f}.png")
        sys.exit()
    out = sys.argv[1]
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 300 == 0: print(i, '/', n, flush=True)
    p.stdin.close(); p.wait(); print('done')
