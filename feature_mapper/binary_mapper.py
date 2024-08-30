from .mapper import Mapper


class PulseMapper(Mapper):

    def __init__(self, threshold: float):
        self.thresh = threshold


    def process_detection_results(self, value: float):
        mapped = {
            'pulse': 0
        }

        if value > self.thresh:
            mapped = {
                'pulse': 1
            }

        return mapped
