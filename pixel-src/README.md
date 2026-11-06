# Seri Pixel Art — Apotek Berkah Sehat

Video edukasi obat format TikTok 1080×1920, 30 fps, gaya pixel art. Semua visual, musik, dan SFX dibuat dari kode (Python + PIL + numpy + ffmpeg), tanpa gambar eksternal. Suara VO dari Supertonic 3.

## Episode

| Ep | Topik | Video (root repo) | Render | Audio | VO | Timestamp kata |
|---|---|---|---|---|---|---|
| 1 | Salah kaprah antibiotik | `pixel-ep01-antibiotik.mp4` | `render3.py` | `audio3.py` | `vo/vo_st.wav` | `words/words_st.json` (+ `timemap.json`) |
| 2 | Herbal vs farmasi | `pixel-ep02-herbal-vs-farmasi.mp4` | `render4.py` | `audio4.py` | `vo/vo_herbal.wav` | `words/words_herbal.json` |
| 3 | Cara simpan obat | `pixel-ep03-simpan-obat.mp4` | `render5.py` | `audio5.py` | `vo/vo_simpan.wav` | `words/words_simpan.json` |
| 4 | Generik vs bermerek | `pixel-ep04-generik-vs-bermerek.mp4` | `render6.py` | `audio6.py` | `vo/vo_generik.wav` | `words/words_generik.json` |
| 5 | Cara minum obat | `pixel-ep05-cara-minum-obat.mp4` | `render7.py` | `audio7.py` | `vo/vo_minum.wav` | `words/words_minum.json` |
| 6 | Jangan campur obat | `pixel-ep06-jangan-campur-obat.mp4` | `render8.py` | `audio8.py` | `vo/vo_campur.wav` | `words/words_campur.json` |
| 7 | Efek samping obat | `pixel-ep07-efek-samping-obat.mp4` | `render9.py` | `audio9.py` | `vo/vo_efek.wav` | `words/words_efek.json` |

`render2.py` adalah engine inti: palet, sprite, kamera, lighting, kartu/teks HUD, transisi wipe, CTA. Episode berikutnya mengimpor episode sebelumnya, misalnya `render9` → `render8` → `render7` → `render6` → `render5` → `render4` → `render2`. Jadi jangan hapus file lama.

## Alur kerja per episode

1. Claude mengusulkan topik dan menulis naskah dengan tag ekspresi `<breath>`, `<sigh>`, `<laugh>`.
2. Abu membuat VO di Supertonic 3 lalu mengirim wav-nya.
3. Bersihkan VO dan buat versi 16 kHz untuk Whisper:
   ```bash
   ffmpeg -i input.wav -af "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=7" -ar 48000 -ac 1 vo/vo_X.wav
   ffmpeg -i vo/vo_X.wav -ar 16000 -ac 1 -f f32le vo_X16.raw
   ```
4. Ambil timestamp per kata dengan faster-whisper (model `medium`, int8, `word_timestamps=True`, `language='id'`). Input harus berupa array numpy float32, karena path file wav gagal dibaca.
5. Salin `renderN.py` dan `audioN.py` terakhir, lalu ganti isi adegan dan cue SFX. Aturan sinkron:
   - Waktu video = waktu VO + `O` (0,3 dtk).
   - Batas adegan (`VO_B`) diletakkan di jeda bicara.
6. Render dan mux (jalankan dari folder ini):
   ```bash
   python3 renderN.py stills 5.0 12.0 20.0   # cek frame
   python3 audioN.py                         # -> mix_vN.wav
   python3 renderN.py outN.mp4
   ffmpeg -i outN.mp4 -i mix_vN.wav -map 0:v -map 1:a -af loudnorm=I=-14:TP=-1.0:LRA=9 \
     -c:v copy -c:a aac -b:a 192k -shortest pixel-epNN-judul.mp4
   ```
   Hasilnya sekitar −15 LUFS.

## Kebutuhan

- Python 3 dengan `pillow`, `numpy`, dan `faster-whisper`
- `ffmpeg`
- Font sudah disertakan di folder ini: Press Start 2P dan Pixelify Sans, keduanya berlisensi SIL OFL.

## Catatan konten

- Klaim medis di setiap naskah perlu dicek APJ sebelum tayang.
- CTA memakai Jl. Sunan Muria No. 24, Kudus dan WA 0821-3626-9724, diambil dari episode 1. Pastikan data ini masih benar.

## Ide episode berikutnya

- Kapan ke dokter, kapan cukup ke apotek (sempat diusulkan untuk ep07, ditolak)
- Alergi obat
