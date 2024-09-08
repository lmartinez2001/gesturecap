"""
The step-by-step creation of this class is detailed in the README file of this module.
"""
# 1. Creation of the file

# 2. Necessary imports
from .mapper import Mapper
import numpy as np

import logging
logger = logging.getLogger(__name__)

# 3. Definition of the BarycenterMapper class
class BarycenterMapper(Mapper):
    """
    Maps the barycenter of hand landmarks to audio parameters.
    """

    def __init__(self):
        self.audio_params = {
            'tempo': 0.5,
            'resonance': 0.5
        }
        logger.debug(f'Initiazed {__name__} with audio_params: {self.audio_params}')


    # 4. Implementation of the process_feature abstract method
    def process_features(self, raw_landmarker_data: dict) -> dict:
        """
        Calculates the barycenter of hand landmarks and maps it to audio parameters

        Parameters:
        ---
        raw_landmarker_data: dict
            Contains landmarks and handedness of every detected hand

        Returns:
        ---
        audio_params: dict
            Mapped frequency and volume to be output by the audio output module
        """
        hand_landmarks = raw_landmarker_data['landmarks']

        if hand_landmarks:
            # Only processing the first detected hand
            landmarks = hand_landmarks[0]

            barycenter_x = self._compute_barycenter_1D([lm.x for lm in landmarks])
            barycenter_y = self._compute_barycenter_1D([lm.y for lm in landmarks])

            self.audio_params['tempo'] = barycenter_y
            self.audio_params['resonance'] = barycenter_x
           
        return self.audio_params


    def _compute_barycenter_1D(self, coordinates: list) -> float:
        """
        Helper function computing to compute the barycenter along x and y axes of the landmarks

        Parameters
        ---
        coordinates, list, required
            Coordinates of the landmarks along one axis (x or y)

        Returns
        ---
        mean of the list (i.e 1D Barycenter)
        """
        return np.mean(coordinates)
