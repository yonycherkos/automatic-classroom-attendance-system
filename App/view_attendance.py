from PyQt5 import QtWidgets
from PyQt5 import uic
import pandas as pd
import sys
sys.path.append(".")

class ViewAttendance(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/viewAttendance.ui", self)
        self.backBtn.clicked.connect(self.back)
        df = pd.read_csv("output/attendance.csv", index_col=0)

        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        for (i, row) in enumerate(df.values):
            for (j, data) in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(data)))

    def back(self):
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ViewAttendance()
    window.show()
    app.exec_()
