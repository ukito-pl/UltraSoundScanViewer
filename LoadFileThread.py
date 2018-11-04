from PyQt4.QtCore import QThread,SIGNAL
import numpy as np
import colorsys

class LoadFileThread(QThread):

    def __init__(self, file_dir):
        QThread.__init__(self)
        self.file_dir = file_dir
    def __del__(self):
        self.wait()

    def run(self):
        f = open(self.file_dir, "rb")
        f.seek(0, 2)
        size = f.tell()
        print size
        img = np.ones((192, size / 396, 3), dtype=np.uint8)
        f.seek(0, 0)
        it = 0
        while (it < size / 396):
            f1 = f.read(396)
            i = 0
            for byte in f1:
                if (i >= 204):
                    #c = ord(byte)/256.0
                    #color = colorsys.hsv_to_rgb(0.0, 1.0, c)
                    #img[i - 204, it] = [color[0]*255,color[1]*255, color[2]*255]
                    img[i - 204, it] = [ord(byte), ord(byte),ord(byte)]
                i = i + 1
                # print ord(byte)
            # print it
            it = it + 1
        self.emit(SIGNAL('showImage(PyQt_PyObject)'), img)