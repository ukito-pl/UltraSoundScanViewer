# -*- coding: utf-8 -*-

from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication
import numpy as np
from LoadScansThread import LoadScansThread
from PyQt4 import QtCore


import MainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from options import OptionsDialog
from selection import SelectionDialog

class MainApp(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._zoom = 0
        self.mouseMode = 0      #0-przesuwanie, 1 -zaznaczanie
        self.graphicsView.scale(1, 1)
        self.graphicsView_2.scale(2, 6)
        self.graphicsView_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imgScan = 0
        self.startFrame = 0
        self.endFrame = 0
        self.currentFrame = 0
        self.scanLoaded = False
        self.optionsDialog = OptionsDialog()
        self.selectionDialog = SelectionDialog()

        self.connect(self.pushButton_options, SIGNAL('clicked()'), self.openOptions)
        self.connect(self.pushButton_scans, SIGNAL('clicked()'), self.showScans)
        self.connect(self.pushButton_go, SIGNAL('clicked()'), self.goToCurrentFrame)

        horbar = self.graphicsView.horizontalScrollBar()
        horbar.valueChanged.connect(self.scrollLegend)

        self.connect(self.graphicsView, SIGNAL('mousePositionChanged(PyQt_PyObject)'), self.mousePositionChanged)
        self.connect(self.graphicsView, SIGNAL('mouseButtonReleased()'), self.mouseButtonReleased)

        self.scanPixItem = QtGui.QGraphicsPixmapItem()
        self.scene = QtGui.QGraphicsScene()
        self.scene.addItem(self.scanPixItem)
        self.graphicsView.setScene(self.scene)


    def goToCurrentFrame(self):
        self.currentFrame = ((float(self.textEdit_km.toPlainText())*1000)/self.optionsDialog.DeltaX).__int__()
        print self.currentFrame, self.startFrame,self.endFrame
        if (self.startFrame <= self.currentFrame and self.currentFrame <= self.endFrame):
            max = self.graphicsView.horizontalScrollBar().maximum() + self.graphicsView.horizontalScrollBar().pageStep()
            min = self.graphicsView.horizontalScrollBar().minimum()
            frame_range = (self.endFrame - self.startFrame).__float__()
            scroll_bar_range = max - min
            val = ((self.currentFrame - self.startFrame)/frame_range)*scroll_bar_range
            self.graphicsView.horizontalScrollBar().setValue(val)
        else:
            #load new scans
            self.startFrame = (self.currentFrame - 5000).__int__()
            self.textEdit_kmFrom.setText((self.startFrame/1000).__str__())
            self.endFrame = (self.currentFrame + 5000).__int__()
            self.textEdit_kmTo.setText((self.endFrame/1000).__str__())
            text = unicode(self.optionsDialog.dataDir)
            self.loadScansThread = LoadScansThread(text, self.startFrame, self.endFrame)
            self.connect(self.loadScansThread, SIGNAL('showImage(PyQt_PyObject)'), self.showImage)
            self.loadScansThread.start()

    def mouseButtonReleased(self):
        if (self.mouseMode == 1 and self.graphicsView.scene() != 0):
            rect =self.graphicsView.scene().selectionArea().controlPointRect()
            x = rect.x().__int__()
            y = rect.y().__int__()
            w = rect.width().__int__()
            h = rect.height().__int__()
            print rect,x,y,w,h
            self.selectionDialog.show()
            self.selectionDialog.showImage(self.imgScan[y:y+h, x:x+w, :])
            self.selectionDialog.activateWindow()

    def mousePositionChanged(self, pos):
        if self.scanLoaded:
            position = self.graphicsView.mapToScene(pos.x(),pos.y())
            x = ((position.x() + self.startFrame)*self.optionsDialog.DeltaX)/1000 #in meters
            deltaY = 3.14 * self.optionsDialog.Diameter / 256.0
            y = position.y()*deltaY

            indx = position.x()
            if indx < 0:
                indx = 0
            elif indx > (self.imgScan.shape[1] - 1):
                indx = self.imgScan.shape[1] - 1
            indy = position.y()
            if indy < 0:
                indy = 0
            elif indy > (self.imgScan.shape[0] - 1):
                indy = self.imgScan.shape[0] - 1
            C = self.optionsDialog.CoefficientC
            D = self.optionsDialog.CoefficientD
            depth = C * self.imgScan[int(indy),int(indx),0] + D
            self.statusbar.showMessage('X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:.3F}".format(y) + ' mm  Grubosc: ' + "{:.3F}".format(depth) + ' mm')


    def scrollLegend(self):
        val = self.graphicsView.horizontalScrollBar().value()
        self.graphicsView_2.horizontalScrollBar().setValue(val)

    def showScans(self):
        deltaY = 3.14 * self.optionsDialog.Diameter / 256.0
        text = unicode(self.optionsDialog.dataDir)
        self.startFrame = ((float(self.textEdit_kmFrom.toPlainText())*1000) / self.optionsDialog.DeltaX).__int__()
        self.currentFrame = self.startFrame
        self.textEdit_km.setText((self.currentFrame/ 1000.0).__str__())
        self.endFrame = ((float(self.textEdit_kmTo.toPlainText()) * 1000) / self.optionsDialog.DeltaX).__int__()
        print text, self.textEdit_km.toPlainText(), self.startFrame, self.endFrame
        self.loadScansThread = LoadScansThread(text, self.startFrame, self.endFrame)
        self.connect(self.loadScansThread, SIGNAL('showImage(PyQt_PyObject)'), self.showImage)
        self.loadScansThread.start()

        self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)



    def showImage(self, imag):


        self.scene = QtGui.QGraphicsScene()

        self.imgScan = np.array(imag)
        #print self.imgScan, self.imgScan.shape
        image = QtGui.QImage(self.imgScan, self.imgScan.shape[1], self.imgScan.shape[0], self.imgScan.shape[1] * 3, QtGui.QImage.Format_RGB888)


        scanPixMap = QtGui.QPixmap(image)

        self.scanPixItem.setPixmap(scanPixMap)
        self.scanPixItem.scale(1,1)
        self.scene.addItem(self.scanPixItem)

        scale_height = self.addScaleBarToImage(200, 7)
        self.scene.update()
        self.graphicsView.setScene(self.scene)
        self.scanLoaded = True
        self.goToCurrentFrame()

        hor_bar_height =  self.graphicsView.horizontalScrollBar().height()
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 256+scale_height+ hor_bar_height/2 ))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 256+scale_height + hor_bar_height/2 ))

    def addScaleBarToImage(self,spacing, scale_line_height):
        scaleLineImg = 0 * np.ones((scale_line_height, self.imgScan.shape[1], 3), dtype=np.uint8)

        for i in range(self.imgScan.shape[1].__floordiv__(spacing)):
            if i.__mod__(2) == 1:
                scaleLineImg[1:scale_line_height - 1, i * spacing:i * spacing + spacing] = 50 * np.ones((1, spacing, 3))
            else:
                scaleLineImg[1:scale_line_height - 1, i * spacing:i * spacing + spacing] = 255 * np.ones((1, spacing, 3))

        print scaleLineImg, scaleLineImg.shape
        scaleLineImage = QtGui.QImage(scaleLineImg, scaleLineImg.shape[1], scaleLineImg.shape[0],
                                      scaleLineImg.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix2 = QtGui.QPixmap(scaleLineImage)
        pixItem2 = QtGui.QGraphicsPixmapItem()
        pixItem2.setPixmap(pix2)
        pixItem2.setOffset(0, -scale_line_height)
        self.scene.addItem(pixItem2)

        for i in range(self.imgScan.shape[1].__floordiv__(spacing)):
            x = ((i * spacing + self.startFrame) * self.optionsDialog.DeltaX) / 1000  # in meters

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
                textItem.setPos(0 - text_offset_x / 2 + i * spacing, -scale_line_height - text_offset_y)
            # print textItem.boundingRect()
            self.scene.addItem(textItem)
        return text_offset_y + scale_line_height

    def openOptions(self):

        self.optionsDialog.show()

    def wheelEvent(self, event):

        if event.delta() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1

        self.scene.removeItem(self.scanPixItem) #remove item from the scene
        self.scene.clear()                      #delete all items in the scene
        self.scene = QtGui.QGraphicsScene()
        self.scanPixItem.scale(factor,factor)
        self.scene.addItem(self.scanPixItem)
        self.addScaleBarToImage(200,7)
        self.graphicsView.setScene(self.scene)
        #self.graphicsView.scale(factor, 1)

    def keyPressEvent(self, QKeyEvent):
        if (QKeyEvent.key() == QtCore.Qt.Key_Control and self.mouseMode == 0):
            self.graphicsView.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self.mouseMode = 1
        elif (QKeyEvent.key() == QtCore.Qt.Key_Control and self.mouseMode == 1):
            self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.mouseMode = 0








def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()