#!/usr/bin/env python3
"""Generate individual label PNGs sized for Brother P-Touch tape.
Wire labels: 12mm (1/2") tape — 64px high at 180 DPI
Board labels: 18mm (3/4") tape — 96px high
Power/orient/brand: 24mm (1") tape — 128px high

Each label is a separate PNG in labels_ptouch/ folder.
Run with --print to open P-Touch Editor with each label sequentially.
"""

import os
import subprocess
import sys
import time
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "labels_ptouch")
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 180

# Tape height in pixels at 180 DPI
TAPE_12MM = 64   # 1/2" tape
TAPE_18MM = 96   # 3/4" tape
TAPE_24MM = 128  # 1" tape

# Label width — Brother tapes are continuous, so width is flexible
# Typical label length: 1.5" to 3" depending on content
WIDTH_SHORT = int(1.5 * DPI)   # 270px
WIDTH_MED = int(2.0 * DPI)     # 360px
WIDTH_LONG = int(3.0 * DPI)    # 540px

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

def get_font(size, bold=False):
    """Get a monospace font, falling back gracefully."""
    names = [
        "/System/Library/Fonts/SFMono-Bold.otf" if bold else "/System/Library/Fonts/SFMono-Regular.otf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Courier.dfont",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def make_wire_label(filename, fn_text, gpio_text):
    """Wire label — single line, fits 12mm tape."""
    h = TAPE_12MM
    w = WIDTH_SHORT
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    font_fn = get_font(18, bold=True)
    font_gpio = get_font(10)

    # Function name centered
    bbox = draw.textbbox((0, 0), fn_text, font=font_fn)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 8), fn_text, fill=BLACK, font=font_fn)

    # GPIO detail centered below
    bbox2 = draw.textbbox((0, 0), gpio_text, font=font_gpio)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((w - tw2) // 2, 36), gpio_text, fill=GRAY, font=font_gpio)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_board_label(filename, name_text, detail_text):
    """Board label — fits 18mm tape."""
    h = TAPE_18MM
    w = WIDTH_MED
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    font_name = get_font(16, bold=True)
    font_detail = get_font(9)

    # Name top-left aligned
    draw.text((10, 12), name_text, fill=BLACK, font=font_name)

    # Detail below
    draw.text((10, 42), detail_text, fill=GRAY, font=font_detail)

    # Bottom border accent
    draw.line([(10, h - 8), (w - 10, h - 8)], fill=BLACK, width=2)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_power_label(filename, icon, name_text, warning_text):
    """Power label — fits 24mm tape, bold with warning."""
    h = TAPE_24MM
    w = WIDTH_LONG
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    font_icon = get_font(24, bold=True)
    font_name = get_font(18, bold=True)
    font_warn = get_font(9, bold=True)

    # Border
    draw.rectangle([(2, 2), (w - 3, h - 3)], outline=BLACK, width=3)

    # Icon + Name
    draw.text((12, 10), icon, fill=BLACK, font=font_icon)
    draw.text((42, 14), name_text, fill=BLACK, font=font_name)

    # Warning text
    draw.text((12, 50), warning_text, fill=BLACK, font=font_warn)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_orient_label(filename, direction, arrow):
    """Orientation label — fits 24mm tape."""
    h = TAPE_24MM
    w = WIDTH_SHORT
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    font_dir = get_font(22, bold=True)
    font_arrow = get_font(36, bold=True)

    # Direction
    bbox = draw.textbbox((0, 0), direction, font=font_dir)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 8), direction, fill=BLACK, font=font_dir)

    # Arrow
    bbox2 = draw.textbbox((0, 0), arrow, font=font_arrow)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((w - tw2) // 2, 55), arrow, fill=BLACK, font=font_arrow)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_brand_label(filename):
    """Branding label — white on black, 24mm tape."""
    h = TAPE_24MM
    w = WIDTH_LONG
    img = Image.new("RGB", (w, h), BLACK)
    draw = ImageDraw.Draw(img)

    font_team = get_font(28, bold=True)
    font_role = get_font(10)

    # ELKTRON centered
    text = "ELKTRON"
    bbox = draw.textbbox((0, 0), text, font=font_team)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 15), text, fill=WHITE, font=font_team)

    # Subtitle
    sub = "Escort Bot - CoreWeave Hackathon 2026"
    bbox2 = draw.textbbox((0, 0), sub, font=font_role)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((w - tw2) // 2, 65), sub, fill=(170, 170, 170), font=font_role)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def generate_all():
    labels = []

    # ── WIRE LABELS (12mm tape) ──
    wire_labels = [
        ("01_wire_left_fwd.png", "LEFT FWD", "GPIO 17 > L298N IN1"),
        ("02_wire_left_bwd.png", "LEFT BWD", "GPIO 24 > L298N IN2"),
        ("03_wire_right_fwd.png", "RIGHT FWD", "GPIO 22 > L298N IN3"),
        ("04_wire_right_bwd.png", "RIGHT BWD", "GPIO 23 > L298N IN4"),
        ("05_wire_l298n_left.png", "L298N > LEFT", "Motor A Terminal"),
        ("06_wire_l298n_right.png", "L298N > RIGHT", "Motor B Terminal"),
        ("07_wire_ultra_echo.png", "ULTRA ECHO", "GPIO 26 < HC-SR04"),
        ("08_wire_ultra_trig.png", "ULTRA TRIG", "GPIO 25 > HC-SR04"),
        ("09_wire_sensor_5v.png", "SENSOR 5V", "Pin 2 > HC-SR04 VCC"),
        ("10_wire_sensor_gnd.png", "SENSOR GND", "Pin 6 > HC-SR04 GND"),
        ("11_wire_pan_servo.png", "PAN SERVO", "GPIO 12 > MG90S"),
        ("12_wire_tilt_servo.png", "TILT SERVO", "GPIO 13 > MG90S"),
        ("13_wire_18650.png", "18650 > L298N", "7.4V IN - CHECK +/-"),
        ("14_wire_common_gnd.png", "COMMON GND", "Pi GND <> L298N GND"),
    ]
    for fname, fn, gpio in wire_labels:
        labels.append(("WIRE", make_wire_label(fname, fn, gpio), fn))

    # ── BOARD LABELS (18mm tape) ──
    board_labels = [
        ("15_board_pi5.png", "RASPBERRY PI 5", "ESCORT BOT BRAIN - 5V/3A USB-C"),
        ("16_board_l298n.png", "L298N MOTOR DRIVER", "7.4V IN - 2 CH - IN1-IN4"),
        ("17_board_hcsr04.png", "HC-SR04 ULTRASONIC", "FRONT OBSTACLE - 5V>3.3V DIVIDER"),
        ("18_board_divider.png", "VOLTAGE DIVIDER", "1k + 2k - 5V ECHO > 3.3V SAFE"),
        ("19_board_arducam.png", "ARDUCAM IMX708", "120deg FOV - CSI RIBBON - AF"),
        ("20_board_pantilt.png", "PAN/TILT PLATFORM", "2x MG90S - PAN G12 - TILT G13"),
    ]
    for fname, name, detail in board_labels:
        labels.append(("BOARD", make_board_label(fname, name, detail), name))

    # ── POWER LABELS (24mm tape) ──
    labels.append(("POWER", make_power_label(
        "21_power_18650.png", "!",
        "18650 PACK - 7.4V",
        "MOTORS ONLY - CHECK POLARITY - NOT PI"
    ), "18650 PACK"))
    labels.append(("POWER", make_power_label(
        "22_power_bank.png", "*",
        "POWER BANK - 5V",
        "RASPBERRY PI ONLY - 3A MIN - USB-C"
    ), "POWER BANK"))

    # ── ORIENTATION LABELS (24mm tape) ──
    orient_labels = [
        ("23_orient_front.png", "FRONT", "^"),
        ("24_orient_left.png", "LEFT", "<"),
        ("25_orient_right.png", "RIGHT", ">"),
        ("26_orient_cam_up.png", "CAM UP", "^"),
    ]
    for fname, direction, arrow in orient_labels:
        labels.append(("ORIENT", make_orient_label(fname, direction, arrow), direction))

    # ── BRANDING (24mm tape) ──
    labels.append(("BRAND", make_brand_label("27_brand_elktron.png"), "ELKTRON"))

    return labels


def print_sequentially(labels):
    """Open each label in P-Touch Editor one at a time."""
    print(f"\n{'='*50}")
    print(f"  ESCORT BOT LABELS — {len(labels)} labels to print")
    print(f"  Recommended tape: Wire=12mm, Board=18mm, Power/Orient/Brand=24mm")
    print(f"{'='*50}\n")

    for i, (category, path, name) in enumerate(labels, 1):
        print(f"\n[{i}/{len(labels)}] {category}: {name}")
        print(f"  File: {os.path.basename(path)}")
        print(f"  Opening in P-Touch Editor...")

        # Open in P-Touch Editor
        subprocess.run(["open", "-a", "P-touch Editor", path])

        if i < len(labels):
            input(f"  >>> Press ENTER after printing to load next label...")
        else:
            print(f"\n  All {len(labels)} labels sent. Done!")


if __name__ == "__main__":
    labels = generate_all()
    print(f"Generated {len(labels)} label images in: {OUT_DIR}/")

    for cat, path, name in labels:
        print(f"  [{cat:6s}] {name:25s} -> {os.path.basename(path)}")

    if "--print" in sys.argv:
        print_sequentially(labels)
    else:
        print(f"\nTo print one at a time, run:")
        print(f"  python3 {__file__} --print")
