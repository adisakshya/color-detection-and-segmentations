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

    # generate mask to detect red color
    l_red = np.array([100, 40, 40])
    u_red = np.array([100, 255, 255])
    mask_a = cv2.inRange(hsv, l_red, u_red)

    l_red = np.array([155, 40, 40])
    u_red = np.array([180, 255, 255])
    mask_b = cv2.inRange(hsv,l_red, u_red)

    mask = mask_a + mask_b

    # Refining the mask corresponding to the detected red color
    mask_a = cv2.morphologyEx(mask_a, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
    mask_b = cv2.dilate(mask_a,np.ones((3,3),np.uint8),iterations = 1)
    mask_b = cv2.bitwise_not(mask_a)