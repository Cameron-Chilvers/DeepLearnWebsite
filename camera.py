import cv2
import numpy as np
import torch
from yolov5.detect import run
                
model = torch.hub.load('yolov5','custom', path='best.pt',force_reload=True,source='local')

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
#        self.video = cv2.resize(self.video,(840,640))
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()

        results = model(image)
        a = np.squeeze(results.render())

        # Encode the result image as JPEG
        ret, jpeg = cv2.imencode('.jpg', image)

        # Return the JPEG bytes
        return jpeg.tobytes()