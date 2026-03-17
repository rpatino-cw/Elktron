#!/usr/bin/env python3
"""
Stage 2.8 — Blueprint Sheet Generator (MERGED ASSEMBLY VIEW)
Generates a classic engineering blueprint PDF showing the LK-COKOINO 4WD chassis
as ONE unified assembled isometric drawing — all 3 traced views merged into a
single coherent chassis component.

NOT separate viewports. NOT a comparison sheet. One assembled chassis.

Usage:
  python3 generate_blueprint.py

Output:
  chassis_blueprint.pdf (in the same directory)
"""

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
import math
import os

# ─── Blueprint Colors ────────────────────────────────────
BG = Color(0.067, 0.173, 0.294)        # Deep blueprint blue #112C4B
GRID_MAJOR = Color(0.12, 0.28, 0.44)
GRID_MINOR = Color(0.09, 0.22, 0.36)
LINE_COLOR = Color(0.75, 0.88, 1.0)    # Cyan-white outlines
DIM_COLOR = Color(0.5, 0.65, 0.85)
TITLE_COLOR = Color(0.85, 0.92, 1.0)
LABEL_COLOR = Color(0.6, 0.75, 0.9)

# Component fill colors (semi-transparent for depth)
PLATE_FILL = Color(0.5, 0.7, 0.85, 0.08)
PLATE_STROKE = Color(0.65, 0.82, 1.0)
STANDOFF_FILL = Color(0.78, 0.58, 0.23, 0.15)
STANDOFF_STROKE = Color(0.78, 0.58, 0.23)
MOTOR_FILL = Color(0.85, 0.78, 0.2, 0.12)
MOTOR_STROKE = Color(0.85, 0.78, 0.2)
WHEEL_FILL = Color(0.3, 0.3, 0.35, 0.15)
WHEEL_STROKE = Color(0.45, 0.5, 0.6)
BATTERY_FILL = Color(0.3, 0.35, 0.4, 0.1)
BATTERY_STROKE = Color(0.45, 0.55, 0.65)
SENSOR_FILL = Color(0.2, 0.55, 0.3, 0.12)
SENSOR_STROKE = Color(0.3, 0.7, 0.4)
POST_FILL = Color(0.6, 0.6, 0.65, 0.1)
POST_STROKE = Color(0.7, 0.72, 0.78)

# ─── Trace Data (preserved for reference) ──────────────────

SIDE_LINES = [
    {"line":1,  "p1":(1000,3218), "p2":(3631,3203), "bent":False},
    {"line":2,  "p1":(1047,2738), "p2":(2607,2730), "bent":False},
    {"line":3,  "p1":(298,3014),  "p2":(1173,3006), "bent":False},
    {"line":4,  "p1":(3607,2509), "p2":(3615,3195), "bent":False},
    {"line":5,  "p1":(2757,2517), "p2":(3615,2517), "bent":False},
    {"line":6,  "p1":(2788,3203), "p2":(2764,2517), "bent":False},
    {"line":7,  "p1":(1819,2761), "p2":(1827,3195), "bent":False},
    {"line":8,  "p1":(2591,2446), "p2":(2615,2722), "bent":False},
    {"line":9,  "p1":(2394,2738), "p2":(2402,3211), "bent":False},
    {"line":10, "p1":(1803,2478), "p2":(1827,2730), "bent":False},
    {"line":11, "p1":(1157,2990), "p2":(1165,3266), "bent":False},
    {"line":12, "p1":(3584,2572), "p2":(3915,2580), "bent":False},
    {"line":13, "p1":(3915,2572), "p2":(3923,3124), "bent":False},
    {"line":14, "p1":(3915,3140), "p2":(3639,3132), "bent":False},
]

