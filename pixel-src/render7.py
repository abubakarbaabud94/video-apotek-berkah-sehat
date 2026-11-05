#!/usr/bin/env python3
"""Episode 5 - Cara minum obat yang benar."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance
from render6 import *
import render2 as R2
O = 0.3; TOTAL = 61.6
GRN = hx('7bd389'); BL = hx('3066B5')

def pill(d, x, y, col=(255, 255, 255), k=1):
    d.ellipse([x - 4*k, y - 2*k, x + 4*k, y + 2*k], fill=col, outline=INK)
def glass(d, x, y, fill, k=1):
    d.polygon([(x-6*k, y-14*k), (x+6*k, y-14*k), (x+4*k, y), (x-4*k, y)], fill=(220, 240, 250), outline=INK)
    if fill: d.polygon([(x-5*k, y-8*k), (x+5*k, y-8*k), (x+4*k, y-1*k), (x-4*k, y-1*k)], fill=fill)

def s1(t, lt):
    vt = t - O
    im, d = counter_world(t); boxes_pair(im, d)
    for i in range(3): pill(d, 30 + i*14, 95, k=2)
    person(im, RAKA, 37, 142, t, talk=vt < 4.0, seed=1)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 0.0, [("OBATNYA BENAR", None)], y=330, size=60)
    if vt > 1.8: big_text(big, vt, 1.8, [("CARA MINUMNYA?", YELLOW)], y=430, size=60)
    if vt > 3.06: big_text(big, vt, 3.06, [("SUDAH BENAR?", RED)], y=1250, size=72)
    return big

def timeline(dr, vt, y, marks, col, at0, label_text):
    dr.text((70, y - 70), label_text, font=font(F_TITLE, 34), fill=(255, 255, 255))
    dr.rectangle([60, y - 6, 1020, y + 70], fill=INK); dr.rectangle([66, y, 1014, y + 64], fill=hx('2a4a58'))
    for h in range(0, 25, 4): dr.text((66 + h/24*948, y + 100), f"{h:02d}", font=font(F_BODY, 26), fill=hx('b8c8d2'), anchor='mm')
    for i, (h, at) in enumerate(marks):
        if vt > at:
            s = pop(vt, at, .25); x = 66 + h/24*948
            dr.ellipse([x - 28*s, y + 32 - 28*s, x + 28*s, y + 32 + 28*s], fill=col, outline=INK, width=4)

def s2(t, lt):
    vt = t - O
    im, d = bench(t); big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA'); dr = ImageDraw.Draw(big)
    big_text(big, vt, 4.5, [("3 KALI SEHARI", None)], y=330, size=64)
    if vt > 6.78: big_text(big, vt, 6.78, [("±8 JAM SEKALI", GRN)], y=430, size=60)
    if vt > 7.5: timeline(dr, vt, 700, [(6, 7.84), (14, 8.1), (22, 8.4)], GRN, 7.5, "YANG BENAR")
    if vt > 8.92:
        timeline(dr, vt, 1150, [(18, 9.14), (19.5, 9.72), (21, 10.16)], RED, 8.92, "BUKAN BEGINI")
        big_text(big, vt, 10.64, [("DIMINUM BERDEKATAN", RED)], y=1560, size=48)
    return big

def s3(t, lt):
    vt = t - O
    im, d = bench(t)
    d.ellipse([10, 36, 80, 62], fill=(250, 250, 250), outline=INK); d.ellipse([22, 41, 68, 57], fill=hx('e8e8e8'))
    if vt > 20.0:
        d.ellipse([34, 45, 56, 53], fill=hx('e8892b'))
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 13.86, [("KAPAN MINUMNYA?", None)], y=330, size=54)
    mark_row(big, vt - 14.92, 900, "SEBELUM MAKAN", "±30 menit sebelum, perut kosong", hx('3066B5'), '1')
    if vt > 17.46: label(big, (540, 1160), "PERUT KOSONG", 40, YELLOW, F_TITLE)
    if vt > 20.0: mark_row(big, vt - 20.0, 1300, "SESUDAH MAKAN", "sesaat setelah makan", hx('227C4C'), '2')
    if vt > 21.98: label(big, (540, 1560), "LAMBUNG TIDAK PERIH", 40, GRN, F_TITLE)
    return big

def s4(t, lt):
    vt = t - O
    im, d = counter_world(t)
    glass(d, 45, 100, hx('8fd3ff'), k=3)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 24.0, [("MINUM OBAT DENGAN", None), ("AIR PUTIH", GRN)], y=330, size=56)
    pass
    for i, (ti, at) in enumerate((("TEH", 25.9), ("KOPI", 26.42), ("SUSU", 27.12))):
        mark_row(big, vt - at, 1150 + i * 170, ti, "bisa ganggu penyerapan", RED, 'x')
    return big

def s5(t, lt):
    vt = t - O
    im, d = bench(t)
    d.ellipse([10, 40, 40, 56], fill=hx('3066B5'), outline=INK); d.ellipse([46, 40, 76, 56], fill=(250, 250, 250), outline=INK)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 30.96, [("JANGAN ASAL", None), ("RUSAK OBAT", RED)], y=330, size=56)
    for i, (ti, sub, at) in enumerate((("BUKA KAPSUL", "isi kapsul jangan dibuka", 32.42), ("KUNYAH", "jangan dikunyah", 33.48), ("BELAH TABLET", "kecuali dianjurkan", 34.14))):
        mark_row(big, vt - at, 830 + i * 190, ti, sub, RED, 'x')
    if vt > 35.94: big_text(big, vt, 35.94, [("ADA OBAT YANG", None), ("DIRANCANG PELAN", YELLOW)], y=1500, size=52)
    return big

def s6(t, lt):
    vt = t - O
    im, d = counter_world(t)
    person(im, RAKA, 37, 142, t, talk=False, seed=1)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 40.26, [("LUPA MINUM", None), ("SATU DOSIS?", YELLOW)], y=330, size=60)
    if vt > 41.86: mark_row(big, vt - 41.86, 780, "JANGAN 2X LIPAT", "dosis tidak boleh digandakan", RED, 'x')
    if vt > 44.0: mark_row(big, vt - 44.0, 980, "MINUM SAAT INGAT", "segera setelah ingat", hx('227C4C'), 'c')
    if vt > 45.1: mark_row(big, vt - 45.1, 1180, "KECUALI", "sudah dekat dosis berikutnya", hx('e8892b'), '?')
    return big

def s7(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=False, seed=4); counter(d); person(im, RAKA, 8, 112, t, happy=vt > 50.9, seed=5)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 40, 70); big = big.convert('RGBA')
    big_text(big, vt, 47.78, [("ANTIBIOTIK:", YELLOW)], y=330, size=62)
    if vt > 49.36: big_text(big, vt, 49.36, [("HABISKAN", GRN)], y=440, size=72)
    if vt > 50.98: big_text(big, vt, 50.98, [("WALAU SUDAH ENAKAN", None)], y=1500, size=46)
    return big

def s8(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=True, seed=4); counter(d); person(im, RAKA, 8, 112, t, talk=True, seed=5)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 40, 70); big = big.convert('RGBA')
    big_text(big, vt, 53.52, [("RAGU ATURAN", None), ("PAKAI OBAT?", YELLOW)], y=330, size=62)
    return big

def s9(t, lt):
    vt = t - O
    img = R2.sc_cta(lt).convert('RGBA')
    if vt > 58.24: ImageDraw.Draw(img).rectangle([0, 262, 1080, 452], fill=(16, 20, 32, 235))
    big_text(img, vt, 58.24, [("KONSULTASI DULU,", None), ("BARU MINUM.", YELLOW)], y=330, size=56)
    return img

VO_B = [4.2, 13.0, 23.5, 29.8, 39.6, 47.5, 53.2, 58.0]
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
        for tt in map(float, sys.argv[2:]): frame(tt).save(f"f_{tt:05.2f}.png")
        sys.exit()
    p = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{FW}x{FH}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',sys.argv[1]], stdin=subprocess.PIPE)
    n = int(TOTAL*FPS)
    for i in range(n):
        p.stdin.write(frame(i/FPS).tobytes())
        if i % 300 == 0: print(i, '/', n, flush=True)
    p.stdin.close(); p.wait(); print('done')
