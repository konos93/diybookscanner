*'''
this is for screen 1980*1920
with 33.py yοu can check mouse point potition
use also cam1.py cam0.py

```
python3 -m venv ~/the_directory_you_want_to_install/venv

source ~/the_directory_you_want_to_install/venv/bin/activate

pip install pyautogui

###run inside the venv: python3 (hard pathfile of clicker3.py)
source ~/the_directory_you_want_to_install/venv/bin/deactivate


```
'''

#!/usr/bin/python3

import sys  #use this because python for some reason cant find the install path file
sys.path.append('/usr/lib/python3/dist-packages')
from libcamera import controls

from PyQt5 import QtCore, QtGui, QtWidgets
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
import time
import pyautogui

def automate_task():
    tool1_position = (1800, 400)
    tool2_position = (1800, 900)
    pyautogui.click(tool1_position, clicks=2, interval=0.01)
    pyautogui.click(tool2_position, clicks=2, interval=0.01)
    print("Automation completed.")

def keyPressEvent(event):
    if event.key() == QtCore.Qt.Key_Space:
        print("Spacebar pressed!")
        time.sleep(0.01)
        automate_task()
        time.sleep(0.01)
    elif event.key() == QtCore.Qt.Key_Escape:
        print("Escape key pressed! Script interrupted.")
        QtCore.QCoreApplication.quit()  # Quit the application

def create_gui():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    window.setWindowTitle("small button")
    
    layout = QtWidgets.QVBoxLayout(window)
   
    click_both_button = QtWidgets.QPushButton("Left Click or Space", window)
    click_both_button.clicked.connect(click_both)
    click_both_button.setFixedSize(QtCore.QSize(400, 400))
    layout.addWidget(click_both_button, alignment=QtCore.Qt.AlignCenter)
    
    window.show()  # Show the window first
    window.move(0, 300)  # Move the window after it's displayed
    
    app.exec_()

def click_both():
    print("Click Both button clicked!")
    automate_task()
    pyautogui.moveTo(200, 400)  # if cursor is not moved button seems to be pushed 

if __name__ == "__main__":
    create_gui()
