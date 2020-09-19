from videoPlayer import VideoPlayer, FaceDetectionWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import cv2
import sys
import os

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
            frameLayout.replaceWidget(self.videoLabel, self.faceDetectionWidget)

            # connect the image data signal and slot together
            imageDataSlot = self.faceDetectionWidget.imageDataSlot
            self.videoPlayer.imageData.connect(imageDataSlot)
            self.videoLabel = self.faceDetectionWidget

            output = "dataset/{}".format(studentName)
            self.faceDetectionWidget.output = output
            

    def uploadImages(self):
        pass

    def register(self):
        pass

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
            print("[INFO] {} face captured".format(self.faceDetectionWidget.total))
        except:
            pass
        
        cv2.destroyAllWindows()
        self.videoFrame.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = EnrollStudent()
    window.show()
    app.exec_()    
