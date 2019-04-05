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
        #self.connect(self.comboBox_type,SIGNAL('currentIndexChanged(PyQt_PyObject)'),self.setElementType)
        self.comboBox_type.currentIndexChanged.connect(self.setElementType)
        self.reportDir = -1

    def getFile(self):
        dir = QtGui.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)

    def newFile(self):
        dir = QtGui.QFileDialog.getSaveFileName(directory="*.csv", filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)

    def setElementType(self,id):
        print id
        list = self.getTableItemsNamesList(id)
        self.setTableItems(list)

    def getTableItemsNamesList(self,id):
        file = open("tableNamesList.txt",'r')
        i = 0
        for line in file:
            if i == id:
                print line
                return line.split(", ")
            i = i+1
        return []

    def setTableItems(self,item_names_list):
        i = 0
        self.tableWidget.setRowCount(len(item_names_list))
        for name in item_names_list:
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("Dialog", name, None))
            i = i + 1
