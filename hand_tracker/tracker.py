import cv2
import numpy as np
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec

class HandTracker:
    def __init__(self, config):
        self.config = config
        self.lms_name: dict = config.tracker.landmarks_name

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
        self.hand_landmarks_list = None
        print('Hand tracker initialized')


    def _landmarks_to_list(self, landmarks):
        assert landmarks.landmark is not None
        return [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]


    def process_frame(self, frame: np.ndarray) -> None:
        assert frame is not None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        self.hand_landmarks =  results.multi_hand_landmarks

        if self.hand_landmarks:
            # ASSUMING THERE IS ONYL ONE HAND FOR NOW
            self.hand_landmarks_list = self._landmarks_to_list(self.hand_landmarks[0])
            self.current_barycenter = self.compute_barycenter(self.hand_landmarks_list)
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
        num_landmarks = len(landmarks)
        for lm in landmarks:
            x_sum += lm[0]
            y_sum += lm[1]
            z_sum += lm[2]
        return x_sum / num_landmarks, y_sum / num_landmarks, z_sum / num_landmarks


    def smooth_barycenter(self, previous: tuple, current: tuple, alpha: float=0.3) -> tuple:
        assert current is not None

        if previous is None:
            previous = current
        smoothed_barycenter = tuple(alpha * c + (1 - alpha) * p for c, p in zip(current, previous))
        return smoothed_barycenter


    def dist_between_lms(self, lm1_idx: int, lm2_idx: int) -> float:
        """
        Computes the euclidian distance between 2 landmarks among the x and y axis
        """
        lm1, lm2 = self.hand_landmarks_list[lm1_idx], self.hand_landmarks_list[lm2_idx]
        return np.linalg.norm(np.array(lm1[:2]) - np.array(lm2[:2]))


    def update_audio_params(self, audio_thread) -> None:
        if self.smoothed_barycenter is not None:

            finger_dist = self.dist_between_lms(self.lms_name['INDEX_FINGER_TIP'], self.lms_name['THUMB_TIP'])
            if finger_dist > 0.05:
                audio_thread.is_sound_on = False
                return

            normalized_height = 1 - self.smoothed_barycenter[1]
            normalized_width = self.smoothed_barycenter[0]

            # Map pitch to normalized width (C4 to C5)
            audio_thread.target_freq = 261.63 + normalized_width * (523.25 - 261.63)

            # Map volume to normalized height (0-1)
            audio_thread.target_volume = normalized_height

            audio_thread.is_sound_on = True
        else:
            audio_thread.is_sound_on = False
