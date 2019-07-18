import numpy as np
import cv2
import math


class EdgeDetect:

    @staticmethod
    def process(frame):
        gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray_image, 200, 300)
        return edges
