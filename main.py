from PyQt5.QtWidgets import QApplication
from App.pages.login import LoginPage
import qdarkstyle
import sys

app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
window = LoginPage()
window.show()
app.exec_()