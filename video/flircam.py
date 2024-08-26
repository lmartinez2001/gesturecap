#!/usr/bin/env python3

import logging
import cv2
import PySpin

logger = logging.getLogger(__name__)

class Camera(object):
    def __init__(self, cam: PySpin.CameraPtr):
        self.cam = cam
        self.cam.Init()

    def stop(self):
        logger.debug('Cleaning up')
        self.cam.DeInit()
        del self.cam
        self.cam = None

    def configure(self):
        self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        # self.cam.PixelFormat.SetValue(PySpin.PixelFormat_Mono8)
        self.cam.PixelFormat.SetValue(PySpin.PixelFormat_BGR8)
        # self.cam.RgbTransformLightSource(PySpin.SPINNAKER_CCM_COLOR_TEMP_GENERAL)
        self.cam.BinningHorizontal.SetValue(1)
        self.cam.BinningVertical.SetValue(1)
        self.cam.Width.SetValue(720)
        self.cam.Height.SetValue(540)
        self.cam.AcquisitionFrameRateEnable.SetValue(True)
        self.cam.AcquisitionFrameRate.SetValue(250)
        self.cam.TLStream.StreamBufferCountMode.SetValue(PySpin.StreamBufferCountMode_Manual)
        self.cam.TLStream.StreamBufferCountManual.SetValue(1)
        self.cam.TLStream.StreamBufferHandlingMode.SetValue(
            PySpin.StreamBufferHandlingMode_NewestOnly)

    def show_image(self, data):
        print(data.shape)
        cv2.imshow('image', data)
        cv2.waitKey(1)

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
                # comes from the original code but not essential here as the camera is mono

                img_conv = processor.Convert(img, PySpin.PixelFormat_BGR8)
                # or img.GetData().tobytes() for pushing into gstreamer buffers
                self.show_image(img_conv.GetNDArray())

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
    camera = Camera(cam)
    try:
        camera.run()
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        system.ReleaseInstance()


if __name__ == '__main__':
    main()
