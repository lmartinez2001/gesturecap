from abc import ABC, abstractmethod

import numpy as np
from typing import Any


class FeatureExtractor(ABC):
    """
    Module responsible for extracting features from frames output by an instance of video.VideoModule
    Features are then handled by a mapper processing them to fit in the audio output module.
    They can be of any type as long as one ensure that the return type of the process function matches the expected input type of the chosen mapper module.
    """

    @abstractmethod
    def process(self, frame: np.ndarray) -> Any:
        """
        Extract features from a raw captured frame.
        Hence it also include all the potential preprocessing steps required to extract features.
        It's executed at each iteration of the main loop of the program
        """
        pass
