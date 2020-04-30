
import driver
import threading


ready_flag = False
res = (1280, 720)
frame_rate = 90
centroid_x = -1

print("thread")
im_proc = threading.Thread(target=driver.image_processor, args=("R"), daemon=True)
print("starting movement")
im_proc.start()

driver.vehicle_control()

