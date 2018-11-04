# -*- coding: utf-8 -*-

from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication
import numpy as np
from LoadFileThread import LoadFileThread
from PyQt4 import QtCore


import MainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from options import OptionsDialog

class MainApp(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._zoom = 0
        self.graphicsView.scale(2, 2)
        self.graphicsView_2.scale(2, 10)
        self.graphicsView_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dialog = OptionsDialog()

        self.connect(self.pushButton_options, SIGNAL('clicked()'), self.openOptions)
        self.connect(self.pushButton_scans, SIGNAL('clicked()'), self.showScans)

        horbar = self.graphicsView.horizontalScrollBar()
        horbar.valueChanged.connect(self.scrollLegend)



    def scrollLegend(self):
        val = self.graphicsView.horizontalScrollBar().value()
        self.graphicsView_2.horizontalScrollBar().setValue(val)

    def showScans(self):
        text = unicode(self.dialog.dataDir)
        print text
        self.loadFileThread = LoadFileThread(text);
        self.connect(self.loadFileThread, SIGNAL('showImage(PyQt_PyObject)'), self.showImage)
        self.loadFileThread.start()

        self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)



    def showImage(self, imag):
        img = np.array(imag)
        print img, img.shape
        image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_RGB888)

        scene = QtGui.QGraphicsScene()
        pix1 = QtGui.QPixmap(image)
        pixItem1 = QtGui.QGraphicsPixmapItem()
        pixItem1.setPixmap(pix1)
        #pixItem1.setPos(0,11)
        scene.addItem(pixItem1)

        scaleLineImg = 255 * np.ones((1,img.shape[1],3),dtype=np.uint8)

        for i in  range(img.shape[1].__floordiv__(100)):
            if i.__mod__(2)==1:
                scaleLineImg[0,i*100:i*100+100] = 50* np.ones((1,100,3))
                print "1"
            else:
                scaleLineImg[0, i * 100:i * 100 + 100] = 180* np.ones((1, 100, 3))
                print "0"
        print scaleLineImg, scaleLineImg.shape
        scaleLineImage = QtGui.QImage(scaleLineImg, scaleLineImg.shape[1], scaleLineImg.shape[0], scaleLineImg.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix2 = QtGui.QPixmap(scaleLineImage)
        pixItem2 = QtGui.QGraphicsPixmapItem()
        pixItem2.setPixmap(pix2)
        #pixItem2.setPos(0, -10)

        scene2 = QtGui.QGraphicsScene()

        scene2.addItem(pixItem2)
        #text = QtGui.QGraphicsItem()
        #text = scene2.addText("100")
        #text.setPos(20,20)

        self.graphicsView.setScene(scene)
        self.graphicsView_2.setScene(scene2)



    def openOptions(self):

        self.dialog.show()

    def wheelEvent(self, event):

        if event.delta() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1

        self.graphicsView.scale(factor, 1)
        self.graphicsView_2.scale(factor, 1)

    def keyPressEvent(self, QKeyEvent):
        if (QKeyEvent.key() == QtCore.Qt.Key_Control):
            self.graphicsView.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Control:
            self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()