import cv2
from .video_input import VideoInput
import time


class Webcam(VideoInput):

    def __init__(self, cam_index=0):
        self.cam_index = cam_index
        self.cap = None
        super().__init__()


    def configure(self):
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not self.cap.isOpened():
            raise Exception(f'Failed to open webcam {self.cam_index}')


    def read_frame(self):
        valid, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        return frame


    def cleanup(self):
        self.cap.release()



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
