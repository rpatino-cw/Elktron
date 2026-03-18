#!/usr/bin/env python3
"""Escort Bot — P-Touch Label Printer v3
Types text directly into P-Touch Editor (proven to work).
Auto-switches to P-Touch Editor and back — user stays in terminal.

Usage:
  python3 ptouch_go.py              # Interactive (confirm each label)
  python3 ptouch_go.py --auto       # Fully automated — no prompts
  python3 ptouch_go.py --start 3    # Start from label #3
  python3 ptouch_go.py --auto --start 3  # Auto from label #3
"""

import argparse
import subprocess
import sys
import time

LABELS = [
    # (category, line1, line2)
    # Wire — motor
    ("MOTOR",  "LEFT FWD",       "GPIO17 > IN1"),
    ("MOTOR",  "LEFT BWD",       "GPIO24 > IN2"),
    ("MOTOR",  "RIGHT FWD",      "GPIO22 > IN3"),
    ("MOTOR",  "RIGHT BWD",      "GPIO23 > IN4"),
    ("MOTOR",  "L298N > LEFT",   "Motor A Term"),
    ("MOTOR",  "L298N > RIGHT",  "Motor B Term"),
    # Wire — sensor
    ("SENSOR", "ULTRA ECHO",     "GPIO26 < HC-SR04"),
    ("SENSOR", "ULTRA TRIG",     "GPIO25 > HC-SR04"),
    ("SENSOR", "SENSOR 5V",      "Pin2 > VCC"),
    ("SENSOR", "SENSOR GND",     "Pin6 > GND"),
    # Wire — servo
    ("SERVO",  "PAN SERVO",      "GPIO12 > MG90S"),
    ("SERVO",  "TILT SERVO",     "GPIO13 > MG90S"),
    # Wire — power
    ("POWER",  "18650 > L298N",  "7.4V CHECK +/-"),
    ("POWER",  "COMMON GND",     "Pi <> L298N GND"),
    # Board
    ("BOARD",  "RASPBERRY PI 5", "5V/3A USB-C"),
    ("BOARD",  "L298N DRIVER",   "7.4V 2CH IN1-4"),
    ("BOARD",  "HC-SR04",        "5V>3.3V DIVIDER"),
    ("BOARD",  "V-DIVIDER",      "1k+2k 3.3V SAFE"),
    ("BOARD",  "ARDUCAM IMX708", "CSI RIBBON AF"),
    ("BOARD",  "PAN/TILT",       "PAN G12 TILT G13"),
    # Power warning
    ("WARN",   "18650 7.4V",     "MOTORS ONLY!"),
    ("WARN",   "BANK 5V USB-C",  "PI ONLY 3A MIN"),
    # Orientation
    ("DIR",    "FRONT",          ""),
    ("DIR",    "LEFT",           ""),
    ("DIR",    "RIGHT",          ""),
    ("DIR",    "CAM UP",         ""),
    # Branding
    ("BRAND",  "ELKTRON",        "CW HACKATHON 2026"),
]


def type_label_and_return(line1, line2):
    """Switch to P-Touch Editor, clear, type formatted label, switch back.
    Line 1: Bold, larger (3x), centered.
    Line 2: Regular, smaller (2x), centered."""
    l1 = line1.replace('"', '\\"').replace("'", "'")
    l2 = line2.replace('"', '\\"').replace("'", "'")

    # Build line 2 block only if there's a second line
    line2_block = ""
    if l2:
        line2_block = f'''
            -- New line
            keystroke return
            delay 0.1

            -- Switch to regular weight for line 2
            click menu item "Bold" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1

            -- Make smaller (2x to go from ~32pt back to ~14pt)
            click menu item "Smaller" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1
            click menu item "Smaller" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1
            click menu item "Smaller" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1

            -- Type line 2
            keystroke "{l2}"
        '''

    script = f'''
    -- Remember who called us
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

            -- Select all + delete to clear canvas
            keystroke "a" using command down
            delay 0.2
            key code 51
            delay 0.3

            -- Center align
            click menu item "Align Center" of menu "Text" of menu item "Text" of menu "Format" of menu bar 1
            delay 0.1

            -- Bold ON for line 1
            click menu item "Bold" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1

            -- Make larger (3x to go from 20pt to ~32pt)
            click menu item "Larger" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1
            click menu item "Larger" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1
            click menu item "Larger" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            delay 0.1

            -- Type line 1 (bold, large, centered)
            keystroke "{l1}"
            {line2_block}
        end tell
    end tell

    delay 0.3

    -- Return to caller
    tell application callerApp
        activate
    end tell
    '''

    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.returncode == 0


def print_and_return():
    """Switch to P-Touch Editor, use File > Print menu, switch back."""
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

            -- Use File > Print… (P-Touch Editor's own print, routes to Brother printer)
            click menu item "Print…" of menu "File" of menu bar 1
            delay 2

            -- Confirm the print dialog (press Return or click Print button)
            keystroke return
            delay 1
        end tell
    end tell

    delay 1
    tell application callerApp
        activate
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description="P-Touch Label Printer for Escort Bot")
    parser.add_argument("--auto", action="store_true", help="Fully automated — no prompts")
    parser.add_argument("--start", type=int, default=1, help="Start from label number (1-27)")
    args = parser.parse_args()

    labels_to_print = LABELS[args.start - 1:]
    mode = "AUTO" if args.auto else "INTERACTIVE"

    print(f"\n{'='*55}")
    print(f"  ESCORT BOT — P-TOUCH LABELS")
    print(f"  {len(labels_to_print)} labels | PT-D610BT | 24mm tape")
    print(f"  Mode: {mode}")
    print(f"{'='*55}")
    print(f"\n  1. Open P-Touch Editor with a blank label")
    print(f"  2. Click the label canvas so cursor is active")
    print(f"  3. Come back here\n")

    input("  [ENTER] to start: ")

    for i, (cat, l1, l2) in enumerate(labels_to_print, args.start):
        display = f"{l1} / {l2}" if l2 else l1
        print(f"\n  [{i:2d}/{len(LABELS)}] {cat:6s} | {display}")

        if not args.auto:
            choice = input("  [ENTER] Go  [s] Skip  [q] Quit: ").strip().lower()
            if choice == "q":
                print(f"\n  Stopped at #{i}.")
                break
            if choice == "s":
                print(f"  Skipped.")
                continue

        # Type into P-Touch Editor and auto-return
        print(f"  Typing... ", end="", flush=True)
        ok = type_label_and_return(l1, l2)
        if ok:
            print(f"done.")
        else:
            print(f"FAILED. Click the label canvas and retry.")
            if args.auto:
                print(f"  Retrying in 3s...")
                time.sleep(3)
                ok = type_label_and_return(l1, l2)
                if not ok:
                    print(f"  FAILED again. Skipping #{i}.")
                    continue
            else:
                continue

        if not args.auto:
            action = input("  [ENTER] Print  [s] Skip print: ").strip().lower()
            if action == "s":
                continue

        # Print
        print(f"  Printing... ", end="", flush=True)
        print_and_return()
        print("sent!")

        if args.auto:
            # Wait for printer to finish before next label
            time.sleep(3)

    print(f"\n  All done!\n")


if __name__ == "__main__":
    main()
