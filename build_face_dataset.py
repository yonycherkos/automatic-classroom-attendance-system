# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os

# construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", help="path to model prototxt file")
ap.add_argument("-m", "--model", help="path to model weight file")
ap.add_argument("-o", "--output", help="directory path to put detect faces")
ap.add_argument("-c", "--confidence", default=0.5, type=str, help="confidence to filter weak predictions")
args = vars(ap.parse_args())

# track the number of face detected
total = 0

# load the face detector model
print("[INFO] loading face detector model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# start video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2)

while True:
    # read current frame
    frame = vs.read()
    orig = frame.copy()
    (h, w) = frame.shape[:2]

    # preprocess the frame
    resized = cv2.resize(frame, (300, 300))
    blob = cv2.dnn.blobFromImage(resized,  scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))

    # pass the process frame through the network
    net.setInput(blob)
    detections = net.forward()

    # loop over the detect faces
    idx = np.argmax(detections[0, 0, :, 2])
    confidence = detections[0, 0, idx, 2]
    if confidence > args["confidence"]:
        # extract the bounding box
        box = detections[0, 0, idx, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # draw the boundidxbox = detections[0, 0, idxng box the frame
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
        text = "{:.2f}".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        # display the detected faces
        cv2.imshow("detected face", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("k"):
            if not os.path.exists(args["output"]):
                os.makedirs(args["output"])
            p = os.path.sep.join([args["output"], "{}.png".format(str(total).zfill(5))])
            cv2.imwrite(p, orig)
            total += 1
        elif key == ord("q"):
            break

print("[INFO] {} face saved to disk".format(total))
print("[INFO] cleaning up")
cv2.destroyAllWindows()
vs.stop()