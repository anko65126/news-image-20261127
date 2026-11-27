"""Compose the 27 November 2026 front page and store it as entry.png.

One page that carries the whole day: a Thanksgiving storm on the U.S.
East Coast as the lead, then Trump pressing Putin over Ukraine, Kim
Jong Un's nuclear vow, Musk's SpaceX-share pledge, and the end of the
Colombia supermarket siege, with a strip of shorter items along the
foot. Drawn entirely with PIL, so the bytes never change between runs.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
PAPER = (247, 242, 231)
INK = (26, 24, 20)
GREY = (92, 86, 74)
RED = (146, 32, 24)
NAVY = (24, 30, 44)
SKY = (203, 213, 224)
CLOUD = (74, 84, 98)
BOLT = (240, 192, 64)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS_R = "DejaVuSans.ttf"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def fit(d, text, fnt, width):
    """Greedy word wrap: the lines of text that fit inside width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        elif cur:
            lines.append(cur)
            cur = word
        else:
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, width, kicker, headline, body, hsize):
    """Render one story and return the y just below its last line."""
    d.text((x, y), kicker, font=font(SANS_B, 19), fill=RED)
    y += 29
    hf = font(SERIF_B, hsize)
    for ln in fit(d, headline, hf, width):
        d.text((x, y), ln, font=hf, fill=INK)
        y += hsize + 6
    y += 3
    bf = font(SERIF_R, 20)
    for ln in fit(d, body, bf, width):
        d.text((x, y), ln, font=bf, fill=INK)
        y += 27
    return y


def storm_panel(d, x, y, size):
    """A storm cloud with a lightning bolt, boxed beside the lead story."""
    d.rounded_rectangle([x, y, x + size, y + size], radius=14,
                        fill=SKY, outline=INK, width=3)
    # Cloud: three humps on a flat base, sitting in the upper half,
    # with an ink arc over the top so the shape reads at a glance.
    cx, cy = x + size // 2, y + 52
    for dx, dy, r in ((-30, 6, 20), (0, -8, 27), (30, 6, 20)):
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=CLOUD)
    d.rectangle([cx - 50, cy, cx + 50, cy + 16], fill=CLOUD)
    d.arc([cx - 50, cy - 34, cx + 50, cy + 18], start=180, end=360,
          fill=INK, width=3)
    d.line([cx - 50, cy + 16, cx + 50, cy + 16], fill=INK, width=3)
    # Lightning bolt dropping from the cloud base.
    bolt = [(cx + 4, cy + 16), (cx - 12, cy + 44), (cx + 2, cy + 44),
            (cx - 6, cy + 68), (cx + 20, cy + 38), (cx + 6, cy + 38),
            (cx + 16, cy + 16)]
    d.polygon(bolt, fill=BOLT, outline=INK)
    # Rain slanting in from the left under the cloud.
    for i in range(3):
        rx = x + 18 + i * 16
        d.line([rx, cy + 34, rx - 7, cy + 56], fill=(110, 128, 148),
               width=3)
        rx = x + size - 34 + i * 16
        d.line([rx, cy + 34, rx - 7, cy + 56], fill=(110, 128, 148),
               width=3)


LEAD = (
    "WEATHER",
    "STORM CRASHES THANKSGIVING",
    "A powerful storm battered the U.S. East Coast on Thanksgiving "
    "Day, cutting power to hundreds of thousands as gusts of 70 mph "
    "brought down trees and lines. New York's Thanksgiving parade "
    "was postponed by weather for the first time in a hundred years.",
    44,
)

ROWS = [
    [
        ("UKRAINE",
         "TRUMP URGES PUTIN TO PULL BACK",
         "President Trump said he had asked Vladimir Putin to pull "
         "back Russia's aggression in Europe in hopes of a quick "
         "settlement. President Zelensky warned Russia is preparing "
         "a new mass strike within days.",
         34),
        ("NORTH KOREA",
         "KIM VOWS BIGGER NUCLEAR ARSENAL",
         "Kim Jong Un called for an expansion of North Korea's "
         "nuclear programme despite Washington's overtures, as "
         "Ukraine said Pyongyang has halted missile shipments to "
         "ally Russia.",
         34),
    ],
    [
        ("SPACE",
         "SPACEX SHARES FOR EVERY U.S. CHILD",
         "Elon Musk said every child in the United States will "
         "receive two SpaceX shares, a pledge estimated at about "
         "$18 billion.",
         31),
        ("COLOMBIA",
         "HOSTAGES FREED AFTER SIEGE",
         "All hostages were freed after a 16-hour siege at a "
         "Colombian supermarket, ending an overnight standoff.",
         31),
    ],
]

BAND_TOP = ("ALSO TODAY  Explosions hit three tankers in Hormuz · "
            "Ebola cases in DR Congo top 12,000")
BAND_BOTTOM = ("Diesel tanker capsizes off Ibiza · Ukraine, Russia "
               "swap soldiers' remains · SpaceX satellite clearance")


def centred(d, y, text, fnt, fill):
    d.text(((SIDE - d.textlength(text, font=fnt)) / 2, y), text,
           font=fnt, fill=fill)


def build_page():
    page = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(page)
    margin = 46
    right = SIDE - margin

    centred(d, 30, "THE WORLD IN ONE PAGE", font(SERIF_B, 64), INK)
    d.line([margin, 118, right, 118], fill=INK, width=4)
    d.line([margin, 126, right, 126], fill=INK, width=1)
    centred(d, 136, "Friday, 27 November 2026  ·  One image, the "
            "whole day", font(SANS_R, 19), GREY)

    storm_panel(d, right - 168, 184, 150)
    y = block(d, margin, 178, 730, *LEAD)

    col_w = 448
    for row in ROWS:
        rule_y = y + 12
        d.line([margin, rule_y, right, rule_y], fill=INK, width=2)
        row_y = rule_y + 18
        ends = [block(d, margin, row_y, col_w, *row[0]),
                block(d, right - col_w, row_y, col_w, *row[1])]
        y = max(ends)
    assert y <= 946, "stories overflow the page"

    d.rectangle([0, 958, SIDE, SIDE], fill=NAVY)
    centred(d, 968, BAND_TOP, font(SANS_B, 18), (240, 236, 224))
    centred(d, 998, BAND_BOTTOM, font(SANS_R, 16), (196, 200, 210))

    out = Path(__file__).with_name("entry.png")
    page.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    print(build_page())
