import logging
from typing import Dict, Any

import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from google.protobuf.json_format import MessageToDict

from .strategy import RightHandStrategy, LeftHandStrategy

logger = logging.getLogger(__name__)

class HandTracker:
    def __init__(self, config, device: str = 'cpu'):
        self.config = config
        self.hand_strategies = {
            'Right': RightHandStrategy(config),
            'Left': LeftHandStrategy(config)
        }
        self.device = device
        self.lms_name: Dict[str, int] = config.tracker.landmarks_name

        # Initialize mediapipe backend
        self.mp_hands = mp.solutions.hands
        self.hands = self._create_hand_landmarker()

        # Keep track of the true barycenter and the smoothed (previous) one for exponential smoothing
        self._reset_tracking_parameters()
        logger.info('HandTracker class initialized')


    def _create_hand_landmarker(self, device: str):
        base_options = python.BaseOptions(
            model_asset_path='hand_landmarker.task',  # You'll need to download this model
            # delegate=python.BaseOptions.Delegate.CPU,
            delegate=python.BaseOptions.Delegate.GPU if self.device == 'gpu' else python.BaseOptions.Delegate.CPU
        )
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=self.config.tracker.n_hands,
            min_hand_detection_confidence=self.config.tracker.detection_confidence,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        return vision.HandLandmarker.create_from_options(options)


    def _landmarks_to_list(self, landmarks) -> list:
        assert landmarks.landmark is not None
        return [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]


    def _empty_hand_dict(self) -> Dict[str, None]:
        return {'Left': None, 'Right': None}


    def _extract_handedness_label(self, handedness) -> str:
        return MessageToDict(handedness)['classification'][0]['label']


    def _reset_tracking_parameters(self) -> None:
        self.current_barycenter: Dict[str, Any] = self._empty_hand_dict()
        self.smoothed_barycenter: Dict[str, Any] = self._empty_hand_dict()
        self.hand_landmarks: Dict[str, Any] = self._empty_hand_dict()
        self.hand_landmarks_list: Dict[str, Any] = self._empty_hand_dict()


    def process_frame(self, frame: np.ndarray) -> None:
        assert frame is not None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = self.hands.process(frame_rgb)

        self._reset_tracking_parameters()

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                handedness_label: str = self._extract_handedness_label(handedness)

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


    def smooth_barycenter(self, previous: tuple | None, current: tuple, alpha: float) -> tuple:
        assert current is not None

        if previous is None:
            previous = current
        smoothed_barycenter = tuple(alpha * c + (1 - alpha) * p for c, p in zip(current, previous))
        return smoothed_barycenter


    def update_audio_params(self, audio_thread) -> None:
        for hand, strategy in self.hand_strategies.items():
            landmarks = {
                'list': self.hand_landmarks_list[hand],
                'barycenter': self.smoothed_barycenter[hand]
            }
            strategy.process(landmarks, audio_thread)
