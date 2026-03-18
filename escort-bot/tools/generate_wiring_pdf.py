#!/usr/bin/env python3
"""Generate Escort Bot — 100% Visual Wiring Diagram PDF.
Every component drawn as a recognizable shape with color-coded wires."""

from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
import os, math

OUT = os.path.join(os.path.dirname(__file__), "wiring-diagram.pdf")
W, H = landscape(LETTER)

# ─── Palette ──────────────────────────────────────────────
BG        = HexColor("#0a0a0c")
PANEL     = HexColor("#141416")
ACCENT    = HexColor("#c9943a")
TEXT      = HexColor("#e8e4dc")
DIM       = HexColor("#6b6860")
PI_GREEN  = HexColor("#1a6b3a")
PI_LIGHT  = HexColor("#2ecc71")
L298N_RED = HexColor("#b83230")
L298N_DK  = HexColor("#8b2524")
TERM_BLUE = HexColor("#2471a3")
HC_BLUE   = HexColor("#1a5276")
HC_SILVER = HexColor("#bdc3c7")
MOTOR_YEL = HexColor("#d4ac0d")
MOTOR_DK  = HexColor("#9a7d0a")
SERVO_BLU = HexColor("#2e86c1")
CAM_GREEN = HexColor("#1e8449")
BATT_GRAY = HexColor("#515a5a")
BATT_GOLD = HexColor("#d4a017")
PB_BLACK  = HexColor("#1c1c1e")
LCD_BLUE  = HexColor("#1b4f72")
LCD_BLACK = HexColor("#0b0b0b")
# Wire colors
W_BLUE    = HexColor("#2d5fa0")
W_LBLUE   = HexColor("#3a7daa")
W_ORANGE  = HexColor("#e67e22")
W_YELLOW  = HexColor("#f1c40f")
W_PURPLE  = HexColor("#8e44ad")
W_LPURPLE = HexColor("#a855f7")
W_RED     = HexColor("#e74c3c")
W_BLACK   = HexColor("#3a3a3a")
W_GREEN   = HexColor("#27ae60")
W_LGREEN  = HexColor("#5aad64")
W_CSI     = HexColor("#9b59b6")
W_GOLD    = HexColor("#ddaa00")
W_USB     = HexColor("#e74c3c")


def rrect(c, x, y, w, h, r=4):
    """Rounded rect path (no fill/stroke — caller does that)."""
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    return p


def filled_rrect(c, x, y, w, h, r=4, fill=None, stroke=None, lw=1):
    p = rrect(c, x, y, w, h, r)
    if fill: c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)


def label(c, x, y, text, size=7, color=TEXT, font="Helvetica", align="left"):
    c.setFillColor(color); c.setFont(font, size)
    if align == "center": c.drawCentredString(x, y, text)
    elif align == "right": c.drawRightString(x, y, text)
    else: c.drawString(x, y, text)


def wire(c, pts, color, lw=2):
    """Draw a polyline wire through list of (x,y) points."""
    c.setStrokeColor(color); c.setLineWidth(lw); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    c.drawPath(p, fill=0, stroke=1)


def wire_dot(c, x, y, color, r=3):
    c.setFillColor(color); c.circle(x, y, r, fill=1, stroke=0)


# ═══════════════════════════════════════════════════════════
# COMPONENT DRAWING FUNCTIONS
# ═══════════════════════════════════════════════════════════

def draw_raspberry_pi(c, x, y):
    """Raspberry Pi 5 — green PCB, GPIO header, USB-C, CSI, ethernet."""
    w, h = 160, 110
    # PCB
    filled_rrect(c, x, y, w, h, 5, fill=PI_GREEN, stroke=PI_LIGHT, lw=2)
    # Mounting holes (4 corners)
    for hx, hy in [(x+8, y+8), (x+w-8, y+8), (x+8, y+h-8), (x+w-8, y+h-8)]:
        c.setFillColor(HexColor("#0d3d1a")); c.circle(hx, hy, 4, fill=1, stroke=0)
        c.setFillColor(BATT_GRAY); c.circle(hx, hy, 2, fill=1, stroke=0)
    # SoC (center square)
    filled_rrect(c, x+55, y+35, 30, 30, 2, fill=HexColor("#2c2c2c"))
    filled_rrect(c, x+57, y+37, 26, 26, 1, fill=HexColor("#444444"))
    label(c, x+70, y+48, "BCM", 5, HexColor("#888888"), align="center")
    label(c, x+70, y+40, "2712", 5, HexColor("#888888"), align="center")
    # RAM chip
    filled_rrect(c, x+95, y+40, 20, 20, 1, fill=HexColor("#333333"))
    label(c, x+105, y+48, "4GB", 4, DIM, align="center")
    # GPIO header — 2 rows of 20 gold pins along top edge
    for col in range(20):
        for row in range(2):
            px = x + 18 + col * 6.2
            py = y + h - 12 - row * 6
            c.setFillColor(BATT_GOLD)
            c.rect(px-1.5, py-1.5, 3, 3, fill=1, stroke=0)
    label(c, x + 18, y + h - 4, "GPIO 40-pin", 5, HexColor("#a0d8b0"))
    # USB-C power port (bottom edge)
    filled_rrect(c, x + 10, y - 4, 16, 8, 3, fill=HexColor("#555555"), stroke=HexColor("#888888"), lw=0.5)
    label(c, x + 18, y - 12, "USB-C", 4, DIM, align="center")
    # CSI camera connector (right edge)
    filled_rrect(c, x + w - 4, y + 55, 8, 18, 2, fill=HexColor("#444444"))
    label(c, x + w + 6, y + 62, "CSI", 4, DIM)
    # USB-A ports (bottom-right)
    for i in range(2):
        filled_rrect(c, x + w - 30 + i*14, y - 4, 12, 8, 1, fill=HexColor("#3a7daa"))
    # Ethernet (bottom far right)
    filled_rrect(c, x + w - 4, y + 10, 8, 16, 1, fill=HexColor("#ddaa00"))
    # HDMI ports
    for i in range(2):
        filled_rrect(c, x + 35 + i*18, y - 4, 14, 6, 1, fill=HexColor("#333333"))
    # Label
    label(c, x + w/2, y + 25, "RASPBERRY PI 5", 8, white, "Helvetica-Bold", "center")
    label(c, x + w/2, y + 15, "Bookworm 64-bit", 5, HexColor("#a0d8b0"), align="center")
    # Return pin connection points
    return {
        "gpio17": (x + 18 + 0*6.2, y + h - 12),   # leftmost pins
        "gpio24": (x + 18 + 1*6.2, y + h - 12),
        "gpio22": (x + 18 + 2*6.2, y + h - 12),
        "gpio23": (x + 18 + 3*6.2, y + h - 12),
        "gpio26": (x + 18 + 4*6.2, y + h - 12),
        "gpio25": (x + 18 + 5*6.2, y + h - 12),
        "gpio12": (x + 18 + 6*6.2, y + h - 12),
        "gpio13": (x + 18 + 7*6.2, y + h - 12),
        "5v":     (x + 18 + 8*6.2, y + h - 18),
        "5v2":    (x + 18 + 9*6.2, y + h - 18),   # second 5V (Pin 4)
        "gnd":    (x + 18 + 10*6.2, y + h - 18),   # L298N GND
        "gnd2":   (x + 18 + 11*6.2, y + h - 18),  # HC-SR04 GND
        "gnd3":   (x + 18 + 12*6.2, y + h - 18),  # Servo GND
        "gnd4":   (x + 18 + 13*6.2, y + h - 18),  # LCD GND
        "gpio2":  (x + 18 + 14*6.2, y + h - 12),  # I2C SDA
        "gpio3":  (x + 18 + 15*6.2, y + h - 12),  # I2C SCL
        "usbc":   (x + 18, y - 4),
        "csi":    (x + w + 4, y + 64),
        "center": (x + w/2, y + h/2),
    }


