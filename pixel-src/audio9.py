#!/usr/bin/env python3
"""Ep7 - Chiptune bed + SFX generated from code, mixed under the VO with sidechain ducking."""
import numpy as np, wave
SR = 48000; O = 0.3; TOTAL = 55.6
def T(x): return x + O
N = int(TOTAL * SR)
rng = np.random.default_rng(9)

def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a=.005, r=.1):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4)); return e
def sq(f, d, duty=.5):
    t = tt(d); return np.where((t * f) % 1 < duty, 1., -1.)
def tri(f, d):
    t = tt(d); p = (t * f) % 1; return 4 * np.abs(p - .5) - 1
def sine(f, d): return np.sin(2 * np.pi * f * tt(d))
def noise(d): return rng.uniform(-1, 1, int(d * SR))
def lp(x, a=.1):
    y = np.empty_like(x); acc = 0.
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def lp_fast(x, k=8):
    return np.convolve(x, np.ones(k) / k, mode='same')
def place(buf, x, at, gain=1.):
    i = int(at * SR); j = min(len(buf), i + len(x))
    if i < len(buf) and j > i: buf[i:j] += x[:j - i] * gain
def mid(n): return 440 * 2 ** ((n - 69) / 12)

# ---------- music: C G Am F, 112 bpm ----------
bpm = 112; beat = 60 / bpm; bar = beat * 4
prog = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [57, 60, 64]), (41, [57, 60, 65])]
mus = np.zeros(N)
nbars = int(TOTAL / bar) + 1
for b in range(nbars):
    root, chord = prog[b % 4]; t0 = b * bar
    for k in range(8):  # bass eighths
        n = root if k % 2 == 0 else root + 12
        x = tri(mid(n), beat / 2 * .9) * env(int(beat / 2 * .9 * SR), .003, .25); place(mus, x, t0 + k * beat / 2, .55)
    for k in range(16):  # arp sixteenths
        n = chord[k % 3] + (12 if (k // 3) % 2 else 0)
        x = sq(mid(n), beat / 4 * .8, .25) * env(int(beat / 4 * .8 * SR), .002, .06); place(mus, x, t0 + k * beat / 4, .11)
    for k in range(4):  # kick + hat
        if k in (0, 2):
            d = .18; t = tt(d); f = 120 * np.exp(-t * 25) + 45
            x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .08); place(mus, x, t0 + k * beat, .6)
        else:
            x = noise(.05) * env(int(.05 * SR), .001, .012); place(mus, x - lp_fast(x, 6), t0 + k * beat, .25)
        x = noise(.03) * env(int(.03 * SR), .001, .008); place(mus, x - lp_fast(x, 4), t0 + k * beat + beat / 2, .12)
    if b % 2 == 1:  # little lead hook every other bar
        mel = [chord[2] + 12, chord[1] + 12, chord[0] + 12, chord[1] + 12]
        for k, n in enumerate(mel):
            x = sq(mid(n), beat * .45, .5) * env(int(beat * .45 * SR), .004, .18); place(mus, x, t0 + 2 * beat + k * beat / 2, .07)
# mute music during rewind, fade at end
m = np.ones(N)
fade = int(1.2 * SR); m[-fade:] *= np.linspace(1, 0, fade)
mus *= m

# ---------- SFX ----------
sfx = np.zeros(N)
def whoosh(d=.28):
    x = noise(d); x = x - lp_fast(x, 30); e = np.sin(np.linspace(0, np.pi, len(x))) ** 2; return x * e
def click(): x = noise(.03) * env(int(.03 * SR), .0005, .006) + sine(2200, .03) * env(int(.03 * SR), .0005, .01) * .6; return x
def thud(): d = .35; t = tt(d); f = 90 * np.exp(-t * 12) + 38; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .15)
def blip(f=1320, d=.09): return sq(f, d, .5) * env(int(d * SR), .001, .04)
def buzz(): return (sq(110, .18, .5) + sq(116, .18, .5)) * .5 * env(int(.18 * SR), .001, .08)
def popx(): d = .1; t = tt(d); f = 900 * np.exp(-t * 30) + 180; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .04)
def tear(): x = noise(.09); x = x - lp_fast(x, 3); return x * env(len(x), .002, .03)
def ding(): return (sine(1568, .7) + .5 * sine(2349, .7) + .25 * sine(3136, .7)) * env(int(.7 * SR), .002, .25)
def sparkle():
    out = np.zeros(int(.5 * SR))
    for k, n in enumerate([84, 88, 91, 96]): place(out, sine(mid(n), .2) * env(int(.2 * SR), .001, .07), k * .06, .6)
    return out
