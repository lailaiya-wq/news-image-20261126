#!/usr/bin/env python3
"""Draw the news-image-20261126 front page (1024x1024 PNG).

Fresh artwork for Thursday 26 November 2026: 50 stories, every one first
reported that day (see ../news-list.md). Pure function of this file: no
network, no clock, no randomness. Run: python3 draw_news.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26                      # outer margin
CW = W - 2 * M              # content width = 972

PAPER = (247, 243, 234)
INK = (20, 18, 16)
RED = (179, 35, 27)
GREY = (110, 104, 92)
LIGHT = (216, 210, 194)
DARK = (28, 26, 24)
BLUE = (38, 84, 138)
TEAL = (18, 110, 104)
GREEN = (46, 120, 62)
BROWN = (146, 90, 40)
ORANGE = (198, 92, 26)
PURPLE = (110, 72, 150)

FDIR = "/usr/share/fonts/truetype/noto"
SERIF_BLACK = os.path.join(FDIR, "NotoSerif-Black.ttf")
SERIF_BLACK_IT = os.path.join(FDIR, "NotoSerif-BlackItalic.ttf")
SERIF_BOLD_IT = os.path.join(FDIR, "NotoSerif-BoldItalic.ttf")
SERIF_BOLD = os.path.join(FDIR, "NotoSerif-Bold.ttf")
SANS = os.path.join(FDIR, "NotoSans-Regular.ttf")
SANS_BOLD = os.path.join(FDIR, "NotoSans-Bold.ttf")
SANS_BLACK = os.path.join(FDIR, "NotoSans-Black.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, width, fill=INK, spacing=2, max_lines=None):
    lines = wrap(text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def fit_font(path, text, start, width):
    size = start
    while size > 8 and font(path, size).getlength(text) > width:
        size -= 1
    return font(path, size)


def hline(d, x, y, w, fill=INK, width=1):
    d.line([(x, y), (x + w, y)], fill=fill, width=width)


def badge(d, x, y, text, fill):
    f = font(SANS_BLACK, 8)
    tw = f.getlength(text) + 8
    d.rounded_rectangle([x, y, x + tw, y + 12], radius=2, fill=fill)
    d.text((x + 4, y + 1.5), text, font=f, fill=(255, 255, 255))
    return tw


# ---------------------------------------------------------------- art pieces
def art_city(d, x, y, w, h):
    """Beige apartment blocks, one dark smoke column (Gaza)."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 224, 200))
    d.rectangle([x + 4, y + h - 34, x + 30, y + h], fill=(196, 178, 140))
    d.rectangle([x + 34, y + h - 48, x + 62, y + h], fill=(178, 158, 118))
    d.rectangle([x + 66, y + h - 28, x + w - 4, y + h], fill=(206, 188, 152))
    for bx, by in [(9, h - 28), (18, h - 20), (40, h - 42), (50, h - 34),
                   (72, h - 22), (82, h - 14)]:
        d.rectangle([x + bx, y + by, x + bx + 5, y + by + 6], fill=(255, 214, 120))
    d.rectangle([x + w - 16, y + 2, x + w - 10, y + 18], fill=(70, 66, 60))
    d.ellipse([x + w - 22, y + 14, x + w - 4, y + 30], fill=(120, 116, 108))
    d.ellipse([x + w - 26, y + 24, x + w - 6, y + 42], fill=(150, 146, 138))


def art_storm(d, x, y, w, h):
    """Dark storm cloud, rain, lightning (Thanksgiving nor'easter)."""
    d.rectangle([x, y, x + w, y + h], fill=(44, 62, 84))
    d.ellipse([x + 8, y + 6, x + 46, y + 34], fill=(120, 132, 148))
    d.ellipse([x + 34, y + 2, x + 76, y + 32], fill=(140, 152, 168))
    d.ellipse([x + 62, y + 8, x + w - 8, y + 34], fill=(120, 132, 148))
    d.polygon([(x + 52, y + 30), (x + 44, y + 52), (x + 54, y + 52),
               (x + 46, y + h - 4), (x + 64, y + 46), (x + 54, y + 46),
               (x + 62, y + 30)], fill=(255, 214, 80))
    for rx in (12, 26, 78, 90):
        d.line([(x + rx, y + 44), (x + rx - 3, y + 56)], fill=(160, 190, 220), width=2)


