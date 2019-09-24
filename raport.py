# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL
import csv
from PIL import Image
import os
import copy
import numpy as np
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
        self.connect(self.pushButton_next, SIGNAL('clicked()'),self.nextImage)
        self.connect(self.pushButton_prev, SIGNAL('clicked()'), self.prevImage)
        self.modesList = ["NormalMode","AddMode","ChangeMode"]
        self.mode = -1
        self.setMode("NormalMode")
        self.elementNames = []
        self.elementTypeIdBases = []
        self.setElementTypes()
        self.setElementType(self.comboBox_type.currentIndex())
        self.reportDir = -1
        self.pushButton_delete.setEnabled(False)
        self.PILImageList = []
        self.currentImageIndex = -1
        self.currentPILImage = Image.Image()

    def closeEvent(self, QCloseEvent):
        self.reportLoadDialog.close()
        super(self.__class__, self).closeEvent(QCloseEvent)

    def setMode(self,mode):
        self.mode = mode
        if mode == "NormalMode":
            self.pushButton_delete.setEnabled(False)
            self.pushButton_add_change.setEnabled(False)
            self.treeWidget.setEnabled(True)
            self.tableWidget.clearContents()
            self.clearImages()
        elif mode == "AddMode":
            self.pushButton_delete.setEnabled(True)
            self.pushButton_delete.setText("Anuluj")
            self.pushButton_add_change.setEnabled(True)
            self.treeWidget.setEnabled(False)
            self.pushButton_add_change.setText("Dodaj")
        elif mode == "ChangeMode":
            self.pushButton_delete.setEnabled(True)
            self.pushButton_delete.setText(_translate("Dialog", "Usuń".__str__(), None))
            self.pushButton_add_change.setEnabled(True)
            self.treeWidget.setEnabled(True)
            self.pushButton_add_change.setText(_translate("Dialog", "Zmień".__str__(), None))

    def treeItemSelected(self,item, item_prev):
        if item:
            if item.parent():
                element_data = self.getElementData(item.text(1))
                element_type_id = item.parent().data(1,QtCore.Qt.UserRole).toInt()
                if element_type_id:
                    element_type_id = element_type_id[0]
                    self.setElementType(element_type_id)
                self.clearImages()
                self.setTableItems(element_data)
                self.setMode("ChangeMode")
            else:
                self.setMode("NormalMode")

    def setTreeWidget(self):
        self.treeWidget.clear()
        self.treeWidget.header().resizeSection(0,200)
        parent_item = self.treeWidget
        report = open(self.reportDir, 'r')
        read_report = csv.reader(report)
        for line in read_report:
            if len(line) > 3 and line[0] == "Rodzaj:":
                item = QtGui.QTreeWidgetItem(self.treeWidget)
                item.setText(0, _translate("Dialog", line[1].__str__(), None))
                item.setData(1, QtCore.Qt.UserRole, _translate("Dialog", line[3].__str__(), None))
                parent_item = item
            elif len(line) > 1 and line[0] != "Id":
                child_item = QtGui.QTreeWidgetItem(parent_item)
                child_item.setText(0, _translate("Dialog", line[1].__str__(), None))
                child_item.setText(1, _translate("Dialog", line[0].__str__(), None))


        report.close()

    def getFile(self):
        dir = QtGui.QFileDialog.getOpenFileName(filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)
            self.setTreeWidget()
            if not self.isEnabled():
                self.reportLoadDialog.close()
                self.setEnabled(True)
            if self.mode == "AddMode":
                id, nb = self.generateId(self.comboBox_type.currentIndex())
                name = self.elementNames[self.comboBox_type.currentIndex()] + "#" + nb.__str__()
                self.setTableItems([id, name], clear=False)
            elif self.mode == "ChangeMode":
                self.setMode("NormalMode")


    def newFile(self):
        dir = QtGui.QFileDialog.getSaveFileName(directory="*.csv", filter="CSV files (*.csv)")
        if dir:
            self.reportDir = dir
            self.label_file_dir.setText(dir)
            report = open(dir, 'w')
            report_writer = csv.writer(report)
            for i in range(0,self.comboBox_type.count()):
                header1 = ["Rodzaj:", self.comboBox_type.itemText(i).__str__().encode('utf-8'), "RodzajID:", i.__str__() ]
                header2 = self.getTableItemsNamesList(i)
                report_writer.writerow(header1)
                report_writer.writerow(header2)
                report_writer.writerow([])
            report.close()
            self.setTreeWidget()
            if not self.isEnabled():
                self.reportLoadDialog.close()
                self.setEnabled(True)
            if self.mode == "AddMode":
                id, nb = self.generateId(self.comboBox_type.currentIndex())
                name = self.elementNames[self.comboBox_type.currentIndex()] + "#" + nb.__str__()
                self.setTableItems([id, name], clear=False)
            elif self.mode == "ChangeMode":
                self.setMode("NormalMode")



    def setCurrentElement(self,data, image =-1):
        element_type_id = data[0]
        property_list = data[1]
        self.show()
        self.activateWindow()
        self.setMode("AddMode")
        id = ''
        name = ''
        if self.reportDir != -1:
            id, nb = self.generateId(element_type_id)
            name = self.elementNames[element_type_id] + "#" + nb.__str__()
        else:
            self.setEnabled(False)
            self.reportLoadDialog.show()
            self.reportLoadDialog.activateWindow()

        self.setElementType(element_type_id)
        property_list.insert(0, name)
        property_list.insert(0, id)
        if image != -1:
            for i in range(0,property_list.__len__()):
                if property_list[i] == "imgPath":
                    property_list[i] = "generateImgPath"
            self.clearImages()
            self.PILImageList.append(image)
            self.currentImageIndex = 0
        self.setTableItems(property_list)

    def addCurrentElementToReport(self):
        lineData = []
        for i in range(0,self.tableWidget.rowCount()):
            lineData.append(self.tableWidget.item(i,0).text().__str__().encode('utf-8'))
            if self.tableWidget.verticalHeaderItem(i).text() == "Zdjęcia".decode('utf-8'):
                paths = self.tableWidget.item(i,0).text().__str__().encode('utf-8')
                if "," in paths:
                    paths = paths.split(",")
                else:
                    paths = [paths]
                print paths
                base_dir = self.reportDir.__str__().rsplit("/", 1)[0]
                for j in range(0,paths.__len__()):
                    if j < self.PILImageList.__len__():
                        print base_dir + "/" + paths[j]
                        self.PILImageList[j].save(base_dir + "/" + paths[j])
        self.setTableItems(lineData)

        type_id = self.comboBox_type.currentIndex()
        element_id = self.tableWidget.item(0,0).text()
        report = open(self.reportDir,"r")
        found = False
        new = False
        j = -1
        i = 0
        report_reader = csv.reader(report)
        report_content = []
        for line in report_reader:
            report_content.append(line)
            if len(line) >= 3 and line[2] == "RodzajID:" and line[3]==type_id.__str__():

                found = True
            if found and len(line) == 0:
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
        report_writer = csv.writer(report)
        report_writer.writerows(report_content)
        report.close()
        for i in range(0,self.treeWidget.topLevelItemCount()):
            top_level_item = self.treeWidget.topLevelItem(i)
            element_type_id = top_level_item.data(1, QtCore.Qt.UserRole).toString()
            if type_id.__str__() == element_type_id:
                name = lineData[1]
                id = lineData[0]
                if new:
                    child_item = QtGui.QTreeWidgetItem()
                    child_item.setText(0, _translate("Dialog", name, None))
                    child_item.setText(1, _translate("Dialog", id, None))
                    top_level_item.addChild(child_item)
                else:
                    for j in range(0,top_level_item.childCount()):
                        child = top_level_item.child(j)
                        if child.text(1) == id:
                            child_item = child
                            child_item.setText(0, _translate("Dialog", name, None))
                self.treeWidget.setCurrentItem(child_item,0)

    def getElementData(self,id):
        report = open(self.reportDir,'r')
        report_reader = csv.reader(report)
        for line in report_reader:
            if len(line) > 1 and line[0] == id.__str__():
                return line
        report.close()

    def deleteCurrentElementFromReport(self):
        if self.mode == "AddMode":
            self.tableWidget.clearContents()
            self.clearImages()
            self.setMode("NormalMode")
        elif self.mode == "ChangeMode":
            current_item = self.treeWidget.currentItem()
            parent = current_item.parent()
            id = current_item.text(1)
            self.deleteElementFromReport(id)
            parent.takeChild(parent.indexOfChild(current_item))
            self.pushButton_delete.setEnabled(False)
            self.pushButton_add_change.setEnabled(False)
            self.tableWidget.clearContents()
            self.clearImages()

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

    def setTableItems(self,item_list, clear=True):
        if clear:
            self.tableWidget.clearContents()
        i = 0
        for item_val in item_list:
            item = QtGui.QTableWidgetItem()
            if i == 0:
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.item(i, 0).setText(item_val.decode('utf-8'))
            if self.tableWidget.verticalHeaderItem(i).text() == "Zdjęcia".decode('utf-8'):
                if (item_val.decode('utf-8')) == "generateImgPath":
                    self.tableWidget.item(i,0).setText(item_list[0] + ".png")
                else:
                    self.clearImages()
                    self.loadImages((item_val.decode('utf-8')).split(","))
                self.currentImageIndex = 0
                if self.PILImageList.__len__() > 1:
                    self.pushButton_next.setEnabled(True)
                    self.pushButton_prev.setEnabled(True)
                else:
                    self.pushButton_next.setEnabled(False)
                    self.pushButton_prev.setEnabled(False)
                self.showCurrentImage()
            else:
                self.pushButton_next.setEnabled(False)
                self.pushButton_prev.setEnabled(False)
            i = i + 1
        for i in range(0,self.tableWidget.rowCount()):
            if self.tableWidget.verticalHeaderItem(i).text() == "Zdjęcia".decode('utf-8'):
                if self.tableWidget.item(i, 0) and (self.tableWidget.item(i, 0).text().__str__().decode('utf-8')) == ".png":
                    self.tableWidget.item(i, 0).setText(item_list[0] + ".png")

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
        new_id = 0
        ids = []
        report = open(self.reportDir,'r')
        found_type = False
        report_reader = csv.reader(report)

        for line in report_reader:
            if len(line) >= 3 and line[2] == "RodzajID:" and line[3]==element_type_id.__str__():
                found_type = True
            elif found_type and len(line) == 0:
                if len(ids) != 0:
                    ids.sort()
                    for id in ids:
                        if new_id == id:
                            new_id = id +1
                        else:
                            return id_base + (new_id).__str__(), (new_id)
                return id_base + (new_id).__str__(), (new_id)
            elif found_type and len(line) != 0  and line[0] != "Id":
                ids.append(int(line[0].replace(id_base,'')))


        return id_base + (new_id).__str__(),(new_id)

    def showCurrentImage(self):
        self.showImage(self.currentImageIndex)

    def showImage(self, index):
        array = np.array(self.PILImageList[index])
        image = QtGui.QImage(array, array.shape[1], array.shape[0], array.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(image)
        pixitem = QtGui.QGraphicsPixmapItem(pixmap)
        scene = QtGui.QGraphicsScene()
        scene.addItem(pixitem)
        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(pixitem,QtCore.Qt.KeepAspectRatio)
        self.setImageCountLabel()

    def clearImages(self):
        print "clear"
        self.PILImageList = []
        self.currentImageIndex = -1
        if self.graphicsView.scene():
            self.graphicsView.scene().clear()
        self.graphicsView.update()
        self.setImageCountLabel()

    def setImageCountLabel(self):
        if self.PILImageList.__len__() > 0:
            text = (self.currentImageIndex + 1).__str__() + "/" + (self.PILImageList.__len__()).__str__()
            self.label_img.setText(text)
        else:
            self.label_img.setText("0/0")

    def nextImage(self):
        self.currentImageIndex = (self.currentImageIndex + 1).__mod__(self.PILImageList.__len__())
        self.showCurrentImage()

    def prevImage(self):
        self.currentImageIndex = (self.currentImageIndex - 1).__mod__(self.PILImageList.__len__())
        self.showCurrentImage()

    def loadImages(self, image_names_list):
        base_dir = self.reportDir.__str__().rsplit("/", 1)[0]
        for image_name in image_names_list:
            self.currentPILImage = Image.open(base_dir + "/" + image_name)
            img = copy.deepcopy(self.currentPILImage)
            self.PILImageList.append(img)



