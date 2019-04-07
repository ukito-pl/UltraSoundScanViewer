# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL


import RaportWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ReportDialog(QtGui.QDialog, RaportWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.connect(self.pushButton_open_report, SIGNAL('clicked()'), self.getFile)
        self.connect(self.pushButton_new_report, SIGNAL('clicked()'), self.newFile)
        self.connect(self.pushButton_add_change, SIGNAL('clicked()'), self.addElementToReport)
        self.connect(self.pushButton_delete, SIGNAL('clicked()'), self.deleteCurrentElementFromReport)
        self.comboBox_type.currentIndexChanged.connect(self.setElementType)
        self.setElementType(self.comboBox_type.currentIndex())
        self.reportDir = -1

    def setTreeView(self):
        self.treeWidget.clear()
        self.treeWidget.header().resizeSection(0,200)
        parent_item = self.treeWidget
        report = open(self.reportDir, 'r')
        line = report.readline()
        while line:
            line = line.replace("\n", "").split(',')
            if len(line) > 3 and line[0] == "Rodzaj:":
                item = QtGui.QTreeWidgetItem(self.treeWidget)
                item.setText(0, _translate("Dialog", line[1].__str__(), None))
                parent_item = item
                line = report.readline()
                line = report.readline()
            elif len(line) > 1:
                child_item = QtGui.QTreeWidgetItem(parent_item)
                child_item.setText(0, _translate("Dialog", line[1].__str__(), None))
                child_item.setText(1, _translate("Dialog", line[0].__str__(), None))
                line = report.readline()
            else:
                line = report.readline()

    def getFile(self):
        dir = QtGui.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)
            self.setTreeView()


    def newFile(self):
        dir = QtGui.QFileDialog.getSaveFileName(directory="*.csv", filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)
            report = open(dir, 'w')
            for i in range(0,self.comboBox_type.count()):
                header1 = "\nRodzaj:," + self.comboBox_type.itemText(i).__str__().encode('utf-8')+ ",RodzajID:," + i.__str__() + "\n"
                header2 = ",".join(self.getTableItemsNamesList(i)) + "\n"
                report.writelines(header1)
                report.writelines(header2)
            report.close()
            self.setTreeView()

    def addElementToReport(self):
        lineData = ""
        for i in range(0,self.tableWidget.rowCount()):
            lineData = lineData + self.tableWidget.item(i,0).text() + ","
        lineData = lineData + "\n"
        id = self.comboBox_type.currentIndex()
        report = open(self.reportDir,"r")
        found = False
        j = -1
        i = 0
        report_content = report.readlines()
        for line in report_content:
            line = line.replace("\n","").split(',')
            if len(line) >= 3 and line[3]==id.__str__():
                found = True
            if found and line[0] == '':
                j = i
                found = False
            i = i+1
        report.close()
        if j != -1:
            report_content.insert(j,lineData)
        report = open(self.reportDir, "w")
        report.writelines(report_content)
        report.close()

    def deleteCurrentElementFromReport(self):
        id = self.tableWidget.item(0,0).text()
        self.deleteElementFromReport(id)

    def deleteElementFromReport(self,elem_id):
        report = open(self.reportDir, "r")
        j = -1
        i = 0
        report_content = report.readlines()
        for line in report_content:
            line = line.replace("\n", "").split(',')
            if line[0] == elem_id.__str__():
                j = i
            i = i + 1
        report.close()
        if j != -1:
            report_content.__delitem__(j)
        print
        report = open(self.reportDir, "w")
        report.writelines(report_content)
        report.close()

    def setElementType(self,id):
        list = self.getTableItemsNamesList(id)
        self.setTableItems(list)

    def getTableItemsNamesList(self,id):
        file = open("tableNamesList.txt",'r')
        i = 0
        for line in file:
            if i == id:
                file.close()
                return line.replace("\n","").split(", ")
            i = i+1
        file.close
        return []

    def setTableItems(self,item_names_list):
        i = 0
        self.tableWidget.setRowCount(len(item_names_list))
        for name in item_names_list:
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("Dialog", name, None))
            self.tableWidget.setVerticalHeaderItem(i, item)
            i = i + 1
