from .file_parsers import parse_yml
from video import *
from audio import *
from feature_extractor import *
from feature_mapper import *

import logging

logger = logging.getLogger(__name__)

class Scenario:

    def __init__(self, scenario_file: str):
        self.parameters: dict = parse_yml(scenario_file)

        self.video_input = self._create_module('video_input')
        self.feature_extractor = self._create_module('feature_extractor')
        self.feature_mapper = self._create_module('feature_mapper')
        self.audio_generator = self._create_module('audio_generator')


    def _create_module(self, module_name: str):
        module_class = globals()[self.parameters[module_name]['class']]
        module_params = self.parameters[module_name].get('params', {})
        module = module_class(**module_params)
        return module
