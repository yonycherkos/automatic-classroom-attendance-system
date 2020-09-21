import sys
sys.path.append(".")

from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from face_recognizer_widget import FaceRecognizerWidget
from video_recorder import VideoRecorder
from PyQt5 import uic
import numpy as np
import cv2
import os


class TakeAttendance(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/takeAttendance.ui", self)
        self.videoFrame.setVisible(False)

        self.takeAttendanceBtn.clicked.connect(self.takeAttendance)
        self.quitBtn.clicked.connect(self.quit)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)
        self.backBtn.clicked.connect(self.back)

    def takeAttendance(self):
        self.videoFrame.setVisible(True)
        self.videoLabel.setText("")
        self.faceRecognizerWidget = FaceRecognizerWidget()
        self.videoRecorder = VideoRecorder()
        self.videoRecorder.startRecording()
        frameLayout = self.videoFrame.layout()
        frameLayout.replaceWidget(self.videoLabel, self.faceRecognizerWidget)

        # connect the image data signal and slot together
        imageDataSlot = self.faceRecognizerWidget.imageDataSlot
        self.videoRecorder.imageData.connect(imageDataSlot)
        self.videoLabel = self.faceRecognizerWidget

    def quit(self):
        self.videoRecorder.camera.release()
        cv2.destroyAllWindows()
        self.faceRecognizerWidget.saveDataframe()
        df = self.faceRecognizerWidget.df
        absentNames = list(df[df.iloc[:, -1] == 0]["names"])
        absentNames = " ".join(absentNames).replace(" ", ", ")
        totalCount = len(df.iloc[:, -1])
        presentCount = df.iloc[:, -1].sum()
        displayText = "{} students present out of {} students. \n absent students: {}\n".format(
            presentCount, totalCount, absentNames)
        displayLabel = QLabel(displayText)
        frameLayout = self.videoFrame.layout()
        frameLayout.replaceWidget(self.videoLabel, displayLabel)
        self.quitBtn.close()

    def back(self):
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

    def viewAttendance(self):
        from view_attendance import ViewAttendance
        self.ViewAttendance = ViewAttendance()
        self.ViewAttendance.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TakeAttendance()
    window.show()
    app.exec_()
