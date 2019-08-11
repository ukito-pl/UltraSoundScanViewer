from PyQt4.QtCore import QThread,SIGNAL
import numpy as np
import pyqtgraph.opengl as gl
from math import sqrt,cos,pi

class Create3dScanThread(QThread):

    def __init__(self,dataPerFrame,deltaX, diameter, nominal_distance,startFrame,a,b,distArray,imgScanColored, x_start,x_end,smooth,shaded,w):
        QThread.__init__(self)
        self.dataPerFrame = dataPerFrame
        self.deltaX = deltaX
        self.diameter = diameter
        self.startFrame = startFrame
        self.a = a
        self.b = b
        self.distArray = distArray
        self.imgScanColored = imgScanColored
        self.x_start = x_start
        self.x_end = x_end
        self.smooth = smooth
        self.shaded = shaded
        self.standOff = nominal_distance
        self.w = w

    def __del__(self):
        self.wait()

    def run(self):
        items = []
        N = self.dataPerFrame
        length = (self.x_end - self.x_start) * 1000.0  # in millimeters
        L = int(length / self.deltaX)
        r = 1  # in scene coordinates
        nominal_r_mm = self.diameter / 2
        r_base = self.diameter - self.standOff  # mm
        y_base = int(self.x_start / (self.deltaX / 1000.0) - self.startFrame)
        l = float(length / nominal_r_mm * r)
        phi = np.linspace(0, 2 * pi, N)
        x = np.zeros((N, 1))
        y = np.linspace(0, l, L)
        z = np.zeros((N, L))

        verts = np.zeros((L * len(x), 3))
        faces = np.zeros((2 * L * len(x) - L, 3), dtype=np.int32)
        colors = np.ones((L * len(x), 4))
        v = 0  # vertex counter
        f = 0  # faces counter
        for i in range(0, N + 1):
            for j in range(len(y)):
                if i < N:
                    dval = self.a * self.distArray[i, y_base + j] + self.b
                    r_mm = r_base + dval + (dval - self.standOff )*(self.w-1)
                    r = float(r_mm / nominal_r_mm)
                    x[i] = r * cos(phi[i])

                    if i < N / 2:
                        z[i, j] = - sqrt(abs(r * r - x[i] * x[i]))
                    else:
                        z[i, j] = sqrt(abs(r * r - x[i] * x[i]))
                    ######################
                    verts[v, :] = [x[i], y[j], z[i, j]]
                    colors[v, 0:3] = [(float(w) / 255) for w in self.imgScanColored[i, y_base + j]]
                    if i > 0 and j > 0 and j < L - 1:
                        if self.distArray[i, y_base + j] < 255 and self.distArray[i, y_base + j - 1] < 255 and \
                                self.distArray[i - 1, y_base + j] < 255:
                            faces[f, :] = [v, v - 1, v - L]
                            f = f + 1
                        elif self.distArray[i, y_base + j] < 255 and self.distArray[i - 1, y_base + j] < 255 and \
                                self.distArray[i - 1, y_base + j - 1] < 255:
                            faces[f, :] = [v, v - L, v - L - 1]
                            f = f + 1
                        if self.distArray[i, y_base + j] < 255 and self.distArray[i - 1, y_base + j] < 255 and \
                                self.distArray[i - 1, y_base + j + 1] < 255:
                            faces[f, :] = [v, v - L, v - L + 1]
                            f = f + 1
                        elif self.distArray[i, y_base + j] < 255 and self.distArray[i - 1, y_base + j] < 255 and \
                                self.distArray[i, y_base + j + 1] < 255:
                            faces[f, :] = [v, v - L, v + 1]
                            f = f + 1
                    elif i > 0 and j == 0:
                        if self.distArray[i, y_base + j] < 255 and self.distArray[i - 1, y_base + j] < 255 and \
                                self.distArray[i - 1, y_base + j + 1] < 255:
                            faces[f, :] = [v, v - L, v - L + 1]
                            f = f + 1
                        elif self.distArray[i, y_base + j] < 255 and self.distArray[i - 1, y_base + j] < 255 and \
                                self.distArray[i, y_base + j + 1] < 255:
                            faces[f, :] = [v, v - L, v + 1]
                            f = f + 1
                    elif i > 0 and j == L - 1:
                        if self.distArray[i, y_base + j] < 255 and self.distArray[i, y_base + j - 1] < 255 and \
                                self.distArray[i - 1, y_base + j] < 255:
                            faces[f, :] = [v, v - L, v - 1]
                            f = f + 1
                        elif self.distArray[i, y_base + j] < 255 and self.distArray[i - 1, y_base + j] < 255 and \
                                self.distArray[i - 1, y_base + j - 1] < 255:
                            faces[f, :] = [v, v - L, v - L - 1]
                            f = f + 1
                elif i == N:
                    if j > 0 and j < L - 1:
                        if self.distArray[0, y_base + j] < 255 and self.distArray[0, y_base + j - 1] < 255 and \
                                self.distArray[N - 1, y_base + j] < 255:
                            faces[f, :] = [j, j - 1, v - L]
                            f = f + 1
                        elif self.distArray[0, y_base + j] < 255 and self.distArray[N - 1, y_base + j] < 255 and \
                                self.distArray[N - 1, y_base + j - 1] < 255:
                            faces[f, :] = [j, v - L, v - L - 1]
                            f = f + 1
                        if self.distArray[0, y_base + j] < 255 and self.distArray[N - 1, y_base + j] < 255 and \
                                self.distArray[N - 1, y_base + j + 1] < 255:
                            faces[f, :] = [j, v - L, v - L + 1]
                            f = f + 1
                        elif self.distArray[0, y_base + j] < 255 and self.distArray[N - 1, y_base + j] < 255 and \
                                self.distArray[0, y_base + j + 1] < 255:
                            faces[f, :] = [j, v - L, j + 1]
                            f = f + 1
                    elif j == 0:
                        if self.distArray[0, y_base + j] < 255 and self.distArray[N - 1, y_base + j] < 255 and \
                                self.distArray[N - 1, y_base + j + 1] < 255:
                            faces[f, :] = [j, v - L, v - L + 1]
                            f = f + 1
                        elif self.distArray[0, y_base + j] < 255 and self.distArray[N - 1, y_base + j] < 255 and \
                                self.distArray[0, y_base + j + 1] < 255:
                            faces[f, :] = [j, v - L, j + 1]
                            f = f + 1
                    elif j == L - 1:
                        if self.distArray[0, y_base + j] < 255 and self.distArray[0, y_base + j - 1] < 255 and \
                                self.distArray[N - 1, y_base + j] < 255:
                            faces[f, :] = [j, v - L, j - 1]
                            f = f + 1
                        elif self.distArray[0, y_base + j] < 255 and self.distArray[N - 1, y_base + j] < 255 and \
                                self.distArray[N - 1, y_base + j - 1] < 255:
                            faces[f, :] = [j, v - L, v - L - 1]
                            f = f + 1
                v = v + 1

        if self.smooth:
            m1 = gl.GLMeshItem(vertexes=verts, faces=faces, vertexColors=colors, smooth=True)
        else:
            m1 = gl.GLMeshItem(vertexes=verts, faces=faces, vertexColors=colors, smooth=False)
        if self.shaded:
            m1.setShader('shaded')
        print v, f
        items.append(m1)
        self.emit(SIGNAL('3dScanCreated(PyQt_PyObject)'), items)

