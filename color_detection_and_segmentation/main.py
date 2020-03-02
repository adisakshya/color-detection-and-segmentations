# Logger Function
def log(label, message):
	print('[{}] => {}'.format(label, message))

# Import required modules
try:
	import cv2
	import numpy as np
	import time	 
except Exception as error:
	log('ERROR', error)

# Versions of modules used
log('INFO', 'OpenCV Version: ' + cv2.__version__)
log('INFO', 'NumPy Version: ' + np.__version__)

# Capture Video
capture_video = cv2.VideoCapture(0)

# Let the camera warm up
log('INFO', 'Warming up camera')
time.sleep(1) 

# Variable to store background
background = None

# Capture the background
log('INFO', 'Capturing background')
for i in range(60):
	return_val, background = capture_video.read()
	if return_val == False :
		continue 

# Flip background
background = np.flip(background, axis=1)

# Reading from video 
log('INFO', 'Capturing from video')
while (capture_video.isOpened()):
	
	try:

		# Read image
		return_val, image = capture_video.read()
		if not return_val :
			break 
		
		# Flip the image
		image = np.flip(image, axis=1)
		
		# Transform BGR to HSV
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		
		# Generate mask to detect red color
		# lower range 1
		lower_red = np.array([100, 40, 40])
		# upper range 1
		upper_red = np.array([100, 255, 255])
		# Mask 1
		mask1 = cv2.inRange(hsv,lower_red, upper_red)

		# lower range 2
		lower_red = np.array([155, 40, 40])
		# upper range 2
		upper_red = np.array([180, 255, 255])
		# Mask 2
		mask2 = cv2.inRange(hsv,lower_red, upper_red)

		# Mask to detect red color
		mask1 = mask1 + mask2

		# Refining the mask corresponding to the detected red color
		mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=2)
		mask1 = cv2.dilate(mask1, np.ones((3,3), np.uint8), iterations = 1)
		mask2 = cv2.bitwise_not(mask1)

		# Generating the final output
		res1 = cv2.bitwise_and(background, background, mask=mask1)
		res2 = cv2.bitwise_and(image, image, mask=mask2)
		final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

		cv2.imshow("Color Detection & Segmentation", final_output)
		k = cv2.waitKey(10)
		if k == 27:
			log('INFO', 'Exiting')
			break
	
	except Exception as error:

		log('ERROR', error)
		log('INFO', 'Exiting')
		break