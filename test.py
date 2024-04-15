from picamera2 import Picamera2
from libcamera import controls
import threading

def capture(cam, config, filename):
    cam.configure(config)
    cam.start()
    cam.capture_file(filename)
    cam.stop()

cam2 = Picamera2(1)

config2 = cam2.create_still_configuration(buffer_count=4)

# We are going to test LensPosition control, from 0.0 to 10.0, incrementing 0.5 everytime saving all
for i in range(0, 21):
    cam2.set_controls({"ExposureTime": 32680, "AnalogueGain": 6.78, "AfMode": controls.AfModeEnum.Manual, "LensPosition": i / 20})
    thread2 = threading.Thread(target=capture, args=(cam2, config2, f"demo2_{i}.jpg"))
    thread2.start()
    thread2.join()
#cam2.set_controls({"ExposureTime": 32680, "AnalogueGain": 6.78, "AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.5})
