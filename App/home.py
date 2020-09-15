import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic


class HomePage(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/home.ui", self)
        self.enrollStudentBtn.clicked.connect(self.enrollStudent)
        self.takeAttendanceBtn.clicked.connect(self.takeAttendance)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)
    
    def enrollStudent(self):
        print("Enroll Student")

    def takeAttendance(self):
        print("Take Attendance")
    
    def viewAttendance(self):
        print("View Attendance")
        

app = QtWidgets.QApplication(sys.argv)
window = HomePage()
window.show()
app.exec_()