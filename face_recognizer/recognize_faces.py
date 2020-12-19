# import the necessary packages
from detect_faces import face_detection
from imutils import paths
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import os

# construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to input image")
ap.add_argument("-e", "--encodings", help="path to face encodings")
ap.add_argument("-d", "--detection_method", default="hog", type=str, help="detection method to use 'hog' or 'cnn' ")
ap.add_argument("-p", "--prototxt", help="path to caffe protxt file")
ap.add_argument("-m", "--model", help="path to caffe pre-trained model file")
ap.add_argument("-c", "--confidence", default=0.5, type=float,
                help="minimum dection confidence to filter weeak detection")
args = vars(ap.parse_args())

# load face encodings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# load input image and preproces it
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# recognizing faces
print("[INFO] detecting faces...")
start = time.time()
# boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
(boxes, _) = face_detection(image, args["prototxt"], args["model"], args["confidence"])
boxes = [(box[1], box[2], box[3], box[0]) for (i, box) in enumerate(boxes)]
end = time.time()
print("[INFO] face detection tooks: {} ms".format((end - start)*1000))

print("[INFO] encoding faces...")
encodings = face_recognition.face_encodings(rgb, boxes)
names = []

# loop over encodings
print("[INFO] matching faces...")
for encoding in encodings:
    matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)
    name = "Unknown"
    if True in matches:
        matchIdxs = [i for (i, match) in enumerate(matches) if match]
        counts = {}
        for i in matchIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1
        name = max(counts, key=counts.get)
    names.append(name)

# loop over the recognized faces
for ((top, right, bottom, left), name) in zip(boxes, names):
	# draw the predicted face name on the image
	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
	y = top - 15 if top - 15 > 15 else top + 15
	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
		0.75, (0, 255, 0), 2)

# show the output image
cv2.imwrite("output/yony.jpg", image)
cv2.imshow("Image", image)
cv2.waitKey(0)
        