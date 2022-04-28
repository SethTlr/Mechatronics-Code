import cv2
import os
import numpy as np

def pixcheck(r, g, b, rp, gp, bp, x, y, height, width, oogi):

    # set inverse of tolerance value for checking
    boogi = 1 / oogi

    # check that pixels are within bounds of frame
    if x < 0:
        return False

    if width - x < 0:
        return False

    if y < 0:
        return False

    if height - y:
        return False

    one = (pow((r + 1) / (g + 1), 2) / pow((rp + 1) / (gp + 1), 2) < oogi)
    two = (pow((r + 1) / (g + 1), 2) / pow((rp + 1) / (gp + 1), 2) > boogi)
    three = (pow((r + 1) / (b + 1), 2) / pow((rp + 1) / (bp + 1), 2) < oogi)
    four = (pow((r + 1) / (b + 1), 2) / pow((rp + 1) / (bp + 1), 2) > boogi)
    five = (pow((b + 1) / (g + 1), 2) / pow((bp + 1) / (gp + 1), 2) < oogi)
    six = (pow((b + 1) / (g + 1), 2) / pow((bp + 1) / (gp + 1), 2) > boogi)

    # long if statement that checks pixels ratios to each other
    if (one and two) and (three and four) and (five and six):
        return True
    return False


def recfun(r, g, b, rp, gp, bp, x, y, height, width, val, picArray, counter, area, color):

    if not pixcheck(r, g, b, rp, gp, bp, x, y, height, width, val):
        return

    # update usage
    picArray[x][y] = 1

    # add another pixel to the area value
    counter[area][0][color] = counter[area][0][color] + 1

    # update boundary pixels of rectangle if they provide new bounds
    if y > counter[area][1][color]:
        counter[area][1][color] = y

    if y < counter[area][2][color]:
        counter[area][2][color] = y

    if x > counter[area][3][color]:
        counter[area][3][color] = x

    if x > counter[area][4][color]:
        counter[area][4][color] = x

    # call recursive function in each direction
    recfun(r, g, b, rp, gp, bp, x, y + 1, height, width, val, picArray, counter, area, color)
    recfun(r, g, b, rp, gp, bp, x, y - 1, height, width, val, picArray, counter, area, color)
    recfun(r, g, b, rp, gp, bp, x + 1, y, height, width, val, picArray, counter, area, color)
    recfun(r, g, b, rp, gp, bp, x - 1, y, height, width, val, picArray, counter, area, color)

def getItems():

    # NOTE, pixel order is BGR
    buoyred = [30, 50, 200]
    buoygre = [30, 200, 50]

    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # read in individual frame
    ret, frame = cap.read()

    # find frame height and width
    height = frame.shape[0]
    width = frame.shape[1]

    # set 3D usage array, depth of two for checking two colors
    picArray = np.zeros((width, height))

    # set 3D counter array
    #   first dimension is to keep track of pixels per relevant area
    #   second dimension:
    #       0: pixel numbers
    #       1: highest pixel
    #       2: lowest pixel
    #       3: rightmost pixel
    #       4: leftmost pixel
    counter = np.zeros((2, 5, width*height))

    # brightness adjustment value
    brightnessVal = 0

    # arrays for green and red pixels
    rp = [0, 0]
    gp = [0, 0]
    bp = [0, 0]

    rp[0] = buoyred[2] + brightnessVal
    gp[0] = buoyred[1] + brightnessVal
    bp[0] = buoyred[0] + brightnessVal

    rp[1] = buoygre[2] + brightnessVal
    gp[1] = buoygre[1] + brightnessVal
    bp[1] = buoygre[0] + brightnessVal

    # start the pixel area counting at the zero position
    area = 0

    # run for loop that continues through entire frame
    for y in range(height - 1):
        for x in range(width - 1):

            # start checking if usage array denotes unchecked pixel
            if picArray[x][y] == 0:

                # update usage array
                picArray[x][y] = 1

                # read in current pixel's RGB values
                r = frame[y][x][2]
                g = frame[y][x][1]
                b = frame[y][x][0]

                # check if this pixel is close to target shade of red
                tval = pixcheck(r, g, b, rp[0], gp[0], bp[0], x, y, height, width, 1.5)

                if tval:

                    # set initial far point values
                    counter[0][1][area] = y
                    counter[0][2][area] = y
                    counter[0][3][area] = x
                    counter[0][4][area] = x

                    # recursively find entire area of red
                    recfun(r, g, b, rp, gp, bp, x, y, height, width, 1.5, picArray, counter, area, 0)

                    # increment area position after checking entire area recursively
                    area = area + 1

                # do the above checks but for the relevant green shade
                tval = pixcheck(r, g, b, rp[1], gp[1], bp[1], x, y, height, width, 1.5)

                if tval:
                    picArray[x][y] = 1
                    area = area + 1
                    counter[1][1][area] = y
                    counter[1][2][area] = y
                    counter[1][3][area] = x
                    counter[1][4][area] = x

                    recfun(r, g, b, rp, gp, bp, x, y, height, width, 1.5, picArray, counter, area, 1)

    list_red = np.zeros((width * height))
    list_gre = np.zeros((width * height))

    for z in range( width * height ):
        list_red[z] = counter[0][0][z]
        list_gre[z] = counter[1][0][z]

    max_red = np.where(list_red == np.amax(list_red))
    max_gre = np.where(list_gre == np.amax(list_gre))

    red_center_x = (counter[0][3][max_red] - counter[0][4][max_red]) / 2
    red_center_x = red_center_x + counter[0][4][max_red]

    gre_center_x = (counter[1][3][max_gre] - counter[1][4][max_gre]) / 2
    gre_center_x = gre_center_x + counter[1][4][max_gre]

    red_center_y = (counter[0][1][max_red] - counter[0][2][max_red]) / 2
    red_center_y = red_center_y + counter[0][2][max_red]

    gre_center_y = (counter[1][1][max_gre] - counter[1][2][max_gre]) / 2
    gre_center_y = gre_center_y + counter[1][2][max_gre]

    # send in gre_center_x/gre_center_y and red_center_x/red_center_y
    green = ([gre_center_x, gre_center_y], 'G')
    red = ([red_center_x, red_center_y]), 'R')

    items = [green, red]

    return items

    cap.release()