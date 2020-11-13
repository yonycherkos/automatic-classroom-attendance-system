from PyQt5.QtWidgets import QApplication
from App.pages.login import LoginPage
import sys

app = QApplication(sys.argv)
window = LoginPage()
window.show()
app.exec_()