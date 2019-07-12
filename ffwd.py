import numpy as np
import cv2
from random import randint, randrange
import sys

def mix(c):
    rand_c = c + randrange(40)
    c = (c + rand_c)
    if r > 255:
        return rand_c
    return c

def createTrackerByName(trackerType):
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

def rand_color():
    r = randrange(255)
    g = randrange(255)
    b = randrange(255)
    return [r, g, b]

cap = cv2.VideoCapture('highway.mov')

r = 0
g = 0
b = 0

bboxes = []
colors = []

ret, frame = cap.read()
box = cv2.selectROI('Tracker', frame)
bboxes.append(box)
colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))


multiTracker = cv2.MultiTracker_create()
for bbox in bboxes:
  multiTracker.add(createTrackerByName('CSRT'), frame, bbox)

while(cap.isOpened()):
    ret, frame = cap.read()
    success, boxes = multiTracker.update(frame)

    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        # cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        left_x = int(newbox[0]) # x1 value
        right_x = int(newbox[0] + newbox[2]) # x2 value

        top_y = int(newbox[1]) # y1 value
        bottom_y = int(newbox[1] + newbox[3]) # y2 value

        tracking = frame[top_y:bottom_y, left_x:right_x]
        edges = cv2.Canny(tracking, 100, 200)

        for i, row in enumerate(edges):
            for j, pixel in enumerate(row):
                if pixel == 255:
                    print('i: ' + str(i) + ', j:' + str(j))
                    print('left x:' + str(left_x) + ', bottom_y: ' + str(bottom_y))
                    frame[top_y + i, left_x + j] = rand_color()

        cv2.imshow('Edges', edges)


    cv2.imshow('Tracker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



def other():
    conv_hsv_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, mask = cv2.threshold(conv_hsv_gray, 40, 255, cv2.THRESH_BINARY_INV)
    ret2, mask2 = cv2.threshold(conv_hsv_gray, 30, 254, cv2.THRESH_BINARY_INV)
    ret3, mask3 = cv2.threshold(conv_hsv_gray, 20, 253, cv2.THRESH_BINARY_INV)

    r = mix(r)
    g = mix(g)
    b = mix(b)
    frame[mask == 255] = [r, g, b]

    r = mix(r)
    g = mix(g)
    b = mix(b)
    frame[mask2 == 254] = [r, g, b]

    r = mix(r)
    g = mix(g)
    b = mix(b)
    frame[mask3 == 253] = [r, g, b]
