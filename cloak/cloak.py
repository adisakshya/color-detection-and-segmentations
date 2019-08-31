import cv2, time, numpy as np

print('OpenCV Version:',cv2.__version__)

# video capture
capture_video = cv2.VideoCapture(0)


time.sleep(1)
count = 0
background = 0

# capture background
for i in range(60):
    flag, background = capture_video.read()
    if not flag:
        continue

background = np.flip(background, axis=1)