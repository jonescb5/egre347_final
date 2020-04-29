import image_processing
import driver
import threading


res = (1280, 720)
frame_rate = 90
centroid_x = -1

print("thread")
im_proc = threading.Thread(target=image_processing.image_processing, daemon=True)
print("starting movement")
im_proc.start()

driver.vehicle_control()

