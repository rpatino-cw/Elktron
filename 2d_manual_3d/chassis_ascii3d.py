#!/usr/bin/env python3
"""ASCII 3D chassis preview — spinning wireframe with adjustable camera pitch."""
import math, time, sys, os, select, termios, tty

# ─── Chassis components (mm) — from Stage 3 CORRECTED blueprint ──
# [x, y, z, w, d, h, label]  Origin: front-left-bottom. X=right, Y=back, Z=up.
#
# ┌─────────────────────────────────────────────────────────────────┐
# │ COORDINATE MAPPING (applied systematically to every component) │
# │                                                                 │
# │  Blueprint (Stage 3)          Python (Stage 4)                  │
# │  X = length (front→rear)  →  Y = length (back)                 │
# │  Y = width  (left→right)  →  X = width  (right)                │
# │  Z = height (bottom→up)   →  Z = height (up)                   │
# │  W = length extent        →  D = depth  (back)                 │
# │  D = width  extent        →  W = width  (right)                │
# │  H = height extent        →  H = height (up)                   │
# │                                                                 │
# │  py.x = bp.Y    py.y = bp.X    py.z = bp.Z                    │
# │  py.w = bp.D    py.d = bp.W    py.h = bp.H                    │
# └─────────────────────────────────────────────────────────────────┘
#
# Body: 260mm (length) × 130mm (width) × 3mm (thick)
# Standoff height: 25mm. Top plate at Z=25.
# Real dimensions: TT motor 70×22×19mm, wheel 65mm dia × 27mm wide.
#
PARTS = [
    # ── Plates ──────────────────────────────────────────────
    # bp: x=0, y=0, z=0, w=260, d=130, h=3
    (0,   0,   0,  130, 260, 3,  'BOTTOM PLATE'),
    # bp: x=5, y=0, z=25, w=154, d=130, h=3
    (0,   5,  25,  130, 154, 3,  'TOP PLATE'),
    # bp: x=-50, y=-10, z=0, w=50, d=150, h=3  (realistic wing, not trace bounding box)
    (-10, -50, 0, 150, 50, 3,  'HEAD'),
    # bp: x=197, y=0, z=0, w=63, d=130, h=3  (CORRECTED from trace)
    (0,  197,  0,  130,  63, 3,  'REAR'),

    # ── Standoffs (M3×25mm brass, 6×6mm) ──────────────────
    # Side view gives X positions: 16, 81, 138, 175mm
    # Real chassis has L/R pairs at y≈18 and y≈108 (inside body edges)
    # bp: x=16,  y=18,  z=0  (front-left)
    (18,  16,  0,   6,   6, 25, ''),
    # bp: x=16,  y=108, z=0  (front-right)
    (108, 16,  0,   6,   6, 25, ''),
    # bp: x=81,  y=18,  z=0  (center-left)
    (18,  81,  0,   6,   6, 25, ''),
    # bp: x=81,  y=108, z=0  (center-right)
    (108, 81,  0,   6,   6, 25, 'STANDOFF'),
    # bp: x=138, y=18,  z=0  (mid-rear-left)
    (18, 138,  0,   6,   6, 25, ''),
    # bp: x=138, y=108, z=0  (mid-rear-right)
    (108,138,  0,   6,   6, 25, ''),
    # bp: x=175, y=18,  z=0  (rear-left)
    (18, 175,  0,   6,   6, 25, ''),
    # bp: x=175, y=108, z=0  (rear-right)
    (108,175,  0,   6,   6, 25, ''),

    # ── Upper posts (6×6×17mm, z=28 = standoff 25 + plate 3) ─
    # bp: x=81, y=18, z=28  (center-left)
    (18,  81, 28,   6,   6, 17, ''),
    # bp: x=158, y=108, z=28  (rear-right)
    (108,158, 28,   6,   6, 17, 'POST'),

    # ── Motors (TT gear motor, 70×22×19mm) ─────────────────
    # CORRECTED from trace blobs (were 223×23×17)
    # bp: x=32,  y=-2,  z=0, w=70, d=22, h=19  (front-left)
    (-2,  32,  0,  22,  70, 19, 'MTR'),
    # bp: x=32,  y=110, z=0  (front-right)
    (110, 32,  0,  22,  70, 19, 'MTR'),
    # bp: x=162, y=-2,  z=0  (rear-left)
    (-2, 162,  0,  22,  70, 19, ''),
    # bp: x=162, y=110, z=0  (rear-right)
    (110,162,  0,  22,  70, 19, ''),

    # ── Wheels (65mm dia × 27mm wide) ──────────────────────
    # CORRECTED from trace blobs (were 224×57×26)
    # bp: x=35,  y=-14, z=-20, w=65, d=27, h=65  (front-left)
    (-14, 35, -20,  27,  65, 65, 'WHL'),
    # bp: x=35,  y=117, z=-20  (front-right)
    (117, 35, -20,  27,  65, 65, 'WHL'),
    # bp: x=165, y=-14, z=-20  (rear-left)
    (-14,165, -20,  27,  65, 65, ''),
    # bp: x=165, y=117, z=-20  (rear-right)
    (117,165, -20,  27,  65, 65, ''),

    # ── Battery box ────────────────────────────────────────
    # bp: x=265, y=10, z=3, w=33, d=110, h=32
    (10, 265,  3,  110,  33, 32, 'BATT'),

    # ── Sensor bar (IR) ───────────────────────────────────
    # bp: x=-69, y=22, z=12, w=87, d=5, h=5
    (22, -69, 12,   5,  87,  5, 'SENSOR'),

    # ── Switch enclosure ──────────────────────────────────
    # bp: x=173, y=0, z=1, w=85, d=130, h=40
    (0,  173,  1,  130,  85, 40, 'SWITCH'),
]

