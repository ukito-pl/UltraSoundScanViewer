from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication
import numpy as np





class MyGraphicsView(QtGui.QGraphicsView):
    def __init__(self,centralWidget):
        super(self.__class__, self).__init__(centralWidget)
        self.setMouseTracking(True)

    def mouseReleaseEvent(self, QMouseEvent):
        super(self.__class__, self). mouseReleaseEvent(QMouseEvent)
        self.emit(SIGNAL('mouseButtonReleased()'))

    def mouseMoveEvent(self, QMouseEvent):
        super(self.__class__, self).mouseMoveEvent(QMouseEvent)
        self.emit(SIGNAL('mousePositionChanged(PyQt_PyObject)'), QMouseEvent.pos())

    def wheelEvent(self, QWheelEvent):
        super(self.__class__, self).wheelEvent(QWheelEvent)
        self.emit(SIGNAL('wheelEvent(PyQt_PyObject)'), QWheelEvent)