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
        # self.is_running = False
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


    # def start(self):
    #     self.is_running = True
    #     self.thread = Thread(target=self._capture_loop, daemon=True)
    #     self.thread.start()

    def run(self):
        while not self.stop_event.is_set():
            self.frame = self.read_frame()
            self.frame_available.set()


    # def _capture_loop(self):
    #     while self.is_running:
    #         self.frame = self.read_frame()
    #         self.frame_available.set()


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
