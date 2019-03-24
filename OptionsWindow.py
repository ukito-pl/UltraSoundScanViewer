# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OptionsWindows.ui'
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
        Dialog.resize(667, 573)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_4 = QtGui.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_4.addWidget(self.line_2, 0, 0, 1, 1)
        self.label_30 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setAlignment(QtCore.Qt.AlignCenter)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.gridLayout_4.addWidget(self.label_30, 1, 0, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)
        self.textEdit_url = QtGui.QTextEdit(Dialog)
        self.textEdit_url.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_url.setMaximumSize(QtCore.QSize(16777215, 27))
        self.textEdit_url.setObjectName(_fromUtf8("textEdit_url"))
        self.gridLayout_4.addWidget(self.textEdit_url, 3, 0, 1, 1)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_23 = QtGui.QLabel(Dialog)
        self.label_23.setMinimumSize(QtCore.QSize(260, 0))
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.horizontalLayout_3.addWidget(self.label_23)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_22 = QtGui.QLabel(Dialog)
        self.label_22.setMinimumSize(QtCore.QSize(260, 0))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.horizontalLayout_3.addWidget(self.label_22)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_24 = QtGui.QLabel(Dialog)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.horizontalLayout_2.addWidget(self.label_24)
        self.spinBox_dist_b_start = QtGui.QSpinBox(Dialog)
        self.spinBox_dist_b_start.setMaximum(999)
        self.spinBox_dist_b_start.setObjectName(_fromUtf8("spinBox_dist_b_start"))
        self.horizontalLayout_2.addWidget(self.spinBox_dist_b_start)
        self.label_25 = QtGui.QLabel(Dialog)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.horizontalLayout_2.addWidget(self.label_25)
        self.spinBox_dist_b_end = QtGui.QSpinBox(Dialog)
        self.spinBox_dist_b_end.setMaximum(999)
        self.spinBox_dist_b_end.setObjectName(_fromUtf8("spinBox_dist_b_end"))
        self.horizontalLayout_2.addWidget(self.spinBox_dist_b_end)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_27 = QtGui.QLabel(Dialog)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.horizontalLayout_2.addWidget(self.label_27)
        self.spinBox_thick_b_start = QtGui.QSpinBox(Dialog)
        self.spinBox_thick_b_start.setMaximum(999)
        self.spinBox_thick_b_start.setObjectName(_fromUtf8("spinBox_thick_b_start"))
        self.horizontalLayout_2.addWidget(self.spinBox_thick_b_start)
        self.label_26 = QtGui.QLabel(Dialog)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.horizontalLayout_2.addWidget(self.label_26)
        self.spinBox_thick_b_end = QtGui.QSpinBox(Dialog)
        self.spinBox_thick_b_end.setMaximum(999)
        self.spinBox_thick_b_end.setObjectName(_fromUtf8("spinBox_thick_b_end"))
        self.horizontalLayout_2.addWidget(self.spinBox_thick_b_end)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)
        self.line_3 = QtGui.QFrame(Dialog)
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_4.addWidget(self.line_3, 7, 0, 1, 1)
        self.label_28 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setAlignment(QtCore.Qt.AlignCenter)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.gridLayout_4.addWidget(self.label_28, 8, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 0, 5, 2, 1)
        self.textEdit_deltaX = QtGui.QTextEdit(Dialog)
        self.textEdit_deltaX.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_deltaX.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_deltaX.setObjectName(_fromUtf8("textEdit_deltaX"))
        self.gridLayout.addWidget(self.textEdit_deltaX, 0, 6, 2, 1)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 0, 7, 2, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.textEdit_A = QtGui.QTextEdit(Dialog)
        self.textEdit_A.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_A.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_A.setObjectName(_fromUtf8("textEdit_A"))
        self.gridLayout.addWidget(self.textEdit_A, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.textEdit_B = QtGui.QTextEdit(Dialog)
        self.textEdit_B.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_B.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_B.setObjectName(_fromUtf8("textEdit_B"))
        self.gridLayout.addWidget(self.textEdit_B, 1, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 4, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.textEdit_C = QtGui.QTextEdit(Dialog)
        self.textEdit_C.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_C.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_C.setObjectName(_fromUtf8("textEdit_C"))
        self.gridLayout.addWidget(self.textEdit_C, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.textEdit_D = QtGui.QTextEdit(Dialog)
        self.textEdit_D.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_D.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_D.setObjectName(_fromUtf8("textEdit_D"))
        self.gridLayout.addWidget(self.textEdit_D, 2, 3, 1, 1)
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 2, 5, 1, 1)
        self.textEdit_dist = QtGui.QTextEdit(Dialog)
        self.textEdit_dist.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_dist.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_dist.setObjectName(_fromUtf8("textEdit_dist"))
        self.gridLayout.addWidget(self.textEdit_dist, 2, 6, 1, 1)
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout.addWidget(self.label_16, 2, 7, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 9, 0, 1, 1)
        self.line_4 = QtGui.QFrame(Dialog)
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout_4.addWidget(self.line_4, 10, 0, 1, 1)
        self.label_29 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setAlignment(QtCore.Qt.AlignCenter)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.gridLayout_4.addWidget(self.label_29, 11, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)
        self.textEdit_diameter = QtGui.QTextEdit(Dialog)
        self.textEdit_diameter.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_diameter.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_diameter.setObjectName(_fromUtf8("textEdit_diameter"))
        self.gridLayout_2.addWidget(self.textEdit_diameter, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 0, 2, 1, 1)
        self.label_19 = QtGui.QLabel(Dialog)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 0, 3, 1, 1)
        self.textEdit_smys = QtGui.QTextEdit(Dialog)
        self.textEdit_smys.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_smys.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_smys.setObjectName(_fromUtf8("textEdit_smys"))
        self.gridLayout_2.addWidget(self.textEdit_smys, 0, 4, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBox, 0, 5, 1, 1)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 1, 0, 1, 1)
        self.textEdit_thickness = QtGui.QTextEdit(Dialog)
        self.textEdit_thickness.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_thickness.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_thickness.setObjectName(_fromUtf8("textEdit_thickness"))
        self.gridLayout_2.addWidget(self.textEdit_thickness, 1, 1, 1, 1)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 1, 2, 1, 1)
        self.label_20 = QtGui.QLabel(Dialog)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_2.addWidget(self.label_20, 1, 3, 1, 1)
        self.textEdit_F = QtGui.QTextEdit(Dialog)
        self.textEdit_F.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_F.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_F.setObjectName(_fromUtf8("textEdit_F"))
        self.gridLayout_2.addWidget(self.textEdit_F, 1, 4, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.textEdit_P = QtGui.QTextEdit(Dialog)
        self.textEdit_P.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_P.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_P.setObjectName(_fromUtf8("textEdit_P"))
        self.gridLayout_2.addWidget(self.textEdit_P, 2, 1, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBox_2, 2, 2, 1, 1)
        self.label_21 = QtGui.QLabel(Dialog)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_2.addWidget(self.label_21, 2, 3, 1, 1)
        self.textEdit_T = QtGui.QTextEdit(Dialog)
        self.textEdit_T.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_T.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_T.setObjectName(_fromUtf8("textEdit_T"))
        self.gridLayout_2.addWidget(self.textEdit_T, 2, 4, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 12, 0, 1, 1)
        self.line_5 = QtGui.QFrame(Dialog)
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout_4.addWidget(self.line_5, 13, 0, 1, 1)
        self.label_31 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.gridLayout_4.addWidget(self.label_31, 14, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_17 = QtGui.QLabel(Dialog)
        self.label_17.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_3.addWidget(self.label_17, 0, 0, 1, 1)
        self.textEdit_corr_treshold = QtGui.QTextEdit(Dialog)
        self.textEdit_corr_treshold.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_corr_treshold.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_corr_treshold.setObjectName(_fromUtf8("textEdit_corr_treshold"))
        self.gridLayout_3.addWidget(self.textEdit_corr_treshold, 0, 1, 1, 1)
        self.label_18 = QtGui.QLabel(Dialog)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_3.addWidget(self.label_18, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 15, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_4.addWidget(self.buttonBox, 16, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_30.setText(_translate("Dialog", "Dane wejściowe", None))
        self.label_6.setText(_translate("Dialog", "Ścieżka do pliku:", None))
        self.textEdit_url.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_8.setText(_translate("Dialog", "Struktura ramki danych", None))
        self.label_23.setText(_translate("Dialog", "Pomiary odległości", None))
        self.label_22.setText(_translate("Dialog", "Pomiary grubości:", None))
        self.label_24.setText(_translate("Dialog", "Od bajtu:", None))
        self.label_25.setText(_translate("Dialog", "Do bajtu:", None))
        self.label_27.setText(_translate("Dialog", "Od bajtu:", None))
        self.label_26.setText(_translate("Dialog", "Do bajtu:", None))
        self.label_28.setText(_translate("Dialog", "Parametry pomiaru", None))
        self.label_14.setText(_translate("Dialog", "Rozdzielczość wzdłużna \n"
"pomiaru:", None))
        self.textEdit_deltaX.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_13.setText(_translate("Dialog", "mm", None))
        self.label_2.setText(_translate("Dialog", "A:", None))
        self.textEdit_A.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_3.setText(_translate("Dialog", "B:", None))
        self.textEdit_B.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_4.setText(_translate("Dialog", "C:", None))
        self.textEdit_C.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_5.setText(_translate("Dialog", "D:", None))
        self.textEdit_D.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_15.setText(_translate("Dialog", "Nominalna odległość\n"
"czujników od ścianki:", None))
        self.textEdit_dist.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_16.setText(_translate("Dialog", "mm", None))
        self.label.setText(_translate("Dialog", "Współczynniki:", None))
        self.label_29.setText(_translate("Dialog", "Parametry rurociągu", None))
        self.label_9.setText(_translate("Dialog", "Zewnętrzna średnica\n"
"rurociągu:", None))
        self.textEdit_diameter.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_10.setText(_translate("Dialog", "mm", None))
        self.label_19.setText(_translate("Dialog", "SMYS:", None))
        self.textEdit_smys.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.comboBox.setItemText(0, _translate("Dialog", "Pa", None))
        self.comboBox.setItemText(1, _translate("Dialog", "hPa", None))
        self.comboBox.setItemText(2, _translate("Dialog", "bar", None))
        self.comboBox.setItemText(3, _translate("Dialog", "psi", None))
        self.comboBox.setItemText(4, _translate("Dialog", "atm", None))
        self.label_12.setText(_translate("Dialog", "Nominalna grubość\n"
"ścianki:", None))
        self.textEdit_thickness.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_11.setText(_translate("Dialog", "mm", None))
        self.label_20.setText(_translate("Dialog", "Współczynnik F:", None))
        self.textEdit_F.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_7.setText(_translate("Dialog", "Ciśnienie robocze:", None))
        self.textEdit_P.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.comboBox_2.setItemText(0, _translate("Dialog", "Pa", None))
        self.comboBox_2.setItemText(1, _translate("Dialog", "hPa", None))
        self.comboBox_2.setItemText(2, _translate("Dialog", "bar", None))
        self.comboBox_2.setItemText(3, _translate("Dialog", "psi", None))
        self.comboBox_2.setItemText(4, _translate("Dialog", "atm", None))
        self.label_21.setText(_translate("Dialog", "Współczynnik T:", None))
        self.textEdit_T.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1</p></body></html>", None))
        self.label_31.setText(_translate("Dialog", "Pozostałe", None))
        self.label_17.setText(_translate("Dialog", "Próg korozji:", None))
        self.textEdit_corr_treshold.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_18.setText(_translate("Dialog", "%", None))

