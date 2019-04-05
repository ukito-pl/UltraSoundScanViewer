# -*- coding: utf-8 -*-

from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4.QtCore import  SIGNAL
import sys # We need sys so that we can pass argv to QApplication

from PyQt4 import QtCore
import pyqtgraph.opengl as gl


import MainWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from options import OptionsDialog
from evaluate import EvaluationDialog
from ScanManager import ScanManager
from generate3d import Generate3dDialog
from Miscellaneous import ToolModes

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
        self.thicknessButtonClicked()
        self.statusBarMessage = ""
        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setText(self.statusBarMessage)
        self.statusbar.addWidget(self.statusLabel)
        self.optionsDialog = OptionsDialog()
        self.evaluationDialog = EvaluationDialog()
        self.scanManager = ScanManager()
        self.generate3dDialog = Generate3dDialog()

        self.connect(self.pushButton_move,SIGNAL('released()'),self.moveButtonClicked)
        self.connect(self.pushButton_corrosions, SIGNAL('released()'), self.corosionButtonClicked)
        self.connect(self.pushButton_raport, SIGNAL('released()'), self.raportButtonClicked)
        self.connect(self.pushButton_auto_detect, SIGNAL('released()'), self.autoDetectButtonClicked)

        self.connect(self.pushButton_thickness,SIGNAL('clicked()'),self.thicknessButtonClicked)
        self.connect(self.pushButton_distance, SIGNAL('clicked()'), self.distanceButtonClicked)

        self.connect(self.pushButton_options, SIGNAL('clicked()'), self.openOptions)
        self.connect(self.pushButton_3d,SIGNAL('clicked()'),self.openGenerete3dDialog)
        self.connect(self.pushButton_go, SIGNAL('clicked()'), self.loadScan)

        self.connect(self.optionsDialog,SIGNAL("accepted()"),self.optionsAccepted)
        self.optionsDialog.connect(self.evaluationDialog,SIGNAL('changeTreshold(PyQt_PyObject)'),self.optionsDialog.setTreshold)

        self.connect(self.scanViewer, SIGNAL('mousePositionChanged(PyQt_PyObject)'), self.mousePositionChanged)
        self.connect(self.scanViewer, SIGNAL('areaSelected(PyQt_PyObject)'), self.areaSelected)
        self.connect(self.scanViewer, SIGNAL('changeScale()'), self.changeScale)
        self.connect(self.scanViewer, SIGNAL('tempDragModeActivated()'), self.tempDragModeEnable)
        self.connect(self.scanViewer, SIGNAL('tempDragModeDeactivated()'), self.tempDragModeDisable)

        self.connect(self.scanManager, SIGNAL('scans2dLoaded()'), self.setScans2dLoaded)
        self.connect(self.scanManager, SIGNAL('scans3dLoaded()'), self.setScans3dLoaded)

        self.connect(self.evaluationDialog, SIGNAL('changeParams(PyQt_PyObject)'), self.openOptions)
        self.connect(self.evaluationDialog, SIGNAL('activateRefSelection()'), self.activateRefSelectionMode)
        self.connect(self.evaluationDialog, SIGNAL('deactivateRefSelection()'), self.deactivateRefSelectionMode)

        self.connect(self.generate3dDialog,SIGNAL('generate3d(PyQt_PyObject)'),self.generate3d)

        self.verticalSlider.valueChanged.connect(self.rearrangeScan)

        self.graphicsView.setBackgroundColor([128,128,128,255])

    def tempDragModeEnable(self):
        self.pushButton_move.setChecked(True)
        self.pushButton_corrosions.setChecked(False)
        self.pushButton_raport.setChecked(False)
        self.pushButton_auto_detect.setChecked(False)

    def tempDragModeDisable(self):
        self.setToolMode(self.toolMode)
        
    def moveButtonClicked(self):
        self.setToolMode(ToolModes.MoveMode)

    def corosionButtonClicked(self):
        self.setToolMode(ToolModes.CorrosionMode)

    def raportButtonClicked(self):
        self.setToolMode(ToolModes.RaportMode)

    def autoDetectButtonClicked(self):
        self.setToolMode(ToolModes.AutoDetectMode)

    def setToolMode(self, mode):
        self.pushButton_move.setChecked(False)
        self.pushButton_corrosions.setChecked(False)
        self.pushButton_raport.setChecked(False)
        self.pushButton_auto_detect.setChecked(False)
        if mode == ToolModes.MoveMode:

            self.scanViewer.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)####to psuje, pewnie dlatego że te zmienione eventy moje są
            self.toolMode = mode
            self.pushButton_move.setChecked(True)
        elif mode == ToolModes.CorrosionMode:
            self.toolMode = mode
            self.pushButton_corrosions.setChecked(True)
            self.scanViewer.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        elif mode == ToolModes.RaportMode:
            self.toolMode = mode
            self.pushButton_raport.setChecked(True)
        elif mode == ToolModes.AutoDetectMode:
            self.toolMode = mode
            self.pushButton_auto_detect.setChecked(True)
        elif mode == ToolModes.RefSelectionMode:
            self.toolMode = mode

    def setScans2dLoaded(self):
        self.scans2dLoaded = True
        self.show2dScan()

    def setScans3dLoaded(self):
        self.scans3dLoaded = True
        self.show3dScan()

    def activateRefSelectionMode(self):
        self.setRefSelectionMode(True)
        self.activateWindow()

    def deactivateRefSelectionMode(self):
        self.setRefSelectionMode(False)

    def setRefSelectionMode(self,bool):
        self.refSelectionMode = bool
        self.thicknessButtonClicked()
        self.pushButton_3d.setEnabled(not bool)
        self.pushButton_go.setEnabled(not bool)
        self.pushButton_options.setEnabled(not bool)
        self.textEdit_km.setEnabled(not bool)
        self.textEdit_km_range.setEnabled(not bool)
        self.pushButton_distance.setEnabled(not bool)
        self.comboBox_3.setEnabled(not bool)

    def thicknessButtonClicked(self):
        self.pushButton_thickness.setChecked(True)
        self.pushButton_distance.setChecked(False)
        self.viewDataType = "thickness"
        try:
            self.rearrangeScan()
            self.colorLegend()
        except:
            return

    def distanceButtonClicked(self):
        self.pushButton_distance.setChecked(True)
        self.pushButton_thickness.setChecked(False)
        self.viewDataType = "distance"
        try:
            self.rearrangeScan()
            self.colorLegend()
        except:
            return

    def optionsAccepted(self):
        self.setEvalDialogParams()

    def closeEvent(self, QCloseEvent):
        self.evaluationDialog.close()
        self.optionsDialog.close()
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
        thickness_data_array = self.scanManager.getThicknessData(y, y + h, x, x + w)
        if self.refSelectionMode:
            self.evaluationDialog.showRefDialog(thickness_data_array, self.scanManager.thicknessScanColoredRearranged[y:y + h, x:x + w, :],self.scanViewer.aspect_ratio)
        else:
            self.evaluationDialog.show()
            self.setEvalDialogParams()
            self.evaluationDialog.setData(thickness_data_array, self.scanManager.thicknessScanColoredRearranged[y:y + h, x:x + w, :], self.scanViewer.aspect_ratio)
            self.evaluationDialog.activateWindow()

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
        self.scanManager.load3dScan(x1,x2,smooth,shaded)

    def show3dScan(self):
        if self.scans3dLoaded:
            if self.graphicsView.items.__len__() > 0:
                for i in range(0, self.graphicsView.items.__len__()):
                    self.graphicsView.items.__delitem__(0)
            g = gl.GLGridItem()
            g.scale(2, 2, 1)
            g.setDepthValue(10)
            self.graphicsView.addItem(g)

            items = self.scanManager.get3dScanItems()
            for item in items:
                self.graphicsView.addItem(item)
            self.pushButton_3d.setEnabled(True)

    def changeScale(self):
        spacing_px_org = self.scale_spacing / self.optionsDialog.DeltaX * 1000
        spacing_px = float(spacing_px_org * self.scanViewer.view_scale)
        if spacing_px > 130:
            self.scale_spacing = self.scale_spacing / 2
        elif spacing_px < 40:
            self.scale_spacing = self.scale_spacing * 2
        self.addScaleBar(7)

    def rearrangeScan(self):
        val = float(self.verticalSlider.value())
        min = float(self.verticalSlider.minimum())
        max = float(self.verticalSlider.maximum())
        val_ratio = float(val / (max - min))
        self.scanManager.rearrangeScan(val_ratio)
        self.update2dScan()

    def loadScan(self):
        self.scans2dLoaded = False
        self.scans3dLoaded = False
        self.generate3dDialog.textEdit.clear()
        self.generate3dDialog.textEdit_2.clear()
        if self.comboBox_3.currentIndex() == 0:
            multiplier = 1
        elif self.comboBox_3.currentIndex() == 1:
            multiplier = 1000
        elif self.comboBox_3.currentIndex() == 2:
            multiplier = 1000000
        milimeters = float(self.textEdit_km.toPlainText().replace(",",".")) * multiplier
        milimeters_range = float(self.textEdit_km_range.toPlainText().replace(",",".")) * 1000
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
        self.scanManager.loadScan(milimeters, milimeters_range, scan_dir, a, b, c, d, delta_x, diameter,
                                  nominal_thickness, nominal_distance, bd0,bd1,bt0,bt1,frame_length)

    def show2dScan(self):
        if self.scans2dLoaded:
            if self.viewDataType == "thickness":
                image = self.scanManager.getThicknessImageScan()
            elif self.viewDataType == "distance":
                image = self.scanManager.getDistanceImageScan()
            self.scanViewer.clearScene()
            self.scanViewer.resetViewScale()
            self.scanViewer.aspect_ratio = self.scanManager.resolutionRatio
            self.scanViewer.setScanImage(image)

            self.addScaleBar(7)

            frame_range = (self.scanManager.endFrame - self.scanManager.startFrame).__float__()
            px = ((self.scanManager.currentFrame - self.scanManager.startFrame) / frame_range)
            self.scanViewer.goTo(px)
            self.scanViewer.moveScaleBar()
            self.scanViewer.moveScaleBar()
            self.colorLegend()

            self.pushButton_3d.setEnabled(True)

    def update2dScan(self):
        if self.viewDataType == "thickness":
            image = self.scanManager.getThicknessImageScan()
        elif self.viewDataType == "distance":
            image = self.scanManager.getDistanceImageScan()
        self.scanViewer.setScanImage(image)

    def addScaleBar(self, scale_line_height):
        # scale_line_height - in pixels
        items = self.scanManager.getScaleBarItems(self.scale_spacing, scale_line_height, self.scanViewer.view_scale, self.optionsDialog.DeltaX)
        for i in range(0,len(items)):
            self.scanViewer.addItem(items[i][0],items[i][1],items[i][2])


    def colorLegend(self):
        scene = QtGui.QGraphicsScene()
        items = self.scanManager.getColorLegendItems(400,self.viewDataType)
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