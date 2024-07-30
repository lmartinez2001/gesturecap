import cv2
import numpy as np
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec

class HandTracker:
    def __init__(self, config):
        self.config = config
        self.lms: dict = config.tracker.landmarks_name

        # Initialize mediapipe backend
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=config.tracker.n_hands,
            min_detection_confidence=config.tracker.detection_confidence
        )

        # Keep track of the true barycenter and the smoothed (previous) one for exponential smoothing
        self.current_barycenter = None
        self.smoothed_barycenter = None

        # Keep track of the current landmarks position
        self.hand_landmarks = None
        print('Hand tracker initialized')


    def process_frame(self, frame: np.ndarray) -> None:
        assert frame is not None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.hand_landmarks = self.hands.process(frame_rgb).multi_hand_landmarks

        if self.hand_landmarks:
            # For now only handles one hand
            self.current_barycenter = self.compute_barycenter(self.hand_landmarks[0])
            self.smoothed_barycenter = self.smooth_barycenter(
                previous=self.smoothed_barycenter,
                current=self.current_barycenter,
                alpha=self.config.tracker.alpha_barycenter)
        else:
            self.current_barycenter = None
            self.smoothed_barycenter = None


    def compute_barycenter(self, landmarks) -> tuple:
        assert landmarks is not None

        x_sum, y_sum, z_sum = 0, 0, 0
        num_landmarks = len(landmarks.landmark)
        for lm in landmarks.landmark:
            x_sum += lm.x
            y_sum += lm.y
            z_sum += lm.z
        return x_sum / num_landmarks, y_sum / num_landmarks, z_sum / num_landmarks


    def smooth_barycenter(self, previous: tuple, current: tuple, alpha: float=0.3) -> tuple:
        assert current is not None

        if previous is None:
            previous = current
        smoothed_barycenter = tuple(alpha * c + (1 - alpha) * p for c, p in zip(current, previous))
        return smoothed_barycenter


    def dist_between_lms(self, lm1_idx: int, lm2_idx: int) -> float:
        lm1, lm2 = self.hand_landmarks[0][lm1_idx], self.hand_landmarks[0][lm2_idx]
        return np.linalg.norm(np.array(lm1)[:-1] - np.array(lm2)[:-1])


    def update_audio_params(self, audio_thread) -> None:
        if self.smoothed_barycenter is not None:
            print(self.dist_between_lms(self.lms['INDEX_FINGER_TIP'], self.lms['THUMB_TIP']))
            normalized_height = 1 - self.smoothed_barycenter[1]
            normalized_width = self.smoothed_barycenter[0]

            # Map pitch to normalized width (C4 to C5)
            audio_thread.target_freq = 261.63 + normalized_width * (523.25 - 261.63)

            # Map volume to normalized height (0-1)
            audio_thread.target_volume = normalized_height

            audio_thread.is_sound_on = True
        else:
            audio_thread.is_sound_on = False