def draw_l298n(c, x, y):
    """L298N motor driver — red PCB, black heatsink, blue terminals, pins."""
    w, h = 120, 110
    # PCB
    filled_rrect(c, x, y, w, h, 4, fill=L298N_RED, stroke=HexColor("#dd4444"), lw=1.5)
    # Heatsink (large black rectangle with fins)
    hs_x, hs_y, hs_w, hs_h = x+25, y+35, 70, 45
    filled_rrect(c, hs_x, hs_y, hs_w, hs_h, 2, fill=HexColor("#1a1a1a"))
    # Heatsink fins
    for i in range(8):
        fx = hs_x + 4 + i * 8.5
        c.setStrokeColor(HexColor("#333333")); c.setLineWidth(0.5)
        c.line(fx, hs_y + 3, fx, hs_y + hs_h - 3)
    # IC chip under heatsink
    filled_rrect(c, hs_x+20, hs_y+10, 30, 25, 1, fill=HexColor("#0d0d0d"))
    label(c, hs_x+35, hs_y+22, "L298N", 5, HexColor("#555555"), align="center")
    # Blue screw terminals — motor outputs (left and right sides)
    # Left terminals (Motor A outputs)
    for i in range(2):
        ty = y + h - 20 - i*14
        filled_rrect(c, x-4, ty, 14, 10, 2, fill=TERM_BLUE, stroke=HexColor("#1a5276"), lw=1)
        c.setFillColor(HexColor("#aaaaaa")); c.circle(x+3, ty+5, 2, fill=1, stroke=0)
    label(c, x - 6, y + h - 8, "OUT", 4, DIM, align="center")
    label(c, x - 6, y + h - 14, "A", 5, W_GOLD, "Helvetica-Bold", "center")
    # Right terminals (Motor B outputs)
    for i in range(2):
        ty = y + h - 20 - i*14
        filled_rrect(c, x+w-10, ty, 14, 10, 2, fill=TERM_BLUE, stroke=HexColor("#1a5276"), lw=1)
        c.setFillColor(HexColor("#aaaaaa")); c.circle(x+w-3, ty+5, 2, fill=1, stroke=0)
    label(c, x + w + 6, y + h - 8, "OUT", 4, DIM, align="center")
    label(c, x + w + 6, y + h - 14, "B", 5, W_GOLD, "Helvetica-Bold", "center")
    # Power terminal (top — +12V, GND, +5V)
    for i in range(3):
        tx = x + 30 + i * 20
        filled_rrect(c, tx, y + h - 4, 14, 10, 2, fill=TERM_BLUE, stroke=HexColor("#1a5276"), lw=1)
        c.setFillColor(HexColor("#aaaaaa")); c.circle(tx+7, y+h+1, 2, fill=1, stroke=0)
    label(c, x+37, y+h+8, "+12V", 4, W_RED)
    label(c, x+57, y+h+8, "GND", 4, DIM)
    label(c, x+77, y+h+8, "+5V", 4, W_ORANGE)
    # Input pins (bottom row — ENA, IN1-IN4, ENB)
    pin_labels = ["ENA", "IN1", "IN2", "IN3", "IN4", "ENB"]
    pin_colors = [DIM, W_BLUE, W_LBLUE, W_ORANGE, W_YELLOW, DIM]
    for i, (pl, pc) in enumerate(zip(pin_labels, pin_colors)):
        px = x + 10 + i * 17
        c.setFillColor(pc if pc != DIM else HexColor("#666666"))
        c.rect(px, y-2, 3, 8, fill=1, stroke=0)
        label(c, px+1, y-10, pl, 4, pc, align="center")
    # Jumper caps on ENA/ENB (ON = full speed)
    filled_rrect(c, x+9, y+3, 5, 6, 1, fill=HexColor("#222222"))
    label(c, x+11, y+10, "ON", 3.5, W_GREEN, align="center")
    filled_rrect(c, x+10+5*17-1, y+3, 5, 6, 1, fill=HexColor("#222222"))
    label(c, x+10+5*17+1, y+10, "ON", 3.5, W_GREEN, align="center")
    # Label
    label(c, x + w/2, y + 15, "L298N DRIVER", 7, white, "Helvetica-Bold", "center")
    label(c, x + w/2, y + 6, "Dual H-Bridge", 5, HexColor("#f0b0b0"), align="center")
    # Connection points
    return {
        "in1": (x + 10 + 1*17 + 1.5, y - 2),
        "in2": (x + 10 + 2*17 + 1.5, y - 2),
        "in3": (x + 10 + 3*17 + 1.5, y - 2),
        "in4": (x + 10 + 4*17 + 1.5, y - 2),
        "12v": (x + 37, y + h + 6),
        "gnd": (x + 57, y + h + 6),
        "outA_top": (x - 4, y + h - 15),
        "outA_bot": (x - 4, y + h - 29),
        "outB_top": (x + w + 4, y + h - 15),
        "outB_bot": (x + w + 4, y + h - 29),
        "center": (x + w/2, y + h/2),
    }


