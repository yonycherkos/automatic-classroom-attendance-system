import sys
sys.path.append(".")
sys.path.append("./App/pages")

import os
import sqlite3
from PyQt5 import uic
from home import HomePage
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLineEdit


class SignupPage(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/signup.ui", self)
        self.signupBtn.clicked.connect(self.signup)
        self.backBtn.clicked.connect(self.back)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.confirmPasswordLineEdit.setEchoMode(QLineEdit.Password)

    def signup(self):
        fullname = self.fullnameLineEdit.text()
        username = self.usernameLineEdit.text()
        email = self.emailLineEdit.text()
        password = self.passwordLineEdit.text()
        confirmPassword = self.confirmPasswordLineEdit.text()

        if (len(fullname) == 0 or len(username) == 0 or len(email) == 0 or len(password) == 0):
            displayText = "Required fields cannot be empty."
            self.showDialog(icon=QMessageBox.Warning,
                            displayText=displayText, windowTitle="Signup")
        elif (password != confirmPassword):
            displayText = "Password mismatch"
            self.showDialog(icon=QMessageBox.Warning,
                            displayText=displayText, windowTitle="Signup")
            
        else:
            try:
                connection = sqlite3.connect("output/login.db")
                try:
                    connection.execute(
                        "CREATE TABLE USERS (FULLNAME TEXT, USERNAME TEXT NOT NULL UNIQUE, EMAIL TEXT, PASSWORD TEXT NOT NULL)")
                except:
                    pass

                try:
                    connection.execute("INSERT INTO USERS VALUES (?, ?, ?, ?)", (fullname, username, email, password))
                    connection.commit()
                    connection.close()
                
                    self.homePage = HomePage()
                    self.homePage.show()
                    self.close()
                except:
                    displayText = "Duplicated user, {} already registered".format(username)
                    self.showDialog(icon=QMessageBox.Warning,
                                displayText=displayText, windowTitle="Signup")
            except:
                displayText = "Error connecting to database"
                self.showDialog(icon=QMessageBox.Warning,
                                displayText=displayText, windowTitle="Signup")

    def back(self):
        from login import LoginPage
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
