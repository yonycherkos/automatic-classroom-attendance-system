import sys
sys.path.append(".")
sys.path.append("./App/widgets")
sys.path.append("./App/utils")

import os
import cv2
import shutil
import config
from PyQt5 import uic
from imutils import paths
from video_recorder import VideoRecorder
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from face_detection_widget import FaceDetectionWidget
from face_recognizer.face_encoder import FaceEncoder


class RegisterStudent(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/registerStudent.ui", self)
        self.videoFrame.setVisible(False)

        self.takeImagesBtn.clicked.connect(self.takeImages)
        self.captureBtn.clicked.connect(self.capture)
        self.quitBtn.clicked.connect(self.quit)
        self.uploadImagesBtn.clicked.connect(self.uploadImages)
        self.registerBtn.clicked.connect(self.register)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)
        self.backBtn.clicked.connect(self.back)

        self.capturedFaces = 0
        self.output = ""

        self.dataset = config.DATASET
        self.encodings = config.ENCODINGS_PATH
        self.attendance = config.ATTENDANCE_PATH
        self.prototxt = config.PROTOTXT_PATH
        self.model = config.MODEL_PATH

        self.capturedFacesCount = 0
        self.cameraOn = False

    def takeImages(self):
        if self.lineEdit.text() == "":
            self.showDialog(icon=QMessageBox.Warning,
                            displayText="Enter student fullname", windowTitle="Student Name")
        else:
            self.constructOutput()
            self.cameraOn = True
            self.videoFrame.setVisible(True)
            self.faceDetectionWidget = FaceDetectionWidget()
            self.videoRecorder = VideoRecorder()
            self.videoRecorder.startRecording()
            frameLayout = self.videoFrame.layout()
            frameLayout.replaceWidget(
                self.videoLabel, self.faceDetectionWidget)

            # connect the image data signal and slot together
            imageDataSlot = self.faceDetectionWidget.imageDataSlot
            self.videoRecorder.imageData.connect(imageDataSlot)
            self.videoLabel = self.faceDetectionWidget
            self.faceDetectionWidget.output = self.output

    def capture(self):
        self.faceDetectionWidget.capture = True
        self.capturedFacesCount += 1
        self.registerLabel.setText("Captured {} faces".format(self.capturedFacesCount))

    def quit(self):
        self.videoRecorder.camera.release()
        cv2.destroyAllWindows()
        self.cameraOn = False

        displayText = "{} faces captured".format(self.capturedFacesCount)
        self.showDialog(icon=QMessageBox.Information,
                        displayText=displayText, windowTitle="Capture Images")
        print(displayText)
        self.videoFrame.close()

    def uploadImages(self):
        if self.lineEdit.text() == "":
            self.showDialog(icon=QMessageBox.Warning,
                            displayText="Enter student fullname", windowTitle="Student Name")
        else:
            self.constructOutput()
            dlg = QFileDialog(self)
            dlg.setFileMode(QFileDialog.Directory)
            facesDir = dlg.getExistingDirectory()
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            for imagePath in list(paths.list_images(facesDir)):
                shutil.copy(imagePath, self.output)

            uploadedFaces = len(list(paths.list_images(self.output)))
            displayText = "{} faces uploaded".format(uploadedFaces)
            self.showDialog(icon=QMessageBox.Information,
                            displayText=displayText, windowTitle="Upload Images")

    def register(self):
        if self.lineEdit.text() == "":
            self.showDialog(icon=QMessageBox.Warning,
                            displayText="Enter student fullname", windowTitle="Student Name")
        elif not os.path.exists(self.output):
            self.showDialog(icon=QMessageBox.Warning,
                            displayText="take or upload face images for {}".format(self.lineEdit.text()), windowTitle="face images doesn't exists")
        else:
            self.videoRecorder.camera.release()
            cv2.destroyAllWindows()
            self.cameraOn = False
            self.registerLabel.setText("Registering...")

            # encode faces
            self.face_encoder = FaceEncoder(self.output, self.encodings, self.attendance, self.prototxt, self.model)
            self.face_encoder.encode_faces()
            self.face_encoder.save_face_encodings()

            displayText = "{} successful registered".format(
                self.lineEdit.text())
            self.showDialog(icon=QMessageBox.Information,
                            displayText=displayText, windowTitle="Register Student")
            self.registerLabel.setText(displayText)

    def back(self):
        if self.cameraOn:
            self.videoRecorder.camera.release()
            cv2.destroyAllWindows()
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

    def viewAttendance(self):
        if self.cameraOn:
            self.videoRecorder.camera.release()
            cv2.destroyAllWindows()
        from view_attendance import ViewAttendance
        self.ViewAttendance = ViewAttendance()
        self.ViewAttendance.show()
        self.close()

    def constructOutput(self):
        studentName = self.lineEdit.text()
        studentName = studentName.replace(" ", "_")
        self.output = "dataset/{}".format(studentName)

    def showDialog(self, icon, displayText, windowTitle):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(displayText)
        msg.setWindowTitle(windowTitle)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegisterStudent()
    window.show()
    app.exec_()
