"""
This class a copy pf the HandLandmarker class, but using the Pose Landmarker model from Mediapipe instead.
The step-by-step creation of this class is detailed in the README file of this module.
"""

# 1. Creation of the file

# 2. Necessary imports
from .feature_extractor import FeatureExtractor

import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Optional imports for typing
from typing import List, Dict, Any
from mediapipe.tasks.python.components.containers import landmark as landmark_module
from mediapipe.framework.formats import landmark_pb2
from utils.mediapipe import convert_to_landmark_list


import logging
logger = logging.getLogger(__name__)

# 3. Definition of the PoseLandmarker class
class PoseLandmarker(FeatureExtractor):
    """
    Extracts pose landmarks from frames. It uses the Mediapipe pose landmarker model to detect human poses.
    """

    def __init__(self, device: str = 'cpu'):
        """
        Initializes the PoseLandmarker.

        Parameters:
        ---
        device: str, default = 'cpu'
            The device to run the model on. Choose between 'cpu' and 'gpu'.
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        base_options = python.BaseOptions(
            model_asset_path='pose_landmarker_lite.task',  # You'll need to download this model
            delegate=python.BaseOptions.Delegate.GPU if device == 'gpu' else python.BaseOptions.Delegate.CPU
        )
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False,  # Optional, for segmenting the person from the background
        )
        self.pose = vision.PoseLandmarker.create_from_options(options)


    # 4. implementation of the process abstract method defined in FeatureExtractor
    def process(self, image: np.ndarray) -> Dict[str, List[Any]]:
        """
        Runs mediapipe model inference on the frame. The model determines landmarks of detected pose(s)


        Parameters
        ---
        image: np.ndarray, required
            Frame to be processed


        Returns
        ---
        res: dict[landmarks] or None
            Pose landmarker detection results or None if no pose is detected
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        detection_result = self.pose.detect(mp_image)
        res = {
            'landmarks': detection_result.pose_landmarks,
        }
        return res
