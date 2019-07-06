#example of how to handle live streaming camera in flask
#taken from https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
#pip install opencv-python

import cv2
from base_camera import BaseCamera

class Camera(BaseCamera):
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
