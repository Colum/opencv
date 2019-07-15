import numpy as np
import cv2
from edge_fill.fill import EdgeFiller

def read_frames():

    edge_filler = EdgeFiller()

    cap = cv2.VideoCapture('highway.mov') # todo video as arg

    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = edge_filler.process_frame(frame)

        cv2.imshow('Main', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

read_frames()
