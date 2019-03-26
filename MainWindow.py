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
        MainWindow.resize(790, 766)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_options = QtGui.QPushButton(self.centralwidget)
        self.pushButton_options.setObjectName(_fromUtf8("pushButton_options"))
        self.horizontalLayout_2.addWidget(self.pushButton_options)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit_km_range = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_km_range.setMaximumSize(QtCore.QSize(50, 27))
        self.textEdit_km_range.setObjectName(_fromUtf8("textEdit_km_range"))
        self.gridLayout.addWidget(self.textEdit_km_range, 0, 4, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.textEdit_km = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_km.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_km.setMaximumSize(QtCore.QSize(150, 27))
        self.textEdit_km.setObjectName(_fromUtf8("textEdit_km"))
        self.gridLayout.addWidget(self.textEdit_km, 0, 1, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_3, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(10, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.pushButton_go = QtGui.QPushButton(self.centralwidget)
        self.pushButton_go.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_go.setObjectName(_fromUtf8("pushButton_go"))
        self.gridLayout.addWidget(self.pushButton_go, 0, 6, 1, 1, QtCore.Qt.AlignLeft)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(15, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 5, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalSlider = QtGui.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setInvertedAppearance(True)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.horizontalLayout_3.addWidget(self.verticalSlider)
        self.scanViewer = ScanViewer(self.centralwidget)
        self.scanViewer.setMinimumSize(QtCore.QSize(0, 0))
        self.scanViewer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scanViewer.setStyleSheet(_fromUtf8("background-color:  rgba(255, 255, 255, 0)"))
        self.scanViewer.setLineWidth(0)
        self.scanViewer.setObjectName(_fromUtf8("scanViewer"))
        self.horizontalLayout_3.addWidget(self.scanViewer)
        self.graphicsView_2 = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.graphicsView_2.setAutoFillBackground(True)
        self.graphicsView_2.setStyleSheet(_fromUtf8("background-color:  rgba(255, 255, 255, 0)"))
        self.graphicsView_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.graphicsView_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.graphicsView_2.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.graphicsView_2.setForegroundBrush(brush)
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.horizontalLayout_3.addWidget(self.graphicsView_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_3d = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3d.setEnabled(False)
        self.pushButton_3d.setObjectName(_fromUtf8("pushButton_3d"))
        self.verticalLayout.addWidget(self.pushButton_3d)
        self.graphicsView = GLViewWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsView.setStyleSheet(_fromUtf8(""))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 25))
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
        self.pushButton_options.setText(_translate("MainWindow", "Opcje", None))
        self.textEdit_km_range.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5</p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "Idź do:", None))
        self.textEdit_km.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>", None))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "mm", None))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "m", None))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "km", None))
        self.label.setText(_translate("MainWindow", "±", None))
        self.pushButton_go.setText(_translate("MainWindow", "Idź!", None))
        self.label_2.setText(_translate("MainWindow", "m", None))
        self.pushButton_3d.setText(_translate("MainWindow", "Generuj widok 3D", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

from ScanViewer import ScanViewer
from pyqtgraph.opengl import GLViewWidget
