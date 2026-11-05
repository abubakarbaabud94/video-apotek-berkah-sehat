#!/usr/bin/env python3
"""Episode 3 - Cara menyimpan obat yang benar. Reuses render2/render4 engine; synced to words_simpan.json timing."""
import math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
from render4 import *   # also brings render2 names (R, sprite, person, camera, w2s, card, label, big_text, tstroke, wipe, light ...)
import render2 as R2

O = 0.3
TOTAL = 65.6

MEDBOX = ["CCCCCCCCCCCC", "CWWWWWWWWWWC", "CWWWWKWWWWWC", "CWWWKKKWWWWC", "CWWWWKWWWWWC", "CWWWWWWWWWWC", "CCCCCCCCCCCC"]
PEN = ["..DDDDDDDDDD.", "DDWWWWWWWWPPD", "DDWWWWWWWWPPD", "..DDDDDDDDDD."]

def mark_row(big, c, y, title, sub, col, glyph):
    if c < 0: return
    dr = ImageDraw.Draw(big); ox = int((1 - ease(c / .3)) * 700); x0 = 70 + ox; x1 = 1010 + ox
    dr.rectangle([x0 - 6, y - 6, x1 + 6, y + 170], fill=INK); dr.rectangle([x0, y, x1, y + 164], fill=CREAM)
    dr.rectangle([x0, y, x0 + 18, y + 164], fill=col)
    bx = x0 + 50; dr.rectangle([bx, y + 32, bx + 100, y + 132], fill=col, outline=INK, width=5)
    if glyph == 'x':
        dr.line([(bx + 25, y + 57), (bx + 75, y + 107)], fill=(255, 255, 255), width=14); dr.line([(bx + 75, y + 57), (bx + 25, y + 107)], fill=(255, 255, 255), width=14)
    elif glyph == '?':
        dr.text((bx + 50, y + 84), "?", font=font(F_TITLE, 64), fill=(255, 255, 255), anchor='mm')
    else:
        dr.line([(bx + 20, y + 84), (bx + 42, y + 108), (bx + 82, y + 54)], fill=(255, 255, 255), width=14)
    dr.text((x0 + 190, y + 34), title, font=fit(dr, title, 740, 40, F_TITLE), fill=INK)
    dr.text((x0 + 190, y + 98), sub, font=font(F_BODY2, 46), fill=hx('4a4358'))

def head(big, vt, at1, t1, at2, t2, c1=YELLOW):
    big_text(big, vt, at1, [(t1, c1)], y=330, size=64)
    big_text(big, vt, at2, [(t2, None)], y=430, size=max(30, min(52, int(960 / len(t2)))))

# ---------------- worlds ----------------
def bathroom(t, vt):
    im = Image.new('RGBA', (W, H), hx('b8dce8')); d = ImageDraw.Draw(im)
    for y in range(0, 104, 8): R(d, 0, y, W, 1, hx('9cc7d6'))
    for x in range(0, W, 8): R(d, x, 0, 1, 104, hx('9cc7d6'))
    R(d, 0, 104, W, H - 104, hx('6f8394'))
    for x in range(0, W, 12): R(d, x, 104, 1, H - 104, hx('5d7080'))
    R(d, 56, 8, 3, 14, hx('9aa3ad')); d.ellipse([50, 20, 66, 26], fill=hx('9aa3ad'), outline=INK)
    R(d, 8, 52, 40, 3, hx('8b5a3c')); sp(im, MEDBOX, 'mb', 10, 34, {'C': 'P'}, k=2); sp(im, MEDBOX, 'mb', 28, 34, {'C': 'R'}, k=2)
    rnd = random.Random(4); n = 46 if vt > 13.0 else 10
    for i in range(n):
        x = (rnd.randrange(W) + math.sin(t * 1.2 + i) * 3) % W; y = (rnd.randrange(H) - t * 9 * (1 + (i % 3) * .3)) % H
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=hx('eef7fa'))
    R(d, 74, 40, 6, 40, hx('f4f4f4')); d.rectangle([73, 39, 80, 80], outline=INK)
    g = ease((vt - 13.54) / 1.0) if vt > 13.54 else 0
    hh = int(36 * g)
    if hh > 0: R(d, 75, 79 - hh, 4, hh, RED)
    d.ellipse([71, 78, 83, 90], fill=RED, outline=INK)
    return im, d

