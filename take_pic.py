import time
import picamera
import picamera.array
import cv2
import image_processing

res = (1280, 720)

proc_check = True
col = "R"

cam = picamera.PiCamera()
cam.resolution = res
cam.framerate = 90
cap = picamera.array.PiRGBArray(cam, size=res)
# create references to the capture array and capture stream
cam.start_preview()
# wait for camera to warm up
time.sleep(2.0)


for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):
    image = frame.array  # capture a frame
    if proc_check:
        image_mask = image_processing.preprocess(image, col)
        centroid = image_processing.find_centroid(image, col)
        print(centroid)
        cv2.circle(image, centroid, 5, (0, 255, 0), 1)
        cv2.imwrite('cent_image_' + col + '.jpg', image)
        cv2.imwrite('image_mask_' + col + '.jpg', image_mask)

    cv2.imwrite('image.jpg', image)
    cap.truncate(0)  # reset capture array size to zero. effectively clears the array
    break

