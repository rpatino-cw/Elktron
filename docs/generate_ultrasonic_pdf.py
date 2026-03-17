#!/usr/bin/env python3
"""Generate the Ultrasonic Sensor Integration Paths decision PDF for Elktron."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Flowable
)

# ── Colors ──────────────────────────────────────────────────────────────────
DARK_BG = HexColor("#1a1a2e")
ACCENT_BLUE = HexColor("#0f3460")
ACCENT_TEAL = HexColor("#16213e")
HIGHLIGHT = HexColor("#e94560")
SOFT_GRAY = HexColor("#f0f0f0")
MED_GRAY = HexColor("#d0d0d0")
LIGHT_BLUE = HexColor("#e8f0fe")
LIGHT_GREEN = HexColor("#e6f4ea")
LIGHT_RED = HexColor("#fce8e6")
LIGHT_YELLOW = HexColor("#fef7e0")
CODE_BG = HexColor("#f5f5f5")

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(OUT_DIR, "ultrasonic-integration-paths.pdf")


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "CoverTitle", parent=styles["Title"], fontSize=28, leading=34,
        textColor=white, alignment=TA_CENTER, spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        "CoverSub", parent=styles["Normal"], fontSize=14, leading=18,
        textColor=HexColor("#cccccc"), alignment=TA_CENTER, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "SectionHead", parent=styles["Heading1"], fontSize=18, leading=22,
        textColor=ACCENT_BLUE, spaceBefore=16, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "SubHead", parent=styles["Heading2"], fontSize=14, leading=17,
        textColor=ACCENT_TEAL, spaceBefore=10, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=10, leading=14,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "BodySmall", parent=styles["Normal"], fontSize=9, leading=12,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "CodeBlock", parent=styles["Normal"], fontName="Courier", fontSize=8.5,
        leading=11, spaceAfter=6, leftIndent=12, backColor=CODE_BG,
    ))
    styles.add(ParagraphStyle(
        "CalloutText", parent=styles["Normal"], fontSize=10, leading=14,
        leftIndent=8, rightIndent=8, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "TableCell", parent=styles["Normal"], fontSize=9, leading=11,
    ))
    styles.add(ParagraphStyle(
        "TableCellBold", parent=styles["Normal"], fontSize=9, leading=11,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "TableHead", parent=styles["Normal"], fontSize=9, leading=11,
        fontName="Helvetica-Bold", textColor=white,
    ))
    return styles


class CalloutBox(Flowable):
    """Colored callout box with a left border accent."""

    def __init__(self, text, bg_color=LIGHT_BLUE, border_color=ACCENT_BLUE, width=None):
        super().__init__()
        self._text = text
        self._bg = bg_color
        self._border = border_color
        self._width = width or 6.5 * inch

    def wrap(self, availWidth, availHeight):
        self._width = min(self._width, availWidth)
        style = ParagraphStyle("_cb", fontName="Helvetica", fontSize=10, leading=14,
                               leftIndent=8, rightIndent=8)
        self._para = Paragraph(self._text, style)
        pw, self._ph = self._para.wrap(self._width - 24, availHeight)
        self._ph += 16  # padding
        return self._width, self._ph

    def draw(self):
        self.canv.setFillColor(self._bg)
        self.canv.roundRect(0, 0, self._width, self._ph, 4, fill=1, stroke=0)
        self.canv.setFillColor(self._border)
        self.canv.rect(0, 0, 4, self._ph, fill=1, stroke=0)
        self._para.drawOn(self.canv, 12, 8)


def make_table(data, col_widths=None, header_bg=ACCENT_BLUE):
    """Build a styled table with header row and alternating row colors."""
    styles = build_styles()
    # Wrap strings in Paragraphs
    wrapped = []
    for i, row in enumerate(data):
        new_row = []
        for cell in row:
            if isinstance(cell, str):
                st = styles["TableHead"] if i == 0 else styles["TableCell"]
                new_row.append(Paragraph(cell, st))
            else:
                new_row.append(cell)
        wrapped.append(new_row)

    t = Table(wrapped, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, MED_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    # Alternating rows
    for i in range(1, len(wrapped)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), SOFT_GRAY))
    t.setStyle(TableStyle(cmds))
    return t


def cover_page(styles):
    """Page 1: Cover."""
    elements = []
    elements.append(Spacer(1, 2.5 * inch))

    # Dark banner table
    banner_data = [[
        Paragraph("Elktron Escort Bot", styles["CoverTitle"]),
    ], [
        Paragraph("Ultrasonic Sensor Integration Paths", styles["CoverSub"]),
    ], [
        Paragraph("Technical Decision Document", styles["CoverSub"]),
    ], [
        Spacer(1, 24),
    ], [
        Paragraph("Team Elktron  |  March 17, 2026  |  Hackathon Demo: March 23", styles["CoverSub"]),
    ]]
    banner = Table(banner_data, colWidths=[6.5 * inch])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, 0), 20),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [8, 8, 8, 8]),
    ]))
    elements.append(banner)
    elements.append(PageBreak())
    return elements


def executive_summary(styles):
    """Page 2: Executive Summary."""
    elements = []
    elements.append(Paragraph("Executive Summary", styles["SectionHead"]))

    elements.append(Paragraph(
        "<b>The Problem:</b> The HC-SR04 ultrasonic sensor outputs a 5V echo signal. "
        "The Raspberry Pi 5 GPIO pins are rated for 3.3V max. Connecting the echo pin "
        "directly to the Pi <b>will damage the GPIO header</b> and potentially brick the board. "
        "We need a safe way to interface the sensor with the Pi.",
        styles["Body"]
    ))
    elements.append(Spacer(1, 8))

    elements.append(CalloutBox(
        "<b>WARNING:</b> Connecting a 5V signal directly to Pi 5 GPIO will cause permanent damage. "
        "Both paths below solve this safely. Do NOT skip level shifting.",
        bg_color=LIGHT_RED, border_color=HIGHLIGHT
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Path A: Voltage Divider (Resistors)</b>", styles["SubHead"]))
    elements.append(Paragraph(
        "Use a simple resistor voltage divider (1k + 2k ohm) to step the 5V echo signal down to ~3.3V "
        "before it reaches the Pi GPIO. This is the textbook approach — cheap, well-documented, and requires "
        "no additional compute devices. However, we currently <b>do not have resistors or a breadboard</b> "
        "in the parts inventory.",
        styles["Body"]
    ))

    elements.append(Paragraph("<b>Path B: Pico 2 Middleware</b>", styles["SubHead"]))
    elements.append(Paragraph(
        "Use a Raspberry Pi Pico 2 as an intermediary. The Pico's GPIO is 3.3V native and 5V tolerant on "
        "inputs, so the HC-SR04 echo pin connects directly — no resistors needed. The Pico reads distance "
        "in a real-time loop (no Linux scheduling jitter) and sends readings to the Pi over USB serial. "
        "We <b>already own 2 Pico 2 boards</b>.",
        styles["Body"]
    ))
    elements.append(Spacer(1, 12))

    elements.append(CalloutBox(
        "<b>RECOMMENDATION:</b> Path B (Pico 2 Middleware). Eliminates the resistor blocker entirely, "
        "provides more reliable distance readings, frees Pi CPU for YOLO inference, and follows the "
        "same sensor-microcontroller-SBC pattern used in commercial robotics. All parts are already in hand.",
        bg_color=LIGHT_GREEN, border_color=HexColor("#34a853")
    ))
    elements.append(PageBreak())
    return elements


def path_a(styles):
    """Pages 3-4: Path A — Direct HC-SR04 to Pi 5."""
    elements = []
    elements.append(Paragraph("PATH A — Direct HC-SR04 to Pi 5 (Voltage Divider)", styles["SectionHead"]))

    # Architecture diagram
    elements.append(Paragraph("Architecture", styles["SubHead"]))
    arch_lines = [
        "HC-SR04          Voltage Divider        Raspberry Pi 5",
        "+---------+      +-------------+        +-------------+",
        "| VCC  ---|----->| 5V rail     |        |             |",
        "| TRIG ---|<-----|-GPIO 25 (out)|<------| GPIO 25     |",
        "| ECHO ---|----->| 1k resistor |------->| GPIO 24     |",
        "|         |      |    |        |        |             |",
        "|         |      |  2k to GND  |        |             |",
        "| GND  ---|----->| GND rail    |------->| GND         |",
        "+---------+      +-------------+        +-------------+",
    ]
    for line in arch_lines:
        elements.append(Paragraph(line, styles["CodeBlock"]))
    elements.append(Spacer(1, 8))

    # Voltage divider explanation
    elements.append(Paragraph("Voltage Divider Circuit", styles["SubHead"]))
    elements.append(Paragraph(
        "The voltage divider uses two resistors to reduce the 5V echo signal to a Pi-safe voltage. "
        "With R1=1k ohm and R2=2k ohm: V<sub>out</sub> = 5V x (2k / (1k + 2k)) = 3.33V. "
        "This is within the Pi 5 GPIO input threshold (3.3V max).",
        styles["Body"]
    ))
    divider_lines = [
        "  ECHO (5V) ----[ 1k ohm ]----+---- GPIO 24 (3.33V)",
        "                               |",
        "                          [ 2k ohm ]",
        "                               |",
        "                              GND",
    ]
    for line in divider_lines:
        elements.append(Paragraph(line, styles["CodeBlock"]))
    elements.append(Spacer(1, 8))

    # Required parts
    elements.append(Paragraph("Required Parts", styles["SubHead"]))
    parts_data = [
        ["Part", "Qty", "Status", "Est. Cost"],
        ["1k ohm resistor", "2", "NOT IN HAND", "$0.10"],
        ["2k ohm resistor", "2", "NOT IN HAND", "$0.10"],
        ["Half-size breadboard", "1", "NOT IN HAND", "$3-5"],
        ["Jumper wires (M-M)", "4+", "LIMITED (from ELEGOO kit)", "$0"],
        ["HC-SR04 sensor", "1", "DELIVERED 3/12", "$0"],
    ]
    elements.append(make_table(parts_data, col_widths=[2.2*inch, 0.6*inch, 2*inch, 1*inch]))
    elements.append(Spacer(1, 8))

    # GPIO pins
    elements.append(Paragraph("GPIO Pin Assignments", styles["SubHead"]))
    gpio_data = [
        ["Function", "GPIO (BCM)", "Physical Pin", "Direction"],
        ["TRIG", "GPIO 25", "Pin 22", "Output (Pi to sensor)"],
        ["ECHO", "GPIO 24", "Pin 18", "Input (sensor to Pi, via divider)"],
        ["VCC", "5V rail", "Pin 2 or 4", "Power"],
        ["GND", "GND", "Pin 6, 9, 14, etc.", "Ground"],
    ]
    elements.append(make_table(gpio_data, col_widths=[1.2*inch, 1.2*inch, 1.2*inch, 2.6*inch]))
    elements.append(Spacer(1, 8))

    # Wiring steps
    elements.append(Paragraph("Wiring Steps", styles["SubHead"]))
    steps = [
        "1. Place 1k and 2k resistors on breadboard in series (voltage divider configuration).",
        "2. Connect HC-SR04 VCC to Pi 5V rail (Pin 2 or 4).",
        "3. Connect HC-SR04 GND to Pi GND (Pin 6).",
        "4. Connect HC-SR04 TRIG to GPIO 25 (Pin 22) — direct, no resistor needed.",
        "5. Connect HC-SR04 ECHO to one end of 1k resistor.",
        "6. Connect junction of 1k and 2k resistors to GPIO 24 (Pin 18).",
        "7. Connect other end of 2k resistor to GND.",
        "8. Double-check: ECHO line should read ~3.3V with multimeter when sensor triggers.",
    ]
    for s in steps:
        elements.append(Paragraph(s, styles["Body"]))
    elements.append(Spacer(1, 8))

    # Code
    elements.append(Paragraph("Python Code (Pi Side)", styles["SubHead"]))
    code_lines = [
        "from gpiozero import DistanceSensor",
        "from time import sleep",
        "",
        "sensor = DistanceSensor(echo=24, trigger=25, max_distance=4.0)",
        "",
        "while True:",
        "    d = sensor.distance * 100  # meters to cm",
        '    print(f"Distance: {d:.1f} cm")',
        "    sleep(0.1)",
    ]
    for line in code_lines:
        elements.append(Paragraph(line if line else "&nbsp;", styles["CodeBlock"]))
    elements.append(Spacer(1, 12))

    # Pros / Cons
    elements.append(Paragraph("Pros", styles["SubHead"]))
    pros = [
        "Simpler software — single device, one codebase, gpiozero handles timing",
        "Fewer physical components on the chassis (no extra board)",
        "Well-documented approach — thousands of Pi + HC-SR04 tutorials",
        "Lower latency — no serial communication overhead",
    ]
    for p in pros:
        elements.append(Paragraph("+ " + p, styles["Body"]))

    elements.append(Paragraph("Cons", styles["SubHead"]))
    cons = [
        "Resistors and breadboard NOT in inventory — must order or buy locally",
        "5V risk: incorrect resistor values or loose breadboard connection = fried GPIO",
        "Linux timing jitter: gpiozero uses polling, not real-time — readings can be noisy",
        "Breadboard reliability: vibration on a moving robot can loosen connections",
        "Uses 2 GPIO pins that could be needed for future expansion",
    ]
    for c in cons:
        elements.append(Paragraph("- " + c, styles["Body"]))

    elements.append(PageBreak())
    return elements


def path_b(styles):
    """Pages 5-6: Path B — HC-SR04 to Pico 2 to Pi 5."""
    elements = []
    elements.append(Paragraph("PATH B — HC-SR04 to Pico 2 to Pi 5 (Microcontroller Middleware)", styles["SectionHead"]))

    # Architecture
    elements.append(Paragraph("Architecture", styles["SubHead"]))
    arch_lines = [
        "HC-SR04          Pico 2                  Raspberry Pi 5",
        "+---------+      +----------------+      +-------------+",
        "| VCC  ---|----->| 3V3 or VBUS(5V)|      |             |",
        "| TRIG ---|<-----|  GP2 (output)  |      |             |",
        "| ECHO ---|----->|  GP3 (input)   |      |             |",
        "| GND  ---|----->|  GND           |      |             |",
        "+---------+      |                |      |             |",
        "                 |  USB (serial)  |=====>| /dev/ttyACM0|",
        "                 +----------------+      +-------------+",
        "                  micro-USB cable          USB-A port",
    ]
    for line in arch_lines:
        elements.append(Paragraph(line, styles["CodeBlock"]))
    elements.append(Spacer(1, 8))

    # Why no voltage divider
    elements.append(Paragraph("Why No Voltage Divider Needed", styles["SubHead"]))
    elements.append(Paragraph(
        "The Raspberry Pi Pico 2 (RP2350) GPIO pins are 3.3V logic but <b>5V tolerant on inputs</b>. "
        "The HC-SR04 echo pin outputs 5V — the Pico can read this directly without damage. "
        "The Pico's bare-metal MicroPython firmware handles the precise microsecond timing needed "
        "for ultrasonic pulse measurement far better than Linux on the Pi 5.",
        styles["Body"]
    ))
    elements.append(Spacer(1, 8))

    elements.append(CalloutBox(
        "<b>KEY ADVANTAGE:</b> The Pico eliminates the resistor requirement entirely. All parts "
        "for this path are already in the inventory — no ordering, no waiting, no risk of wrong values.",
        bg_color=LIGHT_GREEN, border_color=HexColor("#34a853")
    ))
    elements.append(Spacer(1, 8))

    # Required parts
    elements.append(Paragraph("Required Parts", styles["SubHead"]))
    parts_data = [
        ["Part", "Qty", "Status", "Est. Cost"],
        ["Raspberry Pi Pico 2", "1", "OWNED (have 2)", "$0"],
        ["Micro-USB cable", "1", "CHECK INVENTORY", "$0-5"],
        ["Jumper wires (M-F)", "4", "FROM ELEGOO KIT", "$0"],
        ["HC-SR04 sensor", "1", "DELIVERED 3/12", "$0"],
    ]
    elements.append(make_table(parts_data, col_widths=[2.2*inch, 0.6*inch, 2*inch, 1*inch]))
    elements.append(Spacer(1, 8))

    # GPIO pins
    elements.append(Paragraph("GPIO Pin Assignments", styles["SubHead"]))
    elements.append(Paragraph("<b>Pico 2 Side:</b>", styles["Body"]))
    pico_gpio = [
        ["Function", "Pico GPIO", "Physical Pin", "Direction"],
        ["TRIG", "GP2", "Pin 4", "Output (Pico to sensor)"],
        ["ECHO", "GP3", "Pin 5", "Input (sensor to Pico)"],
        ["VCC", "VBUS (5V)", "Pin 40", "Power (USB 5V passthrough)"],
        ["GND", "GND", "Pin 3, 8, etc.", "Ground"],
    ]
    elements.append(make_table(pico_gpio, col_widths=[1.2*inch, 1.2*inch, 1.2*inch, 2.6*inch]))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("<b>Pi 5 Side:</b>", styles["Body"]))
    pi_gpio = [
        ["Function", "Connection", "Notes"],
        ["USB Serial", "/dev/ttyACM0", "Auto-detected when Pico plugged in"],
        ["Baud rate", "115200", "Standard serial speed"],
        ["Protocol", "Line-based ASCII", 'Each line: "DIST:123.4" (cm)'],
    ]
    elements.append(make_table(pi_gpio, col_widths=[1.5*inch, 1.8*inch, 3*inch]))
    elements.append(Spacer(1, 8))

    # Wiring steps
    elements.append(Paragraph("Wiring Steps", styles["SubHead"]))
    steps = [
        "1. Flash MicroPython firmware onto Pico 2 (if not already done).",
        "2. Connect HC-SR04 VCC to Pico VBUS (Pin 40) — provides 5V from USB.",
        "3. Connect HC-SR04 GND to Pico GND (Pin 3).",
        "4. Connect HC-SR04 TRIG to Pico GP2 (Pin 4).",
        "5. Connect HC-SR04 ECHO to Pico GP3 (Pin 5) — direct, no resistor.",
        "6. Upload sonar_bridge.py to Pico as main.py (runs on boot).",
        "7. Connect Pico to Pi 5 via micro-USB cable (Pi USB-A port).",
        "8. Verify: ls /dev/ttyACM0 on Pi — should appear immediately.",
    ]
    for s in steps:
        elements.append(Paragraph(s, styles["Body"]))
    elements.append(Spacer(1, 8))

    # Pico code
    elements.append(Paragraph("MicroPython Code (Pico 2 Side — sonar_bridge.py)", styles["SubHead"]))
    pico_code = [
        "import machine, time, sys",
        "",
        "trig = machine.Pin(2, machine.Pin.OUT)",
        "echo = machine.Pin(3, machine.Pin.IN)",
        "",
        "def measure_cm():",
        '    """Send 10us trigger pulse, measure echo duration, return cm."""',
        "    trig.low()",
        "    time.sleep_us(2)",
        "    trig.high()",
        "    time.sleep_us(10)",
        "    trig.low()",
        "",
        "    # Wait for echo to go HIGH (timeout 30ms)",
        "    t0 = time.ticks_us()",
        "    while echo.value() == 0:",
        "        if time.ticks_diff(time.ticks_us(), t0) > 30000:",
        "            return -1  # timeout",
        "    start = time.ticks_us()",
        "",
        "    # Wait for echo to go LOW",
        "    while echo.value() == 1:",
        "        if time.ticks_diff(time.ticks_us(), start) > 30000:",
        "            return -1  # timeout",
        "    end = time.ticks_us()",
        "",
        "    duration = time.ticks_diff(end, start)",
        "    distance_cm = (duration * 0.0343) / 2",
        "    return round(distance_cm, 1)",
        "",
        "# Main loop: send readings over USB serial at ~10Hz",
        "while True:",
        "    dist = measure_cm()",
        "    if dist >= 0:",
        '        print(f"DIST:{dist}")',
        "    else:",
        '        print("DIST:ERR")',
        "    time.sleep_ms(100)",
    ]
    for line in pico_code:
        elements.append(Paragraph(line if line else "&nbsp;", styles["CodeBlock"]))
    elements.append(Spacer(1, 8))

    # Pi code
    elements.append(Paragraph("Python Code (Pi 5 Side — serial reader)", styles["SubHead"]))
    pi_code = [
        "import serial, threading",
        "",
        "class PicoSonar:",
        '    """Read distance from Pico 2 over USB serial."""',
        "",
        "    def __init__(self, port='/dev/ttyACM0', baud=115200):",
        "        self.ser = serial.Serial(port, baud, timeout=1)",
        "        self.distance_cm = -1",
        "        self._running = True",
        "        self._thread = threading.Thread(",
        "            target=self._read_loop, daemon=True",
        "        )",
        "        self._thread.start()",
        "",
        "    def _read_loop(self):",
        "        while self._running:",
        "            try:",
        "                line = self.ser.readline().decode().strip()",
        '                if line.startswith("DIST:"):",',
        '                    val = line.split(":")[1]',
        '                    if val != "ERR":',
        "                        self.distance_cm = float(val)",
        "            except Exception:",
        "                pass",
        "",
        "    @property",
        "    def distance_m(self):",
        "        return self.distance_cm / 100.0 if self.distance_cm > 0 else -1",
        "",
        "    def close(self):",
        "        self._running = False",
        "        self.ser.close()",
        "",
        "# Usage in main.py:",
        "# sonar = PicoSonar()",
        "# if sonar.distance_m < STOP_DISTANCE:",
        "#     robot.stop()  # emergency brake",
    ]
    for line in pi_code:
        elements.append(Paragraph(line if line else "&nbsp;", styles["CodeBlock"]))
    elements.append(Spacer(1, 12))

    # Pros / Cons
    elements.append(Paragraph("Pros", styles["SubHead"]))
    pros = [
        "No resistors or breadboard needed — all parts already owned",
        "Real-time timing: Pico runs bare-metal, microsecond-accurate pulse measurement",
        "Frees Pi 5 CPU: no GPIO polling thread competing with YOLOv8n inference",
        "3-tier architecture: sensor > microcontroller > SBC (same pattern as commercial robots)",
        "Pico powered by USB from Pi — no extra power supply needed",
        "Spare Pico 2 available for demo day backup",
    ]
    for p in pros:
        elements.append(Paragraph("+ " + p, styles["Body"]))

    elements.append(Paragraph("Cons", styles["SubHead"]))
    cons = [
        "Extra physical device on chassis — needs mounting space",
        "USB cable routing through chassis (adds a cable to manage)",
        "Two codebases: MicroPython on Pico + Python on Pi",
        "Serial communication adds ~1-5ms latency per reading",
        "MicroPython flashing required (one-time setup, ~5 min)",
        "If USB disconnects during operation, sonar readings stop (need error handling)",
    ]
    for c in cons:
        elements.append(Paragraph("- " + c, styles["Body"]))

    elements.append(PageBreak())
    return elements


def comparison_table(styles):
    """Page 7: Side-by-side comparison."""
    elements = []
    elements.append(Paragraph("Side-by-Side Comparison", styles["SectionHead"]))

    data = [
        ["Criteria", "Path A: Voltage Divider", "Path B: Pico 2 Middleware"],
        ["Parts in hand?", "NO — need resistors + breadboard", "YES — Pico 2 owned, have 2"],
        ["Estimated cost", "$5-10 (resistor kit + breadboard)", "$0 (all owned)"],
        ["Wiring time", "~30 min (breadboard + divider)", "~15 min (4 jumper wires + USB)"],
        ["Code complexity", "Low — gpiozero handles it", "Medium — 2 scripts, serial protocol"],
        ["Timing accuracy", "Medium — Linux polling, some jitter", "High — bare-metal microsecond"],
        ["CPU impact on Pi", "Uses 1 GPIO polling thread", "Zero — offloaded to Pico"],
        ["Reliability", "Medium — breadboard can loosen", "High — soldered Pico + USB"],
        ["Failure mode", "Loose wire = 5V to GPIO = damage", "USB disconnect = no readings (safe)"],
        ["Pi GPIO pins used", "2 (GPIO 24, 25)", "0 (USB only)"],
        ["Physical footprint", "Small (breadboard on chassis)", "Small (Pico board + USB cable)"],
        ["Debug difficulty", "Easy — direct GPIO, no layers", "Medium — check both Pico + Pi"],
        ["Expandability", "Limited — each sensor needs divider", "High — Pico can read multiple sensors"],
        ["Time to demo impact", "BLOCKED until resistors arrive", "Can start immediately"],
    ]
    elements.append(make_table(data, col_widths=[1.8*inch, 2.3*inch, 2.3*inch]))
    elements.append(Spacer(1, 12))

    elements.append(CalloutBox(
        "<b>BOTTOM LINE:</b> Path B wins on 9 of 13 criteria. The only advantages of Path A are "
        "simpler code and easier debugging — but Path A is blocked by missing parts. "
        "With 6 days to demo, eliminating the parts blocker is the decisive factor.",
        bg_color=LIGHT_YELLOW, border_color=HexColor("#f9ab00")
    ))

    elements.append(PageBreak())
    return elements


def gpio_map(styles):
    """Page 8: Full GPIO pin map."""
    elements = []
    elements.append(Paragraph("Complete GPIO Pin Map (Full Bot)", styles["SectionHead"]))

    elements.append(Paragraph(
        "This table shows every GPIO pin assignment on the escort bot. "
        "Note how Path A uses GPIO 24/25 while Path B frees those pins entirely.",
        styles["Body"]
    ))
    elements.append(Spacer(1, 8))

    data = [
        ["GPIO (BCM)", "Function", "Subsystem", "Path A", "Path B"],
        ["GPIO 2 (SDA)", "I2C Data", "Pan/Tilt Board", "Same", "Same"],
        ["GPIO 3 (SCL)", "I2C Clock", "Pan/Tilt Board", "Same", "Same"],
        ["GPIO 12 (PWM0)", "ENA / Pan Servo", "Motors or Pan/Tilt", "Same", "Same"],
        ["GPIO 13 (PWM1)", "ENB / Tilt Servo", "Motors or Pan/Tilt", "Same", "Same"],
        ["GPIO 17", "IN1 (Left Forward)", "L298N Motors", "Same", "Same"],
        ["GPIO 22", "IN3 (Right Forward)", "L298N Motors", "Same", "Same"],
        ["GPIO 23", "IN4 (Right Backward)", "L298N Motors", "Same", "Same"],
        ["GPIO 24", "HC-SR04 ECHO", "Ultrasonic", "USED (via divider)", "FREE"],
        ["GPIO 25", "HC-SR04 TRIG", "Ultrasonic", "USED", "FREE"],
        ["GPIO 27", "IN2 (Left Backward)", "L298N Motors", "Same", "Same"],
        ["USB-A port", "Pico 2 serial", "Ultrasonic", "Not used", "USED (/dev/ttyACM0)"],
    ]
    elements.append(make_table(data, col_widths=[1.2*inch, 1.4*inch, 1.3*inch, 1.4*inch, 1.2*inch]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "<b>Path B advantage:</b> GPIO 24 and 25 are freed up for future use — "
        "additional sensors, status LEDs, or a buzzer for demo day feedback.",
        styles["Body"]
    ))

    elements.append(PageBreak())
    return elements


def recommendation(styles):
    """Page 9: Recommendation and next steps."""
    elements = []
    elements.append(Paragraph("Recommendation and Next Steps", styles["SectionHead"]))

    elements.append(CalloutBox(
        "<b>RECOMMENDED: Path B — Pico 2 Middleware</b><br/><br/>"
        "Use one Raspberry Pi Pico 2 as a dedicated ultrasonic sensor processor. "
        "Wire the HC-SR04 directly to the Pico, send distance readings to the Pi over USB serial. "
        "This eliminates the resistor blocker, provides better timing accuracy, and follows "
        "industrial robotics architecture patterns.",
        bg_color=LIGHT_GREEN, border_color=HexColor("#34a853")
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Decision Deadline", styles["SubHead"]))
    elements.append(Paragraph(
        "Decide by <b>end of day Tuesday, March 18</b>. Wiring must start Wednesday (3/19) "
        "to leave 4 days for integration testing and demo polish.",
        styles["Body"]
    ))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("If Path B (Pico 2) — Action Items", styles["SubHead"]))
    items_b = [
        "1. Flash MicroPython onto Pico 2 (~5 min with Thonny or mpremote)",
        "2. Upload sonar_bridge.py as main.py on Pico",
        "3. Wire HC-SR04 to Pico (4 jumper wires, ~10 min)",
        "4. Connect Pico to Pi via micro-USB cable",
        "5. Test serial output: python3 -c \"import serial; s=serial.Serial('/dev/ttyACM0', 115200); [print(s.readline()) for _ in range(10)]\"",
        "6. Integrate PicoSonar class into main.py (replace gpiozero DistanceSensor)",
        "7. Mount Pico on chassis with velcro or zip tie",
    ]
    for item in items_b:
        elements.append(Paragraph(item, styles["Body"]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("If Path A (Voltage Divider) — Action Items", styles["SubHead"]))
    items_a = [
        "1. Order resistor assortment kit on Amazon (next-day delivery)",
        "2. Order half-size breadboard if not in kit",
        "3. Wait for delivery (earliest: March 19)",
        "4. Build voltage divider on breadboard",
        "5. Wire HC-SR04 to Pi via divider (GPIO 24/25)",
        "6. Test with sonar_test.py (already written)",
        "7. Secure breadboard to chassis (tape or velcro — breadboards vibrate loose)",
    ]
    for item in items_a:
        elements.append(Paragraph(item, styles["Body"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Timeline to Demo (March 23)", styles["SubHead"]))
    timeline = [
        ["Day", "Date", "Path A", "Path B"],
        ["Tue", "Mar 18", "Order resistors", "Flash Pico + wire sensor"],
        ["Wed", "Mar 19", "Resistors arrive, build divider", "Serial integration in main.py"],
        ["Thu", "Mar 20", "Wire + test ultrasonic", "Motor power + first drive test"],
        ["Fri", "Mar 21", "Motor power + drive test", "Mast assembly + integrated test"],
        ["Sat", "Mar 22", "Integrated test + debug", "Demo polish + backup check"],
        ["Sun", "Mar 23", "DEMO DAY", "DEMO DAY"],
    ]
    elements.append(make_table(timeline, col_widths=[0.6*inch, 0.9*inch, 2.4*inch, 2.4*inch]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "<b>Path B gives 1 extra day of integration time</b> because there is no parts wait. "
        "That extra day is the difference between a polished demo and a last-minute scramble.",
        styles["Body"]
    ))

    elements.append(PageBreak())
    return elements


def appendix(styles):
    """Page 10: Appendix — wiring reference."""
    elements = []
    elements.append(Paragraph("Appendix — Wiring Reference", styles["SectionHead"]))

    # Resistor color codes
    elements.append(Paragraph("Resistor Color Codes (Path A only)", styles["SubHead"]))
    resistor_data = [
        ["Resistor", "Band 1", "Band 2", "Band 3 (Multiplier)", "Band 4 (Tolerance)"],
        ["1k ohm", "Brown", "Black", "Red (x100)", "Gold (5%)"],
        ["2k ohm", "Red", "Black", "Red (x100)", "Gold (5%)"],
    ]
    elements.append(make_table(resistor_data, col_widths=[1*inch, 1*inch, 1*inch, 1.5*inch, 1.5*inch]))
    elements.append(Spacer(1, 12))

    # Pico 2 pinout
    elements.append(Paragraph("Raspberry Pi Pico 2 — Key Pins", styles["SubHead"]))
    pico_pins = [
        ["Pin #", "Label", "Function in This Project"],
        ["3", "GND", "Common ground (sensor + Pi)"],
        ["4", "GP2", "HC-SR04 TRIG (output)"],
        ["5", "GP3", "HC-SR04 ECHO (input, 5V tolerant)"],
        ["36", "3V3 OUT", "3.3V output (not used here)"],
        ["38", "GND", "Additional ground"],
        ["39", "VSYS", "System power input (1.8-5.5V)"],
        ["40", "VBUS", "USB 5V (powers HC-SR04 VCC)"],
        ["USB", "micro-USB", "Serial to Pi 5 (/dev/ttyACM0)"],
    ]
    elements.append(make_table(pico_pins, col_widths=[0.8*inch, 1.2*inch, 4.2*inch]))
    elements.append(Spacer(1, 12))

    # Pi 5 GPIO header
    elements.append(Paragraph("Raspberry Pi 5 — GPIO Header (Used Pins)", styles["SubHead"]))
    pi_pins = [
        ["Phys Pin", "GPIO (BCM)", "Assignment", "Subsystem"],
        ["Pin 2", "5V", "HC-SR04 VCC (Path A only)", "Ultrasonic"],
        ["Pin 3", "GPIO 2 (SDA)", "I2C Data", "Pan/Tilt"],
        ["Pin 5", "GPIO 3 (SCL)", "I2C Clock", "Pan/Tilt"],
        ["Pin 6", "GND", "Common ground", "All"],
        ["Pin 11", "GPIO 17", "L298N IN1 (left fwd)", "Motors"],
        ["Pin 13", "GPIO 27", "L298N IN2 (left bwd)", "Motors"],
        ["Pin 15", "GPIO 22", "L298N IN3 (right fwd)", "Motors"],
        ["Pin 16", "GPIO 23", "L298N IN4 (right bwd)", "Motors"],
        ["Pin 18", "GPIO 24", "HC-SR04 ECHO (Path A only)", "Ultrasonic"],
        ["Pin 22", "GPIO 25", "HC-SR04 TRIG (Path A only)", "Ultrasonic"],
        ["Pin 32", "GPIO 12 (PWM0)", "ENA / Pan servo", "Motors/Pan-Tilt"],
        ["Pin 33", "GPIO 13 (PWM1)", "ENB / Tilt servo", "Motors/Pan-Tilt"],
    ]
    elements.append(make_table(pi_pins, col_widths=[0.8*inch, 1.4*inch, 2.4*inch, 1.6*inch]))
    elements.append(Spacer(1, 12))

    # HC-SR04 specs
    elements.append(Paragraph("HC-SR04 Sensor Specifications", styles["SubHead"]))
    specs = [
        ["Parameter", "Value"],
        ["Operating voltage", "5V DC"],
        ["Operating current", "15mA"],
        ["Frequency", "40kHz"],
        ["Max range", "4m (13ft)"],
        ["Min range", "2cm (0.8in)"],
        ["Trigger pulse", "10us HIGH on TRIG pin"],
        ["Echo output", "HIGH pulse, width = round-trip time"],
        ["Beam angle", "~15 degrees"],
        ["Resolution", "0.3cm"],
    ]
    elements.append(make_table(specs, col_widths=[2*inch, 4.2*inch]))

    return elements


def build_pdf():
    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        title="Elktron Escort Bot — Ultrasonic Integration Paths",
        author="Team Elktron",
    )
    styles = build_styles()
    story = []

    story.extend(cover_page(styles))
    story.extend(executive_summary(styles))
    story.extend(path_a(styles))
    story.extend(path_b(styles))
    story.extend(comparison_table(styles))
    story.extend(gpio_map(styles))
    story.extend(recommendation(styles))
    story.extend(appendix(styles))

    doc.build(story)
    print(f"PDF generated: {OUT_PDF}")


if __name__ == "__main__":
    build_pdf()
