import sys
sys.path.append(".")

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QHeaderView
from PyQt5 import QtGui
from PyQt5 import uic
import pandas as pd

class ViewAttendance(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/viewAttendance.ui", self)
        self.backBtn.clicked.connect(self.back)
        df = pd.read_csv("output/attendance.csv", index_col=0)

        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.horizontalHeader().setStretchLastSection(True);
        counts = df.sum(axis=1)/df.shape[1]
        for (i, row) in enumerate(df.values):
            if counts[i] >= 0.8:
                color = QtGui.QColor(0, 255, 0, 150)
            else:
                color = QtGui.QColor(255, 0, 0, 150)
            for (j, data) in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(data)))
                self.table.item(i, j).setBackground(color)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def back(self):
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ViewAttendance()
    window.show()
    app.exec_()

# TODO: add search bar to search and display student info's
