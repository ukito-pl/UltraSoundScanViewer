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
        self.startFrame = 0
        self.endFrame = 0
        self.currentFrame = 0
        self.scanLoaded = False
        self.statusBarMessage = ""
        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setText(self.statusBarMessage)
        self.statusbar.addWidget(self.statusLabel)
        self.optionsDialog = OptionsDialog()
        self.selectionDialog = SelectionDialog()
        self.scanManager = ScanManager()

        self.connect(self.pushButton_options, SIGNAL('clicked()'), self.openOptions)
        self.connect(self.pushButton_go, SIGNAL('clicked()'), self.goToCurrentFrame)

        self.connect(self.scanViewer, SIGNAL('mousePositionChanged(PyQt_PyObject)'), self.mousePositionChanged)
        self.connect(self.scanViewer, SIGNAL('mouseButtonReleased()'), self.mouseButtonReleased)
        self.connect(self.scanViewer, SIGNAL('changeScale()'), self.changeScale)

        self.connect(self.scanManager, SIGNAL('showScan(PyQt_PyObject)'), self.showScan)
        self.connect(self.scanManager, SIGNAL('updateScan(PyQt_PyObject)'), self.updateScan)

        self.verticalSlider.valueChanged.connect(self.rearrangeScan)


    def changeScale(self):
        spacing_px_org = self.scale_spacing / self.optionsDialog.DeltaX * 1000
        spacing_px = float(spacing_px_org * self.scanViewer.view_scale)
        if spacing_px > 130:
            self.scale_spacing = self.scale_spacing / 2
        elif spacing_px < 40:
            self.scale_spacing = self.scale_spacing * 2
        #print self.scale_spacing
        self.addScaleBarToImage(self.scale_spacing, 7)

    def rearrangeScan(self):
        val = float(self.verticalSlider.value())
        min = float(self.verticalSlider.minimum())
        max = float(self.verticalSlider.maximum())
        val_ratio = float(val / (max - min))
        self.scanManager.rearrangeScan(val_ratio)


    def goToCurrentFrame(self):
        self.currentFrame = ((float(self.textEdit_km.toPlainText()) * 1000) / self.optionsDialog.DeltaX).__int__()
        self.startFrame = (self.currentFrame - 5000).__int__()
        self.endFrame = (self.currentFrame + 5000).__int__()
        scan_dir = unicode(self.optionsDialog.dataDir)
        self.scanManager.loadScan(self.currentFrame, scan_dir)



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
        if self.scanLoaded:
            position = self.scanViewer.mapToScene(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            position = position/self.scanViewer.view_scale
            x = ((position.x() + self.startFrame)*self.optionsDialog.DeltaX)/1000 #in meters
            deltaY = 3.14 * self.optionsDialog.Diameter / 256.0
            y = position.y()*deltaY

            indx = position.x()
            if indx < 0:
                indx = 0
            elif indx > (self.scanManager.imgScan.shape[1] - 1):
                indx = self.scanManager.imgScan.shape[1] - 1
            indy = position.y()
            if indy < 0:
                indy = 0
            elif indy > (self.scanManager.imgScan.shape[0] - 1):
                 indy = self.scanManager.imgScan.shape[0] - 1
            C = self.optionsDialog.CoefficientC
            D = self.optionsDialog.CoefficientD
            depth = C * self.scanManager.imgScan[int(indy),int(indx),0] + D
            self.statusBarMessage = 'X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:.3F}".format(y) + ' mm  Grubosc: ' + "{:.3F}".format(depth) + ' mm'
            self.statusLabel.setText(self.statusBarMessage)
            self.statusbar.update()


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


    def updateScan(self,image):
        self.scanViewer.setScanImage(image)

    def showScan(self, image):
        self.scanViewer.clearScene()
        self.scanViewer.setScanImage(image)

        scale_height = self.addScaleBarToImage(self.scale_spacing, 7)

        hor_bar_height = self.scanViewer.horizontalScrollBar().height()
        self.scanViewer.setMinimumSize(QtCore.QSize(0, 256 + scale_height + hor_bar_height / 2))
        self.scanViewer.setMaximumSize(QtCore.QSize(16777215, 256 + scale_height + hor_bar_height / 2))
        self.graphicsView_2.setMaximumHeight(self.scanViewer.height())
        self.verticalSlider.setMaximumHeight(self.scanViewer.height())

        self.scanLoaded = True
        self.colorLegend("ironfire")

        frame_range = (self.endFrame - self.startFrame).__float__()
        px = ((self.currentFrame - self.startFrame) / frame_range)
        self.scanViewer.goTo(px)
        self.scanViewer.moveScaleBar()

    ##jeszcze to przesuń do scanManagera
    def addScaleBarToImage(self, spacing, scale_line_height):
        # spacing - in meters
        # scale_line_height - in pixels
        self.scanViewer.pos = np.zeros((10000, 2))
        spacing_px_org = spacing / self.optionsDialog.DeltaX * 1000  # because deltaX is in mm
        spacing_px = float(spacing_px_org * self.scanViewer.view_scale)
        scaleLineImg = 0 * np.ones(
            (scale_line_height, (self.scanManager.imgScan.shape[1] * self.scanViewer.view_scale).__int__(), 3), dtype=np.uint8)
        # print spacing_px
        for i in range(((self.scanManager.imgScan.shape[1] * self.scanViewer.view_scale) // spacing_px).__int__()):
            left_bound = (i * spacing_px).__int__()
            right_bound = (i * spacing_px + spacing_px).__int__()
            if i.__mod__(2) == 1:
                scaleLineImg[1:scale_line_height - 1, left_bound:right_bound] = 50 * np.ones(
                    (1, right_bound - left_bound, 3))
            else:
                scaleLineImg[1:scale_line_height - 1, left_bound:right_bound] = 255 * np.ones(
                    (1, right_bound - left_bound, 3))

        scaleLineImage = QtGui.QImage(scaleLineImg, scaleLineImg.shape[1], scaleLineImg.shape[0],
                                      scaleLineImg.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.scanViewer.addImage(scaleLineImage, 0, -scale_line_height, 1000)

        for i in range(((self.scanManager.imgScan.shape[1] * self.scanViewer.view_scale) // spacing_px).__int__()):
            x = ((i * spacing_px_org.__int__() + self.startFrame) * self.optionsDialog.DeltaX) / 1000  # in meters

            textItem = QtGui.QGraphicsTextItem(x.__str__())
            font = QtGui.QFont()
            font.setPointSize(8)
            textItem.setFont(font)
            textItem.document().setDocumentMargin(0)
            text_offset_x = textItem.boundingRect().width()
            text_offset_y = textItem.boundingRect().height()
            if i == 0:
                textItem.setPos(0, -scale_line_height - text_offset_y)
            else:
                textItem.setPos(0 - text_offset_x / 2 + i * spacing_px, -scale_line_height - text_offset_y)
            textItem.setZValue(1000)
            self.scanViewer.scanScene.addItem(textItem)

        scale_background = 255 * np.ones(((scale_line_height + text_offset_y).__int__(),
                                          (self.scanManager.imgScan.shape[1] * self.scanViewer.view_scale).__int__(), 3),
                                         dtype=np.uint8)
        scale_background_image = QtGui.QImage(scale_background, scale_background.shape[1], scale_background.shape[0],
                                              scale_background.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.scanViewer.addImage(scale_background_image, 0, -scale_line_height - text_offset_y, 900)

        textItem = QtGui.QGraphicsTextItem()
        textItem.setHtml("<div style='background-color: #ffffff;'>" + "[m]" + "</div>")
        font = QtGui.QFont()
        font.setPointSize(8)
        textItem.setFont(font)
        textItem.document().setDocumentMargin(0)
        text_offset_x = self.scanViewer.width() - textItem.boundingRect().width() - self.scanViewer.verticalScrollBar().width() - 15
        text_offset_y = textItem.boundingRect().height()
        textItem.setPos(text_offset_x, -scale_line_height - text_offset_y)
        textItem.setZValue(1000)
        self.scanViewer.scanScene.addItem(textItem)
        return text_offset_y + scale_line_height


    def openOptions(self):
        self.optionsDialog.show()


    def keyPressEvent(self, QKeyEvent):
        if (QKeyEvent.key() == QtCore.Qt.Key_Control and self.mouseMode == 0):
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self.mouseMode = 1
        elif (QKeyEvent.key() == QtCore.Qt.Key_Control and self.mouseMode == 1):
            self.scanViewer.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.mouseMode = 0








def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()