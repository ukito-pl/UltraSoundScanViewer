from PyQt4.QtCore import QThread,SIGNAL
import numpy as np
import string

class LoadScansThread(QThread):

    def __init__(self, file_dir, start_frame, end_frame, bd0,bd1,bt0,bt1,frame_length):
        QThread.__init__(self)
        self.base_file_dir = file_dir        #directory of a base file i.e. F0000000.800
        self.nb_of_digits = 0
        filename = self.base_file_dir.split("/")[-1].split(".")[0]
        for i in range(0,filename.__len__()):
            if string.digits.__contains__(filename[-i-1]):
                self.nb_of_digits = self.nb_of_digits + 1
            elif string.letters.__contains__((filename[-i-1])):
                break
        print self.nb_of_digits
        #frame variables
        self.data_frame_length = frame_length    #in bytes
        self.data_length = bt1-bt0 + 1          #
        self.start_byte_thick = bt0           #
        self.end_byte_thick = bt1
        self.start_byte_dist = bd0
        self.end_byte_dist = bd1
        #scan variables
        f = open(self.base_file_dir, "rb")
        f.seek(0, 2)
        size = f.tell()
        self.frames_in_file = size / self.data_frame_length
        f.close()
        if start_frame < 0:
            self.start_frame = 0
        else:
            self.start_frame = start_frame

        if end_frame < 0 or end_frame > self.maxEndFrame():
            self.end_frame = self.maxEndFrame()
        else:
            self.end_frame = end_frame


    def __del__(self):
        self.wait()

    def maxEndFrame(self):
        end_frame = 0
        i = 0
        file_exists = True
        while file_exists:
            dir = self.base_file_dir.split('.')
            file_dir = dir[0][0:len(dir[0]) - self.nb_of_digits] + i.__str__().zfill((self.nb_of_digits)) + '.' + dir[1]
            try:
                f = open(file_dir, "rb")
            except:
                file_exists = False
                #print "cannot open file", file_dir
            if file_exists:
                f.seek(0, 2)
                size = f.tell()
                frames_in_file = size / self.data_frame_length
                end_frame = end_frame + frames_in_file
                f.close()
            else:
                end_frame = end_frame - 1
            i = i + 1
        return end_frame

    def run(self):
        #print "run thread"
        print self.start_frame, self.end_frame
        img = np.ones((self.data_length, self.end_frame - self.start_frame + 1), dtype=np.uint8)
        dist = np.ones((self.data_length, self.end_frame - self.start_frame + 1), dtype=np.uint8)
        end_file_index = (self.end_frame/self.frames_in_file).__int__()
        end_file_frames_to_get =  self.end_frame - end_file_index*self.frames_in_file + 1
        start_file_index =  (self.start_frame/self.frames_in_file).__int__()
        start_file_frames_to_get =  self.frames_in_file - (self.start_frame - start_file_index*self.frames_in_file)
        it = 0
        it2 = 0
        #print start_file_index, start_file_frames_to_get
        #print end_file_index, end_file_frames_to_get
        for i in range(start_file_index,end_file_index+1):

            dir = self.base_file_dir.split('.')
            file_dir = dir[0][0:len(dir[0]) - self.nb_of_digits] + i.__str__().zfill((self.nb_of_digits)) + '.' + dir[1]

            f = open(file_dir, "rb")

            if (end_file_index==start_file_index):
                count = self.end_frame - self.start_frame + 1
                f.seek((self.start_frame - i*self.frames_in_file) * self.data_frame_length, 0)
            elif (i == start_file_index):
                f.seek((self.start_frame - start_file_index*self.frames_in_file) * self.data_frame_length, 0)
                count = start_file_frames_to_get
            elif (i == end_file_index):
                count = start_file_frames_to_get + (it2-1)*self.frames_in_file + end_file_frames_to_get
            elif (i > start_file_index and i < end_file_index):
                count = start_file_frames_to_get + (it2) * self.frames_in_file
            #print it, count
            while ( it < count):
                f.seek(self.start_byte_dist, 1)
                #print f.tell()
                f1 = f.read(self.data_length)
                b = bytearray()
                b.extend(f1)
                dist[:, it] = b

                f1 = f.read(self.data_length)
                b = bytearray()
                b.extend(f1)
                img[:,it] = b

                it = it + 1
                f.seek(self.data_frame_length-self.end_byte_thick-1,1)
                #print "it:", it, "thick: ", b[0]
            f.close()

            it2 = it2 + 1

        #print img, img.shape
        self.emit(SIGNAL('scansLoaded(PyQt_PyObject)'), [img,dist])