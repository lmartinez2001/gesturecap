import logging
import numpy as np
import cv2
import yaml

# Video module
from video import Webcam

# Display
from display import Display
from utils.display_components import create_fps_counter
from utils.file_parsers import parse_yml
from utils.scenario import Scenario

logger = logging.getLogger(__name__)


def main(scenario_file: str):
    logging.basicConfig(level=logging.DEBUG)

    scenario: Scenario = Scenario(scenario_file)

    #feedback display
    display = Display()

    # Starting input and output threads
    scenario.video_input.start()
    scenario.audio_generator.start()

    # Display config
    fps_counter = create_fps_counter(display)
    display.add_component(fps_counter)
    display.start()

    try:
        while scenario.video_input.is_alive():
            # Frame acquisition
            frame: np.ndarray = scenario.video_input.get_frame()

            # feature extractor output
            features = scenario.feature_extractor.process(frame)

            # mapping between features and audio data
            audio_params = scenario.feature_mapper.process_features(features)

            # sending audio params
            scenario.audio_generator.data_to_send = audio_params

            # frame to display
            display.frame = frame

    except KeyboardInterrupt:
        pass

    finally:
        display.stop()
        scenario.video_input.stop()
        scenario.audio_generator.stop()

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--scenario', type=str, help='Scenario to load (.yml format)')

if __name__ == "__main__":
    args = parser.parse_args()
    main(scenario_file=args.scenario)
