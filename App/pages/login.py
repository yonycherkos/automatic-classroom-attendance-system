import sys
sys.path.append(".")
sys.path.append("./App/pages")

import os
import sqlite3
from PyQt5 import uic
from home import HomePage
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLineEdit


class LoginPage(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/login.ui", self)
        self.loginBtn.clicked.connect(self.login)
        self.signupBtn.clicked.connect(self.signup)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        if (len(username) == 0 or len(password) == 0):
            displayText = "Required fields cannot be empty."
            self.showDialog(icon=QMessageBox.Warning,
                            displayText=displayText, windowTitle="Signup")
        else:
            try:
                connection = sqlite3.connect("output/login.db")
                results = connection.execute(
                    "SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
                if len(results.fetchall()) > 0:
                    self.homePage = HomePage()
                    self.homePage.show()
                    self.close()
                else:
                    displayText = "Invalid username and password"
                    self.showDialog(icon=QMessageBox.Warning,
                                    displayText=displayText, windowTitle="Signup")
                connection.close()
            except:
                displayText = "Error connecting to database"
                self.showDialog(icon=QMessageBox.Warning,
                                displayText=displayText, windowTitle="Signup")

    def signup(self):
        from signup import SignupPage
        self.signupPage = SignupPage()
        self.signupPage.show()
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
    window = LoginPage()
    window.show()
    app.exec_()

# TODO: login on this device