def draw_hcsr04(c, x, y):
    """HC-SR04 ultrasonic sensor — blue PCB, 2 silver transducer cylinders."""
    w, h = 90, 50
    # PCB
    filled_rrect(c, x, y, w, h, 3, fill=HC_BLUE, stroke=HexColor("#2980b9"), lw=1.5)
    # Two ultrasonic transducers (the "eyes")
    for i in range(2):
        cx_t = x + 25 + i * 40
        cy_t = y + h/2 + 3
        # Silver outer ring
        c.setFillColor(HC_SILVER); c.circle(cx_t, cy_t, 14, fill=1, stroke=0)
        c.setFillColor(HexColor("#95a5a6")); c.circle(cx_t, cy_t, 11, fill=1, stroke=0)
        # Mesh pattern (concentric circles)
        c.setStrokeColor(HexColor("#7f8c8d")); c.setLineWidth(0.3)
        for r in [3, 6, 9]:
            c.circle(cx_t, cy_t, r, fill=0, stroke=1)
    # Crystal/resonator (small rectangle between)
    filled_rrect(c, x + 40, y + h/2 - 4, 10, 8, 1, fill=HexColor("#333333"))
    # 4 pins at bottom
    pin_labels = ["VCC", "TRIG", "ECHO", "GND"]
    pin_colors = [W_RED, W_PURPLE, W_LPURPLE, W_BLACK]
    for i, (pl, pc) in enumerate(zip(pin_labels, pin_colors)):
        px = x + 15 + i * 18
        c.setFillColor(BATT_GOLD); c.rect(px, y - 6, 2, 8, fill=1, stroke=0)
        label(c, px + 1, y - 14, pl, 4, pc, align="center")
    # Label
    label(c, x + w/2, y + 4, "HC-SR04", 6, white, "Helvetica-Bold", "center")
    return {
        "vcc":  (x + 16, y - 6),
        "trig": (x + 34, y - 6),
        "echo": (x + 52, y - 6),
        "gnd":  (x + 70, y - 6),
    }


def draw_motor(c, x, y, label_text="MOTOR"):
    """TT DC Motor — yellow body, silver shaft, wires."""
    w, h = 50, 30
    # Body
    filled_rrect(c, x, y, w, h, 3, fill=MOTOR_YEL, stroke=MOTOR_DK, lw=1.5)
    # Shaft
    filled_rrect(c, x + w, y + h/2 - 3, 14, 6, 2, fill=HC_SILVER, stroke=BATT_GRAY, lw=0.5)
    # Gear housing bump
    filled_rrect(c, x - 6, y + 5, 8, h - 10, 2, fill=MOTOR_DK)
    # Wire tabs
    c.setFillColor(W_RED); c.rect(x + 8, y - 3, 4, 5, fill=1, stroke=0)
    c.setFillColor(W_BLACK); c.rect(x + 18, y - 3, 4, 5, fill=1, stroke=0)
    # Label
    label(c, x + w/2, y + h/2 - 3, label_text, 5, HexColor("#5a4a0a"), "Helvetica-Bold", "center")
    return {"wire_in": (x + 13, y - 3)}


def draw_servo(c, x, y, lbl="PAN"):
    """MG90S micro servo — blue body, white horn."""
    w, h = 40, 25
    # Body
    filled_rrect(c, x, y, w, h, 2, fill=SERVO_BLU, stroke=HexColor("#1a5276"), lw=1)
    # Mounting tabs
    filled_rrect(c, x - 5, y + 5, 6, 3, 1, fill=SERVO_BLU)
    filled_rrect(c, x + w - 1, y + 5, 6, 3, 1, fill=SERVO_BLU)
    # Horn (white circle + arm)
    cx_h = x + w - 10
    c.setFillColor(white); c.circle(cx_h, y + h - 3, 6, fill=1, stroke=0)
    c.setFillColor(HexColor("#dddddd")); c.circle(cx_h, y + h - 3, 2, fill=1, stroke=0)
    filled_rrect(c, cx_h - 1, y + h, 2, 8, 1, fill=white)
    # Wire bundle (3 wires out bottom)
    for i, wc in enumerate([HexColor("#8b4513"), W_RED, HexColor("#444444")]):
        c.setFillColor(wc); c.rect(x + 10 + i*4, y - 5, 2, 7, fill=1, stroke=0)
    label(c, x + w/2, y + h/2 - 3, lbl, 5, white, "Helvetica-Bold", "center")
    label(c, x + w/2, y + 2, "MG90S", 4, HexColor("#aaccee"), align="center")
    return {"wire_in": (x + 14, y - 5)}


def draw_camera(c, x, y):
    """Arducam IMX708 — square green PCB with lens."""
    w, h = 45, 40
    filled_rrect(c, x, y, w, h, 3, fill=CAM_GREEN, stroke=HexColor("#27ae60"), lw=1)
    # Lens housing (black circle)
    cx_l, cy_l = x + w/2, y + h/2 + 3
    c.setFillColor(HexColor("#111111")); c.circle(cx_l, cy_l, 12, fill=1, stroke=0)
    c.setFillColor(HexColor("#222233")); c.circle(cx_l, cy_l, 8, fill=1, stroke=0)
    c.setFillColor(HexColor("#334455")); c.circle(cx_l, cy_l, 4, fill=1, stroke=0)
    # Ribbon connector
    filled_rrect(c, x + 10, y - 3, 25, 5, 1, fill=HexColor("#444444"))
    label(c, x + w/2, y + 4, "IMX708", 4, HexColor("#a0d8b0"), align="center")
    return {"ribbon": (x + 22, y - 3)}


