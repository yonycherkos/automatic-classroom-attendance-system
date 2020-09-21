import sys
sys.path.append(".")

import os
import cv2
import numpy as np
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from videoPlayer import VideoPlayer, FaceRecognizerWidget


class TakeAttendance(QtWidgets.QMainWindow):

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
        self.videoPlayer = VideoPlayer()
        self.videoPlayer.startRecording()
        frameLayout = self.videoFrame.layout()
        frameLayout.replaceWidget(self.videoLabel, self.faceRecognizerWidget)

        # connect the image data signal and slot together
        imageDataSlot = self.faceRecognizerWidget.imageDataSlot
        self.videoPlayer.imageData.connect(imageDataSlot)
        self.videoLabel = self.faceRecognizerWidget

    def quit(self):
        self.videoPlayer.camera.release()
        cv2.destroyAllWindows()
        self.faceRecognizerWidget.saveDataframe()
        df = self.faceRecognizerWidget.df
        absentNames = list(df[df.iloc[:, -1] == 0]["names"])
        absentNames = " ".join(absentNames).replace(" ", ", ")
        totalCount = len(df.iloc[:, -1])
        presentCount = df.iloc[:, -1].sum()
        displayText = "{} students present out of {} students. \n absent students: {}\n".format(
            presentCount, totalCount, absentNames)
        displayLabel = QtWidgets.QLabel(displayText)
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
    app = QtWidgets.QApplication(sys.argv)
    window = TakeAttendance()
    window.show()
    app.exec_()
