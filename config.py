from dataclasses import dataclass, field
from typing import Dict

@dataclass
class AudioConfig:
   sampling_rate: int = 44100

   buffer_size: int = 1024

   default_freq: int = 440

   default_volume: float = 0.3

   # Volume smoothing factor
   alpha_vol: float = 0.15

   # Frequency smoothing factor
   alpha_freq: float = 0.15

   note_frequencies: Dict[str, float] = field(default_factory= lambda: ({
                            'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
                            'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25
                            }))

@dataclass
class DisplayConfig:
    landmarks_color: tuple = (49, 209, 255)

    connections_color: tuple = (255, 0, 0)

    connections_thickness: int = 1

    barycenter_color: tuple = (0, 0, 255)

    barycenter_radius: int = 10

    note_lines_color: tuple = (0, 255, 0)

    cam_id: int = 0


@dataclass
class TrackerConfig:
    # Barycenter smoothing factor
    alpha_barycenter: float = 0.3

    # Number of hands to be tracked
    n_hands: int = 1

    detection_confidence: float = 0.6

    landmarks_name: Dict[str, int] = field(default_factory= lambda: ({
         'WRIST': 0,
         'THUMB_CMC': 1,
         'THUMB_MCP': 2,
         'THUMB_IP': 3,
         'THUMB_TIP': 4,
         'INDEX_FINGER_MCP': 5,
         'INDEX_FINGER_PIP': 6,
         'INDEX_FINGER_DIP': 7,
         'INDEX_FINGER_TIP': 8,
         'MIDDLE_FINGER_MCP': 9,
         'MIDDLE_FINGER_PIP': 10,
         'MIDDLE_FINGER_DIP': 11,
         'MIDDLE_FINGER_TIP': 12,
         'RING_FINGER_MCP': 13,
         'RING_FINGER_PIP': 14,
         'RING_FINGER_DIP': 15,
         'RING_FINGER_TIP': 16,
         'PINKY_MCP': 17,
         'PINKY_PIP': 18,
         'PINKY_DIP': 19,
         'PINKY_TIP': 20
    }))

@dataclass
class Config:
    audio: AudioConfig = field(default_factory=AudioConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    tracker: TrackerConfig = field(default_factory=TrackerConfig)