FRONT_LINES = [
    {"line":1,  "p1":(952,3061),  "p2":(2008,3077), "bent":False},
    {"line":2,  "p1":(2008,3077), "p2":(2678,3084), "bent":True, "cp":(2339,3069)},
    {"line":3,  "p1":(2670,3084), "p2":(3781,3100), "bent":False},
    {"line":4,  "p1":(1898,3281), "p2":(2796,3289), "bent":False},
    {"line":5,  "p1":(2118,3274), "p2":(2118,3108), "bent":False},
    {"line":6,  "p1":(2599,3084), "p2":(2599,3297), "bent":False},
    {"line":7,  "p1":(1890,2738), "p2":(2835,2738), "bent":False},
    {"line":8,  "p1":(2189,2738), "p2":(2189,3053), "bent":False},
    {"line":9,  "p1":(2599,2730), "p2":(2591,3069), "bent":False},
    {"line":10, "p1":(2047,2478), "p2":(2047,2722), "bent":False},
    {"line":11, "p1":(2717,2486), "p2":(2717,2738), "bent":False},
]

TOP_LINES = [
    {"line":1,  "p1":(517,1114), "p2":(567,875),   "bent":True, "cp":(550,960)},
    {"line":2,  "p1":(909,1108), "p2":(916,1360),  "bent":True, "cp":(913,1286)},
    {"line":3,  "p1":(894,1399), "p2":(541,1401),  "bent":False},
    {"line":4,  "p1":(522,1364), "p2":(517,1114),  "bent":True, "cp":(519,1277)},
    {"line":5,  "p1":(848,866),  "p2":(909,1108),  "bent":False},
    {"line":6,  "p1":(515,707),  "p2":(517,803),   "bent":False},
    {"line":7,  "p1":(896,701),  "p2":(898,805),   "bent":False},
    {"line":8,  "p1":(848,699),  "p2":(842,511),   "bent":False},
    {"line":9,  "p1":(565,701),  "p2":(563,518),   "bent":False},
    {"line":10, "p1":(844,509),  "p2":(985,429),   "bent":False},
    {"line":11, "p1":(413,437),  "p2":(563,522),   "bent":False},
    {"line":12, "p1":(363,381),  "p2":(626,316),   "bent":False},
    {"line":13, "p1":(759,311),  "p2":(1027,363),  "bent":False},
    {"line":14, "p1":(524,1364), "p2":(541,1401),  "bent":True, "cp":(517,1395)},
    {"line":15, "p1":(894,1401), "p2":(918,1360),  "bent":True, "cp":(916,1399)},
    {"line":16, "p1":(517,805),  "p2":(567,877),   "bent":True, "cp":(589,790)},
    {"line":17, "p1":(896,805),  "p2":(846,866),   "bent":True, "cp":(828,790)},
    {"line":18, "p1":(848,701),  "p2":(896,701),   "bent":False},
    {"line":19, "p1":(513,707),  "p2":(565,703),   "bent":False},
    {"line":20, "p1":(415,440),  "p2":(361,383),   "bent":True, "cp":(348,448)},
    {"line":21, "p1":(985,433),  "p2":(1031,363),  "bent":True, "cp":(1059,422)},
    {"line":22, "p1":(626,313),  "p2":(761,313),   "bent":True, "cp":(698,357)},
]

# ─── Physical Dimensions & Scale ────────────────────────
# Known: 260mm long, 130mm wide, ~85mm tall

_side_l1_px = math.dist((1000, 3218), (3631, 3203))
SIDE_MM_PER_PX = 260.0 / _side_l1_px

_front_head_px = math.dist((952, 3061), (3781, 3100))
FRONT_MM_PER_PX = 130.0 / _front_head_px

_top_all_ys = []
for _l in TOP_LINES:
    _top_all_ys.extend([_l["p1"][1], _l["p2"][1]])
    if _l.get("cp"):
        _top_all_ys.append(_l["cp"][1])
_top_y_span = max(_top_all_ys) - min(_top_all_ys)
TOP_MM_PER_PX = 260.0 / _top_y_span


# ═══════════════════════════════════════════════════════════
# COMPONENT DEFINITIONS — 3D bounding boxes in mm
# All derived from trace pixel data → mm conversion
# Origin: bottom-left-front corner of bottom plate
# X = length (0→260, front→rear)
# Y = height (0 = bottom plate surface, up is positive)
# Z = width (-65→+65, centered)
# ═══════════════════════════════════════════════════════════

