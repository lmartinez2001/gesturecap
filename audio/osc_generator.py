from typing import Dict, Any
from pythonosc import udp_client
from audio_generator import AudioGenerator

class SimpleOSCGenerator(AudioGenerator):

    def __init__(
            self,
            ip: str = '127.0.0.1',
            port: int = 11111,
    ):
        self.client = udp_client.SimpleUDPClient(osc_ip, osc_port)
        super().__init__()



    def update_data_to_send(self):
        assert (self.freq_route in params) and (self.vol_route in params)
        # Additional processing if required
        self.params: Dict[str, Any] = params


    def output_audio(self):
        """
        Ouputs OSC signals so that the actual sound generation is handled
        by an external tool (like puredata or Max/MSP)
        """
        for route, val in self.audio_params:
            self.client.send_message(route, val)
