import numpy as np
import cv2
import math


class LaneDetect:

    @staticmethod
    def process(frame, og_frame):
        lines = cv2.HoughLinesP(frame, rho=6, theta=np.pi / 60,
            threshold=160, lines=np.array([]), minLineLength=40,
            maxLineGap=25)

        left_line_x = []
        left_line_y = []
        right_line_x = []
        right_line_y = []

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == x2:
                    continue

                slope = (y2 - y1) / (x2 - x1)
                if math.fabs(slope) < 0.5:
                    continue

                if slope <= 0:
                    left_line_x.extend([x1, x2])
                    left_line_y.extend([y1, y2])
                else:
                    right_line_x.extend([x1, x2])
                    right_line_y.extend([y1, y2])

        left_lane = LaneDetect.calculate_line(frame, left_line_y, left_line_x)
        right_lane = LaneDetect.calculate_line(frame, right_line_y, right_line_x)
        both_lanes = cv2.addWeighted(left_lane, 1, right_lane, 1.0, 0.0)

        lanes_rgb = cv2.cvtColor(both_lanes, cv2.COLOR_GRAY2RGB)
        og_frame_with_lanes = cv2.addWeighted(lanes_rgb, 1, og_frame, 1.0, 0.0)

        return og_frame_with_lanes

    @staticmethod
    def calculate_line(frame, line_y, line_x):

        if len(line_x) == 0 or len(line_y) == 0:
            return np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8,)

        min_y = frame.shape[0] * (3 / 5) # shape[0] is frame height
        max_y = frame.shape[0]

        poly_line = np.poly1d(np.polyfit(line_y, line_x, deg=1))

        line_start = int(poly_line(max_y))
        line_end = int(poly_line(min_y))

        line = [int(line_start), int(max_y), int(line_end), int(min_y)]
        line_image = LaneDetect.draw_line(frame, line)
        return line_image


    @staticmethod
    def draw_line(frame, line, color=[255, 0, 0], thickness=3):
        if line is None:
            return
        frame_cp = np.copy(frame)
        line_image = np.zeros((frame_cp.shape[0], frame_cp.shape[1]), dtype=np.uint8,)

        x1, y1, x2, y2 = line
        cv2.line(line_image, (x1, y1), (x2, y2), color, thickness)
        return line_image
