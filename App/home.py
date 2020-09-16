from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import sys
import os


class HomePage(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/home.ui", self)
        self.enrollStudentBtn.clicked.connect(self.enrollStudent)
        self.takeAttendanceBtn.clicked.connect(self.takeAttendance)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)

    def enrollStudent(self):
        from enroll_student import EnrollStudent
        self.enrollStudent = EnrollStudent()
        self.enrollStudent.show()
        self.close()

    def takeAttendance(self):
        print("Take Attendance")

    def viewAttendance(self):
        print("View Attendance")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HomePage()
    window.show()
    app.exec_()
