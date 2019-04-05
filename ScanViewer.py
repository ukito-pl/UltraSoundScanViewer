from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication
import numpy as np
from PyQt4 import QtCore




class ScanViewer(QtGui.QGraphicsView):
    def __init__(self,centralWidget):
        super(self.__class__, self).__init__(centralWidget)
        self.setMouseTracking(True)
        self.scanPixItem = QtGui.QGraphicsPixmapItem()
        self.scanScene = QtGui.QGraphicsScene()
        self.aspect_ratio = 1 #y/x
        self.view_scale = 1
        self.zoom_in_factor = 1.25
        self.zoom_out_factor = 0.8
        self.pos = []
        self.lockPos = []
        self.sceneItems = []
        self.scanScene.addItem(self.scanPixItem)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.prevoiusMouseDragMode = -1

    def mousePressEvent(self, QMouseEvent):

        if QMouseEvent.button() == QtCore.Qt.RightButton or QMouseEvent.button() == QtCore.Qt.MidButton:
            self.prevoiusMouseDragMode = self.dragMode()
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.emit(SIGNAL('tempDragModeActivated()'))
            qm = QtGui.QMouseEvent(QMouseEvent.type(),QMouseEvent.pos(), QMouseEvent.globalPos(), QtCore.Qt.LeftButton,
                                   QtCore.Qt.LeftButton,QMouseEvent.modifiers())
            super(self.__class__, self).mousePressEvent(qm)
        else:
            super(self.__class__, self).mousePressEvent(QMouseEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        if (self.dragMode() == QtGui.QGraphicsView.RubberBandDrag and self.scene() != 0):
            super(self.__class__, self).mouseReleaseEvent(QMouseEvent)
            rect =self.scene().selectionArea().controlPointRect()
            x = (rect.x()/self.view_scale).__int__()
            y = (rect.y() / (self.view_scale*self.aspect_ratio)).__int__()
            w = (rect.width() / self.view_scale).__int__()
            h = (rect.height() / (self.view_scale*self.aspect_ratio)).__int__()
            self.emit(SIGNAL('areaSelected(PyQt_PyObject)'),[x,y,w,h])
        elif (QMouseEvent.button() == QtCore.Qt.RightButton or QMouseEvent.button() == QtCore.Qt.MidButton):
            qm = QtGui.QMouseEvent(QMouseEvent.type(), QMouseEvent.pos(),QMouseEvent.globalPos(), QtCore.Qt.LeftButton,
                                   QtCore.Qt.NoButton, QMouseEvent.modifiers())
            super(self.__class__, self).mouseReleaseEvent(qm)
            self.setDragMode(self.prevoiusMouseDragMode)
            self.emit(SIGNAL('tempDragModeDeactivated()'))
        else:
            super(self.__class__, self).mouseReleaseEvent(QMouseEvent)

    def mouseMoveEvent(self, QMouseEvent):
        super(self.__class__, self).mouseMoveEvent(QMouseEvent)
        self.emit(SIGNAL('mousePositionChanged(PyQt_PyObject)'), QMouseEvent)

    def wheelEvent(self, QWheelEvent):
        super(self.__class__, self).wheelEvent(QWheelEvent)
        pos = self.mapToScene(QWheelEvent.x(), QWheelEvent.y())
        if QWheelEvent.delta() > 0:
            self.view_scale = self.view_scale * self.zoom_in_factor
            pos = pos * self.zoom_in_factor
        else:
            self.view_scale = self.view_scale * self.zoom_out_factor
            pos = pos * self.zoom_out_factor
        self.clearScene()
        self.scanPixItem.setScale(self.view_scale)
        self.emit(SIGNAL('changeScale()'))
        self.setScene(self.scanScene)
        self.centerOn(pos)
        self.moveScaleBar()

    def scrollContentsBy(self, p_int, p_int_1):
        super(self.__class__,self).scrollContentsBy(p_int, p_int_1)
        self.moveScaleBar()


    def setScanImage(self, scan_image):
        scanPixMap = QtGui.QPixmap(scan_image)
        scanPixMap = scanPixMap.scaled(scanPixMap.width(), int(scanPixMap.height() * self.aspect_ratio))
        self.scanPixItem.setPixmap(scanPixMap)
        self.scanPixItem.setScale(self.view_scale)
        self.setScene(self.scanScene)



    def goTo(self,px):
        page_step = self.horizontalScrollBar().pageStep()
        max = self.horizontalScrollBar().maximum() + page_step
        min = self.horizontalScrollBar().minimum()
        scroll_bar_range = max - min
        val = px * scroll_bar_range - (page_step / 2).__int__()
        self.horizontalScrollBar().setValue(val)


    def addItem(self,qgraphicsitem, lockX, lockY):
        self.scanScene.addItem(qgraphicsitem)
        self.pos.append([qgraphicsitem.x(), qgraphicsitem.y()])
        self.lockPos.append([lockX,lockY])
        self.sceneItems.append(qgraphicsitem)


    def clearScene(self):
        #deletes all items in the scanScene except scanPixItem and creates new scanScene with scanPixItem added
        self.scanScene.removeItem(self.scanPixItem)  # remove item from the scene
        self.scanScene.clear()
        self.sceneItems = []
        self.pos = []
        self.lockPos = []
        self.scanScene = QtGui.QGraphicsScene()
        self.scanScene.addItem(self.scanPixItem)

    def moveScaleBar(self):
        #moves the scale bar so it will always be on top of the graphicView
        vertical_offset = 0
        if self.verticalScrollBar().isVisible():
            page_step = self.verticalScrollBar().pageStep()
            max = self.verticalScrollBar().maximum() + page_step
            min = self.verticalScrollBar().minimum()
            scroll_bar_range = max - min
            val = self.verticalScrollBar().value()
            offset_ratio = (val - min)/float(scroll_bar_range)
            vertical_offset = self.scanScene.height() * offset_ratio
        horizontal_offset = 0
        if self.horizontalScrollBar().isVisible():
            page_step = self.horizontalScrollBar().pageStep()
            max = self.horizontalScrollBar().maximum() + page_step
            min = self.horizontalScrollBar().minimum()
            scroll_bar_range = max - min
            val = self.horizontalScrollBar().value()
            offset_ratio = (val - min) / float(scroll_bar_range)
            horizontal_offset = self.scanScene.width() * offset_ratio

        self.scanScene.removeItem(self.scanPixItem)
        for i in range(0,len(self.sceneItems)):
            if self.lockPos[i][1] == True:
                self.sceneItems[i].setY(self.pos[i][1] + vertical_offset)
            if self.lockPos[i][0] == True:
                self.sceneItems[i].setX(self.pos[i][0] + horizontal_offset)

        self.scanPixItem.setZValue(1)
        self.scanScene.addItem(self.scanPixItem)
        self.scanScene.update()
        self.update()

    def resetViewScale(self):
        self.view_scale = 1
        self.scanPixItem.setScale(self.view_scale)