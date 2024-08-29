import time
import cv2

def create_fps_counter():
    fps_counter = {'last_time': time.time(), 'fps': 0}

    def fps_element(frame):
        current_time = time.time()
        fps_counter['fps'] = 1 / (current_time - fps_counter['last_time'])
        fps_counter['last_time'] = current_time

        cv2.putText(frame, f"FPS: {fps_counter['fps']:.2f}",
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return fps_element
