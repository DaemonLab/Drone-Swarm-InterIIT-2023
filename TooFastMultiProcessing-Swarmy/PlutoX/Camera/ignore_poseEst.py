


# import the necessary packages
from threading import Thread
import cv2
from PlutoX.Camera.marker import *
# import matplotlib.pyplot as plt

# size of the frames
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
        (self.grabbed, self.frame) = self.stream.read()
        self.aruco = Aruco("DICT_4X4_50")
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    # def start(self):
    #     # start the thread to read frames from the video stream
    #     Thread(target=self.update, args=(), daemon=False).start()
    #     return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read_pose(self):
        # return the frame most recently read
        corners, ids, _ = self.aruco.detectMarkers(self.frame)
        pose, is_detected, detected_markers = self.aruco.get_pose(corners, ids, self.frame, [550,192], display=True)
        return pose, detected_markers #self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


# def poseMain():

# # if __name__ == "__main__":
#     path = []
#     # fig = plt.figure()
#     # ax = fig.add_subplot(1,1,1, projection='3d')
#     camera = WebcamVideoStream(src=0) #.start()
    
#     while camera.stream.isOpened():
#         pose, image = camera.read_pose()
#         if pose is not None:
#             path.append(pose)
#             print(path)
#             patht = np.array(path).T
#             ax.plot(patht[0], patht[1], patht[2])
#             ax.set_zlabel("Z")
#             ax.set_ylabel("Y")
#             ax.set_xlabel("X")
#             plt.pause(0.01)
#         print(f"Pose: {pose}")
#         # cv2.imshow("Image", image)
        
