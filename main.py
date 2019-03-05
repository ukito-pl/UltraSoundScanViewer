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
        self.view_scale = 1
        self.zoom_in_factor = 1.25
        self.zoom_out_factor = 0.8
        self.mouseMode = 0      #0-przesuwanie, 1 -zaznaczanie
        self.graphicsView.scale(1, 1)
        self.y = np.zeros(10000)

        self.imgScan = 0
        self.startFrame = 0
        self.endFrame = 0
        self.currentFrame = 0
        self.scanLoaded = False
        self.optionsDialog = OptionsDialog()
        self.selectionDialog = SelectionDialog()

        self.connect(self.pushButton_options, SIGNAL('clicked()'), self.openOptions)
        self.connect(self.pushButton_go, SIGNAL('clicked()'), self.goToCurrentFrame)


        self.connect(self.graphicsView, SIGNAL('mousePositionChanged(PyQt_PyObject)'), self.mousePositionChanged)
        self.connect(self.graphicsView, SIGNAL('mouseButtonReleased()'), self.mouseButtonReleased)
        self.connect(self.graphicsView, SIGNAL('wheelEvent(PyQt_PyObject)'), self.zoom)

        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView.verticalScrollBar().valueChanged.connect(self.moveScaleBar)

        self.scanPixItem = QtGui.QGraphicsPixmapItem()
        self.scene = QtGui.QGraphicsScene()
        self.scene.addItem(self.scanPixItem)
        self.graphicsView.setScene(self.scene)


    def goToCurrentFrame(self):
        self.y = np.zeros(10000)
        self.currentFrame = ((float(self.textEdit_km.toPlainText())*1000)/self.optionsDialog.DeltaX).__int__()
        self.startFrame = (self.currentFrame - 5000).__int__()
        if self.startFrame < 0:
            self.startFrame = 0;
        self.endFrame = (self.currentFrame + 5000).__int__()
        text = unicode(self.optionsDialog.dataDir)
        self.loadScansThread = LoadScansThread(text, self.startFrame, self.endFrame)
        self.connect(self.loadScansThread, SIGNAL('showImage(PyQt_PyObject)'), self.showImage)
        self.loadScansThread.start()

        self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)


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
            #position = position/self.view_scale
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
            self.statusbar.showMessage('X: ' + "{:.3F}".format(position.x()) +" m" + ', Y: ' + "{:.3F}".format(position.y()) + ' mm  Grubosc: ' + "{:.3F}".format(depth) + ' mm')


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

        hor_bar_height = self.graphicsView.horizontalScrollBar().height()
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 256+scale_height+ hor_bar_height/2 ))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 256+scale_height + hor_bar_height/2 ))

        page_step = self.graphicsView.horizontalScrollBar().pageStep()
        max = self.graphicsView.horizontalScrollBar().maximum() + page_step
        min = self.graphicsView.horizontalScrollBar().minimum()
        frame_range = (self.endFrame - self.startFrame).__float__()
        scroll_bar_range = max - min
        val = ((self.currentFrame - self.startFrame) / frame_range) * scroll_bar_range - (page_step/2).__int__()
        self.graphicsView.horizontalScrollBar().setValue(val)

        self.moveScaleBar()

    def addScaleBarToImage(self,spacing, scale_line_height):
        org_spacing = spacing
        spacing = (spacing * self.view_scale)
        scaleLineImg = 0 * np.ones((scale_line_height, (self.imgScan.shape[1]*self.view_scale).__int__(), 3), dtype=np.uint8)

        for i in range(((self.imgScan.shape[1]*self.view_scale).__floordiv__(spacing)).__int__()):
            left_bound = (i * spacing).__int__()
            right_bound = (i * spacing + spacing).__int__()
            if i.__mod__(2) == 1:
                scaleLineImg[1:scale_line_height - 1, left_bound:right_bound] = 50 * np.ones((1, right_bound - left_bound, 3))
            else:
                scaleLineImg[1:scale_line_height - 1, left_bound:right_bound] = 255 * np.ones((1, right_bound - left_bound, 3))

        scaleLineImage = QtGui.QImage(scaleLineImg, scaleLineImg.shape[1], scaleLineImg.shape[0],
                                      scaleLineImg.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix2 = QtGui.QPixmap(scaleLineImage)
        pixItem2 = QtGui.QGraphicsPixmapItem()
        pixItem2.setPixmap(pix2)
        pixItem2.setPos(0, -scale_line_height)
        pixItem2.setZValue(1000)
        self.scene.addItem(pixItem2)

        for i in range(((self.imgScan.shape[1]*self.view_scale).__floordiv__(spacing)).__int__()):
            x = ((i * org_spacing + self.startFrame) * self.optionsDialog.DeltaX) / 1000  # in meters

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
            textItem.setZValue(1000)
            self.scene.addItem(textItem)

        scale_background = 255 * np.ones(((scale_line_height+ text_offset_y).__int__(), (self.imgScan.shape[1] * self.view_scale).__int__(), 3), dtype=np.uint8)
        scale_background_image = QtGui.QImage(scale_background, scale_background.shape[1], scale_background.shape[0],
                                      scale_background.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix3 = QtGui.QPixmap(scale_background_image)
        pixItem3 = QtGui.QGraphicsPixmapItem()
        pixItem3.setPixmap(pix3)
        pixItem3.setPos(0, -scale_line_height - text_offset_y)
        pixItem3.setZValue(900)
        self.scene.addItem(pixItem3)

        return text_offset_y + scale_line_height

    def moveScaleBar(self):
        offset = 0
        if self.graphicsView.verticalScrollBar().isVisible():
            page_step = self.graphicsView.verticalScrollBar().pageStep()
            max = self.graphicsView.verticalScrollBar().maximum() + page_step
            min = self.graphicsView.verticalScrollBar().minimum()
            scroll_bar_range = max - min
            val = self.graphicsView.verticalScrollBar().value()
            offset_ratio = (val - min)/float(scroll_bar_range)
            offset = self.scene.height() * offset_ratio

        self.scene.removeItem(self.scanPixItem) #remove item from the scene
        scene_items = self.scene.items()
        for i in range(0,len(scene_items)):
            if self.y[i] == 0:
                self.y[i] = scene_items[i].y()
            scene_items[i].setY(self.y[i] + offset)
        self.scanPixItem.setZValue(1)
        self.scene.addItem(self.scanPixItem)




    def openOptions(self):
        self.optionsDialog.show()

    def zoom(self,event):
        pos = self.graphicsView.mapToScene(event.x(), event.y())
        if event.delta() > 0:
            self.view_scale = self.view_scale*self.zoom_in_factor
            pos = pos * self.zoom_in_factor
        else:
            self.view_scale = self.view_scale*self.zoom_out_factor
            pos = pos * self.zoom_out_factor

        print "poz: ", pos
        self.scene.removeItem(self.scanPixItem) #remove item from the scene
        self.scene.clear()                      #delete all items in the scene
        self.scene = QtGui.QGraphicsScene()
        self.scanPixItem.setScale(self.view_scale)
        self.scene.addItem(self.scanPixItem)
        print "scan pixel width: ", self.scanPixItem.sceneBoundingRect().width()
        self.addScaleBarToImage(200,7)
        self.graphicsView.setScene(self.scene)

        self.graphicsView.centerOn(pos)
        self.moveScaleBar()



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