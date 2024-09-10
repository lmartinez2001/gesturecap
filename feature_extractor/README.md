# Tutorial: Implementing the `pose_landmarker` script

In GestureCap, a feature refers to any data which can be extracted from a single frame or a set of frames. Extrated features are then processed by the Feature Mapper module to link it with audio parameters.  
Currently the project handles three types of features:
1. Landmarks as 3D coordinates
2. Handedness when we're interest on hand landmarks detection
3. Frame difference as the mean absolute pixel wise difference between two images (this feature is mainly used for timing measurement purposes) 


In this tutorial, we will create a `pose_landmarker` script that detects body landmarks. It's a wrapper around the Mediapipe `PoseLandmarker_Lite` model.  

> [!NOTE]
> The `pose_landmarker` feature extractor is nothing more but a copy of the the already existing `hand_landmarker` script in the same package. The only difference lies in the `.task` file used by mediapipe under the wood to run the model. However, the implementation of any more complex feature extractor will follow the exact same steps explained bellow.

> [!TIP]
> Medipipe code snippets used here are copied as is from the [Google developer](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/python) website. For more detailed information about these instructions, please refer to Google website.

## 1. Create the `pose_landmarker.py` file

Navigate to the `feature_extractor` directory within your project and create a new Python file named `pose_landmarker.py`.

``` bash
cd feature_mapper
touch pose_landmarker.py
```


## 2. Import necessary modules


Open `pose_landmarker.py` and import the required modules:

``` python
# Super class
from .feature_extractor import FeatureExtractor

import cv2
import numpy as np

# Mediapipe model
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
```

## 3. Define the `PoseLandmarker` class

Create a class named `PoseLandmarker` that inherits from the `FeatureExtractor` class.

``` python
class PoseLandmarker(FeatureExtractor):

    def __init__(self, device: str = 'cpu'):
        # Setting up mediapipe model
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        base_options = python.BaseOptions(
            model_asset_path='pose_landmarker_lite.task',  # You'll need to download this model
            delegate=python.BaseOptions.Delegate.GPU if device == 'gpu' else python.BaseOptions.Delegate.CPU
        )
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False,  # Optional, for segmenting the person from the background
        )
        self.pose = vision.PoseLandmarker.create_from_options(options)

```
    

## 4. Implement the `process` abstract method

The `process` method is defined in the `FeatureExtractor` super class. It's called at each iteration of the main loop of the program. This method will run the Mediapipe `Pose landmarker` model and return detected landmarks in a dictionary.


``` python
    def process(self, image):
        # Convert grabbed BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Run mediapipe pipeline on the frame
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        detection_result = self.pose.detect(mp_image)
        
        # Reformat detection results
        res = {
            'landmarks': detection_result.pose_landmarks,
        }
        
        return res

```

## 5. Update `feature_extractor/__init__.py`

Import and add the `PoseLandmarker` class to the `__all__` list in `feature_extractor/__init__.py`.

``` python
# ... other imports
from .pose_landmarker import PoseLandmarker

__all__ = [
    # ... other mappers
    'PoseLandmarker'
]
```

## 6. (Optional) Use the newly created module in a scenario file (located in `scenarios` directory)

> [!CAUTION]
> For now, the `PoseLandmarker` script isn't intended to be used with any other module. However, the provided scenario will work as it won't throw any error, but the output `Audio Parameter` might be meaningless. concretely, the barycenter of all the detected landmarks exists but might have some awkward position, according to how the user stands in front of the camera

Navigate to the `scenarios` directory and open any `.yml` scenario file.
Fill the file with the following configuration:

``` yaml

scenario: Some demo

video_input:
  class: Webcam
  params:
    cam_index: 0

feature_extractor:
  class: PoseLandmarker # Uses the newly created PoseLandmarker module

feature_mapper:
  class: BarycenterMapper # Computes the barycenter all the detected landmarks

audio_generator:
  class: OSCGenerator
  params:
    ip: "127.0.0.1"
    port: 11111
```


## 7. (Optional) Run the program with the new configuration

First make sure that the corresponding Pure Data patch. In this tutorial, the `puredata/barycenter_demo.pd` patch created for the tutorial on how to create a feature extractor will work.

1. In PureData go to `File ->  Open` and select the `barycenter_demo.pd` file
<div align="center"><img src="../assets/images/gesturecap_pd_open_script.png" alt="Opening a script"></div>
<div align="center"><img src="../assets/images/gesturecap_pd_diagram_structure.png" alt="Diagram structure"></div>

2. Locate the *Play/Pause the melody* check box and tick it. You should hear a melody
<div align="center"><img src="../assets/images/gesturecap_pd_play_melody_box.png" alt="Play/Pause box"></div>

3. Start the main program:

``` bash
python main.py --scenario scenarios/<your_scenario_file>.yml
```

A display should appear and moving in front of the camera will change the output audio.

## Useful links
<a id="useful-links"></a>

- [Blog page from which the PureData scripof t is widely inspired](https://reallyusefulplugins.tumblr.com/richsynthesis)
- [Google tutorial to setup the PoseLandmarker model](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/python)