COMPONENTS = [
    # ─── Plates ───
    {"name": "Bottom Plate", "type": "plate",
     "x": 0, "y": 0, "z": -65, "w": 260, "h": 3, "d": 130,
     "fill": PLATE_FILL, "stroke": PLATE_STROKE, "lw": 1.0},

    {"name": "Top Plate", "type": "plate",
     "x": 5, "y": 43, "z": -50, "w": 154, "h": 3, "d": 100,
     "fill": PLATE_FILL, "stroke": PLATE_STROKE, "lw": 1.0},

    {"name": "Head Plate", "type": "plate",
     "x": 0, "y": 3, "z": -65, "w": 3, "h": 35, "d": 130,
     "fill": PLATE_FILL, "stroke": PLATE_STROKE, "lw": 0.8},

    # ─── Standoffs (6) ───
    {"name": "Standoff FL", "type": "standoff",
     "x": 13, "y": 3, "z": -42, "w": 6, "h": 40, "d": 6,
     "fill": STANDOFF_FILL, "stroke": STANDOFF_STROKE, "lw": 0.7},
    {"name": "Standoff FR", "type": "standoff",
     "x": 13, "y": 3, "z": 36, "w": 6, "h": 40, "d": 6,
     "fill": STANDOFF_FILL, "stroke": STANDOFF_STROKE, "lw": 0.7},
    {"name": "Standoff ML", "type": "standoff",
     "x": 78, "y": 3, "z": -37, "w": 6, "h": 40, "d": 6,
     "fill": STANDOFF_FILL, "stroke": STANDOFF_STROKE, "lw": 0.7},
    {"name": "Standoff MR", "type": "standoff",
     "x": 134, "y": 3, "z": 31, "w": 6, "h": 40, "d": 6,
     "fill": STANDOFF_FILL, "stroke": STANDOFF_STROKE, "lw": 0.7},
    {"name": "Standoff RL", "type": "standoff",
     "x": 173, "y": 3, "z": -42, "w": 6, "h": 40, "d": 6,
     "fill": STANDOFF_FILL, "stroke": STANDOFF_STROKE, "lw": 0.7},
    {"name": "Standoff RR", "type": "standoff",
     "x": 173, "y": 3, "z": 36, "w": 6, "h": 40, "d": 6,
     "fill": STANDOFF_FILL, "stroke": STANDOFF_STROKE, "lw": 0.7},

    # ─── Upper Posts (2) ───
    {"name": "Post Front", "type": "post",
     "x": 76, "y": 46, "z": -32, "w": 5, "h": 25, "d": 5,
     "fill": POST_FILL, "stroke": POST_STROKE, "lw": 0.6},
    {"name": "Post Rear", "type": "post",
     "x": 154, "y": 46, "z": 27, "w": 5, "h": 25, "d": 5,
     "fill": POST_FILL, "stroke": POST_STROKE, "lw": 0.6},

    # ─── Motors (2) ───
    {"name": "Motor Front", "type": "motor",
     "x": 15, "y": 5, "z": -14, "w": 50, "h": 30, "d": 28,
     "fill": MOTOR_FILL, "stroke": MOTOR_STROKE, "lw": 0.8},
    {"name": "Motor Rear", "type": "motor",
     "x": 115, "y": 5, "z": -14, "w": 50, "h": 30, "d": 28,
     "fill": MOTOR_FILL, "stroke": MOTOR_STROKE, "lw": 0.8},

    # ─── Wheels (4) ───
    {"name": "Wheel FL", "type": "wheel",
     "x": 14, "y": -18, "z": -91, "w": 26, "h": 66, "d": 26,
     "fill": WHEEL_FILL, "stroke": WHEEL_STROKE, "lw": 0.9},
    {"name": "Wheel FR", "type": "wheel",
     "x": 14, "y": -18, "z": 65, "w": 26, "h": 66, "d": 26,
     "fill": WHEEL_FILL, "stroke": WHEEL_STROKE, "lw": 0.9},
    {"name": "Wheel RL", "type": "wheel",
     "x": 174, "y": -18, "z": -91, "w": 26, "h": 66, "d": 26,
     "fill": WHEEL_FILL, "stroke": WHEEL_STROKE, "lw": 0.9},
    {"name": "Wheel RR", "type": "wheel",
     "x": 174, "y": -18, "z": 65, "w": 26, "h": 66, "d": 26,
     "fill": WHEEL_FILL, "stroke": WHEEL_STROKE, "lw": 0.9},

    # ─── Battery Box ───
    {"name": "Battery Box", "type": "battery",
     "x": 258, "y": 4, "z": -25, "w": 33, "h": 44, "d": 50,
     "fill": BATTERY_FILL, "stroke": BATTERY_STROKE, "lw": 0.7},

    # ─── Sensor Bar ───
    {"name": "Sensor Bar", "type": "sensor",
     "x": -83, "y": -2, "z": -6, "w": 86, "h": 5, "d": 12,
     "fill": SENSOR_FILL, "stroke": SENSOR_STROKE, "lw": 0.7},

    # ─── Switch Enclosure ───
    {"name": "Switch", "type": "box",
     "x": 215, "y": 3, "z": 33, "w": 30, "h": 20, "d": 15,
     "fill": BATTERY_FILL, "stroke": BATTERY_STROKE, "lw": 0.6},
]


