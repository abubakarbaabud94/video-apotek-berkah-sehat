#!/usr/bin/env python3
"""Episode 7 - Efek samping obat: wajar atau bahaya."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance
from render8 import *
import render2 as R2
O = 0.3; TOTAL = 55.6
ORG = hx('e8892b')

def s1(t, lt):
    vt = t - O
    im, d = counter_world(t); boxes_pair(im, d)
    person(im, RAKA, 37, 142, t, talk=vt < 5.2, sick=vt < 5.2, seed=1)
    big, cam = camera(im, 1.0, 45, 80, shake=(3 if 4.74 < vt < 5.1 else 0), t=t); big = big.convert('RGBA')
    big_text(big, vt, 0.0, [("HABIS MINUM OBAT", None)], y=330, size=50)
    chip(big, 270, 590, "MUAL", ORG, vt, 1.74, 30)
    chip(big, 810, 590, "NGANTUK", hx('7a3fa0'), vt, 2.96, 30)
    if vt > 3.58: big_text(big, vt, 3.58, [("WAJAR?", GRN)], y=1180, size=72)
    if vt > 4.74: big_text(big, vt, 4.74, [("ATAU BAHAYA?", RED)], y=1300, size=64)
    return big

def s2(t, lt):
    vt = t - O
    im, d = bench(t)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 5.5, [("SEMUA OBAT", YELLOW), ("PUNYA EFEK SAMPING", None)], y=330, size=54)
    check_row(big, vt - 9.26, 640, "MUAL", "efek ringan di awal", ORG)
    check_row(big, vt - 10.14, 820, "MENGANTUK", "efek ringan di awal", ORG)
    check_row(big, vt - 10.9, 1000, "MULUT KERING", "efek ringan di awal", ORG)
    if vt > 13.16: big_text(big, vt, 13.16, [("SERING HILANG SENDIRI", GRN)], y=1290, size=44)
    if vt > 14.74: big_text(big, vt, 14.74, [("CEK BROSUR KEMASAN", YELLOW)], y=1450, size=46)
    if vt > 16.3: big_text(big, vt, 16.3, [("ATAU TANYA APOTEKER", None)], y=1560, size=40)
    return big

def s3(t, lt):
    vt = t - O
    im, d = scanlab(t)
    pulse = .5 + .5 * math.sin(vt * 9)
    im = light(im, (.85, .85, .85), [(45, 50, 70, .45 * pulse, (1.0, .1, .1))])
    big, cam = camera(im, 1.0, 45, 80, shake=(5 if 26.2 < vt < 26.6 else 0), t=t); big = big.convert('RGBA')
    big_text(big, vt, 17.7, [("WASPADA!", RED)], y=330, size=64)
    if vt > 18.94: big_text(big, vt, 18.94, [("KALAU MUNCUL", None)], y=430, size=44)
    mark_row(big, vt - 19.5, 540, "BENTOL & GATAL", "di seluruh badan", RED, 'x')
    mark_row(big, vt - 22.08, 720, "BIBIR/MATA BENGKAK", "bibir atau kelopak mata", RED, 'x')
    mark_row(big, vt - 23.84, 900, "SESAK NAPAS", "sulit bernapas", RED, 'x')
    mark_row(big, vt - 24.78, 1080, "NYARIS PINGSAN", "hampir tidak sadar", RED, 'x')
    if vt > 26.2: stamp(big, 540, 1380, "TANDA ALERGI!", 64, RED, -6, shake=(8 if vt < 26.6 else 0))
    if vt > 27.16: big_text(big, vt, 27.16, [("HENTIKAN OBATNYA", YELLOW)], y=1540, size=46)
    if vt > 29.36: big_text(big, vt, 29.36, [("CARI BANTUAN MEDIS", GRN)], y=1650, size=44)
    return big

def clock(d, cx, cy, vt, at):
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=INK); d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=hx('f6f1e3'))
    for k in range(12):
        a = k * math.pi / 6; R(d, int(cx + math.sin(a) * 11), int(cy - math.cos(a) * 11), 1, 1, INK)
    a = (vt - at) * 3.2; d.line([(cx, cy), (cx + math.sin(a) * 11, cy - math.cos(a) * 11)], fill=RED, width=1)
    a2 = (vt - at) * .4; d.line([(cx, cy), (cx + math.sin(a2) * 7, cy - math.cos(a2) * 7)], fill=INK, width=1)

def s4(t, lt):
    vt = t - O
    im, d = bench(t); clock(d, 45, 62, vt, 30.86)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 30.86, [("JANGAN MENUNGGU", RED)], y=330, size=56)
    mark_row(big, vt - 31.84, 1100, "JANGAN TUTUPI GEJALA", "dengan obat lain", RED, 'x')
    return big

def s5(t, lt):
    vt = t - O
    im, d = bench(t); sp(im, BOTTLE, 'jb', 36, 40, {'C': 'P'}, k=3)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 34.6, [("EFEK RINGAN", YELLOW), ("TAPI MENGGANGGU?", None)], y=330, size=50)
    if vt > 35.6: label(big, (540, 985), "OBAT DOKTER", 36, YELLOW, F_TITLE)
    mark_row(big, vt - 38.38, 1050, "BERHENTI SENDIRI", "untuk obat dari dokter", RED, 'x')
    mark_row(big, vt - 39.82, 1240, "TANYAKAN DULU", "ke apoteker atau dokter", ORG, '?')
    return big

def s6(t, lt):
    vt = t - O
    im, d = bench(t)
    R(d, 26, 38, 38, 46, INK); R(d, 27, 39, 36, 44, hx('f6f1e3')); R(d, 27, 39, 4, 44, hx('c94a4a'))
    n = max(0, min(5, int((vt - 41.4) / .55)))
    for i in range(n): R(d, 35, 47 + i * 6, 22 - (i % 3) * 4, 2, hx('3a3a4a'))
    sp(im, PEN, 'pen', 52, 44 + n * 6, k=1)
    big, cam = camera(im, 1.0, 45, 80); big = big.convert('RGBA')
    big_text(big, vt, 41.0, [("CATAT NAMA", YELLOW), ("OBAT PENYEBAB", None)], y=330, size=50)
    check_row(big, vt - 43.02, 1000, "KABARI APOTEKER", "dan dokter", GREEN)
    if vt > 44.78: big_text(big, vt, 44.78, [("SUPAYA TIDAK", None), ("DIBERIKAN LAGI", RED)], y=1300, size=48)
    return big

def s7(t, lt):
    vt = t - O
    im, d = apotek_int(t)
    person(im, APT, 58, 88, t, talk=vt > 49.4, seed=4); counter(d); person(im, RAKA, 8, 112, t, talk=vt < 49.4, seed=5)
    im = light(im, (1, 1, 1), [(20, 6, 30, .2, (1, 1, .9)), (66, 6, 30, .2, (1, 1, .9))])
    big, cam = camera(im, 1.1, 40, 70); big = big.convert('RGBA')
    big_text(big, vt, 47.06, [("RAGU EFEK SAMPING", None), ("WAJAR ATAU TIDAK?", YELLOW)], y=330, size=48)
    if vt > 49.42: big_text(big, vt, 49.42, [("TANYA", None), ("APOTEKER KAMI", GRN)], y=1450, size=56)
    return big

def s8(t, lt):
    vt = t - O
    img = R2.sc_cta(lt).convert('RGBA')
    if vt > 52.26: ImageDraw.Draw(img).rectangle([0, 262, 1080, 452], fill=(16, 20, 32, 235))
    big_text(img, vt, 52.26, [("KONSULTASI DULU,", None), ("BARU MINUM.", YELLOW)], y=330, size=56)
    return img

VO_B = [5.3, 17.4, 30.6, 34.3, 40.7, 46.6, 52.0]
_B = [0] + [b + O for b in VO_B] + [TOTAL]
_F = [s1, s2, s3, s4, s5, s6, s7, s8]
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
