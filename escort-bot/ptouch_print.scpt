-- Brother P-Touch D610BT Label Printer Script
-- Creates text labels directly in P-Touch Editor and prints one at a time

on run argv
    set labelName to item 1 of argv
    set labelDetail to item 2 of argv

    tell application "P-touch Editor"
        activate
    end tell

    delay 1

    tell application "System Events"
        tell process "P-touch Editor"
            -- Click on the label canvas area to make sure it's focused
            -- Then use keyboard to add text

            -- Select all existing content and delete
            keystroke "a" using command down
            delay 0.3
            key code 51 -- delete
            delay 0.3

            -- Click Text Box button (keyboard shortcut or menu)
            -- Insert > Text Box
            click menu item "Text Box" of menu "Insert" of menu bar 1
            delay 0.5

            -- Type the label text
            keystroke labelName
            keystroke return
            keystroke labelDetail

            delay 0.3

            -- Print
            keystroke "p" using command down
            delay 1

            -- Press Enter to confirm print dialog
            keystroke return
        end tell
    end tell
end run
