import os
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = "libcamerasrc"

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        # GST_PIPELINE = f"libcamerasrc ! video/x-raw, width=1280, height=720, framerate=30/1 ! videoconvert ! videoscale ! video/x-raw, width=1280, height=720  ! appsink"
        GST_PIPELINE  =  f"libcamerasrc ! video/x-raw, width=1280, height=720, framerate=30/1 ! videoconvert ! videoscale ! clockoverlay time-format=\"%D %H:%M:%S\" !  appsink"

        camera = cv2.VideoCapture (GST_PIPELINE, cv2.CAP_GSTREAMER)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            # _, img = camera.read()

            yield bytes (cv2.imencode('.jpg', camera.read()[1])[1])

            # encode as a jpeg image and return it
            # yield cv2.imencode('.jpg', img)[1].tobytes()
        camera.release()
