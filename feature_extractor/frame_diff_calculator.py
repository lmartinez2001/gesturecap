from .feature_extractor import FeatureExtractor
import cv2
import numpy as np


class FrameDiffCalculator(FeatureExtractor):

    def __init__(self):
        self.previous_frame = None

    def process(self, current_frame):
        mean_diff = None
        frame_diff = np.zeros(current_frame.shape[:-1])
        if self.previous_frame is not None:
            frame_diff = self._compute_abs_frame_diff(current_frame, self.previous_frame)
            mean_diff = np.mean(frame_diff)

        self.previous_frame = current_frame.copy()
        return mean_diff



    def _compute_abs_frame_diff(self, previous_frame, current_frame):

        current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

        frame_diff = cv2.absdiff(current_gray, previous_gray)
        return frame_diff