def cabinet(t, vt):
    im = Image.new('RGBA', (W, H), hx('efe6cf')); d = ImageDraw.Draw(im)
    for y in range(0, 100, 8): R(d, 0, y, W, 1, hx('e2d7ba'))
    R(d, 0, 100, W, H - 100, hx('9a6b45'))
    for y in range(104, H, 7): R(d, 0, y, W, 1, hx('7d5538'))
    R(d, 4, 8, 24, 28, hx('8b5a3c')); R(d, 6, 10, 20, 24, hx('a8def5')); d.ellipse([10, 14, 20, 24], fill=hx('F7CD00'), outline=INK)
    for k in range(5): d.line([(20, 22), (40 + k * 6, 50 + k * 12)], fill=hx('ffe98a'), width=1)
    R(d, 36, 30, 50, 76, hx('8b5a3c')); d.rectangle([35, 29, 86, 106], outline=INK); R(d, 38, 32, 46, 72, hx('4a2f20'))
    R(d, 38, 66, 46, 2, hx('8b5a3c')); R(d, 38, 100, 46, 2, hx('8b5a3c'))
    sp(im, MEDBOX, 'mb', 46, 57, {'C': 'P'}); sp(im, MEDBOX, 'mb', 62, 57, {'C': 'G'}); sp(im, MEDBOX, 'mb', 54, 91, {'C': 'Y'})
    if vt > 18.34:
        dw = int(46 * ease((vt - 18.34) / .4)); R(d, 38, 32, dw, 72, hx('a26c48')); d.rectangle([38, 32, 38 + dw, 104], outline=INK)
    return im, d

def table_world(t, vt):
    im = Image.new('RGBA', (W, H), hx('d9cfb4')); d = ImageDraw.Draw(im)
    for y in range(0, 96, 8): R(d, 0, y, W, 1, hx('cdc19f'))
    R(d, 0, 96, W, H - 96, hx('8b6a4a'))
    person(im, RAKA, 36, 106, t, sick=vt > 29.46, talk=False, seed=2)
    R(d, 0, 104, W, 10, hx('b07a52')); R(d, 0, 104, W, 2, hx('d29c6a')); R(d, 4, 114, 4, 40, hx('6e4630')); R(d, W - 8, 114, 4, 40, hx('6e4630'))
    R(d, 0, 114, W, 2, hx('6e4630'))
    R2.strip(d, 12, 96, used=3)
    for x, y in ((38, 99), (50, 100), (62, 98)): sp(im, CAPS, 'cp', x, y)
    sp(im, MEDBOX, 'mb', 70, 95, {'C': 'a'})
    if vt > 29.46:
        for i in range(3):
            a = t * 6 + i * 2.09; x = 45 + 11 * math.cos(a); y = 72 + 3 * math.sin(a)
            R(d, x - 1, y, 3, 1, YELLOW); R(d, x, y - 1, 1, 3, YELLOW)
    return im, d

def fridge_world(t, vt):
    im = Image.new('RGBA', (W, H), hx('e8dfc6')); d = ImageDraw.Draw(im)
    for y in range(0, 110, 8): R(d, 0, y, W, 1, hx('dccfae'))
    R(d, 0, 110, W, H - 110, hx('8b6a4a'))
    R(d, 14, 16, 62, 110, hx('c9d4dc')); d.rectangle([13, 15, 76, 126], outline=INK)
    R(d, 18, 20, 54, 102, hx('f4fbff'))
    for sy in (50, 80, 108): R(d, 18, sy, 54, 2, hx('b8c8d2'))
    cols = ['R', 'Y', 'G', 'P', 'O', 'R']
    for i, (x, y) in enumerate(((22, 40), (38, 40), (54, 40), (22, 70), (38, 70), (54, 98))):
        sp(im, MEDBOX, 'mb', x, y, {'C': cols[i]})
    if vt > 37.26:
        p = int(vt * 4) % 2
        d.rectangle([52, 96, 68, 107], outline=YELLOW if p else hx('fff3b0'), width=1)
        for dx, dy in ((0, -3), (0, 3), (-3, 0), (3, 0)): R(d, 60 + dx, 91 + dy, 1, 1, hx('7fc4ff'))
    dw = int(62 * (1 - ease((vt - 32.44) / .6))) if vt >= 32.44 else 62
    if dw > 6:
        R(d, 14, 16, dw, 110, hx('dfe7ee')); d.rectangle([13, 15, 14 + dw, 126], outline=INK); R(d, 14 + dw - 5, 60, 2, 14, hx('8a949c'))
    else:
        R(d, 4, 16, 9, 110, hx('dfe7ee')); d.rectangle([3, 15, 13, 126], outline=INK)
    if vt > 40.26:
        s = ease((vt - 40.26) / .4); sp(im, PEN, 'pen', 6 + int((1 - s) * 80), 130, None, k=3)
    return im, d

