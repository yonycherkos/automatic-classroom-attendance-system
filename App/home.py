from PyQt5 import QtCore, QtGui, QtWidgets
from register_student import RegisterStudent
from PyQt5 import uic
import sys
import os


class HomePage(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/home.ui", self)
        self.registerStudentBtn.clicked.connect(self.registerStudent)
        self.takeAttendanceBtn.clicked.connect(self.takeAttendance)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)

    def registerStudent(self):
        self.registerStudent = RegisterStudent()
        self.registerStudent.show()
        self.close()

    def takeAttendance(self):
        print("Take Attendance")

    def viewAttendance(self):
        from view_attendance import ViewAttendance
        self.ViewAttendance = ViewAttendance()
        self.ViewAttendance.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HomePage()
    window.show()
    app.exec_()
