#!/usr/bin/env python3
"""Episode 4 - Obat generik vs bermerek. Synced to words_generik.json timing (vt = video time - O)."""
import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
from render5 import *      # brings render4 + render2 names, mark_row, head, MEDBOX, sp, stamp, fit ...
import render2 as R2

O = 0.3
TOTAL = 53.6
GRN = hx('7bd389')

def tag(big, x, y, text, col, size=34, fg=(255, 255, 255)):
    dr = ImageDraw.Draw(big); f = font(F_TITLE, size); w = int(dr.textlength(text, font=f)) + 44; h = size + 36
    dr.rectangle([x - w // 2 - 6, y - h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6], fill=INK)
    dr.rectangle([x - w // 2, y - h // 2, x + w // 2, y + h // 2], fill=col)
    dr.text((x, y), text, font=f, fill=fg, anchor='mm')

def counter_world(t):
    im = Image.new('RGBA', (W, H), hx('1d3a45')); d = ImageDraw.Draw(im)
    for y in range(0, 80, 8): R(d, 0, y, W, 1, hx('26505e'))
    for x in range(0, W, 10): R(d, x, 0, 1, 80, hx('26505e'))
    R(d, 0, 80, W, 5, hx('b07a52')); R(d, 0, 80, W, 1, hx('d29c6a'))
    R(d, 0, 85, W, H - 85, hx('8b5a3c'))
    for x in range(0, W, 12): R(d, x, 85, 1, H - 85, hx('6e4630'))
    return im, d

def boxes_pair(im, d):
    sp(im, MEDBOX, 'mb', 2, 53, {'C': 'G'}, k=3); sp(im, MEDBOX, 'mb', 46, 53, {'C': 'P'}, k=3)
    R(d, 60, 62, 3, 3, YELLOW); R(d, 59, 63, 5, 1, YELLOW); R(d, 61, 61, 1, 5, YELLOW)   # star mark on branded box

# ---------------- scenes ----------------
def sc_g1(t, lt):
    vt = t - O
    im, d = counter_world(t); boxes_pair(im, d)
    person(im, RAKA, 37, 142, t, talk=0.2 < vt < 3.5, seed=1)
    big, cam = camera(im, 1.0, 45, 80, shake=(3 if 2.04 < vt < 2.5 else 0), t=t); big = big.convert('RGBA')
    big_text(big, vt, 0.2, [("OBAT GENERIK", None)], y=330, size=60)
    big_text(big, vt, 0.9, [("LEBIH MURAH", YELLOW)], y=430, size=60)
    if vt > .54: tag(big, 270, 590, "GENERIK", hx('227C4C'), 34)
    if vt > 1.5: tag(big, 810, 590, "BERMEREK", hx('3066B5'), 34)
    if vt > 1.14: tag(big, 270, 1010, "MURAH", hx('227C4C'), 40)
    if vt > 1.7: tag(big, 810, 1010, "MAHAL", RED, 40)
    if vt > 2.04: big_text(big, vt, 2.04, [("KURANG AMPUH?", RED)], y=1250, size=72)
    return big

def sc_g2(t, lt):
    vt = t - O
    im, d = counter_world(t); boxes_pair(im, d)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 4.28, [("KURANG AMPUH?", None)], y=330, size=54)
    big_text(big, vt, 5.14, [("TIDAK.", GRN)], y=450, size=92)
    tag(big, 270, 590, "GENERIK", hx('227C4C'), 34); tag(big, 810, 590, "BERMEREK", hx('3066B5'), 34)
    if vt > 6.52: label(big, (540, 800), "=", 120, YELLOW, F_TITLE)
    check_row(big, vt - 6.52, 1000, "ZAT AKTIF SAMA", "bahan kerja obatnya sama")
    check_row(big, vt - 9.52, 1200, "DOSIS SAMA", "kekuatan obatnya sama")
    check_row(big, vt - 10.60, 1400, "BENTUK SAMA", "tablet tetap tablet")
    return big

def bar(dr, x, y, h, segs, vt, label_text):
    dr.text((x, y - 56), label_text, font=font(F_TITLE, 36), fill=(255, 255, 255))
    cx = x
    for (w, col, txt, at) in segs:
        g = ease((vt - at) / .5) if vt > at else 0
        ww = int(w * g)
        if ww > 4:
            dr.rectangle([cx - 4, y - 4, cx + ww + 4, y + h + 4], fill=INK); dr.rectangle([cx, y, cx + ww, y + h], fill=col)
            if g > .95: dr.text((cx + ww // 2, y + h // 2), txt, font=fit(dr, txt, ww - 20, 32, F_BODY), fill=(255, 255, 255), anchor='mm')
        cx += ww

def sc_g3(t, lt):
    vt = t - O
    im, d = bench(t); big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    big_text(big, vt, 12.26, [("KENAPA LEBIH MURAH?", None)], y=330, size=50)
    BL, OR = hx('3066B5'), hx('e8892b')
    bar(dr, 70, 760, 120, [(300, BL, "OBAT", 14.10), (260, OR, "RISET AWAL", 15.88), (260, RED, "PROMOSI MEREK", 17.06)], vt, "BERMEREK")
    bar(dr, 70, 1060, 120, [(300, BL, "OBAT", 14.10)], vt, "GENERIK")
    if vt > 14.10: label(big, (540, 1760), "ilustrasi, bukan harga sebenarnya", 30, hx('b8c8d2'))
    if vt > 18.84:
        big_text(big, vt, 18.84, [("SELISIH HARGA", None)], y=1380, size=56)
        big_text(big, vt, 19.2, [("BUKAN SELISIH MUTU", YELLOW)], y=1480, size=50)
    return big

def scale_scene(t, vt):
    im, d = apotek_int(t)
    im = light(im, (.38, .4, .5), [(45, 60, 50, .9, (1, .95, .8))]); d = ImageDraw.Draw(im)
    cx, cy = 45, 66; L = 24
    k = max(0, 1 - (vt - 25.76) / 2.4)
    tilt = (math.cos((vt - 25.76) * 7) * .28 * k) if vt > 25.76 else 0.28
    lx, ly = cx - L * math.cos(tilt), cy - L * math.sin(tilt); rx, ry = cx + L * math.cos(tilt), cy + L * math.sin(tilt)
    R(d, cx - 1, cy, 3, 40, hx('6b737c')); R(d, cx - 10, 104, 21, 4, hx('3a3f4a'))
    d.line([(lx, ly), (rx, ry)], fill=hx('c9a24a'), width=2); d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=hx('e0c060'), outline=INK)
    for ex, ey in ((lx, ly), (rx, ry)):
        d.line([(ex, ey), (ex - 9, ey + 14)], fill=hx('c9a24a')); d.line([(ex, ey), (ex + 9, ey + 14)], fill=hx('c9a24a')); R(d, ex - 10, ey + 14, 21, 2, hx('e0c060'))
    sp(im, MEDBOX, 'mb', lx - 7, ly + 6, {'C': 'G'}); sp(im, MEDBOX, 'mb', rx - 7, ry + 6, {'C': 'P'})
    return im, (lx, ly, rx, ry)

def sc_g4(t, lt):
    vt = t - O
    if vt < 25.7:
        im, d = scanlab(t)
        bx = -45 + 69 * ease((vt - 21.0) / 3.0) if vt > 21.0 else -45
        sp(im, MEDBOX, 'mb', bx, 85, {'C': 'G'}, k=3)
        big, cam = camera(im, 1.25, 45, 85); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
        big_text(big, vt, 20.98, [("WAJIB TERDAFTAR", None), ("DI BPOM", GRN)], y=330, size=56)
        x, y = w2s(cam, 45, 62); tstroke(dr, (x, y), "BPOM", font(F_TITLE, 44), hx('4fe38a'), 5, 'mm')
        if vt > 23.44: stamp(big, 540, 1000, "TERDAFTAR", 84, hx('4fe38a'), -10, shake=(8 if vt < 23.7 else 0))
        check_row(big, vt - 24.14, 1330, "STANDAR MUTU", "wajib terpenuhi")
        return big
    im, (lx, ly, rx, ry) = scale_scene(t, vt)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    x, y = w2s(cam, lx, ly + 26); label(big, (x, y), "GENERIK", 40, GRN, F_TITLE)
    x, y = w2s(cam, rx, ry + 26); label(big, (x, y), "BERMEREK", 40, hx('9fd0ff'), F_TITLE)
    big_text(big, vt, 25.76, [("DIUJI SETARA", None)], y=330, size=64)
    if vt > 28.14: big_text(big, vt, 28.14, [("KERJA SETARA", GRN)], y=440, size=70)
    card(big, vt - 25.76, "BANYAK JENIS OBAT", "kerjanya diuji setara", accent=GRN)
    return big

def sc_g5(t, lt):
    vt = t - O
    if vt < 35.5:
        im, d = bench(t)
        d.ellipse([12, 36, 40, 64], fill=(250, 250, 250), outline=INK); d.line([(14, 50), (38, 50)], fill=hx('b8c8d2'))
        d.ellipse([50, 42, 82, 58], fill=hx('3066B5'), outline=INK); R(d, 66, 49, 2, 2, YELLOW); R(d, 65, 50, 4, 1, YELLOW)
        big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
        big_text(big, vt, 29.64, [("TAPI ADA YANG", None), ("BISA BERBEDA", YELLOW)], y=330, size=56)
        tag(big, 270, 800, "GENERIK", hx('227C4C'), 30); tag(big, 780, 800, "BERMEREK", hx('3066B5'), 30)
        for i, (ti, at) in enumerate((("WARNA", 31.94), ("BENTUK TABLET", 32.68), ("RASA", 33.76), ("BAHAN TAMBAHAN", 34.38))):
            mark_row(big, vt - at, 920 + i * 190, ti, "bisa berbeda", hx('e8892b'), '?')
        return big
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=True, seed=4); counter(d); person(im, RAKA, 8, 112, t, seed=5)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.15, 40, 70); big = big.convert('RGBA')
    big_text(big, vt, 35.6, [("PUNYA ALERGI?", RED)], y=330, size=64)
    if vt > 38.44: big_text(big, vt, 38.44, [("SAMPAIKAN KE", None), ("APOTEKER", YELLOW)], y=560, size=60)
    card(big, vt - 35.6, "RIWAYAT ALERGI", "terhadap bahan tertentu", accent=RED)
    return big

def sc_g6(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=True, seed=4); counter(d); person(im, RAKA, 8, 112, t, seed=5)
    R(d, 34, 70, 12, 14, hx('f6f1e3')); d.rectangle([33, 69, 46, 84], outline=INK)
    for i in range(3): R(d, 36, 73 + i * 3, 8, 1, hx('9a9a9a'))
    if vt > 43.06:
        s = pop(vt, 43.06, .3); bubble(d, 24, 42, 30, 24, 46); logo_k(d, 39, 54, max(1, int(9 * min(s, 1.15))))
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 45, 70); big = big.convert('RGBA')
    if vt < 41.4: big_text(big, vt, 40.2, [("DAN SATU HAL LAGI...", None)], y=330, size=50)
    else: big_text(big, vt, 41.54, [("MURAH ATAU MAHAL", None)], y=330, size=56)
    x, y = w2s(cam, 40, 77); label(big, (x, y), "Rx", 40, INK, F_TITLE)
    if vt > 43.06: big_text(big, vt, 43.06, [("ANTIBIOTIK", YELLOW), ("WAJIB RESEP DOKTER", RED)], y=1640, size=50)
    return big

def sc_g7(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=False, seed=4); counter(d); person(im, RAKA, 8, 112, t, talk=True, seed=5)
    sp(im, MEDBOX, 'mb', 2, 56, {'C': 'P'}, k=2); sp(im, MEDBOX, 'mb', 34, 56, {'C': 'G'}, k=2)
    d.polygon([(26, 62), (26, 70), (32, 66)], fill=YELLOW, outline=INK); R(d, 18, 65, 8, 3, YELLOW)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 40, 70); big = big.convert('RGBA')
    big_text(big, vt, 45.62, [("GANTI KE", None), ("GENERIK?", GRN)], y=330, size=70)
    return big

def sc_g8(t, lt):
    vt = t - O
    img = R2.sc_cta(lt).convert('RGBA')
    if vt > 50.64: ImageDraw.Draw(img).rectangle([0, 262, 1080, 452], fill=(16, 20, 32, 235))
    big_text(img, vt, 50.64, [("KONSULTASI DULU,", None), ("BARU MINUM.", YELLOW)], y=330, size=56)
    return img

VO_B = [4.1, 12.0, 20.8, 29.58, 39.8, 45.4, 47.5]
_B = [0] + [b + O for b in VO_B] + [TOTAL]
_F = [sc_g1, sc_g2, sc_g3, sc_g4, sc_g5, sc_g6, sc_g7, sc_g8]
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
        for tt in map(float, sys.argv[2:]): frame(tt).save(f"e_{tt:05.2f}.png")
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', sys.argv[1]], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 300 == 0: print(i, '/', n, flush=True)
    p.stdin.close(); p.wait(); print('done')
