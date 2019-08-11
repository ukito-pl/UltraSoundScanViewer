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
        MainWindow.resize(803, 723)
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
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_thickness = QtGui.QPushButton(self.centralwidget)
        self.pushButton_thickness.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton_thickness.setMaximumSize(QtCore.QSize(59, 16777215))
        self.pushButton_thickness.setStyleSheet(_fromUtf8("QPushButton{\n"
"background-color: rgb(248, 248, 248);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgb(180, 180, 180);\n"
"border-top-left-radius: 5px;\n"
"\n"
"\n"
"}\n"
"QPushButton:checked{\n"
"    background-color: rgb(225, 225, 225);\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: rgb(180, 180, 180);\n"
"    border-top-left-radius: 5px;\n"
"\n"
"}\n"
"\n"
""))
        self.pushButton_thickness.setCheckable(True)
        self.pushButton_thickness.setChecked(False)
        self.pushButton_thickness.setFlat(True)
        self.pushButton_thickness.setObjectName(_fromUtf8("pushButton_thickness"))
        self.horizontalLayout.addWidget(self.pushButton_thickness)
        self.pushButton_distance = QtGui.QPushButton(self.centralwidget)
        self.pushButton_distance.setMinimumSize(QtCore.QSize(0, 23))
        self.pushButton_distance.setMaximumSize(QtCore.QSize(72, 16777215))
        self.pushButton_distance.setStyleSheet(_fromUtf8("QPushButton{\n"
"background-color: rgb(248, 248, 248);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgb(180, 180, 180);\n"
"border-top-right-radius: 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"    background-color: rgb(225, 225, 225);\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: rgb(180, 180, 180);\n"
"    border-top-right-radius: 5px;\n"
"\n"
"\n"
"}"))
        self.pushButton_distance.setCheckable(True)
        self.pushButton_distance.setChecked(False)
        self.pushButton_distance.setObjectName(_fromUtf8("pushButton_distance"))
        self.horizontalLayout.addWidget(self.pushButton_distance)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.textEdit_km = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_km.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_km.setMaximumSize(QtCore.QSize(150, 27))
        self.textEdit_km.setObjectName(_fromUtf8("textEdit_km"))
        self.horizontalLayout.addWidget(self.textEdit_km)
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_3)
        self.pushButton_go = QtGui.QPushButton(self.centralwidget)
        self.pushButton_go.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_go.setObjectName(_fromUtf8("pushButton_go"))
        self.horizontalLayout.addWidget(self.pushButton_go)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.scanViewer.setStyleSheet(_fromUtf8("background-color:  rgba(255, 255, 255, 0);\n"
""))
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOptions = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/options.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOptions.setIcon(icon)
        self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
        self.actionMove = QtGui.QAction(MainWindow)
        self.actionMove.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_move.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMove.setIcon(icon1)
        self.actionMove.setObjectName(_fromUtf8("actionMove"))
        self.actionCorrosions = QtGui.QAction(MainWindow)
        self.actionCorrosions.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_corrosion.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCorrosions.setIcon(icon2)
        self.actionCorrosions.setObjectName(_fromUtf8("actionCorrosions"))
        self.actionReportAdd = QtGui.QAction(MainWindow)
        self.actionReportAdd.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_report_add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReportAdd.setIcon(icon3)
        self.actionReportAdd.setObjectName(_fromUtf8("actionReportAdd"))
        self.actionAutoDetect = QtGui.QAction(MainWindow)
        self.actionAutoDetect.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_autodetect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAutoDetect.setIcon(icon4)
        self.actionAutoDetect.setObjectName(_fromUtf8("actionAutoDetect"))
        self.actionSW = QtGui.QAction(MainWindow)
        self.actionSW.setCheckable(True)
        self.actionSW.setChecked(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_SW.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSW.setIcon(icon5)
        self.actionSW.setVisible(True)
        self.actionSW.setIconVisibleInMenu(False)
        self.actionSW.setObjectName(_fromUtf8("actionSW"))
        self.actionSP = QtGui.QAction(MainWindow)
        self.actionSP.setCheckable(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_SP.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSP.setIcon(icon6)
        self.actionSP.setVisible(True)
        self.actionSP.setObjectName(_fromUtf8("actionSP"))
        self.actionL = QtGui.QAction(MainWindow)
        self.actionL.setCheckable(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_lamination.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionL.setIcon(icon7)
        self.actionL.setVisible(True)
        self.actionL.setObjectName(_fromUtf8("actionL"))
        self.actionReport = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_report.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReport.setIcon(icon8)
        self.actionReport.setObjectName(_fromUtf8("actionReport"))
        self.screenShoot2D = QtGui.QAction(MainWindow)
        self.screenShoot2D.setCheckable(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_screenshot2d.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.screenShoot2D.setIcon(icon9)
        self.screenShoot2D.setObjectName(_fromUtf8("screenShoot2D"))
        self.screenShoot3D = QtGui.QAction(MainWindow)
        self.screenShoot3D.setCheckable(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8("icons/icon_screenshot3d.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.screenShoot3D.setIcon(icon10)
        self.screenShoot3D.setObjectName(_fromUtf8("screenShoot3D"))
        self.toolBar.addAction(self.actionOptions)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMove)
        self.toolBar.addAction(self.actionCorrosions)
        self.toolBar.addAction(self.actionAutoDetect)
        self.toolBar.addAction(self.screenShoot2D)
        self.toolBar.addAction(self.screenShoot3D)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionReport)
        self.toolBar.addAction(self.actionReportAdd)
        self.toolBar.addAction(self.actionL)
        self.toolBar.addAction(self.actionSW)
        self.toolBar.addAction(self.actionSP)

        self.retranslateUi(MainWindow)
        self.comboBox_3.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_thickness.setText(_translate("MainWindow", "Grubość", None))
        self.pushButton_distance.setText(_translate("MainWindow", "Odległość", None))
        self.label_3.setText(_translate("MainWindow", "Idź do:", None))
        self.textEdit_km.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>", None))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "mm", None))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "m", None))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "km", None))
        self.pushButton_go.setText(_translate("MainWindow", "Idź!", None))
        self.pushButton_3d.setText(_translate("MainWindow", "Generuj widok 3D", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionOptions.setText(_translate("MainWindow", "Opcje", None))
        self.actionMove.setText(_translate("MainWindow", "M", None))
        self.actionCorrosions.setText(_translate("MainWindow", "C", None))
        self.actionReportAdd.setText(_translate("MainWindow", "R+", None))
        self.actionAutoDetect.setText(_translate("MainWindow", "A", None))
        self.actionSW.setText(_translate("MainWindow", "SW", None))
        self.actionSP.setText(_translate("MainWindow", "SP", None))
        self.actionL.setText(_translate("MainWindow", "L", None))
        self.actionReport.setText(_translate("MainWindow", "R", None))
        self.screenShoot2D.setText(_translate("MainWindow", "C2D", None))
        self.screenShoot3D.setText(_translate("MainWindow", "C3D", None))

from ScanViewer import ScanViewer
from pyqtgraph.opengl import GLViewWidget