def room_world(t, vt):
    im = Image.new('RGBA', (W, H), hx('efe0c2')); d = ImageDraw.Draw(im)
    for y in range(0, 100, 8): R(d, 0, y, W, 1, hx('e2d1ac'))
    R(d, 0, 100, W, H - 100, hx('9a6b45'))
    for y in range(104, H, 7): R(d, 0, y, W, 1, hx('7d5538'))
    R(d, 44, 34, 40, 30, hx('8b5a3c')); d.rectangle([43, 33, 84, 64], outline=INK); R(d, 46, 36, 36, 26, hx('4a2f20'))
    R(d, 4, 108, 38, 4, hx('b07a52')); R(d, 6, 112, 3, 22, hx('6e4630')); R(d, 37, 112, 3, 22, hx('6e4630'))
    up = ease((vt - 45.56) / 1.0) if vt > 45.56 else 0
    by = 98 - up * 52
    sp(im, MEDBOX, 'mb', 14 + int(up * 36), by, {'C': 'P'}, k=1)
    if vt > 46.84:
        dw = int(36 * ease((vt - 46.84) / .35)); R(d, 46, 36, dw, 26, hx('a26c48')); d.rectangle([46, 36, 46 + dw, 62], outline=INK)
        if dw > 30: R(d, 62, 45, 8, 6, YELLOW); d.rectangle([62, 45, 70, 51], outline=INK); d.rectangle([64, 41, 68, 45], outline=INK)
    kid = sprite(RAKA, 'kid', {'R': 'Y', 'r': 'x', 'q': 'Y'}); kid = kid.resize((int(kid.width * .62), int(kid.height * .62)), Image.NEAREST)
    kx = 48 - (0 if vt < 45.56 else min(8, (vt - 45.56) * 8)); kfeet = 126
    reach = 44.0 < vt < 45.56
    im.paste(kid, (int(kx), int(kfeet - kid.height + 2 + (math.sin(t * 5) if reach else 0))), kid)
    return im, d

# ---------------- scenes ----------------
def sc_hook3(t, lt):
    vt = t - O
    im, d = kitchen(t)
    person(im, RAKA, 37, 122, t, talk=0.2 < vt < 8.0, sick=vt > 6.98, seed=1)
    sp(im, MEDBOX, 'mb', 50, 110 + int(math.sin(t * 3)), {'C': 'P'})
    big, cam = camera(im, 1.5 - .1 * eio(lt / 8.7), 46, 86, shake=(4 if 6.98 < vt < 7.5 else 0), t=t); big = big.convert('RGBA')
    big_text(big, vt, 0.2, [("OBAT DI RUMAH", None)], y=330, size=62)
    big_text(big, vt, 1.74, [("DISIMPAN DI MANA?", YELLOW)], y=430, size=54)
    if vt < 6.3:
        mark_row(big, vt - 4.06, 1100, "KAMAR MANDI?", "lembap", RED, 'x')
        mark_row(big, vt - 5.08, 1300, "DEKAT KOMPOR?", "panas", RED, 'x')
    if vt > 6.98:
        big_text(big, vt, 6.98, [("OBAT RUSAK", RED)], y=1050, size=84)
    if vt > 7.82:
        big_text(big, vt, 7.82, [("SEBELUM KEDALUWARSA", YELLOW)], y=1180, size=44)
    return big

def sc_store1(t, lt):
    vt = t - O
    im, d = bathroom(t, vt) if vt < 16.0 else cabinet(t, vt)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    if vt < 16.0:
        head(big, vt, 9.36, "KESALAHAN 1", 10.68, "LEMBAB & PANAS", RED)
        if vt > 13.0: big_text(big, vt, 13.0, [("UAP & SUHU TINGGI", RED)], y=1500, size=52)
        if vt > 14.2: label(big, (540, 1620), "merusak kandungan obat", 44, (255, 255, 255))
    else:
        head(big, vt, 16.16, "SOLUSI", 16.52, "SEJUK & KERING", hx('7bd389'))
        if vt > 18.34:
            x, y = w2s(cam, 16, 22)
            dr.line([(x - 90, y - 90), (x + 90, y + 90)], fill=RED, width=22); dr.line([(x + 90, y - 90), (x - 90, y + 90)], fill=RED, width=22)
            card(big, vt - 18.34, "JAUH DARI MATAHARI", "hindari sinar langsung", accent=hx('7bd389'))
    return big

