# Overview

This project performs simple lane detection on videos filmed from dashcams. Video files are processed and lines are drawn on the video where the lanes are perceived to be.
The object of this codebase is the explore the possibilities of opencv2.

### Method
The video is read frame-by-frame, and passed through a pipeline:

1. Run Canny edge detection on a gray scale image of the frame.
2. Mask the upper half of the screen, in order to reduce 'noise' to our lane detection.
3. Produce lines (y = mx + c) which correspond to the edges using Hough Line transform.
4. Find an average of all the lines to produced in 3. to produce a larger line which represents the interpreted lane.

### Issues

Algorithm is not sophisticated enough to draw turns (lane markings are curved).

The dash cam footage is subject to being recorded from different angles since the camera is internally mounted, and might move between recordings.
A calibration feature has been added to allow the mask to be properly applied. This indicator is represented by a blue dot.

![](https://github.com/Colum/opencv/blob/master/data/sample.gif)