import sys
sys.path.append(".")
sys.path.append("./App/pages")

from PyQt5.QtWidgets import QMainWindow, QApplication
from register_student import RegisterStudent
from take_attendance import TakeAttendance
from view_attendance import ViewAttendance
from PyQt5 import uic
import os


class HomePage(QMainWindow):

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
        self.takeAttendance = TakeAttendance()
        self.takeAttendance.show()
        self.close()

    def viewAttendance(self):
        self.viewAttendance = ViewAttendance()
        self.viewAttendance.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    app.exec_()
