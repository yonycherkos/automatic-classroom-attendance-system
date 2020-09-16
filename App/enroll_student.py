from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import sys
import os


class EnrollStudent(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/enrollStudent.ui", self)
        self.takeImagesBtn.clicked.connect(self.takeImages)
        self.uploadImagesBtn.clicked.connect(self.uploadImages)
        self.registerBtn.clicked.connect(self.register)
        self.backBtn.clicked.connect(self.back)

    def takeImages(self):
        pass

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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = EnrollStudent()
    window.show()
    app.exec_()    
