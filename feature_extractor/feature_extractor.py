from abc import ABC, abstractmethod
from typing import Any
import numpy as np

class FeatureExtractor(ABC):

    @abstractmethod
    def process(self, frame: np.ndarray) -> Any:
        pass
