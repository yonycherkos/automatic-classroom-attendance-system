# import the necessary packages
import face_recognition
import numpy as np
import argparse
import cv2

def alignFace(image, face_locations, face_landmarks):
	'''
	Let's find and angle of the face. First calculate 
	the center of left and right eye by using eye landmarks.
	'''
	leftEyePts = face_landmarks['left_eye']
	rightEyePts = face_landmarks['right_eye']

	leftEyeCenter = np.array(leftEyePts).mean(axis=0).astype("int")
	rightEyeCenter = np.array(rightEyePts).mean(axis=0).astype("int")

	leftEyeCenter = (leftEyeCenter[0],leftEyeCenter[1])
	rightEyeCenter = (rightEyeCenter[0],rightEyeCenter[1])

	# find and angle of line by using slop of the line.
	dY = rightEyeCenter[1] - leftEyeCenter[1]
	dX = rightEyeCenter[0] - leftEyeCenter[0]
	angle = np.degrees(np.arctan2(dY, dX))

	# to get the face at the center of the image,
	# set desired left eye location. Right eye location 
	# will be found out by using left eye location.
	# this location is in percentage.
	desiredLeftEye=(0.35, 0.35)
	#Set the croped image(face) size after rotaion.
	desiredFaceWidth = 128
	desiredFaceHeight = 128

	desiredRightEyeX = 1.0 - desiredLeftEye[0]
	
	# determine the scale of the new resulting image by taking
	# the ratio of the distance between eyes in the *current*
	# image to the ratio of distance between eyes in the
	# *desired* image
	dist = np.sqrt((dX ** 2) + (dY ** 2))
	desiredDist = (desiredRightEyeX - desiredLeftEye[0])
	desiredDist *= desiredFaceWidth
	scale = desiredDist / dist

	# compute center (x, y)-coordinates (i.e., the median point)
	# between the two eyes in the input image
	eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,
		(leftEyeCenter[1] + rightEyeCenter[1]) // 2)

	# grab the rotation matrix for rotating and scaling the face
	M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)

	# update the translation component of the matrix
	tX = desiredFaceWidth * 0.5
	tY = desiredFaceHeight * desiredLeftEye[1]
	M[0, 2] += (tX - eyesCenter[0])
	M[1, 2] += (tY - eyesCenter[1])

	# apply the affine transformation
	(w, h) = (desiredFaceWidth, desiredFaceHeight)
	(y2,x2,y1,x1) = face_locations 
			
	output = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)

	return output

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
	help="path to input image")
	args = vars(ap.parse_args())

	# load image and find face locations.
	image = cv2.imread(args["image"])
	face_locations = face_recognition.face_locations(image, model="hog")
	
	# detect 68-landmarks from image. This includes left eye, right eye, lips, eye brows, nose and chins
	face_landmarks = face_recognition.face_landmarks(image)

	for i in range(0, len(face_locations)):
		# align faces
		faceAligned = alignFace(image, face_locations[i], face_landmarks[i])
			
		# display the output images
		cv2.imshow("Original", image)
		cv2.imshow("Aligned", faceAligned)
		cv2.waitKey(0)																			