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
        self.filterComboBox.activated[str].connect(self.filter)
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

    def filter(self, selected):
        self.df = pd.read_csv("output/attendance.csv", index_col=0)
        if selected == "Good":
            attend_frac = self.df.sum(axis=1)/self.df.shape[1]
            self.df = self.df[attend_frac >= 0.9]
        elif selected == "Warning":
            attend_frac = self.df.sum(axis=1)/self.df.shape[1]
            self.df =  self.df[(attend_frac >= 0.8) & (attend_frac < 0.9)]
        elif selected == "Danger":
            attend_frac = self.df.sum(axis=1)/self.df.shape[1]
            self.df = self.df[attend_frac < 0.8]
        else:
            self.df = pd.read_csv("output/attendance.csv", index_col=0)
        self.detailLabel.close()
        self.displayTable()

    def displayTable(self):
        self.table.setRowCount(self.df.shape[0])
        self.table.setColumnCount(self.df.shape[1])
        self.table.setHorizontalHeaderLabels(self.df.columns)
        self.table.horizontalHeader().setStretchLastSection(True)

        counts = list(self.df.sum(axis=1)/self.df.shape[1])
        colorMap = {"Good": QtGui.QColor(0, 255, 0, 150), "Warning": QtGui.QColor(
            255, 255, 0, 150), "Danger": QtGui.QColor(255, 0, 0, 150)}

        df = self.df.replace({0: "absent", 1: "present"})
        for (i, row) in enumerate(df.values):
            if counts[i] >= 0.9:
                color = colorMap["Good"]
            elif counts[i] >= 0.8:
                color = colorMap["Warning"]
            else:
                color = colorMap["Danger"]

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
            displayText = "name: {}\nabsent: {}/{} classes\nattendance: {}%".format(
                name, (num_classes - attend_count), num_classes, attend_frac*100)
            self.detailLabel.setText(displayText)
            self.detailLabel.show()

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
