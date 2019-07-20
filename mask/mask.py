import numpy as np
import cv2


class NonRoiMask:

    def __init__(self):
        self.ref_point = None
        self.frame = None

    def process(self, frame, og_frame):
        if self.ref_point is None:
            print('Click to select ref point, then press enter')
            self.frame = frame
            cv2.imshow('Main', og_frame)
            cv2.setMouseCallback('Main', self.select_ref_point)
            cv2.waitKey(0)

        height = frame.shape[0]
        width = frame.shape[1]

        region_of_interest_vertices = [(0, height), (self.ref_point[0], self.ref_point[1]), (width, height),]
        vertices = np.array([region_of_interest_vertices], np.int32)

        mask = np.zeros_like(frame)
        match_mask_color = 255

        cv2.fillPoly(mask, vertices, match_mask_color)

        masked_image = cv2.bitwise_and(frame, mask)
        return masked_image

    def add_mask_guideline(self, frame):
        y = self.ref_point[1]
        x = self.ref_point[0]
        radius = 10
        cv2.circle(frame, (x, y), radius, (245, 215, 66), -1)
        return frame

    def select_ref_point(self, event, x, y, flags, param):
        if self.ref_point is not None:
            return

        if event == cv2.EVENT_LBUTTONDOWN:
            self.ref_point = (x, y)


