#!/usr/bin/env python3
"""Type labels directly into P-Touch Editor using AppleScript keyboard automation.
For PT-D610BT with 24mm tape.

Usage: python3 ptouch_type.py
"""

import subprocess
import sys
import time

# All labels: (category, line1, line2_optional)
LABELS = [
    # Wire labels
    ("WIRE", "LEFT FWD", "GPIO17 > IN1"),
    ("WIRE", "LEFT BWD", "GPIO27 > IN2"),
    ("WIRE", "RIGHT FWD", "GPIO22 > IN3"),
    ("WIRE", "RIGHT BWD", "GPIO23 > IN4"),
    ("WIRE", "L298N>LEFT", "Motor A"),
    ("WIRE", "L298N>RIGHT", "Motor B"),
    ("WIRE", "ULTRA ECHO", "GPIO24<HC-SR04"),
    ("WIRE", "ULTRA TRIG", "GPIO25>HC-SR04"),
    ("WIRE", "SENSOR 5V", "Pin2>VCC"),
    ("WIRE", "SENSOR GND", "Pin6>GND"),
    ("WIRE", "PAN SERVO", "GPIO12>MG90S"),
    ("WIRE", "TILT SERVO", "GPIO13>MG90S"),
    ("WIRE", "18650>L298N", "7.4V CHECK+/-"),
    ("WIRE", "COMMON GND", "Pi<>L298N GND"),
    # Board labels
    ("BOARD", "RASPBERRY PI 5", "5V/3A USB-C"),
    ("BOARD", "L298N DRIVER", "7.4V 2CH IN1-4"),
    ("BOARD", "HC-SR04", "5V>3.3V DIVIDER"),
    ("BOARD", "V-DIVIDER", "1k+2k 3.3V SAFE"),
    ("BOARD", "ARDUCAM IMX708", "CSI RIBBON AF"),
    ("BOARD", "PAN/TILT", "PAN G12 TILT G13"),
    # Power labels
    ("POWER", "18650 7.4V", "MOTORS ONLY!"),
    ("POWER", "BANK 5V", "PI ONLY 3A USB-C"),
    # Orientation
    ("ORIENT", "FRONT", ""),
    ("ORIENT", "LEFT", ""),
    ("ORIENT", "RIGHT", ""),
    ("ORIENT", "CAM UP", ""),
    # Branding
    ("BRAND", "ELKTRON", "CW HACKATHON 26"),
]


def clear_and_type(text_line1, text_line2=""):
    """Clear the P-Touch Editor canvas and type new label text."""
    # Escape special AppleScript characters
    l1 = text_line1.replace('"', '\\"')
    l2 = text_line2.replace('"', '\\"')

    if l2:
        type_block = f'''
            keystroke "{l1}"
            keystroke return
            keystroke "{l2}"
        '''
    else:
        type_block = f'''
            keystroke "{l1}"
        '''

    script = f'''
    tell application "P-touch Editor"
        activate
    end tell
    delay 1

    tell application "System Events"
        tell process "P-touch Editor"
            set frontmost to true
            delay 0.3

            -- Click on the label canvas area (center of window)
            try
                click at {{500, 350}}
                delay 0.3
            end try

            -- Select all and delete existing content
            keystroke "a" using command down
            delay 0.3
            key code 51
            delay 0.3

            -- Type the new label text
            {type_block}
        end tell
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  AppleScript error: {result.stderr.strip()}")
        return False
    return True


def print_current():
    """Click P-Touch Editor's own Print button in the toolbar (not Cmd+P).
    P-Touch Editor prints directly to the label printer via its own driver."""
    script = '''
    tell application "P-touch Editor"
        activate
    end tell
    delay 0.8

    tell application "System Events"
        tell process "P-touch Editor"
            -- Try clicking the Print button in the toolbar
            try
                click button "Print" of toolbar 1 of window 1
                delay 2
            on error
                -- Fallback: try the menu bar File > Print
                try
                    click menu item "Print" of menu "File" of menu bar 1
                    delay 2
                on error
                    -- Last resort: Cmd+P (but make sure P-Touch Editor has focus)
                    set frontmost to true
                    delay 0.3
                    keystroke "p" using command down
                    delay 2
                end try
            end try

            -- Confirm print dialog if one appears
            try
                click button "Print" of sheet 1 of window 1
            on error
                try
                    keystroke return
                end try
            end try
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True)


def main():
    print(f"\n{'='*55}")
    print(f"  ESCORT BOT — P-TOUCH LABEL PRINTER")
    print(f"  {len(LABELS)} labels | PT-D610BT | 24mm tape")
    print(f"{'='*55}")
    print(f"\n  Open P-Touch Editor with a blank label first.")
    print(f"  Click on the label canvas so text cursor is active.")
    print(f"  Then come back here and press ENTER to start.\n")

    input("  Ready? [ENTER] to begin: ")

    for i, (category, line1, line2) in enumerate(LABELS, 1):
        print(f"\n  [{i:2d}/{len(LABELS)}] {category:6s} | {line1}" + (f" / {line2}" if line2 else ""))

        choice = input(f"  [ENTER] Type & print  |  [s] Skip  |  [q] Quit: ").strip().lower()

        if choice == "q":
            print(f"\n  Stopped at label #{i}. Run again to resume.")
            break
        elif choice == "s":
            print(f"  Skipped.")
            continue

        print(f"  Typing into P-Touch Editor...")
        success = clear_and_type(line1, line2)

        if success:
            time.sleep(0.5)
            action = input(f"  Text inserted. [ENTER] Print  |  [s] Skip print  |  [r] Retype: ").strip().lower()
            if action == "r":
                clear_and_type(line1, line2)
                input(f"  Retyped. [ENTER] to print: ")
                print_current()
                time.sleep(2)
            elif action != "s":
                print(f"  Printing...")
                print_current()
                time.sleep(2)
                print(f"  Sent!")
        else:
            print(f"  Failed — click on the label canvas in P-Touch Editor and try again.")

    print(f"\n{'='*55}")
    print(f"  All done! {len(LABELS)} labels for Escort Bot.")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
