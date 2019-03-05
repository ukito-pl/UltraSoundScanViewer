# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(781, 783)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_go = QtGui.QPushButton(self.centralwidget)
        self.pushButton_go.setObjectName(_fromUtf8("pushButton_go"))
        self.gridLayout.addWidget(self.pushButton_go, 1, 5, 1, 1)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.gridLayout.addWidget(self.plainTextEdit, 4, 0, 1, 6)
        self.graphicsView = MyGraphicsView(self.centralwidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 532))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 532))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 3, 0, 1, 6)
        self.textEdit_km = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_km.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_km.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_km.setObjectName(_fromUtf8("textEdit_km"))
        self.gridLayout.addWidget(self.textEdit_km, 1, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.pushButton_scans = QtGui.QPushButton(self.centralwidget)
        self.pushButton_scans.setObjectName(_fromUtf8("pushButton_scans"))
        self.gridLayout.addWidget(self.pushButton_scans, 0, 2, 1, 4)
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_3, 1, 4, 1, 1)
        self.pushButton_options = QtGui.QPushButton(self.centralwidget)
        self.pushButton_options.setObjectName(_fromUtf8("pushButton_options"))
        self.gridLayout.addWidget(self.pushButton_options, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 781, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.comboBox_3.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_go.setText(_translate("MainWindow", "Idź!", None))
        self.textEdit_km.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "Idź do:", None))
        self.pushButton_scans.setText(_translate("MainWindow", "Załaduj i wyświetl scany", None))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "mm", None))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "m", None))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "km", None))
        self.pushButton_options.setText(_translate("MainWindow", "Opcje", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

from MyGraphicsView import MyGraphicsView
