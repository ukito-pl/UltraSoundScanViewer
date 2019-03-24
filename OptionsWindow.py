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
        Dialog.resize(566, 407)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.textEdit_url = QtGui.QTextEdit(Dialog)
        self.textEdit_url.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_url.setMaximumSize(QtCore.QSize(16777215, 27))
        self.textEdit_url.setObjectName(_fromUtf8("textEdit_url"))
        self.verticalLayout.addWidget(self.textEdit_url)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.textEdit_diameter = QtGui.QTextEdit(Dialog)
        self.textEdit_diameter.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_diameter.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_diameter.setObjectName(_fromUtf8("textEdit_diameter"))
        self.gridLayout_2.addWidget(self.textEdit_diameter, 1, 1, 1, 1)
        self.textEdit_deltaX = QtGui.QTextEdit(Dialog)
        self.textEdit_deltaX.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_deltaX.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_deltaX.setObjectName(_fromUtf8("textEdit_deltaX"))
        self.gridLayout_2.addWidget(self.textEdit_deltaX, 0, 1, 1, 1)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 0, 2, 1, 1)
        self.textEdit_dist = QtGui.QTextEdit(Dialog)
        self.textEdit_dist.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_dist.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_dist.setObjectName(_fromUtf8("textEdit_dist"))
        self.gridLayout_2.addWidget(self.textEdit_dist, 3, 1, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_18 = QtGui.QLabel(Dialog)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 0, 6, 1, 1)
        self.label_17 = QtGui.QLabel(Dialog)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_2.addWidget(self.label_17, 0, 4, 1, 1)
        self.textEdit_corr_treshold = QtGui.QTextEdit(Dialog)
        self.textEdit_corr_treshold.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_corr_treshold.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_corr_treshold.setObjectName(_fromUtf8("textEdit_corr_treshold"))
        self.gridLayout_2.addWidget(self.textEdit_corr_treshold, 0, 5, 1, 1)
        self.label_20 = QtGui.QLabel(Dialog)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_2.addWidget(self.label_20, 2, 4, 1, 1)
        self.textEdit_F = QtGui.QTextEdit(Dialog)
        self.textEdit_F.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_F.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_F.setObjectName(_fromUtf8("textEdit_F"))
        self.gridLayout_2.addWidget(self.textEdit_F, 2, 5, 1, 1)
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_2.addWidget(self.label_15, 3, 0, 1, 1)
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_2.addWidget(self.label_16, 3, 2, 1, 1)
        self.label_19 = QtGui.QLabel(Dialog)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 1, 4, 1, 1)
        self.textEdit_smys = QtGui.QTextEdit(Dialog)
        self.textEdit_smys.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_smys.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_smys.setObjectName(_fromUtf8("textEdit_smys"))
        self.gridLayout_2.addWidget(self.textEdit_smys, 1, 5, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBox, 1, 6, 1, 1)
        self.textEdit_depth = QtGui.QTextEdit(Dialog)
        self.textEdit_depth.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_depth.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_depth.setObjectName(_fromUtf8("textEdit_depth"))
        self.gridLayout_2.addWidget(self.textEdit_depth, 2, 1, 1, 1)
        self.label_21 = QtGui.QLabel(Dialog)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_2.addWidget(self.label_21, 3, 4, 1, 1)
        self.textEdit_T = QtGui.QTextEdit(Dialog)
        self.textEdit_T.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_T.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_T.setObjectName(_fromUtf8("textEdit_T"))
        self.gridLayout_2.addWidget(self.textEdit_T, 3, 5, 1, 1)
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_2.addWidget(self.label_14, 0, 0, 1, 1)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 1, 2, 1, 1)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 2, 2, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 3, 1, 1)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 2, 3, 1, 1)
        self.line_3 = QtGui.QFrame(Dialog)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_2.addWidget(self.line_3, 3, 3, 1, 1)
        self.line_4 = QtGui.QFrame(Dialog)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout_2.addWidget(self.line_4, 0, 3, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 0, 1, 2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit_C = QtGui.QTextEdit(Dialog)
        self.textEdit_C.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_C.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_C.setObjectName(_fromUtf8("textEdit_C"))
        self.gridLayout.addWidget(self.textEdit_C, 2, 1, 1, 1)
        self.textEdit_D = QtGui.QTextEdit(Dialog)
        self.textEdit_D.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_D.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_D.setObjectName(_fromUtf8("textEdit_D"))
        self.gridLayout.addWidget(self.textEdit_D, 2, 3, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.textEdit_B = QtGui.QTextEdit(Dialog)
        self.textEdit_B.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_B.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_B.setObjectName(_fromUtf8("textEdit_B"))
        self.gridLayout.addWidget(self.textEdit_B, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.textEdit_A = QtGui.QTextEdit(Dialog)
        self.textEdit_A.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_A.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_A.setObjectName(_fromUtf8("textEdit_A"))
        self.gridLayout.addWidget(self.textEdit_A, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 5, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 4, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_6.setText(_translate("Dialog", "Ścieżka do pliku:", None))
        self.textEdit_url.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textEdit_diameter.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textEdit_deltaX.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_12.setText(_translate("Dialog", "Nominalna grubość\n"
"ścianki", None))
        self.label_13.setText(_translate("Dialog", "mm", None))
        self.textEdit_dist.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_9.setText(_translate("Dialog", "Zewnętrzna średnica\n"
"rurociągu:", None))
        self.label_18.setText(_translate("Dialog", "%", None))
        self.label_17.setText(_translate("Dialog", "Próg korozji:", None))
        self.textEdit_corr_treshold.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_20.setText(_translate("Dialog", "Współczynnik F:", None))
        self.textEdit_F.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_15.setText(_translate("Dialog", "Nominalna odległość\n"
"czujników od ścianki", None))
        self.label_16.setText(_translate("Dialog", "mm", None))
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
        self.textEdit_depth.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_21.setText(_translate("Dialog", "Współczynnik T:", None))
        self.textEdit_T.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1</p></body></html>", None))
        self.label_14.setText(_translate("Dialog", "Odległosć pomiędzy\n"
"pomiarami:", None))
        self.label_10.setText(_translate("Dialog", "mm", None))
        self.label_11.setText(_translate("Dialog", "mm", None))
        self.textEdit_C.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textEdit_D.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
        self.label_2.setText(_translate("Dialog", "A:", None))
        self.textEdit_A.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_4.setText(_translate("Dialog", "C:", None))
        self.label_5.setText(_translate("Dialog", "D:", None))
        self.label.setText(_translate("Dialog", "Współczynniki:", None))

