import numpy as np
from Miscellaneous import isclose
from math import sqrt
class EvaulatorMAOP:
    def __init__(self):
        self.MAOP = 0
        self.data = 0 #matrix of processed data, every element in data represents depth (in mm) of segment of pipeline
        self.P = 1
    def evaluateMAOP(self,data,nominal_depth,nominal_diameter,dx):
        nominal_diameter = float(nominal_diameter)
        nominal_depth = float(nominal_depth)
        self.data = np.array(data)
        d = 0.18
        Lm = 10
        t =0.25
        D = 20
        MAOP = 400
        S = 35000
        F = 0.5
        T = 1
        P = max(MAOP, 2*S*t*F*T/D)
        A = 0.893 * (Lm / sqrt(D * t))
        if A > 4:
            Pprim = 1.1 * P * (1 - d / t)
        elif A < 4:
            skl = ((1 - 2.0 / 3.0 * (d / t)) / (1 - 2.0 / 3.0 * (d / (t * sqrt(A * A + 1)))))
            Pprim = 1.1 * P * skl
        print P, Pprim

        # corrosion_sets = self.findCorrosions(self.data,nominal_depth)
        # for corrosion in corrosion_sets:
        #     d = self.findDepthOfCorrosion(self.data, corrosion,nominal_depth)
        #     if d/nominal_depth > 0.1 and d/nominal_depth < 0.8:
        #         Lmax = self.evaluateL(nominal_diameter,nominal_depth,d)
        #         Lm = self.measureL(corrosion,dx)
        #         print Lmax, Lm
        #         if Lm > Lmax:
        #             A = 0.893 * (Lm / sqrt(nominal_diameter * nominal_depth))
        #             print A, d/nominal_depth
        #             if A > 4:
        #                 Pprim = 1.1*self.P*(1 - d/nominal_depth)
        #             elif A < 4:
        #                 skl = ((1-2.0/3.0*(d/nominal_depth))/(1 - 2.0/3.0*(d/(nominal_depth*sqrt(A*A+1)))))
        #                 Pprim = 1.1*self.P*skl
        #             print Pprim, self.P
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
    def evaluateL(self,diameter, nominal_depth, d):
        B = sqrt(pow((d/nominal_depth)/(1.1*d/nominal_depth - 0.15),2)-1)
        if B > 4.0:
            B = 4
        L = 1.12*B*sqrt(diameter*nominal_depth)
        return L

    def findCorrosions(self, data,nominal_depth):
        corrosion_map = self.createOccupancyGrid(data, 0.9*nominal_depth)
        corrosion_sets = []
        corrosion_sets.append([])
        s = 1
        for j in range(corrosion_map.shape[1]):
            for i in range(corrosion_map.shape[0]):
                if corrosion_map[i,j] == 1:
                    #check neighboors
                    neighboors_sets = []
                    for m in range(j-1,j+2):
                        for n in range(i-1,i+2):
                            if n > corrosion_map.shape[0]-1:
                                n = corrosion_map.shape[0]-1
                            if m > corrosion_map.shape[1]-1:
                                m = corrosion_map.shape[1]-1
                            if n < 0:
                                n = 0
                            if m < 0:
                                m = 0
                            #check if neighbors belong to any set
                            sc = 0
                            while sc < s:
                                if [n,m] in corrosion_sets[sc]:
                                    if not sc in neighboors_sets:
                                        neighboors_sets.append(sc)
                                sc = sc + 1
                    if neighboors_sets == []:
                        corrosion_sets[s-1].append([i,j])
                        s = s + 1
                        corrosion_sets.append([])
                    elif len(neighboors_sets) == 1:
                        corrosion_sets[neighboors_sets[0]].append([i, j])
                    elif len(neighboors_sets) > 1:
                        for w in range(1,len(neighboors_sets)):
                            corrosion_sets[neighboors_sets[0]] += corrosion_sets[neighboors_sets[w]]
                            corrosion_sets.remove(corrosion_sets[neighboors_sets[w]])
                            s = s-1
        corrosion_sets.remove([])
        return corrosion_sets


    def createOccupancyGrid(self,data, threshold):
        grid = np.zeros(data.shape)
        for j in range(data.shape[1]):
            for i in range(data.shape[0]):
                if data[i,j] <= threshold and data[i,j] > 0.0:
                    grid[i,j] = 1
                else:
                    grid[i,j] = 0
        return grid