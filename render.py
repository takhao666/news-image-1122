#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

One image that sums up Sunday 22 November 2026: a newspaper front page
with a masthead naming the day, a lead story (COP31 climate talks in
Antalya), four illustrated stories and a France strip, plus an
"Also today" ticker. Every story happened or was first reported on
22 November 2026 (AP / AFP / Reuters via major outlets that day).

Run:  python3 render.py   -> writes entry.png next to this file.
Deterministic: fixed palette, fixed fonts, no randomness, no network.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
CARD = (255, 253, 247)
INK = (20, 20, 20)
RED = (168, 30, 30)
NAVY = (29, 58, 95)
TEAL = (14, 92, 86)
GOLD = (176, 124, 24)
GREY = (90, 86, 78)
LINE = (180, 172, 156)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r_out, r_in, fill):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_globe(draw, cx, cy, r):
    """Stylised globe: blue disc, meridians, green land blobs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 165),
                 outline=NAVY, width=3)
    for k in (-0.55, 0, 0.55):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 90 + k * 60, 270 + k * 60,
                 fill=(120, 175, 215), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(120, 175, 215), width=2)
    draw.ellipse([cx - r * 0.75, cy - r * 0.72, cx - r * 0.05, cy - r * 0.18],
                 fill=(74, 140, 74))
    draw.ellipse([cx + r * 0.08, cy + r * 0.05, cx + r * 0.72, cy + r * 0.62],
                 fill=(74, 140, 74))
    draw.ellipse([cx + r * 0.30, cy - r * 0.70, cx + r * 0.78, cy - r * 0.28],
                 fill=(96, 160, 82))


def draw_factory(draw, x, y, w, h):
    """Small factory with smokestacks and smoke puffs."""
    base = y + h
    draw.rectangle([x, base - h * 0.45, x + w, base], fill=(60, 60, 60))
    draw.rectangle([x + w * 0.10, base - h * 0.95, x + w * 0.28, base - h * 0.40],
                   fill=(50, 50, 50))
    draw.rectangle([x + w * 0.42, base - h * 0.80, x + w * 0.58, base - h * 0.40],
                   fill=(50, 50, 50))
    draw.rectangle([x + w * 0.70, base - h * 0.65, x + w * 0.84, base - h * 0.40],
                   fill=(50, 50, 50))
    for sx, sy, sr in ((0.19, 0.16, 13), (0.50, 0.26, 11), (0.77, 0.36, 10),
                       (0.30, 0.06, 9)):
        draw.ellipse([x + w * sx - sr, y + h * sy - sr,
                      x + w * sx + sr, y + h * sy + sr],
                     fill=(150, 148, 142))
    draw.rectangle([x, base - 4, x + w, base], fill=RED)


def fit_lines(draw, text, path, size, max_w, max_lines):
    """Shrink the font until the wrapped text fits in max_lines lines."""
    while size > 14:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, size)
    return fnt, wrap(draw, text, fnt, max_w)


def draw_flame(draw, cx, cy, s):
    outer = [(cx - s * 0.12, cy - s), (cx + s * 0.55, cy - s * 0.45),
             (cx + s * 0.68, cy + s * 0.05), (cx + s * 0.55, cy + s * 0.55),
             (cx + s * 0.18, cy + s * 0.88), (cx - s * 0.18, cy + s * 0.88),
             (cx - s * 0.60, cy + s * 0.50), (cx - s * 0.68, cy - s * 0.05),
             (cx - s * 0.45, cy - s * 0.50)]
    draw.polygon(outer, fill=(226, 88, 26))
    inner = [(cx - s * 0.05, cy - s * 0.42), (cx + s * 0.30, cy - s * 0.10),
             (cx + s * 0.34, cy + s * 0.30), (cx + s * 0.10, cy + s * 0.55),
             (cx - s * 0.12, cy + s * 0.55), (cx - s * 0.32, cy + s * 0.25),
             (cx - s * 0.30, cy - s * 0.08)]
    draw.polygon(inner, fill=(250, 196, 52))


def draw_boat(draw, cx, cy, s):
    draw.polygon([(cx - s, cy - s * 0.25), (cx + s, cy - s * 0.25),
                  (cx + s * 0.70, cy + s * 0.45), (cx - s * 0.70, cy + s * 0.45)],
                 fill=(70, 60, 52))
    draw.rectangle([cx - 3, cy - s * 1.05, cx + 3, cy - s * 0.25], fill=(70, 60, 52))
    draw.polygon([(cx + 3, cy - s * 1.05), (cx + s * 0.62, cy - s * 0.30),
                  (cx + 3, cy - s * 0.30)], fill=(240, 240, 235))
    for k, yy in enumerate((cy + s * 0.68, cy + s * 0.90)):
        draw.arc([cx - s - 8, yy - 10, cx - 8, yy + 10], 200, 340,
                 fill=(52, 110, 165), width=4)
        draw.arc([cx + 8, yy - 10, cx + s + 8, yy + 10], 200, 340,
                 fill=(52, 110, 165), width=4)


def draw_shield(draw, cx, cy, s):
    draw.polygon([(cx - s * 0.72, cy - s * 0.55), (cx + s * 0.72, cy - s * 0.55),
                  (cx + s * 0.72, cy + s * 0.10), (cx, cy + s * 0.85),
                  (cx - s * 0.72, cy + s * 0.10)], fill=NAVY)
    star(draw, cx, cy - s * 0.05, s * 0.42, s * 0.18, (250, 196, 52))


def draw_card(draw, cx, cy, s):
    draw.rounded_rectangle([cx - s, cy - s * 0.62, cx + s, cy + s * 0.62],
                           radius=12, fill=NAVY)
    draw.rectangle([cx - s, cy - s * 0.30, cx + s, cy - s * 0.02], fill=(220, 220, 210))
    draw.text((cx - s + 12, cy - s * 0.30), "10%", font=font(SANS_B, 26),
              fill=(250, 196, 52))
    draw.text((cx - s + 12, cy + s * 0.22), "CAP", font=font(SANS_B, 13),
              fill=(255, 255, 255))


def draw_megaphone(draw, cx, cy, s):
    # Cone pointing up-right, handle below, sound arcs.
    draw.polygon([(cx - s * 0.55, cy - s * 0.10), (cx + s * 0.30, cy - s * 0.75),
                  (cx + s * 0.75, cy - s * 0.35), (cx + s * 0.75, cy + s * 0.25),
                  (cx + s * 0.30, cy + s * 0.55), (cx - s * 0.55, cy + s * 0.35)],
                 fill=(255, 253, 247), outline=INK, width=2)
    draw.rectangle([cx - s * 0.35, cy + s * 0.30, cx - s * 0.05, cy + s * 0.85],
                   fill=RED)
    for r in (s * 0.95, s * 1.15):
        draw.arc([cx + s * 0.30 - r, cy - r, cx + s * 0.30 + r, cy + r],
                 -50, 50, fill=INK, width=3)


def icon_tile(draw, x, y, size, bg, painter):
    draw.rounded_rectangle([x, y, x + size, y + size], radius=10, fill=bg)
    painter(draw, x + size // 2, y + size // 2, size // 2 - 6)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # ---- Masthead -----------------------------------------------------
    d.text((W // 2, 28), "THE WORLD IN ONE DAY  ·  ONE PICTURE",
           font=font(SANS_B, 21), fill=RED, anchor="mt")
    d.text((W // 2, 54), "WORLD NEWS", font=font(SERIF_B, 82), fill=INK,
           anchor="mt")
    d.line([52, 152, 380, 152], fill=INK, width=2)
    d.line([644, 152, 972, 152], fill=INK, width=2)
    d.text((W // 2, 160), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 29),
           fill=INK, anchor="mt")
    d.text((W // 2, 198), "The day's biggest stories — from Antalya to Jakarta — in one image",
           font=font(SANS, 20), fill=GREY, anchor="mt")

    # ---- Lead story: COP31 -------------------------------------------
    lx, ly, lw, lh = 36, 230, 952, 274
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=LINE, width=2)
    d.rectangle([lx, ly, lx + 252, ly + 34], fill=RED)
    d.text((lx + 12, ly + 6), "LEAD STORY · CLIMATE", font=font(SANS_B, 18),
           fill=(255, 255, 255))
    head = "COP31 draft drops fossil fuels as talks run into overtime"
    hfnt, hlines = fit_lines(d, head, SANS_B, 36, 600, 2)
    y = text_block(d, lx + 24, ly + 46, hlines, hfnt, INK, hfnt.size + 7)
    body = ("A final draft released in Antalya early Sunday omits fossil "
            "fuels. About 130 nations want the phase-out pledge restored "
            "today.")
    bfnt, blines = fit_lines(d, body, SANS, 21, 600, 3)
    y = text_block(d, lx + 24, y + 8, blines, bfnt, INK, bfnt.size + 7)
    d.text((lx + 24, ly + lh - 32), "ANTALYA, TÜRKİYE  ·  AP / AFP",
           font=font(SANS_B, 17), fill=GREY)
    # illustration: globe over a factory skyline
    ix, iy = lx + 660, ly + 44
    d.rectangle([ix, iy, ix + 268, iy + 180], fill=(222, 236, 244),
                outline=LINE, width=1)
    draw_globe(d, ix + 82, iy + 82, 62)
    draw_factory(d, ix + 158, iy + 96, 96, 84)
    d.text((ix + 14, iy + 186), "CLIMATE SUMMIT IN OVERTIME",
           font=font(SANS_B, 15), fill=GREY)

    # ---- Four illustrated stories, 2 x 2 grid ------------------------
    stories = [
        ("INDONESIA", "Factory fire near Jakarta: 3 dead, dozens missing",
         "Fire at a confectionery factory; rescuers hunt for the missing.",
         (226, 88, 26), draw_flame),
        ("NIGERIA", "Boat capsizes on its way to a funeral: 24 dead",
         "The boat was carrying mourners when it overturned.",
         (52, 110, 165), draw_boat),
        ("EUROPE", "NATO: 'every inch' of Poland will be defended",
         "The vow follows a Russian airspace violation, allies say.",
         NAVY, draw_shield),
        ("UNITED STATES", "Trump vows a 10% cap on credit-card interest rates",
         "The president says he will work with Democrats to cap rates.",
         (14, 92, 86), draw_card),
    ]
    gx, gy, gw, gh, gap = 36, 518, 468, 160, 16
    for i, (tag, head, body, col, painter) in enumerate(stories):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + gap)
        d.rectangle([x, y, x + gw, y + gh], fill=CARD, outline=LINE, width=2)
        icon_tile(d, x + 14, y + 14, 108, col, painter)
        tx = x + 138
        d.text((tx, y + 10), tag, font=font(SANS_B, 16), fill=RED)
        hfnt, hlines = fit_lines(d, head, SANS_B, 23, gw - 152, 2)
        yy = text_block(d, tx, y + 32, hlines, hfnt, INK, hfnt.size + 5)
        bfnt, blines = fit_lines(d, body, SANS, 18, gw - 152, 2)
        text_block(d, tx, yy + 6, blines, bfnt, GREY, bfnt.size + 5)

    # ---- France strip --------------------------------------------------
    sx, sy, sw, sh = 36, 868, 952, 84
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=CARD, outline=LINE, width=2)
    icon_tile(d, sx + 12, sy + 10, 68, (90, 60, 110), draw_megaphone)
    d.text((sx + 96, sy + 12), "FRANCE", font=font(SANS_B, 16), fill=RED)
    d.text((sx + 96, sy + 34), "Sixth weekend of cost-of-living protests",
           font=font(SANS_B, 25), fill=INK)
    d.text((sx + 96, sy + 64),
           "Crowds rally again over prices and public services.  ·  AFP",
           font=font(SANS, 18), fill=GREY)

    # ---- Also-today ticker + sources ----------------------------------
    d.line([36, 964, 988, 964], fill=INK, width=2)
    d.text((36, 970),
           "ALSO TODAY:  6.7 quake hits Peru — no deaths reported  ·  "
           "EU proposes a tax on Big Tech",
           font=font(SANS_B, 18), fill=INK)
    d.text((36, 994), "Sources: AP, AFP, Reuters — all stories first reported "
           "22 November 2026", font=font(SANS, 15), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
