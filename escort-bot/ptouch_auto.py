#!/usr/bin/env python3
"""Automate Brother P-Touch Editor: insert label image + print, one at a time.
Uses AppleScript to control P-Touch Editor UI.

Usage: python3 ptouch_auto.py
"""

import os
import subprocess
import time

LABELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "labels_ptouch")

# All 27 labels in order
LABELS = [
    # Wire labels (12mm tape recommended, but we'll use whatever's loaded)
    ("WIRE", "01_wire_left_fwd.png", "LEFT FWD"),
    ("WIRE", "02_wire_left_bwd.png", "LEFT BWD"),
    ("WIRE", "03_wire_right_fwd.png", "RIGHT FWD"),
    ("WIRE", "04_wire_right_bwd.png", "RIGHT BWD"),
    ("WIRE", "05_wire_l298n_left.png", "L298N > LEFT"),
    ("WIRE", "06_wire_l298n_right.png", "L298N > RIGHT"),
    ("WIRE", "07_wire_ultra_echo.png", "ULTRA ECHO"),
    ("WIRE", "08_wire_ultra_trig.png", "ULTRA TRIG"),
    ("WIRE", "09_wire_sensor_5v.png", "SENSOR 5V"),
    ("WIRE", "10_wire_sensor_gnd.png", "SENSOR GND"),
    ("WIRE", "11_wire_pan_servo.png", "PAN SERVO"),
    ("WIRE", "12_wire_tilt_servo.png", "TILT SERVO"),
    ("WIRE", "13_wire_18650.png", "18650 > L298N"),
    ("WIRE", "14_wire_common_gnd.png", "COMMON GND"),
    # Board labels
    ("BOARD", "15_board_pi5.png", "RASPBERRY PI 5"),
    ("BOARD", "16_board_l298n.png", "L298N MOTOR DRIVER"),
    ("BOARD", "17_board_hcsr04.png", "HC-SR04 ULTRASONIC"),
    ("BOARD", "18_board_divider.png", "VOLTAGE DIVIDER"),
    ("BOARD", "19_board_arducam.png", "ARDUCAM IMX708"),
    ("BOARD", "20_board_pantilt.png", "PAN/TILT PLATFORM"),
    # Power labels
    ("POWER", "21_power_18650.png", "18650 PACK - 7.4V"),
    ("POWER", "22_power_bank.png", "POWER BANK - 5V"),
    # Orientation
    ("ORIENT", "23_orient_front.png", "FRONT"),
    ("ORIENT", "24_orient_left.png", "LEFT"),
    ("ORIENT", "25_orient_right.png", "RIGHT"),
    ("ORIENT", "26_orient_cam_up.png", "CAM UP"),
    # Branding
    ("BRAND", "27_brand_elktron.png", "ELKTRON"),
]


def insert_image_via_applescript(image_path):
    """Use AppleScript to insert an image into the current P-Touch Editor label."""
    posix_path = os.path.abspath(image_path)

    script = f'''
    tell application "P-touch Editor"
        activate
    end tell
    delay 0.5

    tell application "System Events"
        tell process "P-touch Editor"
            -- Cmd+A to select all, then delete to clear canvas
            keystroke "a" using command down
            delay 0.3
            key code 51
            delay 0.3

            -- Use Insert > Image > From File menu
            try
                click menu item "From File..." of menu "Image" of menu item "Image" of menu "Insert" of menu bar 1
                delay 1
            on error
                -- Try alternate menu path
                try
                    click menu item "Image..." of menu "Insert" of menu bar 1
                    delay 1
                on error
                    -- Last resort: Cmd+Shift+I or toolbar Image button
                    keystroke "a" using command down
                    delay 0.3
                end try
            end try
        end tell
    end tell

    -- Handle the file open dialog
    delay 1
    tell application "System Events"
        tell process "P-touch Editor"
            -- Type the file path in the Go To dialog
            keystroke "g" using {{command down, shift down}}
            delay 0.8
            keystroke "{posix_path}"
            delay 0.5
            keystroke return
            delay 0.5
            keystroke return
            delay 1
        end tell
    end tell
    '''

    subprocess.run(["osascript", "-e", script], capture_output=True)


def print_label():
    """Send Cmd+P then Enter to print."""
    script = '''
    tell application "System Events"
        tell process "P-touch Editor"
            keystroke "p" using command down
            delay 2
            keystroke return
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True)


def main():
    print(f"\n{'='*55}")
    print(f"  ESCORT BOT — P-TOUCH LABEL PRINTER")
    print(f"  {len(LABELS)} labels | PT-D610BT | 24mm tape")
    print(f"{'='*55}")
    print(f"\n  Make sure P-Touch Editor is open and the printer")
    print(f"  is connected via Bluetooth.\n")

    for i, (category, filename, name) in enumerate(LABELS, 1):
        image_path = os.path.join(LABELS_DIR, filename)

        print(f"\n  [{i:2d}/{len(LABELS)}] {category:6s} | {name}")
        print(f"         File: {filename}")

        choice = input(f"\n  [ENTER] Insert & print  |  [s] Skip  |  [q] Quit: ").strip().lower()

        if choice == "q":
            print("\n  Stopped. Resume from label #{} next time.".format(i))
            break
        elif choice == "s":
            print(f"  Skipped.")
            continue

        print(f"  Inserting image into P-Touch Editor...")
        insert_image_via_applescript(image_path)

        time.sleep(1)
        confirm = input(f"  Image inserted. [ENTER] to print, [s] to skip print: ").strip().lower()
        if confirm != "s":
            print(f"  Printing...")
            print_label()
            time.sleep(2)
            print(f"  Sent to printer.")

    print(f"\n{'='*55}")
    print(f"  Done! Labels printed for Escort Bot.")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
