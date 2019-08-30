from PyQt4.QtCore import QThread,SIGNAL
import numpy as np
from Miscellaneous import ReportTools
from math import sqrt
from Miscellaneous import isclose

class CorrosionDetector(QThread):

    def __init__(self, data_raw, nominal_thickness_raw, data, nominal_thickness, treshold,dx,diameter,
                 spacing, weld_width_v, percentage_v, weld_width_h, percentage_h):
        QThread.__init__(self)
        self.thicknessDataRaw = data_raw
        self.nominalThicknessRaw = nominal_thickness_raw
        self.thicknessData = data
        self.nominalThickness = nominal_thickness
        self.treshold = treshold
        self.dx = dx
        self.diameter = diameter
        self.weldWidthV = weld_width_v
        self.weldWidthH = weld_width_h
        self.spacing = spacing
        self.percentageV = percentage_v
        self.percentageH = percentage_h
    def __del__(self):
        self.wait()

    def run(self):
        corrosions = self.findCorrosions(self.thicknessDataRaw,self.nominalThicknessRaw*self.treshold)

    def findCorrosions(self, data, treshold_val):
        corrosion_points = []
        corrosions = []
        for j in range(data.shape[1]):
            for i in range(data.shape[0]):
                if not [i,j] in corrosion_points:
                    if data[i, j] <= treshold_val and data[i, j] > 0.0:
                        corrosion = self.checkCorrosion(data,i,j,treshold_val)
                        if len(corrosion) > 0:
                            corrosions.append(corrosion)
                            name = "Korozja#" + (len(corrosions)).__str__()
                            self.emit(SIGNAL('corrosionDetected(PyQt_PyObject)'), [name, ReportTools.K, i, j])
                        for point in corrosion:
                            corrosion_points.append(point)

    def checkCorrosion(self,data, i, j,treshold_val):
        corrosion = []
        open_list = []
        end = False
        while not end:
            corrosion.append([i,j])
            for m in range(j - 1, j + 2):
                for n in range(i - 1, i + 2):
                    if n > data.shape[0] - 1:
                        n = data.shape[0] - 1
                    if m > data.shape[1] - 1:
                        m = data.shape[1] - 1
                    if n < 0:
                        n = 0
                    if m < 0:
                        m = 0
                    if not [n,m] in corrosion:
                        if data[n, m] <= treshold_val and data[n, m] > 0.0:
                            open_list.append([n,m])
            if len(open_list) > 0:
                point = open_list.pop(0)
                i = point[0]
                j = point[1]
            else:
                end = True
        L_measured = self.measureL(corrosion,self.dx)
        d = self.findDepthOfCorrosion(self.thicknessData,corrosion,self.nominalThickness)
        L_eval = self.evaluateL(self.diameter,self.nominalThickness,d)
        if L_measured > 0.7*L_eval:
            return corrosion
        else:
            return []

    def createOccupancyGrid(self,data, threshold):
        grid = np.zeros(data.shape)
        for j in range(data.shape[1]):
            for i in range(data.shape[0]):
                if data[i,j] <= threshold and data[i,j] > 0.0:
                    grid[i,j] = 1
                else:
                    grid[i,j] = 0
        return grid

    def evaluateL(self,diameter, nominal_depth, d):
        B = sqrt(pow((d/nominal_depth)/(1.1*d/nominal_depth - 0.15),2)-1)
        if B > 4.0:
            B = 4
        L = 1.12*B*sqrt(diameter*nominal_depth)
        return L

    def measureL(self,corrosion_points,dx):
        xmin = corrosion_points[0][1]
        xmax = xmin
        for point in corrosion_points:
            x = point[1]
            if x <= xmin:
                xmin = x
            if x >= xmax:
                xmax = x
        return float((xmax - xmin + 1)*dx)

    def findDepthOfCorrosion(self,data, corrosion_points, nominal_depth):
        dmin = nominal_depth
        for point in corrosion_points:
            i = point[0]
            j = point[1]
            val = data[i,j]
            if not isclose(val, 0):
                if val < dmin:
                    dmin = val
        return nominal_depth - dmin