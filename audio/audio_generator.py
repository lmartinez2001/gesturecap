import logging
for abc import ABC, abstractmethod
from typing import Any
from threading import Thread, Event

logger = logging.getLogger(__name__)

class AudioGenerator(ABC):

    def __init__(self):
        self.is_running: bool = False
        self.data_to_send: Any = None
        self.thread: Thread = None
        self.setup()


    @abstractmethod
    def setup(self) -> None:
        pass


    @abstractmethod
    def output_audio(self) -> None:
        pass


    @abstractmethod
    def update_data_to_send(self) -> Any:
        pass


    @abstractmethod
    def cleanup(self) -> None:
        pass

    def _audio_loop(self):
        while self.is_running:
            self.data_to_send = self.update_data_to_send()
            self.output_audio()

    def start(self):
        logger.info('Starting audio stream')
        self.thread = Thread(target=self._audio_loop, daemon=True)
        self.thread.start()

    def stop(self):
        logger.info('Stopping audio stream')
        self.is_running = False
        self.thread.join()
        self.cleanup()