def sc_store2(t, lt):
    vt = t - O
    im, d = table_world(t, vt)
    big, cam = camera(im, 1.2, 45, 85); big = big.convert('RGBA')
    head(big, vt, 20.58, "KESALAHAN 2", 22.08, "DIKELUARKAN DARI KEMASAN", RED)
    if vt > 24.52: label(big, (540, 560), "YANG IKUT HILANG:", 44, YELLOW, F_TITLE)
    mark_row(big, vt - 25.68, 1000, "NAMA OBAT", "tidak terbaca lagi", RED, 'x')
    mark_row(big, vt - 26.84, 1200, "ATURAN PAKAI", "tidak ada petunjuk", RED, 'x')
    mark_row(big, vt - 27.96, 1400, "TANGGAL KEDALUWARSA", "tidak diketahui", RED, 'x')
    if vt > 29.46 and vt < 32.0: big_text(big, vt, 29.46, [("SALAH MINUM!", RED)], y=1700, size=76)
    return big

def sc_store3(t, lt):
    vt = t - O
    im, d = fridge_world(t, vt)
    im = light(im, (.92, .97, 1.0), [])
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    head(big, vt, 32.44, "KESALAHAN 3", 33.82, "SEMUA OBAT KE KULKAS", RED)
    if 36.04 < vt < 37.2:
        dr.line([(240, 700), (840, 1300)], fill=RED, width=34); dr.line([(840, 700), (240, 1300)], fill=RED, width=34)
        big_text(big, vt, 36.04, [("TIDAK SEMUA PERLU", RED)], y=1420, size=52)
    if vt >= 37.26:
        big_text(big, vt, 37.26, [("HANYA YANG TERTULIS", YELLOW)], y=1380, size=48)
        label(big, (540, 1470), "\"SIMPAN DI KULKAS\"", 44, hx('9fd0ff'), F_TITLE)
    if vt > 40.26:
        label(big, (800, 1650), "INSULIN", 48, (255, 255, 255), F_TITLE)
    return big

def sc_store4(t, lt):
    vt = t - O
    im, d = room_world(t, vt)
    big, cam = camera(im, 1.3, 40, 92); big = big.convert('RGBA')
    if vt < 45.4: head(big, vt, 42.16, "KESALAHAN 4", 43.48, "DALAM JANGKAUAN ANAK", RED)
    if vt > 43.48 and vt < 45.56: label(big, (540, 1500), "!", 150, RED, F_TITLE)
    if vt > 45.56: card(big, vt - 45.56, "SIMPAN TINGGI", "dan tertutup rapat", accent=hx('7bd389'))
    return big

def sc_check(t, lt):
    vt = t - O
    im, d = bench(t)
    pc = 'k' if vt > 51.2 else 'R'
    sp(im, BOTTLE, 'jb', 25, 44, {'C': 'P'}, k=4); sp(im, CAPS, 'cp', 62, 78, {'R': pc}, k=3)
    if 51.72 < vt < 53.3:
        for i in range(3):
            x0 = 66 + i * 7; pts = [(x0 + math.sin(t * 5 + j * .8 + i) * 2, 72 - j * 4) for j in range(8)]
            d.line(pts, fill=hx('7bd389'), width=1)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    if vt < 55.4:
        big_text(big, vt, 48.28, [("SEBELUM MINUM,", None), ("CEK DULU!", YELLOW)], y=330, size=62)
        mark_row(big, vt - 50.60, 1060, "WARNA BERUBAH?", "cek isi dan tablet", hx('e8892b'), '?')
        mark_row(big, vt - 51.72, 1260, "BAU ANEH?", "cium sebelum minum", hx('e8892b'), '?')
        mark_row(big, vt - 52.72, 1460, "LEWAT KEDALUWARSA?", "cek tanggal di kemasan", RED, '?')
    if vt > 52.72:
        x, y = w2s(cam, 45, 72); tstroke(dr, (x, y), "EXP", font(F_TITLE, 34), RED, 0, 'mm')
    if vt > 55.5:
        stamp(big, 540, 900, "JANGAN DIMINUM", 64, RED, 10, shake=(8 if vt < 55.8 else 0))
    return big

def sc_cta3(t, lt):
    vt = t - O
    img = R2.sc_cta(lt).convert('RGBA')
    big_text(img, vt, 62.58, [("KONSULTASI DULU,", None), ("BARU MINUM.", YELLOW)], y=760, size=56)
    return img

VO_B = [9.0, 20.45, 32.2, 42.0, 48.1, 57.1]
_B = [0] + [b + O for b in VO_B] + [TOTAL]
_F = [sc_hook3, sc_store1, sc_store2, sc_store3, sc_store4, sc_check, sc_cta3]
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
        for tt in map(float, sys.argv[2:]): frame(tt).save(f"s_{tt:05.2f}.png")
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', sys.argv[1]], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 300 == 0: print(i, '/', n, flush=True)
    p.stdin.close(); p.wait(); print('done')
