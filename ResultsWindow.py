# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ResultsWindow.ui'
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
        Dialog.resize(407, 218)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_A = QtGui.QLabel(Dialog)
        self.label_A.setAlignment(QtCore.Qt.AlignCenter)
        self.label_A.setObjectName(_fromUtf8("label_A"))
        self.gridLayout_3.addWidget(self.label_A, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_Lmax = QtGui.QLabel(Dialog)
        self.label_Lmax.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Lmax.setObjectName(_fromUtf8("label_Lmax"))
        self.gridLayout_2.addWidget(self.label_Lmax, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_P = QtGui.QLabel(Dialog)
        self.label_P.setAlignment(QtCore.Qt.AlignCenter)
        self.label_P.setObjectName(_fromUtf8("label_P"))
        self.gridLayout_4.addWidget(self.label_P, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_Pprim = QtGui.QLabel(Dialog)
        self.label_Pprim.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Pprim.setObjectName(_fromUtf8("label_Pprim"))
        self.gridLayout.addWidget(self.label_Pprim, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_results = QtGui.QLabel(Dialog)
        self.label_results.setAlignment(QtCore.Qt.AlignCenter)
        self.label_results.setObjectName(_fromUtf8("label_results"))
        self.verticalLayout.addWidget(self.label_results)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_results.raise_()
        self.label_P.raise_()
        self.label_Pprim.raise_()
        self.line.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_Lmax.raise_()
        self.label_A.raise_()
        self.label_3.raise_()

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Wyniki analizy", None))
        self.label_5.setText(_translate("Dialog", "Współczynnik pośredni A:", None))
        self.label_A.setText(_translate("Dialog", "-", None))
        self.label_4.setText(_translate("Dialog", "Oszacowana maksymalna długość korozji (Lmax):", None))
        self.label_Lmax.setText(_translate("Dialog", "-", None))
        self.label_P.setText(_translate("Dialog", "-", None))
        self.label_2.setText(_translate("Dialog", "Ciśnienie projektowe (P):", None))
        self.label_Pprim.setText(_translate("Dialog", "-", None))
        self.label_3.setText(_translate("Dialog", "Bezpieczne ciśnienie (P\'):", None))
        self.label_results.setText(_translate("Dialog", "Opis wyniku", None))

