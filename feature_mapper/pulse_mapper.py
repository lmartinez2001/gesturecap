from .mapper import Mapper
import time
import logging

logger = logging.getLogger(__name__)

class PulseMapper(Mapper):

    def __init__(self, threshold: float, cooldown: int):
        self.thresh = threshold
        self.cooldown = cooldown
        self.last_pulse_time = 0

    def process_features(self, value: float):
        mapped = {
            'pulse': 0
        }
        current_time = time.perf_counter() * 1000
        if value:
            if value > self.thresh:
                if current_time - self.last_pulse_time >= self.cooldown:
                    mapped['pulse'] = 1
                    self.last_pulse_time = current_time
        return mapped
