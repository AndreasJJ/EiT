# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2

# custom imports
from blink import blink
from eye import eye_aspect_ratio, compute_ear
from alarm import sound_warnings
from config import Config

# Use the following to execute: 
# "python src/__main__.py --shape-predictor src/datasets/shape_predictor_68_face_landmarks.dat -a src/audio/alarm.wav -n src/audio/notification.wav"

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
    help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="",
    help="path alarm .WAV file")
ap.add_argument("-n", "--notification", type=str, default="",
    help="path notofication .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
    help="index of webcam on system")
ap.add_argument("-na", "--name", type=str, default="NN",
		help="name of person using the system")
args = vars(ap.parse_args())

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm


FIRST = True
EYE_AR_THRESH = 0.2 # was 0.3
DAMPED_EAR = 0.3
DAMPING_WEIGHT = 0.07
EYE_AR_CONSEC_FRAMES = 48 # was 48 before
CONFIG_MIN_TIME = 10

# initialize the frame counter as well as a boolean used to
# indicate if the alarm is going off
COUNTER = 0
##moving_average = 0.3
##MOVING_AVERAGE_WEIGHT = 0.013
##SLEEPY_AVERAGE = 0.15
SLEEPY = False
ALARM_ON = False
NOTIFICATION_ON = False

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

blink = blink()

c1 = Config(EYE_AR_THRESH, CONFIG_MIN_TIME)

def kill():
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

def main():
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels)
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)


	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]

		# get the average eye aspect ratio
		ear = compute_ear(leftEye, rightEye)

		# if the eye was closed and is now open
		# there was a blink,





		global DAMPED_EAR
		# average the eye aspect ratio together for both eyes
		# Removed noise from ear with MA-filter (low pass filter)
		DAMPED_EAR = DAMPED_EAR + DAMPING_WEIGHT * (ear - DAMPED_EAR)
		EYE_AR_THRESH = c1.get_config_parameter(DAMPED_EAR)

		#calculates the moving average of the eye
		##moving_average = moving_average + MOVING_AVERAGE_WEIGHT * (ear - moving_average)

		global FIRST

		blink_score = blink.get_blink_score(ear, EYE_AR_THRESH, FIRST, args["name"])

		FIRST = False

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		global COUNTER
		##global moving_average
		global SLEEPY
		global ALARM_ON
		global NOTIFICATION_ON
		if DAMPED_EAR < EYE_AR_THRESH:
			COUNTER += 1

			# if the eyes were closed for a sufficient number of
			# then sound the alarm
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				# if the alarm is not on, turn it on
				if not ALARM_ON:
					ALARM_ON = True

					# check to see if an alarm file was supplied,
					# and if so, start a thread to have the alarm
					# sound played in the background
					if args["alarm"] != "":
						t1 = Thread(target=sound_warnings,
							args=(args["alarm"],))
						t1.deamon = True
						t1.start()

				# draw an alarm on the frame
				cv2.putText(frame, "WAKE UP!", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		# otherwise, the eye aspect ratio is not below the blink
		# threshold, so reset the counter and alarm
		else:
			COUNTER = 0
			ALARM_ON = False
		
		if SLEEPY:
			if not NOTIFICATION_ON: 
				NOTIFICATION_ON = True
				if args["notification"] != "":
						t2 = Thread(target=sound_warnings,
							args=(args["notification"],))
						t2.deamon = True
						t2.start()
			cv2.putText(frame, "Take a coffee or powernap", (10, 200),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		else: 
			NOTIFICATION_ON = False
		
		# draw the computed eye aspect ratio on the frame to help
		# with debugging and setting the correct eye aspect ratio
		# thresholds and frame counters
		cv2.putText(frame, "dampedEAR: {:.2f}".format(DAMPED_EAR), (200, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 50),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "tresh: {:.2f}".format(EYE_AR_THRESH), (300, 70),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
	# show the frame
	cv2.imshow("Frame", frame)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    while True:
        main()
        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    kill()