def draw_power_bank(c, x, y):
    """Anker USB-C power bank — rounded black body, LED indicators."""
    w, h = 130, 40
    # Body
    filled_rrect(c, x, y, w, h, 8, fill=PB_BLACK, stroke=HexColor("#333333"), lw=1.5)
    # Anker logo area
    label(c, x + 20, y + h/2 + 3, "ANKER", 9, HexColor("#4a9eff"), "Helvetica-Bold")
    label(c, x + 20, y + h/2 - 7, "10,000 mAh", 5, HexColor("#666666"))
    # LED indicators
    for i in range(4):
        c.setFillColor(HexColor("#00cc44") if i < 3 else HexColor("#333333"))
        c.circle(x + 80 + i * 8, y + h/2, 2, fill=1, stroke=0)
    # USB-C port
    filled_rrect(c, x + w - 3, y + h/2 - 5, 8, 10, 3, fill=HexColor("#555555"))
    label(c, x + w + 7, y + h/2 - 2, "USB-C", 4, DIM)
    return {"usbc": (x + w + 5, y + h/2)}


def draw_battery_pack(c, x, y):
    """18650 battery pack — 2 cylindrical cells in a holder."""
    w, h = 100, 45
    # Holder
    filled_rrect(c, x, y, w, h, 4, fill=HexColor("#2c2c2c"), stroke=BATT_GRAY, lw=1)
    # Two 18650 cells
    for i in range(2):
        cx_b = x + 25 + i * 50
        # Cell body (cylindrical look via rounded rect)
        filled_rrect(c, cx_b - 18, y + 8, 36, 28, 6, fill=BATT_GRAY, stroke=HexColor("#666666"), lw=0.5)
        # Positive nub
        filled_rrect(c, cx_b - 4, y + h - 2, 8, 5, 2, fill=BATT_GOLD)
        # Label
        label(c, cx_b, y + 20, "18650", 5, HexColor("#888888"), align="center")
    # Series wiring indicator
    c.setStrokeColor(W_RED); c.setLineWidth(1)
    c.line(x + 25 + 18, y + 22, x + 75 - 18, y + 22)
    # Output wires
    c.setFillColor(W_RED); c.rect(x + w - 3, y + h - 10, 6, 3, fill=1, stroke=0)
    c.setFillColor(W_BLACK); c.rect(x + w - 3, y + 10, 6, 3, fill=1, stroke=0)
    label(c, x + w/2, y + 2, "7.4V (series)", 5, BATT_GOLD, align="center")
    return {
        "pos": (x + w + 3, y + h - 9),
        "neg": (x + w + 3, y + 11),
    }


def draw_lcd(c, x, y):
    """QA-Pass LCD screen — blue PCB, black display."""
    w, h = 70, 45
    # PCB
    filled_rrect(c, x, y, w, h, 3, fill=LCD_BLUE, stroke=HexColor("#2471a3"), lw=1)
    # Display area
    filled_rrect(c, x + 5, y + 10, w - 10, h - 15, 2, fill=LCD_BLACK)
    # Pixel grid hint
    c.setStrokeColor(HexColor("#0a1a2a")); c.setLineWidth(0.2)
    for row in range(3):
        ry = y + 14 + row * 8
        c.line(x + 8, ry, x + w - 8, ry)
    # "QA-PASS" sticker
    filled_rrect(c, x + 15, y + 2, 40, 7, 1, fill=HexColor("#ddcc00"))
    label(c, x + 35, y + 3, "QA-PASS", 4, black, "Helvetica-Bold", "center")
    # I2C pins
    pin_labels = ["GND", "VCC", "SDA", "SCL"]
    for i, pl in enumerate(pin_labels):
        px = x + 10 + i * 15
        c.setFillColor(BATT_GOLD); c.rect(px, y - 5, 2, 7, fill=1, stroke=0)
        label(c, px + 1, y - 13, pl, 3.5, DIM, align="center")
    label(c, x + w/2, y + h - 5, "I2C LCD", 5, HexColor("#aaccee"), align="center")
    return {
        "gnd": (x + 11, y - 5),
        "vcc": (x + 26, y - 5),
        "sda": (x + 41, y - 5),
        "scl": (x + 56, y - 5),
    }


# ═══════════════════════════════════════════════════════════
# WIRE ROUTING HELPERS
# ═══════════════════════════════════════════════════════════

def route_L(c, x1, y1, x2, y2, color, lw=2, mid_pct=0.5):
    """Route wire: go horizontal to midpoint, then vertical, then horizontal."""
    mx = x1 + (x2 - x1) * mid_pct
    wire(c, [(x1, y1), (mx, y1), (mx, y2), (x2, y2)], color, lw)


def route_down_over(c, x1, y1, x2, y2, color, lw=2, drop=20):
    """Drop down, go horizontal, go up/down to target."""
    wire(c, [(x1, y1), (x1, y1 - drop), (x2, y2 - drop if y2 < y1 else y2 + drop), (x2, y2)], color, lw)


# ═══════════════════════════════════════════════════════════
# PAGE 1: FULL SYSTEM WIRING DIAGRAM
# ═══════════════════════════════════════════════════════════

