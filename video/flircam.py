import cv2
import PySpin
import time
import logging

from .video_input import VideoInput

logger = logging.getLogger(__name__)

class Flircam(VideoInput):

    def __init__(self):
        self.system = None

        logger.debug('Finding camera')
        self.cam = self._find_camera()
        logger.debug('Camera found')
        logger.debug('Initializing camera')
        self.cam.Init()
        logger.debug('Camera initialized')
        # self.color_processor = self._init_color_processor(config.video.flir.color_processor) # TO BE CREATED
        self.color_processor = self._init_color_processor(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_NEAREST_NEIGHBOR) # TO BE CREATED
        super().__init__()


    def _find_camera(self) -> None:
        self.system = PySpin.System.GetInstance()
        version = self.system.GetLibraryVersion()
        logger.debug(f'Library version: {version.major}.{version.minor}.{version.type}.{version.build}')

        cam_list = self.system.GetCameras()
        logger.debug(f'{len(cam_list)} camera detected')
        if not cam_list.GetSize():
            raise Exception('No camera found')
        cam = cam_list[0]
        # del cam_list
        return cam


    def _init_color_processor(self, interpolation) -> PySpin.ImageProcessor:
        processor = PySpin.ImageProcessor()
        processor.SetColorProcessing(interpolation)
        return processor


    def configure(self):
        self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        self.cam.PixelFormat.SetValue(PySpin.PixelFormat_BayerRG8)
        self.cam.BinningHorizontal.SetValue(1)
        self.cam.BinningVertical.SetValue(1)
        max_width, max_height = self.cam.Width.GetMax(), self.cam.Height.GetMax()
        self.cam.Width.SetValue(max_width)
        self.cam.Height.SetValue(max_height)

        # Set frame rate to maximum possible
        self.cam.AcquisitionFrameRateEnable.SetValue(True)
        max_frame_rate = self.cam.AcquisitionFrameRate.GetMax()
        self.cam.AcquisitionFrameRate.SetValue(max_frame_rate)

        self.cam.TLStream.StreamBufferCountMode.SetValue(PySpin.StreamBufferCountMode_Manual)
        num_buffers_min = self.cam.TLStream.StreamBufferCountManual.GetMin()
        self.cam.TLStream.StreamBufferCountManual.SetValue(num_buffers_min)
        self.cam.TLStream.StreamBufferHandlingMode.SetValue(
            PySpin.StreamBufferHandlingMode_NewestOnly)

        # Disable auto exposure, auto gain, and auto white balance
        self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
        self.cam.GainAuto.SetValue(PySpin.GainAuto_Off)
        self.cam.BalanceWhiteAuto.SetValue(PySpin.BalanceWhiteAuto_Off)

        # Set ADC bit depth to 10 bits
        self.cam.AdcBitDepth.SetValue(PySpin.AdcBitDepth_Bit8)

        # Set exposure time and limits
        # self.cam.ExposureTime.SetValue(self.config.video.exposure_time)  # in microseconds
        self.cam.ExposureTime.SetValue(500)  # in microseconds

        # Enable chunk data mode
        self.cam.ChunkModeActive.SetValue(True)

        # Enable timestamp
        self.cam.ChunkSelector.SetValue(PySpin.ChunkSelector_Timestamp)
        self.cam.ChunkEnable.SetValue(True)

        logger.debug(f'Camera frame rate set to: {self.cam.AcquisitionFrameRate.GetValue()} fps')
        logger.debug(f'Camera buffer size set to: {num_buffers_min}')

        # LOGIC TO BE CHANGED
        logger.info('Beginning frame acquisition')
        self.cam.BeginAcquisition()


    def read_frame(self):
        try:
            frame_cam = self.cam.GetNextImage()
            if frame_cam.IsIncomplete():
                logger.warning('Image incomplete')
                return None
            frame_conv = self.color_processor.Convert(frame_cam, PySpin.PixelFormat_BGR8)
            frame = frame_conv.GetNDArray()
            frame.flags.writeable = True
            frame_cam.Release()
            return frame
        except PySpin.SpinnakerException as e:
            logger.exception(e)


    def cleanup(self):
        self.cam.EndAcquisition()
        self.cam.DeInit()
        del self.cam
        self.system.ReleaseInstance()
        logger.debug('Released Flir camera')



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cam = Flircam()
    cam.start()

    frame_count = 0
    start_time = time.time()
    fps = 0
    try:
        while cam.is_running:
            frame = cam.get_frame()

            # Calculate FPS
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:  # Update FPS every second
                fps = frame_count / elapsed_time
                frame_count = 0
                start_time = time.time()

            # Display FPS on the frame
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            cv2.imshow('Test', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cam.stop()
        cv2.destroyAllWindows()
