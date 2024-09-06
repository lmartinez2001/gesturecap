import logging

import cv2
import numpy as np
import matplotlib.pyplot as plt

import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec

from threading import Thread, Event, Lock
import time


logger = logging.getLogger(__name__)

class Display(Thread):
    """
    Display module providing a visual feedback of the video_input or any processed version of this input (it doesn't have to be the raw frame)

    To avoid any drop in performance, the module runs its own thread, and the image to be displayed is stored in the _frame variable.
    A setter and a getter are defined to preven from accessing this variable directly, hence avoiding concurrent access.

    A system of *components* allows to had some predefined features to the display, like an FPS counter or any other relevant visual information.
    """

    def __init__(self, width=800, height=600, display_name='Display'):
        super().__init__()
        self.display_name = display_name
        self._frame = np.zeros((width, height, 3))
        self.components = []
        self.stop_event = Event()
        self.lock = Lock()
        self.width = width
        self.height = height
        self.frame_count = 0
        self.fps = 0
        self.last_fps_update = time.time() # required for the fps_counter visual component
        logger.info('Display class initialized')


    @property
    def frame(self):
        """
        Getter for the _frame attribute
        Prevents from concurrent access with a mutex
        """
        with self.lock:
            return self._frame.copy()


    @frame.setter
    def frame(self, new_frame):
        """
        Setter for the _frame attribute
        Prevents from concurrent access with a mutex

        To ensure that the framerate actually corresponds to the one of the input video stream, it's computed every time the setter is called
        """
        with self.lock:
            self._frame = cv2.resize(new_frame, (self.width, self.height))
            self.frame_count += 1
            current_time = time.time()
            time_diff = current_time - self.last_fps_update
            if time_diff >= 1.0:  # update fps every second
                self.fps = self.frame_count / time_diff
                self.frame_count = 0
                self.last_fps_update = current_time



    def add_component(self, component):
        """
        Adds a component to display
        """
        with self.lock:
            self.components.append(component)


    def run(self):
        """
        Abstract method implmentation from threading.Thread
        Displays the content of the _frame variable (through its getter) after applying visual components
        """
        while not self.stop_event.is_set():
            display_frame = self.frame.copy()
            # Apply components to the frame to display
            for comp in self.components:
                comp(display_frame)

            cv2.imshow(self.display_name, display_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_event.set()
                break
        cv2.destroyAllWindows()

       
    def stop(self):
        """
        Abstract method implementation from threading.Thread
        """
        logger.info('Stopping display stream')
        self.stop_event.set()
