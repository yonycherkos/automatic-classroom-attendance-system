import sys
sys.path.append(".")
sys.path.append("./App/pages")

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from login import LoginPage
from home import HomePage
from PyQt5 import uic
import sqlite3
import os


class SignupPage(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/signup.ui", self)
        self.signupBtn.clicked.connect(self.signup)
        self.backBtn.clicked.connect(self.back)

    def signup(self):
        fullname = self.fullnameLineEdit.text()
        username = self.usernameLineEdit.text()
        email = self.emailLineEdit.text()
        password = self.passwordLineEdit.text()

        if (len(fullname) == 0 or len(username) == 0 or len(email) == 0 or len(password) == 0):
            displayText = "Required fields cannot be empty."
            self.showDialog(icon=QMessageBox.Warning,
                            displayText=displayText, windowTitle="Signup")
        else:
            try:
                connection = sqlite3.connect("output/login.db")
                try:
                    connection.execute(
                        "CREATE TABLE USERS (FULLNAME TEXT, USERNAME TEXT NOT NULL, EMAIL TEXT, PASSWORD TEXT NOT NULL)")
                except:
                    pass

                connection.execute(
                    "INSERT INTO USERS VALUES (?, ?, ?, ?)", (fullname, username, email, password))
                connection.commit()
                connection.close()
                
                self.homePage = HomePage()
                self.homePage.show()
                self.close()
            except:
                displayText = "Error connecting to database"
                self.showDialog(icon=QMessageBox.Warning,
                                displayText=displayText, windowTitle="Signup")

    def back(self):
        self.loginPage = LoginPage()
        self.loginPage.show()
        self.close()

    def showDialog(self, icon, displayText, windowTitle):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(displayText)
        msg.setWindowTitle(windowTitle)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignupPage()
    window.show()
    app.exec_()

# TODO: make password invisible
# TODO: avoid duplicate registration
