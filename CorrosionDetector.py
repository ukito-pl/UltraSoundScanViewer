from PyQt4.QtCore import QThread,SIGNAL
import numpy as np
from Miscellaneous import ReportTools
from math import sqrt
from Miscellaneous import isclose
#import pydevd

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
        percentage_ref = 0.4
        filtered_corrosions = []
        nb = self.thicknessDataRaw.shape[0]*self.thicknessDataRaw.shape[1]

        potential_corrosions = self.findCorrosions(self.thicknessDataRaw,self.treshold)
        for corrosion in potential_corrosions:
            count = 0
            boundry = []
            for pixel in corrosion:
                i = pixel[0]
                j = pixel[1]
                for m in range(j - 1, j + 2):
                    for n in range(i - 1, i + 2):
                        if n > self.thicknessDataRaw.shape[0] - 1:
                            n = self.thicknessDataRaw.shape[0] - 1
                        if m > self.thicknessDataRaw.shape[1] - 1:
                            m = self.thicknessDataRaw.shape[1] - 1
                        if n < 0:
                            n = 0
                        if m < 0:
                            m = 0
                        if not [n,m] in corrosion and not [n,m] in boundry:
                            if self.thicknessDataRaw[n,m] == 255:
                                count = count +1
                            boundry.append([n,m])
            percentage = float(count)/len(boundry)
            if percentage <= percentage_ref:
                filtered_corrosions.append(corrosion)

        #find surrounding welds
        left_weld = -1
        right_weld = -1
        horizontal_weld = -1
        c = 0
        for corrosion in filtered_corrosions:
            [max_i, min_i, max_j, min_j] = self.checkBoundries(corrosion)
            i = min_i + (max_i - min_i) / 2
            j = min_j + (max_j - min_j) / 2
            if not (left_weld <= i <= right_weld):
                left_weld = -1
                right_weld = -1
                horizontal_weld = -1
            if left_weld == -1 and right_weld == -1 and horizontal_weld == -1:
                left_weld = self.findLeftVWeld(int(j))
                right_weld = self.findRightVWeld(int(j))
                if left_weld != None and right_weld != None:
                    horizontal_weld = self.findHorizontalWeld(left_weld,right_weld)
                else:
                    horizontal_weld = None
            if not(min_i <= horizontal_weld <= max_i) and not(min_j < left_weld < max_j) and not(
                    min_j < right_weld < max_j):
                name = "Korozja#" + c.__str__()
                self.emit(SIGNAL('corrosionDetected(PyQt_PyObject)'), [name, ReportTools.K, i, j, percentage])
                c = c + 1




    def findHorizontalWeld(self,left_weld, right_weld):
        width = self.weldWidthH
        percentage_ref = self.percentageH
        local_welds = []
        for i in range(int(width / 2), self.thicknessDataRaw.shape[0] - int(width / 2)):
            if self.thicknessDataRaw[i, left_weld] == 255:
                # print "szuaknie:", j,edge_map.shape[1]
                area = self.thicknessDataRaw[int(i - width / 2):int(i + width / 2), left_weld:right_weld]
                count = 0
                for row in area:
                    for element in row:
                        if element == 255:
                            count = count + 1

                area_size = area.shape[0] * area.shape[1]
                percentage = float(count) / area_size
                if percentage > percentage_ref:
                    local_welds.append([i, percentage])
        if len(local_welds) > 0:
            maxpr = 0
            for weld in local_welds:
                if weld[1] > maxpr:
                    maxpr = weld[1]
                    i_max = weld[0]
            var_max = 0
            i_var_max = i_max
            for n in range(0, area.shape[0] - 1):
                var = self.evalVariance(self.thicknessData[i_var_max + n, :])
                if var > var_max:
                    var_max = var
                    i_var_max = i_max + n
            return i_var_max

    def findLeftVWeld(self,begining):
        percentage_ref = self.percentageV
        width = self.weldWidthV
        max_percentage = 0
        max_percentage_j = 0
        weld_detected = False
        j = begining
        while j > 0 + width:
            if (self.thicknessDataRaw[-2, j] == 255) or weld_detected:
                # print "szuaknie:", j,edge_map.shape[1]
                area = self.thicknessDataRaw[:, j - width:j]
                count = 0
                for row in area:
                    for element in row:
                        if element == 255:
                            count = count + 1
                area_size = area.shape[0] * area.shape[1]
                percentage = float(count) / area_size
                if percentage >= percentage_ref and not weld_detected:
                    weld_detected = True
                    max_percentage = percentage
                    max_percentage_j = j
                elif percentage >= percentage_ref and weld_detected:
                    if percentage > max_percentage:
                        max_percentage = percentage
                        max_percentage_j = j
                elif percentage < percentage_ref and weld_detected:
                    weld_detected = False
                    var_max = 0
                    j_var_max = max_percentage_j
                    for m in range(0, area.shape[1] - 1):
                        var = self.evalVariance(self.thicknessData[:, max_percentage_j + m])
                        if var > var_max:
                            var_max = var
                            j_var_max = max_percentage_j + m
                    return j_var_max
            j = j - 1

    def findRightVWeld(self,begining):
        percentage_ref = self.percentageV
        width = self.weldWidthV
        max_percentage = 0
        max_percentage_j = 0
        weld_detected = False
        j = begining
        while j < self.thicknessDataRaw.shape[1] - width:
            if self.thicknessDataRaw[-2, j] == 255 or weld_detected:
                # print "szuaknie:", j,edge_map.shape[1]
                area = self.thicknessDataRaw[:, j:j + width]
                count = 0
                for row in area:
                    for element in row:
                        if element == 255:
                            count = count + 1
                area_size = area.shape[0] * area.shape[1]
                percentage = float(count) / area_size
                if percentage >= percentage_ref and not weld_detected:
                    weld_detected = True
                    max_percentage = percentage
                    max_percentage_j = j
                elif percentage >= percentage_ref and weld_detected:
                    if percentage > max_percentage:
                        max_percentage = percentage
                        max_percentage_j = j
                elif percentage < percentage_ref and weld_detected:
                    weld_detected = False
                    var_max = 0
                    j_var_max = max_percentage_j
                    for m in range(0, area.shape[1] - 1):
                        var = self.evalVariance(self.thicknessData[:, max_percentage_j + m])
                        if var > var_max:
                            var_max = var
                            j_var_max = max_percentage_j + m
                    return j_var_max
            j = j + 1

    def checkBoundries(self, data):
        max_i = data[0][0]
        min_i = data[0][0]
        max_j = data[0][1]
        min_j = data[0][1]
        for element in data:
            if element[0] > max_i:
                max_i = element[0]
            elif element[0] < min_i:
                min_i = element[0]
            if element[1] > max_j:
                max_j = element[1]
            elif element[1] < min_j:
                min_j = element[1]
        return [max_i,min_i,max_j,min_j]

    def findCorrosions(self, data, treshold_perc):
        sum = 0
        nb = 0
        for n in range(0, data.shape[0] - 1):
            for m in range(0, 200):
                if n > data.shape[0] - 1:
                    n = data.shape[0] - 1
                if m > data.shape[1] - 1:
                    m = data.shape[1] - 1
                if data[n, m] != 0 and data[n, m] != 255:
                    sum = sum + data[n, m]
                    nb = nb + 1
        avg = float(sum) / nb
        treshold_val = avg * treshold_perc
        print treshold_val

        corrosion_points = []
        false_corrosion_points = []
        corrosions = []
        treshold_refresh = 200
        treshold_refresh_cnt = 0
        for j in range(data.shape[1]):
            if treshold_refresh_cnt > treshold_refresh:
                treshold_refresh_cnt = 0
                sum = 0
                nb = 0
                for n in range(0,data.shape[0]-1):
                    for m in range(0,200):
                        m = j+ m
                        if n > data.shape[0] - 1:
                            n = data.shape[0] - 1
                        if m > data.shape[1] - 1:
                            m = data.shape[1] - 1
                        if data[n,m] != 0 and data[n,m] != 255:
                            sum = sum + data[n,m]
                            nb = nb + 1
                avg = float(sum) / nb
                treshold_val = avg * treshold_perc
                print treshold_val

            for i in range(data.shape[0]):
                if not [i,j] in corrosion_points and not [i,j] in false_corrosion_points:
                    if data[i, j] <= treshold_val and data[i, j] > 0.0:
                        area, is_corrosion = self.checkCorrosion(data,i,j,treshold_val)
                        if is_corrosion:
                            #print area
                            for point in area:
                                corrosion_points.append(point)
                            corrosions.append(area)

                        else:
                            for point in area:
                                false_corrosion_points.append(point)
            treshold_refresh_cnt = treshold_refresh_cnt + 1
        return corrosions

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
                    if not [n,m] in corrosion and not [n,m] in open_list:
                        if data[n, m] <= treshold_val and data[n, m] > 0.0:
                            open_list.append([n,m])
            if len(open_list) > 0:
                point = open_list.pop(0)
                i = point[0]
                j = point[1]
            else:
                end = True
            #print len(open_list), len(corrosion), data.shape[0]*data.shape[1], end
        L_measured = self.measureL(corrosion,self.dx)
        d = self.findDepthOfCorrosion(self.thicknessData,corrosion,self.nominalThickness)
        L_eval = self.evaluateL(self.diameter,self.nominalThickness,d)
        if L_measured > 0.7*L_eval:
            return corrosion, True
        else:
            return corrosion, False

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

    def evalVariance(self,data):
        sum = data.sum()
        n = len(data)
        avg = float(sum/n)
        sum_var = 0
        for element in data:
            sum_var = sum_var + pow((element - avg),2)
        var = float(sum_var/n)
        return var