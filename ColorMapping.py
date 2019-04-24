import numpy as np
from PyQt4 import QtGui
#Maps value from 0-255 range to your own RGB8 scale

class ColorMapping():

    def __init__(self):
        self.lookUpTables = {}
        self.gradientColors = {}

    def addScale(self,scale_name):
        array = np.zeros((256,3), dtype=np.uint8)
        #if scale_name in self.lookUpTables:
            #print "Name taken, overriding"
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
                self.lookUpTables[scale_name][start_point:end_point+1] = self.interpolateColorsHSV(start_color, start_point, end_color, end_point)

    def interpolateColorsRGB(self, qcolor1, p1, qcolor2, p2):
        interpolated_array = np.zeros((p2 - p1 +1, 3))
        interpolated_array[0] = [int(x) for x in qcolor1.getRgb()[0:3]]
        interpolated_array[-1] =[int(x) for x in qcolor2.getRgb()[0:3]]

        for i in range(1, interpolated_array.shape[0]-1):
            interpolated_array[i] = interpolated_array[0]  + [int(x) for x in (i * (interpolated_array[-1] - interpolated_array[0])/(p2-p1))]
        return interpolated_array

    def interpolateColorsHSV(self, qcolor1, p1, qcolor2, p2):

        interpolated_array = np.zeros((p2 - p1 +1, 3))
        interpolated_array[0] = [int(x) for x in qcolor1.getHsv()[0:3]]
        interpolated_array[-1] =[int(x) for x in qcolor2.getHsv()[0:3]]
        H1 = interpolated_array[0][0]
        S1 = interpolated_array[0][1]
        V1 = interpolated_array[0][2]
        H2 = interpolated_array[-1][0]
        S2 = interpolated_array[-1][1]
        V2 = interpolated_array[-1][2]

        for i in range(1, interpolated_array.shape[0]-1):

            if 0 < H2 - H1 <= 180:
                H = H1 + i * (H2 - H1) / (p2 - p1)

            elif 180 < H2 - H1 < 360:
                H = H1 - i * (H1 - H2 + 360) / (p2 - p1)

            elif 0 < H1 - H2 <= 180:
                H = H1 - i * (H1 - H2) / (p2 - p1)

            elif 180 < H1 - H2 < 360:
                H = H1 + i * (H2 - H1 + 360) / (p2 - p1)

            else:
                H = H1
            if H < 0:
                H = H + 360
            elif H >= 360:
                H = H - 360
            interpolated_array[i][0] = int(H)
            interpolated_array[i][1] = int(S1 + i * (S2 - S1) / (p2 - p1))
            interpolated_array[i][2] = int(V1 + i * (V2 - V1) / (p2 - p1))
        for i in range(0, interpolated_array.shape[0]):
            qcolor = QtGui.QColor()
            qcolor.setHsv(interpolated_array[i][0],interpolated_array[i][1],interpolated_array[i][2])
            interpolated_array[i] = [int(x) for x in qcolor.getRgb()[0:3]]
        return interpolated_array