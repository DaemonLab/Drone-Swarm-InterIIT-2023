# Task 2

## Camera calibration
The camera used the task 2 is Lenovo 300 FHD Webcam with FHD 1080P 2.1 Megapixel CMOS Camera and an Ultra-Wide 95 Lens.

## Pose Estimation
The pose of the drone is obtained from the Aruco marker attached on the drone. The cv2.aruco library, available in the opencv-contrib-python package, is used to detect the drone and its pose, specifically it's x-y coordinates in pixels, height in meters and yaw in radians.



## PID control


## Running

To run the PID control task, run ``master.py`` which will further start two parallel processes for pose estimation and PID control.
