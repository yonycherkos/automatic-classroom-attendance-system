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
        studentName = self.lineEdit.text()
        studentName = studentName.replace(" ", "_")
        if studentName == "":
            pass
        else:
            prototxt = "model/deploy.prototxt.txt"
            model = "model/res10_300x300_ssd_iter_140000.caffemodel"
            output = "dataset/{}".format(studentName)
            os.system("python build_face_dataset.py --prototxt {} --model {} --output {}".format(prototxt, model, output))

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