def powerup():
    out = np.zeros(int(.7 * SR))
    for k, n in enumerate([60, 64, 67, 72, 76, 79, 84, 88]): place(out, sq(mid(n), .07, .5) * env(int(.07 * SR), .001, .05), k * .055)
    return out
def jingle():
    out = np.zeros(int(1.4 * SR))
    for k, (n, d) in enumerate([(72, .12), (76, .12), (79, .12), (84, .5)]):
        place(out, (sq(mid(n), d + .1, .25) * .6 + tri(mid(n - 12), d + .1)) * env(int((d + .1) * SR), .002, d), [0, .13, .26, .39][k])
    return out
def rewind():
    d = 1.2; t = tt(d); f = 900 + 500 * np.sin(2 * np.pi * 14 * t) - 400 * t
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + noise(d) * .25
    x = x - lp_fast(x, 10); return x * np.minimum(1, t / .05) * np.minimum(1, (d - t) / .1)
def rain(d):
    x = noise(d); x = lp_fast(x, 5) - lp_fast(x, 60)
    for k in range(int(d * 14)):
        i = rng.integers(0, len(x) - 2000); x[i:i + 1200] += noise(.025) * env(1200, .0005, .004) * .8
    e = np.minimum(1, tt(d) / .3) * np.minimum(1, (d - tt(d)) / .3); return x * e

def scan_sweep():
    d = 1.6; t = tt(d); f = 300 + 1200 * (t / d)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * .4 + noise(d) * .1) * np.minimum(1, t / .05) * np.minimum(1, (d - t) / .1)
def zapfx():
    d = .5; x = noise(d) * env(len(noise(d)), .001, .12)
    t = tt(d); return (x * .6 + sq(180, d, .5) * .3 * np.exp(-t * 6)) * (rng.uniform(0, 1, len(t)) > .35)
def dropfx():
    d = .18; t = tt(d); f = 1100 * np.exp(-t * 14) + 200; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .08)
for b in [5.3,17.4,30.6,34.3,40.7,46.6,52.0]: place(sfx, whoosh(), T(b) - .2, .35)
place(sfx, popx(), T(1.74), .45); place(sfx, popx(), T(2.96), .45)
place(sfx, buzz(), T(4.74), .3)
for at in (9.26, 10.14, 10.9): place(sfx, blip(990, .1), T(at), .35)
place(sfx, ding(), T(13.16), .3); place(sfx, blip(1320, .09), T(14.74), .35)
for at in (19.5, 22.08, 23.84, 24.78): place(sfx, buzz(), T(at), .25)
place(sfx, thud(), T(26.2), .7); place(sfx, ding(), T(29.36), .3)
place(sfx, buzz(), T(31.84), .25)
place(sfx, buzz(), T(38.38), .25); place(sfx, blip(660, .1), T(39.82), .3)
for at in (41.4, 42.0, 42.6): place(sfx, click(), T(at), .5)
place(sfx, ding(), T(43.02), .3); place(sfx, thud(), T(44.78), .5)
place(sfx, sparkle(), T(49.42), .4)
place(sfx, jingle(), T(52.26), .45)
# ---------- VO + ducking ----------
w = wave.open('vo/vo_efek.wav'); vo = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
assert w.getframerate() == SR
vbuf = np.zeros(N); place(vbuf, vo, O)
lvl = np.convolve(np.abs(vbuf), np.ones(4800) / 4800, mode='same')
duck = 1 - 0.55 * np.clip(lvl / 0.04, 0, 1)
duck = np.convolve(duck, np.ones(9600) / 9600, mode='same')
mix = vbuf * 1.0 + mus * duck * 0.5 + sfx * 0.9
peak = np.max(np.abs(mix)); mix = mix / max(peak, 1) * 0.95
out = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
with wave.open('mix_v9.wav', 'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(out.tobytes())
print('peak', peak, 'len', len(out) / SR)
