"""Draw the front page for Friday 27 November 2026 and save it as entry.png.

The page is a broadsheet front page built only from the day's reporting:
the Thanksgiving storm that battered the U.S. East Coast and postponed
New York's parade, Trump urging Putin to pull back in Europe, Kim Jong Un
vowing a bigger nuclear arsenal, Elon Musk's SpaceX shares pledge for
every American child, and the hostages freed after a 16-hour siege in
Colombia. Everything is drawn with PIL, so the page is deterministic.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
PAPER = (247, 242, 231)
INK = (26, 24, 20)
FADED = (92, 86, 74)
ACCENT = (146, 32, 24)
BAND = (24, 30, 44)
SKY = (203, 213, 224)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SERIF = str(FONT_DIR / "DejaVuSerif.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Split text into lines that fit width, word by word."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def story(draw, x, y, width, kicker, headline, body, head_size=37):
    """One news block: red kicker, serif headline, then body text."""
    draw.text((x, y), kicker, font=load(SANS_BOLD, 19), fill=ACCENT)
    y += 29
    head_font = load(SERIF_BOLD, head_size)
    for line in wrap(draw, headline, head_font, width):
        draw.text((x, y), line, font=head_font, fill=INK)
        y += head_size + 6
    y += 3
    body_font = load(SERIF, 20)
    for line in wrap(draw, body, body_font, width):
        draw.text((x, y), line, font=body_font, fill=INK)
        y += 27
    return y


def balloon_graphic(draw, x, y, size):
    """A parade balloon leaning into wind and rain, beside the lead story."""
    draw.rounded_rectangle([x, y, x + size, y + size], radius=14,
                           fill=SKY, outline=INK, width=3)
    # Rain streaks across the little sky.
    for i in range(5):
        rx = x + 14 + i * 30
        draw.line([rx, y + 10, rx - 8, y + 34], fill=(110, 128, 148),
                  width=3)
        draw.line([rx + 12, y + 96, rx + 4, y + 120], fill=(110, 128, 148),
                  width=3)
    # The balloon itself: a big round body leaning right, with stripes.
    cx, cy, r = x + size // 2 + 8, y + 58, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 176, 92),
                 outline=INK, width=4)
    for off in (-18, 0, 18):
        draw.arc([cx - r + 6 + off // 3, cy - r, cx + r - 6 + off // 3,
                  cy + r], start=270, end=90, fill=INK, width=2)
    # Tethers converging to a handler point below, blown sideways.
    hx, hy = cx - 16, y + size - 12
    draw.line([cx - 14, cy + r - 4, hx, hy], fill=INK, width=3)
    draw.line([cx + 16, cy + r - 6, hx, hy], fill=INK, width=3)
    draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=ACCENT)
    # Wind gusts pushing from the left.
    for gy in (y + 44, y + 66, y + 88):
        draw.line([x + 8, gy, x + 34, gy], fill=INK, width=3)


def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)
    margin = 46
    right = PAGE_W - margin

    # Masthead
    name_font = load(SERIF_BOLD, 64)
    name = "THE WORLD IN ONE PAGE"
    w = draw.textlength(name, font=name_font)
    draw.text(((PAGE_W - w) / 2, 30), name, font=name_font, fill=INK)
    draw.line([margin, 118, right, 118], fill=INK, width=4)
    draw.line([margin, 126, right, 126], fill=INK, width=1)
    date_font = load(SANS, 19)
    date_line = "Friday, 27 November 2026  ·  One image, the whole day"
    w = draw.textlength(date_line, font=date_font)
    draw.text(((PAGE_W - w) / 2, 136), date_line, font=date_font, fill=FADED)

    # Lead story, with the storm balloon glyph on its right
    lead_y = 178
    balloon_graphic(draw, right - 168, lead_y + 6, 150)
    lead_end = story(
        draw, margin, lead_y, 730,
        "WEATHER",
        "STORM CRASHES THANKSGIVING",
        "A powerful storm battered the U.S. East Coast on Thanksgiving "
        "Day, cutting power to hundreds of thousands as gusts of 70 mph "
        "brought down trees and lines. New York's Thanksgiving parade "
        "was postponed by weather for the first time in a hundred years.",
        head_size=44,
    )

    # Two-column rows; each divider sits below the taller column.
    col_w = 448
    col_r = right - col_w
    rule_y = lead_end + 12
    draw.line([margin, rule_y, right, rule_y], fill=INK, width=2)
    mid_y = rule_y + 18
    mid_left = story(
        draw, margin, mid_y, col_w,
        "UKRAINE",
        "TRUMP URGES PUTIN TO PULL BACK",
        "President Trump said he had asked Vladimir Putin to pull back "
        "Russia's aggression in Europe in hopes of a quick settlement. "
        "President Zelensky warned Russia is preparing a new mass "
        "strike within days.",
        head_size=34,
    )
    mid_right = story(
        draw, col_r, mid_y, col_w,
        "NORTH KOREA",
        "KIM VOWS BIGGER NUCLEAR ARSENAL",
        "Kim Jong Un called for an expansion of North Korea's nuclear "
        "programme despite Washington's overtures, as Ukraine said "
        "Pyongyang has halted missile shipments to ally Russia.",
        head_size=34,
    )

    rule_y = max(mid_left, mid_right) + 12
    draw.line([margin, rule_y, right, rule_y], fill=INK, width=2)
    low_y = rule_y + 18
    low_left = story(
        draw, margin, low_y, col_w,
        "SPACE",
        "SPACEX SHARES FOR EVERY U.S. CHILD",
        "Elon Musk said every child in the United States will receive "
        "two SpaceX shares, a pledge estimated at about $18 billion.",
        head_size=31,
    )
    low_right = story(
        draw, col_r, low_y, col_w,
        "COLOMBIA",
        "HOSTAGES FREED AFTER SIEGE",
        "All hostages were freed after a 16-hour siege at a Colombian "
        "supermarket, ending an overnight standoff.",
        head_size=31,
    )
    assert max(low_left, low_right) <= 946, "stories overflow the page"

    # News band along the foot of the page
    band_y = 958
    draw.rectangle([0, band_y, PAGE_W, PAGE_H], fill=BAND)
    band_font = load(SANS_BOLD, 18)
    band_text = ("ALSO TODAY  Explosions hit three tankers in Hormuz · "
                 "Ebola cases in DR Congo top 12,000")
    w = draw.textlength(band_text, font=band_font)
    draw.text(((PAGE_W - w) / 2, band_y + 10), band_text,
              font=band_font, fill=(240, 236, 224))
    small_font = load(SANS, 16)
    small = ("Diesel tanker capsizes off Ibiza · Ukraine, Russia swap "
             "soldiers' remains · SpaceX satellite clearance")
    w = draw.textlength(small, font=small_font)
    draw.text(((PAGE_W - w) / 2, band_y + 40), small,
              font=small_font, fill=(196, 200, 210))

    out = Path(__file__).with_name("entry.png")
    page.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    print(build_page())
