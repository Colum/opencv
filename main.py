import numpy as np
import cv2
from edge.edge import EdgeDetect
from mask.mask import NonRoiMask
from lane.lane import LaneDetect

def read_frames():

    edge_detect = EdgeDetect()
    mask = NonRoiMask()
    lane = LaneDetect()

    cap = cv2.VideoCapture('data/car5.mp4') # todo video as arg

    while(cap.isOpened()):
        ret, frame = cap.read()
        og_frame = np.copy(frame)

        frame = edge_detect.process(frame)
        frame, mask_ctr = mask.process(frame)
        frame = lane.process(frame, og_frame)
        frame = mask.add_mask_guideline(frame, mask_ctr)

        cv2.imshow('Main', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

read_frames()
