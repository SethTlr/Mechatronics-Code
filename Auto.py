import time
from imageRead import Cam
from PID import PID


Img_x_Size = 1280
Img_y_Size = 720


def One_Green(max_distance_cap, main_objs):
    (x, y), area, color = main_objs["green"]
    error = 0
    if x > 0:
        error = (x * 2)
    if x > max_distance_cap:
        error = -x
    return error


def One_Red(max_distance_cap, main_objs):
    (x, y), area, color = main_objs["red"]
    error = 0
    if x > 0:
        error = -(x * 2)
    if x > max_distance_cap:
        error = x
    return error


def Both(max_distance_cap, main_objs):
    # [(center-x, center-y), area, color]
    # x, y relative to top left of screen
    (Rx, Ry), Ra, Rc = main_objs["red"]
    (Gx, Gy), Ga, Gc = main_objs["green"]

    error = 0
    # assume red and green
    dis = Rx+Gx
    error = dis/2

    return error


def auto(joy, motor, max_motor_speed, max_offset):
    cam_image = Cam()

    Kp = 1
    Kd = 0
    Ki = 0

    # setup
    pid = PID(Kp, Kd, Ki, max_offset)

    last = False


    while True:
        #  vars --------------------------------------------------------------------------------------------------------

        # positive error is turing to the right
        error = 0

        # 1/10 total image size
        default_offset_res = 10

        # one bouie
        max_distance_cap = (Img_x_Size / default_offset_res) * 3

        # --------------------------------------------------------------------------------------------------------------

        # find objects CV
        # center_x, center_y is from center of screen
        # returns [[pos" = (center_x, center_y), area, color], [(center_x, center_y), area, color]]
        objects = cam_image.getItems()

        # check if done
        if last and len(objects) == 0:
            break
        elif len(objects) == 0:
            last = True
            time.sleep(1)  # sleep half a second
        else:
            last = False

        # caculate error value

        main_objs = {"red": None, "green": None}
        for obj in objects:
            (x, y), area, color = obj
            # first item for color
            if main_objs[color] is None:
                main_objs[color] = obj

            else:
                # sort by area
                if main_objs[color]["area"] < area:
                    main_objs[color] = obj

        #transfrom x,y to reative to boat
        for obj in main_objs:
            (x,y) = obj[0]
            x = x-(Img_x_Size/2)
            y = y-(Img_y_Size/2)
            obj[0] = (x, y)

        # only found red objects
        if main_objs["green"] is None:
            error = (max_distance_cap, main_objs)

        # only found red objects
        elif main_objs["red"] is None:
            error = One_Green(max_distance_cap, main_objs)

        else:  # found one of each
            error = Both(max_distance_cap, main_objs)

        # PID
        turn_gain = pid.correct(error)

        # run main section
        motor.run(max_motor_speed, turn_gain)