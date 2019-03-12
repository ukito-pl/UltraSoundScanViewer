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
        self.scanScene.addItem(self.scanPixItem)
        self.setScene(self.scanScene)
        self.view_scale = 1
        self.zoom_in_factor = 1.25
        self.zoom_out_factor = 0.8
        self.pos = np.zeros((10000, 2))

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    def mouseReleaseEvent(self, QMouseEvent):
        super(self.__class__, self). mouseReleaseEvent(QMouseEvent)
        self.emit(SIGNAL('mouseButtonReleased()'))

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


        self.scanScene.removeItem(self.scanPixItem)  # remove item from the scene
        self.scanScene.clear()  # delete all items in the scene
        self.scanScene = QtGui.QGraphicsScene()
        self.scanPixItem.setScale(self.view_scale)
        self.scanScene.addItem(self.scanPixItem)

        self.emit(SIGNAL('changeScale()'))

        self.setScene(self.scanScene)

        self.centerOn(pos)
        self.moveScaleBar()
        self.scanScene.update()
        self.update()

    def scrollContentsBy(self, p_int, p_int_1):
        super(self.__class__,self).scrollContentsBy(p_int, p_int_1)
        self.moveScaleBar()

    def setScanImage(self, scan_image):
        scanPixMap = QtGui.QPixmap(scan_image)
        self.scanPixItem.setPixmap(scanPixMap)
        self.scanPixItem.scale(1, 1)
        self.scanScene.update()
        self.setScene(self.scanScene)
        self.update()


    def goTo(self,px):
        page_step = self.horizontalScrollBar().pageStep()
        max = self.horizontalScrollBar().maximum() + page_step
        min = self.horizontalScrollBar().minimum()
        scroll_bar_range = max - min
        val = px * scroll_bar_range - (page_step / 2).__int__()
        self.horizontalScrollBar().setValue(val)

    def addImage(self,image,pos_x, pos_y, z):
        pix = QtGui.QPixmap(image)
        pixItem = QtGui.QGraphicsPixmapItem()
        pixItem.setPixmap(pix)
        pixItem.setPos(pos_x, pos_y)
        pixItem.setZValue(z)
        self.scanScene.addItem(pixItem)

    def clearScene(self):
        self.scanScene.removeItem(self.scanPixItem)  # remove item from the scene
        self.scanScene.clear()
        self.scanScene.addItem((self.scanPixItem))

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

        self.scanScene.removeItem(self.scanPixItem) #remove item from the scene
        scene_items = self.scanScene.items()
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
        self.scanScene.addItem(self.scanPixItem)
        self.scanScene.update()
        self.update()