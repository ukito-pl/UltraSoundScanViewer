import numpy as np
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4 import QtGui
from PyQt4 import QtCore

import pyqtgraph.opengl as gl

from LoadScansThread import LoadScansThread
from Create3dScanThread import Create3dScanThread
from ColorMapping import ColorMapping
from ScanViewer import ScanViewer
from PIL import Image
from Miscellaneous import qt_image_to_array
import copy
class ScanManager(QObject):
    def __init__(self, scan_viewer=-1, view_3d=-1, legend_view=-1):
        super(self.__class__,self).__init__()
        self.distanceScan = -1
        self.distanceScanRearranged = -1
        self.distanceScanColored = -1
        self.distanceScanColoredRearranged = -1
        self.thicknessScan = -1
        self.thicknessScanRearranged = -1
        self.thicknessScanColored = -1
        self.thicknessScanColoredRearranged = -1
        self.scan3dItems = -1
        self.scanDir = ""
        self.milimeters_start = 0
        self.milimeters_end = 0
        self.currentFrame = -1
        self.frameRange = 5000
        self.frame_length = 0
        self.colorMapping = ColorMapping()
        self.bd0 = 0
        self.bd1 = 0
        self.bt0 = 0
        self.bt1 = 0
        self.startFrame = 0
        self.endFrame = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.deltaX = 0
        self.deltaY = 0
        self.offsetRatio = 0
        self.offsetY = 0
        self.diameter = 0
        self.nominalDistance = 0
        self.nominalDistanceVal = 0
        self.nominalThickness = 0
        self.nominalThicknessVal = 0
        self.dataPerFrame = 0
        self.resolutionRatio = 1 #transverse resolution / longitudinal resolution
        self.viewDataType = "thickness"
        self.scale_spacing = 0.1  # in meters
        self.goTo = 0.5

        self.scanViewer = scan_viewer
        self.graphicsView3D = view_3d
        self.colorLegendView = legend_view


    def createDefaultColorScale(self):
        self.colorMapping.addScale("ironfire")
        self.colorMapping.setColorAt("ironfire", 255, QtGui.QColor(0, 191, 255))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal * 1.5, QtGui.QColor(0, 191, 255))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal * 1.4, QtGui.QColor(0, 128, 255))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal * 1.1, QtGui.QColor(0, 128, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal, QtGui.QColor(0, 255, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal * 0.9, QtGui.QColor(255, 255, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal * 0.7, QtGui.QColor(255, 128, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal * 0.5, QtGui.QColor(255, 0, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalThicknessVal * 0.2, QtGui.QColor(255, 0, 0))
        self.colorMapping.setColorAt("ironfire", 0, QtGui.QColor(0, 0, 0))

        print self.nominalDistanceVal
        self.colorMapping.addScale("ironfire2")
        self.colorMapping.setColorAt("ironfire2", 255, QtGui.QColor(0, 191, 255))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal * 1.25, QtGui.QColor(0, 191, 255))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal * 1.2, QtGui.QColor(0, 128, 255))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal * 1.1, QtGui.QColor(0, 128, 0))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal, QtGui.QColor(0, 255, 0))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal * 0.9, QtGui.QColor(255, 255, 0))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal * 0.7, QtGui.QColor(255, 128, 0))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal * 0.5, QtGui.QColor(255, 0, 0))
        self.colorMapping.setColorAt("ironfire2", self.nominalDistanceVal * 0.2, QtGui.QColor(255, 0, 0))
        self.colorMapping.setColorAt("ironfire2", 0, QtGui.QColor(0, 0, 0))

    def getXYD(self,pixel_x,pixel_y,no_ratio = False):
        if no_ratio:
            resolutionRatio = 1
        else:
            resolutionRatio = self.resolutionRatio
        x = ((pixel_x + self.startFrame) * self.deltaX) / 1000  # in meters
        y = pixel_y/resolutionRatio * self.deltaY - self.offsetY*self.deltaY
        x_min = ((0 + self.startFrame) * self.deltaX) / 1000  # in meters
        x_max = ((self.endFrame) * self.deltaX) / 1000  # in meters
        indx_min = 0
        indx_max = (self.thicknessScanRearranged.shape[1] - 1)
        indx = pixel_x
        if indx < indx_min:
            indx = indx_min
            x = x_min
        elif indx > indx_max:
            indx = indx_max
            x = x_max
        y_range = self.dataPerFrame * self.deltaY
        y_min = - self.offsetY*self.deltaY
        y_max = y_range - self.offsetY*self.deltaY
        indy_min = 0
        indy_max = (self.thicknessScanRearranged.shape[0] - 1)
        indy = pixel_y//resolutionRatio
        if indy < indy_min:
            indy = indy_min
            y = y_min
        elif indy > indy_max:
            indy = indy_max
            y = y_max
        if y < 0:
            y = y_range + y
        new_range = 12
        y = new_range*y/y_range
        minutes = int((y - int(y))*60)
        hours = int(y)
        depth = self.c * self.thicknessScanRearranged[int(indy), int(indx)] + self.d
        return [x,[hours,minutes],depth]

    def loadScanFromTo(self,milimeters_start, milimeters_end, scan_dir, a, b, c, d, delta_x, diameter, nominal_depth, nominal_dist, bd0,bd1,bt0,bt1,frame_length):
        self.frame_length = frame_length
        self.milimeters_start = milimeters_start
        self.milimeters_end = milimeters_end
        self.bd0 = bd0
        self.bd1 = bd1
        self.bt0 = bt0
        self.bt1 = bt1
        self.dataPerFrame = bt1 - bt0 +1
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.deltaX = delta_x
        self.diameter = diameter
        self.deltaY = 3.14 * self.diameter / self.dataPerFrame
        self.resolutionRatio = self.deltaY/self.deltaX
        self.nominalDistance = nominal_dist
        self.nominalDistanceVal = (self.nominalDistance - self.b) / self.a
        self.nominalThickness = nominal_depth
        self.nominalThicknessVal = (self.nominalThickness - self.d) / self.c
        # self.currentFrame = ( milimeters / self.deltaX).__int__()
        self.frameRange = ((milimeters_start - milimeters_end) / self.deltaX).__int__()
        self.startFrame = (milimeters_start/ self.deltaX).__int__()
        if self.startFrame < 0:
            self.startFrame = 0
        if milimeters_end != -1:
            self.endFrame = (milimeters_end/ self.deltaX).__int__()
        else:
            self.endFrame = -1
        self.scanDir = scan_dir
        self.loadScansThread = LoadScansThread(self.scanDir, self.startFrame, self.endFrame,bd0,bd1,bt0,bt1,frame_length)
        self.connect(self.loadScansThread, SIGNAL('scansLoaded(PyQt_PyObject)'), self.set2dScans)
        self.loadScansThread.start()
        self.createDefaultColorScale()
        self.goTo = 0.5

    def loadScan(self,milimeters, scan_dir, a, b, c, d, delta_x, diameter, nominal_depth, nominal_dist, bd0,bd1,bt0,bt1,frame_length):
        self.frame_length = frame_length
        self.bd0 = bd0
        self.bd1 = bd1
        self.bt0 = bt0
        self.bt1 = bt1
        self.dataPerFrame = bt1 - bt0 +1
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.deltaX = delta_x
        self.diameter = diameter
        self.deltaY = 3.14 * self.diameter / self.dataPerFrame
        self.resolutionRatio = self.deltaY/self.deltaX
        self.nominalDistance = nominal_dist
        self.nominalDistanceVal = (self.nominalDistance - self.b) / self.a
        self.nominalThickness = nominal_depth
        self.nominalThicknessVal = (self.nominalThickness - self.d) / self.c
        # self.currentFrame = ( milimeters / self.deltaX).__int__()
        self.frameRange = 32000
        self.startFrame = (milimeters/ self.deltaX).__int__() - self.frameRange/2
        if self.startFrame < 0:
            self.startFrame = 0
        self.endFrame = (milimeters/ self.deltaX).__int__() + self.frameRange/2
        self.milimeters_start = self.startFrame*self.deltaX
        self.milimeters_end =  self.endFrame*self.deltaX
        self.scanDir = scan_dir
        self.loadScansThread = LoadScansThread(self.scanDir, self.startFrame, self.endFrame,bd0,bd1,bt0,bt1,frame_length)
        self.connect(self.loadScansThread, SIGNAL('scansLoaded(PyQt_PyObject)'), self.set2dScans)
        self.loadScansThread.start()
        self.createDefaultColorScale()
        self.goTo = (milimeters/ self.deltaX - self.startFrame)/(self.endFrame - self.startFrame)

    def changeScanRangeAndLoad(self,milimeters_start, milimeters_end):

        print milimeters_start,milimeters_end
        # self.currentFrame = ( milimeters / self.deltaX).__int__()
        # self.frameRange = (milimeters_range / self.deltaX).__int__()
        self.startFrame = (milimeters_start / self.deltaX).__int__()
        if self.startFrame < 0:
            self.startFrame = 0
        self.endFrame = (milimeters_end / self.deltaX).__int__()
        page_step = self.scanViewer.horizontalScrollBar().pageStep()
        max = self.scanViewer.horizontalScrollBar().maximum() + page_step
        min = self.scanViewer.horizontalScrollBar().minimum()
        scroll_bar_range = max - min
        if milimeters_start > self.milimeters_start:
            self.goTo = 0.5 - float(page_step/float(scroll_bar_range))/2
        elif milimeters_start < self.milimeters_start:
            self.goTo = 0.5 + float(page_step / float(scroll_bar_range)) / 2

        self.loadScansThread = LoadScansThread(self.scanDir, self.startFrame, self.endFrame, self.bd0, self.bd1, self.bt0, self.bt1,
                                               self.frame_length)
        self.connect(self.loadScansThread, SIGNAL('scansLoaded(PyQt_PyObject)'), self.set2dScans)
        self.loadScansThread.start()
        self.createDefaultColorScale()
        self.milimeters_start = milimeters_start
        self.milimeters_end = milimeters_end


    def set2dScans(self,data):
        self.thicknessScan = np.array(data[0])
        self.thicknessScanRearranged = self.thicknessScan
        self.thicknessScanColored = self.colorScan(self.thicknessScan, "ironfire")
        self.thicknessScanColoredRearranged = self.thicknessScanColored

        self.distanceScan = np.array(data[1])
        self.distanceScanRearranged = self.thicknessScan
        self.distanceScanColored = self.colorScan(self.distanceScan, "ironfire2")
        self.distanceScanColoredRearranged = self.distanceScanColored

        self.rearrangeScan(self.offsetRatio)
        self.emit(SIGNAL('scans2dLoaded()'))

        if self.viewDataType == "thickness":
            image = self.getThicknessImageScan()
        elif self.viewDataType == "distance":
            image = self.getDistanceImageScan()
        if self.scanViewer != -1:
            self.scanViewer.clearScene()
            self.scanViewer.aspect_ratio = self.resolutionRatio
            self.scanViewer.setScanImage(image)
            #print self.goTo
            self.addScaleBar(7)
            self.scanViewer.goTo(self.goTo)
            self.scanViewer.moveScaleBar()


    def colorScan(self, scan, color_scale_name):
        colored_scan = np.zeros((scan.shape[0],scan.shape[1],3), dtype=np.uint8)
        for i in range(0, self.thicknessScan.shape[0]):
            colored_scan[i,: , :] = self.colorMapping.lookUpTables[color_scale_name][scan[i,:]]
        return colored_scan

    def rearrangeScan(self,val_ratio):

        self.offsetRatio = val_ratio
        rows = self.thicknessScan.shape[0]
        first_row = int(rows*val_ratio)
        self.offsetY = first_row

        self.thicknessScanRearranged = np.zeros(self.thicknessScan.shape, dtype=np.uint8)
        self.thicknessScanRearranged[0:first_row, :] = self.thicknessScan[rows - first_row:rows, :]
        self.thicknessScanRearranged[first_row:rows, :] = self.thicknessScan[0:rows - first_row, :]

        rearranged_array = np.zeros(self.thicknessScanColored.shape, dtype=np.uint8)
        rearranged_array[0:first_row, :, :] = self.thicknessScanColored[rows - first_row:rows, :, :]
        rearranged_array[first_row:rows, :, :] = self.thicknessScanColored[0:rows - first_row, :, :]
        self.thicknessScanColoredRearranged = rearranged_array

        self.distanceScanRearranged = np.zeros(self.distanceScan.shape, dtype=np.uint8)
        self.distanceScanRearranged[0:first_row, :] = self.distanceScan[rows - first_row:rows, :]
        self.distanceScanRearranged[first_row:rows, :] = self.distanceScan[0:rows - first_row, :]

        rearranged_array = np.zeros(self.distanceScanColored.shape, dtype=np.uint8)
        rearranged_array[0:first_row, :, :] = self.distanceScanColored[rows - first_row:rows, :, :]
        rearranged_array[first_row:rows, :, :] = self.distanceScanColored[0:rows - first_row, :, :]
        self.distanceScanColoredRearranged = rearranged_array

        self.update2dScan()

    def addScaleBar(self, scale_line_height):
        # scale_line_height - in pixels
        print "scale added",self.scanViewer.view_scale,self.scale_spacing
        items = self.getScaleBarItems(self.scale_spacing, scale_line_height, self.scanViewer.view_scale, self.deltaX)
        for i in range(0,len(items)):
            self.scanViewer.addItem(items[i][0],items[i][1],items[i][2])

    def getScaleBarItems(self,spacing, scale_line_height, scale, deltaX):
        items = []
        spacing_px_org = spacing / deltaX * 1000  # because deltaX is in mm
        spacing_px = float(spacing_px_org * scale)
        scaleLineImg = 0 * np.ones(
            (scale_line_height, (self.thicknessScan.shape[1] * scale).__int__(), 3),
            dtype=np.uint8)
        for i in range(((self.thicknessScan.shape[1] * scale) // spacing_px).__int__()):
            left_bound = (i * spacing_px).__int__()
            right_bound = (i * spacing_px + spacing_px).__int__()
            if i.__mod__(2) == 1:
                scaleLineImg[1:scale_line_height - 1, left_bound:right_bound] = 50 * np.ones(
                    (1, right_bound - left_bound, 3))
            else:
                scaleLineImg[1:scale_line_height - 1, left_bound:right_bound] = 255 * np.ones(
                    (1, right_bound - left_bound, 3))

        scaleLineImage = QtGui.QImage(scaleLineImg, scaleLineImg.shape[1], scaleLineImg.shape[0],
                                      scaleLineImg.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(scaleLineImage)
        pixItem = QtGui.QGraphicsPixmapItem()
        pixItem.setPixmap(pix)
        pixItem.setPos(0, -scale_line_height)
        pixItem.setZValue(1000)
        items.append([pixItem,False,True])

        for i in range(((self.thicknessScan.shape[1] * scale) // spacing_px).__int__()):
            x = ((i * spacing_px_org + self.startFrame) * deltaX) / 1000  # in meters

            textItem = QtGui.QGraphicsTextItem("{:.3F}".format(x))
            font = QtGui.QFont()
            font.setPointSize(8)
            textItem.setFont(font)
            textItem.document().setDocumentMargin(0)
            text_offset_x = textItem.boundingRect().width()
            text_offset_y = textItem.boundingRect().height()
            if i == 0:
                textItem.setPos(0, -scale_line_height - text_offset_y)
            else:
                textItem.setPos(0 - text_offset_x / 2 + i * spacing_px, -scale_line_height - text_offset_y)
            textItem.setZValue(1000)
            items.append([textItem, False, True])


        scale_background = 255 * np.ones(((scale_line_height + text_offset_y).__int__(),
                                          (self.thicknessScan.shape[1] * scale).__int__(),
                                          3),
                                         dtype=np.uint8)
        scale_background_image = QtGui.QImage(scale_background, scale_background.shape[1], scale_background.shape[0],
                                              scale_background.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(scale_background_image)
        pixItem = QtGui.QGraphicsPixmapItem()
        pixItem.setPixmap(pix)
        pixItem.setPos(0, -scale_line_height - text_offset_y)
        pixItem.setZValue(900)
        items.append([pixItem, False, True])

        textItem = QtGui.QGraphicsTextItem()
        textItem.setHtml("<div style='background-color: #ffffff;'>" + "[m]" + "</div>")
        font = QtGui.QFont()
        font.setPointSize(8)
        textItem.setFont(font)
        textItem.document().setDocumentMargin(0)
        text_offset_x = textItem.boundingRect().width()
        text_offset_y = textItem.boundingRect().height()
        textItem.setPos(text_offset_x, -scale_line_height - text_offset_y)
        textItem.setZValue(1000)
        items.append([textItem, True,True])

        return items

    def changeScale(self):
        spacing_px_org = self.scale_spacing / self.deltaX * 1000
        spacing_px = float(spacing_px_org * self.scanViewer.view_scale)
        if spacing_px > 130:
            self.scale_spacing = self.scale_spacing / 2
        elif spacing_px < 40:
            self.scale_spacing = self.scale_spacing * 2
        self.addScaleBar(7)

    def getColorLegendItems(self, legend_height):
        items = []
        if self.viewDataType == "thickness":
            ndval = self.nominalThicknessVal
            scale_name = "ironfire"
        elif self.viewDataType == "distance":
            ndval = self.nominalDistanceVal
            scale_name = "ironfire2"
        max_dval = ndval * 1.5
        min_dval = ndval * 0
        scale_values = np.array([0,0.25,0.5, 0.65, 0.8, 0.9, 1, 1.1, 1.2, 1.35, 1.5]) * ndval
        scale_values = [int(x) for x in scale_values]
        step = legend_height / (max_dval - min_dval + 1)
        # legend_array = np.zeros((legend_height, 21, 4), dtype=np.uint8)
        # legend_array[:,0:21,3] = 255
        legend_array = np.zeros((legend_height, 20, 4), dtype=np.uint8)
        legend_array[:, 0:15, 3] = 255
        j = 0
        for val in range(int(min_dval), int(max_dval + 1)):
            color = self.colorMapping.lookUpTables[scale_name][val]
            legend_array[int((-j - 1) * step - 1 -1 ):int((-j) * step - 1), 1:15, 0:3] = list(reversed(color))
            #legend_array[int((-j - 1) * step - 1 - 1):int((-j) * step - 1), 1:20, 0:3] = list(reversed(color))

            if val in scale_values:
                mid = int(((-j - 1) * step - 1 - 1 + (-j) * step - 1) / 2)
                legend_array[mid, 10:20, :] = [0, 0, 0, 255]
                if self.viewDataType == "thickness":
                    real_val = self.c * val + self.d
                elif self.viewDataType == "distance":
                    real_val = self.a * val + self.b
                textItem = QtGui.QGraphicsTextItem(real_val.__str__())
                font = QtGui.QFont()
                font.setPointSize(8)
                textItem.setFont(font)
                textItem.document().setDocumentMargin(0)
                text_offset_y = textItem.boundingRect().height()
                textItem.setPos(20, legend_array.shape[0] + mid - text_offset_y / 2)
                items.append(textItem)

            j = j + 1

        textItem = QtGui.QGraphicsTextItem("[mm]")
        font = QtGui.QFont()
        font.setPointSize(8)
        textItem.setFont(font)
        textItem.document().setDocumentMargin(0)
        textItem.setPos(-5, -15 )
        items.append(textItem)

        legend_array[:, 0, :] = [0, 0, 0, 255]
        legend_array[:, 15, :] = [0, 0, 0, 255]
        legend_array[0, 0:15, :] = [0, 0, 0, 255]
        legend_array[-1, 0:15, :] = [0, 0, 0, 255]

        # legend_array[:, 0, :] = [0, 0, 0, 255]
        # legend_array[:, 20, :] = [0, 0, 0, 255]
        # legend_array[0, 0:20, :] = [0, 0, 0, 255]
        # legend_array[-1, 0:20, :] = [0, 0, 0, 255]

        image = QtGui.QImage(legend_array, legend_array.shape[1], legend_array.shape[0], legend_array.shape[1] * 4,
                             QtGui.QImage.Format_ARGB32)
        legendPixMap = QtGui.QPixmap(image)
        legendPixMapItem = QtGui.QGraphicsPixmapItem(legendPixMap)
        items.append(legendPixMapItem)

        return items

    def create3dScan(self, x_start, x_end, smooth, shaded,w):
        self.create3dScanThread = Create3dScanThread(self.dataPerFrame, self.deltaX, self.diameter, self.nominalDistance,  self.startFrame, self.a, self.b, self.distanceScan, self.thicknessScanColored, x_start, x_end, smooth, shaded,w)
        self.connect(self.create3dScanThread, SIGNAL('3dScanCreated(PyQt_PyObject)'), self.set3dScan)
        self.create3dScanThread.start()

    def set3dScan(self,items):
        self.scan3dItems = items
        if self.graphicsView3D.items.__len__() > 0:
            for i in range(0, self.graphicsView3D.items.__len__()):
                self.graphicsView3D.items.__delitem__(0)
        g = gl.GLGridItem()
        g.scale(2, 2, 1)
        g.setDepthValue(10)
        self.graphicsView3D.addItem(g)

        for item in self.scan3dItems:
            self.graphicsView3D.addItem(item)
        self.emit(SIGNAL('scans3dLoaded()'))




    def getThicknessData(self,i1,i2,j1,j2, all=False):
        if all:
            data = self.c*self.thicknessScan + self.d
            return data
        else:
            data = np.zeros((i2-i1,j2-j1))
            k = 0
            for i in range(i1,i2):
                l = 0
                for j in range(j1,j2):
                    data[k,l] = self.c * self.thicknessScanRearranged[i, j] + self.d
                    l = l+1
                k = k+1
            return data

    def getThicknessImageScan(self):
        image_thick = QtGui.QImage(self.thicknessScanColoredRearranged, self.thicknessScanColoredRearranged.shape[1],
                                   self.thicknessScanColoredRearranged.shape[0], self.thicknessScanColoredRearranged.shape[1] * 3,
                                   QtGui.QImage.Format_RGB888)
        return image_thick

    def getDistanceImageScan(self):
        image_dist = QtGui.QImage(self.distanceScanColoredRearranged, self.distanceScanColoredRearranged.shape[1],
                                  self.distanceScanColoredRearranged.shape[0], self.distanceScanColoredRearranged.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888)
        return image_dist

    def update2dScan(self):
        if self.viewDataType == "thickness":
            image = self.getThicknessImageScan()
        elif self.viewDataType == "distance":
            image = self.getDistanceImageScan()
        if self.scanViewer != -1:
            self.scanViewer.setScanImage(image)

    def checkIfScanLimitsReached(self):
        max = self.scanViewer.horizontalScrollBar().maximum()
        min = self.scanViewer.horizontalScrollBar().minimum()
        scroll_bar_range = max - min
        val = self.scanViewer.horizontalScrollBar().value()
        milimeters_range =  self.milimeters_end - self.milimeters_start
        #print val
        if val == max:
            self.changeScanRangeAndLoad(self.milimeters_start + milimeters_range/2, self.milimeters_end + milimeters_range/2 )
        if val == min:
            self.changeScanRangeAndLoad(self.milimeters_start - milimeters_range/2, self.milimeters_end - milimeters_range/2 )

    def get2DImageToSave(self, x,y,w,h):
        arrayToSave = []
        if self.viewDataType == "thickness":
            arrayToSave = self.thicknessScanColoredRearranged[y:y + h, x:x + w, :]
        elif self.viewDataType == "distance":
            arrayToSave = self.distanceScanColoredRearranged[y:y + h, x:x + w, :]
        image2d = Image.fromarray(arrayToSave)
        image2d = image2d.resize((w, int(h * self.scanViewer.aspect_ratio)))
        legendImg = self.getLegendImage()
        images = [image2d, legendImg]
        imageToSave = self.stackImageHorizontally(images)
        return imageToSave


    def get3DImageToSave(self):
        image3d = self.convertQImageToPILImage(self.graphicsView3D.grabFrameBuffer())
        legendImg = self.getLegendImage()
        images = [image3d, legendImg]
        imageToSave = self.stackImageHorizontally(images)
        return imageToSave


    def convertQImageToPILImage(self, qimage):
        s = qimage.bits().asstring(qimage.width() * qimage.height() * 4)
        arr = np.fromstring(s, dtype=np.uint8).reshape((qimage.height(), qimage.width(), 4))
        rgb_arr = copy.deepcopy(arr)
        rgb_arr[:, :, 2] = arr[:, :, 0]
        rgb_arr[:, :, 0] = arr[:, :, 2]
        PILImage = Image.fromarray(rgb_arr)
        return PILImage

    def getLegendImage(self):
        # convert legendview to PIL Image
        rect = self.colorLegendView.viewport().rect()
        pixmap = QtGui.QPixmap(rect.size())
        pixmap.fill(color=QtGui.QColor(255, 255, 255))
        painter = QtGui.QPainter(pixmap)
        self.colorLegendView.render(painter, QtCore.QRectF(pixmap.rect()), rect)
        painter.end()
        legend_Qimage = pixmap.toImage()
        legendImg = self.convertQImageToPILImage(legend_Qimage)
        return legendImg

    def stackImageHorizontally(self, PILimages):
        widths, heights = zip(*(i.size for i in PILimages))
        max_height = max(heights)
        resized_images = []
        for image in PILimages:
            ratio = float(max_height / float(image.size[1]))
            resized_images.append(image.resize((int(image.size[0] * ratio), int(image.size[1] * ratio))))
        widths, heights = zip(*(i.size for i in resized_images))
        total_width = sum(widths)
        max_height = max(heights)
        stacked_image = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in resized_images:
            stacked_image.paste(im, (x_offset, 0))
            x_offset += im.size[0]
        return stacked_image