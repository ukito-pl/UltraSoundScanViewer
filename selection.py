from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL

import numpy as np

import SelectionWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer

class SelectionDialog(QtGui.QDialog, SelectionWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.graphicsView.scale(2,2)
        self.pixItem1 = QtGui.QGraphicsPixmapItem()
        self.connect(self.pushButton,SIGNAL("clicked()"),self.evaluateClicked)
        self.data_rect = 0

    def evaluateClicked(self):
        self.emit(SIGNAL("evaluateMAOP(PyQt_PyObject)"),self.data_rect)

    def showImage(self,rect,img_to_show, aspect_ratio ):
        self.data_rect = rect
        img = np.array(img_to_show)
        #print img, img.shape
        image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        scene = QtGui.QGraphicsScene()
        pix1 = QtGui.QPixmap(image)
        pix1 = pix1.scaled(pix1.width(), int(pix1.height() * aspect_ratio))
        self.pixItem1.setPixmap(pix1)
        scene.addItem(self.pixItem1)
        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(self.pixItem1, QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, QResizeEvent):
        super(self.__class__,self).resizeEvent(QResizeEvent)
        self.graphicsView.fitInView(self.pixItem1,QtCore.Qt.KeepAspectRatio)