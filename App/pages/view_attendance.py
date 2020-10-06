from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QHeaderView, QMessageBox
from PyQt5.QtCore import QModelIndex
from PyQt5 import QtGui
from PyQt5 import uic
import pandas as pd
import numpy as np
import sys
sys.path.append(".")


class ViewAttendance(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/viewAttendance.ui", self)
        self.searchBtn.clicked.connect(self.search)
        self.backBtn.clicked.connect(self.back)
        self.df = pd.read_csv("output/attendance.csv", index_col=0)
        self.displayTable()

    def search(self):
        self.df = pd.read_csv("output/attendance.csv", index_col=0)
        if self.searchText.text() == "":
            self.showDialog(icon=QMessageBox.Warning,
                            displayText="Enter student fullname", windowTitle="Search Name")
        else:
            name = self.searchText.text().replace(" ", "_")
            self.df = self.df[self.df["names"] == name]
            if len(self.df) == 0:
                self.showDialog(icon=QMessageBox.Warning, displayText="student with the name {} is not registered".format(
                    name), windowTitle="Search Name")
            else:
                self.displayTable()
                self.detail()

    def displayTable(self):
        self.table.setRowCount(self.df.shape[0])
        self.table.setColumnCount(self.df.shape[1])
        self.table.setHorizontalHeaderLabels(self.df.columns)
        self.table.horizontalHeader().setStretchLastSection(True)
        counts = list(self.df.sum(axis=1)/self.df.shape[1])
        for (i, row) in enumerate(self.df.values):
            color = QtGui.QColor(0, 255, 0, 150) if counts[i] >= 0.8 else QtGui.QColor(255, 0, 0, 150)
            for (j, data) in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(data)))
                self.table.item(i, j).setBackground(color)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.clicked.connect(self.detail)

    def detail(self):
        if self.table.rowCount() == 1:
            row = 0
        else:
            row = self.table.currentRow()
        if row > -1:
            name = self.table.item(row, 0).text()
            attend_count = list(self.df.sum(axis=1))[row]
            num_classes = self.df.shape[1]
            attend_frac = np.round(attend_count/num_classes, 2)
            displayText = "name: {}\n absent: {}/{} classes\n attendance: {}%".format(
                name, (num_classes - attend_count), num_classes, attend_frac*100)
            self.detailLabel.setText(displayText)

    def back(self):
        from home import HomePage
        self.homePage = HomePage()
        self.homePage.show()
        self.close()

    def showDialog(self, icon, displayText, windowTitle):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(displayText)
        msg.setWindowTitle(windowTitle)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ViewAttendance()
    window.show()
    app.exec_()

# TODO: add filter dropdown to filter student