# ═══════════════════════════════════════════════════════════
# ISOMETRIC PROJECTION
# ═══════════════════════════════════════════════════════════

# Isometric angles
ISO_ANGLE = math.radians(30)
COS30 = math.cos(ISO_ANGLE)
SIN30 = math.sin(ISO_ANGLE)


def iso_project(x, y, z):
    """Project 3D point (x, y, z) to 2D isometric (screen_x, screen_y)."""
    sx = (x - z) * COS30
    sy = y + (x + z) * SIN30
    return sx, sy


def iso_box_faces(x, y, z, w, h, d):
    """
    Get the 3 visible isometric faces of a box.
    Returns (top_face, right_face, left_face) as lists of (sx, sy) points.
    Box corner is at (x, y, z), dimensions (w=X, h=Y, d=Z).
    """
    # 8 vertices
    v = [
        (x,     y,     z),      # 0: bottom-front-left
        (x + w, y,     z),      # 1: bottom-front-right
        (x + w, y,     z + d),  # 2: bottom-back-right
        (x,     y,     z + d),  # 3: bottom-back-left
        (x,     y + h, z),      # 4: top-front-left
        (x + w, y + h, z),      # 5: top-front-right
        (x + w, y + h, z + d),  # 6: top-back-right
        (x,     y + h, z + d),  # 7: top-back-left
    ]
    proj = [iso_project(*v_i) for v_i in v]

    # Visible faces in isometric (camera from front-right-top):
    top_face = [proj[4], proj[5], proj[6], proj[7]]    # top
    right_face = [proj[1], proj[2], proj[6], proj[5]]  # right side
    left_face = [proj[0], proj[4], proj[7], proj[3]]   # left side
    front_face = [proj[0], proj[1], proj[5], proj[4]]  # front

    return top_face, right_face, left_face, front_face


def draw_iso_box(c, x, y, z, w, h, d, fill_color, stroke_color, line_width,
                 scale, offset_x, offset_y):
    """Draw an isometric box on the canvas."""
    top, right, left, front = iso_box_faces(x, y, z, w, h, d)

    def to_page(pts):
        return [(px * scale + offset_x, py * scale + offset_y) for px, py in pts]

    # Slightly darker variants for depth
    darker = Color(
        max(0, stroke_color.red * 0.7),
        max(0, stroke_color.green * 0.7),
        max(0, stroke_color.blue * 0.7),
        getattr(stroke_color, 'alpha', 1.0)
    )
    lightest = Color(
        min(1, stroke_color.red * 1.1),
        min(1, stroke_color.green * 1.1),
        min(1, stroke_color.blue * 1.1),
        getattr(stroke_color, 'alpha', 1.0)
    )

    # Draw faces back-to-front for correct occlusion
    for face_pts, face_fill, face_stroke in [
        (left, Color(fill_color.red * 0.8, fill_color.green * 0.8,
                     fill_color.blue * 0.8, fill_color.alpha), darker),
        (right, Color(fill_color.red * 0.9, fill_color.green * 0.9,
                      fill_color.blue * 0.9, fill_color.alpha), stroke_color),
        (front, fill_color, stroke_color),
        (top, Color(min(1, fill_color.red * 1.2), min(1, fill_color.green * 1.2),
                    min(1, fill_color.blue * 1.2), fill_color.alpha), lightest),
    ]:
        page_pts = to_page(face_pts)
        c.setFillColor(face_fill)
        c.setStrokeColor(face_stroke)
        c.setLineWidth(line_width)
        c.setLineJoin(1)  # Round join
        p = c.beginPath()
        p.moveTo(*page_pts[0])
        for pt in page_pts[1:]:
            p.lineTo(*pt)
        p.close()
        c.drawPath(p, stroke=1, fill=1)


