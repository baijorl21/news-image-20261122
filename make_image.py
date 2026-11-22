#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up the world news of
Sunday 22 November 2026.

Everything is drawn from scratch with PIL primitives - no photos, no
downloaded assets, no randomness - so the output is byte-for-byte
deterministic. The entry program (main.py) copies the PNG this script
writes to /output/entry.png.

Layout (1024 x 1024):
  - masthead band naming the day
  - six story panels (2 columns x 3 rows), each with a simple icon,
    a bold headline and a one-line summary
  - a bottom strip with four shorter items
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PAPER = (247, 243, 234)
INK = (24, 24, 28)
NAVY = (20, 33, 61)
GOLD = (252, 163, 17)
RED = (192, 57, 43)
TEAL = (0, 128, 128)
CARD = (255, 255, 255)
GREY = (90, 90, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def center_text(draw, cx, y, text, fnt, fill):
    w, _ = text_size(draw, text, fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_size(draw, trial, fnt)[0] <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons

def icon_globe(draw, x, y, s):
    """Globe with a thermometer: the climate talks."""
    cx, cy, r = x + s * 0.42, y + s * 0.52, s * 0.34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=7)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=TEAL, width=4)
    draw.line([cx - r, cy, cx + r, cy], fill=TEAL, width=4)
    draw.line([cx - r * 0.85, cy - r * 0.5, cx + r * 0.85, cy - r * 0.5], fill=TEAL, width=4)
    draw.line([cx - r * 0.85, cy + r * 0.5, cx + r * 0.85, cy + r * 0.5], fill=TEAL, width=4)
    # thermometer at the right edge
    tx = x + s * 0.86
    draw.rounded_rectangle([tx - 9, y + s * 0.12, tx + 9, y + s * 0.72], radius=9,
                           outline=RED, width=5)
    draw.rectangle([tx - 4, y + s * 0.30, tx + 4, y + s * 0.72], fill=RED)
    draw.ellipse([tx - 16, y + s * 0.66, tx + 16, y + s * 0.98], outline=RED, width=5, fill=RED)


def icon_badge(draw, x, y, s):
    """Shield badge with a star: the cartel boss captured."""
    cx = x + s * 0.5
    top, bot = y + s * 0.08, y + s * 0.94
    left, right = x + s * 0.16, x + s * 0.84
    draw.polygon([(left, top), (right, top), (right, y + s * 0.55),
                  (cx, bot), (left, y + s * 0.55)], outline=NAVY, width=7)
    # star
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = s * 0.22 if i % 2 == 0 else s * 0.09
        pts.append((cx + rad * math.cos(ang), y + s * 0.42 + rad * math.sin(ang)))
    draw.polygon(pts, fill=GOLD, outline=INK)
    draw.line([left + 12, y + s * 0.66, right - 12, y + s * 0.66], fill=NAVY, width=5)


def icon_missile(draw, x, y, s):
    """Ballistic missile arcing down: the strike on Kryvyi Rih."""
    import math
    cx, cy = x + s * 0.55, y + s * 0.45
    ang = math.radians(38)
    length, width = s * 0.78, s * 0.20

    def rot(px, py):
        return (cx + px * math.cos(ang) - py * math.sin(ang),
                cy + px * math.sin(ang) + py * math.cos(ang))

    body = [rot(-length / 2, -width / 2), rot(length / 2 - s * 0.14, -width / 2),
            rot(length / 2, 0), rot(length / 2 - s * 0.14, width / 2),
            rot(-length / 2, width / 2)]
    draw.polygon(body, fill=(70, 74, 84), outline=INK)
    fin1 = [rot(-length / 2, -width / 2), rot(-length / 2 - s * 0.13, -width * 1.15),
            rot(-length / 2 + s * 0.10, -width / 2)]
    fin2 = [rot(-length / 2, width / 2), rot(-length / 2 - s * 0.13, width * 1.15),
            rot(-length / 2 + s * 0.10, width / 2)]
    draw.polygon(fin1, fill=RED, outline=INK)
    draw.polygon(fin2, fill=RED, outline=INK)
    flame = [rot(-length / 2 - s * 0.02, -width * 0.32), rot(-length / 2 - s * 0.30, 0),
             rot(-length / 2 - s * 0.02, width * 0.32)]
    draw.polygon(flame, fill=GOLD, outline=INK)
    # ground line
    draw.line([x + s * 0.08, y + s * 0.92, x + s * 0.92, y + s * 0.92], fill=INK, width=6)


