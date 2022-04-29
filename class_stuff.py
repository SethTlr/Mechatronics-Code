import cv2
import time
import numpy as np


class Cam:
    def __init__(self, cam_num, thresh_BGR, thresh_corridor, corridor_filter):

        self.thresh_BGR = thresh_BGR
        self.thresh_corridor = thresh_corridor
        self.filter = corridor_filter
        self.cam_num = int(cam_num)
        self.cam = cv2.VideoCapture(self.cam_num)
        if not self.cam.isOpened():
            raise IOError("Cannot open webcam")

    def Pic(self):
        ret, frame = self.cam.read(self.cam_num)
        return frame

    def pipeline(self, img):
        origonal_img = img
        img = cv2.blur(img, (7, 7), cv2.BORDER_DEFAULT)
        img = self.threshold(img)
        corridors = self.find_corridors(img)
        objs = self.filter_corridors(corridors)
        objs = self.find_color(origonal_img, objs)

        return objs

    def getItems(self):
        img = self.Pic()
        obj = self.pipeline(img)
        return obj

    def close(self):
        self.cam.release()

    def threshold(self, img):
        # used to print debug info to screen
        # should be False by Default
        debug = False

        if debug:
            cv2.imshow("Pre_Threshold", img)

        (B, G, R) = cv2.split(img)

        (b_low, b_high) = self.thresh_BGR["blue"]
        (g_low, g_high) = self.thresh_BGR["green"]
        (r_low, r_high) = self.thresh_BGR["red"]

        mask_b = cv2.inRange(B, b_low, b_high)
        mask_g = cv2.inRange(G, g_low, g_high)
        mask_r = cv2.inRange(R, r_low, r_high)

        full_mask = mask_b + mask_g + mask_r

        if debug:
            cv2.imshow("mask_b", mask_b)
            cv2.imshow("mask_g", mask_g)
            cv2.imshow("mask_r", mask_r)
            cv2.imshow("mask_full", full_mask)

        return full_mask

    def find_corridors(self, threshold):
        # used to print debug info to screen
        # should be False by Default
        debug = False

        a, b = self.thresh_corridor
        if debug:
            cv2.imshow("pre_threshold_img", threshold)
            print(f"Find_Corridors: A: {a}, B: {b}")

        contours, hierarchy = cv2.findContours(threshold, a, b)

        if debug:
            threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)
            threshold = cv2.drawContours(threshold, contours, -1, (0, 255, 0), 3)
            print(f"contours: {len(contours)}")
            cv2.imshow("threshold_img", threshold)
            # threshold img, contours list, -1 = all contours, color (r,g,b), thickness of line pixels

        return contours

    def filter_corridors(self, contours):
        debug = False

        contours_filter = self.filter
        amin, amax = contours_filter["area"]
        angleMin, angleMax = contours_filter["angle"]
        whMin, whMax = contours_filter["whRatio"]

        if debug:
            print(f"Area [Min: {amin}, Max: {amax}]\n"
                  f"Angle [Min: {amin}, Max: {angleMax}]\n"
                  f"wh [Min: {whMin}, Max: {whMax}]\n"
                  f"Contours: {len(contours)}\n"
                  f"epsilon: {contours_filter['epsilon']}")

        # This code simplifies the contour to be more like a rectangle
        for contour in contours:
            # epsilon is an accuracy parameter
            # It's the maximum distance from contour to approximated contour
            epsilon = contours_filter["epsilon"] * cv2.arcLength(contour, True)
            contour = cv2.approxPolyDP(contour, epsilon, True)

        if debug:
            img = self.Pic()
            img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
            cv2.imshow("epsilon image", img)

        objs = []

        # This code filters the contours by area, w to h ratio, and angle
        for contour in contours:
            (center_x, center_y), (w, h), angle = cv2.minAreaRect(contour)
            area = w * h
            if amin < area < amax and whMin < w / h < whMax:
                if angleMin < angle < angleMax:
                    objs.append({"pos": (center_x, center_y), "area": area, "color": "unknowen"})

        return objs

    def find_color(self, img, objs):
        debug = False

        (w, h, _) = img.shape

        if debug:
            cv2.imshow("Picker", img)
            print(img.shape)

        for obj in objs:
            # x and y are center locations
            if debug:
                print(f"Obj: {obj}")

            (x, y) = obj["pos"]
            # bounding
            x, y = int(x), int(y)
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x >= w:
                x = w-1
            if y >= h:
                y = h-1

            # get BGR
            (b, g, r) = (img[x, y])
            if r > b and r > g:
                color = "red"
            elif g > b and g > r:
                color = "green"
            else:
                color = "unknowen"

            obj["color"] = color

        return objs


def main():

    red = (192, 255)
    green = (50, 140)
    blue = (0, 105)

    thresh_BGR = {"red": red, "green": green, "blue": blue}
    Thresh_Contour = (cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # epsilon is an accuracy parameter
    # It's the maximum distance from contour to approximated contour
    # 0.1 represents 10% of arc lenght fit
    Contour_Filter = {"area": (1, 255),
                      "angle": (0, 255),
                      "whRatio": (0, 255),
                      "epsilon": 0.1}

    temp = Cam(1, thresh_BGR, Thresh_Contour, Contour_Filter)

    picture = temp.Pic()
    cv2.imshow('Frame', picture)
    cv2.imwrite("test.jpg", picture)

    # full test
    objs = temp.getItems()
    print(objs)

    # stopping command
    while cv2.waitKey(20) & 0xFF != ord('d'):
        pass

    # thresh = [( rmin, rhigh), (gmin, gmax), (bmin, bmax)]

    temp.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


# node:
# i tested the code it works we will have to play with rgb values and
# area, angle, wh as well as fix the findColor funtion