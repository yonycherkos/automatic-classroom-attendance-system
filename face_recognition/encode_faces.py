# import the necessary packages
from imutils.face_utils import FaceAligner
from detect_faces import face_detection
from imutils import paths
import face_recognition
import pandas as pd
import argparse
import imutils
import pickle
import cv2
import os

# construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", help="path to face + images dataset")
ap.add_argument("-e", "--encodings", help="path to output face encodings")
ap.add_argument("-c", "--csv", help="path to output csv file.")
ap.add_argument("-dm", "--detection_method", default="hog",
                type=str, help="detection method to use 'hog' or 'cnn' ")
ap.add_argument("-p", "--prototxt", help="path to caffe protxt file")
ap.add_argument("-m", "--model", help="path to caffe pre-trained model file")
ap.add_argument("-t", "--confidence", default=0.5, type=float,
                help="minimum dection confidence to filter weeak detection")
args = vars(ap.parse_args())

# extract image paths and intialize empty encoding and names array.
image_paths = list(paths.list_images(args["dataset"]))
knowEncodings = []
KnowNames = []

# loop over image paths
for (i, image_path) in enumerate(image_paths):
    print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))
    name = image_path.split(os.path.sep)[-2]

    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # boxes = face_recognition.face_locations(
    #     rgb, model=args["detection_method"])
    (boxes, _) = face_detection(image, args["prototxt"], args["model"], args["confidence"])
    boxes = [(box[1], box[2], box[3], box[0]) for (i, box) in enumerate(boxes)]
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
        knowEncodings.append(encoding)
        KnowNames.append(name)

# if there are registers faces
if os.path.exists(args["csv"]) and os.path.exists(args["encodings"]):
    # append new encodings to the existing one
    with open(args["encodings"], "rb") as f:
        print("[INFO] loading encodings...")
        data = pickle.loads(f.read())
        data["names"].extend(KnowNames)
        data["encodings"].extend(knowEncodings)
    with open(args["encodings"], "wb") as f:
        print("[INFO] serialize encodings to disk...")
        f.write(pickle.dumps(data))

    # append new dataframe to the existing one.
    df = pd.read_csv(args["csv"], index_col=0)
    new_df = pd.DataFrame(columns=df.columns)
    new_df['names'] = list(set(KnowNames))
    new_df = new_df.fillna(0)

    df = df.append(new_df)
    df = df.sort_values(by='names')
    df = df.reset_index(drop=True)
    print("[INFO] storing additional student names in a dataframe...")
    df.to_csv(args["csv"])
else:
    # serialize encodings to disk
    print("[INFO] serialize encodings to disk...")
    data = {"names": KnowNames, "encodings": knowEncodings}
    f = open(args["encodings"], "wb")
    f.write(pickle.dumps(data))
    f.close()

    # stroring the names in dataframe
    print("[INFO] storing student names in a dataframe...")
    df = pd.DataFrame({"names": sorted(list(set(KnowNames)))})
    df.to_csv(args["csv"])
