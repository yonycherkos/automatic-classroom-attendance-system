from PyQt5.QtWidgets import QApplication
from App.pages.home import HomePage
import sys

app = QApplication(sys.argv)
window = HomePage()
window.show()
app.exec_()