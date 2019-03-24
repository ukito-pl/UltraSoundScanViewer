# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectionWindow.ui'
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
        Dialog.resize(816, 456)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.pushButton_params = QtGui.QPushButton(Dialog)
        self.pushButton_params.setObjectName(_fromUtf8("pushButton_params"))
        self.gridLayout_2.addWidget(self.pushButton_params, 1, 0, 1, 1)
        self.pushButton_maop = QtGui.QPushButton(Dialog)
        self.pushButton_maop.setObjectName(_fromUtf8("pushButton_maop"))
        self.gridLayout_2.addWidget(self.pushButton_maop, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 3, 1)
        self.graphicsView = QtGui.QGraphicsView(Dialog)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout_3.addWidget(self.graphicsView, 0, 1, 3, 1)
        self.pushButton_detect_corr = QtGui.QPushButton(Dialog)
        self.pushButton_detect_corr.setObjectName(_fromUtf8("pushButton_detect_corr"))
        self.gridLayout_3.addWidget(self.pushButton_detect_corr, 0, 2, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 1, 2, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_Lm = QtGui.QLabel(Dialog)
        self.label_Lm.setText(_fromUtf8(""))
        self.label_Lm.setObjectName(_fromUtf8("label_Lm"))
        self.gridLayout.addWidget(self.label_Lm, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_d = QtGui.QLabel(Dialog)
        self.label_d.setText(_fromUtf8(""))
        self.label_d.setObjectName(_fromUtf8("label_d"))
        self.gridLayout.addWidget(self.label_d, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 2, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_4.setText(_translate("Dialog", "Parametry służące do analizy:", None))
        self.pushButton_params.setText(_translate("Dialog", "Zmień parametry", None))
        self.pushButton_maop.setText(_translate("Dialog", "Oblicz MAOP", None))
        self.pushButton_detect_corr.setText(_translate("Dialog", "Wykryj korozje", None))
        self.label.setText(_translate("Dialog", "Paramnetry wybranej korozji", None))
        self.label_2.setText(_translate("Dialog", "- Długość:", None))
        self.label_3.setText(_translate("Dialog", "- Maksymalna głębokość:", None))

