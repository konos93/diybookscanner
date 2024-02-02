"""rasperry 5 one camera module v3"""
import keyboard
from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from libcamera import controls
import os

picam2 = Picamera2()
config = picam2.create_still_configuration(buffer_count=3)
picam2.configure(config)   
picam2.start_preview(Preview.QTGL)
preview_config = picam2.create_preview_configuration({"size": (4096, 2592)})
picam2.configure(preview_config)

picam2.start()


picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous })
#picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 4.7}) #use first app_full.py to check the focus



try:
    while True:
       
        # Wait for the space key to be pressed
        keyboard.wait("space")

        
        # Record the start time
        start_time = time.time()

        # Capture an image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"z_img_{timestamp}.jpg"

        request = picam2.capture_request(flush=False  )
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

except KeyboardInterrupt:
    pass
finally:
    # Clean up
    picam2.stop()
