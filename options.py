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
        self.Diameter = float(self.textEdit_diameter.toPlainText().replace('\n', ""))
        self.thickness = float(self.textEdit_thickness.toPlainText().replace('\n', ""))
        self.nominalDistance = float(self.textEdit_dist.toPlainText().replace('\n', ""))
        self.operatingPressure = float(self.textEdit_P.toPlainText().replace('\n', ""))
        self.pressureUnitP = self.comboBox_2.currentIndex()
        self.smys = float(self.textEdit_smys.toPlainText().replace('\n', ""))
        self.pressureUnitSMYS = self.comboBox.currentIndex()
        self.factorF = float(self.textEdit_F.toPlainText().replace('\n', ""))
        self.factorT = float(self.textEdit_T.toPlainText().replace('\n', ""))
        self.corrosionTreshold = float(self.textEdit_corr_treshold.toPlainText().replace('\n', ""))
        f = open('defaultOptions.txt', 'w')
        lines = [self.dataDir, "\n", self.CoefficientA.__str__(), "\n", self.CoefficientB.__str__(),
                 "\n", self.CoefficientC.__str__(), "\n", self.CoefficientD.__str__(), "\n", self.DeltaX.__str__(),
                 "\n", self.Diameter.__str__(),"\n", self.thickness.__str__(),"\n", self.nominalDistance.__str__(),
                 "\n", self.operatingPressure.__str__(), "\n", self.pressureUnitP.__str__(), "\n", self.smys.__str__(),
                 "\n", self.pressureUnitSMYS.__str__(),"\n", self.factorF.__str__(),"\n", self.factorT.__str__(),
                 "\n", self.corrosionTreshold.__str__()]
        f.writelines(lines)
        self.distanceStartByte = self.spinBox_dist_b_start.value()
        self.distanceEndByte = self.spinBox_dist_b_end.value()
        self.thicknessStartByte = self.spinBox_thick_b_start.value()
        self.thicknessEndByte = self.spinBox_thick_b_end.value()
        f.close()
        f = open('dataStruct.txt', 'w')
        lines = [self.distanceStartByte.__str__(), "\n", self.distanceEndByte.__str__(), "\n", self.thicknessStartByte.__str__(),
                 "\n", self.thicknessEndByte.__str__()]
        f.writelines(lines)
        f.close()
        self.updateOptions()

    def loadOptions(self):
        f = open('defaultOptions.txt', 'r')
        self.dataDir = f.readline().replace('\n', "")
        self.CoefficientA = float(f.readline())
        self.CoefficientB = float(f.readline())
        self.CoefficientC = float(f.readline())
        self.CoefficientD = float(f.readline())
        self.DeltaX = float(f.readline())
        self.Diameter = float(f.readline())
        self.thickness = float(f.readline())
        self.nominalDistance = float(f.readline())
        self.operatingPressure = float(f.readline())
        self.pressureUnitP = int(f.readline())
        self.smys = float(f.readline())
        self.pressureUnitSMYS = int(f.readline())
        self.factorF = float(f.readline())
        self.factorT = float(f.readline())
        self.corrosionTreshold = float(f.readline())
        f.close()
        f = open('dataStruct.txt', 'r')
        self.distanceStartByte = int(f.readline())
        self.distanceEndByte = int(f.readline())
        self.thicknessStartByte = int(f.readline())
        self.thicknessEndByte = int(f.readline())
        f.close()
        self.updateOptions()

    def updateOptions(self):
        self.textEdit_url.setText(self.dataDir)
        self.textEdit_A.setText(self.CoefficientA.__str__())
        self.textEdit_B.setText(self.CoefficientB.__str__())
        self.textEdit_C.setText(self.CoefficientC.__str__())
        self.textEdit_D.setText(self.CoefficientD.__str__())
        self.textEdit_deltaX.setText(self.DeltaX.__str__())
        self.textEdit_diameter.setText(self.Diameter.__str__())
        self.textEdit_thickness.setText(self.thickness.__str__())
        self.textEdit_dist.setText(self.nominalDistance.__str__())
        self.textEdit_P.setText(self.operatingPressure.__str__())
        self.comboBox_2.setCurrentIndex(self.pressureUnitP)
        self.textEdit_smys.setText(self.smys.__str__())
        self.comboBox.setCurrentIndex(self.pressureUnitSMYS)
        self.textEdit_F.setText(self.factorF.__str__())
        self.textEdit_T.setText(self.factorT.__str__())
        self.textEdit_corr_treshold.setText(self.corrosionTreshold.__str__())
        self.spinBox_dist_b_start.setValue(self.distanceStartByte)
        self.spinBox_dist_b_end.setValue(self.distanceEndByte)
        self.spinBox_thick_b_start.setValue(self.thicknessStartByte)
        self.spinBox_thick_b_end.setValue(self.thicknessEndByte)




