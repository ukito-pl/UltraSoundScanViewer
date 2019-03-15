import numpy as np
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4 import QtGui

from LoadScansThread import LoadScansThread
from ColorMapping import ColorMapping

class ScanManager(QObject):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.imgScan = -1
        self.imgScanRearranged = -1
        self.imgScanColored = -1
        self.scanDir = ""
        self.currentFrame = -1
        self.frameRange = 5000
        self.colorMapping = ColorMapping()
        self.startFrame = 0
        self.endFrame = 0
        self.createDefaultColorScale()
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.deltaX = 0
        self.deltaY = 0
        self.diameter = 0
        self.nominalDepth = 0
        self.dataPerFrame = 256
        self.resolutionRatio = 1 #transverse resolution / longitudinal resolution

    def createDefaultColorScale(self):
        self.colorMapping.addScale("ironfire")
        self.colorMapping.setColorAt("ironfire", 0, QtGui.QColor(0, 0, 0))
        self.colorMapping.setColorAt("ironfire", 255, QtGui.QColor(255, 255, 255))
        self.colorMapping.setColorAt("ironfire", 65, QtGui.QColor(0, 0, 255))
        self.colorMapping.setColorAt("ironfire", 60, QtGui.QColor(100, 0, 255))

    def getXYD(self,pixel_x,pixel_y):
        x = ((pixel_x + self.startFrame) * self.deltaX) / 1000  # in meters
        y = pixel_y/self.resolutionRatio * self.deltaY
        indx = pixel_x
        if indx < 0:
            indx = 0
            x = ((0 + self.startFrame) * self.deltaX) / 1000  # in meters
        elif indx > (self.imgScan.shape[1] - 1):
            indx = self.imgScan.shape[1] - 1
            x = ((self.endFrame) * self.deltaX) / 1000  # in meters
        indy = pixel_y//self.resolutionRatio
        if indy < 0:
            indy = 0
            y = 0
        elif indy > (self.imgScan.shape[0] - 1):
            indy = self.imgScan.shape[0] - 1
            y = self.dataPerFrame*self.deltaY
        depth = self.c * self.imgScan[int(indy), int(indx), 0] + self.d
        return [x,y,depth]

    def loadScan(self,milimeters, milimeters_range, scan_dir, a, b, c, d, delta_x, diameter, nominal_depth):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.deltaX = delta_x
        self.diameter = diameter
        self.deltaY = 3.14 * self.diameter / self.dataPerFrame
        self.resolutionRatio = self.deltaY/self.deltaX
        self.nominalDepth = nominal_depth
        self.currentFrame = ( milimeters / self.deltaX).__int__()
        self.frameRange = (milimeters_range / self.deltaX).__int__()
        self.startFrame = (self.currentFrame - self.frameRange).__int__()
        if self.startFrame < 0:
            self.startFrame = 0;
        self.endFrame = (self.currentFrame + self.frameRange).__int__()
        self.scanDir = scan_dir
        self.loadScansThread = LoadScansThread(self.scanDir, self.startFrame, self.endFrame)
        self.connect(self.loadScansThread, SIGNAL('scansLoaded(PyQt_PyObject)'), self.produceImage)
        self.loadScansThread.start()

    def produceImage(self,imag):
        self.imgScan = np.array(imag)
        self.imgScanRearranged = self.imgScan
        self.imgScanColored = self.colorScan(self.imgScan, "ironfire")
        # print self.imgScan, self.imgScan.shape
        image = QtGui.QImage(self.imgScanColored, self.imgScanColored.shape[1], self.imgScanColored.shape[0], self.imgScanColored.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        self.emit(SIGNAL('showScan(PyQt_PyObject)'), image)


    def colorScan(self, scan, color_scale_name):
        colored_scan = np.zeros(scan.shape, dtype=np.uint8)
        for i in range(0,self.imgScan.shape[0]):
            colored_scan[i,: , :] = self.colorMapping.lookUpTables[color_scale_name][scan[i,:,0]]
        return colored_scan

    def rearrangeScan(self,val_ratio):

        rows = self.imgScan.shape[0]
        first_row = int(rows*val_ratio)

        self.imgScanRearranged = np.zeros(self.imgScan.shape, dtype=np.uint8)
        self.imgScanRearranged[0:first_row, :, :] = self.imgScan[rows - first_row:rows, :, :]
        self.imgScanRearranged[first_row:rows, :, :] = self.imgScan[0:rows - first_row, :, :]

        rearranged_array = np.zeros(self.imgScanColored.shape, dtype=np.uint8)
        rearranged_array[0:first_row, :, :] = self.imgScanColored[rows - first_row:rows, :, :]
        rearranged_array[first_row:rows, :, :] = self.imgScanColored[0:rows - first_row, :, :]

        image = QtGui.QImage(rearranged_array, rearranged_array.shape[1], rearranged_array.shape[0],
                             rearranged_array.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        self.emit(SIGNAL('updateScan(PyQt_PyObject)'), image)

    def getScaleBarImage(self,spacing, scale_line_height, scale, deltaX):
        spacing_px_org = spacing / deltaX * 1000  # because deltaX is in mm
        spacing_px = float(spacing_px_org * scale)
        scaleLineImg = 0 * np.ones(
            (scale_line_height, (self.imgScan.shape[1] * scale).__int__(), 3),
            dtype=np.uint8)
        # print spacing_px
        for i in range(((self.imgScan.shape[1] * scale) // spacing_px).__int__()):
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
        return scaleLineImage

    def getScaleBarItems(self,spacing, scale_line_height, scale, deltaX):
        items = []
        spacing_px_org = spacing / deltaX * 1000  # because deltaX is in mm
        spacing_px = float(spacing_px_org * scale)
        scaleLineImg = 0 * np.ones(
            (scale_line_height, (self.imgScan.shape[1] * scale).__int__(), 3),
            dtype=np.uint8)
        # print spacing_px
        for i in range(((self.imgScan.shape[1] * scale) // spacing_px).__int__()):
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

        for i in range(((self.imgScan.shape[1] * scale) // spacing_px).__int__()):
            x = ((i * spacing_px_org.__int__() + self.startFrame) * deltaX) / 1000  # in meters

            textItem = QtGui.QGraphicsTextItem(x.__str__())
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
                                          (self.imgScan.shape[1] * scale).__int__(),
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