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


@dataclass
class Config:
    audio: AudioConfig = field(default_factory=AudioConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    tracker: TrackerConfig = field(default_factory=TrackerConfig)
