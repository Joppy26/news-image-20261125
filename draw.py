#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125.

One 1024x1024 newspaper-style front page summing up Wednesday
25 November 2026 from five stories verified as first reported that day:
  1. Australia formally apologises to LGBTQ veterans (Reuters, 25 Nov).
  2. Asian chip stocks crash (Taiwan -7.2%, Korea -5.4%, Japan -3.3%).
  3. International Day for the Elimination of Violence against Women.
  4. Bitcoin slips below $60,000.
  5. Australia CPI jumps to 4.9%; Japan services prices +4.2%.

Everything is drawn from scratch with PIL + DejaVu fonts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (13, 27, 48)
NAVY2 = (18, 38, 66)
WHITE = (255, 255, 255)
INK = (18, 24, 34)
GREY = (90, 100, 115)
AMBER = (255, 176, 32)
RED = (214, 48, 49)
ORANGE = (232, 106, 24)
GOLD = (247, 147, 26)
TEAL = (0, 140, 140)
RAINBOW = [(228, 59, 59), (245, 130, 32), (252, 212, 61),
           (74, 174, 84), (45, 110, 190), (130, 70, 160)]
CARD = (248, 249, 251)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

# ---------- header ----------
d.rectangle([0, 0, W, 168], fill=NAVY2)
d.rectangle([0, 164, W, 168], fill=AMBER)
center_text(d, W // 2, 26, "25 NOVEMBER 2026", font(FB, 78), WHITE)
center_text(d, W // 2, 126, "WEDNESDAY  ·  THE WORLD IN ONE IMAGE",
            font(FB, 26), AMBER)

# ---------- layout ----------
MX, GAP = 16, 12
TOP = 184
ROW1_H, ROW2_H = 372, 436
row1_w = (W - 2 * MX - GAP) // 2
row2_w = (W - 2 * MX - 2 * GAP) // 3


def card(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD)
    d.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)
    d.rounded_rectangle([x, y + 5, x + w, y + 10], fill=accent)


