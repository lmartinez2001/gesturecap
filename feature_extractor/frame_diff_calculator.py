import cv2
import numpy as np

from .feature_extractor import FeatureExtractor


class FrameDiffCalculator(FeatureExtractor):
    """
    Quantifies the pixel difference from one frame to another, for instance to detect some movement on the video input.
    It computes the mean of the absolute difference between the current frame and the previous one
    In the current context, this feature extractor is mainly intended for timing measurement purposes.


    Attributes
    ---
    previous_frame: np.ndarray
        The previous frame is stored in order to compute the difference with the current one
    """
    def __init__(self):
        self.previous_frame = None


    def process(self, current_frame: np.ndarray) -> float:
        """
        Implementation of the abstract method coming from feature_extractor.FeatureExtractor class.
        Computes per-pixel difference_image = |previous_frame - current_frame|.
        Pixel values of the difference_image are averaged to get a single float quantifying the frame difference


        Parameters
        ---
        current_frame: np.ndarray, required
            Frame used to compute the difference with the stored previous frame=


        Returns
        ---
        mean_diff: float
            Mean difference between current and previous frames
        """

        mean_diff = None
        frame_diff = np.zeros(current_frame.shape[:-1])
        if self.previous_frame is not None:
            frame_diff = self._compute_abs_frame_diff(current_frame, self.previous_frame)
            mean_diff = np.mean(frame_diff)

        self.previous_frame = current_frame.copy()
        return mean_diff



    def _compute_abs_frame_diff(self, previous_frame: np.ndarray, current_frame: np.ndarray):
        """
        Converts input frames to grayscale and computes per-pixel absolute difference.


        Parameters:
        ---
        current_frame: np.ndarray
            The most recent frame.

        previous_frame: np.ndarray
            The frame to be compared with the current frame


        Returns:
        ---
        frame_diff: np.ndarray
            Image of the absolute difference between current and previous frames
        """
        previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
        current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        frame_diff = cv2.absdiff(current_gray, previous_gray)
        return frame_diff
