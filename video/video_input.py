from abc import ABC, abstractmethod
from threading import Thread, Event
import logging

import numpy as np

logger = logging.getLogger(__name__)

class VideoInput(ABC, Thread):
    """
    Wrapper for all the possible video inputs of the pipeline.
    The frame acquisition process by the app runs its own thread in order not to interfere add any delay in the main loop of the program.
    """
    def __init__(self):
        super().__init__()
        self.configure()
        self.frame = None
        self.stop_event = Event()
        self.frame_available = Event()


    @abstractmethod
    def configure(self) -> None:
        """
        Allows to setup some settings or parameters specific to the video input.
        In the case of camera input, it can correspond to the camera settings or any parameter setup to trigger it.
        It can also theoretically handle videos, not only live stream devices.
        """
        pass


    @abstractmethod
    def read_frame(self) -> np.ndarray:
        """
        Grabs a frame from the video input
        """
        pass


    @abstractmethod
    def cleanup(self) -> None:
        pass


    def run(self):
        while not self.stop_event.is_set():
            self.frame = self.read_frame()
            self.frame_available.set()


    def stop(self):
        logger.info('Stopping video stream')
        self.stop_event.set()
        self.cleanup()


    def get_frame(self):
        self.frame_available.wait()
        self.frame_available.clear()
        return self.frame
