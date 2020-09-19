import os
import cv2
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from videoPlayer import VideoPlayer, FaceDetectionWidget
import sys
sys.path.append(".")


class EnrollStudent(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/enrollStudent.ui", self)
        self.videoFrame.setVisible(False)

        self.takeImagesBtn.clicked.connect(self.takeImages)
        self.captureBtn.clicked.connect(self.capture)
        self.quitBtn.clicked.connect(self.quit)
        self.uploadImagesBtn.clicked.connect(self.uploadImages)
        self.registerBtn.clicked.connect(self.register)
        self.backBtn.clicked.connect(self.back)

        self.capturedFaces = 0
        self.output = ""

    def takeImages(self):
        studentName = self.lineEdit.text()
        studentName = studentName.replace(" ", "_")
        self.videoFrame.setVisible(True)
        if studentName == "":
            self.videoLabel.setText("Enter student full name!")
        else:
            self.videoLabel.setText("")
            self.faceDetectionWidget = FaceDetectionWidget()
            self.videoPlayer = VideoPlayer()
            self.videoPlayer.startRecording()
            frameLayout = self.videoFrame.layout()
            frameLayout.replaceWidget(
                self.videoLabel, self.faceDetectionWidget)

            # connect the image data signal and slot together
            imageDataSlot = self.faceDetectionWidget.imageDataSlot
            self.videoPlayer.imageData.connect(imageDataSlot)
            self.videoLabel = self.faceDetectionWidget

            output = "dataset/{}".format(studentName)
            self.faceDetectionWidget.output = output

    def uploadImages(self):
        pass

    def register(self):
        self.registerLabel.setText("Registering...")
        dataset = self.faceDetectionWidget.output
        encodings = "output/encodings2.pickle"
        csv = "output/attendance.csv"
        prototxt = "model/deploy.prototxt.txt"
        model = "model/res10_300x300_ssd_iter_140000.caffemodel"
        os.system("python encode_faces.py --dataset {} --encodings {} --csv {} --prototxt {} --model {}".format(
            dataset, encodings, csv, prototxt, model))
        self.registerLabel.setText(
            "{} student successful registered".format(self.faceDetectionWidget.total))

    def back(self):
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

    def viewAttendance(self):
        pass

    def capture(self):
        self.faceDetectionWidget.capture = True

    def quit(self):
        try:
            print("[INFO] {} face captured".format(
                self.faceDetectionWidget.total))
        except:
            pass

        self.videoPlayer.camera.release()
        cv2.destroyAllWindows()
        self.videoFrame.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = EnrollStudent()
    window.show()
    app.exec_()
