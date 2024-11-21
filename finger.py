import cv2
import mediapipe as mp
from characters import Player

class FingerCatcher:
    def __init__(self, CAMWIDTH, CAMHEIGHT, WIDTH, HEIGHT):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.hand_track = Player(CAMWIDTH, CAMHEIGHT, WIDTH, HEIGHT)
        
    def find_finger(self, img):
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        
        if results.multi_hand_landmarks:
            self.hand_track.pop()
            for hand in results.multi_hand_landmarks:
                x, y = hand.landmark[8].x, hand.landmark[8].y
                self.hand_track.update(x, y)
        else:
            self.hand_track.pop(isDetected=False)
        return self.hand_track