def panel_text(x, y, w, headline, sub, accent, head_size=30, sub_size=20):
    hf, sf = font(FB, head_size), font(FR, sub_size)
    lines = wrap(d, headline, hf, w - 28)
    ly = y
    for ln in lines:
        center_text(d, x + w // 2, ly, ln, hf, INK)
        ly += head_size + 4
    lines2 = wrap(d, sub, sf, w - 28)
    ly += 4
    for ln in lines2:
        center_text(d, x + w // 2, ly, ln, sf, GREY)
        ly += sub_size + 4
    return ly


# ---------- panel 1: Australia apology ----------
x, y = MX, TOP
card(x, y, row1_w, ROW1_H, RAINBOW[3])
# rainbow stripes across the illustration band
bx, by, bw, bh = x + 24, y + 26, row1_w - 48, 178
for i, c in enumerate(RAINBOW):
    d.rectangle([bx, by + i * bh // 6, bx + bw, by + (i + 1) * bh // 6],
                fill=c)
# parliament silhouette on top of the stripes
px, py = bx + bw // 2, by + bh
d.polygon([(px - 150, py), (px, py - 88), (px + 150, py)], fill=NAVY)
d.rectangle([px - 118, py - 46, px + 118, py], fill=NAVY)
d.rectangle([px - 3, py - 118, px + 3, py - 78], fill=NAVY)
d.polygon([(px + 3, py - 118), (px + 42, py - 108), (px + 3, py - 98)],
          fill=AMBER)
d.rectangle([px - 88, py - 30, px + 88, py - 12], fill=WHITE)
panel_text(x, y + 224, row1_w, "AUSTRALIA SAYS SORRY",
           "LGBTQ veterans get a formal apology in parliament",
           RAINBOW[3])

# ---------- panel 2: chip stocks crash ----------
x = MX + row1_w + GAP
card(x, y, row1_w, ROW1_H, RED)
bx, by, bw, bh = x + 24, y + 26, row1_w - 48, 178
# chip
cx, cy, s = bx + 78, by + bh // 2, 92
d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
            fill=NAVY2, outline=AMBER, width=4)
d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=AMBER)
for i in range(5):
    off = -40 + i * 20
    d.rectangle([cx + off - 3, cy - s // 2 - 16, cx + off + 3, cy - s // 2],
                fill=GREY)
    d.rectangle([cx + off - 3, cy + s // 2, cx + off + 3, cy + s // 2 + 16],
                fill=GREY)
    d.rectangle([cx - s // 2 - 16, cy + off - 3, cx - s // 2, cy + off + 3],
                fill=GREY)
    d.rectangle([cx + s // 2, cy + off - 3, cx + s // 2 + 16, cy + off + 3],
                fill=GREY)
# crashing chart
gx0, gy0 = bx + 200, by + 18
gx1, gy1 = bx + bw - 8, by + bh - 18
pts = [(gx0, gy0 + 8), (gx0 + 60, gy0 + 30), (gx0 + 120, gy0 + 22),
       (gx0 + 180, gy0 + 78), (gx0 + 232, gy0 + 118)]
d.line(pts, fill=RED, width=7, joint="curve")
d.polygon([(pts[-1][0] - 14, pts[-1][1] - 4), (pts[-1][0] + 16, pts[-1][1] + 2),
           (pts[-1][0] - 2, pts[-1][1] + 18)], fill=RED)
panel_text(x, y + 224, row1_w, "CHIP STOCKS CRASH",
           "Taiwan -7.2%  ·  Korea -5.4%  ·  Japan -3.3%",
           RED)

# ---------- row 2 ----------
y2 = TOP + ROW1_H + GAP

# panel 3: end violence against women (orange ribbon)
x = MX
card(x, y2, row2_w, ROW2_H, ORANGE)
bx, by, bw, bh = x + 24, y2 + 26, row2_w - 48, 178
# orange awareness ribbon
rx, ry = bx + bw // 2, by + 18
d.ellipse([rx - 52, ry, rx + 52, ry + 78], outline=ORANGE, width=16)
d.polygon([(rx - 34, ry + 58), (rx - 4, ry + 58), (rx - 34, ry + 132),
           (rx - 52, ry + 96)], fill=ORANGE)
d.polygon([(rx + 34, ry + 58), (rx + 4, ry + 58), (rx + 34, ry + 132),
           (rx + 52, ry + 96)], fill=ORANGE)
panel_text(x, y2 + 224, row2_w, "END VIOLENCE AGAINST WOMEN",
           "25 Nov: International Day to end violence against women",
           ORANGE, head_size=26, sub_size=19)

# panel 4: bitcoin below $60,000
x = MX + row2_w + GAP
card(x, y2, row2_w, ROW2_H, GOLD)
bx, by, bw, bh = x + 24, y2 + 26, row2_w - 48, 178
cx, cy, r = bx + bw // 2 - 52, by + bh // 2, 62
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD, outline=(190, 110, 0),
          width=4)
d.text((cx - 26, cy - 46), "B", font=font(FB, 88), fill=WHITE)
d.rectangle([cx - 26, cy - 58, cx - 20, cy + 58], fill=WHITE)
d.rectangle([cx + 20, cy - 58, cx + 26, cy + 58], fill=WHITE)
ax0, ay0 = cx + r + 26, by + 30
d.line([(ax0, ay0 + 10), (ax0 + 44, ay0 + 40), (ax0 + 88, ay0 + 96)],
       fill=RED, width=7)
d.polygon([(ax0 + 88 - 16, ay0 + 96 - 2), (ax0 + 88 + 12, ay0 + 96 + 4),
           (ax0 + 88 - 2, ay0 + 96 + 20)], fill=RED)
panel_text(x, y2 + 224, row2_w, "BITCOIN BELOW $60,000",
           "Crypto slide deepens as ETF outflows hit records",
           GOLD, head_size=26, sub_size=19)

# panel 5: inflation jumps
x = MX + 2 * (row2_w + GAP)
card(x, y2, row2_w, ROW2_H, TEAL)
bx, by, bw, bh = x + 24, y2 + 26, row2_w - 48, 178
bars = [38, 62, 88, 124]
bw2 = 44
for i, hgt in enumerate(bars):
    bx0 = bx + 18 + i * 64
    d.rectangle([bx0, by + bh - hgt, bx0 + bw2, by + bh], fill=TEAL)
d.line([(bx + 8, by + bh - 130), (bx + bw - 8, by + bh - 148)],
       fill=RED, width=5)
d.polygon([(bx + bw - 8, by + bh - 148), (bx + bw - 30, by + bh - 152),
           (bx + bw - 24, by + bh - 132)], fill=RED)
panel_text(x, y2 + 224, row2_w, "INFLATION JUMPS",
           "Australia CPI 4.9%  ·  Japan services prices +4.2%",
           TEAL, head_size=26, sub_size=19)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
