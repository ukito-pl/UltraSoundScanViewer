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
        self.imgScanColored = -1
        self.scanDir = ""
        self.frameToLoad = -1
        self.plusMinusFrames = 5000
        self.colorMapping = ColorMapping()

    def loadScan(self,frame, scan_dir):
        self.frameToLoad = frame
        start_frame = (self.frameToLoad - self.plusMinusFrames).__int__()
        if start_frame < 0:
            start_frame = 0;
        end_frame = (self.frameToLoad + self.plusMinusFrames).__int__()
        self.scanDir = scan_dir
        self.loadScansThread = LoadScansThread(self.scanDir, start_frame, end_frame)
        self.connect(self.loadScansThread, SIGNAL('scansLoaded(PyQt_PyObject)'), self.produceImage)
        self.loadScansThread.start()

    def produceImage(self,imag):
        self.imgScan = np.array(imag)
        self.imgScanColored = self.colorScan(self.imgScan)
        # print self.imgScan, self.imgScan.shape
        image = QtGui.QImage(self.imgScanColored, self.imgScanColored.shape[1], self.imgScanColored.shape[0], self.imgScanColored.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        self.emit(SIGNAL('showScan(PyQt_PyObject)'), image)


    def colorScan(self, scan):
        colored_scan = np.zeros(scan.shape, dtype=np.uint8)
        self.colorMapping.addScale("ironfire")
        self.colorMapping.setColorAt("ironfire", 0, QtGui.QColor(0, 0, 0))
        self.colorMapping.setColorAt("ironfire",255,QtGui.QColor(255,255,255))
        self.colorMapping.setColorAt("ironfire", 65, QtGui.QColor(0, 0, 255))
        self.colorMapping.setColorAt("ironfire", 60, QtGui.QColor(100, 0, 255))
        for i in range(0,self.imgScan.shape[0]):
            colored_scan[i,: , :] = self.colorMapping.lookUpTables["ironfire"][scan[i,:,0]]
        #print self.colorMapping.lookUpTables["ironfire"]
        return colored_scan

    def rearrangeScan(self,val_ratio):

        rows = self.imgScan.shape[0]
        first_row = int(rows*val_ratio)

        rearranged_array = np.zeros(self.imgScanColored.shape, dtype=np.uint8)
        rearranged_array[0:first_row, :, :] = self.imgScanColored[rows - first_row:rows, :, :]
        rearranged_array[first_row:rows, :, :] = self.imgScanColored[0:rows - first_row, :, :]

        image = QtGui.QImage(rearranged_array, rearranged_array.shape[1], rearranged_array.shape[0],
                             rearranged_array.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        self.emit(SIGNAL('updateScan(PyQt_PyObject)'), image)