import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys


class NonRoiMask:

    @staticmethod
    def process(frame):
        height = frame.shape[0]
        width = frame.shape[1]

        region_of_interest_vertices = [(0, height), (width / 2, height / 2 + 0.15 * height ),(width, height),]
        vertices = np.array([region_of_interest_vertices], np.int32)

        mask = np.zeros_like(frame)
        match_mask_color = 255

        cv2.fillPoly(mask, vertices, match_mask_color)

        masked_image = cv2.bitwise_and(frame, mask)
        return masked_image
