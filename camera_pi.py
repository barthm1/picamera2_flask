#!/usr/bin/python3 

import io
import simplejpeg
import time
from picamera2.picamera2 import *
from base_camera import BaseCamera


class Camera(BaseCamera):
    @staticmethod
    def frames():
            camera = Picamera2()
            config = camera.preview_configuration(main={"size": (640, 480)})
            camera.configure(config) 
            
            camera.start_preview (Preview.NULL)
            camera.start()
            output_buffer = io.BytesIO()

            while True:
                  array = camera.capture_array()
                  buf = simplejpeg.encode_jpeg (array, colorspace='RGBX')

                  output_buffer.seek(0)
                  output_buffer.write(buf)

                  yield  output_buffer.getvalue()

                  output_buffer.seek(0)
                  output_buffer.truncate()
            camera.stop_preview(Preview.NULL)
            camera.stop()




