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
        self.updateChangesBtn.clicked.connect(self.updateChanges)
        self.backBtn.clicked.connect(self.back)

        self.attendance = config.ATTENDANCE_PATH
        self.df = df
        self.currentRow = currentRow

        s = self.df.iloc[self.currentRow]
        self.name = s['names']
        self.studentName.setText(self.name)
        percentage = s['attend_percent']
        self.attendancePercentage.setText("{}".format(percentage))

        currentDf = pd.DataFrame(columns=['Date', 'Status'])
        currentDf['Date'] = s[1:-1].keys()
        currentDf['Status'] = s[1:-1].values
        self.currentDf = currentDf

        self.displayTable()

    def displayTable(self):
        self.table.setRowCount(self.currentDf.shape[0])
        self.table.setColumnCount(self.currentDf.shape[1])
        self.table.setHorizontalHeaderLabels(self.currentDf.columns)
        self.table.horizontalHeader().setStretchLastSection(True)

        colorMap = {"present": QtGui.QColor(0, 255, 0, 150), "absent": QtGui.QColor(255, 0, 0, 150), "excused": QtGui.QColor(0, 255, 0, 150)}

        currentDf = self.currentDf.replace({0: "absent", 1: "present", None: "excused"})
        for (i, row) in enumerate(currentDf.values):
            color = colorMap[row[1]]
            for (j, data) in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(data)))
                self.table.item(i, j).setBackground(color)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def updateChanges(self):
        updatedDf = pd.DataFrame()  

        rows = self.table.rowCount()
        columns = self.table.columnCount()        
        for row in range(rows):         
            for column in range(columns):  
                item = self.table.item(row, column)  
                if item is not None:  
                    updatedDf.loc[row, column] = str(item.text())  
        updatedDf = updatedDf.replace({"absent": 0, "present": 1, "excused": None}) 
        self.df = self.df.drop("attend_percent", axis=1)
        updateDf = np.array(updatedDf[1]).reshape(1, self.df.shape[1] - 1)
        self.df.loc[self.df["names"] == self.name, self.df.columns[1]:] = list(updateDf)
        self.updateChangesConfirmation()

    def back(self):
        from view_attendance import ViewAttendance
        self.viewAttendancePage = ViewAttendance()
        self.viewAttendancePage.show()
        self.close()

    def updateChangesConfirmation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("The document has been modified.")
        msg.setInformativeText("Do you want to save your changes?")
        msg.setWindowTitle("update changes")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)
        ret = msg.exec_()

        if (ret == QMessageBox.Save):
            self.df.to_csv(self.attendance)
            s = self.df.iloc[self.currentRow][1:]
            percentage = round(s.sum()/s.count()*100, 2)
            self.attendancePercentage.setText("{}".format(percentage))
        else:
            pass