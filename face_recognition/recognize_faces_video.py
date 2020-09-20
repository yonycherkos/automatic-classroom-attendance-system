# import the necessary packages
from imutils.video import VideoStream
from datetime import datetime
from imutils import paths
import face_recognition
import pandas as pd
import argparse
import imutils
import pickle
import time
import cv2
import os

# construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", help="path to face encodings")
ap.add_argument("-c", "--csv", help="path to output csv file.")
ap.add_argument("-o", "--output", default=None, type=str,
                help="path to output video file")
ap.add_argument("-d", "--detection_method", default="hog",
                type=str, help="detection method to use 'hog' or 'cnn' ")
args = vars(ap.parse_args())

# load face encodings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# initilize face occurance counters
faceCounter = {name: 0 for name in data["names"]}

# start video stream and warming up the camera
print("[INFO] start video stream...")
vs = VideoStream(src=0).start()
writer = None
time.sleep(2)

while True:
    # load current frame and convert it to rgb color
    frame = vs.read()
    frame = imutils.resize(frame, width=750)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    r = frame.shape[1] / float(rgb.shape[1])

    # recognizing faces
    boxes = face_recognition.face_locations(
        rgb, model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over encodings
    for encoding in encodings:
        matches = face_recognition.compare_faces(
            data["encodings"], encoding, tolerance=0.5)
        name = "Unknown"
        if True in matches:
            matchIdxs = [i for (i, match) in enumerate(matches) if match]
            counts = {}
            for i in matchIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
            faceCounter[name] = faceCounter.get(name, 0) + 1
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # resize the bounding boxes
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        # draw the predicted face name on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    # save the frame
    if writer is None and args["output"] is not None:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(
            args["output"], fourcc, 20.0, (frame.shape[1], frame.shape[0]), True)

    if writer is not None:
        writer.write(frame)

    # show the output frame
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# append current attendance result to the dataframe
faceCounter = {key: 1 if value >=
               30 else 0 for(key, value) in faceCounter.items()}
date_col = datetime.now().strftime("%Y-%m-%d %H:%M")
df = pd.read_csv(args["csv"], index_col=0)
df[date_col] = df["names"].map(lambda name: faceCounter[name])
print("[INOF] writing attendance result to the csv file...")
df.to_csv(args["csv"])
print(df)

# cleaning up
print("[INFO] cleaning up")
cv2.destroyAllWindows()
vs.stop()

if writer is not None:
    writer.release()

# Futur works
# TODO: add face alignmnt
# TODO: use only a single image of a person for registration.
# TODO: improve the face detection model or use other model.
# TODO: add image enhancement feature
