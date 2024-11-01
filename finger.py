import cv2
import mediapipe as mp
import numpy as np
from collections import deque

def curve_len(points):
    if len(points) == 0 or len(points) == 1:
        return 0
    
    total_len = 0
    x0, y0 = points[0]
    for i in range(1, len(points)):
        x1, y1 =  points[i]
        total_len += np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
        x0, y0 = x1, y1
    return total_len

def narrow_curve(points, thr):
    new_points = points
    while curve_len(new_points) > thr:
        for i in range(len(new_points) - 1, 0, -1):
            x0 = new_points[i][0]
            y0 = new_points[i][1]
            x1 = new_points[i - 1][0]
            y1 = new_points[i - 1][1]
            x_new = min(x0, x1) + (max(x0, x1) - min(x0, x1)) // 2
            y_new = min(y0, y1) + (max(y0, y1) - min(y0, y1)) // 2
            new_points[i] = (x_new, y_new)
    return new_points


class FingerCatcher:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.hand_track = deque()
    
    def find_finger(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if len(self.hand_track) >= 4:
            self.hand_track.pop()
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                w, h, _ = img.shape
                x, y = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
                self.hand_track.appendleft((x, y))
                self.hand_track = narrow_curve(self.hand_track, 40)
        else:
            self.hand_track.clear()
        return self.hand_track
