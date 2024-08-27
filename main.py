import logging

import cv2

from config import Config

# AI models
from models.hand_pose import HandLandmarker

# Video module
from video import Webcam

# Hand strategy module

logger = logging.getLogger(__name__)

# def get_cam(idx) -> cv2.VideoCapture:
#     cap = cv2.VideoCapture(idx)
#     logger.info(f'Camera loaded with index {idx}')

#     cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#     if not cap.isOpened():
#         raise RuntimeError('Failed to open webcam')
#     return cap

# from video import webcam, flircam

# cam = webcam/filrcam(bunch of options)
# hand_tracker = HandTracker(device='cpu')
# while...
#   frame = cam.read()


def main():
    logging.basicConfig(level=logging.INFO)

    config = Config()

    cam = Webcam(0)

    hand_landmarker = HandLandmarker(config)

    # display = Display(hand_tracker, config)

    # audio_thread = AudioThread(config)
    # audio_thread.start()
    # logger.info('Audio thread started')

    cam.start()

    try:
        while cam.is_running:
            frame = cam.get_frame()
            landmarks = hand_landmarker.detect_hand_pose(frame)
            print(len(landmarks))

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