def draw_iso_label(c, comp, scale, offset_x, offset_y):
    """Draw a label for a component at its top-center."""
    cx = comp["x"] + comp["w"] / 2
    cy = comp["y"] + comp["h"] + 3  # slightly above top
    cz = comp["z"] + comp["d"] / 2
    sx, sy = iso_project(cx, cy, cz)
    px = sx * scale + offset_x
    py = sy * scale + offset_y

    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica", 4.5)
    c.drawCentredString(px, py + 3, comp["name"])


def draw_dimension_line(c, p1_3d, p2_3d, label, scale, ox, oy,
                        offset_dir=(0, 8), color=DIM_COLOR):
    """Draw a dimension line between two 3D points."""
    sx1, sy1 = iso_project(*p1_3d)
    sx2, sy2 = iso_project(*p2_3d)
    x1 = sx1 * scale + ox + offset_dir[0]
    y1 = sy1 * scale + oy + offset_dir[1]
    x2 = sx2 * scale + ox + offset_dir[0]
    y2 = sy2 * scale + oy + offset_dir[1]

    c.setStrokeColor(color)
    c.setLineWidth(0.4)
    c.setDash(1.5, 1.5)
    c.line(x1, y1, x2, y2)
    c.setDash()

    # Arrowheads
    c.setFillColor(color)
    c.circle(x1, y1, 1.2, stroke=0, fill=1)
    c.circle(x2, y2, 1.2, stroke=0, fill=1)

    # Label at midpoint
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    c.setFont("Helvetica", 5)
    c.drawCentredString(mx, my + 4, label)


def draw_grid(c, x, y, w, h, spacing_major=30, spacing_minor=7):
    """Draw blueprint grid."""
    c.setStrokeColor(GRID_MINOR)
    c.setLineWidth(0.15)
    for gx in range(0, int(w) + 1, int(spacing_minor)):
        c.line(x + gx, y, x + gx, y + h)
    for gy in range(0, int(h) + 1, int(spacing_minor)):
        c.line(x, y + gy, x + w, y + gy)

    c.setStrokeColor(GRID_MAJOR)
    c.setLineWidth(0.3)
    for gx in range(0, int(w) + 1, int(spacing_major)):
        c.line(x + gx, y, x + gx, y + h)
    for gy in range(0, int(h) + 1, int(spacing_major)):
        c.line(x, y + gy, x + w, y + gy)


def draw_scale_bar(c, x, y, scale):
    """Draw a 50mm scale bar."""
    bar_mm = 50
    # In iso projection, 50mm along X axis
    sx1, sy1 = iso_project(0, 0, 0)
    sx2, sy2 = iso_project(bar_mm, 0, 0)
    bar_pts = (sx2 - sx1) * scale

    c.setStrokeColor(TITLE_COLOR)
    c.setLineWidth(0.8)
    c.line(x, y, x + bar_pts, y)
    c.line(x, y - 3, x, y + 3)
    c.line(x + bar_pts, y - 3, x + bar_pts, y + 3)

    c.setFillColor(TITLE_COLOR)
    c.setFont("Helvetica", 6)
    c.drawCentredString(x + bar_pts / 2, y + 5, f"{bar_mm}mm (along X)")