def page1(c):
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1)

    # Title
    label(c, 30, H - 30, "ESCORT BOT — WIRING DIAGRAM", 18, ACCENT, "Helvetica-Bold")
    label(c, 30, H - 45, "Elktron Hackathon  |  All connections  |  BCM pin numbering", 8, DIM)

    # ─── Place components ─────────────────────────────────
    # Pi 5 (center)
    pi = draw_raspberry_pi(c, 310, 280)

    # L298N (left of Pi)
    l298n = draw_l298n(c, 60, 260)

    # HC-SR04 (top right)
    hc = draw_hcsr04(c, 580, 460)

    # 4 Motors — left pair (Channel A) far left, right pair (Channel B) far right
    fl = draw_motor(c, 10, 440, "FL")
    rl = draw_motor(c, 10, 390, "RL")
    fr = draw_motor(c, 690, 440, "FR")
    rr = draw_motor(c, 690, 390, "RR")

    # Pan/tilt servos (right)
    pan = draw_servo(c, 590, 340, "PAN")
    tilt = draw_servo(c, 650, 340, "TILT")

    # Camera (far right, clear of FR motor)
    cam = draw_camera(c, 705, 460)

    # Power bank (top left)
    pb = draw_power_bank(c, 80, 500)

    # Battery pack (bottom left)
    batt = draw_battery_pack(c, 60, 120)

    # LCD screen (bottom right)
    lcd = draw_lcd(c, 580, 210)

    # ─── Draw wires ───────────────────────────────────────

    # GPIO -> L298N control wires (4 wires)
    gpio_l298n = [
        (pi["gpio17"], l298n["in1"], W_BLUE, "GPIO17 -> IN1"),
        (pi["gpio24"], l298n["in2"], W_LBLUE, "GPIO24 -> IN2"),
        (pi["gpio22"], l298n["in3"], W_ORANGE, "GPIO22 -> IN3"),
        (pi["gpio23"], l298n["in4"], W_YELLOW, "GPIO23 -> IN4"),
    ]
    for i, (src, dst, color, _lbl) in enumerate(gpio_l298n):
        drop = 25 + i * 10
        wire(c, [src, (src[0], src[1] + drop), (dst[0], dst[1] - 15 - i*3), (dst[0], dst[1])], color, 1.8)
        wire_dot(c, src[0], src[1], color, 2)
        wire_dot(c, dst[0], dst[1], color, 2)
        # Pin label at source
        label(c, src[0] - 1, src[1] + drop + 4, _lbl.split(" -> ")[0][-2:], 4, color, align="center")

    # Pi GND -> L298N GND
    route_L(c, pi["gnd"][0], pi["gnd"][1], l298n["gnd"][0], l298n["gnd"][1], W_BLACK, 2.5, 0.3)
    wire_dot(c, pi["gnd"][0], pi["gnd"][1], W_BLACK, 2.5)
    wire_dot(c, l298n["gnd"][0], l298n["gnd"][1], W_BLACK, 2.5)

    # L298N OUT -> Motors
    # Channel A (left pair) -> FL, RL — wires go left
    wire(c, [l298n["outA_top"], (l298n["outA_top"][0] - 15, l298n["outA_top"][1]),
             (fl["wire_in"][0] + 30, fl["wire_in"][1] + 15), fl["wire_in"]], W_GOLD, 2)
    wire(c, [l298n["outA_bot"], (l298n["outA_bot"][0] - 20, l298n["outA_bot"][1]),
             (rl["wire_in"][0] + 30, rl["wire_in"][1] + 15), rl["wire_in"]], W_GOLD, 2)
    # Channel B (right pair) -> FR, RR — wires go right
    wire(c, [l298n["outB_top"], (l298n["outB_top"][0] + 25, l298n["outB_top"][1]),
             (l298n["outB_top"][0] + 25, 465),
             (fr["wire_in"][0] - 8, 465), (fr["wire_in"][0] - 8, fr["wire_in"][1]),
             fr["wire_in"]], W_GOLD, 2)
    wire(c, [l298n["outB_bot"], (l298n["outB_bot"][0] + 30, l298n["outB_bot"][1]),
             (l298n["outB_bot"][0] + 30, 415),
             (rr["wire_in"][0] - 8, 415), (rr["wire_in"][0] - 8, rr["wire_in"][1]),
             rr["wire_in"]], W_GOLD, 2)

    # Battery -> L298N +12V
    wire(c, [batt["pos"], (batt["pos"][0] + 20, batt["pos"][1]),
             (l298n["12v"][0], batt["pos"][1]),
             l298n["12v"]], W_RED, 2.5)
    wire(c, [batt["neg"], (batt["neg"][0] + 25, batt["neg"][1]),
             (l298n["gnd"][0] + 10, batt["neg"][1]),
             (l298n["gnd"][0] + 10, l298n["gnd"][1]),
             l298n["gnd"]], W_BLACK, 2.5)

    # Pi -> HC-SR04 (4 wires, spaced 14pt apart)
    hc_base = pi["gpio25"][1] + 55
    wire(c, [pi["gpio25"], (pi["gpio25"][0], hc_base),
             (hc["trig"][0], hc_base),
             (hc["trig"][0], hc["trig"][1] + 20), hc["trig"]], W_PURPLE, 1.8)
    wire(c, [pi["gpio26"], (pi["gpio26"][0], hc_base + 14),
             (hc["echo"][0], hc_base + 14),
             (hc["echo"][0], hc["echo"][1] + 20), hc["echo"]], W_LPURPLE, 1.8)
    wire(c, [pi["5v"], (pi["5v"][0], hc_base + 28),
             (hc["vcc"][0], hc_base + 28),
             (hc["vcc"][0], hc["vcc"][1] + 20), hc["vcc"]], W_RED, 1.5)
    wire(c, [pi["gnd2"], (pi["gnd2"][0], hc_base + 42),
             (hc["gnd"][0], hc_base + 42),
             (hc["gnd"][0], hc["gnd"][1] + 20), hc["gnd"]], W_BLACK, 1.5)
    for p in [hc["trig"], hc["echo"], hc["vcc"], hc["gnd"]]:
        wire_dot(c, p[0], p[1], ACCENT, 2)

    # Pi -> Servos (signal + VCC + GND — each servo has 3 wires)
    # Signal wires (12pt apart)
    servo_sig_base = pi["gpio12"][1] + 38
    wire(c, [pi["gpio12"], (pi["gpio12"][0], servo_sig_base),
             (pan["wire_in"][0], servo_sig_base),
             (pan["wire_in"][0], pan["wire_in"][1] + 10), pan["wire_in"]], W_GREEN, 1.8)
    wire(c, [pi["gpio13"], (pi["gpio13"][0], servo_sig_base - 12),
             (tilt["wire_in"][0], servo_sig_base - 12),
             (tilt["wire_in"][0], tilt["wire_in"][1] + 10), tilt["wire_in"]], W_LGREEN, 1.8)
    # Servo VCC (5V from Pi) — shared bus to both servos
    servo_vcc_y = pi["5v2"][1] + 52
    wire(c, [pi["5v2"], (pi["5v2"][0], servo_vcc_y),
             (pan["wire_in"][0] + 5, servo_vcc_y),
             (pan["wire_in"][0] + 5, pan["wire_in"][1] + 10)], W_RED, 1.8)
    wire(c, [(pan["wire_in"][0] + 5, servo_vcc_y),
             (tilt["wire_in"][0] + 5, servo_vcc_y),
             (tilt["wire_in"][0] + 5, tilt["wire_in"][1] + 10)], W_RED, 1.8)
    # Servo GND — shared bus (separate GND pin from HC-SR04)
    servo_gnd_y = servo_vcc_y + 12
    wire(c, [pi["gnd3"], (pi["gnd3"][0], servo_gnd_y),
             (pan["wire_in"][0] + 10, servo_gnd_y),
             (pan["wire_in"][0] + 10, pan["wire_in"][1] + 10)], W_BLACK, 1.8)
    wire(c, [(pan["wire_in"][0] + 10, servo_gnd_y),
             (tilt["wire_in"][0] + 10, servo_gnd_y),
             (tilt["wire_in"][0] + 10, tilt["wire_in"][1] + 10)], W_BLACK, 1.8)

    # Pi CSI -> Camera
    wire(c, [pi["csi"], (pi["csi"][0] + 40, pi["csi"][1]),
             (cam["ribbon"][0] + 40, cam["ribbon"][1]),
             cam["ribbon"]], W_CSI, 3)
    label(c, pi["csi"][0] + 50, pi["csi"][1] + 5, "CSI RIBBON", 5, W_CSI)

    # Power bank -> Pi USB-C
    wire(c, [pb["usbc"], (pb["usbc"][0] + 20, pb["usbc"][1]),
             (pi["usbc"][0] - 20, pb["usbc"][1]),
             (pi["usbc"][0] - 20, pi["usbc"][1]),
             pi["usbc"]], W_USB, 3)
    label(c, pb["usbc"][0] + 25, pb["usbc"][1] + 5, "USB-C (5V/3A)", 5, W_USB)

    # Pi -> LCD (I2C — 4 wires: SDA, SCL, VCC, GND)
    W_I2C_SDA = HexColor("#3498db")
    W_I2C_SCL = HexColor("#2ecc71")
    # SDA: GPIO2 -> LCD SDA
    i2c_bus_y = pi["gpio2"][1] + 75
    wire(c, [pi["gpio2"], (pi["gpio2"][0], i2c_bus_y),
             (lcd["sda"][0], i2c_bus_y), lcd["sda"]], W_I2C_SDA, 1.5)
    wire_dot(c, pi["gpio2"][0], pi["gpio2"][1], W_I2C_SDA, 2)
    # SCL: GPIO3 -> LCD SCL (14pt below SDA)
    wire(c, [pi["gpio3"], (pi["gpio3"][0], i2c_bus_y + 14),
             (lcd["scl"][0], i2c_bus_y + 14), lcd["scl"]], W_I2C_SCL, 1.5)
    wire_dot(c, pi["gpio3"][0], pi["gpio3"][1], W_I2C_SCL, 2)
    # LCD VCC (from Pi 5V — actually connects from pin)
    lcd_vcc_y = i2c_bus_y + 28
    wire(c, [pi["5v"], (pi["5v"][0], lcd_vcc_y),
             (lcd["vcc"][0], lcd_vcc_y), lcd["vcc"]], W_RED, 1.5)
    # LCD GND (from dedicated GND pin — 14pt below VCC)
    lcd_gnd_y = lcd_vcc_y + 14
    wire(c, [pi["gnd4"], (pi["gnd4"][0], lcd_gnd_y),
             (lcd["gnd"][0], lcd_gnd_y), lcd["gnd"]], W_BLACK, 1.5)
    label(c, lcd["sda"][0] + 15, lcd["sda"][1] + 30, "I2C", 5, W_I2C_SDA)

    # ─── Voltage divider callout ──────────────────────────
    vd_x, vd_y = 530, 430
    filled_rrect(c, vd_x, vd_y, 45, 20, 3, fill=HexColor("#2c1810"), stroke=W_YELLOW, lw=1)
    label(c, vd_x + 5, vd_y + 7, "1k + 2k", 5, W_YELLOW)
    label(c, vd_x + 5, vd_y + 1, "divider!", 4, W_RED)

    # ─── Wire legend ──────────────────────────────────────
    leg_x, leg_y = 590, 90
    filled_rrect(c, leg_x, leg_y, 160, 110, 6, fill=PANEL, stroke=DIM, lw=0.5)
    label(c, leg_x + 8, leg_y + 95, "WIRE COLORS", 7, ACCENT, "Helvetica-Bold")
    legend = [
        ("Motor ctrl (IN1-4)", W_BLUE), ("Motor output", W_GOLD),
        ("Ultrasonic", W_PURPLE), ("Servo signal", W_GREEN),
        ("I2C (SDA/SCL)", HexColor("#3498db")),
        ("Power (+)", W_RED), ("Ground", W_BLACK), ("CSI ribbon", W_CSI),
    ]
    for i, (ltxt, lcolor) in enumerate(legend):
        ly = leg_y + 80 - i * 10
        c.setStrokeColor(lcolor); c.setLineWidth(2.5)
        c.line(leg_x + 8, ly + 1, leg_x + 28, ly + 1)
        label(c, leg_x + 32, ly - 2, ltxt, 5.5, TEXT)

    # ─── Critical note ────────────────────────────────────
    note_y = 30
    filled_rrect(c, 30, note_y, W - 60, 45, 6, fill=HexColor("#1a1008"), stroke=W_YELLOW, lw=1.5)
    label(c, 45, note_y + 30, "CRITICAL", 9, W_YELLOW, "Helvetica-Bold")
    label(c, 45, note_y + 17, "Common GND between Pi and L298N required  |  HC-SR04 ECHO needs voltage divider (5V -> 3.3V)", 7, TEXT)
    label(c, 45, note_y + 5, "Do NOT power Pi from Smart Car Board  |  Pi needs dedicated 5V/3A+ USB-C bank  |  Left motors parallel = Ch.A  |  Right = Ch.B", 6, DIM)


