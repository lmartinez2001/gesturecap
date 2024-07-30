import cv2

from audio import AudioThread
from hand_tracker import HandTracker
from display import Display

def get_cam(idx) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(idx)

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not cap.isOpened():
        raise RuntimeError("Failed to open webcam")
    return cap


def main():
    cap = get_cam(0)
    hand_tracker = HandTracker(n_hands=1)
    display = Display(hand_tracker)

    audio_thread = AudioThread()
    audio_thread.start()

    try:
        while cap.isOpened():
            valid, frame = cap.read()
            if not valid:
                continue

            # Vertical flip (more intuitive)
            frame = cv2.flip(frame, 1)
            hand_tracker.process_frame(frame)
            display.update(frame)
            hand_tracker.update_audio_params(audio_thread)
            # cv2.imshow("Output", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    finally:
        audio_thread.stop()
        audio_thread.join()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
