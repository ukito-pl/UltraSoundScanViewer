# -*- coding: utf-8 -*-

from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication
import numpy as np
from LoadScansThread import LoadScansThread
from PyQt4 import QtCore
import time


import MainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from options import OptionsDialog
from selection import SelectionDialog
from ScanManager import ScanManager

class MainApp(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mouseMode = 0      #0-przesuwanie, 1 -zaznaczanie
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
        self.connect(self.scanViewer, SIGNAL('mouseButtonReleased()'), self.mouseButtonReleased)
        self.connect(self.scanViewer, SIGNAL('changeScale()'), self.changeScale)

        self.connect(self.scanManager, SIGNAL('showScan(PyQt_PyObject)'), self.showScan)
        self.connect(self.scanManager, SIGNAL('updateScan(PyQt_PyObject)'), self.updateScan)

        self.verticalSlider.valueChanged.connect(self.rearrangeScan)

    def mouseButtonReleased(self):
        if (self.mouseMode == 1 and self.scanViewer.scene() != 0):
            rect =self.scanViewer.scene().selectionArea().controlPointRect()
            x = rect.x().__int__()
            y = rect.y().__int__()
            w = rect.width().__int__()
            h = rect.height().__int__()
            print rect,x,y,w,h
            self.selectionDialog.show()
            self.selectionDialog.showImage(self.scanManager.imgScan[y:y+h, x:x+w, :])
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
        if (QKeyEvent.key() == QtCore.Qt.Key_Control and self.mouseMode == 0):
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self.mouseMode = 1
        elif (QKeyEvent.key() == QtCore.Qt.Key_Control and self.mouseMode == 1):
            self.scanViewer.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.mouseMode = 0

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
        currentFrame = ((float(self.textEdit_km.toPlainText()) * 1000) / self.optionsDialog.DeltaX).__int__()
        scan_dir = unicode(self.optionsDialog.dataDir)
        a = self.optionsDialog.CoefficientA
        b = self.optionsDialog.CoefficientB
        c = self.optionsDialog.CoefficientC
        d = self.optionsDialog.CoefficientD
        delta_x = self.optionsDialog.DeltaX
        diameter = self.optionsDialog.Diameter
        nominal_depth = self.optionsDialog.Depth
        self.scanManager.loadScan(currentFrame, scan_dir, a, b, c, d, delta_x, diameter, nominal_depth)

    def showScan(self, image):
        self.scanViewer.clearItems()
        self.scanViewer.aspect_ratio = self.scanManager.resolutionRatio
        self.scanViewer.setScanImage(image)

        self.addScaleBar(7)

        hor_bar_height = self.scanViewer.horizontalScrollBar().height()

        if self.scanViewer.view_scale == 1:
            self.scanViewer.setMinimumSize(QtCore.QSize(0, self.scanViewer.scanScene.height() + hor_bar_height + self.scanViewer.frameWidth()*2))
            self.scanViewer.setMaximumSize(QtCore.QSize(16777215, self.scanViewer.scanScene.height() + hor_bar_height + self.scanViewer.frameWidth()*2))
            self.graphicsView_2.setMaximumHeight(self.scanViewer.height())
            self.verticalSlider.setMaximumHeight(self.scanViewer.height())

        self.colorLegend("ironfire")

        frame_range = (self.scanManager.endFrame - self.scanManager.startFrame).__float__()
        px = ((self.scanManager.currentFrame - self.scanManager.startFrame) / frame_range)
        self.scanViewer.goTo(px)
        self.scanViewer.moveScaleBar()

    def updateScan(self,image):
        self.scanViewer.setScanImage(image)

    def addScaleBar(self, scale_line_height):
        # scale_line_height - in pixels
        items = self.scanManager.getScaleBarItems(self.scale_spacing, scale_line_height, self.scanViewer.view_scale, self.optionsDialog.DeltaX)
        for i in range(0,len(items)):
            self.scanViewer.addItem(items[i][0],items[i][1],items[i][2])


    def colorLegend(self,scale_name):
        legend_array =  np.zeros((256,20,3),dtype=np.uint8)
        for i in range(1,legend_array.shape[0] - 1):
            legend_array[i,1:19 , :] = self.scanManager.colorMapping.lookUpTables["ironfire"][-i-1]

        image = QtGui.QImage(legend_array, legend_array.shape[1], legend_array.shape[0], legend_array.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        legendPixMap = QtGui.QPixmap(image)
        legendPixMapItem = QtGui.QGraphicsPixmapItem(legendPixMap)
        scene = QtGui.QGraphicsScene()
        scene.addItem(legendPixMapItem)
        self.graphicsView_2.setScene(scene)
        self.graphicsView_2.fitInView(scene.sceneRect())







def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()