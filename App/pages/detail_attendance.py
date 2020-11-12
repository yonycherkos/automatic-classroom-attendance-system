import sys
sys.path.append(".")
sys.path.append("./App/utils")

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QHeaderView, QMessageBox
from PyQt5.QtCore import QModelIndex
from PyQt5 import QtGui
from PyQt5 import uic
import pandas as pd
import numpy as np
import config


class DetailAttendance(QMainWindow):

    def __init__(self, df, currentRow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("App/ui/detailAttendance.ui", self)
        self.backBtn.clicked.connect(self.back)

        s = df.iloc[currentRow]

        name = s['names']
        self.studentName.setText(name)
        percentage = s['attend_percent']
        self.attendancePercentage.setText("{}".format(percentage))

        df = pd.DataFrame(columns=['Date', 'Status'])
        df['Date'] = s[1:-1].keys()
        df['Status'] = s[1:-1].values
        self.df = df

        self.displayTable()

    def displayTable(self):
        self.table.setRowCount(self.df.shape[0])
        self.table.setColumnCount(self.df.shape[1])
        self.table.setHorizontalHeaderLabels(self.df.columns)
        self.table.horizontalHeader().setStretchLastSection(True)

        colorMap = {"present": QtGui.QColor(0, 255, 0, 150), "absent": QtGui.QColor(255, 0, 0, 150)}

        df = self.df.replace({0: "absent", 1: "present"})
        for (i, row) in enumerate(df[1:].values):
            color = colorMap[row[1]]

            for (j, data) in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(data)))
                self.table.item(i, j).setBackground(color)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def back(self):
        from view_attendance import ViewAttendance
        self.viewAttendancePage = ViewAttendance()
        self.viewAttendancePage.show()
        self.close()