from .file_parsers import parse_yml
from video import *
from audio import *
from feature_extractor import *
from feature_mapper import *

import logging

logger = logging.getLogger(__name__)

class Scenario:
    """
    Wrapper class to create modules of the pipeline, based on a YAML scenario file.
    Modules are dynamically instanced with the content of the scenario file.
    This class is not meant to be changed as long as the logic of the pipeline is kept
    Pay close attention to the type returned by the modules. They may vary from one scenario to another, depending on module combinations.

    """
    def __init__(self, scenario_file: str):
        """
        Initializes a scenario

        Parameters
        ---
        scenario_file: str, required
            Path to the the yaml scenario file

        Attributes
        ---
        video_input: video.VideoInput

        feature_extractor: feature_extractor.FeatureExtractor
            Extracts relevant features from the captured frames in the context of the scenario
            see: class`feature_extractor.FeatureExtractor`

        feature_mapper: feature_mapper.FeatureMapper
            Instance of a feature mapper in charge of converting features extrated from the image to audio parameters

        audio_generator: audio_generator.AudioGenerator
            Instance of the audio module, responsible for outputing audio with parameters output by the feature mapper
        """
        self.parameters: dict = parse_yml(scenario_file)

        self.video_input = self._create_module('video_input')
        self.feature_extractor = self._create_module('feature_extractor')
        self.feature_mapper = self._create_module('feature_mapper')
        self.audio_generator = self._create_module('audio_generator')


    def _create_module(self, module_name: str):
        """
        Dynamically creates a module based on the scenario configuration

        Parameters:
        ---
        module_name: str
            The name of the module to create (e.g., 'video_input', 'feature_extractor')

        Returns:
        ---
        module: Any
            An instance of the specified module class, initialized with its parameters from the scenario
        """
        module_class = globals()[self.parameters[module_name]['class']]
        module_params = self.parameters[module_name].get('params', {})
        module = module_class(**module_params)
        return module
