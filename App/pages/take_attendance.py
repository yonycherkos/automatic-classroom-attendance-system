import sys
sys.path.append(".")
sys.path.append("./App/widgets")
sys.path.append("./App/utils")

from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QFileDialog
from face_recognizer_widget import FaceRecognizerWidget
from video_recorder import VideoRecorder
from PyQt5.QtCore import QTimer
from threading import Timer
from PyQt5 import uic
import numpy as np
import config
import cv2
import os


class TakeAttendance(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/takeAttendance.ui", self)
        self.setCentralWidget(self.takeAttendancePage)
        self.videoFrame.setVisible(False)

        self.captureVideoBtn.clicked.connect(self.captureVideo)
        self.uploadVideoBtn.clicked.connect(self.uploadVideo)
        self.quitBtn.clicked.connect(self.quit)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)
        self.backBtn.clicked.connect(self.back)

        self.timer = QTimer()
        self.timer.setInterval(config.CAPTURE_DURATION)
        self.timer.timeout.connect(self.quit)

        self.cameraOn = False

    def takeAttendance(self, videoPath=None):
        self.timer.start()
        self.videoFrame.setVisible(True)
        self.faceRecognizerWidget = FaceRecognizerWidget()
        if videoPath is None:
            self.videoRecorder = VideoRecorder()
        else:
            self.videoRecorder = VideoRecorder(videoPath)
        self.videoRecorder.startRecording()
        frameLayout = self.videoFrame.layout()
        frameLayout.replaceWidget(self.videoLabel, self.faceRecognizerWidget)

        # connect the image data signal and slot together
        imageDataSlot = self.faceRecognizerWidget.imageDataSlot
        self.videoRecorder.imageData.connect(imageDataSlot)
        self.videoLabel = self.faceRecognizerWidget

        self.cameraOn = True

    def captureVideo(self):
        self.takeAttendance()

    def uploadVideo(self):
        dlg = QFileDialog(self)
        videoPath, _ = dlg.getOpenFileName(self)
        self.takeAttendance(videoPath)

    def quit(self):
        self.closeCamera()
        self.faceRecognizerWidget.saveDataframe()
        self.videoLabel.hide()
        displayText = self.constructDisplayText()
        displayLabel = QLabel(displayText)
        frameLayout = self.videoFrame.layout()
        frameLayout.replaceWidget(self.videoLabel, displayLabel)
        self.videoLabel.show()
        self.quitBtn.close()

    def back(self):
        if self.cameraOn:
            self.closeCamera()
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

    def viewAttendance(self):
        if self.cameraOn:
            self.closeCamera()
        from view_attendance import ViewAttendance
        self.ViewAttendance = ViewAttendance()
        self.ViewAttendance.show()
        self.close()

    def constructDisplayText(self):
        df = self.faceRecognizerWidget.df
        absentNames = list(df[df.iloc[:, -1] == 0]["names"])
        totalCount = len(df.iloc[:, -1])
        presentCount = df.iloc[:, -1].sum()

        absentNames = ["{}, {}".format(i + 1, name)  for (i, name) in enumerate(absentNames)]
        absentNameString = ""
        for i in np.arange(0, len(absentNames), 3):
            newAbsentNameString = "  ".join(absentNames[i:i + 3])
            absentNameString = "{}\t{}\n".format(absentNameString, newAbsentNameString)

        displayText = "{} students present out of {} students. \n\n absent students: \n{}".format(
            presentCount, totalCount, absentNameString)
        return displayText       

    def closeCamera(self):
        self.videoRecorder.camera.release()
        cv2.destroyAllWindows()
        self.cameraOn = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TakeAttendance()
    window.show()
    app.exec_()
