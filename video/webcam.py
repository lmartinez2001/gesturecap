import cv2
from .video_input import VideoInput
import time
import logging

logger = logging.getLogger(__name__)


class Webcam(VideoInput):
    """
    Wrapper for any basic webcam.
    It uses opencv to trigger the camera and handle the incoming video stream
    """

    def __init__(self, cam_index=0):
        """
        Initializes the Webcam.

        Parameters:
        ---
        cam_index: int, default=0
            The index of the webcam to use.
        """
        self.cam_index = cam_index
        self.cap = None
        super().__init__()


    def configure(self):
        """
        Abstract method implementation
        Instanciate the desired camera and sets the buffer to 1 and disables frames buffering to ensure minimal latency
        """
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not self.cap.isOpened():
            raise Exception(f'Failed to open webcam {self.cam_index}')


    def read_frame(self):
        """
        Abstract method implementation
        Uses cv2.VideoCapture to capture a frame
        """
        valid, frame = self.cap.read()
        return frame


    def cleanup(self):
        """
        Abstract method implementation
        """
        self.cap.release()
        logger.debug('Webcam released')



# TEST
if __name__ == '__main__':
    cam = Webcam(0)
    cam.start()

    frame_count = 0
    start_time = time.time()
    fps = 0

    while cam.is_running:
        frame = cam.get_frame()

        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 1:  # Update FPS every second
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()

        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
       
        
        cv2.imshow('Test', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.stop()
    cv2.destroyAllWindows()
