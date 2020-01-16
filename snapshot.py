import cv2
from io import BytesIO

class Snapshot:
    camera_port  = 0
    image_width  = 1280
    image_height = 720

    def __init__(self):
        self.camera = cv2.VideoCapture(self.camera_port)
        
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)
        
        cv2.setUseOptimized(True) 


    def takePicture(self):
        print('taking picture')
        return_value, image = self.camera.read()

        is_success, imbuffer = cv2.imencode(".jpg", image)
        io_buf = BytesIO(imbuffer)
        io_buf.seek(0)

        return io_buf

