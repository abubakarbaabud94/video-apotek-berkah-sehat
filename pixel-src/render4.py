#!/usr/bin/env python3
"""Episode 2 - Obat herbal vs farmasi. Reuses the render2 engine (world/camera/HUD/scanlines),
new scenes synced to word timestamps of the supplied VO (vo time = video time - O)."""
import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
import render2 as R2
from render2 import *   # W,H,S,FW,FH,FPS, R, ease, eio, pop, shade, sprite, person, camera, w2s, card, label, big_text, tstroke, brand_tag, wipe, light, apotek_int, counter, bubble, fonts, colors

O = 0.3
TOTAL = 66.0
PAL['O'] = hx('e8892b'); PAL['N'] = hx('b5651d'); PAL['C'] = hx('d6dde3')

LEAF = ["...LLLLL...", ".LLLLLLLLL.", "LLLlLLLlLLL", "LLLLLLLLLLL", ".LLLLLLLLL.", "..LLLLLLL..", "....LLL....", ".....g.....", ".....g....."]
ROOT = [".OOOO.......", "OOOOOOOO....", "ONOOOOOOOO..", ".OOONOOOOOO.", "..OOOOOOONO.", "....OOOOOO.."]
BOTTLE = ["..DDDD..", "..DDDD..", ".CCCCCC.", "CCCCCCCC", "CWWWWWWC", "CWKKKKWC", "CWWWWWWC", "CWKKKKWC", "CWWWWWWC", "CCCCCCCC", "CCCCCCCC"]
CAPS = [".RRRWWW.", "RRRRWWWW", "RRRRWWWW", ".RRRWWW."]
DROP = ["..X..", ".XXX.", "XXXXX", "XXXXX", ".XXX."]
JAMU = [r.replace('G', 'R').replace('g', 'r').replace('j', 'q').replace('W', 'Y').replace('w', 'Y') for r in APT]

def sp(im, rows, key, x, y, swap=None, k=1, flip=False):
    s = sprite(rows, key, swap)
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    if k != 1: s = s.resize((s.width * k, s.height * k), Image.NEAREST)
    im.paste(s, (int(x), int(y)), s)
    return s.size

