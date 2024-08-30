import logging
from abc import ABC, abstractmethod
from typing import Any
from threading import Thread, Event, Lock

logger = logging.getLogger(__name__)

class AudioGenerator(ABC, Thread):


    def __init__(self):
        super().__init__()
        self.stop_event = Event()
        self._data_to_send: Any = None
        self._data_lock = Lock()


    @property
    def data_to_send(self):
        with self._data_lock:
            return self._data_to_send


    @data_to_send.setter
    def data_to_send(self, value):
        with self._data_lock:
            self._data_to_send = value


    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def output_audio(self) -> None:
        pass


    def run(self):
        while not self.stop_event.is_set():
            self.output_audio()


    def stop(self):
        logger.info('Stopping audio stream')
        self.stop_event.set()
        self.cleanup()
