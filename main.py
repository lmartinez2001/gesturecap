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


logger = logging.getLogger(__name__)


def main(scenario_file: str):
    logging.basicConfig(level=logging.DEBUG)

    with open(scenario_file, 'r') as f:
        scenario = yaml.safe_load(f)

    logger.info(f"Loading scenario {scenario['scenario']}")
    # video input module
    video_input_class = globals()[scenario['video_input']['class']]
    video_input_params = scenario['video_input'].get('params', {})
    video_input = video_input_class(**video_input_params)

    # feature selector module
    feature_extractor_class = globals()[scenario['feature_extractor']['class']]
    feature_extractor_params = scenario['feature_extractor'].get('params', {})
    feature_extractor = feature_extractor_class(**feature_extractor_params)

    # feature mapper module
    feature_mapper_class = globals()[scenario['feature_mapper']['class']]
    mapper_params = scenario['feature_mapper'].get('params', {})  # Get params if present
    mapper = feature_mapper_class(**mapper_params)

    # audio output module
    audio_generator_class = globals()[scenario['audio_generator']['class']]
    audio_generator_params = scenario['audio_generator'].get('params', {})
    audio_generator = audio_generator_class(**audio_generator_params)


    # cam = Webcam(0)

    # FRAME FEATURE EXTRACTOR
    # hand_landmarker = HandLandmarker(config)
    # frame_diff_calculator = FrameDiffCalculator()

    # FEATURES TO AUDIO DATA MAPPER
    # mapper = PinchGestureMapper()
    # mapper = PulseMapper(threshold=1.25, cooldown=500)

    # AUDIO GENERATOR
    osc_generator = OSCGenerator()

    # FEEDBACK DISPLAY
    display = Display()


    # Starting threads
    # cam.start()
    # osc_generator.start()

    video_input.start()
    audio_generator.start()

    # Display config
    fps_counter = create_fps_counter(display)
    display.add_component(fps_counter)
    display.start()

    try:
        while video_input.is_alive():
            # Frame acquisition
            # frame: np.ndarray = cam.get_frame()
            frame: np.ndarray = video_input.get_frame()

            # feature extractor output
            # detection_res = hand_landmarker.process(frame)
            # diff_val, frame_diff = frame_diff_calculator.process(frame)
            features = feature_extractor.process(frame)
            # print(f'Features {features}, {type(features)}')
            # mapping between features and audio data
            # audio_params = mapper.process_detection_results(detection_res)
            # audio_params: int = mapper.process_detection_results(diff_val) # 0 or 1
            audio_params = mapper.process_features(features)

            # sending audio params
            # osc_generator.data_to_send: dict = audio_params
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
