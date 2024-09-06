from .audio_generator import AudioGenerator
import pyaudio

class SinewaveGenerator(AudioGenerator):

    def __init__(self):
        raise NotImplementedError('Sinewave generator not implemented yet')

    def output_audio(self):
        raise NotImplementedError('Sinewave generator not implemented yet')

    def cleanup(self):
        raise NotImplementedError('Sinewave generator not implemented yet')

    def generate_sinewave(self):
        raise NotImplementedError('Sinewave generator not implemented yet')
