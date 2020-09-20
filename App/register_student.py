import sys
sys.path.append(".")

from videoPlayer import VideoPlayer, FaceDetectionWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from imutils import paths
from PyQt5 import uic
import shutil
import cv2
import os


class RegisterStudent(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/registerStudent.ui", self)
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
            self.showDialog(icon=QtWidgets.QMessageBox.Warning,
                            displayText="Enter student fullname", windowTitle="Student Name")
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

    def capture(self):
        self.faceDetectionWidget.capture = True

    def quit(self):
        self.videoPlayer.camera.release()
        cv2.destroyAllWindows()

        capturedFaces = len(list(paths.list_images(self.output)))
        displayText = "{} faces captured".format(capturedFaces)
        self.showDialog(icon=QtWidgets.QMessageBox.Information,
                        displayText=displayText, windowTitle="Capture Images")
        print(displayText)
        self.videoFrame.close()
 

    def uploadImages(self):
        if self.lineEdit.text() == "":
            self.showDialog(icon=QtWidgets.QMessageBox.Warning,
                            displayText="Enter student fullname", windowTitle="Student Name")
        else:
            self.constructOutput()
            dlg = QtWidgets.QFileDialog(self)
            dlg.setFileMode(QtWidgets.QFileDialog.Directory)
            facesDir = dlg.getExistingDirectory()
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            for imagePath in list(paths.list_images(facesDir)):
                shutil.copy(imagePath, self.output)

            uploadedFaces = len(list(paths.list_images(self.output)))
            displayText = "{} faces uploaded".format(uploadedFaces)
            self.showDialog(icon=QtWidgets.QMessageBox.Information,
                            displayText=displayText, windowTitle="Upload Images")

    def register(self):
        self.registerLabel.setText("Registering...")
        os.system("python encode_faces.py --dataset {} --encodings {} --csv {} --prototxt {} --model {}".format(
            self.output, self.encodings, self.csv, self.prototxt, self.model))
        displayText = "{} successful registered".format(self.lineEdit.text())
        self.showDialog(icon=QtWidgets.QMessageBox.Information,
                        displayText=displayText, windowTitle="Register Student")
        self.registerLabel.setText(displayText)

    def back(self):
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

    def viewAttendance(self):
        pass

    def constructOutput(self):
        studentName = self.lineEdit.text()
        studentName = studentName.replace(" ", "_")
        self.output = "dataset/{}".format(studentName)

    def showDialog(self, icon, displayText, windowTitle):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setText(displayText)
        msg.setWindowTitle(windowTitle)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterStudent()
    window.show()
    app.exec_()
