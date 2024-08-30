import logging
import numpy as np
import cv2

from config import Config

# AI models
from feature_extractor import HandLandmarker, FrameDiffCalculator

# Video module
from video import Webcam

# Gesture mapper module
from feature_mapper import PinchGestureMapper, PulseMapper

# Audio module
from audio import OSCGenerator
from audio import SinewaveGenerator

# Display
from display import Display
from utils.display_components import create_fps_counter


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    config = Config()

    cam = Webcam(0)

    # FRAME FEATURE EXTRACTOR
    # hand_landmarker = HandLandmarker(config)
    frame_diff_calculator = FrameDiffCalculator()

    # FEATURES TO AUDIO DATA MAPPER
    mapper = PulseMapper(threshold=3, cooldown=500)

    # AUDIO GENERATOR
    osc_generator = OSCGenerator()

    # FEEDBACK DISPLAY
    display = Display()


    # Starting threads
    cam.start()
    osc_generator.start()

    # Display config
    # fps_counter = create_fps_counter(display)
    # display.add_component(fps_counter)
    display.start()

    try:
        while cam.is_alive():
            # Frame acquisition
            frame: np.ndarray = cam.get_frame()

            # feature extractor output
            # detection_res = hand_landmarker.detect_hand_pose(frame)
            diff_val, frame_diff = frame_diff_calculator.process(frame)
            # print(diff_val)

            # mapping between features and audio data
            # audio_params = mapper.process_detection_results(detection_res)
            audio_pulse: int = mapper.process_detection_results(diff_val) # 0 or 1

            print(audio_pulse)

            # sending audio params
            osc_generator.data_to_send: dict = audio_pulse

            # frame to display
            display.frame = frame_diff

        # while cam.is_alive() :

            # osc_generator.data_to_send = {
            #     'pulse':1
            # }

    except KeyboardInterrupt:
        pass

    finally:
        display.stop()
        cam.stop()
        osc_generator.stop()


if __name__ == "__main__":
    main()
