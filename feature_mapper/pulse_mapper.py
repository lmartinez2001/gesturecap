from .mapper import Mapper
import time
import logging

logger = logging.getLogger(__name__)

class PulseMapper(Mapper):
    """
    Maps any float value to a binary signal sent to the audio output module.
    This mapper is mainly useful for timing measurement purposes.
    For instance, if it's coupled with the feature_extractor.FrameDiffCalculator class, it allows to send a pulse whenever a movement between two frames is detected.
    """

    def __init__(self, threshold: float, cooldown: int):
        """
        Initializes the PulseMapper.


        Parameters:
        ---
        threshold: float
            The threshold value above which a pulse is triggered

        cooldown: int
            The minimum time in milliseconds between two consecutive pulses
        """
        self.thresh = threshold
        self.cooldown = cooldown
        self.last_pulse_time = 0


    def process_features(self, value: float) -> dict:
        """
        Abstract method implementation.
        Send a pulse, as a binary variable whenever the value variable is above a threshold.
        As the whole pipeline is intended to run at a high refresh rate,
        a cooldown is setup to prevent the pulse from being continuously sent.
        This can happen for example when a movements lasts for several frames (which occurs often) but we're actually interested in the beginning of the movement.

        For other usecases where pulses sent continuously is not an issue, the cooldown can just be set to 0, hence disabled.


        Parameters
        ---
        value: float, required
            To be compared with the threshold attribute


        Returns
        ---
        mapped: dict
            Value of the pulse. Either 0 or 1
        """
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
