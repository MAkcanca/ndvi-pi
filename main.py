from picamera2 import Picamera2

# cam1 = Picamera2(0)
# cam2 = Picamera2(1)

# config1 = cam1.create_still_configuration()
# config2 = cam2.create_still_configuration()


# cam1.configure(config1)
# cam2.configure(config2)
# cam1.start()

# np_array = cam1.capture_array()
# cam1.capture_file("demo.jpg")
# cam1.stop()

# cam2.start()
# np_array = cam2.capture_array()
# cam2.capture_file("demo2.jpg")
# cam2.stop()

# Do this capture process in parallel
from picamera2 import Picamera2
from libcamera import controls
import threading

def capture(cam, config, filename):
    cam.configure(config)
    cam.start()
    cam.capture_file(filename)
    cam.stop()

cam1 = Picamera2(0)
cam2 = Picamera2(1)

config1 = cam1.create_still_configuration(buffer_count=4)
config2 = cam2.create_still_configuration(buffer_count=4)

cam1.set_controls({"ExposureTime": 240, "AnalogueGain": 1})
cam2.set_controls({"ExposureTime": 240, "AnalogueGain": 1})
thread1 = threading.Thread(target=capture, args=(cam1, config1, "left_image.jpg"))
thread2 = threading.Thread(target=capture, args=(cam2, config2, "right_image.jpg"))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
