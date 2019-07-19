import numpy as np
import cv2



class NonRoiMask:

    @staticmethod
    def process(frame):
        height = frame.shape[0]
        width = frame.shape[1]

        mask_ctr = int(height / 2 + 0.15 * height)

        region_of_interest_vertices = [(0, height), (width / 2, mask_ctr),(width, height),]
        vertices = np.array([region_of_interest_vertices], np.int32)

        mask = np.zeros_like(frame)
        match_mask_color = 255

        cv2.fillPoly(mask, vertices, match_mask_color)

        masked_image = cv2.bitwise_and(frame, mask)
        return masked_image, mask_ctr

    @staticmethod
    def add_mask_guideline(frame, mask_ctr):
        y = mask_ctr
        x = frame.shape[1] // 2
        radius = 5
        cv2.circle(frame, (x, y), radius, (245, 215, 66), -1)
        return frame
