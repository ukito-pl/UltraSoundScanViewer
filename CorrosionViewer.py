from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication
import numpy as np
from PyQt4 import QtCore




class CorrosionViewer(QtGui.QGraphicsView):
    def __init__(self,centralWidget):
        super(self.__class__, self).__init__(centralWidget)
        self.setMouseTracking(True)

    def mousePressEvent(self, QMouseEvent):
        super(self.__class__, self).mouseMoveEvent(QMouseEvent)
        self.emit(SIGNAL('mouseClicked(PyQt_PyObject)'), QMouseEvent)