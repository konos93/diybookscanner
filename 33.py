#!/usr/bin/python3

import time
import pyautogui

def print_cursor_position():
    try:
        while True:
            # Get and print the current cursor position
            current_position = pyautogui.position()
            print(f"Cursor Position: {current_position}")

            # Add a delay if needed to control the loop speed
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nLoop stopped by user.")

if __name__ == "__main__":
    print_cursor_position()
