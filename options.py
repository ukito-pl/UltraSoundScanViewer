from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL


import OptionsWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer

class OptionsDialog(QtGui.QDialog, OptionsWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.loadOptions()

        self.connect(self.buttonBox, SIGNAL('accepted()'), self.setOptions)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.updateOptions)

    def setOptions(self):
        self.dataDir = self.textEdit_url.toPlainText().replace('\n', "").replace('\r', "").replace('file://', "")
        self.CoefficientA = float(self.textEdit_A.toPlainText().replace('\n', ""))
        self.CoefficientB = float(self.textEdit_B.toPlainText().replace('\n', ""))
        self.CoefficientC = float(self.textEdit_C.toPlainText().replace('\n', ""))
        self.CoefficientD = float(self.textEdit_D.toPlainText().replace('\n', ""))
        self.DeltaX = float(self.textEdit_deltaX.toPlainText().replace('\n', ""))
        self.DeltaY = float(self.textEdit_deltaY.toPlainText().replace('\n', ""))
        f = open('defaultOptions.txt', 'w')
        lines = [self.dataDir, "\n", self.CoefficientA.__str__(), "\n", self.CoefficientB.__str__(),
                 "\n", self.CoefficientC.__str__(), "\n", self.CoefficientD.__str__(), "\n", self.DeltaX.__str__(),
                 "\n", self.DeltaY.__str__()]
        f.writelines(lines)
        self.updateOptions()

    def loadOptions(self):
        f = open('defaultOptions.txt', 'r')
        self.dataDir = f.readline().replace('\n', "")
        self.CoefficientA = float(f.readline())
        self.CoefficientB = float(f.readline())
        self.CoefficientC = float(f.readline())
        self.CoefficientD = float(f.readline())
        self.DeltaX = float(f.readline())
        self.DeltaY = float(f.readline())
        self.updateOptions()

    def updateOptions(self):
        self.textEdit_url.setText(self.dataDir)
        self.textEdit_A.setText(self.CoefficientA.__str__())
        self.textEdit_B.setText(self.CoefficientB.__str__())
        self.textEdit_C.setText(self.CoefficientC.__str__())
        self.textEdit_D.setText(self.CoefficientD.__str__())
        self.textEdit_deltaX.setText(self.DeltaX.__str__())
        self.textEdit_deltaY.setText(self.DeltaY.__str__())






