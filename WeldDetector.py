from PyQt4.QtCore import QThread,SIGNAL
import numpy as np

class WeldDetector(QThread):

    def __init__(self, data):
        QThread.__init__(self)
        self.thicknessData = data
    def __del__(self):
        self.wait()

    def run(self):
        weld_data = ['weld',1]
        for i in range(0, self.thicknessData.shape[0]):
            for j in range(0, self.thicknessData.shape[1]):
                if self.thicknessData[i, j] < 54:
                    self.thicknessData[i, j] = 0
                elif self.thicknessData[i, j] > 54 and self.thicknessData[i, j] < 75:
                    self.thicknessData[i, j] = int(255 / 21 * (self.thicknessData[i, j] - 54))
                else:
                    self.thicknessData[i, j] = 255
        gradient = self.evalGradient(self.thicknessData)

        N = 0
        sum = 0
        for m in range(1, gradient.shape[0] - 1):
            for n in range(1, gradient.shape[1] - 1):
                sum = sum + gradient[m, n]
                N = N + 1
        avg = sum / N

        for i in range(0, gradient.shape[0] - 1):
            for j in range(0, gradient.shape[1] - 1):
                if gradient[i, j] > (0.4 * avg):
                    gradient[i, j] = 255
                else:
                    gradient[i, j] = 0

        edge_map = gradient
        segments = self.findSegments(edge_map)

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

    def findSegments(self, edge_map):
        segments = []
        j = 0
        while j < edge_map.shape[1]:
            if edge_map[-2, j] == 255:
                weld_segment = self.checkWeld(edge_map, edge_map.shape[0] - 2, j, 0)
                if weld_segment != False:
                    print "znaleziono spojenie: ", weld_segment
                    name = "Spoina obwodowa#" + (len(segments)).__str__()
                    self.emit(SIGNAL('weldDetected(PyQt_PyObject)'), [name,j])
                    segments.append(weld_segment)
                    j = j + 20
            j = j + 1
        return segments

    def checkWeld(self, edge_map, origin_i, origin_j, dest_i):
        i = origin_i
        j = origin_j
        open_list = []  # do odwiedzenia
        weld = [[i, j]]  # odwiedzone, dodane do "spoiny"
        previous_nodes = []
        end = False
        while not end:
            for m in [i - 1, i, i + 1]:
                for n in [j - 1, j, j + 1]:
                    if m > edge_map.shape[0] - 1:
                        m = edge_map.shape[0] - 1
                    if n > edge_map.shape[1] - 1:
                        n = edge_map.shape[1] - 1
                    if n < 0:
                        n = 0
                    if m < 0:
                        m = 0
                    if m != i or n != j:

                        if not open_list.__contains__([m, n]) and not weld.__contains__([m, n]):
                            if edge_map[m, n] == 255:
                                open_list.append([m, n])
            if open_list == []:
                return False
            new_node = open_list.pop(-1)
            i = new_node[0]
            j = new_node[1]
            weld.append(new_node)
            if i == dest_i and abs(j - origin_j) < 20:
                end = True
        return weld