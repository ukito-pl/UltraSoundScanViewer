import numpy as np
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4 import QtGui
import pyqtgraph.opengl as gl
from math import sqrt,cos,pi
from LoadScansThread import LoadScansThread
from ColorMapping import ColorMapping
from EvaluatorMAOP import EvaulatorMAOP

class ScanManager(QObject):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.distArray = -1
        self.imgScan = -1
        self.imgScanRearranged = -1
        self.imgScanColored = -1
        self.imgScanColoredRearranged = -1
        self.scanDir = ""
        self.currentFrame = -1
        self.frameRange = 5000
        self.colorMapping = ColorMapping()
        self.startFrame = 0
        self.endFrame = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.deltaX = 0
        self.deltaY = 0
        self.diameter = 0
        self.nominalDepth = 0
        self.nominalDepthval = 0
        self.dataPerFrame = 256
        self.resolutionRatio = 1 #transverse resolution / longitudinal resolution
        self.evaluatorMAOP = EvaulatorMAOP()

    def createDefaultColorScale(self):
        self.colorMapping.addScale("ironfire")
        self.colorMapping.setColorAt("ironfire", 255, QtGui.QColor(0, 191, 255))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval * 1.5, QtGui.QColor(0, 191, 255))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval * 1.2, QtGui.QColor(0, 128, 255))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval * 1.1, QtGui.QColor(0, 128, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval, QtGui.QColor(0, 255, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval * 0.9, QtGui.QColor(255, 255, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval * 0.7, QtGui.QColor(255, 128, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval * 0.5, QtGui.QColor(255, 0, 0))
        self.colorMapping.setColorAt("ironfire", self.nominalDepthval * 0.2, QtGui.QColor(255, 0, 0))
        self.colorMapping.setColorAt("ironfire", 0, QtGui.QColor(0, 0, 0))

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
        self.nominalDepthval = (self.nominalDepth - self.d) / self.c
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
        self.createDefaultColorScale()


    def produceImage(self,data):
        self.distArray = np.array(data[1])
        print self.distArray
        self.imgScan = np.array(data[0])
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
        self.imgScanColoredRearranged = rearranged_array
        image = QtGui.QImage(rearranged_array, rearranged_array.shape[1], rearranged_array.shape[0],
                             rearranged_array.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        self.emit(SIGNAL('updateScan(PyQt_PyObject)'), image)

    def getScaleBarItems(self,spacing, scale_line_height, scale, deltaX):
        items = []
        spacing_px_org = spacing / deltaX * 1000  # because deltaX is in mm
        spacing_px = float(spacing_px_org * scale)
        scaleLineImg = 0 * np.ones(
            (scale_line_height, (self.imgScan.shape[1] * scale).__int__(), 3),
            dtype=np.uint8)
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

    def getColorLegendItems(self, legend_height):
        items = []
        ndval = self.nominalDepthval
        max_dval = ndval * 1.5
        min_dval = ndval * 0.01
        scale_values = np.array([0,0.25,0.5, 0.65, 0.8, 0.9, 1, 1.1, 1.2, 1.35, 1.5]) * ndval
        scale_values = [int(x) for x in scale_values]
        step = legend_height / (max_dval - min_dval + 1)
        legend_array = np.zeros((legend_height, 20, 4), dtype=np.uint8)
        j = 0
        for val in range(int(min_dval), int(max_dval + 1)):
            color = self.colorMapping.lookUpTables["ironfire"][val]
            legend_array[int((-j - 1) * step - 1):int((-j) * step - 1), 1:15, 0:3] = list(reversed(color))
            legend_array[int(j * step):int((j + 1) * step), 1:15, 3] = 255

            if val in scale_values:
                mid = int((int((-j - 1) * step - 1) + int((-j) * step - 1)) / 2)
                legend_array[mid, 10:20, :] = [0, 0, 0, 255]
                real_val = self.c * val + self.d
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

        image = QtGui.QImage(legend_array, legend_array.shape[1], legend_array.shape[0], legend_array.shape[1] * 4,
                             QtGui.QImage.Format_ARGB32)
        legendPixMap = QtGui.QPixmap(image)
        legendPixMapItem = QtGui.QGraphicsPixmapItem(legendPixMap)
        items.append(legendPixMapItem)

        return items

    def evaluateMAOP(self,rect):
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        data_to_eval = [self.c * el + self.d for el in self.imgScanRearranged[y:y+h, x:x+w, 0]]
        self.evaluatorMAOP.evaluateMAOP(data_to_eval, self.nominalDepth,self.diameter, self.deltaX)

    def get3DViewPipeItems(self):
        items = []
        N = self.dataPerFrame
        length = 500 #in millimeters
        L = int(length/self.deltaX)
        r = 1 #in scene coordinates
        nominal_r_mm = self.diameter/2
        base = 60 #mm
        l = float(length/nominal_r_mm*r)
        phi = np.linspace(0,2*pi,N)
        x = np.zeros((N,1))
        y = np.linspace(0, l, L)
        z = np.zeros((N, L))

        verts = np.zeros((L*len(x),3))
        faces =  np.zeros((2*L*len(x)-L,3),dtype=np.int32)
        colors = np.ones((L*len(x),4))
        v = 0 #vertex counter
        f = 0 #faces counter
        for i in range(0,N+1):
            for j in range(len(y)):
                if i < N:
                    r_mm = base + self.a * self.distArray[i, self.distArray.shape[1] / 2 + j] + self.b
                    r = float(r_mm / nominal_r_mm)
                    x[i] = r * cos(phi[i])

                    if i < N / 2:
                        z[i, j] = - sqrt(abs(r * r - x[i] * x[i]))
                    else:
                        z[i, j] = sqrt(abs(r * r - x[i] * x[i]))
                    ######################
                    verts[v,:] = [x[i],y[j],z[i,j]]
                    colors[v, 0:3] = [(float(w) / 255) for w in self.imgScanColored[i, self.imgScanColored.shape[1] / 2 + j] ]
                    if i >0 and j > 0 and j < L-1:
                        if self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i, self.distArray.shape[1] / 2 + j -1] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j] < 255:
                            faces[f, :] = [v, v - 1, v - L]
                            f = f+1
                        elif self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j - 1] < 255:
                            faces[f, :] = [v, v - L, v - L -1]
                            f = f+1
                        if self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j+1] < 255:
                            faces[f, :] = [v, v - L, v - L + 1]
                            f = f +1
                        elif self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[i, self.distArray.shape[1] / 2 + j + 1] < 255:
                            faces[f, :] = [v, v - L, v + 1]
                            f = f+1
                    elif i > 0 and j == 0:
                        if self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j+1] < 255:
                            faces[f,:] = [v,v-L,v-L+1]
                            f = f+1
                        elif self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[i, self.distArray.shape[1] / 2 + j + 1] < 255:
                            faces[f, :] = [v, v - L, v + 1]
                            f = f+1
                    elif i > 0 and j == L-1:
                        if self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i, self.distArray.shape[1] / 2 + j -1] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j] < 255:
                            faces[f,:] = [v,v-L,v-1]
                            f = f+1
                        elif self.distArray[i, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[i-1, self.distArray.shape[1] / 2 + j - 1] < 255:
                            faces[f, :] = [v, v - L, v - L -1]
                            f = f+1
                elif i == N:
                    if j > 0 and j < L-1:
                        if self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[0, self.distArray.shape[1] / 2 + j -1] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j] < 255:
                            faces[f, :] = [j, j - 1, v - L]
                            f = f+1
                        elif self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j - 1] < 255:
                            faces[f, :] = [j, v - L, v - L -1]
                            f = f+1
                        if self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j+1] < 255:
                            faces[f, :] = [j, v - L, v - L + 1]
                            f = f +1
                        elif self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[0, self.distArray.shape[1] / 2 + j + 1] < 255:
                            faces[f, :] = [j, v - L, j + 1]
                            f = f+1
                    elif j == 0:
                        if self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j+1] < 255:
                            faces[f,:] = [j,v-L,v-L+1]
                            f = f+1
                        elif self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[0, self.distArray.shape[1] / 2 + j + 1] < 255:
                            faces[f, :] = [j, v - L, j + 1]
                            f = f+1
                    elif j == L-1:
                        if self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[0, self.distArray.shape[1] / 2 + j -1] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j] < 255:
                            faces[f,:] = [j,v-L,j-1]
                            f = f+1
                        elif self.distArray[0, self.distArray.shape[1] / 2 + j] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j ] < 255 and self.distArray[N-1, self.distArray.shape[1] / 2 + j - 1] < 255:
                            faces[f, :] = [j, v - L, v - L -1]
                            f = f+1
                v = v + 1
        m1 = gl.GLMeshItem(vertexes=verts, faces=faces, vertexColors=colors, smooth=True)

        items.append(m1)

        return items