# -*- coding: utf-8 -*-

from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication
import numpy as np
from LoadScansThread import LoadScansThread
from PyQt4 import QtCore
import time
import pyqtgraph.opengl as gl


import MainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from options import OptionsDialog
from selection import SelectionDialog
from ScanManager import ScanManager
from math import log10
from Miscellaneous import isclose

class MainApp(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.scale_spacing = 0.1 # in meters
        self.statusBarMessage = ""
        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setText(self.statusBarMessage)
        self.statusbar.addWidget(self.statusLabel)
        self.optionsDialog = OptionsDialog()
        self.selectionDialog = SelectionDialog()
        self.scanManager = ScanManager()

        self.connect(self.pushButton_options, SIGNAL('clicked()'), self.openOptions)
        self.connect(self.pushButton_go, SIGNAL('clicked()'), self.loadScan)

        self.connect(self.scanViewer, SIGNAL('mousePositionChanged(PyQt_PyObject)'), self.mousePositionChanged)
        self.connect(self.scanViewer, SIGNAL('areaSelected(PyQt_PyObject)'), self.showSelection)
        self.connect(self.scanViewer, SIGNAL('changeScale()'), self.changeScale)

        self.connect(self.scanManager, SIGNAL('showScan(PyQt_PyObject)'), self.showScan)
        self.connect(self.scanManager, SIGNAL('updateScan(PyQt_PyObject)'), self.updateScan)

        self.connect(self.selectionDialog, SIGNAL('evaluateMAOP(PyQt_PyObject)'), self.scanManager.evaluateMAOP)

        self.verticalSlider.valueChanged.connect(self.rearrangeScan)

        ukl_wsp_line_length = 3
        ukl_wsp_line_width = 4
        ukl_wsp_x = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [ukl_wsp_line_length, 0, 0]]), color=[1, 0, 0, 1],
                                      width=ukl_wsp_line_width,
                                      antialias=True, mode='lines')
        ukl_wsp_y = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, ukl_wsp_line_length, 0]]), color=[0, 1, 0, 1],
                                      width=ukl_wsp_line_width,
                                      antialias=True, mode='lines')
        ukl_wsp_z = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 0, ukl_wsp_line_length]]), color=[0, 0, 1, 1],
                                      width=ukl_wsp_line_width,
                                      antialias=True, mode='lines')
        self.graphicsView.addItem(ukl_wsp_x)
        self.graphicsView.addItem(ukl_wsp_y)
        self.graphicsView.addItem(ukl_wsp_z)
        self.graphicsView.setBackgroundColor([128,128,128,255])

    def closeEvent(self, QCloseEvent):
        self.selectionDialog.close()
        self.optionsDialog.close()
        super(self.__class__, self).closeEvent(QCloseEvent)

    def showSelection(self, rect):
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        self.selectionDialog.show()
        self.selectionDialog.showImage(rect,self.scanManager.imgScanColoredRearranged[y:y+h, x:x+w, :],self.scanViewer.aspect_ratio)
        self.selectionDialog.activateWindow()

    def mousePositionChanged(self, QMouseEvent):
        try:
            position = self.scanViewer.mapToScene(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            position = position/self.scanViewer.view_scale
            [x, y, d] = self.scanManager.getXYD(position.x(), position.y())
            self.statusBarMessage = 'X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:.3F}".format(y) + ' mm  Grubosc: ' + "{:.3F}".format(d) + ' mm'
            self.statusLabel.setText(self.statusBarMessage)
            self.statusbar.update()
        except:

            return

    def keyPressEvent(self, QKeyEvent):
        if (QKeyEvent.key() == QtCore.Qt.Key_Control):
            self.scanViewer.changeDragMode()


    def openOptions(self):
        self.optionsDialog.show()

    def changeScale(self):
        spacing_px_org = self.scale_spacing / self.optionsDialog.DeltaX * 1000
        spacing_px = float(spacing_px_org * self.scanViewer.view_scale)
        if spacing_px > 130:
            self.scale_spacing = self.scale_spacing / 2
        elif spacing_px < 40:
            self.scale_spacing = self.scale_spacing * 2
        self.addScaleBar(7)

    def rearrangeScan(self):
        val = float(self.verticalSlider.value())
        min = float(self.verticalSlider.minimum())
        max = float(self.verticalSlider.maximum())
        val_ratio = float(val / (max - min))
        self.scanManager.rearrangeScan(val_ratio)

    def loadScan(self):
        if self.comboBox_3.currentIndex() == 0:
            multiplier = 1
        elif self.comboBox_3.currentIndex() == 1:
            multiplier = 1000
        elif self.comboBox_3.currentIndex() == 2:
            multiplier = 1000000
        milimeters = float(self.textEdit_km.toPlainText().replace(",",".")) * multiplier
        milimeters_range = float(self.textEdit_km_range.toPlainText().replace(",",".")) * 1000
        scan_dir = unicode(self.optionsDialog.dataDir)
        a = self.optionsDialog.CoefficientA
        b = self.optionsDialog.CoefficientB
        c = self.optionsDialog.CoefficientC
        d = self.optionsDialog.CoefficientD
        delta_x = self.optionsDialog.DeltaX
        diameter = self.optionsDialog.Diameter
        nominal_depth = self.optionsDialog.Depth
        self.scanManager.loadScan(milimeters, milimeters_range, scan_dir, a, b, c, d, delta_x, diameter, nominal_depth)

    def showScan(self, image):
        self.scanViewer.clearScene()
        self.scanViewer.resetViewScale()
        self.scanViewer.aspect_ratio = self.scanManager.resolutionRatio
        self.scanViewer.setScanImage(image)

        self.addScaleBar(7)

        self.rearrangeScan()

        frame_range = (self.scanManager.endFrame - self.scanManager.startFrame).__float__()
        px = ((self.scanManager.currentFrame - self.scanManager.startFrame) / frame_range)
        self.scanViewer.goTo(px)
        self.scanViewer.moveScaleBar()
        self.scanViewer.moveScaleBar()
        self.colorLegend("ironfire")

    def updateScan(self,image):
        self.scanViewer.setScanImage(image)

    def addScaleBar(self, scale_line_height):
        # scale_line_height - in pixels
        items = self.scanManager.getScaleBarItems(self.scale_spacing, scale_line_height, self.scanViewer.view_scale, self.optionsDialog.DeltaX)
        for i in range(0,len(items)):
            self.scanViewer.addItem(items[i][0],items[i][1],items[i][2])


    def colorLegend(self,scale_name):
        scene = QtGui.QGraphicsScene()
        items = self.scanManager.getColorLegendItems(400)
        for item in items:
            scene.addItem(item)
        self.graphicsView_2.setScene(scene)
        self.graphicsView_2.setMinimumHeight(scene.sceneRect().height())







def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()