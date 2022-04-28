import time
from MotorControl import MotorContol
from PID import PID
from imageRead import cam
from Tele import tele

# from imageRead import get_Items

max_speed = 2048
ratio_of_turn = 0.25  # 0 to 1

max_offset = max_speed * ratio_of_turn
max_motor_speed = max_speed - max_offset

Img_x_Size = 300
Img_y_Size = 300


# temp delete later
# will import from imageRead.py
def get_Image_Objects():
    center_x, center_y, area, color = 0
    return [{"pos": (center_x, center_y), "area": area, "color": color}, {"pos": (center_x, center_y), "area": area, "color": color}]


def auto():
    Left_Motor_Pin = 12
    Right_Motor_Pin = 13

    Kp = 1
    Kd = 0
    Ki = 0

    # setup
    pid = PID(Kp, Kd, Ki, max_offset)
    motors = MotorContol(max_motor_speed, max_offset, Left_Motor_Pin, Right_Motor_Pin)

    last = False

    cam_image = cam()

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
        objects =
        # center_x, center_y is from center of screen
        # returns [[pos" = (center_x, center_y), area, color], [(center_x, center_y), area, color]]
        objects = get_Image_Objects()

        # check if done
        if last and len(objects) == 0:
            break
        elif len(objects) == 0:
            last = True
            time.sleep(0.5)  # sleep half a second
        else:
            last = False

        # caculate error value
        if len(objects) == 1: # one boyie found
            default_error_offset = Img_x_Size / default_offset_res
            (x, y), area, color = objects[0]
            if color == "red":  # red is on left side of channel
                error = default_error_offset
            else:  # Green is on right side of channel
                error = -default_error_offset

        else: # many found
            main_objs = {"red":[], "green":[]}
            for obj in objects:
                (x, y), area, color = obj
                # first item for color
                if len(main_objs[color]) == 0:
                    main_objs[color] = obj

                else:
                    # sort by area
                    if main_objs[color]["area"] < area:
                        main_objs[color] = obj

                if not bool(main_objs["red"]):  # only found green objects
                    (x_red, y_red), area_red, color_red = main_objs["red"]
                    if x_red > 0:
                        error = -(x_red*2)
                    if x_red > max_distance_cap:
                        error =

                elif not bool(main_objs["green"]):  # only found red objects
                    (x_green, y_green), area_green, color_green = main_objs["green"]

                else: # found one of each
                    (x_red, y_red), area_red, color_red = main_objs["red"]
                    (x_green, y_green), area_green, color_green = main_objs["green"]


        # PID
        turn_gain = pid.correct(error)

        # run main section
        motors.run(max_motor_speed, turn_gain)


def main():
    # tele
    if auto():
        print("yes")


if __name__ == "__main__":
    main()


# def forwardbackward(self, pin):
#     # read pin duration
#     # interpolate value to range
#     # check/cap value in range
#     # return value
#     return 0
#
#
# def leftright(self):
#     # read pin duration
#     # interpolate value to range
#     # check/cap value in range
#     # return value
#     return 0
#
#
# def kill(self):
#     # read in kill switch value
#     # if the value(s) read in are in a certain range, shut down
#     return 0
#
#
# def autonomous(self):
#     # read in autonomous/tele button value(s)
#     # if the value(s) are in their respiective ranges switch to auto or tele based on the range it is in
#     return 0
#
#
# def motorcontrol(self):
#     return 0
