# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL
import numpy as np
from math import sqrt
import AutoDetectWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
import matplotlib
import matplotlib.pyplot as plt
import time
from ScanManager import ScanManager
from WeldDetector import WeldDetector
from CorrosionDetector import CorrosionDetector
from Miscellaneous import ReportTools
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class AutoDetectDialog(QtGui.QDialog, AutoDetectWindow.Ui_Dialog):
    def __init__(self,opt_dialog):
        super(self.__class__, self).__init__()
        self.options = opt_dialog
        self.setupUi(self)
        self.dataLoaded = False
        self.scanManager = ScanManager()
        self.connect(self.pushButton_detect,SIGNAL('clicked()'), self.loadData)
        self.connect(self.scanManager, SIGNAL('scans2dLoaded()'), self.startDetection)
        self.connect(self.pushButton_show,SIGNAL('clicked()'),self.showElementInMainWindow)
        self.connect(self.pushButton_report, SIGNAL('clicked()'), self.reportElement)
        self.comboBox_element.currentIndexChanged.connect(self.setElementType)
        self.treeWidget.currentItemChanged.connect(self.treeItemSelected)
        self.tableWidget.verticalHeader().geometriesChanged.connect(self.adjustTableSize)
        self.comboBox_element.setCurrentIndex(0)
        self.radioButton_select.setVisible(False)
        self.pushButton_select.setVisible(False)
        self.pushButton_report.setEnabled(False)
        self.pushButton_show.setEnabled(False)
        self.milimiters_from = 0
        self.milimiters_end = 0
        self.start_time = 0

    def setElementType(self,index):
        self.setTreeWidgetHeader(index)
        self.tableWidget.clear()
        if index == 0:
            self.setTableItems(["Minimalna odległość między spoinami obwodowymi l [mm]",
                                      "Wysokość okna poszukiwania spoiny obwodowej W [mm]",
                                      "Próg odnalezienia spoiny d_o [%] "], [50,25,50])
        elif index == 1:
            self.setTableItems(["Minimalna odległość między spoinami obwodowymi l [mm]",
                                      "Szerokość okna poszukiwania spoiny obwodowej W [mm]",
                                      "Próg odnalezienia spoiny obowodowej d_o [%]",
                                      "Wysokość okna poszukiwania spoiny wzdłużnej H [mm]",
                                      "Próg odnalezienia spoiny wzdłużnej d_w [%]"], [50,25,50,25,40])
        elif index == 2:
            self.setTableItems(["Minimalna odległość między spoinami obwodowymi l [mm]",
                                      "Szerokość okna poszukiwania spoiny obwodowej W [mm]",
                                      "Próg odnalezienia spoiny obowodowej d_o [%]",
                                      "Wysokosć okna poszukiwania spoiny wzdłużnej H [mm]",
                                      "Próg odnalezienia spoiny wzdłużnej d_w [%]",
                                      "Próg korozji t_p [%]",
                                      "Próg sąsiedztwa l_bmax [%]",
                                      "Współczynnik progujący l_p [%]"], [50,25,50,25,40, 15, 50, 70])
        self.tableWidget.hide() # hide and show in order to fire geomtriesChanged signal to update size of tablewidget
        self.tableWidget.show()



    def getAlgParameters(self):
        params = []
        for i in range(0,self.tableWidget.rowCount()):
            params.append(self.tableWidget.item(i, 0).text())
        return params

    def setTableItems(self, item_names_list, val_list):
        i = 0
        self.tableWidget.setRowCount(len(item_names_list))
        for name in item_names_list:
            item = QtGui.QTableWidgetItem()
            item.setText(_translate("Dialog", name, None))
            self.tableWidget.setVerticalHeaderItem(i, item)
            item = QtGui.QTableWidgetItem()
            item.setText(val_list[i].__str__().decode('utf-8'))
            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.item(i, 0)
            i = i + 1

    def adjustTableSize(self):
        #print self.tableWidget.verticalHeader().width() + self.tableWidget.columnWidth(0)
        margins = self.tableWidget.getContentsMargins()
        height = self.tableWidget.verticalHeader().length() + margins[1] + margins[3]
        width = self.tableWidget.columnWidth(0) + self.tableWidget.verticalHeader().width()
        self.tableWidget.setMaximumHeight(height)
        self.tableWidget.setMinimumHeight(height)
        self.tableWidget.setMaximumWidth(width)
        self.tableWidget.setMinimumWidth(width)


    def showElementInMainWindow(self):
        item = self.treeWidget.currentItem()
        milimiters = item.data(1, QtCore.Qt.UserRole).toList()[1].toFloat()[0]*1000
        self.emit(SIGNAL('showElement(PyQt_PyObject)'),[milimiters])

    def reportElement(self):
        item = self.treeWidget.currentItem()
        id = item.data(1, QtCore.Qt.UserRole).toList()[0].toInt()[0]
        if id==ReportTools.SP.value:
            x = item.data(1, QtCore.Qt.UserRole).toList()[1].toFloat()[0]
            loc = "X: " + x.__str__() + " m"
            self.emit(SIGNAL('reportElement(PyQt_PyObject)'), [ReportTools.SP.value, [loc, "-", "-", "-"]])
        elif id==ReportTools.SW.value:
            x = item.data(1, QtCore.Qt.UserRole).toList()[1].toFloat()[0]
            y = item.data(1, QtCore.Qt.UserRole).toList()[2].toList()
            yh = y[0].toInt()[0]
            ym = y[1].toInt()[0]
            w = item.data(1, QtCore.Qt.UserRole).toList()[3].toFloat()[0]
            width = w.__str__() + " m"
            loc = "X: "+ x.__str__() + " m, " + "Y: " + yh.__str__() + " h "+ ym.__str__() + " min"
            self.emit(SIGNAL('reportElement(PyQt_PyObject)'), [ReportTools.SP.value, [loc, width, "-", "-"]])
        #self.emit(SIGNAL('reportElement(PyQt_PyObject)'),[ReportTools.SP.value, [loc,"-","-","-"]] )

    def treeItemSelected(self,item):
        if item:
            self.pushButton_report.setEnabled(True)
            self.pushButton_show.setEnabled(True)
        else:
            self.pushButton_report.setEnabled(False)
            self.pushButton_show.setEnabled(False)

    def setTreeWidgetHeader(self, index):
        if index == 0:
            self.treeWidget.headerItem().setText(0, _translate("Dialog", "Nazwa", None))
            self.treeWidget.headerItem().setText(1, _translate("Dialog", "Lokalizacja", None))

    def startDetection(self):
        print "load data time: ", time.time() -  self.start_time
        print "bytes:", self.scanManager.thicknessScan.nbytes
        self.dataLoaded = True
        self.treeWidget.clear()
        id = self.comboBox_element.currentIndex()
        if id == 0:
            params = self.getAlgParameters()
            spacing = int(float(params[0])/self.scanManager.deltaX)
            weld_width_v = int(float(params[1])/self.scanManager.deltaX)
            percentage_v = float(params[2])/100.0
            self.weldDetector = WeldDetector(self.scanManager.thicknessScan, self.scanManager.getThicknessData(0,0,0,0,all=True),
                                             0, spacing, weld_width_v, percentage_v)
            self.connect(self.weldDetector, SIGNAL('weldDetected(PyQt_PyObject)'), self.addToList)
            self.connect(self.weldDetector, SIGNAL('reportProgress(PyQt_PyObject)'), self.setProgress)
            self.connect(self.weldDetector, SIGNAL('finished()'), self.detectionFinished)
            self.weldDetector.start()
        elif id == 1:
            params = self.getAlgParameters()
            spacing = int(float(params[0]) / self.scanManager.deltaX)
            weld_width_v = int(float(params[1]) / self.scanManager.deltaX)
            percentage_v = float(params[2]) / 100.0
            weld_width_h = int(float(params[3]) / self.scanManager.deltaY)
            percentage_h = float(params[4]) / 100.0
            self.weldDetector = WeldDetector(self.scanManager.thicknessScan, self.scanManager.getThicknessData(0,0,0,0,all=True),
                                             1, spacing, weld_width_v, percentage_v, weld_width_h, percentage_h)
            self.connect(self.weldDetector, SIGNAL('weldDetected(PyQt_PyObject)'), self.addToList)
            self.connect(self.weldDetector, SIGNAL('reportProgress(PyQt_PyObject)'), self.setProgress)
            self.connect(self.weldDetector, SIGNAL('finished()'), self.detectionFinished)
            self.weldDetector.start()
        elif id == 2:
            params = self.getAlgParameters()
            spacing = int(float(params[0]) / self.scanManager.deltaX)
            weld_width_v = int(float(params[1]) / self.scanManager.deltaX)
            percentage_v = float(params[2]) / 100.0
            weld_width_h = int(float(params[3]) / self.scanManager.deltaY)
            percentage_h = float(params[4]) / 100.0
            treshold = 1 - float(params[5]) / 100.0
            lbmax = float(params[6]) / 100.0
            lp = float(params[7]) / 100.0
            self.corrosionDetector = CorrosionDetector(self.scanManager.thicknessScan,self.scanManager.nominalThicknessVal,
                                                       self.scanManager.getThicknessData(0,0,0,0,all=True),
                                                       self.scanManager.nominalThickness, treshold,self.scanManager.deltaX,self.scanManager.diameter,
                                                       spacing, weld_width_v, percentage_v, weld_width_h, percentage_h, lbmax, lp)
            self.connect(self.corrosionDetector, SIGNAL('corrosionDetected(PyQt_PyObject)'), self.addToList)
            self.connect(self.corrosionDetector, SIGNAL('reportProgress(PyQt_PyObject)'), self.setProgress)
            self.connect(self.corrosionDetector, SIGNAL('finished()'), self.detectionFinished)
            self.corrosionDetector.start()

    def setProgress(self,percentage):
        progress_bar_val = int(percentage*100)
        self.progressBar.setValue(progress_bar_val)

    def addToList(self,list):
        item = QtGui.QTreeWidgetItem(self.treeWidget)
        name = list[0]
        id = list[1]
        if id==ReportTools.SP:
            x = (float(list[2] * self.options.DeltaX) + self.milimiters_from) / 1000
            item.setText(0, _translate("Dialog", name.__str__(), None))
            item.setText(1, _translate("Dialog", "X: " + x.__str__() + " m", None))
            item.setData(1, QtCore.Qt.UserRole, [ReportTools.SP.value, x])
        elif id==ReportTools.SW:
            x = (float(list[3] * self.options.DeltaX) + self.milimiters_from) / 1000
            y = float(list[2])
            x,y,d = self.scanManager.getXYD(list[3],list[2], no_ratio=True)
            width = float(list[4] * self.options.DeltaX)/ 1000
            item.setText(0, _translate("Dialog", name.__str__(), None))
            item.setText(1, _translate("Dialog", "X: " + x.__str__() + " m, " + "Y: " + y[0].__str__() + " h "+ y[1].__str__() + " min,"  + " Dlugość: " + width.__str__() + " m", None))
            item.setData(1, QtCore.Qt.UserRole, [ReportTools.SW.value, x,y,width])
        elif id==ReportTools.K:
            x, y, d = self.scanManager.getXYD(list[3], list[2], no_ratio=True)
            item.setText(0, _translate("Dialog", name.__str__(), None))
            item.setText(1, _translate("Dialog", "X: " + x.__str__() + " m, " + "Y: " + y[0].__str__() + " h " + y[
                1].__str__() + " min", None))
            item.setData(1, QtCore.Qt.UserRole, [ReportTools.SW.value, x, y])

    def detectionFinished(self):
        self.dataLoaded = False
        self.pushButton_detect.setEnabled(True)
        print "detection time: ", time.time() - self.start_time

    def loadData(self):
        self.start_time = time.time()
        self.pushButton_detect.setEnabled(False)
        if not self.dataLoaded:
            if self.radioButton_all.isChecked():
                self.milimiters_from = 0
                self.milimiters_end = -1
            elif self.radioButton_start_end.isChecked():
                if self.comboBox_m_unit_start.currentIndex() == 0:
                    multiplier = 1
                elif self.comboBox_m_unit_start.currentIndex() == 1:
                    multiplier = 1000
                elif self.comboBox_m_unit_start.currentIndex() == 2:
                    multiplier = 1000000
                self.milimiters_from = float(self.textEdit_m_start.toPlainText().replace(",",".")) * multiplier
                if self.comboBox_m_unit_end.currentIndex() == 0:
                    multiplier = 1
                elif self.comboBox_m_unit_end.currentIndex() == 1:
                    multiplier = 1000
                elif self.comboBox_m_unit_end.currentIndex() == 2:
                    multiplier = 1000000
                self.milimiters_end = float(self.textEdit_m_end.toPlainText().replace(",", ".")) * multiplier
            elif self.radioButton_select.isChecked():
                self.milimiters_from = 0
                self.milimiters_end = 0
                print "unsupported yet"
            scan_dir = unicode(self.options.dataDir)
            a = self.options.CoefficientA
            b = self.options.CoefficientB
            c = self.options.CoefficientC
            d = self.options.CoefficientD
            delta_x = self.options.DeltaX
            diameter = self.options.Diameter
            nominal_thickness = self.options.thickness
            nominal_distance = self.options.nominalDistance
            bd0 = self.options.distanceStartByte
            bd1 = self.options.distanceEndByte
            bt0 = self.options.thicknessStartByte
            bt1 = self.options.thicknessEndByte
            frame_length = self.options.frameLength
            self.scanManager.loadScanFromTo(self.milimiters_from, self.milimiters_end, scan_dir, a, b, c, d, delta_x, diameter,
                                      nominal_thickness, nominal_distance, bd0,bd1,bt0,bt1,frame_length)
        else:
            self.startDetection()
