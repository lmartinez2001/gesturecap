from utils.mediapipe import convert_to_landmark_list
from .mapper import Mapper
import math

class PinchGestureMapper(Mapper):

    def __init__(self):
        self.audio_params = {
            'frequency': 440,
            'volume': 0.5
        }


    def process_features(self, raw_landmarker_data) -> dict:
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

                    if distance < 0.1:
                        freq = 100000/((index_pos.x**2) * 1000 + 100)
                        volume = index_pos.y

                        self.audio_params['frequency'] = freq
                        self.audio_params['volume'] = volume

        return self.audio_params
