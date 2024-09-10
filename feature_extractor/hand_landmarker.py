import time
import logging

import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# For typing
from typing import List, Dict, Any
from mediapipe.tasks.python.components.containers import landmark as landmark_module
from mediapipe.framework.formats import landmark_pb2
from utils.mediapipe import convert_to_landmark_list

from .feature_extractor import FeatureExtractor

logger = logging.getLogger(__name__)


class HandLandmarker(FeatureExtractor):
    """
    Extracts hand landmarks from frames. It uses the Mediapipe hand landmarker model to detect hands.
    In addition to the hand(s) landmarks, handedness is returned as well
    """

    def __init__(self, n_hands=2, device: str = 'cpu'):
        """
        Initializes the HandLandmarker.


        Parameters:
        ---
        n_hands: int, default=2
            The maximum number of hands to detect in each frame

        device: str, default = 'cpu'
            The device to run the model on. Choose between 'cpu' and 'gpu'.
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        base_options = python.BaseOptions(
            model_asset_path='hand_landmarker.task',  # You'll need to download this model
            delegate=python.BaseOptions.Delegate.GPU if device == 'gpu' else python.BaseOptions.Delegate.CPU
        )
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=n_hands,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.hands = vision.HandLandmarker.create_from_options(options)


    def process(self, image: np.ndarray) -> Dict[str, List[List[Any]]]:
        """
        Implementation of the abstract method coming from feature_extractor.FeatureExtractor class.
        Runs mediapipe model inference on the frame. The model determines landmarks and handedness of detected hand(s)


        Parameters
        ---
        image: np.ndarray, required
            Frame to be processed


        Returns
        ---
        res: dict[lansmarks, handedness] or None
            Hand landmarker detection results or None if no hand is detected
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        detection_result = self.hands.detect(mp_image)
        res = {
            'landmarks': detection_result.hand_landmarks,
            'handedness': detection_result.handedness
        }
        return res


    def draw_landmarks(self, image, hand_landmarks: List[List[landmark_module.NormalizedLandmark]]):
        """
        Draws hand landmarks on the image

        Parameters:
        ---
        image: np.ndarray
            The image on which to draw the landmarks
        hand_landmarks: List[List[landmark_module.NormalizedLandmark]]
            The list of hand landmarks to draw

        Returns:
        ---
        np.ndarray
            The image with landmarks drawn on it
        """
        # List with as many elements as detected hands
        if hand_landmarks:
            # One list per hand
            for landmarks in hand_landmarks:
                lms = self.convert_to_landmark_list(landmarks)
                self.mp_drawing.draw_landmarks(
                    image,
                    lms,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
        return image 
