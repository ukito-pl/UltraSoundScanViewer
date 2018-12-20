from PyQt4.QtCore import QThread,SIGNAL
import numpy as np
import colorsys

class LoadScansThread(QThread):

    def __init__(self, file_dir, start_frame, end_frame):
        QThread.__init__(self)
        self.base_file_dir = file_dir        #directory of a base file i.e. F0000000.800
        #frame variables
        self.data_frame_length = 517    #in bytes
        self.data_length = 256          #
        self.start_byte = 261           #

        #scan variables
        self.start_frame = start_frame
        self.end_frame = end_frame

        f = open(self.base_file_dir, "rb")
        f.seek(0, 2)
        size = f.tell()
        self.frames_in_file = size / self.data_frame_length
        print "frames: ", self.frames_in_file
        f.close()
    def __del__(self):
        self.wait()

    def run(self):
        img = np.ones((self.data_length, self.end_frame - self.start_frame + 1, 3), dtype=np.uint8)
        end_file_index = (self.end_frame/self.frames_in_file).__int__()
        end_file_frames_to_get =  self.end_frame - end_file_index*self.frames_in_file + 1
        start_file_index =  (self.start_frame/self.frames_in_file).__int__()
        start_file_frames_to_get =  self.frames_in_file - (self.start_frame - start_file_index*self.frames_in_file)
        it = 0
        it2 = 0
        print start_file_index, start_file_frames_to_get
        print end_file_index, end_file_frames_to_get
        for i in range(start_file_index,end_file_index+1):

            dir = self.base_file_dir.split('.')
            file_dir = dir[0][0:len(dir[0]) - 7] + i.__str__().zfill((7)) + '.' + dir[1]
            print file_dir

            f = open(file_dir, "rb")

            if (end_file_index==start_file_index):
                count = self.end_frame - self.start_frame + 1
            elif (i == start_file_index):
                f.seek((self.start_frame - start_file_index*self.frames_in_file) * self.data_frame_length, 0)
                count = start_file_frames_to_get
            elif (i == end_file_index):
                count = start_file_frames_to_get + (it2-1)*self.frames_in_file + end_file_frames_to_get
            elif (i > start_file_index and i < end_file_index):
                count = start_file_frames_to_get + (it2) * self.frames_in_file
            print count
            while ( it < count):
                f.seek(self.start_byte,1)
                f1 = f.read(self.data_length)
                b = bytearray()
                b.extend(f1)
                img[:,it,0] = b
                img[:, it, 1] = b
                img[:, it, 2] = b
                it = it + 1
            f.close()

            it2 = it2 + 1


        self.emit(SIGNAL('showImage(PyQt_PyObject)'), img)