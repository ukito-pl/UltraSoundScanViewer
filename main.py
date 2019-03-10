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
from ColorMapping import ColorMapping

class MainApp(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.view_scale = 1
        self.zoom_in_factor = 1.25
        self.zoom_out_factor = 0.8
        self.mouseMode = 0      #0-przesuwanie, 1 -zaznaczanie
        self.graphicsView.scale(1, 1)
        self.pos = np.zeros((10000,2))
        self.scale_spacing = 0.1 # in meters
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
        #self.connect(self.graphicsView, SIGNAL('contentScrolled()'), self.moveScaleBar)

        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView.verticalScrollBar().valueChanged.connect(self.moveScaleBar)
        #self.graphicsView.horizontalScrollBar().valueChanged.connect(self.moveScaleBar)

        self.scanPixItem = QtGui.QGraphicsPixmapItem()
        self.scene = QtGui.QGraphicsScene()
        self.scene.addItem(self.scanPixItem)
        self.graphicsView.setScene(self.scene)

        self.verticalSlider.valueChanged.connect(self.rearrangeScan)

        self.colorMapping = ColorMapping()


    def rearrangeScan(self):
        val = float(self.verticalSlider.value())
        min = float(self.verticalSlider.minimum())
        max = float(self.verticalSlider.maximum())
        val_ratio = float(val/(max - min))
        rows = self.imgScan.shape[0]
        first_row = int(rows*val_ratio)

        rearranged_array = np.zeros(self.imgScan.shape, dtype=np.uint8)
        rearranged_array[0:first_row,:,:] = self.imgScan[rows-first_row:rows,:,:]
        rearranged_array[first_row:rows,:,:] = self.imgScan[0:rows-first_row,:,:]
        colored_scan = self.colorScan(rearranged_array)

        image = QtGui.QImage(colored_scan, colored_scan.shape[1], colored_scan.shape[0], colored_scan.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)

        scanPixMap = QtGui.QPixmap(image)

        self.scanPixItem.setPixmap(scanPixMap)


    def goToCurrentFrame(self):

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
            position = position/self.view_scale
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

    def colorLegend(self,scale_name):
        legend_array =  np.zeros((256,20,3),dtype=np.uint8)
        for i in range(1,legend_array.shape[0] - 1):
            legend_array[i,1:19 , :] = self.colorMapping.lookUpTables["ironfire"][-i-1]

        image = QtGui.QImage(legend_array, legend_array.shape[1], legend_array.shape[0], legend_array.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        legendPixMap = QtGui.QPixmap(image)
        legendPixMapItem = QtGui.QGraphicsPixmapItem(legendPixMap)
        scene = QtGui.QGraphicsScene()
        scene.addItem(legendPixMapItem)
        self.graphicsView_2.setScene(scene)
        self.graphicsView_2.fitInView(scene.sceneRect())



    def colorScan(self, scan):
        colored_scan = np.zeros(scan.shape, dtype=np.uint8)
        self.colorMapping.addScale("ironfire")
        self.colorMapping.setColorAt("ironfire", 0, QtGui.QColor(0, 0, 0))
        self.colorMapping.setColorAt("ironfire",255,QtGui.QColor(255,255,255))
        self.colorMapping.setColorAt("ironfire", 65, QtGui.QColor(0, 0, 255))
        self.colorMapping.setColorAt("ironfire", 60, QtGui.QColor(100, 0, 255))
        for i in range(0,self.imgScan.shape[0]):
            colored_scan[i,: , :] = self.colorMapping.lookUpTables["ironfire"][scan[i,:,0]]
        #print self.colorMapping.lookUpTables["ironfire"]


        return colored_scan

    def showImage(self, imag):
        self.scene = QtGui.QGraphicsScene()

        self.imgScan = np.array(imag)
        colored_scan = self.colorScan(self.imgScan)
        #print self.imgScan, self.imgScan.shape
        image = QtGui.QImage(colored_scan, colored_scan.shape[1], colored_scan.shape[0], colored_scan.shape[1] * 3, QtGui.QImage.Format_RGB888)


        scanPixMap = QtGui.QPixmap(image)

        self.scanPixItem.setPixmap(scanPixMap)
        self.scanPixItem.scale(1,1)
        self.scene.addItem(self.scanPixItem)

        scale_height = self.addScaleBarToImage(self.scale_spacing, 7)
        self.scene.update()
        self.graphicsView.setScene(self.scene)
        self.scanLoaded = True

        hor_bar_height = self.graphicsView.horizontalScrollBar().height()
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 256+scale_height+ hor_bar_height/2 ))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 256+scale_height + hor_bar_height/2 ))
        self.graphicsView_2.setMaximumHeight(self.graphicsView.height())
        self.verticalSlider.setMaximumHeight(self.graphicsView.height())
        print self.graphicsView.height()

        page_step = self.graphicsView.horizontalScrollBar().pageStep()
        max = self.graphicsView.horizontalScrollBar().maximum() + page_step
        min = self.graphicsView.horizontalScrollBar().minimum()
        frame_range = (self.endFrame - self.startFrame).__float__()
        scroll_bar_range = max - min
        val = ((self.currentFrame - self.startFrame) / frame_range) * scroll_bar_range - (page_step/2).__int__()
        self.graphicsView.horizontalScrollBar().setValue(val)

        self.moveScaleBar()

        self.colorLegend("ironfire")

    def addScaleBarToImage(self,spacing, scale_line_height):
        #spacing - in meters
        #scale_line_height - in pixels
        self.pos = np.zeros((10000,2))
        spacing_px_org = spacing /self.optionsDialog.DeltaX * 1000 #because deltaX is in mm
        spacing_px = float(spacing_px_org * self.view_scale)
        scaleLineImg = 0 * np.ones((scale_line_height, (self.imgScan.shape[1]*self.view_scale).__int__(), 3), dtype=np.uint8)
        #print spacing_px
        for i in range(((self.imgScan.shape[1]*self.view_scale)//spacing_px).__int__()):
            left_bound = (i * spacing_px).__int__()
            right_bound = (i * spacing_px + spacing_px).__int__()
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

        for i in range(((self.imgScan.shape[1]*self.view_scale)//spacing_px).__int__()):
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

        textItem = QtGui.QGraphicsTextItem()
        textItem.setHtml("<div style='background-color: #ffffff;'>" + "[m]" + "</div>")
        font = QtGui.QFont()
        font.setPointSize(8)
        textItem.setFont(font)
        textItem.document().setDocumentMargin(0)
        text_offset_x = self.graphicsView.width() -  textItem.boundingRect().width() - self.graphicsView.verticalScrollBar().width() -15
        text_offset_y = textItem.boundingRect().height()
        textItem.setPos(text_offset_x, -scale_line_height - text_offset_y)
        textItem.setZValue(1000)
        #self.scene.addItem(textItem)

        return text_offset_y + scale_line_height
    def vert_test(self):
        print "vertical scroolbar called"

    def horz_test(self):
        print "horizontal scroolbar called"

    def moveScaleBar(self):
        #moves the scale bar so it will always be on top of the graphicView
        vertical_offset = 0
        if self.graphicsView.verticalScrollBar().isVisible():
            page_step = self.graphicsView.verticalScrollBar().pageStep()
            max = self.graphicsView.verticalScrollBar().maximum() + page_step
            min = self.graphicsView.verticalScrollBar().minimum()
            scroll_bar_range = max - min
            val = self.graphicsView.verticalScrollBar().value()
            offset_ratio = (val - min)/float(scroll_bar_range)
            vertical_offset = self.scene.height() * offset_ratio

        horizontal_offset = 0
        if self.graphicsView.verticalScrollBar().isVisible():
            page_step = self.graphicsView.horizontalScrollBar().pageStep()
            max = self.graphicsView.horizontalScrollBar().maximum() + page_step
            min = self.graphicsView.horizontalScrollBar().minimum()
            scroll_bar_range = max - min
            val = self.graphicsView.horizontalScrollBar().value()
            offset_ratio = (val - min) / float(scroll_bar_range)
            horizontal_offset = self.scene.width() * offset_ratio

        self.scene.removeItem(self.scanPixItem) #remove item from the scene
        scene_items = self.scene.items()
        for i in range(0,len(scene_items)):
            if self.pos[i,1] == 0:
                self.pos[i,1] = scene_items[i].y()
                self.pos[i, 0] = scene_items[i].x()
            scene_items[i].setY(self.pos[i,1] + vertical_offset)
            if isinstance(scene_items[i],QtGui.QGraphicsTextItem):
                text = scene_items[i].toPlainText()
                if text == "[m]":
                    scene_items[i].setX(self.pos[i, 0] + horizontal_offset)
        self.scanPixItem.setZValue(1)
        self.scene.addItem(self.scanPixItem)
        self.scene.update()
        self.graphicsView.update()


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
        spacing_px_org = self.scale_spacing / self.optionsDialog.DeltaX * 1000
        spacing_px = float(spacing_px_org * self.view_scale)
        if spacing_px > 130:
            self.scale_spacing = self.scale_spacing / 2
        elif spacing_px < 40:
            self.scale_spacing = self.scale_spacing * 2
        print self.scale_spacing


        #print "poz: ", pos
        self.scene.removeItem(self.scanPixItem) #remove item from the scene
        self.scene.clear()                      #delete all items in the scene
        self.scene = QtGui.QGraphicsScene()
        self.scanPixItem.setScale(self.view_scale)
        self.scene.addItem(self.scanPixItem)
        #print "scan pixel width: ", self.scanPixItem.sceneBoundingRect().width()
        self.addScaleBarToImage(self.scale_spacing,7)
        self.graphicsView.setScene(self.scene)

        self.graphicsView.centerOn(pos)
        self.moveScaleBar()
        self.scene.update()
        self.graphicsView.update()


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