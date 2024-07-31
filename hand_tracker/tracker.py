import cv2
import numpy as np
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
from mediapipe.python.solutions.drawing_utils import DrawingSpec

class HandTracker:
    def __init__(self, config):
        self.config = config
        self.lms_name: dict = config.tracker.landmarks_name
        # self.notes: dict = config.audio.note_frequencies

        # Initialize mediapipe backend
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=config.tracker.n_hands,
            min_detection_confidence=config.tracker.detection_confidence
        )
        #
        # Keep track of the true barycenter and the smoothed (previous) one for exponential smoothing
        self._reset_tracking_parameters()
        print('Hand tracker initialized')


    def _landmarks_to_list(self, landmarks) -> list:
        assert landmarks.landmark is not None
        return [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]


    def _empty_hand_dict(self) -> dict:
        return {'Left': None, 'Right': None}


    def _extract_handedness_label(self, handedness) -> str:
        return MessageToDict(handedness)['classification'][0]['label']


    def _reset_tracking_parameters(self) -> None:
        self.current_barycenter = self._empty_hand_dict()
        self.smoothed_barycenter = self._empty_hand_dict()
        self.hand_landmarks = self._empty_hand_dict()
        self.hand_landmarks_list = self._empty_hand_dict()


    def process_frame(self, frame: np.ndarray) -> None:
        assert frame is not None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        self._reset_tracking_parameters()

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                handedness_label = self._extract_handedness_label(handedness)

                self.hand_landmarks[handedness_label] = hand_landmarks

                self.hand_landmarks_list[handedness_label] = self._landmarks_to_list(hand_landmarks)

                self.current_barycenter[handedness_label] = self.compute_barycenter(self.hand_landmarks_list[handedness_label])
                self.smoothed_barycenter[handedness_label] = self.smooth_barycenter(
                    previous=self.smoothed_barycenter[handedness_label],
                    current=self.current_barycenter[handedness_label],
                    alpha=self.config.tracker.alpha_barycenter
                )

           
    def compute_barycenter(self, landmarks) -> tuple:
        assert landmarks is not None
        x_sum, y_sum, z_sum = 0, 0, 0
        num_landmarks = len(landmarks)
        for lm in landmarks:
            x_sum += lm[0]
            y_sum += lm[1]
            z_sum += lm[2]
        return x_sum / num_landmarks, y_sum / num_landmarks, z_sum / num_landmarks


    def smooth_barycenter(self, previous: tuple, current: tuple, alpha: float) -> tuple:
        assert current is not None

        if previous is None:
            previous = current
        smoothed_barycenter = tuple(alpha * c + (1 - alpha) * p for c, p in zip(current, previous))
        return smoothed_barycenter


    def dist_between_lms(self, lm1_idx: int, lm2_idx: int, hand: str) -> float:
        """
        Computes the euclidian distance between 2 landmarks among the x and y axis
        """
        lm1, lm2 = self.hand_landmarks_list[hand][lm1_idx], self.hand_landmarks_list[hand][lm2_idx]
        return np.linalg.norm(np.array(lm1[:2]) - np.array(lm2[:2]))


    def update_audio_params(self, audio_thread) -> None:
        # Map left hand with volume and right hand
        # If the right hand is not detected, no music
        # If the left hand is not detected but the right hand is detected, default volume
        if self.smoothed_barycenter['Right']:
            finger_dist = self.dist_between_lms(self.lms_name['INDEX_FINGER_TIP'], self.lms_name['THUMB_TIP'], 'Right')
            if finger_dist > 0.05:
                audio_thread.is_sound_on = False
            else:
                normalized_width = self.smoothed_barycenter['Right'][0]

                # Map pitch to normalized width (C4 to C5)
                audio_thread.target_freq = self.config.audio.min_freq + normalized_width * (self.config.audio.max_freq - self.config.audio.min_freq)
                audio_thread.is_sound_on = True
        else:
            audio_thread.is_sound_on = False

        if self.smoothed_barycenter['Left']:
            normalized_height = 1 - self.smoothed_barycenter['Left'][1]
            # Map volume to normalized height (0-1)
            audio_thread.target_volume = normalized_height
        else:
            audio_thread.target_volume = self.config.audio.default_volume
