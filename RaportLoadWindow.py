# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RaportLoadWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(201, 78)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_new = QtGui.QPushButton(Dialog)
        self.pushButton_new.setObjectName(_fromUtf8("pushButton_new"))
        self.verticalLayout.addWidget(self.pushButton_new)
        self.pushButton_open = QtGui.QPushButton(Dialog)
        self.pushButton_open.setObjectName(_fromUtf8("pushButton_open"))
        self.verticalLayout.addWidget(self.pushButton_open)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton_new.setText(_translate("Dialog", "Utwórz nowy raport", None))
        self.pushButton_open.setText(_translate("Dialog", "Załaduj istniejący raport", None))

