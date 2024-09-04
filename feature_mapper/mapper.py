from abc import ABC, abstractmethod
from typing import Any

class Mapper(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def process_features(features) -> Any:
        pass
