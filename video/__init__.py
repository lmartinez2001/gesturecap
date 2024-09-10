# if PySpin:
#     from .flircam import Flircam
# else:
#     Flircam = None
import importlib.util

from .webcam import Webcam

# Conditional import whether spinnaker-python is installed or not
if importlib.util.find_spec('PySpin'):
    from .flircam import Flircam
    __all__ = ['Flircam', 'Webcam']
else:
    __all__ = ['Webcam']
