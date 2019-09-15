# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL

import numpy as np
from math import sqrt
import SelectionWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer

from EvaluatorMAOP import EvaulatorMAOP
from results import ResultsDialog
from reference import ReferenceSelectionDialog
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class EvaluationDialog(QtGui.QDialog, SelectionWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.scene = QtGui.QGraphicsScene()
        self.pixItem = QtGui.QGraphicsPixmapItem()
        self.selectionPixItems = []
        self.corrosions = []
        self.corrosionsParams = []
        self.selectedCorrosionIndex = -1
        self.evaluatorMOAP = EvaulatorMAOP()
        self.resultsDialog = ResultsDialog()
        self.referenceDialog = ReferenceSelectionDialog()

        self.connect(self.pushButton_params,SIGNAL("clicked()"), self.changeParams)
        self.connect(self.pushButton_detect_corr,SIGNAL('clicked()'),self.detectCorrosions)
        self.connect(self.pushButton_maop,SIGNAL('clicked()'),self.evaluateMAOP)
        self.connect(self.graphicsView,SIGNAL("mouseClicked(PyQt_PyObject)"),self.mouseSelect)
        self.connect(self.pushButton_choose_ref_plane,SIGNAL('clicked()'),self.activateRefSelection)
        self.connect(self.referenceDialog,SIGNAL('rejected()'), self.enable)
        self.connect(self.referenceDialog, SIGNAL('setNominalThickness(PyQt_PyObject)'), self.setNominalThickness)
        self.connect(self.resultsDialog.pushButton_report, SIGNAL('clicked()'), self.sendReportSignal)

        self.diameter = 0
        self.deltaX = 0
        self.nominalThickness = 0
        self.smys = 0
        self.pressureUnitSMYS = 0
        self.pressureMAOP = 0
        self.pressureUnitMAOP = 0
        self.factorT = 0
        self.factorF = 0
        self.thicknessTreshold = 0
        self.pressureUnitsList = ["Pa", "hPa", "bar", "psi", "atm"]
        self.pressureUnitsDividers = [10000.0, 100.0, 1.0, 14.5038, 0.987] #convertion array to bars
        self.thicknessDataAray = 0
        self.aspectRatio = 1
        self.reportData = []
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def sendReportSignal(self):
        self.emit(SIGNAL('corrosionReportSignal(PyQt_PyObject)'), self.reportData)

    def setNominalThickness(self,t):
        self.enable()
        self.thicknessTreshold = t
        self.emit(SIGNAL('changeTreshold(PyQt_PyObject)'),t)

    def enable(self):
        self.setEnabled(True)
        self.emit(SIGNAL('deactivateRefSelection()'))

    def activateRefSelection(self):
        self.emit(SIGNAL('activateRefSelection()'))
        self.setEnabled(False)

    def showRefDialog(self,data,data_colored,aspect_ratio):
        self.activateWindow()
        self.referenceDialog.show()
        self.referenceDialog.setData(data,data_colored,aspect_ratio)
        self.referenceDialog.evaluateThickness()
        self.referenceDialog.activateWindow()

    def evaluateMAOP(self):
        self.resultsDialog.clearResults()
        index = self.selectedCorrosionIndex
        description = "-"
        Lm = "-"
        Lmax = "-"
        t = "-"
        d = "-"
        P = "-"
        Pprim = "-"
        if index >= 0:
            d = self.corrosionsParams[index][0] #depth of corrsion
            Lm = self.corrosionsParams[index][1]  # measured length of corrosion
            t = self.nominalThickness
            D = self.diameter
            F = self.factorF
            T = self.factorT
            S = self.smys / self.pressureUnitsDividers[self.pressureUnitSMYS] #convert to bars
            MAOP = self.pressureMAOP / self.pressureUnitsDividers[self.pressureUnitMAOP]#convert to bars
            print d/t
            if d / t > 0.1 and d / t < 0.8:
                Lmax = self.evaluatorMOAP.evaluateL(D, t, d)
                A = 0.893 * (Lm / sqrt(d * t))
                P = max(MAOP, 2 * S * t * F * T / D) # in bars
                self.resultsDialog.label_P.setText("{:.3F}".format(P * self.pressureUnitsDividers[self.pressureUnitMAOP]) + self.pressureUnitsList[self.pressureUnitMAOP])
                self.resultsDialog.label_Lmax.setText("{:.3F}".format(Lmax) + " mm")
                if Lm > Lmax:
                    if A > 4:
                        Pprim = 1.1*P*(1 - d/t)
                    elif A < 4:
                        skl = ((1-2.0/3.0*(d/t))/(1 - 2.0/3.0*(d/(t*sqrt(A*A+1)))))
                        Pprim = 1.1*P*skl
                    Pprim = Pprim * self.pressureUnitsDividers[self.pressureUnitMAOP] #convert to original unit
                    MAOP = MAOP * self.pressureUnitsDividers[self.pressureUnitMAOP] #convert to original unit
                    self.resultsDialog.label_Pprim.setText("{:.3F}".format(Pprim) + self.pressureUnitsList[self.pressureUnitMAOP])
                    self.resultsDialog.label_A.setText("{:.3F}".format(A))
                    print Pprim, MAOP
                    if Pprim > MAOP:
                        description = " Rurociąg może być dalej bezpiecznie eksploatowany przy ciśnieniu roboczym: " + "{:.3F}".format(
                            MAOP) + " " + self.pressureUnitsList[self.pressureUnitMAOP]
                    elif Pprim < MAOP:
                        description = "Należy zredukować ciśnienie robocze do: " + "{:.3F}".format(Pprim) + " " + \
                                      self.pressureUnitsList[
                                          self.pressureUnitMAOP] + ",\n aby rurociąg mógł być bezpiecznie eksploatowany"
                else:
                    MAOP = MAOP * self.pressureUnitsDividers[self.pressureUnitMAOP]  # convert to original unit
                    description = "Długość korozji: " + "{:.3F}".format(
                        Lm) + " mm" + " mniejsza niż Lmax: " + "{:.3F}".format(
                        Lmax) + " mm" + "\n Rurociąg może być bezpiecznie eksploatowany przy ciśnieniu roboczym: " + "{:.3F}".format(
                        MAOP) + " " + self.pressureUnitsList[self.pressureUnitMAOP]

            elif d / t < 0.1:
                description = "Minimalna grubość ścianki mniejsza niż 10% nominalnej grubości\n Rurociąg należy naprawić"

            elif d / t > 0.8:
                description = "Minimalna grubość ścianki większa niż 80% nominalnej grubości\n Rurociąg może być bezpiecznie eksploatowany"
        else:
            description = "Błąd: Nie wybrano żadnego obszaru korozji"

        self.resultsDialog.label_results.setText(
            _translate("Dialog", description, None))
        if Lm != "-":
            Lm = "{:.3F}".format(Lm) + " mm"
        if Lmax != "-":
            Lmax = "{:.3F}".format(Lmax) + " mm"
        if t != "-":
            t = "{:.3F}".format(t) + " mm"
        if d != "-":
            d = "{:.3F}".format(d) + " mm"
        if P != "-":
            P = "{:.3F}".format(P * self.pressureUnitsDividers[self.pressureUnitMAOP]) + self.pressureUnitsList[self.pressureUnitMAOP]
        if Pprim != "-":
            Pprim = "{:.3F}".format(Pprim) + self.pressureUnitsList[self.pressureUnitMAOP]
        max_i,min_i,max_j,min_j = self.checkBoundries(self.corrosions[index])
        x = self.x + min_j - 5
        y = self.y + min_i - 5
        w = (max_j - min_j) + 10
        h = (max_i - min_i) + 10
        self.reportData = [[x,y,w,h], Lm, Lmax, t, d, P, Pprim, description]
        self.resultsDialog.show()

    def mouseSelect(self, QMouseEvent):
        for i in range(len(self.selectionPixItems)):
            if self.graphicsView.itemAt(QMouseEvent.pos()) == self.selectionPixItems[i]:
                self.selectCorrosion(i)
        if self.graphicsView.itemAt(QMouseEvent.pos()) == self.pixItem:
            self.selectCorrosion(-1)

    def selectCorrosion(self,index):
        if self.selectedCorrosionIndex >= 0 and self.selectedCorrosionIndex < len(self.corrosions):
            self.label_d.setText("")
            self.label_Lm.setText("")

            selection = np.zeros((self.thicknessDataAray.shape[0], self.thicknessDataAray.shape[1], 4), dtype=np.uint8)
            for element in self.corrosions[self.selectedCorrosionIndex]:
                selection[element[0], element[1], :] = [200, 200, 200, 200]
            selection_img = QtGui.QImage(selection, selection.shape[1], selection.shape[0], selection.shape[1] * 4,
                                         QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap(selection_img)

            self.selectionPixItems[self.selectedCorrosionIndex].setPixmap(pixmap)
            self.selectedCorrosionIndex = index

        if index >= 0:
            self.selectedCorrosionIndex = index
            self.label_d.setText("{:.1F}".format(self.corrosionsParams[index][0]) + " mm")
            self.label_Lm.setText("{:.1F}".format(self.corrosionsParams[index][1]) + " mm")

            selection = np.zeros((self.thicknessDataAray.shape[0], self.thicknessDataAray.shape[1], 4), dtype=np.uint8)
            for element in self.corrosions[index]:
                selection[element[0], element[1], :] = [200, 200, 200, 255]
            selection_img = QtGui.QImage(selection, selection.shape[1], selection.shape[0], selection.shape[1] * 4,
                                         QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap(selection_img)

            self.selectionPixItems[index].setPixmap(pixmap)
        else:
            self.label_d.setText("")
            self.label_Lm.setText("")
            #self.label_corr_number.setText("")
            self.selectedCorrosionIndex = index

    def changeParams(self):
        self.emit(SIGNAL("changeParams(PyQt_PyObject)"),True)

    def setParameters(self, d, dx, t, smys, smys_unit, p, p_unit, factor_T, factor_F ,th):
        self.diameter = d
        self.deltaX = dx
        self.nominalThickness = t
        self.smys = smys
        self.pressureUnitSMYS = smys_unit
        self.pressureMAOP = p
        self.pressureUnitMAOP = p_unit
        self.factorT = factor_T
        self.factorF = factor_F
        self.thicknessTreshold = th
        self.showParams()

    def showParams(self):
        text = "Parametry służące do analizy: \n"
        text += "- D = " + self.diameter.__str__() + " mm\n"
        text += "- t = " + self.nominalThickness.__str__() + " mm\n"
        text += "- MAOP = " + self.pressureMAOP.__str__() + " " + self.pressureUnitsList[self.pressureUnitMAOP] + "\n"
        text += "- SMYS = " + self.smys.__str__() + " " + self.pressureUnitsList[self.pressureUnitSMYS] + "\n"
        text += "- F = " + self.factorF.__str__() + "\n"
        text += "- T = " + self.factorT.__str__() + "\n"
        text += "- th = " + self.thicknessTreshold.__str__() + " %"
        self.label_params.setText(_translate("Dialog", text, None))


    def setData(self, thickness_data_array, img_to_show, aspect_ratio, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pushButton_maop.setEnabled(False)
        self.selectionPixItems = []
        self.corrosions = []
        self.corrosionsParams = []
        self.selectCorrosion(-1)
        self.label_corr_number.setText("")

        self.aspectRatio = aspect_ratio
        self.thicknessDataAray = thickness_data_array
        img = np.array(img_to_show)
        image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.scene = QtGui.QGraphicsScene()
        pix1 = QtGui.QPixmap(image)
        self.pixItem = QtGui.QGraphicsPixmapItem(pix1)
        self.pixItem.scale(1,aspect_ratio)
        self.scene.addItem(self.pixItem)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.fitInView(self.pixItem, QtCore.Qt.KeepAspectRatio)

    def detectCorrosions(self):
        self.selectionPixItems = []
        self.corrosions = []
        self.corrosionsParams = []
        self.corrosions = self.evaluatorMOAP.findCorrosions(self.thicknessDataAray,self.nominalThickness,
                                                            float((100 - self.thicknessTreshold)/100.0))
        if self.corrosions != []:
            self.label_corr_number.setText(len(self.corrosions).__str__())
        else:
            self.label_corr_number.setText("0")
        for corrosion in self.corrosions:
            selection = np.zeros((self.thicknessDataAray.shape[0],self.thicknessDataAray.shape[1],4),dtype=np.uint8)
            for element in corrosion:
                selection[element[0],element[1],:] = [200,200,200,200]
            selection_img = QtGui.QImage(selection, selection.shape[1], selection.shape[0], selection.shape[1] * 4, QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap(selection_img)
            pixItem = QtGui.QGraphicsPixmapItem(pixmap)
            pixItem.scale(1, self.aspectRatio)
            self.selectionPixItems.append(pixItem)
            self.scene.addItem(self.selectionPixItems[-1])
            params = [0,0]
            params[0] = self.evaluatorMOAP.findDepthOfCorrosion(self.thicknessDataAray,corrosion,self.nominalThickness)
            params[1] = self.evaluatorMOAP.measureL(corrosion,self.deltaX)
            self.corrosionsParams.append(params)
        self.selectCorrosion(len(self.corrosions) - 1)
        self.pushButton_maop.setEnabled(True)

    def checkBoundries(self, corrosion_points_data):
        max_i = corrosion_points_data[0][0]
        min_i = corrosion_points_data[0][0]
        max_j = corrosion_points_data[0][1]
        min_j = corrosion_points_data[0][1]
        for element in corrosion_points_data:
            if element[0] > max_i:
                max_i = element[0]
            elif element[0] < min_i:
                min_i = element[0]
            if element[1] > max_j:
                max_j = element[1]
            elif element[1] < min_j:
                min_j = element[1]
        return [max_i,min_i,max_j,min_j]

    def resizeEvent(self, QResizeEvent):
        super(self.__class__,self).resizeEvent(QResizeEvent)
        self.graphicsView.fitInView(self.pixItem,QtCore.Qt.KeepAspectRatio)