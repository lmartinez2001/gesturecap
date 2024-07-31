import cv2
import numpy as np
import matplotlib.pyplot as plt

import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec


class Display:
    def __init__(self, hand_tracker, config):
        self.config = config
        self.notes: dict = config.audio.note_frequencies

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.landmarks_style = DrawingSpec(
            color=config.display.landmarks_color
        )
        self.connections_style = DrawingSpec(
            color=config.display.connections_color,
            thickness=config.display.connections_thickness
        )
        self.mp_hands = mp.solutions.hands

        self.tracker = hand_tracker


    def draw_note_lines(self, frame: np.ndarray) -> np.ndarray:
        h, w, _ = frame.shape
        for note, freq in self.notes.items():
            x = int((freq - self.config.audio.min_freq) / (self.config.audio.max_freq - self.config.audio.min_freq) * w)
            frame = cv2.line(frame, (x, 0), (x, h), self.config.display.note_lines_color, 1)
            frame = cv2.putText(frame, note, (x + 5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        return frame


    def draw_hand_landmarks(self, frame: np.ndarray) -> np.ndarray:
        row, col, _ = frame.shape
        if self.tracker.hand_landmarks['Right']:
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=self.tracker.hand_landmarks['Right'],
                connections=self.mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=self.landmarks_style,
                connection_drawing_spec=self.connections_style)


            cx, cy = int(self.tracker.smoothed_barycenter['Right'][0] * col), int(self.tracker.smoothed_barycenter['Right'][1] * row)
            frame = cv2.circle(
                frame,
                (cx, cy),
                self.config.display.barycenter_radius,
                self.config.display.barycenter_color,
                -1
            )

        if self.tracker.hand_landmarks['Left']:
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=self.tracker.hand_landmarks['Left'],
                connections=self.mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=self.landmarks_style,
                connection_drawing_spec=self.connections_style)


            cx, cy = int(self.tracker.smoothed_barycenter['Left'][0] * col), int(self.tracker.smoothed_barycenter['Left'][1] * row)
            frame = cv2.circle(
                frame,
                (cx, cy),
                self.config.display.barycenter_radius,
                self.config.display.barycenter_color,
                -1
            )
        return frame


    def update(self, frame: np.ndarray) -> None:
        frame = self.draw_hand_landmarks(frame)
        frame = self.draw_note_lines(frame)
        cv2.imshow('Output', frame)
