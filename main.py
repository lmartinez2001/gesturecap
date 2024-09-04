import logging
import numpy as np
import cv2
import yaml

# Feature extractors
from feature_extractor import HandLandmarker, FrameDiffCalculator

# Video module
from video import Webcam

# Gesture mapper module
from feature_mapper import PinchGestureMapper, PulseMapper

# Audio module
from audio import OSCGenerator, SinewaveGenerator

# Display
from display import Display
from utils.display_components import create_fps_counter
from utils.file_parsers import parse_yml

logger = logging.getLogger(__name__)

def create_module(scenario, module_name: str):
    module_class = globals()[scenario[module_name]['class']]
    module_params = scenario[module_name].get('params', {})
    module = module_class(**module_params)
    return module


def load_scenario(scenario):
    logger.info(f"Loading scenario {scenario['scenario']}")
    video_input = create_module(scenario, 'video_input')
    feature_extractor = create_module(scenario, 'feature_extractor')
    feature_mapper = create_module(scenario, 'feature_mapper')
    audio_generator = create_module(scenario, 'audio_generator')
    return video_input, feature_extractor, feature_mapper, audio_generator


def main(scenario_file: str):
    logging.basicConfig(level=logging.DEBUG)

    scenario: dict = parse_yml(scenario_file)

    video_input, feature_extractor, mapper, audio_generator = load_scenario(scenario)

    #feedback display
    display = Display()

    # Starting input and output threads
    video_input.start()
    audio_generator.start()

    # Display config
    fps_counter = create_fps_counter(display)
    display.add_component(fps_counter)
    display.start()

    try:
        while video_input.is_alive():
            # Frame acquisition
            frame: np.ndarray = video_input.get_frame()

            # feature extractor output
            features = feature_extractor.process(frame)

            # mapping between features and audio data
            audio_params = mapper.process_features(features)

            # sending audio params
            audio_generator.data_to_send = audio_params

            # frame to display
            display.frame = frame

    except KeyboardInterrupt:
        pass

    finally:
        display.stop()
        video_input.stop()
        audio_generator.stop()

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--scenario', type=str, help='Scenario to load (.yml format)')

if __name__ == "__main__":
    args = parser.parse_args()
    main(scenario_file=args.scenario)