# ═══════════════════════════════════════════════════════════
# PAGE 2: GPIO CLOSE-UP
# ═══════════════════════════════════════════════════════════

def page2(c):
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1)
    label(c, 30, H - 30, "GPIO HEADER — PIN REFERENCE", 18, ACCENT, "Helvetica-Bold")
    label(c, 30, H - 45, "BCM numbering  |  Physical pin numbers  |  Used pins highlighted", 8, DIM)

    # Draw large GPIO header — 2 columns, 20 rows
    hdr_x = W/2 - 120
    hdr_y = 60
    row_h = 24
    col_gap = 240

    # Header background
    filled_rrect(c, hdr_x - 15, hdr_y - 10, col_gap + 30, 20 * row_h + 20, 8, fill=HexColor("#0d3d1a"), stroke=PI_LIGHT, lw=2)

    # Pin data: (phys, bcm_label, role, color, connection)
    odd_pins = [
        (1, "3.3V", "", ACCENT, ""), (3, "GPIO2", "SDA", HexColor("#3498db"), "LCD SDA"), (5, "GPIO3", "SCL", HexColor("#2ecc71"), "LCD SCL"),
        (7, "GPIO4", "", DIM, ""), (9, "GND", "", W_BLACK, ""), (11, "GPIO17", "L-FWD", W_BLUE, "L298N IN1"),
        (13, "GPIO24", "L-BWD", W_LBLUE, "L298N IN2"), (15, "GPIO22", "R-FWD", W_ORANGE, "L298N IN3"),
        (17, "3.3V", "", ACCENT, ""), (19, "GPIO10", "MOSI", DIM, ""), (21, "GPIO9", "MISO", DIM, ""),
        (23, "GPIO11", "SCLK", DIM, ""), (25, "GND", "", W_BLACK, ""), (27, "GPIO0", "", DIM, ""),
        (29, "GPIO5", "", DIM, ""), (31, "GPIO6", "", DIM, ""), (33, "GPIO13", "TILT", W_LGREEN, "Tilt servo"),
        (35, "GPIO19", "", DIM, ""), (37, "GPIO26", "ECHO", W_LPURPLE, "HC-SR04 (divider!)"), (39, "GND", "", W_BLACK, ""),
    ]
    even_pins = [
        (2, "5V", "", W_RED, "HC-SR04 VCC"), (4, "5V", "", W_RED, "Servos VCC"), (6, "GND", "", W_BLACK, "HC-SR04/L298N"),
        (8, "GPIO14", "TX", DIM, ""), (10, "GPIO15", "RX", DIM, ""), (12, "GPIO18", "", DIM, ""),
        (14, "GND", "", W_BLACK, ""), (16, "GPIO23", "R-BWD", W_YELLOW, "L298N IN4"),
        (18, "GPIO24", "L-BWD", W_LBLUE, "L298N IN2"), (20, "GND", "", W_BLACK, ""),
        (22, "GPIO25", "TRIG", W_PURPLE, "HC-SR04 TRIG"), (24, "GPIO8", "CE0", DIM, ""),
        (26, "GPIO7", "CE1", DIM, ""), (28, "GPIO1", "", DIM, ""), (30, "GND", "", W_BLACK, ""),
        (32, "GPIO12", "PAN", W_GREEN, "Pan servo"), (34, "GND", "", W_BLACK, ""),
        (36, "GPIO16", "", DIM, ""), (38, "GPIO20", "", DIM, ""), (40, "GPIO21", "", DIM, ""),
    ]

    for i, (phys, bcm, role, color, conn) in enumerate(odd_pins):
        py = hdr_y + (19 - i) * row_h
        used = color != DIM
        if used:
            filled_rrect(c, hdr_x - 12, py - 5, col_gap/2 - 5, row_h - 2, 3, fill=HexColor("#1a2a1a"))
        # Pin dot
        c.setFillColor(BATT_GOLD if used else HexColor("#555555"))
        c.circle(hdr_x, py + 5, 5, fill=1, stroke=0)
        # Physical number
        label(c, hdr_x + 10, py + 2, str(phys), 7, color if used else DIM, "Helvetica-Bold" if used else "Helvetica")
        # BCM
        label(c, hdr_x + 28, py + 2, bcm, 7, color if used else DIM, "Helvetica-Bold" if used else "Helvetica")
        # Role
        if role:
            label(c, hdr_x + 75, py + 2, role, 6, color if used else DIM)
        # Connection
        if conn:
            label(c, hdr_x + 105, py + 2, conn, 5, TEXT)

    for i, (phys, bcm, role, color, conn) in enumerate(even_pins):
        py = hdr_y + (19 - i) * row_h
        used = color != DIM
        rx = hdr_x + col_gap
        if used:
            filled_rrect(c, rx - col_gap/2 + 17, py - 5, col_gap/2 - 5, row_h - 2, 3, fill=HexColor("#1a2a1a"))
        c.setFillColor(BATT_GOLD if used else HexColor("#555555"))
        c.circle(rx, py + 5, 5, fill=1, stroke=0)
        label(c, rx - 10, py + 2, str(phys), 7, color if used else DIM, "Helvetica-Bold" if used else "Helvetica", "right")
        label(c, rx - 28, py + 2, bcm, 7, color if used else DIM, "Helvetica-Bold" if used else "Helvetica", "right")
        if role:
            label(c, rx - 75, py + 2, role, 6, color if used else DIM, align="right")
        if conn:
            label(c, rx - 105, py + 2, conn, 5, TEXT, align="right")

    # Summary
    label(c, W/2, hdr_y - 25, "10 GPIO pins used  |  4 motor control  |  2 ultrasonic  |  2 servo  |  2 I2C (LCD)", 8, TEXT, align="center")


