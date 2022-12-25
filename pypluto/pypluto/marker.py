import cv2
import numpy as np
import math

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
        
    def display(self,corners, ids, rejected, image):
        _, w, _ = image.shape
        if len(corners) > 0:
            
            ids = ids.flatten()
            
            for (markerCorner, markerID) in zip(corners, ids):
                
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                topRight = np.array([int(topRight[0]), int(topRight[1])])
                bottomRight = np.array([int(bottomRight[0]), int(bottomRight[1])])
                bottomLeft = np.array([int(bottomLeft[0]), int(bottomLeft[1])])
                topLeft = np.array([int(topLeft[0]), int(topLeft[1])])

                cX,cY = (topRight + bottomLeft)//2
                hX,hY = (topLeft+topRight)//2

                cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                

                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                cv2.arrowedLine(image, (cX,cY), (hX,hY),(0, 0, 255))
                
                image = cv2.flip(image,1)
                cv2.putText(image, f"Drone ID: {markerID}",(w-topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                print("[Inference] ArUco marker ID: {}".format(markerID))
        else:
            image = cv2.flip(image,1)

        return image

    def get_pose(self,corners, ids, rejected, image, matrix_coefficients, distortion_coefficients):
        
        #matrix_coefficients - Intrinsic matrix of the calibrated camera
        #distortion_coefficients - Distortion coefficients associated with our camera

        is_detected = False
        pose_r_t_dict = {} 
        If you have multiple markers, you could use cv::aruco::estimatePoseSingleMarkers that will solve this instability in the solution

        
        #prev method
        if len(corners) > 0:
            
            
            for (markerCorner, markerID) in zip(corners, ids):
                
                # to get z dist in tvec --------------
                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[markerID], 0.02, matrix_coefficients,
                                                                       distortion_coefficients)
                
                #-----------------------------
                
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                topRight = np.array([int(topRight[0]), int(topRight[1])])
                bottomRight = np.array([int(bottomRight[0]), int(bottomRight[1])])
                bottomLeft = np.array([int(bottomLeft[0]), int(bottomLeft[1])])
                topLeft = np.array([int(topLeft[0]), int(topLeft[1])])

                cX, cY = int((topRight + bottomLeft)/2)
                hX, hY = int((topLeft+topRight)/2)
                tX, tY = hX-cX, hY-cY
                yaw = np.arctan2(tY, tX) 
                pose = np.array([cX,cY,tvec[2] , yaw])      #mostly idx 2 is for z 
                is_detected = True
                
        return pose, is_detected



if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    while cap.isOpened():
        
        ret, image = cap.read()
        

        aruco = Aruco("DICT_5X5_50")

        corners, ids, rejected = aruco.detectMarkers(image)

        detected_markers = aruco.display(corners, ids, rejected, image)

        cv2.imshow("Image", detected_markers)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    cap.release()
