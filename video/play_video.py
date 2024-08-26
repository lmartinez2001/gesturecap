#!/usr/bin/env python3

import os
import cv2


def play_video(path):
    home = os.environ['HOME']
    video_root = os.path.join(home, 'Videos', 'blackfly')

    video = cv2.VideoCapture(os.path.join(video_root, '18_29_00Uncompressed-0001.avi'))

    original_fps = video.get(cv2.CAP_PROP_FPS)

    desired_fps = 200

    delay = int(1000 / desired_fps)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
