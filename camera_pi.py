#!/usr/bin/python3 

import io
import simplejpeg
import time
import picamera2
import null_preview
from base_camera import BaseCamera


class Camera(BaseCamera):
    @staticmethod
    def frames():
            camera = picamera2.Picamera2()
            preview = null_preview.NullPreview(camera)
            camera.configure(camera.preview_configuration(main={"size": (640, 480)}))

            camera.start()
            output_buffer = io.BytesIO()

            while True:
                  array = camera.capture_array()
                  buf = simplejpeg.encode_jpeg (array, colorspace='BGRX')

                  output_buffer.seek(0)
                  output_buffer.write(buf)

                  yield  output_buffer.getvalue()

                  output_buffer.seek(0)
                  output_buffer.truncate()


