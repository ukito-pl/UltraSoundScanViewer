from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL

import numpy as np
from PIL import Image
import SavePictureWindow

class SavePictureDialog(QtGui.QDialog, SavePictureWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pilImage = Image.Image()

        self.connect(self.pushButton_url, SIGNAL('clicked()'), self.getDir)

    def saveImg(self, PILImage):
        self.show()
        self.pilImage = PILImage
        array = np.array(PILImage)
        image = QtGui.QImage(array, array.shape[1], array.shape[0], array.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(image)
        pixitem = QtGui.QGraphicsPixmapItem(pixmap)
        scene = QtGui.QGraphicsScene()
        scene.addItem(pixitem)
        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(QtCore.QRectF(0, 0, PILImage.size[0], PILImage.size[1]), QtCore.Qt.KeepAspectRatio)

    def accept(self):
        super(self.__class__,self).accept()
        directory = self.lineEdit_url.text()
        self.pilImage.save(directory.__str__())
        print "saved"

    def resizeEvent(self, QResizeEvent):
        super(self.__class__,self).resizeEvent(QResizeEvent)
        self.graphicsView.fitInView(QtCore.QRectF(0, 0, self.pilImage.size[0], self.pilImage.size[1]), QtCore.Qt.KeepAspectRatio)

    def getDir(self):
        dir = QtGui.QFileDialog.getSaveFileNameAndFilter(filter = ".png;;.jpg")
        if dir:
            if ((".png" or ".jpg") not in dir[0].__str__()):
                self.lineEdit_url.setText(dir[0]+dir[1])
            else:
                self.lineEdit_url.setText(dir[0])