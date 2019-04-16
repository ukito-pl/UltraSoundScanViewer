# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtCore import  SIGNAL
import numpy as np
from math import sqrt
import TestWindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
import matplotlib
import matplotlib.pyplot as plt

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class TestDialog(QtGui.QDialog, TestWindow.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.thicknessRawData = []
        self.pixItem = QtGui.QGraphicsPixmapItem()
        self.pixItem2 = QtGui.QGraphicsPixmapItem()
        self.connect(self.pushButton,SIGNAL('clicked()'),self.process)

    def setData(self,thickness_raw_data, aspect_ratio):
        self.thicknessRawData = thickness_raw_data
        self.aspectRatio = aspect_ratio
        self.showData(self.thicknessRawData)

    def showImage(self,qimage):
        self.scene = QtGui.QGraphicsScene()
        pix1 = QtGui.QPixmap(qimage)
        self.pixItem = QtGui.QGraphicsPixmapItem(pix1)
        self.pixItem.scale(1, self.aspectRatio)
        self.scene.addItem(self.pixItem)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.fitInView(self.pixItem, QtCore.Qt.KeepAspectRatio)

    def showData(self,data):
        img = np.array(data,dtype=np.uint8)
        image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1], QtGui.QImage.Format_Indexed8)
        self.scene = QtGui.QGraphicsScene()
        pix1 = QtGui.QPixmap(image)
        self.pixItem = QtGui.QGraphicsPixmapItem(pix1)
        self.pixItem.scale(1, self.aspectRatio)
        self.scene.addItem(self.pixItem)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.fitInView(self.pixItem, QtCore.Qt.KeepAspectRatio)

    def showData2(self,data):
        img = np.array(data,dtype=np.uint8)
        image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1], QtGui.QImage.Format_Indexed8)
        self.scene2 = QtGui.QGraphicsScene()
        pix1 = QtGui.QPixmap(image)
        self.pixItem2 = QtGui.QGraphicsPixmapItem(pix1)
        self.pixItem2.scale(1, self.aspectRatio)
        self.scene2.addItem(self.pixItem2)
        self.graphicsView_2.setScene(self.scene2)
        self.graphicsView_2.fitInView(self.pixItem2, QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, QResizeEvent):
        super(self.__class__,self).resizeEvent(QResizeEvent)
        self.graphicsView.fitInView(self.pixItem,QtCore.Qt.KeepAspectRatio)
        self.graphicsView_2.fitInView(self.pixItem2, QtCore.Qt.KeepAspectRatio)

    def process(self):
        data = np.array(self.thicknessRawData)
        #self.histogram(data)
        for i in range(0,data.shape[0]):
            for j in range(0,data.shape[1]):
                if data[i,j] < 54:
                    data[i,j] = 0
                elif data[i,j]> 54 and data[i,j] < 75:
                    data[i,j] = int(255/21*(data[i,j] - 54))
                else:
                    data[i, j] = 255
        #self.histogram(data)
        self.showData(data)
        gradient = self.evalGradient(data)

        N = 0
        sum = 0
        for m in range(1, gradient.shape[0] - 1):
            for n in range(1, gradient.shape[1] - 1):
                sum = sum + gradient[m, n]
                N = N + 1
        avg = sum / N

        for i in range(0,gradient.shape[0]-1):
            for j in range(0,gradient.shape[1]-1):
                if gradient[i, j] > (0.4*avg):
                        gradient[i,j] = 255
                else:
                        gradient[i,j] = 0

        edge_map = gradient
        segments = self.findSegments(edge_map)
        self.showData2(gradient)

    def histogram(self,data):

        plt.hist(data)
        plt.show()

    def evalGradient(self,data):
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

    def findSegments(self,edge_map):
        segments = []
        j = 0
        while j < edge_map.shape[1]:
            if edge_map[-2,j] == 255:
                weld_segment = self.checkWeld(edge_map,edge_map.shape[0]-2, j, 0)
                if weld_segment != False:
                    print "znaleziono spojenie: ",weld_segment
                    segments.append(weld_segment)
                    j = j + 20
            j = j + 1
        return segments

    def checkWeld(self,edge_map,origin_i,origin_j, dest_i):
        i = origin_i
        j = origin_j
        open_list = [] #do odwiedzenia
        weld = [[i,j]] #odwiedzone, dodane do "spoiny"
        previous_nodes = []
        end = False
        while not end:
            for m in [i-1,i,i+1]:
                for n in [j-1,j,j+1]:
                    if m > edge_map.shape[0] - 1:
                        m = edge_map.shape[0] - 1
                    if n > edge_map.shape[1] - 1:
                        n = edge_map.shape[1] - 1
                    if n < 0:
                        n = 0
                    if m < 0:
                        m = 0
                    if m!= i or n != j:

                        if not open_list.__contains__([m,n]) and not weld.__contains__([m,n]):
                            if edge_map[m,n] == 255:
                                open_list.append([m,n])
            if open_list == []:
                return False
            new_node = open_list.pop(-1)
            i = new_node[0]
            j = new_node[1]
            weld.append(new_node)
            if i == dest_i and abs(j - origin_j) < 20:
                end = True
        return weld