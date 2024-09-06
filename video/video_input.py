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
        As it's called during the initialization and most of the time needs the camera to be instanced before configuring it, the super().__init__() must be called *at the end* of the __init__ function of a subclass
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
        """
        Cleanup the current context.
        For example, the code in charge of the camera unbinding should be written in this function
        It's  called in the `stop` function
        """
        pass


    def run(self):
        """
        Abstract method implementation coming from threading.Thread
        It contains the main loop of this thread.
        At each iteration, it grabs a new frame and it signals that the image is available via the frame_available threading.Event
        The while loop stops when the stop_event evnet is triggered. See: function`stop`
        """
        while not self.stop_event.is_set():
            self.frame = self.read_frame()
            self.frame_available.set()


    def stop(self):
        """
        Abstract method implementation coming from threading.Thread
        When called, it triggers the stop_event event and calls the cleanup method
        """
        logger.info('Stopping video stream')
        self.stop_event.set()
        self.cleanup()


    def get_frame(self):
        self.frame_available.wait()
        self.frame_available.clear()
        return self.frame
