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
from ScanManager import ScanManager
from WeldDetector import WeldDetector
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
        self.comboBox_element.currentIndexChanged.connect(self.setTreeWidgetHeader)
        self.treeWidget.currentItemChanged.connect(self.treeItemSelected)
        self.setTreeWidgetHeader(0)
        self.radioButton_select.setVisible(False)
        self.pushButton_select.setVisible(False)
        self.pushButton_report.setEnabled(False)
        self.pushButton_show.setEnabled(False)
        self.milimiters_from = 0
        self.milimiters_end = 0

    def showElementInMainWindow(self):
        item = self.treeWidget.currentItem()
        milimiters = item.data(1, QtCore.Qt.UserRole).toList()[1].toFloat()[0]*1000
        range = 500.0
        self.emit(SIGNAL('showElement(PyQt_PyObject)'),[milimiters - range, milimiters + range])

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
        self.dataLoaded = True
        self.treeWidget.clear()
        self.weldDetector = WeldDetector(self.scanManager.thicknessScan)
        self.connect(self.weldDetector, SIGNAL('weldDetected(PyQt_PyObject)'), self.addToList)
        self.connect(self.weldDetector, SIGNAL('finished()'), self.detectionFinished)
        self.weldDetector.start()

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


    def detectionFinished(self):
        self.dataLoaded = False
        self.pushButton_detect.setEnabled(True)

    def loadData(self):
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
