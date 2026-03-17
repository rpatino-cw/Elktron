#!/usr/bin/env python3
"""Generate the Escort Bot Pi 5 Setup Guide PDF — beginner-friendly, visual, complete."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas as pdfcanvas
import os

# ── Colors ──────────────────────────────────────────────────
BG_DARK = HexColor('#1a1a2e')
BG_CARD = HexColor('#16213e')
ACCENT = HexColor('#e94560')
ACCENT_DIM = HexColor('#533a4a')
GREEN = HexColor('#2ecc71')
GREEN_DIM = HexColor('#1a3a2a')
BLUE = HexColor('#3498db')
YELLOW = HexColor('#f39c12')
TEXT_WHITE = HexColor('#e8e8e8')
TEXT_DIM = HexColor('#8a8a9a')
TEXT_DARK = HexColor('#2a2520')
CODE_BG = HexColor('#0d1117')
TERMINAL_GREEN = HexColor('#44dd66')

# ── Page Background ─────────────────────────────────────────
def draw_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(HexColor('#fafaf7'))
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    # Top accent bar
    canvas.setFillColor(ACCENT)
    canvas.rect(0, letter[1] - 4, letter[0], 4, fill=1, stroke=0)
    # Footer
    canvas.setFillColor(TEXT_DIM)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(72, 30, 'Elktron Escort Bot — Pi 5 Setup Guide')
    canvas.drawRightString(letter[0] - 72, 30, f'Page {canvas.getPageNumber()}')
    canvas.restoreState()

# ── Styles ──────────────────────────────────────────────────
sTitle = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=28, leading=34,
                        textColor=TEXT_DARK, alignment=TA_LEFT, spaceAfter=6)
sSubtitle = ParagraphStyle('Subtitle', fontName='Helvetica', fontSize=13, leading=18,
                           textColor=TEXT_DIM, spaceAfter=24)
sH1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=20, leading=26,
                      textColor=ACCENT, spaceBefore=24, spaceAfter=12)
sH2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=15, leading=20,
                      textColor=TEXT_DARK, spaceBefore=16, spaceAfter=8)
sH3 = ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=12, leading=16,
                      textColor=BLUE, spaceBefore=12, spaceAfter=6)
sBody = ParagraphStyle('Body', fontName='Helvetica', fontSize=11, leading=16,
                        textColor=TEXT_DARK, spaceAfter=8)
sSimple = ParagraphStyle('Simple', fontName='Helvetica', fontSize=11, leading=16,
                          textColor=HexColor('#2a7a3a'), spaceAfter=8,
                          leftIndent=12, borderColor=GREEN, borderWidth=0,
                          backColor=HexColor('#e8f5e8'), borderPadding=6)
sCode = ParagraphStyle('Code', fontName='Courier', fontSize=10, leading=14,
                        textColor=HexColor('#1a1a1a'), spaceAfter=10,
                        leftIndent=16, backColor=HexColor('#f0ede6'),
                        borderColor=HexColor('#d0cdc4'), borderWidth=1,
                        borderPadding=(8, 10, 8, 10))
sCodeGreen = ParagraphStyle('CodeGreen', fontName='Courier-Bold', fontSize=10, leading=14,
                             textColor=HexColor('#1a6a2a'), spaceAfter=10,
                             leftIndent=16, backColor=HexColor('#e0f0e0'),
                             borderColor=GREEN, borderWidth=1,
                             borderPadding=(8, 10, 8, 10))
sWarning = ParagraphStyle('Warning', fontName='Helvetica-Bold', fontSize=11, leading=15,
                           textColor=HexColor('#c0392b'), spaceAfter=10,
                           leftIndent=12, backColor=HexColor('#fde8e8'),
                           borderColor=ACCENT, borderWidth=1,
                           borderPadding=(8, 10, 8, 10))
sTip = ParagraphStyle('Tip', fontName='Helvetica', fontSize=10, leading=14,
                       textColor=HexColor('#2a6ab8'), spaceAfter=10,
                       leftIndent=12, backColor=HexColor('#e8f0fa'),
                       borderColor=BLUE, borderWidth=1,
                       borderPadding=(8, 10, 8, 10))
sStepNum = ParagraphStyle('StepNum', fontName='Helvetica-Bold', fontSize=36, leading=40,
                           textColor=HexColor('#d8d0c8'), alignment=TA_LEFT)
sBullet = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=11, leading=16,
                          textColor=TEXT_DARK, spaceAfter=4, leftIndent=20,
                          bulletIndent=8, bulletFontName='Helvetica', bulletFontSize=11)
sCheckbox = ParagraphStyle('Checkbox', fontName='Helvetica', fontSize=11, leading=18,
                            textColor=TEXT_DARK, spaceAfter=4, leftIndent=24)

def hr():
    return HRFlowable(width='100%', thickness=1, color=HexColor('#e0dcd4'),
                       spaceBefore=12, spaceAfter=12)

def step_header(num, title, simple_desc):
    """Create a visual step header with number, title, and plain-English explanation."""
    elements = []
    elements.append(Spacer(1, 8))

    # Step number + title in a table for layout
    step_data = [[
        Paragraph(f'STEP {num:02d}', ParagraphStyle('SN', fontName='Courier-Bold', fontSize=11,
                                                      textColor=ACCENT, leading=14)),
        Paragraph(title, sH2)
    ]]
    step_table = Table(step_data, colWidths=[70, 400])
    step_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('LEFTPADDING', (1, 0), (1, 0), 8),
    ]))
    elements.append(step_table)

    # Plain English explanation
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(simple_desc, sSimple))
    elements.append(Spacer(1, 4))
    return elements

# ── Build PDF ───────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), 'PI-SETUP-GUIDE.pdf')

doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    topMargin=0.8*inch,
    bottomMargin=0.8*inch,
    leftMargin=0.75*inch,
    rightMargin=0.75*inch,
)

story = []

# ════════════════════════════════════════════════════════════
# COVER PAGE
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 60))
story.append(Paragraph('ELKTRON', ParagraphStyle('Brand', fontName='Courier-Bold', fontSize=12,
                                                   textColor=ACCENT, letterSpacing=4)))
story.append(Spacer(1, 8))
story.append(Paragraph('Escort Bot', sTitle))
story.append(Paragraph('Raspberry Pi 5 Setup Guide', ParagraphStyle('Sub', fontName='Helvetica',
    fontSize=18, leading=24, textColor=TEXT_DIM)))
story.append(Spacer(1, 16))
story.append(HRFlowable(width='40%', thickness=2, color=ACCENT, spaceAfter=16))
story.append(Paragraph(
    'Everything you need to go from a blank Raspberry Pi to a working robot — '
    'no tech experience required. Every command is explained in plain English.',
    ParagraphStyle('Intro', fontName='Helvetica', fontSize=12, leading=18,
                   textColor=TEXT_DIM, spaceAfter=24)
))

# What you'll need checklist
story.append(Paragraph('What You Need', sH2))
checklist = [
    ('Raspberry Pi 5', 'The robot\'s brain — a small green computer board'),
    ('MicroSD Card (32GB+)', 'Tiny memory card — stores the operating system and robot code'),
    ('SD Card Reader', 'Plugs the microSD into your laptop so you can install the OS'),
    ('USB-C Power Supply or Power Bank', 'Powers the Pi — like a phone charger (5V, 3A minimum)'),
    ('Laptop or Mac', 'Used to set up the SD card and connect to the Pi remotely'),
    ('WiFi Network + Password', 'The Pi connects to WiFi so you can control it from your laptop'),
    ('HDMI Monitor + Micro-HDMI Cable (optional)', 'Only if WiFi setup fails — lets you see the Pi\'s screen directly'),
]
for item, desc in checklist:
    story.append(Paragraph(
        f'<font face="Courier-Bold" color="#2ecc71">[  ]</font>  '
        f'<b>{item}</b><br/>'
        f'<font size="9" color="#7a7268">{desc}</font>',
        sCheckbox
    ))
story.append(Spacer(1, 8))
story.append(Paragraph(
    '<b>TIP:</b> Get everything laid out on a table before you start. '
    'The whole setup takes about 30 minutes.',
    sTip
))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# STEP 1: FLASH THE SD CARD
# ════════════════════════════════════════════════════════════
story.extend(step_header(1, 'Flash the SD Card',
    'Think of the SD card like a USB drive for the Pi. Right now it\'s blank — we need to '
    'put an operating system on it (like installing Windows on a new computer, but way simpler).'))

story.append(Paragraph('<b>1a. Download Raspberry Pi Imager</b>', sH3))
story.append(Paragraph(
    'This is the official tool from Raspberry Pi that writes the operating system onto your SD card. '
    'It\'s free and works on Mac, Windows, and Linux.',
    sBody
))
story.append(Paragraph('On your laptop (not the Pi), go to:', sBody))
story.append(Paragraph('https://www.raspberrypi.com/software/', sCode))
story.append(Paragraph('Or on Mac, open Terminal and type:', sBody))
story.append(Paragraph('brew install --cask raspberry-pi-imager', sCodeGreen))
story.append(Paragraph(
    '<b>What is Terminal?</b> It\'s an app on your Mac that lets you type commands. '
    'Find it in Applications > Utilities > Terminal, or press Cmd+Space and type "Terminal".',
    sTip
))

story.append(Spacer(1, 8))
story.append(Paragraph('<b>1b. Write the OS to the SD Card</b>', sH3))
story.append(Paragraph('Plug your MicroSD card into your laptop (use the SD card reader if needed). Then:', sBody))

imager_steps = [
    ('Open Raspberry Pi Imager', 'Double-click the app you just downloaded'),
    ('Click CHOOSE DEVICE', 'Select "Raspberry Pi 5" from the list'),
    ('Click CHOOSE OS', 'Go to: Raspberry Pi OS (other) > Raspberry Pi OS Lite (64-bit)'),
    ('Click CHOOSE STORAGE', 'Select your MicroSD card (be careful not to pick your hard drive!)'),
    ('Click NEXT', 'It will ask about settings — this is the important part...'),
]
for i, (action, detail) in enumerate(imager_steps, 1):
    story.append(Paragraph(
        f'<font face="Courier-Bold" color="#e94560">{i}.</font> '
        f'<b>{action}</b> — {detail}',
        sBullet
    ))

story.append(Spacer(1, 8))
story.append(Paragraph(
    '<b>IMPORTANT — DO NOT SKIP THIS!</b> When it asks "Would you like to apply OS customisation settings?", '
    'click EDIT SETTINGS. This is where you set up WiFi and remote access.',
    sWarning
))

story.append(Spacer(1, 8))
story.append(Paragraph('<b>1c. Configure Settings (EDIT SETTINGS screen)</b>', sH3))
story.append(Paragraph('These settings let you connect to the Pi over WiFi without plugging in a keyboard or monitor.', sBody))

settings_data = [
    ['Setting', 'What to Enter', 'Why'],
    ['Hostname', 'escort-bot', 'The name of your Pi on the network'],
    ['Username', 'pi', 'Your login name (keep it simple)'],
    ['Password', '(pick something)', 'You\'ll type this to log in remotely'],
    ['WiFi SSID', '(your WiFi name)', 'Exact name — capitalization matters!'],
    ['WiFi Password', '(your WiFi password)', 'Has to be exact'],
    ['Country', 'US', 'Required for WiFi to work'],
    ['Timezone', 'America/Chicago', 'Or your local timezone'],
    ['Enable SSH', 'Check the box!', 'This lets you control the Pi from your laptop'],
]
settings_table = Table(settings_data, colWidths=[90, 150, 200])
settings_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fafaf7')),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#d0cdc4')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#fafaf7'), HexColor('#f0ede6')]),
]))
story.append(settings_table)
story.append(Spacer(1, 8))
story.append(Paragraph('Click <b>SAVE</b>, then <b>YES</b> twice. Wait for it to finish writing (~5-10 min).', sBody))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# STEP 2: FIRST BOOT
# ════════════════════════════════════════════════════════════
story.extend(step_header(2, 'First Boot',
    'The SD card now has the operating system on it. Time to put it in the Pi, plug in power, '
    'and watch it come alive. You won\'t need a keyboard or monitor — everything is done from your laptop.'))

boot_steps = [
    'Eject the SD card from your laptop (safely remove it first)',
    'Slide the MicroSD card into the Pi 5 — the slot is on the bottom of the board, label facing up',
    'Plug in the USB-C power cable (Pi side) and connect to your power bank or wall adapter',
    'Wait 60-90 seconds — the Pi is booting up and connecting to your WiFi',
    'The red LED on the Pi should be solid (power) and the green LED should blink (activity)',
]
for i, step in enumerate(boot_steps, 1):
    story.append(Paragraph(
        f'<font face="Courier-Bold" color="#e94560">{i}.</font> {step}',
        sBullet
    ))

story.append(Spacer(1, 8))
story.append(Paragraph(
    '<b>What if nothing happens?</b> Check that the USB-C cable is plugged in firmly. '
    'The red LED should light up immediately. If it doesn\'t, try a different cable or power source. '
    'Pi 5 needs at least 5V / 3A — some cheap cables can\'t deliver enough power.',
    sWarning
))

story.append(Spacer(1, 12))
story.append(Paragraph('<b>2b. Connect to the Pi from Your Laptop</b>', sH3))
story.append(Paragraph(
    'Open Terminal on your Mac (Cmd+Space, type "Terminal", hit Enter). Then type:',
    sBody
))
story.append(Paragraph('ssh pi@escort-bot.local', sCodeGreen))
story.append(Paragraph(
    'It will ask for your password — type the one you set in Step 1c. '
    '<b>You won\'t see the characters as you type</b> — that\'s normal! Just type it and press Enter.',
    sBody
))
story.append(Paragraph(
    '<b>What is SSH?</b> It stands for "Secure Shell." It lets you control the Pi\'s '
    'command line from your laptop, over WiFi. It\'s like remote desktop, but text-only.',
    sTip
))

story.append(Spacer(1, 8))
story.append(Paragraph('<b>If escort-bot.local doesn\'t work:</b>', sH3))
story.append(Paragraph('Find the Pi\'s IP address by running this on your Mac:', sBody))
story.append(Paragraph('arp -a | grep -i "raspberry\\|dc:a6\\|b8:27\\|d8:3a\\|2c:cf"', sCode))
story.append(Paragraph('Then connect using the IP address instead:', sBody))
story.append(Paragraph('ssh pi@192.168.1.XXX', sCode))
story.append(Paragraph('(Replace XXX with the actual number you found)', sBody))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# STEP 3: SET UP WIFI (if needed)
# ════════════════════════════════════════════════════════════
story.extend(step_header(3, 'Set Up WiFi (If Not Already Connected)',
    'If you set WiFi in Step 1c, you can skip this. But if the Pi didn\'t connect to WiFi '
    '(or you need to change networks), here\'s how to do it from the command line.'))

story.append(Paragraph(
    'If you\'re connected via SSH, WiFi is already working — skip to Step 4. '
    'If you\'re on a keyboard+monitor plugged directly into the Pi, do this:',
    sBody
))
story.append(Spacer(1, 4))
story.append(Paragraph('<b>Option A — The easy way (graphical menu):</b>', sH3))
story.append(Paragraph('sudo raspi-config', sCodeGreen))
story.append(Paragraph(
    'Use arrow keys to go to: <b>System Options</b> > <b>S1 Wireless LAN</b><br/>'
    'Type your WiFi name, press Enter, type password, press Enter.<br/>'
    'Select Finish and reboot.',
    sBody
))
story.append(Spacer(1, 4))
story.append(Paragraph('<b>Option B — Direct command (if raspi-config gives an error):</b>', sH3))
story.append(Paragraph('sudo nmcli dev wifi list', sCodeGreen))
story.append(Paragraph(
    'This shows all WiFi networks the Pi can see. Find yours in the list, then:',
    sBody
))
story.append(Paragraph('sudo nmcli dev wifi connect "YOUR_WIFI_NAME" password "YOUR_PASSWORD"', sCodeGreen))
story.append(Paragraph('Replace YOUR_WIFI_NAME and YOUR_PASSWORD with your actual WiFi credentials. Keep the quotes.', sBody))

story.append(Spacer(1, 4))
story.append(Paragraph('<b>Verify WiFi is working:</b>', sH3))
story.append(Paragraph('ping -c 3 google.com', sCodeGreen))
story.append(Paragraph(
    'If you see replies with times (like "time=12.3 ms"), WiFi is working. '
    'Press Ctrl+C to stop. If you see "Network is unreachable", double-check your WiFi name and password.',
    sBody
))

story.append(Spacer(1, 4))
story.append(Paragraph(
    '<b>WiFi still not working?</b> Try: <font face="Courier" size="9">sudo rfkill unblock wifi</font> '
    'then retry the nmcli command. If the WiFi chip isn\'t detected at all, '
    'make sure you\'re using Raspberry Pi OS (not Ubuntu) and the Pi 5 board isn\'t defective.',
    sWarning
))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# STEP 4: UPDATE THE SYSTEM
# ════════════════════════════════════════════════════════════
story.extend(step_header(4, 'Update the System',
    'Just like updating your phone, the Pi needs the latest software patches before we install anything. '
    'This is always the first thing you do on a new Pi.'))

story.append(Paragraph('Run this command (copy the whole line and press Enter):', sBody))
story.append(Paragraph('sudo apt-get update &amp;&amp; sudo apt-get upgrade -y', sCodeGreen))

story.append(Spacer(1, 4))
story.append(Paragraph('<b>What this does:</b>', sH3))
cmd_explain = [
    ['Part', 'What It Means'],
    ['sudo', 'Run as administrator (like "Run as Admin" on Windows)'],
    ['apt-get update', 'Downloads the latest list of available software'],
    ['&&', '"If that worked, then also do this next thing"'],
    ['apt-get upgrade -y', 'Installs all available updates. -y means "yes to everything"'],
]
cmd_table = Table(cmd_explain, colWidths=[120, 340])
cmd_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BG_CARD),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (0, -1), 'Courier'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#d0cdc4')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#fafaf7'), HexColor('#f0ede6')]),
]))
story.append(cmd_table)
story.append(Spacer(1, 8))
story.append(Paragraph(
    '<b>This takes 5-10 minutes.</b> You\'ll see lots of text scrolling — that\'s normal. '
    'Don\'t touch anything until you see the command prompt again (the line ending with <font face="Courier">$</font>).',
    sTip
))

story.append(hr())

# ════════════════════════════════════════════════════════════
# STEP 5: INSTALL SYSTEM PACKAGES
# ════════════════════════════════════════════════════════════
story.extend(step_header(5, 'Install System Packages',
    'These are the core apps the robot needs — the camera driver, the pin controller that talks to motors '
    'and sensors, and some helper tools for downloading files.'))

story.append(Paragraph('sudo apt-get install -y python3-picamera2 python3-libcamera python3-lgpio python3-pip unzip wget', sCodeGreen))

story.append(Spacer(1, 4))
pkg_explain = [
    ['Package', 'Plain English'],
    ['python3-picamera2', 'Lets the robot\'s code control the camera'],
    ['python3-libcamera', 'Low-level camera driver (picamera2 needs this)'],
    ['python3-lgpio', 'Controls the Pi\'s GPIO pins (motors, sensors, servos)'],
    ['python3-pip', 'Tool for installing Python packages (like an app store for code)'],
    ['unzip', 'Extracts .zip files (we need this for the AI model)'],
    ['wget', 'Downloads files from the internet via command line'],
]
pkg_table = Table(pkg_explain, colWidths=[140, 320])
pkg_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (0, -1), 'Courier'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#d0cdc4')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#fafaf7'), HexColor('#f0ede6')]),
]))
story.append(pkg_table)

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# STEP 6: INSTALL PYTHON PACKAGES
# ════════════════════════════════════════════════════════════
story.extend(step_header(6, 'Install Python Packages',
    'Python is the programming language the robot uses. These packages are like apps — each one gives '
    'the robot a new ability (see with AI, control motors, take photos, etc).'))

story.append(Paragraph(
    '<b>Run each line one at a time.</b> Wait for each to finish before typing the next one. '
    'You\'ll see "Successfully installed..." when each is done.',
    sBody
))
story.append(Spacer(1, 4))

pip_commands = [
    ('pip install --break-system-packages picamera2>=0.3.12',
     'Camera interface — lets the code take photos and video'),
    ('sudo apt install -y python3-opencv',
     'AI engine — OpenCV DNN lets the robot recognize people'),
    ('pip install --break-system-packages gpiozero>=2.0',
     'Motor/sensor controller — simple commands to drive wheels and read distances'),
    ('pip install --break-system-packages lgpio>=0.2.2.0',
     'Pi 5 pin driver — required for gpiozero to work on the Pi 5'),
    ('pip install --break-system-packages numpy>=1.24.0',
     'Math library — the AI uses this to process camera images'),
    ('pip install --break-system-packages Pillow',
     'Image library — saves photos from the camera as files'),
]
for cmd, desc in pip_commands:
    story.append(Paragraph(cmd, sCodeGreen))
    story.append(Paragraph(f'<i>{desc}</i>', ParagraphStyle('PipDesc', fontName='Helvetica',
        fontSize=9, leading=13, textColor=TEXT_DIM, spaceAfter=8, leftIndent=16)))

story.append(Spacer(1, 4))
story.append(Paragraph(
    '<b>What is --break-system-packages?</b> The Pi\'s new OS (Bookworm) is extra cautious about '
    'installing Python packages. This flag says "I know what I\'m doing, install it anyway." '
    'It\'s safe for our use.',
    sTip
))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# STEP 7: DOWNLOAD THE AI MODEL
# ════════════════════════════════════════════════════════════
story.extend(step_header(7, 'Download the AI Model',
    'The robot needs a pre-trained AI brain to recognize people. We\'re downloading a model from Google '
    'that already knows what a person looks like — no training needed.'))

story.append(Paragraph('Run each command one at a time:', sBody))
story.append(Spacer(1, 4))

model_commands = [
    ('mkdir -p ~/escort-bot/models',
     'Creates a folder to store the AI model. The -p flag means "don\'t complain if it already exists."'),
    ('wget -q "https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip" -O /tmp/ssd_model.zip',
     'Downloads the AI model from Google (4.3 MB). wget is like clicking a download link, but in the terminal.'),
    ('unzip -o /tmp/ssd_model.zip -d ~/escort-bot/models/',
     'Unzips the downloaded file into the models folder. Like double-clicking a .zip on your desktop.'),
    ('mv ~/escort-bot/models/detect.tflite ~/escort-bot/models/ssd_mobilenet_v2.tflite',
     'Renames the file so the robot\'s code can find it. The code looks for "ssd_mobilenet_v2.tflite" specifically.'),
]
for cmd, desc in model_commands:
    story.append(Paragraph(cmd, sCodeGreen))
    story.append(Paragraph(f'<i>{desc}</i>', ParagraphStyle('ModelDesc', fontName='Helvetica',
        fontSize=9, leading=13, textColor=TEXT_DIM, spaceAfter=10, leftIndent=16)))

story.append(hr())

# ════════════════════════════════════════════════════════════
# STEP 8: VERIFY EVERYTHING
# ════════════════════════════════════════════════════════════
story.extend(step_header(8, 'Verify Everything Works',
    'Before we wire up motors and sensors, let\'s make sure the camera, GPIO pins, and AI model '
    'are all working. Think of this as a pre-flight checklist.'))

story.append(Paragraph('<b>8a. Check the camera:</b>', sH3))
story.append(Paragraph('libcamera-hello --list-cameras', sCodeGreen))
story.append(Paragraph(
    'You should see <b>imx708</b> in the output (that\'s the Arducam wide-angle camera). '
    'If nothing shows up, check that the ribbon cable is firmly seated in the CSI port.',
    sBody
))

story.append(Spacer(1, 4))
story.append(Paragraph('<b>8b. Check GPIO pins:</b>', sH3))
story.append(Paragraph('python3 -c "from gpiozero import Device; print(\'GPIO OK:\', Device.pin_factory)"', sCodeGreen))
story.append(Paragraph(
    'Should print "GPIO OK: lgpio" or similar. If you get an error about lgpio, '
    'run <font face="Courier" size="9">sudo apt install python3-lgpio</font> and try again.',
    sBody
))

story.append(Spacer(1, 4))
story.append(Paragraph('<b>8c. Check the AI model:</b>', sH3))
story.append(Paragraph(
    'python3 -c "import cv2; '
    'net=cv2.dnn.readNetFromTensorflow(\'models/ssd_mobilenet_v2.pb\', \'models/ssd_mobilenet_v2.pbtxt\'); '
    'print(\'OpenCV DNN OK\')"',
    sCodeGreen
))
story.append(Paragraph('Should print "OpenCV DNN OK". If you get a file-not-found error, re-run Step 7.', sBody))

story.append(Spacer(1, 8))
story.append(Paragraph(
    'If all three checks pass, the Pi is fully set up! Next: wire up motors, sensors, '
    'and camera, then run <font face="Courier">python3 main.py</font> to start the robot.',
    ParagraphStyle('Done', fontName='Helvetica-Bold', fontSize=12, leading=16,
                   textColor=GREEN, spaceAfter=12, leftIndent=12,
                   backColor=HexColor('#e8f5e8'), borderColor=GREEN, borderWidth=1,
                   borderPadding=(10, 12, 10, 12))
))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# TROUBLESHOOTING
# ════════════════════════════════════════════════════════════
story.append(Paragraph('Troubleshooting', sH1))
story.append(Paragraph('Common problems and how to fix them — in plain English.', sSubtitle))

troubles = [
    ('Can\'t connect via SSH',
     'ssh says "Connection refused" or hangs',
     'The Pi hasn\'t finished booting, or WiFi credentials were wrong. Wait 90 seconds and try again. '
     'If still nothing, plug in a monitor + keyboard and check WiFi settings with sudo raspi-config.'),
    ('WiFi won\'t connect',
     'No networks found, or connection fails',
     'Run: sudo rfkill unblock wifi then: sudo nmcli dev wifi connect "NAME" password "PASS". '
     'If no networks show, the WiFi chip may need a moment — wait 10 seconds and try: sudo nmcli dev wifi list'),
    ('Camera not detected',
     'libcamera-hello shows nothing',
     'The ribbon cable isn\'t seated properly. Pull the black tab on the CSI connector UP, slide the cable in '
     '(blue side facing the USB ports), then push the tab DOWN to lock it. Make sure it\'s the CAM port, not DISP.'),
    ('"No module named lgpio"',
     'GPIO commands fail',
     'Run: sudo apt install python3-lgpio. Pi 5 uses lgpio, not the old RPi.GPIO library.'),
    ('"externally-managed-environment"',
     'pip install fails with a long error',
     'Add --break-system-packages to your pip command. This is normal on Bookworm.'),
    ('Pi is slow or hot',
     'Throttling under load',
     'Attach the active cooler (official heatsink+fan). Pi 5 throttles at 85C. '
     'For demo day: echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor'),
    ('Pi won\'t boot at all',
     'No lights, no activity',
     'Try a different USB-C cable and power source. Pi 5 needs 5V/3A minimum. '
     'Some cables are charge-only (no data) — use a known-good cable.'),
]
for title, symptom, fix in troubles:
    story.append(KeepTogether([
        Paragraph(f'<b>{title}</b>', ParagraphStyle('TTitle', fontName='Helvetica-Bold',
            fontSize=12, leading=16, textColor=ACCENT, spaceBefore=8)),
        Paragraph(f'<i>Symptom: {symptom}</i>', ParagraphStyle('TSym', fontName='Helvetica',
            fontSize=9, leading=13, textColor=TEXT_DIM, spaceAfter=2)),
        Paragraph(fix, ParagraphStyle('TFix', fontName='Helvetica', fontSize=10, leading=15,
            textColor=TEXT_DARK, spaceAfter=10, leftIndent=12,
            backColor=HexColor('#f8f6f0'), borderPadding=8)),
    ]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# GPIO PIN MAP
# ════════════════════════════════════════════════════════════
story.append(Paragraph('GPIO Pin Reference', sH1))
story.append(Paragraph('Which Pi pins connect to which robot parts. You\'ll need this for wiring.', sSubtitle))

gpio_data = [
    ['Pi Pin #', 'GPIO #', 'What It Does', 'Connects To'],
    ['11', '17', 'Left Motor Forward', 'L298N IN1'],
    ['13', '27', 'Left Motor Backward', 'L298N IN2'],
    ['15', '22', 'Right Motor Forward', 'L298N IN3'],
    ['16', '23', 'Right Motor Backward', 'L298N IN4'],
    ['18', '24', 'Ultrasonic Echo', 'HC-SR04 ECHO (through voltage divider!)'],
    ['22', '25', 'Ultrasonic Trigger', 'HC-SR04 TRIG'],
    ['32', '12', 'Pan Servo (left/right)', 'Pan-tilt platform'],
    ['33', '13', 'Tilt Servo (up/down)', 'Pan-tilt platform'],
    ['2', '5V', 'Sensor Power', 'HC-SR04 VCC'],
    ['6', 'GND', 'Common Ground', 'Everything shares this'],
]
gpio_table = Table(gpio_data, colWidths=[55, 55, 145, 205])
gpio_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BG_CARD),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (1, -1), 'Courier-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#d0cdc4')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#fafaf7'), HexColor('#f0ede6')]),
    # Highlight the voltage divider row
    ('BACKGROUND', (0, 6), (-1, 6), HexColor('#fde8e8')),
]))
story.append(gpio_table)

story.append(Spacer(1, 12))
story.append(Paragraph(
    '<b>CRITICAL:</b> The HC-SR04 Echo pin outputs 5V, but Pi 5 GPIO only handles 3.3V. '
    'You MUST use a voltage divider (1k + 2k ohm resistors) on the Echo wire, '
    'or use the 3.3V-safe HC-SR04P version. Skipping this can permanently damage your Pi.',
    sWarning
))

story.append(hr())

# ════════════════════════════════════════════════════════════
# QUICK COMMAND REFERENCE
# ════════════════════════════════════════════════════════════
story.append(Paragraph('Quick Command Reference', sH1))
story.append(Paragraph('Copy-paste cheat sheet — all the commands in one place.', sSubtitle))

ref_data = [
    ['What', 'Command'],
    ['Update system', 'sudo apt-get update && sudo apt-get upgrade -y'],
    ['Install system packages', 'sudo apt-get install -y python3-picamera2 python3-libcamera python3-lgpio python3-pip unzip wget'],
    ['Install picamera2', 'pip install --break-system-packages picamera2>=0.3.12'],
    ['Install OpenCV', 'sudo apt install -y python3-opencv'],
    ['Install gpiozero', 'pip install --break-system-packages gpiozero>=2.0'],
    ['Install lgpio', 'pip install --break-system-packages lgpio>=0.2.2.0'],
    ['Install numpy', 'pip install --break-system-packages numpy>=1.24.0'],
    ['Install Pillow', 'pip install --break-system-packages Pillow'],
    ['Create models dir', 'mkdir -p ~/escort-bot/models'],
    ['Download AI model', 'wget -q "https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip" -O /tmp/ssd_model.zip'],
    ['Unzip model', 'unzip -o /tmp/ssd_model.zip -d ~/escort-bot/models/'],
    ['Rename model', 'mv ~/escort-bot/models/detect.tflite ~/escort-bot/models/ssd_mobilenet_v2.tflite'],
    ['Check camera', 'libcamera-hello --list-cameras'],
    ['Test detection', 'python3 test_camera.py'],
    ['Start robot', 'python3 main.py'],
]
ref_table = Table(ref_data, colWidths=[110, 350])
ref_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BG_CARD),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (1, 1), (1, -1), 'Courier'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#d0cdc4')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#fafaf7'), HexColor('#f0ede6')]),
]))
story.append(ref_table)

story.append(Spacer(1, 24))
story.append(Paragraph(
    'You did it. The Pi is set up, the AI model is loaded, and the robot is ready to be wired. '
    'Next step: follow the Wiring Guide to connect motors, sensors, and camera.',
    ParagraphStyle('Final', fontName='Helvetica-Bold', fontSize=13, leading=18,
                   textColor=TEXT_DARK, alignment=TA_CENTER, spaceAfter=8)
))
story.append(Paragraph(
    'Elktron / Escort Bot / CoreWeave Hackathon 2026',
    ParagraphStyle('Footer', fontName='Helvetica', fontSize=9, leading=12,
                   textColor=TEXT_DIM, alignment=TA_CENTER)
))

# ── Generate ────────────────────────────────────────────────
doc.build(story, onFirstPage=draw_page_bg, onLaterPages=draw_page_bg)
print(f'\nPDF generated: {output_path}')
print(f'Pages: ~10')
print(f'Open: file://{output_path}')
