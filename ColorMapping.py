import numpy as np
from PyQt4 import QtGui
#Maps value from 0-255 range to your own RGB8 scale

class ColorMapping():

    def __init__(self):
        self.lookUpTables = {}
        self.gradientColors = {}

    def addScale(self,scale_name):
        array = np.zeros((256,3), dtype=np.uint8)
        if scale_name in self.lookUpTables:
            print "Name taken, overriding"
        self.lookUpTables[scale_name] = array
        self.gradientColors[scale_name] = []
        qcolor = QtGui.QColor(0,0,0)
        self.setColorAt(scale_name,0,qcolor)
        qcolor = QtGui.QColor(255, 255, 255)
        self.setColorAt(scale_name, 255, qcolor)


    def setColorAt(self,scale_name, point, qcolor):
        self.removeColorAt(scale_name,point)
        self.gradientColors[scale_name].append([int(point),qcolor])
        self.createLookUpTable(scale_name)


    def removeColorAt(self,scale_name, point):
        for item in self.gradientColors[scale_name]:
            if int(item[0]) == int(point):
                self.gradientColors[scale_name].remove(item)


    def createLookUpTable(self,scale_name):
        self.gradientColors[scale_name].sort()
        number_of_gradient_nodes = len(self.gradientColors[scale_name])
        if number_of_gradient_nodes >= 2:
            for i in range(0,number_of_gradient_nodes-1):
                start_color = self.gradientColors[scale_name][i][1]
                end_color = self.gradientColors[scale_name][i+1][1]
                start_point = self.gradientColors[scale_name][i][0]
                end_point = self.gradientColors[scale_name][i+1][0]
                self.lookUpTables[scale_name][start_point:end_point+1] = self.interpolateColors(start_color, start_point, end_color, end_point)

    def interpolateColors(self, qcolor1, p1, qcolor2, p2):
        interpolated_array = np.zeros((p2 - p1 +1, 3))
        interpolated_array[0] = [int(x) for x in qcolor1.getRgb()[0:3]]
        interpolated_array[-1] =[int(x) for x in qcolor2.getRgb()[0:3]]

        for i in range(1, interpolated_array.shape[0]-1):
            interpolated_array[i] = interpolated_array[0]  + [int(x) for x in (i * (interpolated_array[-1] - interpolated_array[0])/(p2-p1))]
        return interpolated_array