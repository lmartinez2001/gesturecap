import logging
from abc import ABC, abstractmethod
from typing import Any
from threading import Thread, Event, Lock

logger = logging.getLogger(__name__)

class AudioGenerator(ABC, Thread):
    """
    Handles how and to what device audio parameters output by the Feature Mapper module are sent.
    The module continuously send audio data, even if there is nothing to output.

    At each iteration of the main loop of this thread, audio parameters are stored in the _data_to_send.
    A setter and a getter are defined in or to safely write and access this variable. *
    Hence it should not directly be accessed from outside of this thread, not even by subclasses.
    """

    def __init__(self):
        super().__init__()
        self.stop_event = Event()
        self._data_to_send: Any = None
        self._data_lock = Lock()


    @property
    def data_to_send(self):
        """
        Getter for the _data_to_send attribute
        Sets a mutex to avoid concurrent access

        Returns:
        ---
        Any: The audio data to be sent.
        """
        with self._data_lock:
            return self._data_to_send


    @data_to_send.setter
    def data_to_send(self, value):
        """
        Setter for the _data_to_send attribute
        Uses a mutex to avoid concurrent access

        Parameters:
        ---
        value: Any
            The new audio data to be set.
        """
        with self._data_lock:
            self._data_to_send = value


    @abstractmethod
    def cleanup(self) -> None:
        """
        Contains all the code in charge of properly closing the connection with the audio device when the Audio module is stopped.
        """
        pass


    @abstractmethod
    def output_audio(self) -> None:
        """
        Contains the concrete actions to be performed to actually send audio parameters to the audio device.
        It's called at every iteration of the main loop of this thread
        """
        pass


    def run(self):
        """
        Abstract method implementation from threading.Thread
        Outputs audio signals at each iteration
        """
        while not self.stop_event.is_set():
            self.output_audio()


    def stop(self):
        """
        Triggers the stop_event Event to stop the main loop of this thread and calls the cleanup method to ensure that streams a correctly closed.
        """
        logger.info('Stopping audio stream')
        self.stop_event.set()
        self.cleanup()
