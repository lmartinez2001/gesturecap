import logging

import cv2

from config import Config

# AI models
from models.hand_pose import HandLandmarker

# Video module
from video import Webcam

# Gesture mapper module
from gesture_mapper import PinchGestureMapper

# Audio module
from audio import OSCGenerator
from audio import SinewaveGenerator
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    config = Config()
    cam = Webcam(0)
    hand_landmarker = HandLandmarker(config)
    mapper = PinchGestureMapper()
    osc_generator = OSCGenerator()

    # Starting threads
    cam.start()
    osc_generator.start()

    try:
        while cam.is_alive():
            # Frame acquisition
            frame = cam.get_frame()

            # hand landmarker output
            detection_res = hand_landmarker.detect_hand_pose(frame)

            # mapping between gestures and audio params
            audio_params = mapper.process_detection_results(detection_res)

            # sending audio params
            osc_generator.data_to_send = audio_params
            print(audio_params)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
    except KeyboardInterrupt:
        pass

    finally:
        cam.stop()
        osc_generator.stop()


if __name__ == "__main__":
    main()