# ═══════════════════════════════════════════════════════════
# PAGE 3: POWER FLOW
# ═══════════════════════════════════════════════════════════

def page3(c):
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1)
    label(c, 30, H - 30, "POWER DISTRIBUTION", 18, ACCENT, "Helvetica-Bold")
    label(c, 30, H - 45, "Two independent sources  |  Never cross them  |  Common GND required", 8, DIM)

    # Source 1: USB-C Power Bank -> Pi -> downstream
    y1 = H - 130
    pb = draw_power_bank(c, 40, y1)
    # Arrow
    c.setStrokeColor(W_USB); c.setLineWidth(4)
    c.line(180, y1 + 20, 250, y1 + 20)
    # Arrowhead
    c.setFillColor(W_USB)
    p = c.beginPath(); p.moveTo(250, y1+20); p.lineTo(242, y1+27); p.lineTo(242, y1+13); p.close()
    c.drawPath(p, fill=1, stroke=0)
    label(c, 195, y1 + 28, "5V / 3A+", 7, W_USB, "Helvetica-Bold")
    pi = draw_raspberry_pi(c, 260, y1 - 30)

    # Pi feeds downstream
    label(c, 450, y1 + 25, "Pi 5V rail feeds:", 7, TEXT, "Helvetica-Bold")
    downstream = ["HC-SR04 VCC (via 5V pin)", "Pan servo VCC (~150mA)", "Tilt servo VCC (~150mA)", "Camera (CSI, internal)"]
    for i, d in enumerate(downstream):
        label(c, 455, y1 + 12 - i*12, d, 6, DIM)

    # Source 2: Battery -> L298N -> Motors
    y2 = y1 - 200
    batt = draw_battery_pack(c, 40, y2)
    c.setStrokeColor(W_RED); c.setLineWidth(4)
    c.line(150, y2 + 25, 220, y2 + 25)
    c.setFillColor(W_RED)
    p = c.beginPath(); p.moveTo(220, y2+25); p.lineTo(212, y2+32); p.lineTo(212, y2+18); p.close()
    c.drawPath(p, fill=1, stroke=0)
    label(c, 160, y2 + 33, "7.4V", 7, W_RED, "Helvetica-Bold")
    l298n = draw_l298n(c, 230, y2 - 20)

    # L298N -> Motors
    c.setStrokeColor(W_GOLD); c.setLineWidth(4)
    c.line(360, y2 + 25, 430, y2 + 25)
    c.setFillColor(W_GOLD)
    p = c.beginPath(); p.moveTo(430, y2+25); p.lineTo(422, y2+32); p.lineTo(422, y2+18); p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Draw 4 motors in a row
    mx = 450
    for i, name in enumerate(["FL", "RL", "FR", "RR"]):
        draw_motor(c, mx + i*70, y2 + 5, name)

    # Common GND box
    gy = y2 - 100
    filled_rrect(c, 40, gy, W - 80, 55, 8, fill=HexColor("#2c1810"), stroke=W_YELLOW, lw=3)
    label(c, 60, gy + 37, "COMMON GROUND — MANDATORY", 12, W_YELLOW, "Helvetica-Bold")
    label(c, 60, gy + 20, "Pi GND (Pin 6) must connect to L298N GND terminal. Without this, GPIO signals have no reference.", 8, TEXT)
    label(c, 60, gy + 6, "Both power sources share ground through this single wire. Diagram above shows separate sources but shared GND.", 7, DIM)

    # DO NOT box
    dy = gy - 65
    filled_rrect(c, 40, dy, W - 80, 50, 8, fill=HexColor("#2c1015"), stroke=W_RED, lw=3)
    label(c, 60, dy + 32, "DO NOT power Pi from Smart Car Board 5V regulator", 11, W_RED, "Helvetica-Bold")
    label(c, 60, dy + 14, "The onboard 5V regulator cannot supply 3A+ that Pi 5 needs under OpenCV load. Use a dedicated USB-C power bank.", 7, TEXT)

    # Voltage divider detail
    vdx, vdy = 40, dy - 110
    filled_rrect(c, vdx, vdy, 340, 85, 8, fill=PANEL, stroke=W_PURPLE, lw=2)
    label(c, vdx + 15, vdy + 68, "VOLTAGE DIVIDER — HC-SR04 ECHO PIN", 9, W_PURPLE, "Helvetica-Bold")
    label(c, vdx + 15, vdy + 52, "ECHO outputs 5V. Pi GPIO is 3.3V tolerant. Must divide down.", 7, TEXT)
    # Draw the divider circuit
    cx = vdx + 30
    cy = vdy + 30
    # ECHO pin
    label(c, cx, cy + 5, "ECHO", 6, W_LPURPLE, "Helvetica-Bold")
    wire(c, [(cx + 30, cy + 5), (cx + 60, cy + 5)], W_LPURPLE, 2)
    # R1 (1k) — horizontal resistor
    filled_rrect(c, cx + 60, cy, 40, 10, 2, fill=HexColor("#884400"), stroke=HexColor("#553300"), lw=1)
    label(c, cx + 80, cy + 2, "1k", 5, white, align="center")
    # Junction
    wire(c, [(cx + 100, cy + 5), (cx + 130, cy + 5)], W_LPURPLE, 2)
    wire_dot(c, cx + 130, cy + 5, W_LPURPLE, 3)
    # To GPIO26
    wire(c, [(cx + 130, cy + 5), (cx + 200, cy + 5)], W_LPURPLE, 2)
    label(c, cx + 210, cy + 2, "-> GPIO26", 6, W_LPURPLE)
    # R2 (2k) — vertical to GND
    wire(c, [(cx + 130, cy + 5), (cx + 130, cy - 15)], W_LPURPLE, 1.5)
    filled_rrect(c, cx + 125, cy - 30, 10, 15, 2, fill=HexColor("#884400"), stroke=HexColor("#553300"), lw=1)
    label(c, cx + 130, cy - 34, "2k", 5, white, align="center")
    wire(c, [(cx + 130, cy - 30), (cx + 130, cy - 40)], W_BLACK, 1.5)
    label(c, cx + 140, cy - 40, "GND", 5, W_BLACK)
    # Result
    label(c, cx + 200, cy - 10, "5V x 2k/(1k+2k) = 3.3V", 6, W_YELLOW)
    label(c, cx + 200, cy - 22, "Safe for Pi 5 GPIO input", 5, W_GREEN)


# ═══════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════

def main():
    c = canvas.Canvas(OUT, pagesize=landscape(LETTER))
    c.setTitle("Escort Bot — Visual Wiring Diagram")
    c.setAuthor("Elktron Hackathon")

    page1(c); c.showPage()
    page2(c); c.showPage()
    page3(c); c.showPage()

    c.save()
    print(f"PDF saved: {OUT}")
    print(f"  3 pages: System Diagram, GPIO Pinout, Power Distribution + Voltage Divider")

if __name__ == "__main__":
    main()
