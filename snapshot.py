# This file is inspired by

import time
import cv2
import os


class Snapshot:
    camera_port = 0
    directory   = r'./pictures' # directory to save the files


    def __init__(self):
        self.camera = cv2.VideoCapture(self.camera_port)
        
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        cv2.setUseOptimized(True) 


    def takePicture(self):
        print('take')
        return_value, image = self.camera.read()

        if os.path.exists(self.directory):
            n_files = len(os.listdir(self.directory))
            file_jpg = os.path.join(self.directory, 'picture-{}.jpg'.format(n_files))
            cv2.imwrite(file_jpg, image)
            print('Snapshot taken: {}'.format(file_jpg))
            return file_jpg

        else:
            print('please create directory to write audio: {}'.format(self.directory))

        return None