# Auto-compute center and scale from bounding box
_xmin = min(p[0] for p in PARTS)
_xmax = max(p[0]+p[3] for p in PARTS)
_ymin = min(p[1] for p in PARTS)
_ymax = max(p[1]+p[4] for p in PARTS)
_zmin = min(p[2] for p in PARTS)
_zmax = max(p[2]+p[5] for p in PARTS)
CX = (_xmin + _xmax) / 2
CY = (_ymin + _ymax) / 2
CZ = (_zmin + _zmax) / 2
_DIAG = math.sqrt((_xmax - _xmin)**2 + (_ymax - _ymin)**2)

def get_term_size():
    cols, rows = os.get_terminal_size()
    return cols, rows - 6  # reserve 6 lines for header + footer

EDGE_MAP = [
    (0,1),(1,2),(2,3),(3,0),  # bottom face
    (4,5),(5,6),(6,7),(7,4),  # top face
    (0,4),(1,5),(2,6),(3,7),  # verticals
]

PRESETS = {
    '1': ('Bird Eye',  0.52),
    '2': ('Low Angle', 0.17),
    '3': ('Eye Level', 0.0),
    '4': ('Under',    -0.17),
}

# Box-drawing chars by component type
def pick_chars(label):
    if 'PLATE' in label or 'SWITCH' in label or 'HEAD' in label or 'REAR' in label:
        return '═', '║', '╬'
    if 'STANDOFF' in label or 'POST' in label or label == '':
        return '│', '│', '+'
    if 'WHL' in label:
        return '●', '●', '●'
    if 'MTR' in label:
        return '█', '█', '█'
    if 'BATT' in label:
        return '▓', '▓', '▓'
    if 'SENSOR' in label:
        return '░', '░', '░'
    return '─', '│', '+'

def project(x, y, z, yaw, pitch, w, h):
    x -= CX; y -= CY; z -= CZ
    # Yaw rotation (spin around Z axis)
    cy, sy_ = math.cos(yaw), math.sin(yaw)
    rx = x*cy - y*sy_
    ry = x*sy_ + y*cy
    rz = z
    # Pitch rotation (tilt around X axis)
    cp, sp = math.cos(pitch), math.sin(pitch)
    ry2 = ry*cp - rz*sp
    rz2 = ry*sp + rz*cp
    # Project to 2D — fill terminal
    # Terminal chars are ~2:1 height:width ratio
    # Chassis max diagonal ~350mm, so scale to fit width
    sx = rx        # horizontal in mm
    sy = -rz2      # vertical in mm (screen Y down)
    depth = ry2
    # Scale: fill ~72% of terminal width with bounding box diagonal
    s = (w * 0.72) / max(_DIAG, 200)
    bx = int(w/2 + sx * s)
    # Char aspect correction: each row is ~2x a column in pixels
    by = int(h/2 + sy * s * 0.45)
    return bx, by, depth

