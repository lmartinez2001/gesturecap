import time
import cv2
import PySpin
import logging
from Gestures.src.hand_pose_detector import HandPoseDetector

logger = logging.getLogger(__name__)

class Camera(object):
    def __init__(self, cam: PySpin.CameraPtr, draw_lms: bool):
        self.cam = cam
        self.cam.Init()
        self.detector = HandPoseDetector()
        self.draw_lms = draw_lms
        self.prev_frame_time = 0
        self.new_frame_time = 0
    
    def stop(self):
        logger.debug('Cleaning up')
        self.cam.DeInit()
        del self.cam
        self.cam = None

    def configure(self):
        self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        self.cam.PixelFormat.SetValue(PySpin.PixelFormat_BGR8)
        self.cam.BinningHorizontal.SetValue(1)
        self.cam.BinningVertical.SetValue(1)
        self.cam.Width.SetValue(720)
        self.cam.Height.SetValue(540)
        self.cam.AcquisitionFrameRateEnable.SetValue(True)
        self.cam.AcquisitionFrameRate.SetValue(200)
        self.cam.TLStream.StreamBufferCountMode.SetValue(PySpin.StreamBufferCountMode_Manual)
        self.cam.TLStream.StreamBufferCountManual.SetValue(1)
        self.cam.TLStream.StreamBufferHandlingMode.SetValue(
            PySpin.StreamBufferHandlingMode_NewestOnly)

    def show_image(self, data):
        cv2.imshow('image', data)
        cv2.waitKey(1)

    def calculate_fps(self):
        self.new_frame_time = time.time()
        fps = 1 / (self.new_frame_time - self.prev_frame_time)
        self.prev_frame_time = self.new_frame_time
        return int(fps)

    def draw_fps(self, image, fps):
        cv2.putText(image, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def run(self):
        processor = PySpin.ImageProcessor()
        processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)
        logger.debug('Starting')
        self.configure()
        self.cam.BeginAcquisition()
        try:
            logger.debug('Streaming')
            while True:
                img = self.cam.GetNextImage()
                if img.IsIncomplete():
                    logger.warning('Image incomplete (%d)',
                                   img.GetImageStatus())
                    continue
                img_conv = processor.Convert(img, PySpin.PixelFormat_BGR8)
                im = img_conv.GetNDArray()
                im.flags.writeable = True
                hand_landmarks = self.detector.detect_hand_pose(im)
                if self.draw_lms:
                    im = self.detector.draw_landmarks(im, hand_landmarks)
                
                fps = self.calculate_fps()
                self.draw_fps(im, fps)
                
                self.show_image(im)
                img.Release()
        except PySpin.SpinnakerException as e:
            logger.exception(e)
        finally:
            logger.debug('Ending')
            self.cam.EndAcquisition()

def main():
    logging.basicConfig(level=logging.DEBUG)
    system = PySpin.System.GetInstance()
    version = system.GetLibraryVersion()
    logger.debug('Library version: %d.%d.%d.%d',
                 version.major, version.minor, version.type, version.build)
    cam_list = system.GetCameras()
    if not cam_list.GetSize():
        logger.error('No cameras found')
        return
    cam = cam_list[0]
    del cam_list
    camera = Camera(cam, draw_lms=True)
    try:
        camera.run()
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        system.ReleaseInstance()


if __name__ == '__main__':
    main()
