import sys
sys.path.append(".")

import os
import cv2
import shutil
from PyQt5 import uic
from imutils import paths
from PyQt5 import QtCore, QtGui, QtWidgets
from videoPlayer import VideoPlayer, FaceDetectionWidget


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

        self.encodings = "output/encodings2.pickle"
        self.csv = "output/attendance.csv"
        self.prototxt = "model/deploy.prototxt.txt"
        self.model = "model/res10_300x300_ssd_iter_140000.caffemodel"

    def takeImages(self):
        if self.lineEdit.text() == "":
            self.showDialog()
        else:
            self.constructOutput()
            self.videoFrame.setVisible(True)
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

            self.faceDetectionWidget.output = self.output

    def uploadImages(self):
        if self.lineEdit.text() == "":
            self.showDialog()
        else:
            self.constructOutput()
            dlg = QtWidgets.QFileDialog(self)
            dlg.setFileMode(QtWidgets.QFileDialog.Directory)
            facesDir = dlg.getExistingDirectory()
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            for imagePath in list(paths.list_images(facesDir)):
                shutil.copy(imagePath, self.output)

    def register(self):
        self.registerLabel.setText("Registering...")
        os.system("python encode_faces.py --dataset {} --encodings {} --csv {} --prototxt {} --model {}".format(
            self.output, self.encodings, self.csv, self.prototxt, self.model))
        registeredFaces = len(list(paths.list_images(self.output)))
        self.registerLabel.setText(
            "{} student successful registered".format(registeredFaces))

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

    def constructOutput(self):
        studentName = self.lineEdit.text()
        studentName = studentName.replace(" ", "_")
        self.output = "dataset/{}".format(studentName)

    def showDialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Enter student fullname")
        msg.setWindowTitle("student name")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = EnrollStudent()
    window.show()
    app.exec_()
