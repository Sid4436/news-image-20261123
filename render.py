#!/usr/bin/env python3
"""Render entry.png: world news of Monday 23 November 2026 in one image."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu/"
BOLD = FD + "DejaVuSans-Bold.ttf"
REG = FD + "DejaVuSans.ttf"

BG = (245, 242, 235)
INK = (20, 20, 24)
MUTED = (80, 80, 88)
HEAD_BG = (18, 28, 48)
SUBINK = (45, 45, 52)
SOURCES = ["Korea JoongAng Daily, Al Jazeera",
           "Al Jazeera, Airways Magazine",
           "Reuters, Al Jazeera",
           "BBC, UK press",
           "USGS via Xinhua, Australian BoM",
           "IANS, Dainik Jagran"]
WHITE = (255, 255, 255)

STORIES = [
    ("ASIA · MARKETS", (200, 40, 40), "Seoul stocks plunge over 5%",
     ["KOSPI fell more than 5% amid AI-bubble fears;",
      "trading curb hit for a 2nd session. Samsung,", "SK Hynix down."]),
    ("EUROPE · LABOUR", (30, 90, 170), "Belgium strike shuts all airports",
     ["National strike against austerity: air traffic",
      "control halted 07:00–21:00; Brussels and",
      "Charleroi flights cancelled."]),
    ("ASIA · DISASTER", (200, 40, 40), "Indonesia factory fire: 24 dead",
     ["Toll confirmed Monday for fire (began Sat.) at",
      "a confectionery factory in Cikande, Banten;",
      "about 30 still missing."]),
    ("EUROPE · HEALTH / TECH", (30, 90, 170), "UK launches huge AI breast-screening trial",
     ["NHS EDITH trial: nearly 700,000 women at 30",
      "sites, described as the world's largest."]),
    ("PACIFIC · SCIENCE", (20, 130, 110), "M6.5 deep quake near Vanuatu",
     ["02:40 UTC, about 600 km deep. No tsunami",
      "threat to Australia; no damage reported."]),
    ("SOUTH ASIA · DIPLOMACY", (190, 110, 20), "Modi hosts Nepal PM Balen Shah",
     ["New Delhi talks on Shah's first state visit;",
      "energy, rail and trade on the agenda."]),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # header
    d.rectangle([0, 0, W, 120], fill=HEAD_BG)
    d.text((W // 2, 44), "WORLD NEWS", font=font(BOLD, 44), fill=WHITE, anchor="mm")
    d.text((W // 2, 92), "MONDAY 23 NOVEMBER 2026", font=font(BOLD, 34), fill=(255, 210, 90), anchor="mm")

    cols, rows = 2, 3
    mx, top, gap = 16, 136, 14
    tw = (W - 2 * mx - gap) // cols
    th = (H - top - 60 - 2 * gap) // rows
    ftag = font(BOLD, 19)
    fhead = font(BOLD, 37)
    fsub = font(REG, 21)
    fsrc = font(REG, 15)
    for i, (tag, col, head, sub) in enumerate(STORIES):
        cx = mx + (i % cols) * (tw + gap)
        cy = top + (i // cols) * (th + gap)
        d.rectangle([cx, cy, cx + tw, cy + th], fill=WHITE, outline=(200, 200, 200))
        d.rectangle([cx, cy, cx + tw, cy + 30], fill=col)
        d.text((cx + 12, cy + 15), tag, font=ftag, fill=WHITE, anchor="lm")
        y = cy + 40
        for line in wrap(d, head, fhead, tw - 24):
            d.text((cx + 12, y), line, font=fhead, fill=INK)
            y += 43
        y += 6
        for line in wrap(d, " ".join(sub), fsub, tw - 24):
            d.text((cx + 12, y), line, font=fsub, fill=SUBINK)
            y += 27
        d.text((cx + 12, cy + th - 10), "Sources: " + SOURCES[i], font=fsrc,
               fill=MUTED, anchor="ls")

    d.text((W // 2, H - 40),
           "All six items are events of, or first confirmed on, Monday 23 November 2026.",
           font=font(REG, 16), fill=MUTED, anchor="mm")
    d.text((W // 2, H - 18),
           "Indonesia fire began Sat 21 Nov; the toll was confirmed Mon 23 Nov. No outcomes beyond those reported.",
           font=font(REG, 14), fill=MUTED, anchor="mm")
    q = im.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
