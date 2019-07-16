import numpy as np
import cv2
import math


class LaneDetect:

    @staticmethod
    def process(frame):
        gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray_image, 200, 300)

        lines = cv2.HoughLinesP(
            edges,
            rho=6,
            theta=np.pi / 60,
            threshold=160,
            lines=np.array([]),
            minLineLength=10,
            maxLineGap=20
            )
        line_image = LaneDetect.detect_lanes(frame, lines)
        return line_image

    @staticmethod
    def draw_lines(img, lines, color=[255, 0, 0], thickness=3):

        if lines is None:
            return

        img = np.copy(img)
        line_img = np.zeros(
            (
                img.shape[0],
                img.shape[1],
                3
            ),
            dtype=np.uint8,
        )    # Loop over all lines and draw them on the blank image.
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

        img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)    # Return the modified image.
        return img

    @staticmethod
    def detect_lanes(frame, lines, color=[255, 0, 0], thickness=3):
        if lines is None:
            return

        left_line_x = []
        left_line_y = []
        right_line_x = []
        right_line_y = []
        img = np.copy(frame)

        line_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8,)
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


        min_y = frame.shape[0] * (3 / 5) # <-- Just below the horizon
        max_y = frame.shape[0] # <-- The bottom of the image

        poly_left = np.poly1d(np.polyfit(
            left_line_y,
            left_line_x,
            deg=1
        ))

        left_x_start = int(poly_left(max_y))
        left_x_end = int(poly_left(min_y))
        poly_right = np.poly1d(np.polyfit(
            right_line_y,
            right_line_x,
            deg=1
        ))
        right_x_start = int(poly_right(max_y))
        right_x_end = int(poly_right(min_y))
        line_image = LaneDetect.draw_lines(
            frame,
            [[
                [left_x_start, max_y, left_x_end, min_y],
                [right_x_start, max_y, right_x_end, min_y],
            ]],
            thickness=5,
        )
        return line_image
