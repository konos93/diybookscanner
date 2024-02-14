#!/usr/bin/python3

from libcamera import controls
from PyQt5 import QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
                             QPushButton, QVBoxLayout, QWidget, QDoubleSpinBox)
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
import numpy as np
import time

STATE_AF = 0
STATE_CAPTURE = 1


def request_callback(request):
    lens_position = request.get_metadata().get('LensPosition', 'N/A')
    # Format the lens position to display up to 3 decimal places
    lens_position_str = f"{float(lens_position):.3f}" if lens_position != 'N/A' else 'N/A'
    label.setText(f"Lens Position: {lens_position_str}")
   

picam2 = Picamera2(1)
picam2.post_callback = request_callback
preview_width = 800# change me to check manual focus
preview_height = picam2.sensor_resolution[1] * preview_width  // picam2.sensor_resolution[0]
preview_height -= preview_height % 2
preview_size = (preview_width, preview_height)
raw_size = tuple([v // 2 for v in picam2.camera_properties['PixelArraySize']])
preview_config = picam2.create_preview_configuration({"size": preview_size}, raw={"size": raw_size})
picam2.configure(preview_config)
if 'AfMode' not in picam2.camera_controls:
    print("Attached camera does not support autofocus")
    quit()
picam2.set_controls({"AfMode": controls.AfModeEnum.Auto,"AfSpeed": controls.AfSpeedEnum.Fast})
app = QApplication([])

def on_button_clicked():
    global state
    button.setEnabled(False)
    manual_focus.setEnabled(False)
    af_checkbox.setEnabled(False)
    state = STATE_AF if af_checkbox.isChecked() else STATE_CAPTURE
    if state == STATE_AF:
        picam2.autofocus_cycle(signal_function=qpicamera2.signal_done)
    else:
        do_capture()
    # Remove focus from QDoubleSpinBox
    lens_position_spinbox.clearFocus()

def on_continuous_af_toggled(checked):
    if checked:
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous,
                             "AfSpeed": controls.AfSpeedEnum.Fast,
                             "AfMetering" : controls.AfMeteringEnum.Windows,
                             "AfWindows" : [ (2104, 1046, 3800, 400) ]})
    else:
        picam2.set_controls({"AfMode": controls.AfModeEnum.Auto,
                             "AfSpeed": controls.AfSpeedEnum.Fast,
                             "AfMetering" : controls.AfMeteringEnum.Windows,
                             "AfWindows" : [ (2104, 1046, 3800, 400) ]})

SAVE_DIRECTORY = "/home/konos93/Desktop/camera/cam1"

def do_capture():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    filename = f"{SAVE_DIRECTORY}/bbb{timestamp}.jpg"
    cfg = picam2.create_still_configuration(buffer_count=3)
    picam2.switch_mode_and_capture_file(cfg, filename, signal_function=qpicamera2.signal_done)
    print(f"Image saved: {filename}")
    
def callback(job):
    global state
    if state == STATE_AF:
        state = STATE_CAPTURE
        success = "succeeded" if picam2.wait(job) else "failed"
        print(f"AF cycle {success} in {job.calls} frames")
        do_capture()
    else:
        picam2.wait(job)
        picam2.set_controls({"AfMode": controls.AfModeEnum.Auto,
                             "AfSpeed": controls.AfSpeedEnum.Fast,
                             "AfMetering" : controls.AfMeteringEnum.Windows,
                             "AfWindows" : [ (2104, 1046, 3800, 400) ]})
        button.setEnabled(True)
        manual_focus.setEnabled(True)
        af_checkbox.setEnabled(True)

def on_manual_toggled(checked):
    mode = controls.AfModeEnum.Continuous if checked else controls.AfModeEnum.Auto
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,
                         "LensPosition": lens_position_spinbox.value()})
        

def on_lens_position_changed(value):
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": value})

# Add an overlay to the camera preview when the checkbox is clicked
def on_overlay_checkbox_toggled(checked):
    global overlay
    if checked:
        qpicamera2.set_overlay(overlay)
    else:
        qpicamera2.set_overlay(None)

overlay_checkbox = QCheckBox("Show Overlay")
overlay_checkbox.setChecked(False)
overlay_checkbox.toggled.connect(on_overlay_checkbox_toggled)

# Define the overlay
overlay = np.zeros((300, 400, 4), dtype=np.uint8)
overlay[:150, 200:] = (255, 0, 0, 64)
overlay[150:, :200] = (0, 255, 0, 64)
overlay[150:, 200:] = (0, 0, 255, 64)    

window = QWidget()
bg_colour = window.palette().color(QPalette.Background).getRgb()[:3]
qpicamera2 = QGlPicamera2(picam2, width=preview_width, height=preview_height, bg_colour=bg_colour, keep_ar=True)
qpicamera2.done_signal.connect(callback, type=QtCore.Qt.QueuedConnection)

button = QPushButton("Click to capture JPEG")
button.clicked.connect(on_button_clicked)

continuous_af_checkbox = QCheckBox("Continuous AF")
continuous_af_checkbox.setChecked(False)
continuous_af_checkbox.toggled.connect(on_continuous_af_toggled)

label = QLabel()
af_checkbox = QCheckBox("AF before capture", checked=False)
manual_focus = QCheckBox("Manual Focus", checked=True)
manual_focus.toggled.connect(on_manual_toggled)

# Add a QDoubleSpinBox for adjusting lens position
lens_position_spinbox = QDoubleSpinBox()
lens_position_spinbox.setSingleStep(0.02)  # Adjust step size to 0.02
lens_position_spinbox.setMinimum(0)     # Set minimum value
lens_position_spinbox.setMaximum(10)    # Set maximum value
lens_position_spinbox.setFixedWidth(100)  # Set fixed width for smaller size
lens_position_spinbox.setValue(5.48)  # Set initial value to 5
lens_position_spinbox.valueChanged.connect(on_lens_position_changed)

window.setWindowTitle("cam1 App")

label.setFixedWidth(200)
label.setFixedHeight(50)
label.setAlignment(QtCore.Qt.AlignTop)
layout_h = QHBoxLayout()
layout_v = QVBoxLayout()
layout_v.addWidget(label)
layout_v.addWidget(manual_focus)
layout_v.addWidget(lens_position_spinbox)  # Add the lens position QDoubleSpinBox
layout_v.addWidget(af_checkbox)
layout_v.addWidget(continuous_af_checkbox)  # Add the continuous autofocus checkbox
layout_v.addWidget(overlay_checkbox)
layout_v.addWidget(button)
layout_h.addWidget(qpicamera2, 1)
layout_h.addLayout(layout_v, 2)
window.resize(1500, 460)
button.setFixedHeight(200)
button.setFixedWidth(200)

window.setLayout(layout_h)

picam2.start()
window.move(500, 560)
window.show()
app.exec()
picam2.stop()
