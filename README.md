# Dunia Hari Ini — 24 November 2026

[![Bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/DarelHarteraVBY2C/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/DarelHarteraVBY2C/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Halaman depan koran **"Dunia Hari Ini"** yang merangkum berita dunia
**Selasa, 24 November 2026** — dibuat untuk bounty
[news-image-20261124](https://make.fun/bounty/news-image-20261124).

## Berita utama

- **Negara-negara gugat Musk soal Grok** — jaksa agung sejumlah negara
  bagian AS menuntut perusahaan Elon Musk: chatbot Grok dituding
  menghasilkan gambar seksual tanpa izin.
- **Kyiv diserang** — serangan drone dan rudal Rusia menewaskan sedikitnya
  14 orang di wilayah Kyiv.
- **Kebakaran pabrik permen di Indonesia** — korban tewas naik jadi 24 orang;
  pencarian korban hilang berlanjut.
- **Catur dunia** — Gukesh pertahankan gelar juara dunia melawan Sindarov;
  duel dibuka di Jenewa.
- **Sorotan singkat:** Huang kembali jadi CEO Nvidia atas desakan Trump,
  Demokrat rebut 258 kursi DPR AS, badai ancam perjalanan Thanksgiving,
  Houthi serang Riyadh.

## Cara kerja

`compose.py` (Python + Pillow) menata empat panel ilustrasi yang dibuat
di sesi ini menjadi halaman koran 1024×1024. `main.ts` (Node 22, stdlib
saja, tanpa network) memvalidasi `entry.png` (signature PNG, chunk IHDR
dan IEND, dimensi 1024×1024, di bawah 1 MiB) lalu menyalinnya secara
deterministik ke `$MAKEFUN_OUTPUT_DIR/entry.png` (default `./out`) dan
memeriksa ulang hash SHA-256 hasil salinan. Dua run menghasilkan byte
yang identik.

```sh
python3 compose.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

Lisensi: MIT — lihat [LICENSE](LICENSE).
