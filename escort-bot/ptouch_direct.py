#!/usr/bin/env python3
"""Direct Brother PT-D610BT label printer via Bluetooth serial.
No P-Touch Editor needed. Sends raster data directly to the printer.

Protocol: Brother PTCBP raster mode over Bluetooth SPP.
Reference: Brother PT-E550W/P750W/P710BT Raster Command Reference

Usage:
  python3 ptouch_direct.py                   # Print all 27 labels
  python3 ptouch_direct.py --test            # Print first label only
  python3 ptouch_direct.py --list            # List labels without printing
  python3 ptouch_direct.py --start 5         # Start from label #5
"""

import argparse
import struct
import sys
import time

import serial
from PIL import Image, ImageDraw, ImageFont

# ── Printer Config ──────────────────────────────────────
SERIAL_PORT = "/dev/cu.PT-D610BT0817"
BAUD_RATE = 9600

# PT-D610BT with 24mm tape
# 24mm tape = 128 dots printable width at 180 DPI
# The raster line is 128 bits = 16 bytes
TAPE_PIXELS = 128  # 24mm tape width in dots
BYTES_PER_LINE = 16  # 128 / 8
TAPE_WIDTH_MM = 24

# Margins (non-printable area on each side of tape)
MARGIN_DOTS = 12  # ~12 dots margin on each side
PRINTABLE_PIXELS = TAPE_PIXELS - (2 * MARGIN_DOTS)  # ~104 usable pixels

# Cable wrap labels — these categories get text printed twice with a gap
WRAP_CATEGORIES = {"MOTOR", "SENSOR", "SERVO", "POWER"}
WRAP_GAP_PIXELS = 80  # ~11mm blank gap for cable wrap at 180 DPI

# ── Fonts ───────────────────────────────────────────────
def get_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/SFMono-Bold.otf" if bold else "/System/Library/Fonts/SFMono-Regular.otf",
        "/System/Library/Fonts/Menlo.ttc",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


