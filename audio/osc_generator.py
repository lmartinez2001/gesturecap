from typing import Dict, Any
from pythonosc import udp_client
from .audio_generator import AudioGenerator
import logging


logger = logging.getLogger(__name__)


class OSCGenerator(AudioGenerator):

    def __init__(self, ip: str = '127.0.0.1', port: int = 11111):
        super().__init__()
        self.client = udp_client.SimpleUDPClient(ip, port)
        logger.info(f'OSC generator initialized at {ip}:{port}')


    def output_audio(self):
        """
        Ouputs OSC signals so that the actual sound generation is handled
        by an external tool (like puredata or Max/MSP)
        """
        if self.data_to_send:

            if type(self.data_to_send) != dict:
                raise TypeError('OSC generator expects dict type with format Dict[str, Any]')
            else:
                for route, val in self.data_to_send.items():
                    route = f'/{route}' if not route.startswith('/') else route
                    self.client.send_message(route, val)
                    # logger.debug(f'Sent {val} to {route} route')


    def cleanup(self):
        pass