def art_chart(d, x, y, w, h):
    """Rising bars with a red trend arrow (Asia stocks rebound)."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 226))
    bars = [(8, 30), (22, 24), (36, 34), (50, 18), (64, 12)]
    for i, (bx, bh) in enumerate(bars):
        col = GREEN if i >= 3 else (120, 140, 110)
        d.rectangle([x + bx, y + h - 8 - bh, x + bx + 11, y + h - 8], fill=col)
    d.line([(x + 6, y + h - 8), (x + w - 6, y + h - 8)], fill=INK, width=1)
    d.line([(x + 8, y + 26), (x + 30, y + 20), (x + 52, y + 12), (x + w - 10, y + 4)],
           fill=RED, width=3)
    d.polygon([(x + w - 14, y + 2), (x + w - 4, y + 2), (x + w - 8, y + 10)], fill=RED)


def art_shield(d, x, y, w, h):
    """Interceptor shield over a skyline (Riyadh missile defence)."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 40, 58))
    for i in range(5):
        d.rectangle([x + 6 + i * 18, y + h - 26 - (i % 2) * 8, x + 18 + i * 18,
                     y + h - 6], fill=(70, 96, 122))
    cx = x + w // 2
    d.polygon([(cx, y + h * 0.12), (cx + 22, y + h * 0.30),
               (cx + 16, y + h * 0.72), (cx, y + h * 0.95),
               (cx - 16, y + h * 0.72), (cx - 22, y + h * 0.30)],
              fill=(214, 178, 60))
    d.line([(cx - 10, y + h * 0.55), (cx + 10, y + h * 0.55)],
           fill=(24, 40, 58), width=3)
    d.ellipse([x + 10, y + 8, x + 16, y + 14], fill=(255, 120, 90))
    d.ellipse([x + w - 18, y + 12, x + w - 12, y + 18], fill=(255, 120, 90))


def art_plant(d, x, y, w, h):
    """Power plant with cooling towers and smoke (Nevinnomyssk)."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    d.polygon([(x + 10, y + h - 6), (x + 16, y + 14), (x + 30, y + 14),
               (x + 36, y + h - 6)], fill=(150, 146, 136))
    d.polygon([(x + 42, y + h - 6), (x + 48, y + 20), (x + 62, y + 20),
               (x + 68, y + h - 6)], fill=(130, 126, 116))
    d.rectangle([x + 74, y + 26, x + 80, y + h - 6], fill=(110, 106, 98))
    d.ellipse([x + 76, y + 8, x + 92, y + 22], fill=(120, 116, 108))
    d.ellipse([x + 70, y + 16, x + 88, y + 32], fill=(150, 146, 138))
    d.rectangle([x + 6, y + h - 14, x + w - 6, y + h - 6], fill=(90, 86, 78))


def art_drones(d, x, y, w, h):
    """Small drone silhouettes over rooftops (Russian barrage)."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 40))
    for dx, dy in [(14, 10), (48, 6), (78, 14)]:
        d.line([(x + dx - 7, y + dy - 4), (x + dx + 7, y + dy + 4)], fill=(220, 220, 220), width=2)
        d.line([(x + dx - 7, y + dy + 4), (x + dx + 7, y + dy - 4)], fill=(220, 220, 220), width=2)
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=RED)
    for i in range(4):
        d.line([(x + 8 + i * 4, y + h - 22), (x + 8 + i * 4, y + h - 22)],
               fill=(0, 0, 0), width=0)
    d.polygon([(x + 6, y + h - 6), (x + 6, y + h - 22), (x + 26, y + h - 22),
               (x + 30, y + h - 14), (x + 44, y + h - 14), (x + 48, y + h - 6)],
              fill=(90, 84, 76))
    d.polygon([(x + 56, y + h - 6), (x + 56, y + h - 18), (x + 76, y + h - 18),
               (x + 80, y + h - 10), (x + w - 6, y + h - 10), (x + w - 6, y + h - 6)],
              fill=(70, 64, 56))


