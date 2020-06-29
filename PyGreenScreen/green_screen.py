import cv2
import numpy as np
from getpass import getuser


"""

A basic green screen software written with PyGreenScreen

"""


class GreenScreenApp:
    def __init__(self, gs_vid_path, gs_background_img_path, vid_dimensions):
        self.gs_vid = cv2.VideoCapture(gs_vid_path)
        self.gs_background_img = cv2.imread(gs_background_img_path)
        self.vid_dimensions = vid_dimensions

        self.col_threshold = [[0, 0, 0], [0, 0, 0]]  # lower, upper

        self.ENTER_KEY = 13
        self.CALIBRATION_WIN_NAME = 'Calibrate Threshold'
        self.OUTPUT_FILE_PATH = f'C:/Users/{getuser()}/Desktop/output.mp4'
        self.CALIBRATION_WIN_SIZE = (600, 400)

        self.CALIBRATION_INSTRUCTIONS = """        -------------------
        Drag the track bars provided to adjust the upper and lower colour threshold values such that the image below
        appears as desired.
        
        Once satisfied with your choice, press 'ENTER' to confirm.
        -------------------"""

        self.instructions_have_been_displayed = False
        self.processing_finished_has_been_displayed = False

    def _first_frame(self):
        """Returns first frame of video for colour threshold calibration"""

        success, frame = self.gs_vid.read()  # If frame is not read correctly, success == False

        if not success:
            print('Error: Cannot read first frame')

        else:
            return cv2.resize(frame, self.vid_dimensions)

    def _init_col_track_bar(self):
        """Initialize the calibration track bars"""

        cv2.namedWindow(self.CALIBRATION_WIN_NAME)

        cv2.createTrackbar('Upper R', self.CALIBRATION_WIN_NAME, 0, 255, self._do_nothing)
        cv2.createTrackbar('Upper G', self.CALIBRATION_WIN_NAME, 0, 255, self._do_nothing)
        cv2.createTrackbar('Upper B', self.CALIBRATION_WIN_NAME, 0, 255, self._do_nothing)

        cv2.createTrackbar('Lower R', self.CALIBRATION_WIN_NAME, 0, 255, self._do_nothing)
        cv2.createTrackbar('Lower G', self.CALIBRATION_WIN_NAME, 0, 255, self._do_nothing)
        cv2.createTrackbar('Lower B', self.CALIBRATION_WIN_NAME, 0, 255, self._do_nothing)

    def first_frame_threshold_calibration(self):
        self._init_col_track_bar()
        ff = self._first_frame()

        while 1:
            ur = cv2.getTrackbarPos('Upper R', self.CALIBRATION_WIN_NAME)
            ug = cv2.getTrackbarPos('Upper G', self.CALIBRATION_WIN_NAME)
            ub = cv2.getTrackbarPos('Upper B', self.CALIBRATION_WIN_NAME)

            lr = cv2.getTrackbarPos('Lower R', self.CALIBRATION_WIN_NAME)
            lg = cv2.getTrackbarPos('Lower G', self.CALIBRATION_WIN_NAME)
            lb = cv2.getTrackbarPos('Lower B', self.CALIBRATION_WIN_NAME)

            u_green = np.array([ub, ug, ur])  # BGR
            l_green = np.array([lb, lg, lr])

            frame = cv2.resize(ff, self.CALIBRATION_WIN_SIZE)
            image = cv2.resize(self.gs_background_img, self.CALIBRATION_WIN_SIZE)

            mask = cv2.inRange(frame, l_green, u_green)
            res = cv2.bitwise_and(frame, frame, mask=mask)

            f = frame - res
            f = np.where(f == 0, image, f)

            cv2.imshow(self.CALIBRATION_WIN_NAME, f)

            if cv2.waitKey(25) == self.ENTER_KEY:
                self.col_threshold = [l_green, u_green]  # Update the threshold on escape
                break

            if not self.instructions_have_been_displayed:
                print(self.CALIBRATION_INSTRUCTIONS)
                self.instructions_have_been_displayed = True

        cv2.destroyAllWindows()

    def output_with_current_threshold(self):

        confirm_text = f"""        -------------------
        Your selected colour threshold is:

        Upper Green: RGB{self.col_threshold[1]}
        Lower Green: RGB{self.col_threshold[0]}
        
        Processing starts now.

        The result will appear on your Desktop.
        -------------------"""

        print(confirm_text)
        out = cv2.VideoWriter(self.OUTPUT_FILE_PATH, -1, 20.0, self.vid_dimensions)

        while 1:
            ret, frame = self.gs_vid.read()

            if not ret:
                break

            frame = cv2.resize(frame, self.vid_dimensions)
            image = cv2.resize(self.gs_background_img, self.vid_dimensions)

            mask = cv2.inRange(frame, self.col_threshold[0], self.col_threshold[1])
            res = cv2.bitwise_and(frame, frame, mask=mask)

            f = frame - res
            f = np.where(f == 0, image, f)

            out.write(f)

            if not self.processing_finished_has_been_displayed:
                print('Processing...')
                self.processing_finished_has_been_displayed = True

        out.release()

    @staticmethod
    def _do_nothing(x):
        pass


"""

Lazy User Interface hahahahahahaahha

"""

APP_NAME = 'PyGreenScreen'

print("""Welcome to python-green-screen!
----------------------------------
Keep this window open as it will be your interface for input and output.

To begin,""")

vid_path = input('Enter green screen video file path: ')
img_path = input('Enter green screen background image file path: ')

size = (int(input('Enter desired final video width (integer): ')), int(input('Enter desired final video height (integer): ')))

gs = GreenScreenApp(gs_vid_path=vid_path, gs_background_img_path=img_path, vid_dimensions=size)
gs.first_frame_threshold_calibration()
gs.output_with_current_threshold()

print('Processing completed')