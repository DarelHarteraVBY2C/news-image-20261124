#!/usr/bin/env python3
"""Susun halaman depan koran 'Dunia Hari Ini' edisi 24 November 2026.

Membaca empat panel ilustrasi (webp) dari ./panels, menata masthead,
headline utama, tiga berita bergambar, dan strip berita singkat menjadi
satu PNG 1024x1024 di ./entry.png. Semua teks digambar dengan PIL.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (18, 18, 18)
NAVY = (16, 32, 64)
RED = (178, 34, 34)
BAND = (16, 32, 64)
BAND_TEXT = (245, 242, 231)
MUTED = (90, 84, 72)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Pecah teks menjadi baris-baris yang muat dalam max_w piksel."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_panel(path, tw, th):
    """Buka gambar, potong tengah ke rasio target, ubah ukuran."""
    img = Image.open(path).convert("RGB")
    sw, sh = img.size
    target = tw / th
    if sw / sh > target:
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def panel_file(stem):
    for name in sorted(os.listdir(PANELS)):
        if name.startswith(stem):
            return os.path.join(PANELS, name)
    raise FileNotFoundError(f"panel {stem} tidak ditemukan di {PANELS}")


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)
    mx = 36  # margin kiri/kanan

    # ---- Masthead ----
    mast = "DUNIA HARI INI"
    f_mast = SERIF_B(86)
    mw = d.textlength(mast, font=f_mast)
    d.text(((W - mw) / 2, 18), mast, font=f_mast, fill=NAVY)
    rule(d, mx, 118, W - mx, 4)
    f_date = SANS_B(26)
    date_line = "SELASA, 24 NOVEMBER 2026  •  EDISI DUNIA"
    dw = d.textlength(date_line, font=f_date)
    d.text(((W - dw) / 2, 130), date_line, font=f_date, fill=RED)
    rule(d, mx, 168, W - mx, 2)

    # ---- Headline utama + hero ----
    head = "NEGARA-NEGARA GUGAT MUSK SOAL GROK"
    f_head = SERIF_B(44)
    hl = wrap(d, head, f_head, 500)
    y = draw_lines(d, hl, mx, 186, f_head, INK, 52)
    sub = ("Jaksa agung sejumlah negara bagian AS menuntut "
           "perusahaan Elon Musk: chatbot Grok dituding "
           "menghasilkan gambar seksual tanpa izin.")
    f_sub = SANS(25)
    y = draw_lines(d, wrap(d, sub, f_sub, 500), mx, y + 8, f_sub, MUTED, 32)

    hero = fit_panel(panel_file("media-generation-panel-grok"), 400, 300)
    canvas.paste(hero, (W - mx - 400, 186))
    d.rectangle([W - mx - 400, 186, W - mx, 486], outline=INK, width=3)
    f_cap = SANS_B(19)
    d.text((W - mx - 400, 494), "GUGATAN GROK  •  WASHINGTON", font=f_cap, fill=RED)

    rule(d, mx, 530, W - mx, 2)

    # ---- Tiga berita bergambar ----
    stories = [
        ("media-generation-panel-kyiv", "KYIV DISERANG",
         "Serangan drone dan rudal Rusia menewaskan sedikitnya "
         "14 orang di wilayah Kyiv."),
        ("media-generation-panel-factory", "PABRIK INDONESIA",
         "Korban tewas kebakaran pabrik permen naik jadi 24; "
         "pencarian korban hilang berlanjut."),
        ("media-generation-panel-chess", "CATUR DUNIA",
         "Gukesh pertahankan gelar juara dunia melawan Sindarov; "
         "duel dibuka di Jenewa."),
    ]
    col_w, gap = 300, 14
    x = mx
    y0 = 544
    for stem, kick, body in stories:
        img = fit_panel(panel_file(stem), col_w, 185)
        canvas.paste(img, (x, y0))
        d.rectangle([x, y0, x + col_w, y0 + 185], outline=INK, width=2)
        yy = y0 + 195
        d.text((x, yy), kick, font=SANS_B(22), fill=RED)
        yy = draw_lines(d, wrap(d, body, SANS(20), col_w), x, yy + 28,
                        SANS(20), INK, 25)
        x += col_w + gap

    # ---- Strip berita singkat ----
    band_y = 872
    d.rectangle([0, band_y, W, band_y + 96], fill=BAND)
    f_tick = SANS_B(23)
    tick = ("NVIDIA: HUANG KEMBALI JADI CEO ATAS DESAKAN TRUMP   •   "
            "DEMOKRAT REBUT 258 KURSI DPR AS   •   BADAI ANCAM "
            "PERJALANAN THANKSGIVING   •   HOUTHI SERANG RIYADH")
    ty = draw_lines(d, wrap(d, tick, f_tick, W - 2 * mx), mx, band_y + 12,
                    f_tick, BAND_TEXT, 30)

    # ---- Footer ----
    f_foot = SANS(19)
    foot = "Dunia Hari Ini — rangkuman berita dunia Selasa, 24 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 984), foot, font=f_foot, fill=MUTED)

    canvas.save(OUT_PATH, "PNG", optimize=True)
    size = os.path.getsize(OUT_PATH)
    print(f"entry.png: {size} byte, {W}x{H}")
    if size > 1048576:
        print("PERINGATAN: melebihi 1 MiB", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
