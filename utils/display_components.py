import time
import cv2


def create_fps_counter(display):
    def fps_element(frame):
        fps_text = f"FPS: {display.fps:.1f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2
        text_color = (255, 255, 255)  # White color for text
        background_color = (0, 0, 0)  # Black color for background

        # Get text size
        text_size = cv2.getTextSize(fps_text, font, font_scale, font_thickness)[0]

        # Position for the FPS counter (top-right corner with padding)
        padding = 10
        text_x = frame.shape[1] - text_size[0] - padding
        text_y = text_size[1] + padding

        # Draw background rectangle
        cv2.rectangle(frame,
                      (text_x - padding, text_y - text_size[1] - padding),
                      (text_x + text_size[0] + padding, text_y + padding),
                      background_color, -1)

        # Draw FPS text
        cv2.putText(frame, fps_text,
                    (text_x, text_y),
                    font, font_scale, text_color, font_thickness)

    return fps_element
