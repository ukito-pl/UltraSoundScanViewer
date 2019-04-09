# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RaportWindow.ui'
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
        Dialog.resize(763, 765)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_new_report = QtGui.QPushButton(Dialog)
        self.pushButton_new_report.setObjectName(_fromUtf8("pushButton_new_report"))
        self.verticalLayout.addWidget(self.pushButton_new_report)
        self.pushButton_open_report = QtGui.QPushButton(Dialog)
        self.pushButton_open_report.setObjectName(_fromUtf8("pushButton_open_report"))
        self.verticalLayout.addWidget(self.pushButton_open_report)
        self.label_file_dir = QtGui.QLabel(Dialog)
        self.label_file_dir.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file_dir.setObjectName(_fromUtf8("label_file_dir"))
        self.verticalLayout.addWidget(self.label_file_dir)
        self.treeWidget = QtGui.QTreeWidget(Dialog)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.header().setDefaultSectionSize(200)
        self.treeWidget.header().setMinimumSectionSize(60)
        self.verticalLayout.addWidget(self.treeWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graphicsView = QtGui.QGraphicsView(Dialog)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setObjectName(_fromUtf8("comboBox_type"))
        self.horizontalLayout.addWidget(self.comboBox_type)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setBaseSize(QtCore.QSize(0, 0))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_delete = QtGui.QPushButton(Dialog)
        self.pushButton_delete.setObjectName(_fromUtf8("pushButton_delete"))
        self.horizontalLayout_2.addWidget(self.pushButton_delete)
        self.pushButton_add_change = QtGui.QPushButton(Dialog)
        self.pushButton_add_change.setObjectName(_fromUtf8("pushButton_add_change"))
        self.horizontalLayout_2.addWidget(self.pushButton_add_change)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton_new_report.setText(_translate("Dialog", "Utwórz nowy raport", None))
        self.pushButton_open_report.setText(_translate("Dialog", "Wybierz istniejący raport", None))
        self.label_file_dir.setText(_translate("Dialog", "-", None))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "Nazwa", None))
        self.treeWidget.headerItem().setText(1, _translate("Dialog", "Identyfikator", None))
        self.label.setText(_translate("Dialog", "Rodzaj wady/elementu:", None))
        self.pushButton_delete.setText(_translate("Dialog", "Usuń", None))
        self.pushButton_add_change.setText(_translate("Dialog", "Dodaj/Zmień", None))

