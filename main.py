# -*- coding: utf-8 -*-

from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication

from PyQt4 import QtCore
import pyqtgraph.opengl as gl


import MainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from options import OptionsDialog
from EvaluationDialog import EvaluationDialog
from ScanManager import ScanManager
from generate3d import Generate3dDialog
from raport import ReportDialog
from TestDialog import TestDialog
from AutoDetectDialog import AutoDetectDialog
from SavePictureDialog import SavePictureDialog
from AboutDialog import AboutDialog
from Miscellaneous import ToolModes,ReportTools

class MainApp(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.scale_spacing = 0.1 # in meters
        self.viewDataType = "thickness"
        self.scans2dLoaded = False
        self.scans3dLoaded = False
        self.refSelectionMode = False
        self.toolMode = -1
        self.setToolMode(ToolModes.MoveMode)
        self.reportTool = -1
        self.setReportTool(ReportTools.L)
        self.statusBarMessage = ""
        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setText(self.statusBarMessage)
        self.statusbar.addWidget(self.statusLabel)
        self.optionsDialog = OptionsDialog()
        self.evaluationDialog = EvaluationDialog()
        self.scanManager = ScanManager(self.scanViewer,self.graphicsView, self.graphicsView_2)
        self.generate3dDialog = Generate3dDialog()
        self.reportDialog = ReportDialog()
        self.testDialog = TestDialog()
        self.autoDetectDialog = AutoDetectDialog(self.optionsDialog)
        self.savePictureDialog = SavePictureDialog()
        self.aboutDialog = AboutDialog()

        self.connect(self.autoDetectDialog,SIGNAL('showElement(PyQt_PyObject)'),self.loadElement)
        self.reportDialog.connect(self.autoDetectDialog,SIGNAL('reportElement(PyQt_PyObject)'),self.reportDialog.setCurrentElement)

        self.toolBar.actionTriggered.connect(self.processAction)
        self.menubar.triggered.connect(self.processAction)

        self.connect(self.pushButton_thickness,SIGNAL('clicked()'),self.thicknessButtonClicked)
        self.connect(self.pushButton_distance, SIGNAL('clicked()'), self.distanceButtonClicked)

        self.connect(self.pushButton_3d,SIGNAL('clicked()'),self.openGenerete3dDialog)
        self.connect(self.pushButton_go, SIGNAL('clicked()'), self.loadScan)

        self.connect(self.optionsDialog,SIGNAL("accepted()"),self.optionsAccepted)
        self.optionsDialog.connect(self.evaluationDialog,SIGNAL('changeTreshold(PyQt_PyObject)'),self.optionsDialog.setTreshold)

        self.connect(self.scanViewer, SIGNAL('mousePositionChanged(PyQt_PyObject)'), self.mousePositionChanged)
        self.connect(self.scanViewer, SIGNAL('areaSelected(PyQt_PyObject)'), self.areaSelected)
        self.connect(self.scanViewer, SIGNAL('tempDragModeActivated()'), self.tempDragModeEnable)
        self.connect(self.scanViewer, SIGNAL('tempDragModeDeactivated()'), self.tempDragModeDisable)
        self.connect(self.scanViewer, SIGNAL('mouseClicked(PyQt_PyObject)'), self.reportElement)
        self.scanManager.connect(self.scanViewer, SIGNAL('changeScale()'), self.scanManager.changeScale)

        self.connect(self.scanManager, SIGNAL('scans2dLoaded()'), self.setScans2dLoaded)
        self.connect(self.scanManager, SIGNAL('scans3dLoaded()'), self.setScans3dLoaded)

        self.connect(self.evaluationDialog, SIGNAL('changeParams(PyQt_PyObject)'), self.openOptions)
        self.connect(self.evaluationDialog, SIGNAL('activateRefSelection()'), self.activateRefSelectionMode)
        self.connect(self.evaluationDialog, SIGNAL('deactivateRefSelection()'), self.deactivateRefSelectionMode)
        self.connect(self.evaluationDialog, SIGNAL('corrosionReportSignal(PyQt_PyObject)'),self.addCorrosionReport)

        self.connect(self.generate3dDialog,SIGNAL('generate3d(PyQt_PyObject)'),self.generate3d)

        self.verticalSlider.valueChanged.connect(self.rearrangeScan)
        self.scanViewer.horizontalScrollBar().sliderReleased.connect(self.scanManager.checkIfScanLimitsReached)
        self.scanManager.connect(self.scanViewer, SIGNAL('checkIfScanLimitsReached()'), self.scanManager.checkIfScanLimitsReached)

        self.graphicsView.setBackgroundColor([255,255,255,255])
        self.thicknessButtonClicked()

    def processAction(self,q_action):
        if q_action == self.actionOptions:
            self.openOptions()
        elif q_action == self.actionMove:
            self.setToolMode(ToolModes.MoveMode)
        elif q_action == self.actionCorrosions:
            self.setToolMode(ToolModes.CorrosionMode)
        elif q_action == self.actionReportAdd:
            self.setToolMode(ToolModes.ReportMode)
        elif q_action == self.actionReport:
            self.reportDialog.show()
        elif q_action == self.actionAutoDetect:
            self.autoDetectDialog.show()
            self.setToolMode(ToolModes.AutoDetectMode)
        elif q_action == self.screenShoot2D:
            self.setToolMode(ToolModes.ScreenShot2DMode)
        elif q_action == self.screenShoot3D:
            image3DToSave = self.scanManager.get3DImageToSave()
            self.savePictureDialog.saveImg(image3DToSave)
            self.setToolMode(ToolModes.ScreenShot3DMode)
        elif q_action == self.actionL:
            self.setReportTool(ReportTools.L)
        elif q_action == self.actionK:
            self.setReportTool(ReportTools.K)
        elif q_action == self.actionSW:
            self.setReportTool(ReportTools.SW)
        elif q_action == self.actionSP:
            self.setReportTool(ReportTools.SP)
        elif q_action == self.actionAbout:
            self.aboutDialog.show()

    def tempDragModeEnable(self):
        self.actionMove.setChecked(True)
        self.actionCorrosions.setChecked(False)
        self.actionReportAdd.setChecked(False)
        self.actionAutoDetect.setChecked(False)
        self.screenShoot3D.setChecked(False)
        self.screenShoot2D.setChecked(False)


    def tempDragModeDisable(self):
        self.setToolMode(self.toolMode)


    def setToolMode(self, mode):
        self.actionMove.setChecked(False)
        self.actionCorrosions.setChecked(False)
        self.actionReportAdd.setChecked(False)
        self.actionAutoDetect.setChecked(False)
        self.screenShoot3D.setChecked(False)
        self.screenShoot2D.setChecked(False)
        if mode == ToolModes.MoveMode:
            self.scanViewer.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.toolMode = mode
            self.actionMove.setChecked(True)
            self.expandReportTools(False)
        elif mode == ToolModes.CorrosionMode:
            self.toolMode = mode
            self.actionCorrosions.setChecked(True)
            self.expandReportTools(False)
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        elif mode == ToolModes.ReportMode:
            self.toolMode = mode
            self.actionReportAdd.setChecked(True)
            self.expandReportTools(True)
        elif mode == ToolModes.AutoDetectMode:
            self.toolMode = mode
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self.actionAutoDetect.setChecked(True)
            self.expandReportTools(False)
        elif mode == ToolModes.RefSelectionMode:
            self.toolMode = mode
            self.expandReportTools(False)
        elif mode == ToolModes.ScreenShot2DMode:
            self.toolMode = mode
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self.screenShoot2D.setChecked(True)
            self.expandReportTools(False)
        elif mode == ToolModes.ScreenShot3DMode:
            self.toolMode = mode
            self.screenShoot3D.setChecked(True)
            self.expandReportTools(False)

    def expandReportTools(self,expand):
        self.actionSP.setVisible(expand)
        self.actionSW.setVisible(expand)
        self.actionL.setVisible(expand)
        self.actionK.setVisible(expand)

    def setReportTool(self,tool):
        self.reportTool = tool
        self.actionL.setChecked(False)
        self.actionSP.setChecked(False)
        self.actionSW.setChecked(False)
        self.actionK.setChecked(False)
        if tool == ReportTools.L:
            self.actionL.setChecked(True)
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        elif tool == ReportTools.SP:
            self.actionSP.setChecked(True)
            self.scanViewer.setDragMode(QtGui.QGraphicsView.NoDrag)
        elif tool == ReportTools.SW:
            self.actionSW.setChecked(True)
            self.scanViewer.setDragMode(QtGui.QGraphicsView.NoDrag)
        elif tool == ReportTools.K:
            self.actionK.setChecked(True)
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

    def addCorrosionReport(self,data):
        x = data[0][0]
        y = data[0][1]
        w = data[0][2]
        h = data[0][3]
        data.append("imgPath")
        image2DToSave = self.scanManager.get2DImageToSave(x, y, w, h)
        [x, y, d] = self.scanManager.getXYD(x + w/ 2, y + h / 2, no_ratio=True)
        data[0] = 'X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:2d}".format(y[0]) + ' h ' + "{:2d}".format(y[1]) + ' min '.__str__()
        self.reportDialog.show()
        self.reportDialog.activateWindow()
        #print "Wysłano raport", data
        self.reportDialog.setCurrentElement([ReportTools.K.value,data],image2DToSave)

    def setScans2dLoaded(self):
        self.scans2dLoaded = True
        self.pushButton_3d.setEnabled(True)
        self.colorLegend()

    def setScans3dLoaded(self):
        self.scans3dLoaded = True
        self.pushButton_3d.setEnabled(True)

    def activateRefSelectionMode(self):
        self.setRefSelectionMode(True)
        self.activateWindow()

    def deactivateRefSelectionMode(self):
        self.setRefSelectionMode(False)

    def setRefSelectionMode(self,bool):
        if bool:
            self.toolMode = ToolModes.RefSelectionMode
        else:
            self.setToolMode(ToolModes.CorrosionMode)
        self.thicknessButtonClicked()
        self.pushButton_3d.setEnabled(not bool)
        self.pushButton_go.setEnabled(not bool)
        self.textEdit_km.setEnabled(not bool)
        self.pushButton_distance.setEnabled(not bool)
        self.comboBox_3.setEnabled(not bool)
        self.actionOptions.setEnabled(not bool)
        self.actionMove.setEnabled(not bool)
        self.actionAutoDetect.setEnabled(not bool)
        self.actionReport.setEnabled(not bool)
        self.actionCorrosions.setEnabled(not bool)
        self.actionReportAdd.setEnabled(not bool)
        self.screenShoot3D.setEnabled(not bool)
        self.screenShoot2D.setEnabled(not bool)
        self.actionL.setEnabled(not bool)
        self.actionSP.setEnabled(not bool)
        self.actionSW.setEnabled(not bool)

    def thicknessButtonClicked(self):
        self.pushButton_thickness.setChecked(True)
        self.pushButton_distance.setChecked(False)
        self.scanManager.viewDataType = "thickness"
        try:
            self.rearrangeScan()
            self.colorLegend()
        except:
            #print "blad tickness button clicked"
            return

    def distanceButtonClicked(self):
        self.pushButton_distance.setChecked(True)
        self.pushButton_thickness.setChecked(False)
        self.scanManager.viewDataType = "distance"
        try:
            self.rearrangeScan()
            self.colorLegend()
        except:
            #print "blad diustance button clicked"
            return

    def optionsAccepted(self):
        self.setEvalDialogParams()

    def closeEvent(self, QCloseEvent):
        self.evaluationDialog.close()
        self.optionsDialog.close()
        self.aboutDialog.close()
        self.savePictureDialog.close()
        self.autoDetectDialog.close()
        self.generate3dDialog.close()
        self.reportDialog.close()
        self.testDialog.close()
        super(self.__class__, self).closeEvent(QCloseEvent)


    def setEvalDialogParams(self):
        d = self.optionsDialog.Diameter
        dx = self.optionsDialog.DeltaX
        t = self.optionsDialog.thickness
        smys = self.optionsDialog.smys
        smys_unit = self.optionsDialog.pressureUnitSMYS
        p = self.optionsDialog.operatingPressure
        p_unit = self.optionsDialog.pressureUnitP
        factor_T = self.optionsDialog.factorT
        factor_F = self.optionsDialog.factorF
        th = self.optionsDialog.corrosionTreshold
        self.evaluationDialog.setParameters(d, dx, t, smys, smys_unit, p, p_unit, factor_T, factor_F, th)

    def areaSelected(self, rect):
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        thickness_data_array = self.scanManager.getThicknessData(y, y + h + 1, x, x + w + 1)
        if self.toolMode == ToolModes.RefSelectionMode:
            self.evaluationDialog.showRefDialog(thickness_data_array, self.scanManager.thicknessScanColoredRearranged[y:y + h + 1, x:x + w + 1, :],self.scanViewer.aspect_ratio)
        elif self.toolMode == ToolModes.CorrosionMode:
            self.evaluationDialog.show()
            self.setEvalDialogParams()
            self.evaluationDialog.setData(thickness_data_array, self.scanManager.thicknessScanColoredRearranged[y:y + h + 1, x:x + w + 1, :], self.scanViewer.aspect_ratio, x, y, w, h)
            self.evaluationDialog.activateWindow()
        elif self.toolMode == ToolModes.ReportMode:
            self.reportDialog.show()
            self.reportDialog.activateWindow()
            image2DToSave = self.scanManager.get2DImageToSave(x, y, w +1, h + 1)
            [x, y, d] = self.scanManager.getXYD(x + w / 2, y + h /2, no_ratio=True)
            if self.reportTool == ReportTools.L:
                self.reportDialog.setCurrentElement([ReportTools.L.value,['X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:2d}".format(y[0]) + ' h ' + "{:2d}".format(y[1]) + ' min '.__str__(), "{:.3F}".format(w* self.scanManager.deltaX) + " mm",  "{:.3F}".format(h* self.scanManager.deltaX) + " mm", "opisik laminacji", "imgPath"]],image2DToSave)
            elif self.reportTool == ReportTools.SP:
                self.reportDialog.setCurrentElement([ReportTools.SP.value,['X: ' + "{:.3F}".format(x) +" m" , "{:.3F}".format(w* self.scanManager.deltaX) + " mm",  "{:.3F}".format(h* self.scanManager.deltaX) + " mm", "opisik spoiny poprzecznej", "imgPath"]],image2DToSave)
            elif self.reportTool == ReportTools.SW:
                self.reportDialog.setCurrentElement([ReportTools.SW.value,['X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:2d}".format(y[0]) + ' h ' + "{:2d}".format(y[1]) + ' min ', "{:.3F}".format(w* self.scanManager.deltaX) + " mm",  "{:.3F}".format(h* self.scanManager.deltaX) + " mm", "opisik spoiny wzdluznej", "imgPath"]],image2DToSave)
            elif self.reportTool == ReportTools.K:
                self.reportDialog.setCurrentElement([ReportTools.K.value,['X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:2d}".format(y[0]) + ' h ' + "{:2d}".format(y[1]) + ' min '.__str__(), "{:.3F}".format(w* self.scanManager.deltaX) + " mm",  "{:.3F}".format(h* self.scanManager.deltaX) + " mm", "-","-","-","-","-", "imgPath"]],image2DToSave)

        elif self.toolMode == ToolModes.AutoDetectMode:
            self.testDialog.show()
            self.testDialog.setData(self.scanManager.thicknessScanRearranged[y:y + h, x:x + w], self.scanViewer.aspect_ratio)
        elif self.toolMode == ToolModes.ScreenShot2DMode:
            image2DToSave = self.scanManager.get2DImageToSave(x,y,w + 1,h + 1)
            self.savePictureDialog.saveImg(image2DToSave)

    def reportElement(self, pos):
        print "MouseClicked: ", pos
        x = pos[0]
        y = pos[1]
        w = 100
        h = self.scanManager.bt1 - self.scanManager.bt0
        if self.toolMode == ToolModes.ReportMode:
            self.reportDialog.show()
            self.reportDialog.activateWindow()
            if self.reportTool == ReportTools.SP:
                w = 100
                h = self.scanManager.bt1 - self.scanManager.bt0
                image2DToSave = self.scanManager.get2DImageToSave(x - w / 2, 0, w, h)
                [x, y, d] = self.scanManager.getXYD(x , y , no_ratio=True)
                self.reportDialog.setCurrentElement([ReportTools.SP.value, ['X: ' + "{:.3F}".format(x) + " m",
                                                                            "opisik spoiny poprzecznej", "imgPath"]],
                                                    image2DToSave)
            elif self.reportTool == ReportTools.SW:
                w = 300
                h = 50
                image2DToSave = self.scanManager.get2DImageToSave(x - 10, y - h/2, w, h)
                [x, y, d] = self.scanManager.getXYD(x, y, no_ratio=True)
                self.reportDialog.setCurrentElement([ReportTools.SW.value, [
                    'X: ' + "{:.3F}".format(x) + " m" + ', Y: ' + "{:2d}".format(y[0]) + ' h ' + "{:2d}".format(
                        y[1]) + ' min ', "-"
                    , "opisik spoiny wzdluznej", "imgPath"]],
                                                    image2DToSave)

    def mousePositionChanged(self, QMouseEvent):
        if self.scans2dLoaded:
            position = self.scanViewer.mapToScene(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            position = position/self.scanViewer.view_scale
            [x, y, d] = self.scanManager.getXYD(position.x(), position.y())
            self.statusBarMessage = 'X: ' + "{:.3F}".format(x) +" m" + ', Y: ' + "{:2d}".format(y[0]) + ' h ' + "{:2d}".format(y[1]) + ' min ' + 'Grubosc: ' + "{:.3F}".format(d) + ' mm'
            self.statusLabel.setText(self.statusBarMessage)
            self.statusbar.update()



    def enableOnlyPipeParameters(self,bool):
        bool = not bool
        self.optionsDialog.textEdit_url.setEnabled(bool)
        self.optionsDialog.spinBox_frame_length.setEnabled(bool)
        self.optionsDialog.spinBox_thick_b_start.setEnabled(bool)
        self.optionsDialog.spinBox_thick_b_end.setEnabled(bool)
        self.optionsDialog.spinBox_dist_b_start.setEnabled(bool)
        self.optionsDialog.spinBox_dist_b_end.setEnabled(bool)
        self.optionsDialog.textEdit_A.setEnabled(bool)
        self.optionsDialog.textEdit_B.setEnabled(bool)
        self.optionsDialog.textEdit_C.setEnabled(bool)
        self.optionsDialog.textEdit_D.setEnabled(bool)
        self.optionsDialog.textEdit_deltaX.setEnabled(bool)
        self.optionsDialog.textEdit_dist.setEnabled(bool)

    def openOptions(self, onlyPipeParameters = False):
        if onlyPipeParameters:
            self.enableOnlyPipeParameters(True)
        else:
            self.enableOnlyPipeParameters(False)
        self.optionsDialog.show()
        self.optionsDialog.activateWindow()

    def openGenerete3dDialog(self):
        if self.comboBox_3.currentIndex() == 0:
            multiplier = 0.001
        elif self.comboBox_3.currentIndex() == 1:
            multiplier = 1
        elif self.comboBox_3.currentIndex() == 2:
            multiplier = 1000
        meters = float(self.textEdit_km.toPlainText().replace(",", ".")) * multiplier
        x1 = meters - 0.5
        x2 = meters + 0.5
        if self.generate3dDialog.textEdit.toPlainText() == '':
            self.generate3dDialog.textEdit.setText(x1.__str__())
        if self.generate3dDialog.textEdit_2.toPlainText() == '':
            self.generate3dDialog.textEdit_2.setText(x2.__str__())
        self.generate3dDialog.show()

    def generate3d(self,data):
        self.pushButton_3d.setEnabled(False)
        x1 = data[0]
        x2 = data[1]
        smooth = data[2]
        shaded = data[3]
        w = data[4]
        self.scanManager.create3dScan(x1, x2, smooth, shaded,w)





    def rearrangeScan(self):
        val = float(self.verticalSlider.value())
        min = float(self.verticalSlider.minimum())
        max = float(self.verticalSlider.maximum())
        val_ratio = float(val / (max - min))
        self.scanManager.rearrangeScan(val_ratio)


    def loadElement(self,data):
        milimiters = data[0]
        self.loadScan(milimiters)

    def loadScan(self, milimiters_start = -1, milimiters_end = -1):
        self.scans2dLoaded = False
        self.scans3dLoaded = False
        self.generate3dDialog.textEdit.clear()
        self.generate3dDialog.textEdit_2.clear()

        scan_dir = unicode(self.optionsDialog.dataDir)
        a = self.optionsDialog.CoefficientA
        b = self.optionsDialog.CoefficientB
        c = self.optionsDialog.CoefficientC
        d = self.optionsDialog.CoefficientD
        delta_x = self.optionsDialog.DeltaX
        diameter = self.optionsDialog.Diameter
        nominal_thickness = self.optionsDialog.thickness
        nominal_distance = self.optionsDialog.nominalDistance
        bd0 = self.optionsDialog.distanceStartByte
        bd1 = self.optionsDialog.distanceEndByte
        bt0 = self.optionsDialog.thicknessStartByte
        bt1 = self.optionsDialog.thicknessEndByte
        frame_length = self.optionsDialog.frameLength
        #print milimiters_start, milimiters_end
        if milimiters_start == -1 and milimiters_end == -1:
            if self.comboBox_3.currentIndex() == 0:
                multiplier = 1
            elif self.comboBox_3.currentIndex() == 1:
                multiplier = 1000
            elif self.comboBox_3.currentIndex() == 2:
                multiplier = 1000000
            milimeters = float(self.textEdit_km.toPlainText().replace(",",".")) * multiplier
            self.scanManager.loadScan(milimeters , scan_dir, a, b, c, d,
                                      delta_x, diameter, nominal_thickness, nominal_distance, bd0, bd1, bt0, bt1,
                                      frame_length)
        elif  milimiters_start != -1 and milimiters_end == -1:
            milimeters = float(milimiters_start)
            self.scanManager.loadScan(milimeters, scan_dir, a, b, c, d,
                                      delta_x, diameter, nominal_thickness, nominal_distance, bd0, bd1, bt0, bt1,
                                      frame_length)
        else:
            self.scanManager.loadScanFromTo(milimiters_start, milimiters_end, scan_dir, a, b, c, d,
                                      delta_x, diameter, nominal_thickness, nominal_distance, bd0,bd1,bt0,bt1,frame_length)




    def colorLegend(self):
        scene = QtGui.QGraphicsScene()
        items = self.scanManager.getColorLegendItems(400)
        for item in items:
            scene.addItem(item)
        self.graphicsView_2.setScene(scene)
        self.graphicsView_2.setMinimumHeight(scene.sceneRect().height())






def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()