def stamp(big, cx, cy, text, size, col, angle, shake=0):
    f = font(F_TITLE, size); tmp = Image.new('RGBA', (1500, 420), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    td.text((750, 210), text, font=f, fill=col + (255,), anchor='mm')
    w = int(td.textlength(text, font=f)) + 70; h = int(size) + 60
    td.rectangle([750 - w // 2, 210 - h // 2, 750 + w // 2, 210 + h // 2], outline=col + (255,), width=14)
    tmp = tmp.rotate(angle, resample=Image.NEAREST)
    ox = random.Random(int(cx + cy + shake * 7)).randint(-shake, shake) if shake else 0
    big.paste(tmp, (int(cx - 750 + ox), int(cy - 210)), tmp)

def fit(dr, s, maxw, size, path=None):
    path = path or F_BODY
    while size > 18 and dr.textlength(s, font=font(path, size)) > maxw: size -= 2
    return font(path, size)

# ---------------- worlds ----------------
def kitchen(t):
    im = Image.new('RGBA', (W, H), hx('eadcb0')); d = ImageDraw.Draw(im)
    for y in range(0, 66, 8):
        for x in range((y // 8) % 2 * 4, W, 8): R(d, x, y + 3, 2, 1, hx('d8c78f'))
    R(d, 0, 66, W, 34, hx('7fb69a')); R(d, 0, 66, W, 2, hx('a5d6bb'))
    for x in range(0, W, 12): R(d, x, 69, 1, 29, hx('6ea489'))
    R(d, 6, 8, 28, 32, hx('8b5a3c')); R(d, 8, 10, 24, 28, hx('a8def5')); R(d, 19, 10, 2, 28, hx('8b5a3c')); R(d, 8, 23, 24, 2, hx('8b5a3c'))
    d.ellipse([10, 28, 22, 40], fill=hx('5cbf6d')); d.ellipse([20, 30, 30, 40], fill=hx('3f9a55'))
    R(d, 44, 34, 42, 2, hx('6e4630')); R(d, 44, 36, 42, 1, hx('4a2f20'))
    for i, c in enumerate(['O', 'R', 'G', 'Y', 'O', 'G']): sp(im, BOTTLE, 'sh', 46 + i * 6, 21, {'C': c})
    for i, x in enumerate((50, 62, 74)):
        R(d, x, 6, 1, 6, hx('6e4630')); sp(im, LEAF, 'hl', x - 5, 11 + (i % 2) * 2)
    R(d, 0, 84, W, 16, hx('b07a52')); R(d, 0, 84, W, 3, hx('d29c6a')); R(d, 0, 100, W, 1, hx('6e4630'))
    R(d, 0, 101, W, H - 101, hx('8b5a3c'))
    for y in range(101, H, 7): R(d, 0, y, W, 1, hx('6e4630'))
    R(d, 8, 76, 10, 8, hx('b5653a')); sp(im, LEAF, 'pt', 7, 66)
    return im, d

def garden(t):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    top, bot = hx('8fd3f4'), hx('e9f7d8')
    for y in range(100):
        u = y / 100; R(d, 0, y, W, 1, tuple(int(top[i] * (1 - u) + bot[i] * u) for i in range(3)))
    d.ellipse([-20, 70, 60, 130], fill=hx('9bd68b')); d.ellipse([30, 76, 120, 140], fill=hx('86c777'))
    for tx, th in ((8, 30), (76, 36)):
        R(d, tx, 100 - th // 2, 4, th // 2, hx('6e4630')); d.ellipse([tx - 9, 100 - th - 6, tx + 13, 100 - th // 2 + 4], fill=hx('3f9a55'))
        d.ellipse([tx - 5, 100 - th - 10, tx + 9, 100 - th // 2 - 2], fill=hx('5cbf6d'))
    R(d, 0, 100, W, H - 100, hx('6fbf73'))
    for y in range(102, H, 6):
        for x in range((y // 6) % 2 * 5, W, 10): R(d, x, y, 2, 1, hx('5aa862'))
    d.polygon([(30, 100), (60, 100), (88, H), (2, H)], fill=hx('e0cf9a'))
    rnd = random.Random(2)
    for i in range(16):
        x = (rnd.randrange(W) + math.sin(t * 1.4 + i) * 4) % W; y = (rnd.randrange(H) + t * (6 + i % 4)) % H
        R(d, int(x), int(y), 2, 1, hx('2f8f4a'))
    return im, d

def bench(t):
    im = Image.new('RGBA', (W, H), hx('1d3a45')); d = ImageDraw.Draw(im)
    for y in range(0, 100, 8): R(d, 0, y, W, 1, hx('26505e'))
    for x in range(0, W, 10): R(d, x, 0, 1, 100, hx('26505e'))
    R(d, 0, 96, W, H - 96, hx('8b5a3c')); R(d, 0, 96, W, 3, hx('b07a52'))
    for y in range(102, H, 8): R(d, 0, y, W, 1, hx('6e4630'))
    return im, d

def scanlab(t):
    im = Image.new('RGBA', (W, H), hx('0b1020')); d = ImageDraw.Draw(im)
    for y in range(0, H, 8): R(d, 0, y, W, 1, hx('141c38'))
    for x in range(0, W, 8): R(d, x, 0, 1, H, hx('141c38'))
    R(d, 0, 112, W, 10, hx('2b3350')); R(d, 0, 112, W, 1, hx('3d4870'))
    for x in range(-(int(t * 12) % 8), W, 8): R(d, x, 116, 3, 2, hx('1b2240'))
    R(d, 14, 50, 4, 62, hx('4a5280')); R(d, 72, 50, 4, 62, hx('4a5280')); R(d, 14, 46, 62, 5, hx('4a5280')); R(d, 14, 46, 62, 1, hx('6a74a8'))
    return im, d

def stage(t):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        u = y / H; R(d, 0, y, W, 1, (int(40 + 30 * u), int(24 + 10 * u), int(70 + 30 * u)))
    for y in range(100, H, 6): R(d, 0, y, W, 1, hx('4a3a78'))
    for x in range(-60, 150, 12): d.line([(45 + (x - 45) * .2, 100), (x, H)], fill=hx('4a3a78'))
    return im, d

# ---------------- HUD helpers ----------------
def check_row(big, c, y, title, sub, col=GREEN):
    if c < 0: return
    dr = ImageDraw.Draw(big); ox = int((1 - ease(c / .3)) * 700)
    x0 = 70 + ox; x1 = 1010 + ox
    dr.rectangle([x0 - 6, y - 6, x1 + 6, y + 170], fill=INK); dr.rectangle([x0, y, x1, y + 164], fill=CREAM)
    dr.rectangle([x0, y, x0 + 18, y + 164], fill=col)
    bx = x0 + 50; dr.rectangle([bx, y + 32, bx + 100, y + 132], fill=col, outline=INK, width=5)
    dr.line([(bx + 20, y + 84), (bx + 42, y + 108), (bx + 82, y + 54)], fill=(255, 255, 255), width=14)
    dr.text((x0 + 190, y + 34), title, font=font(F_TITLE, 40), fill=INK)
    dr.text((x0 + 190, y + 98), sub, font=font(F_BODY2, 46), fill=hx('4a4358'))

def title_lines(big, vt, at, lines, y=330, size=60):
    big_text(big, vt, at, lines, y=y, size=size)

# ---------------- scenes (t = video time, lt = local time) ----------------
def sc_hook(t, lt):
    vt = t - O
    im, d = kitchen(t)
    person(im, RAKA, 37, 122, t, talk=0.2 < vt < 3.5, seed=1)
    sp(im, BOTTLE, 'jb', 49, 108 + int(math.sin(t * 3)), {'C': 'O'})
    im = light(im, (1, .98, .92), [(45, 40, 60, .35, (1, .9, .6))])
    big, cam = camera(im, 1.5 - .12 * eio(lt / 4.6), 46, 86, shake=(4 if 3.62 < vt < 4.2 else 0), t=t)
    big = big.convert('RGBA')
    big_text(big, vt, 1.38, [("OBAT HERBAL", None)], y=330, size=70)
    big_text(big, vt, 1.84, [("PASTI AMAN?", YELLOW)], y=440, size=70)
    if vt > 3.62:
        big_text(big, vt, 3.62, [("BENARKAH?", RED)], y=1690, size=86)
    return big

def sc_scale(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    im = light(im, (.38, .4, .5), [(45, 60, 50, .9, (1, .95, .8))]); d = ImageDraw.Draw(im)
    cx, cy = 45, 66; L = 24
    tilt = math.sin(lt * 6) * max(0, 1 - lt * .55) * .28
    lx, ly = cx - L * math.cos(tilt), cy - L * math.sin(tilt)
    rx, ry = cx + L * math.cos(tilt), cy + L * math.sin(tilt)
    R(d, cx - 1, cy, 3, 40, hx('6b737c')); R(d, cx - 10, 104, 21, 4, hx('3a3f4a'))
    d.line([(lx, ly), (rx, ry)], fill=hx('c9a24a'), width=2); d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=hx('e0c060'), outline=INK)
    for ex, ey in ((lx, ly), (rx, ry)):
        d.line([(ex, ey), (ex - 9, ey + 14)], fill=hx('c9a24a')); d.line([(ex, ey), (ex + 9, ey + 14)], fill=hx('c9a24a'))
        R(d, ex - 10, ey + 14, 21, 2, hx('e0c060'))
    sp(im, LEAF, 'lf', lx - 12, ly + 3); sp(im, BOTTLE, 'jb', lx + 1, ly + 1, {'C': 'O'})
    sp(im, BOTTLE, 'pb', rx - 10, ry + 1, {'C': 'P'}); sp(im, CAPS, 'cp', rx + 2, ry + 10)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 4.74, [("MARI LIHAT", None), ("FAKTANYA", YELLOW)], y=330, size=66)
    x, y = w2s(cam, lx, ly + 24); label(big, (x, y), "HERBAL", 44, hx('ffd28a'), F_TITLE)
    x, y = w2s(cam, rx, ry + 24); label(big, (x, y), "FARMASI", 44, hx('9fd0ff'), F_TITLE)
    return big

def sc_pros(t, lt):
    vt = t - O
    im, d = garden(t)
    person(im, RAKA, 8, 126, t, happy=True, seed=1)
    person(im, JAMU, 36, 124, t, talk=True, seed=8)
    R(d, 54, 114, 16, 10, hx('b5834a')); d.rectangle([53, 113, 70, 124], outline=INK)
    for i, c in enumerate(['R', 'Y', 'G']): sp(im, BOTTLE, 'bk', 55 + i * 5, 102, {'C': c})
    big, cam = camera(im, 1.12 + .03 * math.sin(t), 40, 88); big = big.convert('RGBA')
    big_text(big, vt, 6.86, [("KELEBIHAN", None), ("HERBAL", hx('7bd389'))], y=330, size=70)
    check_row(big, vt - 7.66, 1000, "DARI TANAMAN", "bahan alami dari tumbuhan")
    check_row(big, vt - 9.58, 1200, "TURUN-TEMURUN", "sudah lama dipakai")
    check_row(big, vt - 10.66, 1400, "KELUHAN RINGAN", "bisa jadi pendamping")
    return big

def sc_cons(t, lt):
    vt = t - O
    im, d = bench(t)
    ph = 0 if vt < 17.6 else (1 if vt < 20.3 else 2)
    if ph == 0:
        g = ease((vt - 15.2) / .9)
        for x, lv, col, nm in ((10, .85, hx('7bd389'), "PRODUK A"), (50, .4, hx('e8b84a'), "PRODUK B")):
            sp(im, BOTTLE, 'jb', x, 57, {'C': 'j'}, k=3)
            d.rectangle([x + 8, 14, x + 22, 50], outline=INK, fill=hx('0e1f26'))
            hh = int(34 * lv * g)
            if hh > 0: R(d, x + 9, 50 - hh, 13, hh, col)
    elif ph == 1:
        wob = math.sin(vt * 9) * 2
        d.ellipse([22 + wob, 70, 48 + wob, 82], fill=hx('9aa3ad'), outline=INK); d.ellipse([26 + wob, 66, 44 + wob, 76], fill=hx('e8b84a'))
        d.line([(46 + wob, 78), (74 + wob, 100)], fill=hx('9aa3ad'), width=3)
        sp(im, CAPS, 'cp', 62, 62, None, k=2)
    else:
        R(d, 22, 30, 46, 64, hx('8b5a3c')); R(d, 25, 36, 40, 56, hx('f6f1e3')); R(d, 36, 26, 18, 8, hx('6b737c'))
        for i in range(4):
            d.rectangle([29, 50 + i * 10, 33, 54 + i * 10], outline=INK); R(d, 36, 52 + i * 10, 24, 1, hx('9a9a9a'))
    big, cam = camera(im, 1.25, 45, 70); big = big.convert('RGBA')
    if ph == 0:
        for x, nm in ((10, "PRODUK A"), (50, "PRODUK B")):
            xx, yy = w2s(cam, x + 15, 100); label(big, (xx, yy), nm, 34, (255, 255, 255), F_TITLE)
        if vt > 16.36: big_text(big, vt, 16.36, [("BEDA!", RED)], y=1130, size=80)
        card(big, vt - 13.78, "KEKURANGAN 1", "kadar zat aktif berbeda", accent=hx('e8892b'))
    elif ph == 1:
        xx, yy = w2s(cam, 36, 56); label(big, (xx, yy), "??? mg", 64, YELLOW, F_TITLE)
        xx, yy = w2s(cam, 72, 58); label(big, (xx, yy), "dosis jelas", 34, (255, 255, 255))
        card(big, vt - 17.78, "KEKURANGAN 2", "dosis tidak sepasti obat kimia" if False else "dosis kurang pasti", accent=hx('e8892b'))
    else:
        xx, yy = w2s(cam, 45, 42); label(big, (xx, yy), "UJI KLINIS", 40, INK, F_TITLE)
        if vt > 21.54: stamp(big, 540, 800, "BELUM ADA", 90, RED, 14)
        card(big, vt - 20.54, "KEKURANGAN 3", "banyak belum teruji klinis kuat", accent=hx('e8892b'))
    return big

def sc_bko(t, lt):
    vt = t - O
    im, d = scanlab(t)
    bx = -34 + 64 * ease((vt - 24.2) / .9) if vt < 25.1 else 30
    sp(im, BOTTLE, 'jb', bx, 73, {'C': 'j'}, k=3)
    u = min(1, max(0, (vt - 26.0) / 1.5)); by = 52 + 58 * u
    if 26.0 <= vt < 27.6:
        R(d, 18, by, 54, 2, hx('ff5050')); R(d, 18, by + 2, 54, 1, hx('a02e28'))
    for py, px in ((86, 36), (98, 44)):
        if vt > 26.0 and by > py: sp(im, CAPS, 'cp', px, py)
    big, cam = camera(im, 1.25, 45, 85, shake=(5 if 31.38 < vt < 31.7 else 0), t=t); big = big.convert('RGBA')
    dr = ImageDraw.Draw(big)
    if 27.2 < vt < 28.9:
        big = Image.alpha_composite(big, Image.new('RGBA', big.size, (220, 30, 40, int(50 * (.5 + .5 * math.sin(vt * 20))))))
    if 23.6 < vt < 25.1:
        big_text(big, vt, 23.6, [("YANG PALING", None), ("BERBAHAYA", RED)], y=330, size=64)
    if vt > 25.2 and vt < 29.0:
        x, y = w2s(cam, 45, 88); tstroke(dr, (x, y), "100% HERBAL", font(F_TITLE, 30), INK, 0, 'mm')
        if vt > 27.8:
            dr.line([(x - 190, y), (x + 190, y)], fill=RED, width=10)
    if 26.9 < vt < 28.9:
        big_text(big, vt, 26.9, [("TERDETEKSI:", YELLOW)], y=330, size=60)
        big_text(big, vt, 27.24, [("BAHAN KIMIA OBAT", RED)], y=440, size=56)
    if 27.8 < vt < 31.0:
        label(big, (540, 1560), "TIDAK TERTULIS DI LABEL", 40, (255, 255, 255), F_TITLE)
    if vt > 28.92:
        u2 = ease((vt - 28.92) / .3); ox = int((1 - u2) * 900)
        dr = ImageDraw.Draw(big)
        dr.rectangle([60 + ox, 276, 1020 + ox, 520], fill=INK); dr.rectangle([68 + ox, 284, 1012 + ox, 512], fill=GREEN)
        dr.text((540 + ox, 366), "BPOM", font=font(F_TITLE, 90), fill=(255, 255, 255), anchor='mm', stroke_width=5, stroke_fill=INK)
        dr.text((540 + ox, 460), "PENGUMUMAN PENARIKAN PRODUK", font=font(F_BODY, 40), fill=YELLOW, anchor='mm')
    if vt > 31.38:
        sc = pop(vt, 31.38, .2)
        stamp(big, 540, 960, "DITARIK", 130 * min(sc, 1.2), RED, 12, shake=(10 if vt < 31.7 else 0))
    return big

def zap(d, x0, y0, x1, y1, seed):
    rnd = random.Random(seed); pts = [(x0, y0)]
    for i in range(1, 7): pts.append((x0 + (x1 - x0) * i / 7, y0 + rnd.randint(-5, 5)))
    pts.append((x1, y1)); d.line(pts, fill=hx('F7CD00'), width=2)

def sc_inter(t, lt):
    vt = t - O
    im, d = stage(t)
    if vt < 35.4:
        person(im, RAKA, 37, 118, t, talk=True, seed=1)
        bob = int(math.sin(t * 3) * 2)
        sp(im, BOTTLE, 'jb', 10, 66 + bob, {'C': 'O'}, k=2); sp(im, BOTTLE, 'pb', 62, 66 - bob, {'C': 'P'}, k=2)
        if vt > 33.88: zap(d, 32, 78, 60, 78, int(t * 12))
    else:
        if vt > 36.28:
            y = 56 - (1 - ease((vt - 36.28) / .3)) * 40; sp(im, LEAF, 'lf', 12, y, None, k=3)
        if vt > 36.80:
            y = 60 - (1 - ease((vt - 36.80) / .3)) * 40; sp(im, ROOT, 'rt', 46, y, None, k=3)
        if vt > 39.4:
            y = 92 - (1 - ease((vt - 39.4) / .35)) * 90; sp(im, BOTTLE, 'pb', 30, y, {'C': 'P'}, k=3)
        if vt > 38.3:
            y = 20 + ((vt - 38.3) * 30) % 60; sp(im, DROP, 'dr', 42, y, None, k=3)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 33.28, [("INTERAKSI OBAT", None)], y=330, size=64)
    if vt >= 35.4:
        if vt > 36.28: x, y = w2s(cam, 31, 92); label(big, (x, y), "GINKGO", 34, hx('7bd389'), F_TITLE)
        if vt > 36.80: x, y = w2s(cam, 67, 92); label(big, (x, y), "KUNYIT", 34, hx('ffb060'), F_TITLE)
        if vt > 36.58: label(big, (540, 780), "+", 80, (255, 255, 255), F_TITLE)
        if vt > 39.76: label(big, (540, 1560), "PENGENCER DARAH", 44, hx('9fd0ff'), F_TITLE)
        if vt > 37.98: big_text(big, vt, 37.98, [("RISIKO", RED), ("PERDARAHAN", RED)], y=1320, size=70)
        if vt > 40.0 and int(vt * 6) % 2:
            big = Image.alpha_composite(big, Image.new('RGBA', big.size, (220, 30, 40, 45)))
    else:
        if vt > 33.88: big_text(big, vt, 33.88, [("HERBAL + OBAT", YELLOW)], y=1400, size=56)
    return big

def sc_compare(t, lt):
    vt = t - O
    im, d = apotek_int(t); im = light(im, (.33, .35, .42), [])
    big, cam = camera(im, 1.1, 45, 70); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    big_text(big, vt, 41.32, [("BEDANYA APA?", None)], y=330, size=70)
    if vt > 43.16:
        s = pop(vt, 43.16, .25)
        for x0, x1, nm, col in ((70, 530, "FARMASI", hx('3066B5')), (550, 1010, "HERBAL", hx('e8892b'))):
            dr.rectangle([x0 - 5, 475, x1 + 5, 585], fill=INK); dr.rectangle([x0, 480, x1, 580], fill=col)
            dr.text(((x0 + x1) // 2, 530), nm, font=font(F_TITLE, 44 * min(s, 1.2)), fill=(255, 255, 255), anchor='mm')
    rows = [("MUTU, KEAMANAN, KHASIAT", ["Terdaftar,", "dengan bukti"], ["Banyak yang belum", "teruji klinis kuat"], 43.44, False),
            ("KANDUNGAN & DOSIS", ["Kandungan &", "dosis pasti"], ["Bisa berbeda", "antarproduk"], 47.02, False),
            ("NOMOR REGISTRASI BPOM", ["Wajib ada"], ["Wajib ada, jika", "dijual legal"], 49.46, True)]
    for i, (lab, fl, hl, at, same) in enumerate(rows):
        c = vt - at
        if c < 0: continue
        oy = int((1 - ease(c / .3)) * 300); y0 = 620 + i * 330 + oy
        dr.rectangle([64, y0 - 6, 1016, y0 + 54], fill=INK); dr.text((540, y0 + 24), lab, font=font(F_BODY, 34), fill=(255, 255, 255), anchor='mm')
        for x0, x1, lines, col in ((70, 530, fl, GREEN), (550, 1010, hl, GREEN if same else hx('e8892b'))):
            dr.rectangle([x0 - 5, y0 + 56, x1 + 5, y0 + 285], fill=INK); dr.rectangle([x0, y0 + 62, x1, y0 + 280], fill=CREAM)
            dr.rectangle([x0, y0 + 62, x1, y0 + 76], fill=col)
            for j, ln in enumerate(lines):
                f = fit(dr, ln, 400, 46); dr.text(((x0 + x1) // 2, y0 + 150 + j * 62 - (len(lines) - 1) * 24), ln, font=f, fill=INK, anchor='mm')
        if same and vt > 50.76 and int(vt * 5) % 2:
            dr.rectangle([58, y0 - 10, 1022, y0 + 291], outline=YELLOW, width=10)
    return big

def sc_tips(t, lt):
    vt = t - O
    if vt < 56.2:
        im = Image.new('RGBA', (W, H), hx('2a2438')); d = ImageDraw.Draw(im)
        for y in range(0, H, 10): R(d, 0, y, W, 1, hx('332c47'))
        R(d, 12, 26, 66, 108, hx('7fb069')); d.rectangle([11, 25, 78, 134], outline=INK); R(d, 12, 26, 66, 10, hx('4f8a4a'))
        sp(im, LEAF, 'lf', 26, 44, None, k=3)
        R(d, 18, 96, 54, 32, hx('f6f1e3')); d.rectangle([17, 95, 72, 128], outline=INK)
        for i in range(4): R(d, 22, 116 + i * 2 if False else 120 + (i % 2) * 3, 20 + (i * 9) % 22, 1, hx('9a9a9a'))
        u = eio((vt - 54.0) / 1.0)
        z = 1.0 + .7 * u
        big, cam = camera(im, z, 45 - u, 80 + 30 * u); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
        x, y = w2s(cam, 45, 31); tstroke(dr, (x, y), "PRODUK HERBAL", font(F_TITLE, 26 * z), (255, 255, 255), 4, 'mm')
        x, y = w2s(cam, 44.5, 103); dr.text((x, y), "NO. REGISTRASI", font=font(F_BODY, 24 * z), fill=INK, anchor='mm')
        x, y = w2s(cam, 44.5, 113); dr.text((x, y), "BPOM", font=font(F_TITLE, 34 * z), fill=hx('227C4C'), anchor='mm')
        if vt > 54.16:
            x, y = w2s(cam, 44.5, 111.5); r = 240 * min(1, (vt - 54.16) / .3 + .01)
            dr.ellipse([x - r, y - r, x + r, y + r], outline=YELLOW, width=16)
            dr.line([(x + r * .7, y + r * .7), (x + r * 1.25, y + r * 1.25)], fill=YELLOW, width=22)
        card(big, vt - 53.04, "CEK KEMASAN", "nomor registrasi BPOM")
        return big
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=True, seed=4); counter(d); person(im, RAKA, 8, 112, t, seed=5)
    bob = int(math.sin(t * 3) * 2)
    if vt > 58.28:
        sp(im, BOTTLE, 'jb', 4, 58 + bob, {'C': 'O'}, k=1); sp(im, BOTTLE, 'pb', 18, 58 - bob, {'C': 'P'}, k=1)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.15, 40, 70); big = big.convert('RGBA')
    if 56.5 < vt < 58.28: x, y = w2s(cam, 12, 70); label(big, (x, y), "?", 110, YELLOW, F_TITLE)
    if vt >= 58.28: x, y = w2s(cam, 13, 50); label(big, (x, y), "?", 90, YELLOW, F_TITLE)
    if vt < 59.0: card(big, vt - 56.24, "TANYA APOTEKER", "sebelum minum herbal")
    else: card(big, vt - 59.0, "OBAT LAIN?", "wajib tanya apoteker dulu", accent=hx('e8892b'))
    return big

def sc_cta(t, lt):
    vt = t - O
    img = R2.sc_cta(lt).convert('RGBA')
    big_text(img, vt, 63.46, [("KONSULTASI DULU,", None), ("BARU MINUM.", YELLOW)], y=760, size=56)
    return img

VO_B = [4.65, 6.7, 13.6, 23.4, 33.1, 41.2, 53.0, 61.1]
_B = [0] + [b + O for b in VO_B] + [TOTAL]
_F = [sc_hook, sc_scale, sc_pros, sc_cons, sc_bko, sc_inter, sc_compare, sc_tips, sc_cta]
SCENES = [(_B[i], _B[i + 1], _F[i]) for i in range(len(_F))]
SCAN = None

def frame(t):
    global SCAN
    if SCAN is None: SCAN = R2._mk_scan()
    for a, b, fn in SCENES:
        if a <= t < b:
            lt = t - a; img = fn(t, lt).convert('RGBA')
            if a > 0 and lt < .2: img = wipe(img, 1 - lt / .2, True)
            if b < TOTAL and b - t < .2: img = wipe(img, 1 - (b - t) / .2, False)
            if t > TOTAL - .6: img = ImageEnhance.Brightness(img).enhance(max(0, (TOTAL - t) / .6))
            img = Image.alpha_composite(img, SCAN); brand_tag(img)
            return img.convert('RGB')
    return Image.new('RGB', (FW, FH))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]): frame(tt).save(f"h_{tt:05.2f}.png")
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', sys.argv[1]], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 300 == 0: print(i, '/', n, flush=True)
    p.stdin.close(); p.wait(); print('done')
