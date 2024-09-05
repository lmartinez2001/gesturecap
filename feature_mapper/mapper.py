from abc import ABC, abstractmethod
from typing import Any

class Mapper(ABC):
    """
    Module in charge of processing features extracted from frames provided by the VideoInput module.
    These features are mapped to audio parameters which are then handled by the AudioGenerator module.
    """
    def __init__(self):
        pass


    @abstractmethod
    def process_features(features: Any) -> Any:
        """
        Converts features into audio parameters, such as frequency and volume.
        The format of audio parameters can be of any type as long as it fits the expected input type of the AudioGenerator.
        For instance, the audio.OSCGenerator audio module expects a dictionary with structure: { audio_param_route: value }


        Parameters
        ---
        features: Any
            Features to be extracted from a frame
        """
        pass