def bresenham(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1-x0), abs(y1-y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx: err += dx; y0 += sy
    return pts

def get_key():
    """Non-blocking key read. Returns key string or None."""
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(2)
            if ch2 == '[A': return 'UP'
            if ch2 == '[B': return 'DOWN'
            return None
        return ch
    return None

def render_frame(yaw, pitch):
    tw, th = get_term_size()
    buf = [[' ']*tw for _ in range(th)]
    zb = [[-9999]*tw for _ in range(th)]

    def plot(bx, by, d, ch):
        if 0 <= bx < tw and 0 <= by < th and d >= zb[by][bx]:
            zb[by][bx] = d
            buf[by][bx] = ch

    # Sort parts back-to-front
    def sort_key(p):
        _, _, d = project(p[0]+p[3]/2, p[1]+p[4]/2, p[2]+p[5]/2, yaw, pitch, tw, th)
        return d

    for part in sorted(PARTS, key=sort_key):
        x,y,z,w,d,h,label = part
        hch, vch, cch = pick_chars(label)

        corners = [
            (x,y,z), (x+w,y,z), (x+w,y+d,z), (x,y+d,z),
            (x,y,z+h), (x+w,y,z+h), (x+w,y+d,z+h), (x,y+d,z+h),
        ]
        proj = [project(*c, yaw, pitch, tw, th) for c in corners]

        for a,b in EDGE_MAP:
            pa, pb = proj[a], proj[b]
            avg_d = (pa[2] + pb[2]) / 2
            is_vert = (a < 4 and b >= 4) or (a >= 4 and b < 4)
            ch = vch if is_vert else hch
            for px, py in bresenham(pa[0], pa[1], pb[0], pb[1]):
                plot(px, py, avg_d, ch)

        for p in proj:
            plot(p[0], p[1], p[2]+0.1, cch)

        # Label above top center
        if label:
            cx, cy, cd = project(x+w/2, y+d/2, z+h+5, yaw, pitch, tw, th)
            sx = cx - len(label)//2
            for i, ch in enumerate(label):
                plot(sx+i, cy, 9999, ch)

    # Ground dots — auto-extend to bounding box
    for gy in range(int(_ymin)-40, int(_ymax)+40, 20):
        for gx in range(int(_xmin)-20, int(_xmax)+20, 20):
            bx, by, d = project(gx, gy, -2, yaw, pitch, tw, th)
            plot(bx, by, -9999, '·')

    lines = []
    for row in buf:
        lines.append(''.join(row).rstrip())
    return '\n'.join(lines)


def main():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        pitch = 0.52  # start at bird's eye
        pitch_step = 0.05
        frame_num = 0
        frames_per_rev = 48
        delay = 0.15
        preset_name = 'Bird Eye'

        while True:
            yaw = (frame_num / frames_per_rev) * 2 * math.pi

            # Non-blocking key check
            key = get_key()
            if key == 'UP':
                pitch = min(1.3, pitch + pitch_step)
                preset_name = ''
            elif key == 'DOWN':
                pitch = max(-0.5, pitch - pitch_step)
                preset_name = ''
            elif key in PRESETS:
                preset_name, pitch = PRESETS[key]
            elif key == 'q':
                break

            # Find current preset name if matching
            if not preset_name:
                for k, (name, val) in PRESETS.items():
                    if abs(pitch - val) < 0.01:
                        preset_name = name
                        break

            pitch_deg = int(math.degrees(pitch))
            label = f'{preset_name} {pitch_deg}°' if preset_name else f'{pitch_deg}°'

            frame = render_frame(yaw, pitch)

            sys.stdout.write('\033[2J\033[H')
            sys.stdout.write(f'\033[38;2;201;148;58m  LK-COKOINO 4WD Chassis — ASCII 3D Preview\033[0m\n')
            sys.stdout.write(f'\033[38;2;120;116;114m  Pitch: {label}  |  \033[38;2;80;80;80m↑↓\033[38;2;120;116;114m adjust  \033[38;2;80;80;80m1\033[38;2;120;116;114m bird  \033[38;2;80;80;80m2\033[38;2;120;116;114m low  \033[38;2;80;80;80m3\033[38;2;120;116;114m eye  \033[38;2;80;80;80m4\033[38;2;120;116;114m under  \033[38;2;80;80;80mq\033[38;2;120;116;114m quit\033[0m\n\n')
            sys.stdout.write(frame)
            sys.stdout.write(f'\n\n\033[38;2;120;116;114m  260x130mm · arrow front · 4 TT motors + wheels · battery · sensor bar\033[0m')
            sys.stdout.flush()

            frame_num += 1
            time.sleep(delay)

    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        sys.stdout.write('\033[0m\n')

if __name__ == '__main__':
    main()