def icon_ship(draw, x, y, s):
    """Cargo ship with a drone above it: the Baltic strike."""
    # hull
    draw.polygon([(x + s * 0.08, y + s * 0.62), (x + s * 0.92, y + s * 0.62),
                  (x + s * 0.80, y + s * 0.84), (x + s * 0.22, y + s * 0.84)],
                 fill=NAVY, outline=INK)
    # containers
    for i, col in enumerate([RED, TEAL, GOLD]):
        bx = x + s * (0.20 + i * 0.22)
        draw.rectangle([bx, y + s * 0.40, bx + s * 0.19, y + s * 0.62],
                       fill=col, outline=INK, width=3)
    # waves
    for i in range(3):
        wy = y + s * (0.90 + i * 0.045)
        draw.arc([x + s * 0.10, wy - 8, x + s * 0.40, wy + 8], 180, 360, fill=TEAL, width=4)
        draw.arc([x + s * 0.42, wy - 8, x + s * 0.72, wy + 8], 180, 360, fill=TEAL, width=4)
        draw.arc([x + s * 0.74, wy - 8, x + s * 1.00, wy + 8], 180, 360, fill=TEAL, width=4)
    # drone: X arms with rotors
    dx, dy = x + s * 0.68, y + s * 0.16
    draw.line([dx - 22, dy - 12, dx + 22, dy + 12], fill=INK, width=5)
    draw.line([dx - 22, dy + 12, dx + 22, dy - 12], fill=INK, width=5)
    draw.ellipse([dx - 8, dy - 8, dx + 8, dy + 8], fill=RED, outline=INK)
    for ox, oy in [(-22, -12), (22, -12), (-22, 12), (22, 12)]:
        draw.line([dx + ox - 11, dy + oy, dx + ox + 11, dy + oy], fill=INK, width=4)


def icon_parliament(draw, x, y, s):
    """Columned building: coalition talks in Israel."""
    draw.polygon([(x + s * 0.10, y + s * 0.30), (x + s * 0.50, y + s * 0.08),
                  (x + s * 0.90, y + s * 0.30)], fill=NAVY, outline=INK)
    draw.rectangle([x + s * 0.14, y + s * 0.34, x + s * 0.86, y + s * 0.40],
                   fill=NAVY, outline=INK)
    for i in range(4):
        cx = x + s * (0.22 + i * 0.19)
        draw.rectangle([cx, y + s * 0.44, cx + s * 0.07, y + s * 0.80],
                       fill=(200, 204, 214), outline=INK, width=3)
    draw.rectangle([x + s * 0.12, y + s * 0.84, x + s * 0.88, y + s * 0.92],
                   fill=NAVY, outline=INK)
    draw.ellipse([x + s * 0.44, y + s * 0.16, x + s * 0.56, y + s * 0.28], fill=GOLD, outline=INK)


