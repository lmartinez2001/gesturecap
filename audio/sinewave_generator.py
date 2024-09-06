from .audio_generator import AudioGenerator
import pyaudio

"""
This class is not generic enough as it only handles sinewaves. However it demonstrates how to use the current framework to directly trigger the sound card.
The goal at the end will be to have a more abstract handler for audio signals directly triggering the sound card
Moreover, this class takes audio params as a dictionary, but could be adapted to handle other data formats, like STFT images
"""

class SinewaveGenerator(AudioGenerator):

    def __init__(self):
        raise NotImplementedError('Sinewave generator not implemented yet')

    def output_audio(self):
        raise NotImplementedError('Sinewave generator not implemented yet')

    def cleanup(self):
        raise NotImplementedError('Sinewave generator not implemented yet')

    def generate_sinewave(self):
        raise NotImplementedError('Sinewave generator not implemented yet')
