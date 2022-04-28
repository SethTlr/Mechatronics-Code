import cv2
import os
import time

class Cam:
    def __init__(self, thresh_RGB, thresh_corridor, corridor_filter):

        self.RGBthresh = thresh_RGB
        self.thresh_corridor = thresh_corridor
        self.filter = corridor_filter
        self.cam = cv2.VideoCapture(1)
        if not self.cam.isOpened():
            raise IOError("Cannot open webcam")

    def Pic(self):

        ret, frame = self.cam.read(1)
        return frame

    def pipeline(self, img):

        img = self.threshold(img, self.RGBthresh)
        corridors = self.find_corridors(self.thresh_corridor, 1, 2)
        objs = self.filter_corridors(coridors, self.filter)

        return 0

    def getItems(self):
        img = self.Pic()
        obj = self.pipeline(img)

        return obj

    def close(self):
        self.cam.release()

    def threshold(self, img, threshold):
        return[]

    def find_corridors(self, threshold, a, b):
        return []

    def filter_corridors(self, corridors, filter):
        return []

def main():
    temp = Cam([], [], [])
    picture = temp.Pic()
    cv2.imshow('Frame', picture)

    # stopping command
    while cv2.waitKey(20) & 0xFF != ord('d'):
        pass

    # thresh = [( rmin, rhigh), (gmin, gmax), (bmin, bmax)]

    temp.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
