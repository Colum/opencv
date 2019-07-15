import numpy as np
import cv2
from random import randint, randrange
import sys


class EdgeFiller:

    def __init__(self):
        self.tracker = self.createTrackerByName('CSRT')
        self.poi_selected = False
        self.bounding_boxes = [] # for multiple trackers
        self.bounding_boxes_colors = []
        self.multi_tracker = cv2.MultiTracker_create()


    def process_frame(self, frame):
        if not self.poi_selected:
            box = cv2.selectROI('Tracker', frame)
            self.bounding_boxes.append(box)
            self.bounding_boxes_colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            self.poi_selected = True

            for bbox in self.bounding_boxes:
                self.multi_tracker.add(self.tracker, frame, bbox)

        success, boxes = self.multi_tracker.update(frame)

        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, self.bounding_boxes_colors[i], 2, 1) # draw box around tracked frame

            left_x = int(newbox[0]) # x1 value
            right_x = int(newbox[0] + newbox[2]) # x2 value

            top_y = int(newbox[1]) # y1 value
            bottom_y = int(newbox[1] + newbox[3]) # y2 value

            tracking = frame[top_y:bottom_y, left_x:right_x]
            edges = cv2.Canny(tracking, 100, 200) # do edge detection inside tracked frame
            # self.fill_from_center(edges, frame)

            for i, row in enumerate(edges):
                for j, pixel in enumerate(row):
                    if pixel == 255:
                        frame[top_y + i, left_x + j] = [255, 255, 255]
                        pass

            cv2.imshow('Edges', edges)
            return frame

    def fill_from_center(self, edge_frame, frame):
        edge_frame_width = len(edge_frame[0])
        edge_frame_height = len(edge_frame)

        edge_frame_center_width = edge_frame_width // 2
        edge_frame_center_height = edge_frame_height // 2

        self.flood_fill_recursive(edge_frame_center_width, edge_frame_center_height, edge_frame)

    def flood_fill_recursive(self, width_pos, height_pos, frame):
        pass




    def createTrackerByName(self, trackerType):
      # Create a tracker based on tracker name
      trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
      if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
      elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
      elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
      elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
      elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
      elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
      elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
      elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
      else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
          print(t)

      return tracker
