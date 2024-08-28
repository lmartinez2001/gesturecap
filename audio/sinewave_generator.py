from .audio_generator import AudioGenerator
import pyaudio

"""
This class is not generic enough as it only handles sinewaves. However it demonstrates how to use the current framework to directly trigger the sound card.
The goal at the end will be to have a more abstract handler for audio signals directly triggering the sound card
Moreover, this class takes audio params as a dictionary, but could be adapted to handle other data formats, like STFT images
"""

class SinewaveGenerator(AudioGenerator):

    def __init__(self):
        pass

    def output_audio(self):
        if self.data_to_send:
            if type(self.data_to_send) != dict:
                    raise TypeError('OSC generator expects dict type with format Dict[str, Any]')
            else:
                print('test')

    def cleanup(self):
        pass


    def generate_sinewave(self):
