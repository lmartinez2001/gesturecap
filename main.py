import logging

import cv2

from config import Config

# AI models
from models.hand_pose import HandLandmarker

# Video module
from video import Webcam

from gesture_mapper import PinchGestureMapper

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    config = Config()

    cam = Webcam(0)

    hand_landmarker = HandLandmarker(config)

    mapper = PinchGestureMapper()
    # display = Display(hand_tracker, config)

    # audio_thread = AudioThread(config)
    # audio_thread.start()
    # logger.info('Audio thread started')

    cam.start()

    try:
        while cam.is_running:
            # Frame acquisition
            frame = cam.get_frame()

            # hand landmarker output
            detection_res = hand_landmarker.detect_hand_pose(frame)

            # mapping between gestures and audio params
            audio_params = mapper.process_detection_results(detection_res)
            print(audio_params)

            # sending audio params
            # audio_generator.update_audio_params(audio_params)


            # audio_gen.to_send = new_values
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
    except KeyboardInterrupt:
        pass

    finally:
        cam.stop()
        # audio_thread.stop()
        # audio_thread.join()
        # cap.release()
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
