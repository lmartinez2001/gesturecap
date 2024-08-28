from typing import List

from mediapipe.tasks.python.components.containers import landmark as landmark_module

from mediapipe.framework.formats import landmark_pb2

def convert_to_landmark_list(normalized_landmarks: List[landmark_module.NormalizedLandmark]) -> landmark_pb2.NormalizedLandmarkList:
    landmark_list = landmark_pb2.NormalizedLandmarkList()
    for landmark in normalized_landmarks:
        new_landmark = landmark_list.landmark.add()
        new_landmark.x = landmark.x
        new_landmark.y = landmark.y
        new_landmark.z = landmark.z
    return landmark_list
