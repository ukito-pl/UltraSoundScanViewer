import numpy as np
from Miscellaneous import isclose
from math import sqrt
class EvaulatorMAOP:
    def __init__(self):
        self.MAOP = 0
        self.data = 0 #matrix of processed data, every element in data represents depth (in mm) of segment of pipeline

    def evaluateMAOP(self,data,nominal_depth,nominal_diameter):
        nominal_diameter = float(nominal_diameter)
        nominal_depth = float(nominal_depth)
        self.data = np.array(data)
        d = self.findDepthOfCorrosion(nominal_depth)
        if d/nominal_depth > 0.1 and d/nominal_depth < 0.8:
            Lmax = self.evaluateL(nominal_diameter,nominal_depth,d)
            Lm = self.measureL(self.data,nominal_depth)

    def findDepthOfCorrosion(self, nominal_depth):
        dmin = nominal_depth
        for row in self.data:
            for element in row:
                if not isclose(element,0):
                    if element < dmin:
                        dmin = element
        return nominal_depth - dmin

    def evaluateL(self,diameter, nominal_depth, d):
        B = sqrt(pow((d/nominal_depth)/(1.1*d/nominal_depth - 0.15),2)-1)
        if B > 4.0:
            B = 4
        L = 1.12*B*sqrt(diameter*nominal_depth)
        return L

    def measureL(self, data,nominal_depth):
        corrosion_map = self.createOccupancyGrid(data, 0.9*nominal_depth)
        corrosion_sets = []
        current_set = []
        # for j in range(corrosion_map.shape[1]):
        #     for i in range(corrosion_map.shape[0]):
        #         if corrosion_map[i,j] == 1:

        print corrosion_map
        return 0

    def createOccupancyGrid(self,data, threshold):
        for j in range(data.shape[1]):
            for i in range(data.shape[0]):
                if data[i,j] <= threshold and data[i,j] > 0.0:
                    data[i,j] = 1
                else:
                    data[i,j] = 0
        return data