import cv2
import numpy as np
import math
import time
# from 

CAMERA_HEIGHT = 1.9 #m

#matrix_coefficients - Intrinsic matrix of the calibrated camera
MATRIX_COEFFICIENTS = np.array([[
            1447.9804004365824,
            0.0,
            617.3063266183908
        ],
        [
            0.0,
            1448.4116664252433,
            289.02239681156016
        ],
        [
            0.0,
            0.0,
            1.0
        ]])

#distortion_coefficients - Distortion coefficients associated with our camera
DISTORTION_COEFFICIENTS = np.array([
            0.0397515407032859,
            1.259291585298002,
            -0.010631456171277863,
            -0.00784841820297665,
            -5.925444820936321
        ])
    

class Aruco:

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    def __init__(self, arucoType):
        self.arucoType = arucoType
        self.arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT[self.arucoType])
        self.arucoParams = cv2.aruco.DetectorParameters_create()

    def detectMarkers(self,img):
        #don't we need to use a gray img here? remember to change inputs to gray_img
        #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)
        #cornersm, ids, rejected_img_points

    def get_pose(self, corners, ids, image, desiredVec, display=True):

        is_detected = False
        pose = None
        # print(f"corners, {corners} IDs: {ids}")
        
        if len(corners) > 0:
            
            
            for (markerCorner, markerID) in zip(corners, ids):
                try:
                    rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(np.array(corners[0]), 0.02, cameraMatrix=MATRIX_COEFFICIENTS, distCoeffs=DISTORTION_COEFFICIENTS)
                except cv2.error:
                    print("Pose Est error")
                    return pose, is_detected, image

                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                topRight = np.array([int(topRight[0]), int(topRight[1])])
                bottomRight = np.array([int(bottomRight[0]), int(bottomRight[1])])
                bottomLeft = np.array([int(bottomLeft[0]), int(bottomLeft[1])])
                topLeft = np.array([int(topLeft[0]), int(topLeft[1])])

                cX, cY = (topLeft + bottomRight)//2
                hX, hY = (topLeft + topRight)//2
                tX, tY = hX-cX, hY-cY
                yaw = np.arctan2(tY, tX) 
                # yaw = np.rad2deg(yaw)

                drone_height = CAMERA_HEIGHT - tvec[0,0,2]

                pose = np.array([cX,cY, drone_height,yaw]) 
                is_detected = True
                if display:
                    cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                    

                    cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                    
                    cv2.arrowedLine(image, (cX,cY), (hX,hY),(0, 0, 255))
                    
                    # image = cv2.flip(image,1)
                    cv2.putText(image, f"Drone ID: {markerID} Height: {drone_height}",(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
                    # print("[Inference] ArUco marker ID: {}".format(markerID))
            
        if display:
                dX,dY = desiredVec
                cv2.circle(image, (dX, dY), 7, (255, 0, 0), -1)
                    

                
        return pose, is_detected, image



'''Uncomment only RED commented part below for making camera work'''
def markerMainSender(connCam):  #connCam
# if __name__ == "__main__":
    cap = cv2.VideoCapture(0)   
    start = time.time()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    aruco_obj = Aruco("DICT_4X4_50")
    i = 0 
    while cap.isOpened(): #basically while true case 
    # while True:
    
        now = time.time()
        delay = now-start

        ret, image = cap.read()        
        # print(f"\n-------putting val {i}--{pose}--at time:{delay} --")
        
        

        corners, ids, rejected = aruco_obj.detectMarkers(image)
        # detected_markers = (corners, ids, image, [550,192])

        pose, is_detected, detected_markers = aruco_obj.get_pose(corners, ids, image, [550,192], display=True)
        # cv2.imshow("Image", detected_markers)
        # cv2.imshow("Img", image)

        print(f"\n{i}--From Marker - Pose: {pose}")
        connCam.send(pose)
        i+=1

        time.sleep(0.01)

        # key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break

    cv2.destroyAllWindows()
    cap.release()

