from PyGreenScreen import green_screen

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

gs = green_screen.GreenScreenApp(gs_vid_path=vid_path, gs_background_img_path=img_path, vid_dimensions=size)
gs.first_frame_threshold_calibration()
gs.output_with_current_threshold()

print('Processing completed')