def icon_quake(draw, x, y, s):
    """Seismograph trace over cracked ground: the Peru earthquake."""
    draw.rectangle([x + s * 0.06, y + s * 0.10, x + s * 0.94, y + s * 0.62],
                   outline=INK, width=5)
    mid = y + s * 0.36
    pts = []
    xs = [0.10, 0.22, 0.30, 0.36, 0.44, 0.50, 0.56, 0.64, 0.72, 0.90]
    ys = [0.36, 0.36, 0.20, 0.52, 0.14, 0.58, 0.24, 0.48, 0.36, 0.36]
    for fx, fy in zip(xs, ys):
        pts.append((x + s * fx, y + s * fy))
    draw.line(pts, fill=RED, width=6)
    # cracked ground
    gy = y + s * 0.80
    draw.line([x + s * 0.06, gy, x + s * 0.40, gy], fill=INK, width=6)
    draw.line([x + s * 0.40, gy, x + s * 0.48, gy + s * 0.10], fill=INK, width=5)
    draw.line([x + s * 0.48, gy + s * 0.10, x + s * 0.58, gy], fill=INK, width=5)
    draw.line([x + s * 0.58, gy, x + s * 0.94, gy], fill=INK, width=6)


# ---------------------------------------------------------------- layout

STORIES = [
    (icon_globe, RED, "COP31 DEADLOCK",
     "Talks stall over fossil fuels in Antalya"),
    (icon_badge, NAVY, "CARTEL BOSS SEIZED",
     "Mexico captures 'El Chapo Isidro' in Sinaloa"),
    (icon_missile, RED, "MISSILES HIT KRYVYI RIH",
     "Russia strikes Zelensky's hometown"),
    (icon_ship, TEAL, "BALTIC SHIP DRONE STRIKE",
     "Russian cargo ship hit; Finland on alert"),
    (icon_parliament, NAVY, "ISRAEL COALITION TALKS",
     "Eisenkot invites Netanyahu's Likud"),
    (icon_quake, RED, "PERU QUAKE 6.9",
     "Andes tremor shakes Lima; no casualties"),
]

STRIP = [
    "GULF TENSIONS: Iran strikes a US base in Kuwait; tankers hit off Oman",
    "JAPAN-INDIA DEFENCE PACT: first live-fire training on Indian ranges",
    "FRANCE: sixth Saturday of cost-of-living protests, turnout falls",
    "WHALE GENOMES: drones sequence humpback DNA from breath off Canada",
]


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 150], fill=NAVY)
    draw.rectangle([0, 150, W, 158], fill=GOLD)
    center_text(draw, W / 2, 14, "THE WORLD IN ONE DAY", font(SERIF_B, 58), PAPER)
    center_text(draw, W / 2, 92, "SUNDAY  -  22 NOVEMBER 2026", font(BOLD, 38), GOLD)


def draw_panel(draw, x, y, w, h, icon, accent, headline, summary):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD, outline=INK, width=3)
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=8, fill=accent)
    draw.rectangle([x, y + 8, x + w, y + 16], fill=accent)
    icon(draw, x + 18, y + 30, 150)
    tx = x + 182
    f_head = font(BOLD, 31)
    lines = wrap(draw, headline, f_head, w - 200)
    ty = y + 32
    for line in lines[:3]:
        draw.text((tx, ty), line, font=f_head, fill=INK)
        ty += 37
    f_sub = font(REG, 23)
    for line in wrap(draw, summary, f_sub, w - 200)[:3]:
        draw.text((tx, ty + 2), line, font=f_sub, fill=GREY)
        ty += 29


def draw_strip(draw, y):
    draw.rectangle([0, y, W, H], fill=NAVY)
    draw.rectangle([0, y, W, y + 6], fill=GOLD)
    center_text(draw, W / 2, y + 14, "ALSO TODAY", font(BOLD, 30), GOLD)
    f_item = font(REG, 24)
    ty = y + 58
    for item in STRIP:
        draw.ellipse([34, ty + 8, 46, ty + 20], fill=GOLD)
        draw.text((58, ty), item, font=f_item, fill=PAPER)
        ty += 34


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    margin, gap = 22, 14
    pw = (W - 2 * margin - gap) // 2
    ph = 204
    top = 172
    for i, (icon, accent, headline, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        draw_panel(draw, x, y, pw, ph, icon, accent, headline, summary)
    draw_strip(draw, top + 3 * (ph + gap) + 2)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
