#!/usr/bin/env python3
"""Escort Bot — P-Touch Label Generator v2
Styled labels matching labels.pdf aesthetic, sized for PT-D610BT 24mm tape.
Uses clipboard paste — no window switching required.

Usage:
  python3 ptouch_labels_v2.py              # Generate PNGs only
  python3 ptouch_labels_v2.py --print      # Generate + paste into P-Touch Editor one at a time
"""

import os
import subprocess
import sys
import time
from PIL import Image, ImageDraw, ImageFont

# ── Config ──────────────────────────────────────────────
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "labels_ptouch_v2")
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 180
TAPE_H = 128  # 24mm tape = 0.94" = ~128px at 180 DPI

# Category colors (left bar + accent)
COLORS = {
    "MOTOR":  (30, 132, 73),    # green
    "SENSOR": (36, 113, 163),   # blue
    "SERVO":  (125, 60, 152),   # purple
    "POWER":  (192, 57, 43),    # red
    "BOARD":  (40, 40, 40),     # dark gray
    "ORIENT": (80, 80, 80),     # gray
    "BRAND":  (26, 26, 26),     # near-black
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)


def get_font(size, bold=False, mono=False):
    if mono:
        paths = [
            "/System/Library/Fonts/SFMono-Bold.otf" if bold else "/System/Library/Fonts/SFMono-Regular.otf",
            "/System/Library/Fonts/Menlo.ttc",
        ]
    else:
        paths = [
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        ]
        if bold:
            paths = [
                "/System/Library/Fonts/SFNSBold.otf",
                "/System/Library/Fonts/SFNS.ttf",
                "/Library/Fonts/Arial Bold.ttf",
            ] + paths
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


# ── Label Builders ──────────────────────────────────────

