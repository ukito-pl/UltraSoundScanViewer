# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL
import numpy as np

import ReferenceSelectionWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ReferenceSelectionDialog(QtGui.QDialog, ReferenceSelectionWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.data = -1
        self.t = -1
        self.pixItem = QtGui.QGraphicsPixmapItem()
        self.scene = QtGui.QGraphicsScene()
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.setReferenceThickness)

    def setData(self,data,data_colored,aspect_ratio):
        self.data = data
        img = np.array(data_colored)
        image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.scene = QtGui.QGraphicsScene()
        pix1 = QtGui.QPixmap(image)
        self.pixItem = QtGui.QGraphicsPixmapItem(pix1)
        self.pixItem.scale(1, aspect_ratio)
        self.scene.addItem(self.pixItem)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.fitInView(self.pixItem, QtCore.Qt.KeepAspectRatio)

    def evaluateThickness(self):
        t_sum = 0.0
        for row in self.data:
            for element in row:
                t_sum = t_sum + element
        number_of_elements = float(self.data.shape[0]* self.data.shape[1])
        t_avr = t_sum / number_of_elements
        self.t = t_avr
        self.label_t.setText("{:.3F}".format(self.t) + " mm")

    def setReferenceThickness(self):
        self.emit(SIGNAL('setNominalThickness(PyQt_PyObject)'),self.t)

    def resizeEvent(self, QResizeEvent):
        super(self.__class__,self).resizeEvent(QResizeEvent)
        self.graphicsView.fitInView(self.pixItem,QtCore.Qt.KeepAspectRatio)