def art_refinery(d, x, y, w, h):
    """Refinery towers with flames (Bangkok)."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 210))
    d.rectangle([x + 8, y + 26, x + 20, y + h - 6], fill=(120, 116, 108))
    d.rectangle([x + 26, y + 34, x + 40, y + h - 6], fill=(140, 136, 126))
    d.rectangle([x + 46, y + 18, x + 58, y + h - 6], fill=(110, 106, 98))
    d.ellipse([x + 64, y + 30, x + 88, y + h - 6], fill=(150, 146, 136))
    d.polygon([(x + 12, y + 26), (x + 18, y + 6), (x + 24, y + 26)], fill=(255, 140, 40))
    d.polygon([(x + 48, y + 18), (x + 54, y + 2), (x + 60, y + 18)], fill=(255, 90, 30))
    d.polygon([(x + 66, y + 34), (x + 72, y + 16), (x + 78, y + 34)], fill=(255, 160, 60))


def art_bank(d, x, y, w, h):
    """Bank columns with a rising red arrow (Korea rate hike)."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 234, 240))
    d.polygon([(x + 8, y + 10), (x + w // 2, y + 2), (x + w - 8, y + 10),
               (x + w - 8, y + 16), (x + 8, y + 16)], fill=(90, 100, 112))
    for cx in (14, 34, 54, 74):
        d.rectangle([x + cx, y + 20, x + cx + 8, y + h - 12], fill=(120, 130, 142))
    d.rectangle([x + 6, y + h - 12, x + w - 6, y + h - 6], fill=(90, 100, 112))
    d.line([(x + 10, y + h - 8), (x + 40, y + h - 18), (x + 62, y + h - 24),
            (x + w - 14, y + h - 32)], fill=RED, width=3)
    d.polygon([(x + w - 20, y + h - 36), (x + w - 10, y + h - 34),
               (x + w - 14, y + h - 24)], fill=RED)


def art_fire(d, x, y, w, h):
    """Bushfire: orange flames over green scrub (Flinders Island)."""
    d.rectangle([x, y, x + w, y + h], fill=(74, 94, 52))
    d.polygon([(x + 10, y + h - 6), (x + 14, y + h - 26), (x + 18, y + h - 6)],
              fill=(46, 66, 34))
    d.polygon([(x + 70, y + h - 6), (x + 74, y + h - 30), (x + 78, y + h - 6)],
              fill=(46, 66, 34))
    d.polygon([(x + 30, y + h - 6), (x + 38, y + h - 40), (x + 46, y + h - 6)],
              fill=(255, 140, 30))
    d.polygon([(x + 48, y + h - 6), (x + 56, y + h - 34), (x + 64, y + h - 6)],
              fill=(255, 90, 20))
    d.polygon([(x + 40, y + h - 6), (x + 46, y + h - 24), (x + 52, y + h - 6)],
              fill=(255, 200, 60))
    d.ellipse([x + 20, y + 4, x + 34, y + 14], fill=(200, 200, 190))
    d.ellipse([x + 60, y + 6, x + 78, y + 16], fill=(200, 200, 190))


def art_cross(d, x, y, w, h):
    """Medical cross and virus dots (DR Congo Ebola)."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 228))
    d.rectangle([x + w // 2 - 6, y + 8, x + w // 2 + 6, y + h - 8], fill=RED)
    d.rectangle([x + 10, y + h // 2 - 6, x + w - 10, y + h // 2 + 6], fill=RED)
    for cx, cy in [(14, 12), (w - 14, 12), (16, h - 12), (w - 16, h - 12)]:
        d.ellipse([x + cx - 3, y + cy - 3, x + cx + 3, y + cy + 3], fill=(60, 90, 70))


def art_mine(d, x, y, w, h):
    """Mine shaft cross-section with water line (West Java)."""
    d.rectangle([x, y, x + w, y + h], fill=(150, 118, 84))
    d.rectangle([x + 10, y + 6, x + w - 10, y + h - 6], fill=(110, 82, 56))
    d.rectangle([x + 16, y + 6, x + w - 16, y + h - 22], fill=(70, 52, 36))
    d.rectangle([x + 16, y + h - 22, x + w - 16, y + h - 6], fill=(52, 110, 150))
    d.line([(x + 16, y + h - 22), (x + w - 16, y + h - 22)], fill=(200, 230, 245), width=2)
    d.rectangle([x + w // 2 - 10, y + 10, x + w // 2 + 10, y + 26], fill=(200, 170, 110))
    d.line([(x + w // 2, y + 6), (x + w // 2, y + 10)], fill=(40, 30, 22), width=2)
    for rx, ry in [(22, 34), (w - 26, 40), (30, h - 30)]:
        d.polygon([(x + rx, y + ry), (x + rx + 6, y + ry - 5), (x + rx + 12, y + ry)],
                  fill=(90, 68, 46))


# ---------------------------------------------------------------- world map
# Coarse continent polygons in (lon, lat); drawn into a box with an
# equirectangular projection. Good enough for a small locator map.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 73), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 15), (-95, 18), (-105, 20), (-115, 28),
     (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    # Greenland
    [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-20, 70), (-25, 76),
     (-40, 80), (-55, 76), (-60, 70)],
    # South America
    [(-80, 10), (-75, 11), (-70, 12), (-60, 8), (-52, 5), (-50, 0),
     (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-60, -40),
     (-65, -45), (-70, -52), (-73, -50), (-73, -40), (-72, -30), (-70, -18),
     (-77, -12), (-80, -5), (-81, 0)],
    # Europe
    [(-10, 36), (-5, 36), (0, 38), (3, 42), (10, 44), (12, 45), (18, 40),
     (20, 40), (23, 36), (28, 36), (30, 40), (28, 45), (20, 45), (15, 50),
     (10, 55), (8, 57), (5, 58), (0, 55), (-5, 50), (-10, 48), (-10, 43),
     (-8, 38)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (38, 22), (43, 12), (48, 11), (51, 10), (48, 2), (42, -5),
     (40, -12), (35, -18), (32, -26), (28, -33), (20, -35), (16, -30),
     (13, -18), (12, -8), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 15),
     (-17, 20), (-15, 27), (-10, 31)],
    # Asia
    [(30, 36), (35, 36), (40, 38), (45, 40), (50, 42), (55, 45), (60, 48),
     (65, 50), (70, 55), (75, 60), (80, 65), (85, 70), (90, 72), (100, 75),
     (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 45),
     (142, 45), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 30), (115, 25), (110, 20), (108, 12), (105, 8), (100, 7),
     (98, 10), (95, 15), (92, 20), (88, 22), (85, 18), (80, 13), (77, 8),
     (75, 12), (72, 20), (68, 23), (65, 25), (60, 25), (57, 26), (55, 27),
     (52, 28), (50, 29), (48, 30), (45, 32), (42, 35), (38, 36), (35, 38)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -33), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -27),
     (146, -19), (142, -11), (137, -12), (132, -12), (126, -14), (122, -17),
     (118, -20)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44),
     (141, 45), (138, 40), (135, 35), (132, 33)],
    # New Zealand
    [(167, -45), (170, -42), (174, -38), (177, -38), (175, -41), (172, -43),
     (168, -46)],
]

# story number -> (lon, lat) for the 11 illustrated stories
PINS = {1: (34.5, 31.5), 2: (-74.0, 40.7), 3: (139.7, 35.7), 4: (46.7, 24.6),
        5: (41.9, 44.6), 6: (30.5, 50.4), 7: (100.5, 13.8), 8: (127.0, 37.5),
        9: (148.0, -40.0), 10: (30.0, 1.9), 11: (107.0, -6.9)}
PIN_PLACES = {1: "GAZA", 2: "NEW YORK", 3: "TOKYO", 4: "RIYADH",
              5: "NEVINNOMYSSK", 6: "KYIV", 7: "BANGKOK", 8: "SEOUL",
              9: "FLINDERS IS.", 10: "MONGWALU", 11: "WEST JAVA"}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 230, 220),
                outline=LIGHT, width=1)
    lon0, lon1, lat0, lat1 = -170.0, 190.0, 75.0, -55.0

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return px, py

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(203, 196, 178))
    nf = font(SANS_BLACK, 9)
    for num, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = nf.getlength(t)
        d.text((px - tw / 2, py - 6.5), t, font=nf, fill=(255, 255, 255))


# ---------------------------------------------------------------- content
LEADS = [
    dict(num=1, kick="GAZA · WAR", status=("REPORTED", GREY), art=art_city,
         head="Israeli strike kills 9 in Gaza, including Hamas deputy minister",
         deck="Strike on a Deir al-Balah flat kills Khaled Abu Nada, his wife "
              "and seven others; the third senior Hamas official killed this week.",
         why="WHY IT MATTERS: Israel keeps targeting Hamas officials as Gaza's toll climbs."),
    dict(num=2, kick="NEW YORK · WEATHER", status=("OFFICIAL", BLUE), art=art_storm,
         head="Thanksgiving nor'easter cancels 337 US flights",
         deck="Southwest cancels 125; New York and New Jersey declare emergencies "
              "as gusts reach 60 mph on the year's busiest travel day.",
         why="WHY IT MATTERS: The storm hits the holiday table, not just the airports."),
    dict(num=3, kick="TOKYO · MARKETS", status=("REPORTED", GREY), art=art_chart,
         head="Asia stocks rebound as US shuts for Thanksgiving",
         deck="Nikkei +0.9% to 57,499; Kospi +0.3%; Hang Seng +1.2%; Taiex +2.5% "
              "a day after the AI sell-off.",
         why="WHY IT MATTERS: Chip stocks lead the bounce while Wall Street is dark."),
]

MINIS = [
    dict(num=4, kick="RIYADH · WAR", status=("REPORTED", GREY), art=art_shield,
         head="Saudi defences down Houthi missiles aimed at Riyadh",
         deck="Two missiles downed; one hits Jizan port."),
    dict(num=5, kick="NEVINNOMYSSK · WAR", status=("REPORTED", GREY), art=art_plant,
         head="Ukrainian drones hit Russian power plant",
         deck="Nevinnomyssk plant ablaze; 343 drones downed."),
    dict(num=6, kick="KYIV · WAR", status=("REPORTED", GREY), art=art_drones,
         head="Russia's night barrage: missiles and 113 drones",
         deck="Iskander-M, Tsirkon missiles; 87 drones downed."),
    dict(num=7, kick="BANGKOK · DISASTER", status=("REPORTED", GREY), art=art_refinery,
         head="Blast and fire at Bangkok refinery injures 7",
         deck="All units halted; 120,000 b/d offline."),
    dict(num=8, kick="SEOUL · MARKETS", status=("OFFICIAL", BLUE), art=art_bank,
         head="Bank of Korea lifts rate to 3.25%",
         deck="Third hike since July, 5–2 vote; growth up to 4.1%."),
    dict(num=9, kick="FLINDERS ISLAND · DISASTER", status=("REPORTED", GREY), art=art_fire,
         head="Bushfire razes homes on Flinders Island",
         deck="6 homes lost; 14,000 ha burnt, a tenth of island."),
    dict(num=10, kick="DR CONGO · HEALTH", status=("OFFICIAL", BLUE), art=art_cross,
         head="Ebola cases pass 12,000 in DR Congo",
         deck="12,021 cases, 5,904 dead; 2nd-largest on record."),
    dict(num=11, kick="WEST JAVA · DISASTER", status=("CONFIRMED", GREEN), art=art_mine,
         head="13 dead in flooded Java gold mine",
         deck="13 more missing; rain flooded a 100m-deep pit."),
]

# remaining 39 stories, news-list order: (number, place, one-line text)
ALSO = [
    (2, "IRAN", "BBC hears desperate pleas from women on death row"),
    (4, "HORMUZ", "IRGC vows to choke strait to squeeze US economy"),
    (5, "ERBIL", "Kurds protest Baghdad taking oil and border posts"),
    (6, "ABU DHABI", "Menus must show calories from 1 June 2027"),
    (7, "JERUSALEM", "Eisenkot resumes coalition talks with left"),
    (8, "MOSCOW", "Kremlin accuses Kyiv of widening war to two seas"),
    (10, "KHARKIV", "Russian drone hits flat, 2 dead, 3 hurt"),
    (12, "LONDON", "UK and EU publish treaties with 10-year exit clause"),
    (13, "CHANNEL", "BBC: German dealer supplied smuggling gangs"),
    (14, "LONDON", "Tube strike halts lines in four-day week row"),
    (15, "BRUSSELS", "EU leaders weigh €45bn Ukraine loan"),
    (16, "KYIV", "UK funds 200MW wind farm in Ukraine"),
    (17, "KYIV", "North Korea 'pauses' military aid to Russia"),
    (18, "OSLO", "Norse Atlantic grounds all flights, near bankruptcy"),
    (19, "HONG KONG", "City marks a year since Tai Po fire killed 168"),
    (20, "DHAKA", "Garment minimum wage rises 36% after protests"),
    (22, "KATHMANDU", "Nepal declares 5,000 missing in floods dead"),
    (25, "SINGAPORE", "Nvidia halts server shipments to four nations"),
    (26, "SEOUL", "Kim Do-yeong, 23, youngest two-time KBO MVP"),
    (27, "KINSHASA", "DR Congo summons Uganda envoy over rebel post"),
    (28, "MONGWALU", "MSF hands Ebola centre to health ministry"),
    (29, "LUSAKA", "Zambia bans rally against term-limit repeal"),
    (31, "SOMALIA", "BBC: as foreign troops leave, will al-Shabaab rule?"),
    (32, "MAIDUGURI", "Borno school enrolment hits 1.8 million"),
    (33, "SUDAN", "War and drought threaten harvests"),
    (34, "NAIROBI", "Court: US-backed Ebola unit unconstitutional"),
    (35, "JOHANNESBURG", "Kieswetter: crime outruns the state"),
    (36, "OTTAWA", "Student caps test Carney's talent drive"),
    (37, "IOWA", "Army safely detonates 5 tonnes of explosives"),
    (38, "LOS ANGELES", "Lakers avenge loss to Jazz"),
    (40, "WASHINGTON", "Kushner: Putin 'uninterested' in ceasefire"),
    (41, "LIMA", "Peru central bank chief sees ratings upgrade"),
    (42, "BUENOS AIRES", "Senate debates suspending primary elections"),
    (43, "USA", "NFL: Bears-Lions, Eagles-Cowboys, Chiefs-Bills"),
    (44, "WASHINGTON", "Trump's 00:47 post attacks NYT reporter"),
    (45, "CANBERRA", "Senator Blyth defects to One Nation"),
    (47, "SYDNEY", "Beale returns to Wallabies after five years"),
    (49, "TURIN", "Sinner to miss Australian Open after knee surgery"),
    (50, "GLOBAL", "Bitcoin climbs back above $60,000"),
]

BIG_NUMBERS = [
    ("337", "US FLIGHTS CANCELLED IN STORM"),
    ("12,021", "EBOLA CASES IN DR CONGO"),
    ("3.25%", "BANK OF KOREA RATE AFTER HIKE"),
    ("$60,850", "BITCOIN BACK ABOVE $60,000"),
    ("13", "DEAD IN JAVA GOLD MINE"),
    ("€45BN", "UKRAINE LOAN ON EU TABLE"),
]

REGIONS = [("EUROPE", 11, BLUE), ("AMERICAS", 9, TEAL), ("AFRICA", 9, GREEN),
           ("ASIA", 8, ORANGE), ("MIDDLE EAST", 7, BROWN), ("OCEANIA", 3, PURPLE),
           ("GLOBAL", 3, GREY)]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = M

    # 1. top bar
    f_top = font(SANS_BOLD, 12)
    top = ("THE WORLD IN ONE DAY  ·  50 STORIES  ·  7 REGIONS  ·  19 FIELDS  ·  "
           "ALL FIRST REPORTED ON THURSDAY 26 NOVEMBER 2026")
    d.text(((W - f_top.getlength(top)) / 2, y), top, font=f_top, fill=INK)
    y += 18

    # 2. masthead + kicker + double rule
    f_mast = fit_font(SERIF_BLACK, "Thursday 26 November 2026", 58, CW)
    d.text(((W - f_mast.getlength("Thursday 26 November 2026")) / 2, y),
           "Thursday 26 November 2026", font=f_mast, fill=INK)
    y += f_mast.size + 6
    f_kick = font(SERIF_BOLD_IT, 15)
    kick = ("Gaza strike kills Hamas official  ·  Thanksgiving storm grounds "
            "337 flights  ·  Asia stocks rebound as US markets shut")
    d.text(((W - f_kick.getlength(kick)) / 2, y), kick, font=f_kick, fill=RED)
    y += 22
    hline(d, M, y, CW, width=2)
    y += 3
    hline(d, M, y, CW, width=1)
    y += 8

    # 3. region bar
    total = sum(c for _, c, _ in REGIONS)
    x = M
    f_reg = font(SANS_BLACK, 10)
    bar_h = 18
    for name, count, col in REGIONS:
        seg_w = int(CW * count / total)
        d.rectangle([x, y, x + seg_w - 1, y + bar_h], fill=col)
        label = f"{name} {count}"
        tw = f_reg.getlength(label)
        if tw < seg_w - 6:
            d.text((x + (seg_w - tw) / 2, y + 4), label, font=f_reg,
                   fill=(255, 255, 255))
        x += seg_w
    y += bar_h + 5
    f_field = font(SANS_BOLD, 10)
    fields = ("19 FIELDS — WAR 9 · POLITICS 6 · SPORT 5 · DIPLOMACY 4 · "
              "DISASTER 4 · MARKETS 4 · HEALTH 3 · JUSTICE 2 · LABOUR 2 · "
              "MIGRATION 2 · + 9 MORE")
    d.text((M, y), fields, font=f_field, fill=GREY)
    y += 16

    # 4. big-number strip
    box_w = CW // 6
    f_num = font(SANS_BLACK, 26)
    f_lab = font(SANS_BOLD, 8)
    strip_h = 50
    for i, (num, lab) in enumerate(BIG_NUMBERS):
        bx = M + i * box_w
        d.rectangle([bx + 2, y, bx + box_w - 2, y + strip_h],
                    outline=LIGHT, width=1)
        d.text((bx + box_w / 2 - f_num.getlength(num) / 2, y + 4), num,
               font=f_num, fill=RED)
        for j, ln in enumerate(wrap(lab, f_lab, box_w - 12)):
            d.text((bx + box_w / 2 - f_lab.getlength(ln) / 2, y + 34 + j * 10),
                   ln, font=f_lab, fill=INK)
    y += strip_h + 8

    # 5. UTC strip
    f_utc = font(SANS_BOLD, 10)
    utc = ("THE DAY IN UTC    05:47  Trump posts at 00:47 ET   ·   07:45  "
           "Bangkok refinery blast   ·   12:00  London Tube strike begins   ·   "
           "US MARKETS CLOSED FOR THANKSGIVING")
    d.rectangle([M, y, M + CW, y + 20], fill=DARK)
    d.text((M + 8, y + 4), utc, font=f_utc, fill=(255, 255, 255))
    y += 24

    # 6. three leads
    col_w = CW // 3
    f_k = font(SANS_BLACK, 9)
    f_h = font(SERIF_BOLD, 16)
    f_deck = font(SANS, 10)
    f_why = font(SANS_BOLD, 9)
    lead_top = y
    for i, lead in enumerate(LEADS):
        cx = M + i * col_w
        cw = col_w - 14
        lead["art"](d, cx, y, cw, 66)
        yy = y + 72
        numf = font(SANS_BLACK, 11)
        d.text((cx, yy), f"{lead['num']}.", font=numf, fill=RED)
        d.text((cx + 16, yy), lead["kick"], font=f_k, fill=INK)
        bw = badge(d, cx + 16 + f_k.getlength(lead["kick"]) + 6, yy + 1,
                   lead["status"][0], lead["status"][1])
        yy += 16
        yy = draw_wrapped(d, cx, yy, lead["head"], f_h, cw, spacing=0,
                          max_lines=2)
        yy += 2
        yy = draw_wrapped(d, cx, yy, lead["deck"], f_deck, cw, spacing=1,
                          max_lines=2)
        yy += 3
        yy = draw_wrapped(d, cx, yy, lead["why"], f_why, cw, fill=RED,
                          spacing=1, max_lines=2)
        lead_top = max(lead_top, yy)
    y = lead_top + 6
    hline(d, M, y, CW, fill=LIGHT, width=1)
    y += 6

    # 7. eight minis, 2 rows x 4
    mcol = CW // 4
    f_mh = font(SERIF_BOLD, 12)
    f_md = font(SANS, 9)
    mini_top = y
    for row in range(2):
        for col in range(4):
            mini = MINIS[row * 4 + col]
            cx = M + col * mcol
            cw = mcol - 12
            yy = y + row * 102
            mini["art"](d, cx, yy, cw, 42)
            yy += 46
            d.text((cx, yy), f"{mini['num']}.", font=numf, fill=RED)
            d.text((cx + 14, yy), mini["kick"], font=f_k, fill=INK)
            badge(d, cx + 14 + f_k.getlength(mini["kick"]) + 5, yy + 1,
                  mini["status"][0], mini["status"][1])
            yy += 15
            yy = draw_wrapped(d, cx, yy, mini["head"], f_mh, cw, spacing=0,
                              max_lines=2)
            deck = mini["deck"]
            while deck and f_md.getlength(deck) > cw:
                deck = deck[:-1]
            if deck != mini["deck"]:
                deck = deck[:-1].rstrip() + "…"
            d.text((cx, yy), deck, font=f_md, fill=INK)
            yy += f_md.size + 2
            mini_top = max(mini_top, yy)
    y = y + 2 * 102 + 4
    hline(d, M, y, CW, fill=LIGHT, width=1)
    y += 6

    # 8. map row: map left, pin key right
    f_sec = font(SANS_BLACK, 11)
    d.text((M, y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((M + 470, y), "PINS = STORY NUMBERS", font=f_sec, fill=INK)
    y += 16
    map_w, map_h = 440, 116
    draw_map(d, M, y, map_w, map_h)
    f_key = font(SANS_BOLD, 10)
    kx, ky = M + 470, y
    for i in range(1, 12):
        col = 0 if i <= 6 else 1
        row = (i - 1) % 6
        tx = kx + col * 250
        ty = ky + row * 21
        d.text((tx, ty), f"{i}. {PIN_PLACES[i]}", font=f_key, fill=INK)
    y += map_h + 8

    # 9. ALSO list
    d.text((M, y), "ALSO ON THURSDAY 26 NOVEMBER", font=f_sec, fill=INK)
    y += 16
    f_also = font(SANS, 10)
    f_also_b = font(SANS_BOLD, 10)
    acol = CW // 3
    for idx, (num, place, text) in enumerate(ALSO):
        col = idx // 13
        row = idx % 13
        ax = M + col * acol
        ay = y + row * 13
        head = f"{num}. {place} — "
        hw = f_also_b.getlength(head)
        d.text((ax, ay), head, font=f_also_b, fill=INK)
        # fit the rest on one line, truncate with ellipsis if needed
        rest = text
        while rest and f_also.getlength(rest) > acol - hw - 8:
            rest = rest[:-1]
        if rest != text:
            rest = rest[:-1].rstrip() + "…"
        d.text((ax + hw, ay), rest, font=f_also, fill=INK)
    y += 13 * 13 + 4

    # 10. DATE CHECK + sources
    f_dc = font(SANS_BLACK, 10)
    dc = ("DATE CHECK — Every story above was first reported on Thursday "
          "26 November 2026. Events from 25 November or earlier were excluded.")
    d.rectangle([M, y, M + CW, y + 20], fill=RED)
    d.text((M + 8, y + 4), dc, font=f_dc, fill=(255, 255, 255))
    y += 24
    f_src = font(SANS, 8)
    src = ("Sources: Reuters · BBC · AP · AFP · The Hindu · SCMP · AAP · ABC · "
           "Korea JoongAng Daily · Business Day · Andina · rugby.com.au · and others. "
           "Compiled 26 November 2026.")
    d.text((M, y), src, font=f_src, fill=GREY)
    y += 12

    assert y <= H - 4, f"layout overflow: y={y}"
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {img.size} PNG {size} bytes")
    assert size <= 1048576, "entry.png over 1 MiB"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
