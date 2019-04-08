# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL


import RaportLoadWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ReportLoadDialog(QtGui.QDialog, RaportLoadWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__(flags = QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        #self.connect(self.pushButton_open, SIGNAL('clicked()'), self.getFile)
        #self.connect(self.pushButton_new, SIGNAL('clicked()'), self.newFile)