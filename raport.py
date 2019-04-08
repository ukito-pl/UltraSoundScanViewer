# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL


import RaportWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from ReportLoadDialog import ReportLoadDialog

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
        self.reportLoadDialog = ReportLoadDialog()
        self.connect(self.pushButton_open_report, SIGNAL('clicked()'), self.getFile)
        self.connect(self.pushButton_new_report, SIGNAL('clicked()'), self.newFile)
        self.connect(self.reportLoadDialog.pushButton_open, SIGNAL('clicked()'), self.getFile)
        self.connect(self.reportLoadDialog.pushButton_new, SIGNAL('clicked()'), self.newFile)
        self.connect(self.pushButton_add_change, SIGNAL('clicked()'), self.addCurrentElementToReport)
        self.connect(self.pushButton_delete, SIGNAL('clicked()'), self.deleteCurrentElementFromReport)
        self.treeWidget.currentItemChanged.connect(self.treeItemSelected)
        self.comboBox_type.currentIndexChanged.connect(self.setElementType)

        self.elementNames = []
        self.elementTypeIdBases = []
        self.setElementTypes()
        self.setElementType(self.comboBox_type.currentIndex())
        self.reportDir = -1
        self.pushButton_delete.setEnabled(False)

    def treeItemSelected(self,item, item_prev):
        if item:
            if item.parent():
                element_data = self.getElementData(item.text(1))
                print element_data
                element_type_id = item.parent().data(1,QtCore.Qt.UserRole).toInt()
                if element_type_id:
                    element_type_id = element_type_id[0]
                    self.setElementType(element_type_id)
                self.setTableItems(element_data)
                self.pushButton_delete.setEnabled(True)
                self.pushButton_add_change.setText(_translate("Dialog", "Zmień".__str__(), None))
            else:
                self.pushButton_delete.setEnabled(False)

    def setTreeWidget(self):
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
                item.setData(1, QtCore.Qt.UserRole, _translate("Dialog", line[3].__str__(), None))
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
        report.close()

    def getFile(self):
        dir = QtGui.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)
            self.setTreeWidget()
            if not self.isEnabled():
                id, nb = self.generateId(self.comboBox_type.currentIndex())
                name = self.elementNames[self.comboBox_type.currentIndex()] + "#" + nb.__str__()
                self.setTableItems([id,name])
            self.reportLoadDialog.close()
            self.setEnabled(True)


    def newFile(self):
        dir = QtGui.QFileDialog.getSaveFileName(directory="*.csv", filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)
            report = open(dir, 'w')
            for i in range(0,self.comboBox_type.count()):
                header1 = "\nRodzaj:," + self.comboBox_type.itemText(i).__str__().encode('utf-8')+ ",RodzajID:," + i.__str__() + "\n"
                header2 = ",".join([('"' + x + '"') for x in self.getTableItemsNamesList(i)]) + "\n"
                report.writelines(header1)
                report.writelines(header2)
            report.close()
            self.setTreeWidget()
            if not self.isEnabled():
                id, nb = self.generateId(self.comboBox_type.currentIndex())
                name = self.elementNames[self.comboBox_type.currentIndex()] + "#" + nb.__str__()
                self.setTableItems([id,name])
            self.reportLoadDialog.close()
            self.setEnabled(True)


    def setCurrentElement(self,element_type_id, property_list):
        #property_list = [('"' + x + '"') for x in property_list]
        id = ''
        name = ''
        if self.reportDir != -1:
            id, nb = self.generateId(element_type_id)
            name = self.elementNames[element_type_id] + "#" + nb.__str__()
            self.setTreeWidget()
        else:
            self.setEnabled(False)
            self.reportLoadDialog.show()
            self.reportLoadDialog.activateWindow()

        self.setElementType(element_type_id)
        property_list.insert(0, name)
        property_list.insert(0, id)
        self.setTableItems(property_list)

    def addCurrentElementToReport(self):
        lineData = ""
        for i in range(0,self.tableWidget.rowCount()):
            lineData = lineData + '"'+self.tableWidget.item(i,0).text() + '"' + ","
        lineData = lineData + "\n"
        type_id = self.comboBox_type.currentIndex()
        element_id = self.tableWidget.item(0,0).text()
        report = open(self.reportDir,"r")
        found = False
        new = False
        j = -1
        i = 0
        report_content = report.readlines()
        for line in report_content:
            line = line.replace("\n","").split(',')
            if len(line) >= 3 and line[2] == "RodzajID:" and line[3]==type_id.__str__():

                found = True
            if found and line[0] == '':
                j = i
                found = False
                new = True
            elif found and  line[0] == element_id.__str__():
                j = i
                found = False
            i = i+1
        report.close()
        if j != -1:
            if new:
                report_content.insert(j,lineData)
            else:
                report_content[j] = lineData
        report = open(self.reportDir, "w")
        report.writelines(report_content)
        report.close()
        for i in range(0,self.treeWidget.topLevelItemCount()):
            top_level_item = self.treeWidget.topLevelItem(i)
            element_type_id = top_level_item.data(1, QtCore.Qt.UserRole).toString()
            if type_id.__str__() == element_type_id:
                name = lineData.split(",")[1]
                id = lineData.split(",")[0]
                child_item = QtGui.QTreeWidgetItem()
                child_item.setText(0, _translate("Dialog", name, None))
                child_item.setText(1, _translate("Dialog", id, None))
                top_level_item.addChild(child_item)
                self.treeWidget.setCurrentItem(child_item,0)
        #self.setTreeWidget()

    def getElementData(self,id):
        report = open(self.reportDir,'r')
        for line in report:
            line = line.replace("\n", "").split('","')
            print line[0], id.__str__()
            if len(line) > 1 and line[0] == id.__str__():
                return line
        report.close()

    def deleteCurrentElementFromReport(self):
        current_item = self.treeWidget.currentItem()
        parent = current_item.parent()
        id = current_item.text(1)
        self.deleteElementFromReport(id)
        parent.takeChild(parent.indexOfChild(current_item))
        self.pushButton_delete.setEnabled(False)
        self.tableWidget.clearContents()

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
        report = open(self.reportDir, "w")
        report.writelines(report_content)
        report.close()

    def setElementTypes(self):
        file = open("tableNamesList.txt", 'r')
        nb_of_elements_type = len(file.readlines())
        for i in range(0,nb_of_elements_type):
            self.elementNames.append("")
            self.elementTypeIdBases.append("")
        file.seek(0,0)
        for line in file:
            line = line.replace("\n", "")
            if line != '':
                line = line.split(": ")
                type = line[0].split(", ")
                self.elementNames[int(type[1])] = type[0]
                self.comboBox_type.addItem("")
                self.comboBox_type.setItemText(int(type[1]), _translate("Dialog", type[0], None))
                self.elementTypeIdBases[int(type[1])] = type[2]
        file.close()

    def setElementType(self,id):
        list = self.getTableItemsNamesList(id)
        self.setTableHeaderItems(list)
        self.comboBox_type.setCurrentIndex(id)

    def getTableItemsNamesList(self,id):
        file = open("tableNamesList.txt",'r')
        for line in file:
            line = line.replace("\n", "")
            if line != '':
                line = line.split(": ")
                type = line[0].split(", ")
                headers = line[1].split(", ")
                if type[1] == id.__str__():
                    file.close()
                    return headers
        file.close()
        return []

    def setTableItems(self,item_list):
        i = 0
        for item_val in item_list:
            try:
                item = QtGui.QTableWidgetItem()
                self.tableWidget.setItem(i,0,item)
                self.tableWidget.item(i, 0).setText(item_val)
            except:
                pass
            i = i + 1

    def setTableHeaderItems(self, item_names_list):
        i = 0
        self.tableWidget.setRowCount(len(item_names_list))
        for name in item_names_list:
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("Dialog", name, None))
            self.tableWidget.setVerticalHeaderItem(i, item)
            i = i + 1

    def generateId(self,element_type_id):
        id_base = self.elementTypeIdBases[element_type_id]
        nb_of_elem = 0
        report = open(self.reportDir,'r')
        found_type = False
        line = report.readline()
        while line:
            line = line.replace("\n", "").split(',')
            if len(line) >= 3 and line[2] == "RodzajID:" and line[3]==element_type_id.__str__():
                found_type = True
                line = report.readline()
            elif found_type and line[0] == '':
                generated_id = id_base + (nb_of_elem+1).__str__(), (nb_of_elem+1)
                return generated_id
            elif found_type:
                nb_of_elem = nb_of_elem + 1
            line = report.readline()
        return id_base + (nb_of_elem+1).__str__(),(nb_of_elem+1)