# ── Label Image Generator ──────────────────────────────
def _draw_text_block(label_width, label_height, line1, line2, font_l1, font_l2, text1_w, text2_w, bbox1):
    """Draw a single text block (used once for flat labels, twice for wrap labels)."""
    img = Image.new("1", (label_width, label_height), 1)  # 1 = white
    draw = ImageDraw.Draw(img)

    if line2:
        y1 = (label_height // 2 - 30)
        y2 = (label_height // 2 + 5)
        x1 = (label_width - text1_w) // 2
        x2 = (label_width - text2_w) // 2
        draw.text((x1, y1), line1, font=font_l1, fill=0)
        draw.text((x2, y2), line2, font=font_l2, fill=0)
    else:
        y1 = (label_height - (bbox1[3] - bbox1[1])) // 2
        x1 = (label_width - text1_w) // 2
        draw.text((x1, y1), line1, font=font_l1, fill=0)

    return img


def create_label_image(line1, line2="", bold_line1=True, wrap=False):
    """Create a 1-bit label image ready for the printer.

    If wrap=True, text is printed twice with a blank gap in between,
    so the label can be folded around a cable with both sides readable.
    """
    label_height = TAPE_PIXELS

    font_l1 = get_font(28 if not line2 else 24, bold=bold_line1)
    font_l2 = get_font(14)

    # Measure text
    temp_img = Image.new("1", (1000, label_height), 1)
    temp_draw = ImageDraw.Draw(temp_img)

    bbox1 = temp_draw.textbbox((0, 0), line1, font=font_l1)
    text1_w = bbox1[2] - bbox1[0]

    text2_w = 0
    if line2:
        bbox2 = temp_draw.textbbox((0, 0), line2, font=font_l2)
        text2_w = bbox2[2] - bbox2[0]

    block_width = max(text1_w, text2_w) + 40  # padding
    block_width = max(block_width, 100)  # minimum length

    # Draw the text block
    block = _draw_text_block(block_width, label_height, line1, line2,
                             font_l1, font_l2, text1_w, text2_w, bbox1)

    if wrap:
        # Cable wrap: [text] [gap] [text]
        total_width = block_width + WRAP_GAP_PIXELS + block_width
        img = Image.new("1", (total_width, label_height), 1)
        img.paste(block, (0, 0))
        img.paste(block, (block_width + WRAP_GAP_PIXELS, 0))
    else:
        img = block

    # Rotate 90 degrees clockwise for printer (label feeds lengthwise)
    img = img.rotate(-90, expand=True)

    # Mirror horizontally (required by protocol)
    img = img.transpose(Image.FLIP_LEFT_RIGHT)

    return img


def image_to_raster(img):
    """Convert a 1-bit PIL Image to raster lines (list of 16-byte chunks).

    Each line is BYTES_PER_LINE (16) bytes = 128 pixels wide = tape width.
    The image height becomes the number of raster lines (label length).
    """
    # Ensure image width is exactly TAPE_PIXELS (128)
    w, h = img.size
    if w != TAPE_PIXELS:
        # Pad or crop to 128 pixels wide, centered
        new_img = Image.new("1", (TAPE_PIXELS, h), 1)  # white
        offset = (TAPE_PIXELS - w) // 2
        if offset >= 0:
            new_img.paste(img, (offset, 0))
        else:
            new_img.paste(img.crop((-offset, 0, -offset + TAPE_PIXELS, h)), (0, 0))
        img = new_img

    # Convert to raw bytes
    pixels = img.tobytes()

    raster_lines = []
    for row in range(h):
        line = bytearray(BYTES_PER_LINE)
        for col in range(TAPE_PIXELS):
            pixel_idx = row * TAPE_PIXELS + col
            if pixel_idx < len(pixels):
                # In 1-bit mode: 0 = black (print), 1 = white (no print)
                # Brother protocol: 1 = print dot, 0 = no dot
                # So we need to invert
                if pixels[pixel_idx] == 0:  # black pixel
                    byte_idx = col // 8
                    bit_idx = 7 - (col % 8)
                    line[byte_idx] |= (1 << bit_idx)
        raster_lines.append(bytes(line))

    return raster_lines


# ── Printer Communication ──────────────────────────────

def send_label(ser, raster_lines):
    """Send a single label to the printer using PTCBP raster protocol."""

    num_lines = len(raster_lines)

    # 1. Clear buffer (100 null bytes)
    ser.write(b"\x00" * 100)
    time.sleep(0.1)

    # 2. Initialize (ESC @)
    ser.write(b"\x1b\x40")
    time.sleep(0.1)

    # 3. Enter raster graphics mode (ESC i a 1)
    ser.write(b"\x1b\x69\x61\x01")
    time.sleep(0.05)

    # 4. Set media & quality (ESC i z ...)
    # Byte structure for PT-D610BT 24mm tape:
    # 0x1B 0x69 0x7A — command
    # PI: 0x84 — print info valid flags (width + length + quality)
    # Media type: 0x01 — laminated tape
    # Tape width: 24 (mm)
    # Label height: 0 (continuous)
    # Raster lines: num_lines (2 bytes LE)
    # Starting page: 0
    # 0x00 padding
    media_cmd = bytearray(b"\x1b\x69\x7a")
    media_cmd += b"\x84"  # print info flags
    media_cmd += b"\x01"  # media type: laminated
    media_cmd += bytes([TAPE_WIDTH_MM])  # tape width mm
    media_cmd += b"\x00"  # label height (0 = continuous)
    media_cmd += struct.pack("<I", num_lines)  # raster lines (4 bytes LE)
    media_cmd += b"\x00"  # starting page
    media_cmd += b"\x00"  # padding
    ser.write(media_cmd)
    time.sleep(0.05)

    # 5. Set print chaining off (last label)
    ser.write(b"\x1b\x69\x4b\x08")
    time.sleep(0.05)

    # 6. Set auto-cut on (each label)
    ser.write(b"\x1b\x69\x4d\x40")
    time.sleep(0.05)

    # 7. Set margin/feed (0)
    ser.write(b"\x1b\x69\x64\x00\x00")
    time.sleep(0.05)

    # 8. Set compression mode: no compression (0x00)
    # Using uncompressed for simplicity — \x4D\x00
    ser.write(b"\x4d\x00")
    time.sleep(0.05)

    # 9. Send raster data lines
    for line_data in raster_lines:
        # Uncompressed raster: G + n1 + n2 + data
        # n1,n2 = length of data (16 bytes for 24mm)
        ser.write(b"\x47")
        ser.write(struct.pack("<H", len(line_data)))
        ser.write(line_data)

    # 10. Print with feeding (SUB = 0x1A)
    ser.write(b"\x1a")
    time.sleep(0.5)


# ── Label Definitions ──────────────────────────────────

LABELS = [
    # (category, line1, line2)
    ("MOTOR",  "LEFT FWD",       "GPIO17 > IN1"),
    ("MOTOR",  "LEFT BWD",       "GPIO27 > IN2"),
    ("MOTOR",  "RIGHT FWD",      "GPIO22 > IN3"),
    ("MOTOR",  "RIGHT BWD",      "GPIO23 > IN4"),
    ("MOTOR",  "L298N > LEFT",   "Motor A Terminal"),
    ("MOTOR",  "L298N > RIGHT",  "Motor B Terminal"),
    ("SENSOR", "ULTRA ECHO",     "GPIO24 < HC-SR04"),
    ("SENSOR", "ULTRA TRIG",     "GPIO25 > HC-SR04"),
    ("SENSOR", "SENSOR 5V",      "Pin2 > HC-SR04 VCC"),
    ("SENSOR", "SENSOR GND",     "Pin6 > HC-SR04 GND"),
    ("SERVO",  "PAN SERVO",      "GPIO12 > MG90S"),
    ("SERVO",  "TILT SERVO",     "GPIO13 > MG90S"),
    ("POWER",  "18650 > L298N",  "7.4V IN CHECK +/-"),
    ("POWER",  "COMMON GND",     "Pi GND <> L298N GND"),
    ("BOARD",  "RASPBERRY PI 5", "5V/3A USB-C"),
    ("BOARD",  "L298N DRIVER",   "7.4V 2CH IN1-IN4"),
    ("BOARD",  "HC-SR04",        "5V>3.3V DIVIDER"),
    ("BOARD",  "V-DIVIDER",      "1k+2k 3.3V SAFE"),
    ("BOARD",  "ARDUCAM IMX708", "CSI RIBBON AF"),
    ("BOARD",  "PAN/TILT",       "PAN G12 TILT G13"),
    ("WARN",   "18650 7.4V",     "MOTORS ONLY!"),
    ("WARN",   "BANK 5V USB-C",  "PI ONLY 3A MIN"),
    ("DIR",    "FRONT",          ""),
    ("DIR",    "LEFT",           ""),
    ("DIR",    "RIGHT",          ""),
    ("DIR",    "CAM UP",         ""),
    ("BRAND",  "ELKTRON",        "CW HACKATHON 2026"),
]


def main():
    parser = argparse.ArgumentParser(description="Direct Brother PT-D610BT label printer")
    parser.add_argument("--test", action="store_true", help="Print first label only")
    parser.add_argument("--list", action="store_true", help="List labels without printing")
    parser.add_argument("--start", type=int, default=1, help="Start from label number")
    parser.add_argument("--port", default=SERIAL_PORT, help="Serial port path")
    parser.add_argument("--preview", action="store_true", help="Save preview PNGs instead of printing")
    args = parser.parse_args()

    labels_to_print = LABELS[args.start - 1:]
    if args.test:
        labels_to_print = labels_to_print[:1]

    print(f"\n{'='*55}")
    print(f"  ESCORT BOT — DIRECT LABEL PRINTER")
    print(f"  {len(labels_to_print)} labels | PT-D610BT | 24mm tape")
    print(f"  Port: {args.port}")
    print(f"  FULLY AUTOMATED — no P-Touch Editor needed!")
    print(f"{'='*55}\n")

    if args.list:
        for i, (cat, l1, l2) in enumerate(LABELS, 1):
            display = f"{l1} / {l2}" if l2 else l1
            print(f"  [{i:2d}] {cat:6s} | {display}")
        return

    if args.preview:
        import os
        os.makedirs("labels_preview", exist_ok=True)
        for i, (cat, l1, l2) in enumerate(labels_to_print, args.start):
            wrap = cat in WRAP_CATEGORIES
            img = create_label_image(l1, l2, wrap=wrap)
            path = f"labels_preview/{i:02d}_{cat.lower()}.png"
            # Save un-rotated for human viewing
            preview = create_label_image(l1, l2, wrap=wrap)
            preview = preview.transpose(Image.FLIP_LEFT_RIGHT)
            preview = preview.rotate(90, expand=True)
            preview.save(path)
            print(f"  [{i:2d}] {cat:6s} | {l1:20s} -> {path}")
        print(f"\n  Previews saved to labels_preview/")
        return

    # Open serial connection
    print(f"  Connecting to {args.port}...")
    try:
        ser = serial.Serial(args.port, BAUD_RATE, timeout=5)
        time.sleep(1)  # let connection stabilize
        print(f"  Connected!\n")
    except serial.SerialException as e:
        print(f"  ERROR: Cannot open {args.port}: {e}")
        print(f"  Make sure the printer is on and paired via Bluetooth.")
        sys.exit(1)

    try:
        for i, (cat, l1, l2) in enumerate(labels_to_print, args.start):
            display = f"{l1} / {l2}" if l2 else l1
            print(f"  [{i:2d}/{len(LABELS)}] {cat:6s} | {display}")

            # Generate label image
            wrap = cat in WRAP_CATEGORIES
            img = create_label_image(l1, l2, wrap=wrap)

            # Convert to raster lines
            raster = image_to_raster(img)
            print(f"           {img.size[0]}x{img.size[1]}px, {len(raster)} raster lines")

            # Send to printer
            print(f"           Printing... ", end="", flush=True)
            send_label(ser, raster)
            print(f"done!")

            # Brief pause between labels
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n\n  Interrupted. Closing connection.")
    except Exception as e:
        print(f"\n  ERROR: {e}")
    finally:
        ser.close()
        print(f"\n  Connection closed.")

    print(f"\n{'='*55}")
    print(f"  All labels printed!")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
