"""rasperry 5 two camera module v3"""
import keyboard
from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from libcamera import controls
import os

def capture_image(picam2, filename_prefix):
    # Record the start time
    start_time = time.time()

    # Capture an image
    timeStamp = datetime.now().strftime("%Y%m%d-%H%M%S.%f")[:-4]
    filename = f"{filename_prefix}_img_{timeStamp}.jpg"

    request = picam2.capture_request(flush=False)
    request.save('main', filename)
    request.release()

    # Get the size of the captured image in bytes
    file_size_bytes = os.path.getsize(filename)

    # Convert the file size to megabytes
    file_size_mb = file_size_bytes / (1024 ** 2)

    # Record the end time
    end_time = time.time()

    # Calculate and print the time taken and the size of the image in megabytes
    capture_time = end_time - start_time

    print(f"Image captured: {filename}, Time taken: {capture_time:.2f} seconds, Size: {file_size_mb:.2f} MB")

# Set up the first camera
picam1 = Picamera2(1)
config1 = picam1.create_still_configuration(buffer_count=3)
picam1.configure(config1)
picam1.start_preview(Preview.QTGL)
preview_config1 = picam1.create_preview_configuration({"size": (4096, 2592)})
picam1.configure(preview_config1)
picam1.start()
picam1.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#picam1.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 4.7}) #use first app_full.py to check the focus
# change the lens potition and choose the one that have the most mb in thepage u capture

# Set up the second camera
picam2 = Picamera2(0)
config2 = picam2.create_still_configuration(buffer_count=3)
picam2.configure(config2)
picam2.start_preview(Preview.QTGL)
preview_config2 = picam2.create_preview_configuration({"size": (4096, 2592)})
picam2.configure(preview_config2)
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 4.7}) #use first app_full.py to check the focus
# change the lens potition and choose the one that have the most mb in thepage u capture

try:
    while True:
        # Wait for the space key to be pressed
        keyboard.wait("space")

        # Capture images from both cameras
        capture_image(picam1, "y")
        capture_image(picam2, "x")

except KeyboardInterrupt:
    pass
finally:
    # Close QtGL preview windows
    picam1.stop_preview()
    picam2.stop_preview()
    
    # Clean up both cameras
    picam1.stop()
    picam2.stop()
