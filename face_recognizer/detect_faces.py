# import the necessary packages
import numpy as np
import face_recognition
import argparse
import imutils
import time
import cv2

def face_detection(image, prototxt, model, min_confidence=0.5):
    (h, w) = image.shape[:2]

    # note: we need to resize to image to the desired size
    resized = cv2.resize(image, (300, 300))
    blob = cv2.dnn.blobFromImage(resized, scalefactor=1.0, size=(
        300, 300), mean=(104.0, 177.0, 123.0))

    # load the pretrained model
    # print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # pass the processed image through the network
    # print("[INFO] computing face detection...")
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    boxes = []
    confidences = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > min_confidence:
            # get the bounding box
            box = detections[0, 0, i, 3:7]*np.array([w, h, w, h])
            boxes.append(box.astype("int"))
            confidences.append(confidence)

    return (boxes, confidences)

if __name__ == "__main__":
    # construct argument parse and parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="path to input image")
    ap.add_argument("-p", "--prototxt", help="path to caffe protxt file")
    ap.add_argument("-m", "--model", help="path to caffe pre-trained model file")
    ap.add_argument("-c", "--confidence", default=0.5, type=float,
                    help="minimum dection confidence to filter weeak detection")
    args = vars(ap.parse_args())

    start = time.time()
    # load input image and preproces it
    image = cv2.imread(args["image"])
    print("[INFO] original image shape: {}".format(image.shape))
    image = imutils.resize(image, width=600)
    print("[INFO] resized image shape: {}".format(image.shape))

    # apply face detection
    (boxes, confidences) = face_detection(image, args["prototxt"], args["model"], args["confidence"])

    for ((startX, startY, endX, endY), confidence) in zip(boxes, confidences):
        # draw rectangle around the detected face
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        text = "{:.2f}".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.putText(image, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    end = time.time()
    print("[INFO] face detection tooks: {} ms".format((end - start)*1000))

    # display the output image
    cv2.imshow("face detection", image)
    cv2.waitKey(0)