def draw_title_block(c, page_w, page_h, scale):
    """Engineering title block — bottom-right."""
    bw = 210
    bh = 72
    bx = page_w - bw - 20
    by = 20

    c.setFillColor(Color(0.05, 0.12, 0.22))
    c.setStrokeColor(Color(0.3, 0.5, 0.7))
    c.setLineWidth(0.8)
    c.rect(bx, by, bw, bh, stroke=1, fill=1)

    c.setStrokeColor(Color(0.2, 0.38, 0.55))
    c.setLineWidth(0.4)
    c.line(bx, by + 25, bx + bw, by + 25)
    c.line(bx, by + 48, bx + bw, by + 48)
    c.line(bx + bw / 2, by, bx + bw / 2, by + 25)

    c.setFillColor(TITLE_COLOR)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(bx + 8, by + 55, "LK-COKOINO 4WD CHASSIS")

    c.setFont("Helvetica", 7)
    c.setFillColor(LABEL_COLOR)
    c.drawString(bx + 8, by + 38, "Elktron Hackathon 2026")
    c.drawString(bx + 8, by + 29, "MERGED ASSEMBLY — All views unified")

    c.setFont("Helvetica", 6)
    c.setFillColor(Color(0.45, 0.6, 0.8))
    c.drawString(bx + 6, by + 12, "PROJECTION")
    c.drawString(bx + 6, by + 4, "ISOMETRIC")
    c.drawString(bx + bw / 2 + 6, by + 12, "VIEWS MERGED")
    c.drawString(bx + bw / 2 + 6, by + 4, "SIDE + FRONT + TOP")

    c.setStrokeColor(Color(0.35, 0.55, 0.75))
    c.setLineWidth(1.2)
    c.rect(bx - 2, by - 2, bw + 4, bh + 4, stroke=1, fill=0)


def draw_page_border(c, page_w, page_h):
    """Outer border and corner marks."""
    margin = 15
    c.setStrokeColor(Color(0.25, 0.45, 0.65))
    c.setLineWidth(1.0)
    c.rect(margin, margin, page_w - 2 * margin, page_h - 2 * margin,
           stroke=1, fill=0)
    c.setLineWidth(0.3)
    c.rect(margin + 3, margin + 3,
           page_w - 2 * margin - 6, page_h - 2 * margin - 6,
           stroke=1, fill=0)


def draw_component_legend(c, page_w, page_h):
    """Component legend in top-right corner."""
    lx = page_w - 170
    ly = page_h - 55
    lw = 150
    lh = 0

    legend_items = [
        (PLATE_STROKE, "Acrylic plates (3)"),
        (STANDOFF_STROKE, "Brass standoffs (6)"),
        (POST_STROKE, "Upper posts (2)"),
        (MOTOR_STROKE, "DC motors (2)"),
        (WHEEL_STROKE, "Wheels (4)"),
        (BATTERY_STROKE, "Battery + switch"),
        (SENSOR_STROKE, "Sensor bar"),
    ]

    c.setFont("Helvetica", 5)
    for i, (color, label) in enumerate(legend_items):
        y = ly - i * 10
        c.setFillColor(color)
        c.circle(lx + 4, y + 2, 2, stroke=0, fill=1)
        c.setFillColor(LABEL_COLOR)
        c.drawString(lx + 10, y, label)