def make_wire_label(filename, fn_text, gpio_text, category):
    """Wire flag label — wraps around wire, same text both halves."""
    color = COLORS.get(category, BLACK)
    bar_w = 8
    w = int(2.5 * DPI)  # 2.5 inches long
    h = TAPE_H

    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    # Left color bar
    draw.rectangle([(0, 0), (bar_w, h)], fill=color)

    # Fold line (center horizontal dashed line)
    fold_y = h // 2
    dash_len = 6
    for x in range(bar_w + 4, w - 4, dash_len * 2):
        draw.line([(x, fold_y), (x + dash_len, fold_y)], fill=COLORS["POWER"], width=1)

    # "FOLD" text at right of fold line
    font_fold = get_font(7, mono=True)
    draw.text((w - 35, fold_y - 5), "FOLD", fill=COLORS["POWER"], font=font_fold)

    # Top half — function name + GPIO
    font_fn = get_font(20, bold=True, mono=True)
    font_gpio = get_font(11, mono=True)
    font_cat = get_font(8, bold=True)

    # Function name (top half, centered vertically)
    draw.text((bar_w + 10, 8), fn_text, fill=BLACK, font=font_fn)
    draw.text((bar_w + 10, 32), gpio_text, fill=GRAY, font=font_gpio)

    # Category tag top-right
    cat_text = category.upper()
    bbox = draw.textbbox((0, 0), cat_text, font=font_cat)
    cat_w = bbox[2] - bbox[0]
    draw.text((w - cat_w - 10, 8), cat_text, fill=color, font=font_cat)

    # Bottom half — mirror (for flag fold)
    draw.text((bar_w + 10, fold_y + 8), fn_text, fill=BLACK, font=font_fn)
    draw.text((bar_w + 10, fold_y + 32), gpio_text, fill=GRAY, font=font_gpio)

    # Bottom border accent
    draw.rectangle([(0, h - 2), (w, h)], fill=color)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_board_label(filename, name_text, detail_text):
    """Board/module identification label."""
    color = COLORS["BOARD"]
    bar_w = 8
    w = int(3.0 * DPI)
    h = TAPE_H

    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    # Left color bar
    draw.rectangle([(0, 0), (bar_w, h)], fill=color)
    # Bottom accent
    draw.rectangle([(0, h - 3), (w, h)], fill=color)

    font_name = get_font(20, bold=True)
    font_detail = get_font(11, mono=True)
    font_tag = get_font(8, bold=True)

    # Name
    draw.text((bar_w + 12, 18), name_text, fill=BLACK, font=font_name)

    # Detail
    draw.text((bar_w + 12, 52), detail_text, fill=GRAY, font=font_detail)

    # "ELKTRON" watermark bottom-right
    draw.text((w - 60, h - 18), "ELKTRON", fill=LIGHT_GRAY, font=font_tag)

    # Corner marks
    mark_color = (180, 180, 180)
    for cx, cy in [(bar_w + 2, 2), (w - 6, 2), (bar_w + 2, h - 6), (w - 6, h - 6)]:
        draw.rectangle([(cx, cy), (cx + 4, cy + 4)], outline=mark_color, width=1)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_power_label(filename, name_text, warning_text, is_motor=True):
    """Safety-critical power source label."""
    color = COLORS["POWER"] if is_motor else COLORS["SENSOR"]
    w = int(3.5 * DPI)
    h = TAPE_H

    bg = (253, 237, 236) if is_motor else (234, 242, 248)
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # Heavy border
    draw.rectangle([(0, 0), (w - 1, h - 1)], outline=color, width=4)

    font_icon = get_font(28, bold=True)
    font_name = get_font(20, bold=True)
    font_warn = get_font(10, bold=True, mono=True)

    # Warning icon
    icon = "!" if is_motor else "*"
    draw.text((14, 14), icon, fill=color, font=font_icon)

    # Name
    draw.text((50, 16), name_text, fill=color, font=font_name)

    # Warning text
    draw.text((14, 58), warning_text, fill=BLACK, font=font_warn)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_orient_label(filename, direction, arrow_char):
    """Chassis orientation label."""
    w = int(2.0 * DPI)
    h = TAPE_H

    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (w - 1, h - 1)], outline=BLACK, width=2)

    font_dir = get_font(28, bold=True)
    font_arrow = get_font(42, bold=True)

    # Direction centered
    bbox = draw.textbbox((0, 0), direction, font=font_dir)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 8), direction, fill=BLACK, font=font_dir)

    # Arrow centered below
    bbox2 = draw.textbbox((0, 0), arrow_char, font=font_arrow)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((w - tw2) // 2, 55), arrow_char, fill=BLACK, font=font_arrow)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


def make_brand_label(filename):
    """ELKTRON branding label — white on black."""
    w = int(4.0 * DPI)
    h = TAPE_H

    img = Image.new("RGB", (w, h), BLACK)
    draw = ImageDraw.Draw(img)

    font_team = get_font(36, bold=True)
    font_sub = get_font(11, mono=True)

    # ELKTRON centered
    text = "E L K T R O N"
    bbox = draw.textbbox((0, 0), text, font=font_team)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 10), text, fill=WHITE, font=font_team)

    # Subtitle
    sub = "ESCORT BOT  -  COREWEAVE HACKATHON 2026"
    bbox2 = draw.textbbox((0, 0), sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((w - tw2) // 2, 70), sub, fill=(170, 170, 170), font=font_sub)

    path = os.path.join(OUT_DIR, filename)
    img.save(path, dpi=(DPI, DPI))
    return path


# ── Label Definitions ───────────────────────────────────

def generate_all():
    labels = []

    # Wire labels — motor (green bar)
    wires_motor = [
        ("01_left_fwd.png",    "LEFT FWD",      "GPIO 17 -> L298N IN1"),
        ("02_left_bwd.png",    "LEFT BWD",      "GPIO 24 -> L298N IN2"),
        ("03_right_fwd.png",   "RIGHT FWD",     "GPIO 22 -> L298N IN3"),
        ("04_right_bwd.png",   "RIGHT BWD",     "GPIO 23 -> L298N IN4"),
        ("05_l298n_left.png",  "L298N -> LEFT",  "Motor A Terminal"),
        ("06_l298n_right.png", "L298N -> RIGHT", "Motor B Terminal"),
    ]
    for f, fn, gpio in wires_motor:
        labels.append(("WIRE", make_wire_label(f, fn, gpio, "MOTOR"), fn))

    # Wire labels — sensor (blue bar)
    wires_sensor = [
        ("07_ultra_echo.png", "ULTRA ECHO",  "GPIO 26 <- HC-SR04"),
        ("08_ultra_trig.png", "ULTRA TRIG",  "GPIO 25 -> HC-SR04"),
        ("09_sensor_5v.png",  "SENSOR 5V",   "Pin 2 -> HC-SR04 VCC"),
        ("10_sensor_gnd.png", "SENSOR GND",  "Pin 6 -> HC-SR04 GND"),
    ]
    for f, fn, gpio in wires_sensor:
        labels.append(("WIRE", make_wire_label(f, fn, gpio, "SENSOR"), fn))

    # Wire labels — servo (purple bar)
    wires_servo = [
        ("11_pan_servo.png",  "PAN SERVO",   "GPIO 12 -> MG90S"),
        ("12_tilt_servo.png", "TILT SERVO",  "GPIO 13 -> MG90S"),
    ]
    for f, fn, gpio in wires_servo:
        labels.append(("WIRE", make_wire_label(f, fn, gpio, "SERVO"), fn))

    # Wire labels — power (red bar)
    wires_power = [
        ("13_18650_wire.png",   "18650 -> L298N",  "7.4V IN - CHECK +/-"),
        ("14_common_gnd.png",   "COMMON GND",      "Pi GND <-> L298N GND"),
    ]
    for f, fn, gpio in wires_power:
        labels.append(("WIRE", make_wire_label(f, fn, gpio, "POWER"), fn))

    # Board labels
    boards = [
        ("15_pi5.png",       "RASPBERRY PI 5",      "ESCORT BOT BRAIN - 5V/3A USB-C"),
        ("16_l298n.png",     "L298N MOTOR DRIVER",   "7.4V IN - 2 CH - IN1-IN4"),
        ("17_hcsr04.png",    "HC-SR04 ULTRASONIC",   "FRONT OBSTACLE - 5V>3.3V DIV"),
        ("18_divider.png",   "VOLTAGE DIVIDER",      "1k + 2k - 5V ECHO > 3.3V SAFE"),
        ("19_arducam.png",   "ARDUCAM IMX708",       "120 FOV - CSI RIBBON - AF"),
        ("20_pantilt.png",   "PAN/TILT PLATFORM",    "2x MG90S - PAN G12 - TILT G13"),
    ]
    for f, name, detail in boards:
        labels.append(("BOARD", make_board_label(f, name, detail), name))

    # Power labels
    labels.append(("POWER", make_power_label(
        "21_pwr_18650.png", "18650 PACK - 7.4V",
        "MOTORS ONLY - CHECK POLARITY - NOT PI", True
    ), "18650 PACK"))
    labels.append(("POWER", make_power_label(
        "22_pwr_bank.png", "POWER BANK - 5V",
        "RASPBERRY PI ONLY - 3A MIN - USB-C", False
    ), "POWER BANK"))

    # Orientation
    for f, d, a in [("23_front.png","FRONT","^"), ("24_left.png","LEFT","<"),
                     ("25_right.png","RIGHT",">"), ("26_cam_up.png","CAM UP","^")]:
        labels.append(("ORIENT", make_orient_label(f, d, a), d))

    # Branding
    labels.append(("BRAND", make_brand_label("27_elktron.png"), "ELKTRON"))

    return labels


# ── Clipboard Paste Automation ──────────────────────────

def copy_image_to_clipboard(image_path):
    """Copy a PNG image to the macOS clipboard."""
    abs_path = os.path.abspath(image_path)
    script = f'set the clipboard to (read (POSIX file "{abs_path}") as «class PNGf»)'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.returncode == 0


def paste_into_ptouch_and_return():
    """Activate P-Touch Editor, Cmd+A delete, Cmd+V paste, then return to iTerm."""
    script = '''
    -- Get the name of the current frontmost app (to return to it)
    tell application "System Events"
        set callerApp to name of first application process whose frontmost is true
    end tell

    -- Switch to P-Touch Editor
    tell application "P-touch Editor"
        activate
    end tell
    delay 0.8

    tell application "System Events"
        tell process "P-touch Editor"
            set frontmost to true
            delay 0.3

            -- Clear existing content
            keystroke "a" using command down
            delay 0.2
            key code 51
            delay 0.3

            -- Paste image from clipboard
            keystroke "v" using command down
            delay 0.5
        end tell
    end tell

    -- Switch back to caller (iTerm/Terminal)
    tell application callerApp
        activate
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True, text=True)


def print_in_ptouch_and_return():
    """Activate P-Touch Editor, hit its Print button, return to caller."""
    script = '''
    tell application "System Events"
        set callerApp to name of first application process whose frontmost is true
    end tell

    tell application "P-touch Editor"
        activate
    end tell
    delay 0.6

    tell application "System Events"
        tell process "P-touch Editor"
            set frontmost to true
            delay 0.3

            -- Try the toolbar Print button first
            try
                click button "Print" of toolbar 1 of window 1
                delay 2
            on error
                -- Fallback: File > Print menu
                try
                    click menu item "Print" of menu "File" of menu bar 1
                    delay 2
                    -- Confirm dialog
                    try
                        click button "Print" of sheet 1 of window 1
                    on error
                        keystroke return
                    end try
                end try
            end try
        end tell
    end tell

    delay 1

    -- Return to caller
    tell application callerApp
        activate
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True, text=True)


# ── Main ────────────────────────────────────────────────

def main():
    labels = generate_all()

    print(f"\nGenerated {len(labels)} styled labels in: {OUT_DIR}/")
    for cat, path, name in labels:
        print(f"  [{cat:6s}] {name:25s} -> {os.path.basename(path)}")

    if "--print" not in sys.argv:
        print(f"\nTo print: python3 {os.path.basename(__file__)} --print")
        return

    print(f"\n{'='*58}")
    print(f"  ESCORT BOT — STYLED P-TOUCH LABELS")
    print(f"  {len(labels)} labels | PT-D610BT | 24mm tape")
    print(f"  Clipboard paste — no window switching needed!")
    print(f"{'='*58}")
    print(f"\n  Make sure P-Touch Editor is open with a blank label.")
    print(f"  You stay in this terminal the whole time.\n")

    input("  Ready? [ENTER] to start: ")

    for i, (category, path, name) in enumerate(labels, 1):
        print(f"\n  [{i:2d}/{len(labels)}] {category:6s} | {name}")

        choice = input(f"  [ENTER] Paste & print  |  [s] Skip  |  [q] Quit: ").strip().lower()
        if choice == "q":
            print(f"\n  Stopped at #{i}. Run again to continue.")
            break
        elif choice == "s":
            print(f"  Skipped.")
            continue

        # Copy image to clipboard
        print(f"  Copying to clipboard...")
        if not copy_image_to_clipboard(path):
            print(f"  ERROR: Could not copy image to clipboard.")
            continue

        # Paste into P-Touch Editor (auto-switches and returns)
        print(f"  Pasting into P-Touch Editor...")
        paste_into_ptouch_and_return()

        # Ask to print
        action = input(f"  Pasted! [ENTER] Print  |  [s] Skip print: ").strip().lower()
        if action != "s":
            print(f"  Printing...")
            print_in_ptouch_and_return()
            time.sleep(1)
            print(f"  Done!")

    print(f"\n{'='*58}")
    print(f"  All labels complete!")
    print(f"{'='*58}\n")


if __name__ == "__main__":
    main()
