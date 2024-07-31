from abc import ABC, abstractmethod
from typing import Dict, Any


class HandStrategy(ABC):
    @abstractmethod
    def process(self, landmarks: Dict[str, Any], audio_thread: Any) -> None:
        pass

class RightHandStrategy(HandStrategy):
    def __init__(self, config):
        self.config = config
        self.lms_name = config.tracker.landmarks_name

    def process(self, landmarks: Dict[str, Any], audio_thread: Any) -> None:
        if landmarks['list']:
            finger_dist = self.dist_between_lms(self.lms_name['INDEX_FINGER_TIP'], self.lms_name['THUMB_TIP'], landmarks)
            if finger_dist > 0.05:
                audio_thread.is_sound_on = False
            else:
                normalized_width = landmarks['barycenter'][0]
                audio_thread.target_freq = self.config.audio.min_freq + normalized_width * (self.config.audio.max_freq - self.config.audio.min_freq)
                audio_thread.is_sound_on = True
        else:
            audio_thread.is_sound_on = False

    def dist_between_lms(self, lm1_idx: int, lm2_idx: int, landmarks: Dict[str, Any]) -> float:
        lm1, lm2 = landmarks['list'][lm1_idx], landmarks['list'][lm2_idx]
        return ((lm1[0] - lm2[0])**2 + (lm1[1] - lm2[1])**2)**0.5


class LeftHandStrategy(HandStrategy):
    def __init__(self, config):
        self.config = config

    def process(self, landmarks: Dict[str, Any], audio_thread: Any) -> None:
        if landmarks['list']:
            normalized_height = 1 - landmarks['barycenter'][1]
            audio_thread.target_volume = normalized_height
        else:
            audio_thread.target_volume = self.config.audio.default_volume
