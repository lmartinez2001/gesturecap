from utils.mediapipe import convert_to_landmark_list
from .mapper import Mapper
import math
import numpy as np

class PinchGestureMapper(Mapper):
    """
    Maps landmarks provided by the mediapipe HandLandmarker to frequency and volume values.
    These parameters are changed when a pinch between the thumb and the index is detected.

    Attributes
    ---
    audio_params: dict
        Set of parameters used as an input for the audio module.
        If the audio module is OSCGenerator, the names of the dictionary keys must match the names of the routes used by the generator.
        For more details, see class:`video.OSCGenerator`.
    """
    def __init__(self):
        self.audio_params = {
            'frequency': 440,
            'volume': 0.5
        }


    def process_features(self, raw_landmarker_data: dict) -> dict:
        """
        Abstract method implementation.
        If a right hand is detected and is pinching, (i.e index and thumb are close to eachother)
        the output frequency is mapped with the x (horizontal) position of the midpoint between thumb index landmarks.
        Volume is mapped to the y (vertical) position of that midpoint.


        Parameters
        ---
        raw_landmarker_data: dict, required
            Contains landmarks and handednes every detected hands


        Returns
        ---
        audio_params: dict
            Mapped frequency and volume to be output by the audio output module
        """
        hands_lms =  raw_landmarker_data['landmarks']
        handedness =  raw_landmarker_data['handedness']
        assert len(hands_lms) == len(handedness)


        if hands_lms:
            for lms, handedness in zip(hands_lms, handedness):
                if handedness[0].display_name == 'Right':
                    lms_list = convert_to_landmark_list(lms).landmark
                    index_pos = lms_list[8]
                    thumb_pos = lms_list[4]
                    distance = math.dist([index_pos.x, index_pos.y], [thumb_pos.x, thumb_pos.y])
                    middle = np.mean([index_pos.x, thumb_pos.x]), np.mean([index_pos.y, thumb_pos.y])
                    if distance < 0.1:
                        freq = 200 * 50 ** (1-middle[0])
                        #freq = 100000/((middle[0]**2) * 1000 + 100)
                        volume = 1-middle[1]

                        self.audio_params['frequency'] = freq
                        self.audio_params['volume'] = volume

        return self.audio_params
