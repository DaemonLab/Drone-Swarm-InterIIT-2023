import numpy as np
import time
from PlutoX.Camera.marker import Aruco
import cv2
# from PlutoX.Camera.ignore_poseEst import WebcamVideoStream

KPx, KPy, KPz, KPyaw = 0.01, 0.01, 200, 100
KIx, KIy, KIz, KIyaw = 0, 0, 0, 0
KDx, KDy, KDz, KDyaw = 0, 0, 0, 0



YAW_TARGET = 1.5708



def go_to(pose, target, Err, ErrI):
    """
    PID Control Loop
    """
    xError, yError, zError, yawError = Err
    xErrorI, yErrorI, zErrorI, yawErrorI = ErrI

    xTarget, yTarget, heightTarget = target



    xError_old = xError
    yError_old = yError
    zError_old = zError
    yawError_old = yawError

    x,   y,   z,   yaw = pose

    xError = xTarget-x
    yError = yTarget-y
    zError = heightTarget-z
    yawError = YAW_TARGET-yaw


    xErrorI += xError
    yErrorI += yError
    zErrorI += zError
    yawErrorI += yawError

    # compute derivative (variation) of errors (D)
    xErrorD = xError-xError_old
    yErrorD = yError-yError_old
    zErrorD = zError-zError_old
    yawErrorD = yawError-yawError_old

    # compute commands
    xCommand = KPx*xError + KIx*xErrorI + KDx*xErrorD
    yCommand = KPy*yError + KIy*yErrorI + KDy*yErrorD
    zCommand = KPz*zError + KIz*zErrorI + KDz*zErrorD
    yawCommand = KPyaw*yawError + KIyaw*yawErrorI + KDyaw*yawErrorD

    pitch_command = np.cos(yaw)*xCommand + np.sin(yaw)*yCommand

    roll_command = -(np.sin(yaw)*xCommand - np.cos(yaw)*yCommand)

    throttle_command = zCommand
    Err = [xError, yError, zError, yawError]
    ErrI = [xErrorI, yErrorI, zErrorI, yawErrorI]
    print(f"Yaw error: {yawError}")

    return roll_command, pitch_command, throttle_command, yawCommand, Err, ErrI


        # drone.trim(roll_command,pitch_command, throttle_command, yawCommand)

        # if np.linalg.norm(np.array([xError, yError]))<10 and abs(zError)<0.05:
        #     print("Target Reached. Landing ...")
        #     drone.land()
        #     drone.disarm()



