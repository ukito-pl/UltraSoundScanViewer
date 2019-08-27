from PyQt4.QtCore import QThread,SIGNAL
import numpy as np
from Miscellaneous import ReportTools

class WeldDetector(QThread):

    def __init__(self, data):
        QThread.__init__(self)
        self.thicknessData = data
    def __del__(self):
        self.wait()

    def run(self):
        map = self.evalMap2(self.thicknessData)
        #segments = self.findSegments(map)
        vwelds = self.findWeldsVertical(map)
        hwelds = self.findWeldsHorizontal(map, vwelds)

    def findWeldsVertical(self, map):
        width = 10
        welds = []
        j = 0
        while j < map.shape[1]:
            if map[-2, j] == 255:
                # print "szuaknie:", j,edge_map.shape[1]
                area = map[:, int(j-width/2):int(j+width/2)]
                count = 0
                for row in area:
                    for element in row:
                        if element == 255:
                            count = count + 1

                area_size = area.shape[0]*area.shape[1]
                percentage = float(count)/area_size
                #print "pr:", percentage, count, area_size
                if percentage > 0.5:
                    #print "znaleziono spojenie: ", weld_segment
                    name = "Spoina obwodowa#" + (len(welds)).__str__()
                    self.emit(SIGNAL('weldDetected(PyQt_PyObject)'), [name, ReportTools.SP, j])
                    welds.append(j)
                    j = j + width
            j = j + 1
        return welds

    def findWeldsHorizontal(self,map,vwelds):
        width = 10
        hwelds = []

        for j in range(0,len(vwelds)-1):
            local_welds = []
            for i in range(int(width/2),map.shape[0] - int(width/2)):
                if map[i,vwelds[j]] == 255:
                    # print "szuaknie:", j,edge_map.shape[1]
                    area = map[int(i - width/2):int(i + width/2), vwelds[j]:vwelds[j+1]]
                    count = 0
                    for row in area:
                        for element in row:
                            if element == 255:
                                count = count + 1

                    area_size = area.shape[0] * area.shape[1]
                    percentage = float(count) / area_size
                    #print "pr:", percentage, count, area_size
                    if percentage > 0.4:
                        # print "znaleziono spojenie: ", weld_segment
                        #name = "Spoina wzdluzna#" + (len(hwelds)).__str__()
                        #self.emit(SIGNAL('weldDetected(PyQt_PyObject)'), [name, ReportTools.SW, i, vwelds[j], vwelds[j+1]-vwelds[j] ])
                        local_welds.append([i,percentage])
            if len(local_welds) > 0:
                maxpr = 0
                for weld in local_welds:
                    if weld[1] > maxpr:
                        maxpr=weld[1]
                        i_max = weld[0]
                hwelds.append(i_max)
                name = "Spoina wzdluzna#" + (len(hwelds)).__str__()
                self.emit(SIGNAL('weldDetected(PyQt_PyObject)'), [name, ReportTools.SW, i_max, vwelds[j], vwelds[j+1]-vwelds[j] ])

        return hwelds

    def evalMap2(self,data):
        map = np.zeros(data.shape)
        for i in range(0, data.shape[0]):
            for j in range(0, data.shape[1]):
                if data[i,j] == 255:
                    map[i, j] = 255
        return map


    def evalMap1(self,data):
        h = np.histogram(data, bins=256, range=(0, 255))
        hist = h[0]
        print hist.shape
        cdf = np.zeros((256))
        cdf_min = 0
        for i in range(0, 256):

            cdf[i] = float(np.sum(hist[1:i]) / float(np.sum(hist[1:254])))
            if cdf[i] != 0 and cdf_min == 0:
                cdf_min = cdf[i]
                print cdf_min
        print cdf
        LUT = np.zeros((256))
        for i in range(0, 256):
            LUT[i] = (cdf[i] - cdf_min) / (1 - cdf_min) * 255
        for i in range(0, data.shape[0]):
            for j in range(0, data.shape[1]):
                data[i, j] = LUT[data[i, j]]
        gradient = self.evalGradient(data)

        N = 0
        sum = 0
        for m in range(1, gradient.shape[0] - 1):
            for n in range(1, gradient.shape[1] - 1):
                sum = sum + gradient[m, n]
                N = N + 1
        avg = sum / N

        for i in range(0, gradient.shape[0] - 1):
            for j in range(0, gradient.shape[1] - 1):
                if gradient[i, j] > (2.0 * avg):
                    gradient[i, j] = 255
                else:
                    gradient[i, j] = 0

        edge_map = gradient
        return edge_map

    def evalGradient(self, data):
        gradient = np.zeros(data.shape)
        mask_fx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        mask_fy = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        mask_fx = np.array([[0, 1], [-1, 0]])
        mask_fy = np.array([[1, 0], [0, -1]])
        max = 0
        for m in range(0, gradient.shape[0] - 1):
            for n in range(0, gradient.shape[1] - 1):
                fx = 0.0
                fy = 0.0
                for i in [0, 1]:
                    for j in [0, 1]:
                        fx = fx + data[m + i, n + j] * mask_fx[i, j]
                        fy = fy + data[m + i, n + j] * mask_fy[i, j]
                gradient[m, n] = 1.0 / 4.0 * (fx * fx + fy * fy)
                if gradient[m, n] > max:
                    max = gradient[m, n]

        for i in range(0, gradient.shape[0]):
            for j in range(0, gradient.shape[1]):
                gradient[i, j] = int(gradient[i, j] / max * 255)
        return gradient

    def findSegments(self, map):
        width = 20
        segments = []
        j = 0
        while j < map.shape[1]:
            if map[-2, j] == 255:
                #print "szuaknie:", j,edge_map.shape[1]
                weld_segment = self.checkWeld(map, map.shape[0] - 2, j, 0, width)
                if weld_segment != False:
                    print "znaleziono spojenie: ", weld_segment
                    name = "Spoina obwodowa#" + (len(segments)).__str__()
                    self.emit(SIGNAL('weldDetected(PyQt_PyObject)'), [name,j])
                    segments.append(weld_segment)
                    j = j + width
            j = j + 1
        return segments

    def checkWeld(self, map, origin_i, origin_j, dest_i, width):
        width = width/2
        i = origin_i
        j = origin_j
        open_list = []  # do odwiedzenia
        weld = [[i, j]]  # odwiedzone, dodane do "spoiny"
        previous_nodes = []
        end = False
        while not end:
            for m in [i - 1, i, i + 1]:
                for n in [j - 1, j, j + 1]:
                    if m > map.shape[0] - 1:
                        m = map.shape[0] - 1
                    if n > map.shape[1] - 1:
                        n = map.shape[1] - 1
                    if n < 0:
                        n = 0
                    if m < 0:
                        m = 0
                    if m != i or n != j:

                        if not open_list.__contains__([m, n]) and not weld.__contains__([m, n]) and abs(n - origin_j) <= 10:
                            if map[m, n] == 255:
                                open_list.append([m, n])
            if open_list == []:
                return False
            new_node = open_list.pop(-1)
            i = new_node[0]
            j = new_node[1]
            weld.append(new_node)
            if i == dest_i and abs(j - origin_j) <= width:
                end = True
        return weld