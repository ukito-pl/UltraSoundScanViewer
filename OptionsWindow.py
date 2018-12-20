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
        Dialog.resize(430, 433)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(60, 380, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textEdit_A = QtGui.QTextEdit(Dialog)
        self.textEdit_A.setGeometry(QtCore.QRect(30, 130, 100, 27))
        self.textEdit_A.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_A.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_A.setObjectName(_fromUtf8("textEdit_A"))
        self.textEdit_B = QtGui.QTextEdit(Dialog)
        self.textEdit_B.setGeometry(QtCore.QRect(160, 130, 100, 27))
        self.textEdit_B.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_B.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_B.setObjectName(_fromUtf8("textEdit_B"))
        self.textEdit_C = QtGui.QTextEdit(Dialog)
        self.textEdit_C.setGeometry(QtCore.QRect(30, 180, 100, 27))
        self.textEdit_C.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_C.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_C.setObjectName(_fromUtf8("textEdit_C"))
        self.textEdit_D = QtGui.QTextEdit(Dialog)
        self.textEdit_D.setGeometry(QtCore.QRect(160, 180, 100, 27))
        self.textEdit_D.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_D.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_D.setObjectName(_fromUtf8("textEdit_D"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 100, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 140, 31, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(140, 140, 31, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 190, 31, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(140, 190, 31, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.textEdit_url = QtGui.QTextEdit(Dialog)
        self.textEdit_url.setGeometry(QtCore.QRect(30, 60, 371, 27))
        self.textEdit_url.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_url.setMaximumSize(QtCore.QSize(400, 27))
        self.textEdit_url.setObjectName(_fromUtf8("textEdit_url"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 30, 121, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(30, 280, 141, 31))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.textEdit_deltaX = QtGui.QTextEdit(Dialog)
        self.textEdit_deltaX.setGeometry(QtCore.QRect(180, 230, 100, 27))
        self.textEdit_deltaX.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_deltaX.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_deltaX.setObjectName(_fromUtf8("textEdit_deltaX"))
        self.textEdit_diameter = QtGui.QTextEdit(Dialog)
        self.textEdit_diameter.setGeometry(QtCore.QRect(180, 280, 100, 27))
        self.textEdit_diameter.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_diameter.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_diameter.setObjectName(_fromUtf8("textEdit_diameter"))
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(280, 290, 31, 17))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(280, 340, 31, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(30, 330, 171, 31))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.textEdit_depth = QtGui.QTextEdit(Dialog)
        self.textEdit_depth.setGeometry(QtCore.QRect(180, 330, 100, 27))
        self.textEdit_depth.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_depth.setMaximumSize(QtCore.QSize(100, 27))
        self.textEdit_depth.setObjectName(_fromUtf8("textEdit_depth"))
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(280, 240, 31, 17))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(30, 230, 141, 31))
        self.label_14.setObjectName(_fromUtf8("label_14"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.textEdit_A.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textEdit_B.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
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
        self.label.setText(_translate("Dialog", "Współczynniki:", None))
        self.label_2.setText(_translate("Dialog", "A:", None))
        self.label_3.setText(_translate("Dialog", "B:", None))
        self.label_4.setText(_translate("Dialog", "C:", None))
        self.label_5.setText(_translate("Dialog", "D:", None))
        self.textEdit_url.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_6.setText(_translate("Dialog", "Ścieżka do pliku:", None))
        self.label_9.setText(_translate("Dialog", "Zewnętrzna średnica\n"
"rurociągu:", None))
        self.textEdit_deltaX.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textEdit_diameter.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_10.setText(_translate("Dialog", "mm", None))
        self.label_11.setText(_translate("Dialog", "mm", None))
        self.label_12.setText(_translate("Dialog", "Nominalna grubość\n"
"ścianki", None))
        self.textEdit_depth.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_13.setText(_translate("Dialog", "mm", None))
        self.label_14.setText(_translate("Dialog", "Odległosć pomiędzy\n"
"pomiarami:", None))

