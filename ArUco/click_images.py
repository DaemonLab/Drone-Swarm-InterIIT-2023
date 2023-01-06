import cv2
import time

cap = cv2.VideoCapture(2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

for i in range(50):
    _, img = cap.read()
    time.sleep(5)
    cv2.imshow('img', img)
    cv2.imwrite(f'/home/kshitij/interiit/Drone-Swarm/pypluto/pypluto/ArUco/calibration_checkerboard/img{50+i}.jpg', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
