# Save multiple photos with half a second interval, around 10 photos, save to left/ folder

# from picamera2 import Picamera2
# from time import sleep
# cam1 = Picamera2(1)

# config1 = cam1.create_still_configuration(buffer_count=2)
# cam1.configure(config1)
# cam1.start()

# for i in range(10):
#     cam1.capture_file(f"right/{i}.jpg")
#     sleep(0.5)

# cam1.stop()
import threading
from picamera2 import Picamera2
from time import sleep

def capture(cam, config, filename):
    cam.configure(config)
    cam.start()
    cam.capture_file(filename)
    cam.stop()

cam1 = Picamera2(0)
cam2 = Picamera2(1)

config1 = cam1.create_still_configuration(buffer_count=2)
config2 = cam2.create_still_configuration(buffer_count=2)
cam2.set_controls({"ExposureTime": 32680, "AnalogueGain": 6.78})
sleep(5)
# Now we capture the images in parallel
for i in range(5):
    print(f"Capturing {i} in 2 seconds")
    sleep(2)
    thread1 = threading.Thread(target=capture, args=(cam1, config1, f"left/{i}.jpg"))
    thread2 = threading.Thread(target=capture, args=(cam2, config2, f"right/{i}.jpg"))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    sleep(1)