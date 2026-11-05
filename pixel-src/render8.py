#!/usr/bin/env python3
"""Episode 6 - Jangan campur obat sembarangan."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance
from render7 import *
import render2 as R2
O = 0.3; TOTAL = 62.8
ORG = hx('e8892b')

def chip(big, x, y, text, col, vt, at, size=30):
    if vt < at: return
    s = min(1.0, pop(vt, at, .25)); dr = ImageDraw.Draw(big); f = font(F_TITLE, max(8, int(size * s)))
    w = int(dr.textlength(text, font=f)) + 30; h = int(size * s) + 26
    dr.rectangle([x - w//2 - 5, y - h//2 - 5, x + w//2 + 5, y + h//2 + 5], fill=INK)
    dr.rectangle([x - w//2, y - h//2, x + w//2, y + h//2], fill=col); dr.text((x, y), text, font=f, fill=(255, 255, 255), anchor='mm')

def s1(t, lt):
    vt = t - O
    im, d = counter_world(t); boxes_pair(im, d)
    person(im, RAKA, 37, 142, t, talk=vt < 7.6, sick=vt < 6.9, seed=1)
    big, cam = camera(im, 1.0, 45, 80, shake=(3 if 6.98 < vt < 7.4 else 0), t=t); big = big.convert('RGBA')
    big_text(big, vt, 0.0, [("PUSING?", None)], y=330, size=64)
    if vt > 3.44: big_text(big, vt, 3.44, [("FLU JUGA?", YELLOW)], y=430, size=64)
    chip(big, 270, 590, "SAKIT KEPALA", hx('227C4C'), vt, 1.44, 28)
    chip(big, 810, 590, "OBAT FLU", hx('3066B5'), vt, 4.18, 28)
    if vt > 5.96: big_text(big, vt, 5.96, [("AMAN?", None)], y=1180, size=72)
    if vt > 6.98: big_text(big, vt, 6.98, [("BELUM TENTU.", RED)], y=1300, size=64)
    return big

def s2(t, lt):
    vt = t - O
    im, d = counter_world(t); boxes_pair(im, d)
    big, cam = camera(im, 1.0, 45, 80, shake=(6 if 17.3 < vt < 17.7 else 0), t=t); big = big.convert('RGBA')
    big_text(big, vt, 8.62, [("BANYAK OBAT FLU", None), ("MENGANDUNG", YELLOW)], y=330, size=54)
    chip(big, 810, 590, "OBAT FLU", hx('3066B5'), vt, 8.62, 28); chip(big, 270, 590, "SAKIT KEPALA", hx('227C4C'), vt, 12.48, 28)
    chip(big, 810, 1010, "PARASETAMOL", ORG, vt, 11.18, 30)
    chip(big, 270, 1010, "PARASETAMOL", ORG, vt, 15.6, 30)
    if vt > 15.6: label(big, (540, 1010), "+", 80, YELLOW, F_TITLE)
    if vt > 16.94: stamp(big, 540, 1400, "DOSIS DOBEL!", 76, RED, -8, shake=(8 if vt < 17.7 else 0))
    return big

def liver(d, cx, cy, crack):
    d.polygon([(cx-30, cy-6), (cx-20, cy-16), (cx+4, cy-18), (cx+26, cy-12), (cx+30, cy-4), (cx+18, cy+6), (cx-4, cy+14), (cx-22, cy+12), (cx-32, cy+4)], fill=hx('a8453f'), outline=INK)
    d.line([(cx-18, cy-10), (cx+10, cy-12)], fill=hx('c96a5e'))
    if crack:
        d.line([(cx-4, cy-17), (cx-8, cy-6), (cx-2, cy), (cx-8, cy+12)], fill=INK, width=1)
        d.line([(cx+14, cy-14), (cx+10, cy-4), (cx+16, cy+4)], fill=INK, width=1)

def s3(t, lt):
    vt = t - O
    im, d = scanlab(t)
    liver(d, 45, 78, vt > 20.94)
    big, cam = camera(im, 1.0, 45, 80, shake=(5 if 20.94 < vt < 21.3 else 0), t=t); big = big.convert('RGBA')
    big_text(big, vt, 18.62, [("PARASETAMOL", ORG), ("BERLEBIH", None)], y=330, size=60)
    if vt > 20.2: big_text(big, vt, 20.2, [("BISA MERUSAK HATI", RED)], y=1300, size=52)
    if vt > 22.04: big_text(big, vt, 22.04, [("SERING TANPA GEJALA", None), ("DI AWAL", YELLOW)], y=1480, size=46)
    return big

def s4(t, lt):
    vt = t - O
    im, d = bench(t); sp(im, MEDBOX, 'mb', 24, 40, {'C': 'P'}, k=3)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 24.76, [("CEK KOMPOSISI", YELLOW), ("DI KEMASAN", None)], y=330, size=58)
    check_row(big, vt - 25.56, 1000, "BACA KOMPOSISI", "lihat zat aktifnya")
    mark_row(big, vt - 27.74, 1200, "ZAT AKTIF SAMA?", "bandingkan antar obat", ORG, '?')
    mark_row(big, vt - 30.06, 1400, "JANGAN BERSAMAAN", "kalau zat aktifnya sama", RED, 'x')
    return big

def s5(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=False, seed=4); counter(d); person(im, RAKA, 8, 112, t, talk=vt < 37, seed=5)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 40, 70); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    dr.rectangle([0, 520, 1080, 1720], fill=(16, 20, 32, 200)) if vt > 32.32 else None
    big_text(big, vt, 32.32, [("PUNYA OBAT RUTIN?", YELLOW)], y=330, size=56)
    chip(big, 270, 640, "DARAH TINGGI", hx('3066B5'), vt, 33.8, 30)
    chip(big, 800, 640, "DIABETES", hx('227C4C'), vt, 35.04, 30)
    chip(big, 540, 780, "PENGENCER DARAH", hx('7a3fa0'), vt, 35.74, 30)
    mark_row(big, vt - 37.42, 960, "OBAT FLU TERTENTU", "bisa menaikkan tekanan darah", RED, 'x')
    mark_row(big, vt - 40.34, 1180, "SALING MENGGANGGU", "kerja obat bisa terganggu", ORG, '?')
    return big

def s6(t, lt):
    vt = t - O
    im, d = bench(t)
    for i, c in enumerate(['O', 'G', 'Y']):
        y = 56 - (1 - ease((vt - 44.06 - i*.2) / .3)) * 60 if vt > 44.06 + i*.2 else -40
        sp(im, BOTTLE, 'jb', 18 + i*20, y, {'C': c}, k=2)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 44.06, [("JAMU & SUPLEMEN", YELLOW)], y=330, size=56)
    if vt > 45.26: big_text(big, vt, 45.26, [("JUGA DIHITUNG", None)], y=430, size=56)
    if vt > 46.9: big_text(big, vt, 46.9, [("SEBUTKAN SEMUA", None), ("KE APOTEKER", GRN)], y=1350, size=56)
    return big

def s7(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=False, seed=4); counter(d); person(im, RAKA, 8, 112, t, talk=True, seed=5)
    if vt > 50.92:
        R(d, 34, 66, 12, 16, hx('f6f1e3')); d.rectangle([33, 65, 46, 82], outline=INK)
        for i in range(4): R(d, 36, 69 + i*3, 8, 1, hx('9a9a9a'))
    if vt > 53.08:
        R(d, 22, 70, 7, 12, INK); R(d, 23, 71, 5, 9, hx('8fd3ff')); R(d, 24, 73, 3, 3, hx('3066B5'))
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 40, 70); big = big.convert('RGBA')
    big_text(big, vt, 49.48, [("BELI OBAT BARU?", None)], y=330, size=58)
    if vt > 50.92: big_text(big, vt, 50.92, [("BAWA DAFTAR OBAT", YELLOW)], y=1550, size=50)
    if vt > 53.08: big_text(big, vt, 53.08, [("ATAU FOTO KEMASANNYA", GRN)], y=1650, size=44)
    return big

def s8(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=True, seed=4); counter(d); person(im, RAKA, 8, 112, t, happy=True, seed=5)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 40, 70); big = big.convert('RGBA')
    big_text(big, vt, 54.44, [("TANYA", None), ("APOTEKER KAMI", YELLOW)], y=330, size=62)
    return big

def s9(t, lt):
    vt = t - O
    img = R2.sc_cta(lt).convert('RGBA')
    if vt > 59.38: ImageDraw.Draw(img).rectangle([0, 262, 1080, 452], fill=(16, 20, 32, 235))
    big_text(img, vt, 59.38, [("KONSULTASI DULU,", None), ("BARU MINUM.", YELLOW)], y=330, size=56)
    return img

VO_B = [8.1, 18.1, 24.3, 31.7, 43.6, 49.1, 54.1, 59.0]
_B = [0] + [b + O for b in VO_B] + [TOTAL]
_F = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
SCENES = [(_B[i], _B[i+1], _F[i]) for i in range(len(_F))]
_S = [None]
def frame(t):
    if _S[0] is None: _S[0] = R2._mk_scan()
    for a, b, fn in SCENES:
        if a <= t < b:
            lt = t - a; img = fn(t, lt).convert('RGBA')
            if a > 0 and lt < .2: img = wipe(img, 1 - lt/.2, True)
            if b < TOTAL and b - t < .2: img = wipe(img, 1 - (b-t)/.2, False)
            if t > TOTAL - .6: img = ImageEnhance.Brightness(img).enhance(max(0, (TOTAL - t)/.6))
            img = Image.alpha_composite(img, _S[0]); brand_tag(img); return img.convert('RGB')
    return Image.new('RGB', (FW, FH))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]): frame(tt).save(f"g_{tt:05.2f}.png")
        sys.exit()
    p = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{FW}x{FH}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',sys.argv[1]], stdin=subprocess.PIPE)
    n = int(TOTAL*FPS)
    for i in range(n):
        p.stdin.write(frame(i/FPS).tobytes())
        if i % 300 == 0: print(i, '/', n, flush=True)
    p.stdin.close(); p.wait(); print('done')
