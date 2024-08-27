import time
import logging

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# For typing
from typing import List
from mediapipe.tasks.python.components.containers import landmark as landmark_module

from mediapipe.framework.formats import landmark_pb2

logger = logging.getLogger(__name__)

class HandLandmarker:
    def __init__(self, config=None, n_hands=2, device: str = 'cpu'):

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


    def detect_hand_pose(self, image: np.ndarray):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        detection_result = self.hands.detect(mp_image)

        return detection_result.hand_landmarks


    def convert_to_landmark_list(self, normalized_landmarks: List[landmark_module.NormalizedLandmark]) -> landmark_pb2.NormalizedLandmarkList:
        landmark_list = landmark_pb2.NormalizedLandmarkList()
        for landmark in normalized_landmarks:
            new_landmark = landmark_list.landmark.add()
            new_landmark.x = landmark.x
            new_landmark.y = landmark.y
            new_landmark.z = landmark.z
        return landmark_list


    def draw_landmarks(self, image, hand_landmarks: List[List[landmark_module.NormalizedLandmark]]):
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
