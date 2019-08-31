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

# read from video
while (capture_video.isOpened()):

    flag, img = capture_video.read()
    if not flag:
    	break
    count += 1

    img = np.flip(img, axis=1)

	# convert image - BGR to HSV
	# focus on detection of red color
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)