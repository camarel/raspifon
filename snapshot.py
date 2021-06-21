import cv2
from io import BytesIO

class Snapshot:
    image_width  = 1280
    image_height = 720

    def __init__(self, camera_port):
        self.camera_port = int(camera_port)

    def takePicture(self):
        camera = cv2.VideoCapture(self.camera_port)

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)
        camera.set(cv2.CAP_PROP_SATURATION, 50.0)

        cv2.setUseOptimized(True)

        return_value, image = camera.read()

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        imbytes = cv2.imencode('.jpg', image, encode_param)[1].tobytes()

        return imbytes

