# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL


import ResultsWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ResultsDialog(QtGui.QDialog, ResultsWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

    def clearResults(self):
        self.label_results.setText("-")
        self.label_P.setText("-")
        self.label_A.setText("-")
        self.label_Lmax.setText("-")
        self.label_Pprim.setText("-")