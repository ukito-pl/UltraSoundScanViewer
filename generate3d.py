from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL

import numpy as np

import Generate3dDialog

class Generate3dDialog(QtGui.QDialog, Generate3dDialog.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setText("Generuj")


    def accept(self):
        super(self.__class__,self).accept()
        x1 = float(self.textEdit.toPlainText().replace(",","."))
        x2 = float(self.textEdit_2.toPlainText().replace(",", "."))
        shaded = self.checkBox.checkState()
        smooth = self.checkBox_2.checkState()
        self.emit(SIGNAL('generate3d(PyQt_PyObject)'), [x1, x2, smooth, shaded])