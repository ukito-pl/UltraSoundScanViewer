# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AutoDetectWindow.ui'
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
        Dialog.resize(716, 642)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.comboBox_element = QtGui.QComboBox(Dialog)
        self.comboBox_element.setObjectName(_fromUtf8("comboBox_element"))
        self.comboBox_element.addItem(_fromUtf8(""))
        self.horizontalLayout_4.addWidget(self.comboBox_element)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(531, 151))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 511, 121))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButton_all = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_all.setChecked(True)
        self.radioButton_all.setObjectName(_fromUtf8("radioButton_all"))
        self.verticalLayout.addWidget(self.radioButton_all)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.radioButton_start_end = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_start_end.setObjectName(_fromUtf8("radioButton_start_end"))
        self.horizontalLayout_2.addWidget(self.radioButton_start_end)
        self.textEdit_m_start = QtGui.QTextEdit(self.layoutWidget)
        self.textEdit_m_start.setEnabled(False)
        self.textEdit_m_start.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_m_start.setMaximumSize(QtCore.QSize(150, 27))
        self.textEdit_m_start.setObjectName(_fromUtf8("textEdit_m_start"))
        self.horizontalLayout_2.addWidget(self.textEdit_m_start)
        self.comboBox_m_unit_start = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_m_unit_start.setEnabled(False)
        self.comboBox_m_unit_start.setMaximumSize(QtCore.QSize(50, 16777215))
        self.comboBox_m_unit_start.setObjectName(_fromUtf8("comboBox_m_unit_start"))
        self.comboBox_m_unit_start.addItem(_fromUtf8(""))
        self.comboBox_m_unit_start.addItem(_fromUtf8(""))
        self.comboBox_m_unit_start.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox_m_unit_start)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.textEdit_m_end = QtGui.QTextEdit(self.layoutWidget)
        self.textEdit_m_end.setEnabled(False)
        self.textEdit_m_end.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_m_end.setMaximumSize(QtCore.QSize(150, 27))
        self.textEdit_m_end.setObjectName(_fromUtf8("textEdit_m_end"))
        self.horizontalLayout_2.addWidget(self.textEdit_m_end)
        self.comboBox_m_unit_end = QtGui.QComboBox(self.layoutWidget)
        self.comboBox_m_unit_end.setEnabled(False)
        self.comboBox_m_unit_end.setMaximumSize(QtCore.QSize(50, 16777215))
        self.comboBox_m_unit_end.setObjectName(_fromUtf8("comboBox_m_unit_end"))
        self.comboBox_m_unit_end.addItem(_fromUtf8(""))
        self.comboBox_m_unit_end.addItem(_fromUtf8(""))
        self.comboBox_m_unit_end.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox_m_unit_end)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radioButton_select = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_select.setObjectName(_fromUtf8("radioButton_select"))
        self.horizontalLayout_3.addWidget(self.radioButton_select)
        self.pushButton_select = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_select.setEnabled(False)
        self.pushButton_select.setObjectName(_fromUtf8("pushButton_select"))
        self.horizontalLayout_3.addWidget(self.pushButton_select)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.pushButton_detect = QtGui.QPushButton(Dialog)
        self.pushButton_detect.setObjectName(_fromUtf8("pushButton_detect"))
        self.verticalLayout_2.addWidget(self.pushButton_detect)
        self.treeWidget = QtGui.QTreeWidget(Dialog)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_report = QtGui.QPushButton(Dialog)
        self.pushButton_report.setObjectName(_fromUtf8("pushButton_report"))
        self.horizontalLayout.addWidget(self.pushButton_report)
        self.pushButton_show = QtGui.QPushButton(Dialog)
        self.pushButton_show.setObjectName(_fromUtf8("pushButton_show"))
        self.horizontalLayout.addWidget(self.pushButton_show)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.comboBox_m_unit_start.setCurrentIndex(1)
        self.comboBox_m_unit_end.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.radioButton_start_end, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.textEdit_m_start.setEnabled)
        QtCore.QObject.connect(self.radioButton_start_end, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.comboBox_m_unit_start.setEnabled)
        QtCore.QObject.connect(self.radioButton_start_end, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.textEdit_m_end.setEnabled)
        QtCore.QObject.connect(self.radioButton_start_end, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.comboBox_m_unit_end.setEnabled)
        QtCore.QObject.connect(self.radioButton_select, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.pushButton_select.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Rodzaj poszukiwanego elementu:", None))
        self.comboBox_element.setItemText(0, _translate("Dialog", "Spoina obwodowa", None))
        self.groupBox.setTitle(_translate("Dialog", "Zakres poszukiwań:", None))
        self.radioButton_all.setText(_translate("Dialog", "Całość", None))
        self.radioButton_start_end.setText(_translate("Dialog", "Od:", None))
        self.textEdit_m_start.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>", None))
        self.comboBox_m_unit_start.setItemText(0, _translate("Dialog", "mm", None))
        self.comboBox_m_unit_start.setItemText(1, _translate("Dialog", "m", None))
        self.comboBox_m_unit_start.setItemText(2, _translate("Dialog", "km", None))
        self.label_2.setText(_translate("Dialog", "do:", None))
        self.textEdit_m_end.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>", None))
        self.comboBox_m_unit_end.setItemText(0, _translate("Dialog", "mm", None))
        self.comboBox_m_unit_end.setItemText(1, _translate("Dialog", "m", None))
        self.comboBox_m_unit_end.setItemText(2, _translate("Dialog", "km", None))
        self.radioButton_select.setText(_translate("Dialog", "Wybierz obszar", None))
        self.pushButton_select.setText(_translate("Dialog", "Wybierz", None))
        self.pushButton_detect.setText(_translate("Dialog", "Wyszukaj", None))
        self.pushButton_report.setText(_translate("Dialog", "Raportuj", None))
        self.pushButton_show.setText(_translate("Dialog", "Pokaż w głównym oknie", None))
