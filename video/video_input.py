from abc import ABC, abstractmethod
from threading import Thread, Event
import logging

import numpy as np

logger = logging.getLogger(__name__)

class VideoInput(ABC, Thread):

    def __init__(self):
        super().__init__()
        self.configure()
        self.frame = None
        self.stop_event = Event()
        self.frame_available = Event()


    @abstractmethod
    def configure(self) -> None:
        pass


    @abstractmethod
    def read_frame(self) -> np.ndarray:
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
        # self.is_running = False
        # self.thread.join()
        self.stop_event.set()
        self.cleanup()


    def get_frame(self):
        self.frame_available.wait()
        self.frame_available.clear()
        return self.frame