def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "chassis_blueprint.pdf")

    page_w, page_h = landscape(letter)  # 792 x 612 pts
    c = canvas.Canvas(output_path, pagesize=landscape(letter))

    # ─── Background ──────────────────────────────────────
    c.setFillColor(BG)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    # ─── Page grid ───────────────────────────────────────
    draw_grid(c, 0, 0, page_w, page_h, spacing_major=36, spacing_minor=9)

    # ─── Page border ─────────────────────────────────────
    draw_page_border(c, page_w, page_h)

    # ─── Title ───────────────────────────────────────────
    c.setFillColor(TITLE_COLOR)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w / 2, page_h - 35,
                        "CHASSIS ASSEMBLY — ISOMETRIC VIEW")

    c.setFont("Helvetica", 8)
    c.setFillColor(LABEL_COLOR)
    c.drawCentredString(page_w / 2, page_h - 48,
                        "ALL VIEWS MERGED  |  47 TRACED LINES  |  "
                        "SIDE + FRONT + TOP  |  STAGE 2.8")

    # ─── Compute isometric bounds and scale ──────────────
    # Find bounding box of all projected component vertices
    all_sx = []
    all_sy = []
    for comp in COMPONENTS:
        for dx in [0, comp["w"]]:
            for dy in [0, comp["h"]]:
                for dz in [0, comp["d"]]:
                    sx, sy = iso_project(
                        comp["x"] + dx,
                        comp["y"] + dy,
                        comp["z"] + dz
                    )
                    all_sx.append(sx)
                    all_sy.append(sy)

    iso_w = max(all_sx) - min(all_sx)
    iso_h = max(all_sy) - min(all_sy)

    # Available drawing area
    margin = 45
    avail_w = page_w - 2 * margin - 180  # reserve space for legend
    avail_h = page_h - 80 - 40  # title space + bottom

    # Scale to fit
    scale = min(avail_w / iso_w, avail_h / iso_h) * 0.92

    # Center offset
    center_x = margin + (avail_w - iso_w * scale) / 2 - min(all_sx) * scale
    center_y = 50 + (avail_h - iso_h * scale) / 2 - min(all_sy) * scale

    print(f"Isometric bounds: {iso_w:.0f} x {iso_h:.0f} iso-units")
    print(f"Scale: {scale:.3f} pts/iso-unit")
    print(f"Offset: ({center_x:.0f}, {center_y:.0f})")

    # ─── Sort components by depth (back-to-front) ───────
    # Depth in isometric = x + z (higher = further back)
    def depth_key(comp):
        cx = comp["x"] + comp["w"] / 2
        cz = comp["z"] + comp["d"] / 2
        cy = comp["y"]
        return cx + cz - cy * 0.1  # slight Y bias
    sorted_comps = sorted(COMPONENTS, key=depth_key)

    # ─── Draw all components ─────────────────────────────
    for comp in sorted_comps:
        draw_iso_box(
            c,
            comp["x"], comp["y"], comp["z"],
            comp["w"], comp["h"], comp["d"],
            comp["fill"], comp["stroke"], comp["lw"],
            scale, center_x, center_y
        )

    # ─── Labels ──────────────────────────────────────────
    for comp in sorted_comps:
        draw_iso_label(c, comp, scale, center_x, center_y)

    # ─── Dimension lines ─────────────────────────────────
    # Length: 260mm along bottom plate
    draw_dimension_line(c,
                        (0, -12, -65), (260, -12, -65),
                        "260mm", scale, center_x, center_y)

    # Width: 130mm across front
    draw_dimension_line(c,
                        (-5, -12, -65), (-5, -12, 65),
                        "130mm", scale, center_x, center_y)

    # Height: bottom to top plate
    draw_dimension_line(c,
                        (-15, 0, -65), (-15, 46, -65),
                        "46mm", scale, center_x, center_y)

    # Full height with posts
    draw_dimension_line(c,
                        (-25, 0, -65), (-25, 71, -65),
                        "71mm", scale, center_x, center_y)

    # ─── Legend ───────────────────────────────────────────
    draw_component_legend(c, page_w, page_h)

    # ─── Title block ─────────────────────────────────────
    draw_title_block(c, page_w, page_h, scale)

    # ─── Scale bar ───────────────────────────────────────
    draw_scale_bar(c, margin + 10, 22, scale)

    # ─── Stats ───────────────────────────────────────────
    c.setFillColor(Color(0.4, 0.55, 0.75))
    c.setFont("Helvetica", 5.5)
    c.drawString(margin + 5, page_h - 60,
                 f"{len(COMPONENTS)} components  |  "
                 f"47 trace lines merged  |  "
                 f"3 views (14 side + 11 front + 22 top)")

    # ─── Save ────────────────────────────────────────────
    c.save()
    print(f"Blueprint saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
