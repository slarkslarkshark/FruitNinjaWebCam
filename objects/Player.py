import cv2
import mediapipe as mp

from threading import Thread, Lock
from config import Config as cfg
import cv2
import mediapipe as mp


class Player:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.lock = Lock()
        self.current_frame = None
        self.finger_pos = None
        self.running = True
        self.thread = Thread(target=self._update_frame, daemon=True)
        self.thread.start()

    def _update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = cv2.resize(frame, (cfg.WIDTH, cfg.HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame)

            finger_pos = None
            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    x = int(hand.landmark[8].x * frame.shape[1])
                    y = int(hand.landmark[8].y * frame.shape[0])
                    finger_pos = (x, y)
                    cv2.circle(frame, finger_pos, 4, (0, 255, 0), -1)

            with self.lock:
                self.current_frame = frame.copy()
                self.finger_pos = finger_pos

    def get_frame(self):
        with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None

    def get_finger_position(self):
        with self.lock:
            return self.finger_pos

    def release(self):
        self.running = False
        self.cap.release()
        self.finger_pos = None
        self.thread.join()
